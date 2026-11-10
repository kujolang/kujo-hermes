"""Regression coverage for release-time confidentiality and resource contracts."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from kujo_hermes.config import Config
from kujo_hermes.resources import ROOT
from kujo_hermes.service import Service, redact


class ReleaseBoundaryTests(unittest.TestCase):
    def test_redacts_keys_without_losing_colliding_values(self):
        value = {'sensitive': 'first', '[REDACTED]': 'second', '[REDACTED]#2': 'third'}
        result = redact(value, ['sensitive'])
        self.assertNotIn('sensitive', json.dumps(result))
        self.assertEqual(sorted(result.values()), ['first', 'second', 'third'])
        self.assertEqual(redact(result, ['sensitive']), result)

    def test_secret_json_keys_are_removed_from_response_and_receipt(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            service = Service(Config(profile='full', trusted_workspaces=(temp,), secrets=('API_TOKEN',)),
                              root/'state', lambda *a, **k: {'approved': True},
                              lambda name: 'private-token-value')
            self.addCleanup(service.close)
            item = copy.deepcopy(service.catalog.get('kujo.runtime.version.inspect'))
            item.update(extension=True, binding={'argv': [sys.executable, '-c',
                'import os,json; print(json.dumps({os.environ["API_TOKEN"]:"evidence"}))']})
            item['definition']['output_schema'] = {}
            service.catalog.entries[item['definition']['id']] = item
            result = service.execute(item['definition']['id'], {}, temp)
            self.assertTrue(result['ok'], result)
            self.assertNotIn('private-token-value', json.dumps(result))
            receipt = service.receipts(result['receipt_id'])
            self.assertTrue(receipt['verified'])
            self.assertNotIn('private-token-value', receipt['text'])
            self.assertIn('evidence', receipt['text'])

    def test_runtime_resource_contract(self):
        for name in ('catalog/abilities.json', 'catalog/profiles.json', 'catalog/sources.lock.json',
                     'skills/kujo-engineering/SKILL.md', 'scripts/install-sources.py'):
            self.assertTrue((ROOT/name).is_file(), name)
