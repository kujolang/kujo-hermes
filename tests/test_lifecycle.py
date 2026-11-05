"""Failure and lifecycle regressions from the second hardening pass."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

from kujo_hermes.config import Config
from kujo_hermes.process import run
from kujo_hermes.service import Service


class LifecycleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.service = Service(Config(profile='full', trusted_workspaces=(str(self.root),)),
                               self.root/'state', lambda *a, **k: {'approved': True})
        self.addCleanup(self.service.close)

    def extension(self, operation='custom'):
        item = copy.deepcopy(self.service.catalog.get('kujo.runtime.version.inspect'))
        item.update(extension=True, operation=operation,
                    binding={'argv': [sys.executable, '-c', 'print("actual extension output")']})
        item['definition']['output_schema'] = {}
        self.service.catalog.entries[item['definition']['id']] = item
        return item['definition']['id']

    def test_cancelled_before_start_does_not_spawn(self):
        cancel = threading.Event()
        cancel.set()
        with patch('kujo_hermes.process.subprocess.Popen') as spawn:
            result = run(['/bin/echo', 'must not run'], self.root, {}, 1, 1024, cancel)
            spawn.assert_not_called()
        self.assertEqual(result['status'], 'cancelled')
        self.assertIsNone(result['exit_code'])

    def test_thread_start_failure_releases_execution_slots(self):
        ability = self.extension()
        with patch('kujo_hermes.service.threading.Thread.start', side_effect=RuntimeError('no thread')):
            for _ in range(5):
                result = self.service.execute(ability, {}, str(self.root), background=True)
                self.assertEqual(result['error']['message'], 'no thread')
                self.assertFalse(any(j['status']=='running' for j in self.service.jobs.values()))
                self.assertTrue(all(j['done'].is_set() for j in self.service.jobs.values()))
        self.assertTrue(self.service.execute(ability, {}, str(self.root))['ok'])

    def test_extension_cannot_be_misrouted_by_internal_operation(self):
        result = self.service.execute(self.extension('catalog'), {}, str(self.root))
        self.assertTrue(result['ok'], result)
        self.assertEqual(result['result']['stdout'], 'actual extension output\n')

    def test_receipt_sync_failure_leaves_no_partial_files(self):
        ability = self.extension()
        with patch('kujo_hermes.service.os.fsync', side_effect=OSError('disk failure')):
            result = self.service.execute(ability, {}, str(self.root))
        self.assertFalse(result['ok'])
        self.assertFalse(result['receipt_persisted'])
        self.assertEqual(list((self.root/'state/receipts').iterdir()), [])
        self.assertEqual(self.service.status(result['invocation_id']), result)

    def test_background_receipt_failure_remains_inspectable(self):
        ability = self.extension()
        with patch.object(self.service, 'finish', side_effect=OSError('receipt storage unavailable')):
            result = self.service.execute(ability, {}, str(self.root), background=True)
            job = self.service.jobs[result['invocation_id']]
            self.assertTrue(job['done'].wait(5))
        status = self.service.status(result['invocation_id'])
        self.assertEqual(status['status'], 'failed')
        self.assertFalse(status['receipt_persisted'])
        self.assertIn('storage unavailable', status['error']['message'])

    def test_receipt_not_visible_until_sync_completes(self):
        ability = self.extension()
        observed = []
        def inspect_visibility(fd):
            observed.extend((self.root/'state/receipts').glob('*.json'))
        with patch('kujo_hermes.service.os.fsync', side_effect=inspect_visibility):
            result = self.service.execute(ability, {}, str(self.root))
        self.assertEqual(observed, [])
        self.assertTrue(self.service.receipts(result['receipt_id'])['verified'])
