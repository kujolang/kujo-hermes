"""Subprocess initialization and deeply nested output failure coverage."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

from kujo_hermes.config import Config
from kujo_hermes.process import run, terminate
from kujo_hermes.service import Service


class FailureBoundaryTests(unittest.TestCase):
    def test_setup_failures_reap_child_and_close_pipes(self):
        original = subprocess.Popen
        for target in ('selectors.DefaultSelector', 'os.set_blocking'):
            with self.subTest(target=target):
                children = []
                def spawn(*args, **kwargs):
                    proc = original(*args, **kwargs)
                    children.append(proc)
                    return proc
                try:
                    with patch('kujo_hermes.process.subprocess.Popen', side_effect=spawn), \
                         patch('kujo_hermes.process.'+target, side_effect=OSError('setup failed')):
                        with self.assertRaisesRegex(OSError, 'setup failed'):
                            run([sys.executable, '-c', 'import time; time.sleep(60)'], '.', {}, 2, 1024, threading.Event())
                    proc = children[0]
                    self.assertIsNotNone(proc.poll(), 'child leaked after setup failed')
                    self.assertTrue(proc.stdout.closed)
                    self.assertTrue(proc.stderr.closed)
                finally:
                    # Also clean the deliberately failing baseline implementation.
                    for proc in children:
                        terminate(proc)
                        proc.stdout.close()
                        proc.stderr.close()

    def test_deep_output_retains_raw_evidence_and_failure_receipt(self):
        for depth in (128, 129, 2000):
            with self.subTest(depth=depth), tempfile.TemporaryDirectory() as temp:
                service = Service(Config(profile='full', trusted_workspaces=(temp,)),
                                  Path(temp)/'state', lambda *a, **k: {'approved': True})
                self.addCleanup(service.close)
                item = copy.deepcopy(service.catalog.get('kujo.runtime.version.inspect'))
                item.update(extension=True, operation='custom', binding={'argv':[
                    sys.executable, '-c', 'print("["*'+str(depth)+'+"0"+"]"*'+str(depth)+')']})
                item['definition']['output_schema'] = {}
                service.catalog.entries[item['definition']['id']] = item
                result = service.execute(item['definition']['id'], {}, temp)
                if depth==128:
                    self.assertTrue(result['ok'],result)
                    self.assertTrue(service.receipts(result['receipt_id'])['verified'])
                    continue
                self.assertFalse(result['ok'])
                self.assertIn('receipt_id', result)
                page = service.receipts(result['receipt_id'])
                self.assertTrue(page['verified'])
                receipt = json.loads(page['text'])
                self.assertEqual(receipt['result']['stdout'], '['*depth+'0'+']'*depth+'\n')
                self.assertEqual(receipt['result']['exit_code'], 0)
                self.assertEqual(receipt['error']['type'], 'RecursionError')
