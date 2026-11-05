"""Behavioral regressions for the November 2026 hardening pass."""
import copy
import http.server
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

from kujo_hermes.config import Config
from kujo_hermes.evidence import artifact_inventory
from kujo_hermes.network import watchdog
from kujo_hermes.service import Service


class HardeningTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.service = Service(Config(profile='full', trusted_workspaces=(str(self.root),)),
                               self.root/'state', lambda *a, **k: {'approved': True})
        self.addCleanup(self.service.close)

    def execute(self, code, schema=None):
        item = copy.deepcopy(self.service.catalog.get('kujo.runtime.version.inspect'))
        item.update(extension=True, operation='custom', binding={'argv': [sys.executable, '-c', code]})
        item['definition']['output_schema'] = schema or {}
        self.service.catalog.entries[item['definition']['id']] = item
        return self.service.execute(item['definition']['id'], {}, str(self.root))

    def test_control_character_output_receipt_is_readable(self):
        result = self.execute('import sys; sys.stdout.write(chr(1)*300000)')
        self.assertTrue(result['ok'], result)
        page = self.service.receipts(result['receipt_id'], 12000)
        self.assertTrue(page['verified'])
        self.assertIsNotNone(page['next_offset'])

    def test_receipt_remains_readable_after_output_limit_reduction(self):
        result = self.execute('print("x"*100000)')
        service = Service(Config(max_output_bytes=1024), self.root/'state')
        self.addCleanup(service.close)
        self.assertTrue(service.receipts(result['receipt_id'])['verified'])

    def test_output_contract_failure_preserves_evidence(self):
        result = self.execute('import sys; print("42"); print("diagnostic", file=sys.stderr)',
                              {'type': 'object'})
        self.assertFalse(result['ok'])
        receipt = json.loads(self.service.receipts(result['receipt_id'])['text'])
        self.assertEqual(receipt['error']['type'], 'ValidationError')
        self.assertEqual(receipt['result']['structured'], 42)
        self.assertEqual(receipt['result']['stderr'], 'diagnostic\n')
        self.assertEqual(receipt['result']['exit_code'], 0)

    def test_large_invalid_output_has_bounded_error_and_retained_evidence(self):
        result = self.execute('print("x"*20000)', {'type': 'integer'})
        self.assertFalse(result['ok'])
        self.assertLessEqual(len(result['error']['message']), 8192)
        path = self.root/'state/receipts'/(result['receipt_id']+'.json')
        receipt = json.loads(path.read_text())
        self.assertEqual(receipt['result']['stdout'], 'x'*20000+'\n')
        self.assertTrue(self.service.receipts(result['receipt_id'])['verified'])

    def test_artifacts_follow_selected_subdirectory(self):
        for directory, text in [('nested/.kujo/scout', 'actual'), ('.kujo/scout', 'stale')]:
            target = self.root/directory
            target.mkdir(parents=True)
            (target/'report.json').write_text(text)
        for data in ({'path': 'nested'}, {'path': 'nested', 'output_dir': '.kujo/scout'}):
            result = artifact_inventory(self.root, data, 'scout')
            self.assertEqual([x['path'] for x in result['files']], ['nested/.kujo/scout/report.json'])
            self.assertEqual(result['bytes_hashed'], 6)

    def test_doctor_rejects_failed_version_command(self):
        binary = self.root/'kujo'
        binary.write_text('#!/bin/sh\necho kujo 1.8.0\nexit 17\n')
        binary.chmod(0o700)
        service = Service(Config(kujo_bin=str(binary)), self.root/'state')
        self.addCleanup(service.close)
        self.assertFalse(service.doctor()['runtime_compatible'])
        with self.assertRaises(RuntimeError):
            service.check_runtime()

    def test_watchdog_ignores_host_proxy_settings(self):
        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'{"ok":true}')

            def log_message(self, *args):
                pass

        server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with patch('urllib.request.getproxies', return_value={'http': 'http://127.0.0.1:1'}), \
                 patch('urllib.request.proxy_bypass', return_value=False):
                result = watchdog({'url': 'http://127.0.0.1:'+str(server.server_port)})
                self.assertTrue(result['body']['ok'])
        finally:
            server.shutdown()
            server.server_close()
            thread.join()
