#!/usr/bin/env python3
"""Reproduce real native Hermes -> Spec/Eval -> receipts. No model or fake tool output.
Default approvals are interactive. --test-decisions is a clearly labelled test driver.
A fresh run directory is mandatory: reset by choosing a new --output directory.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sources', required=True)
    parser.add_argument('--kujo', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--test-decisions', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    workspace = output/'workspace'
    shutil.copytree(Path(__file__).parent/'fixture', workspace)
    subprocess.run(['git', 'init', '-q', str(workspace)], check=True)
    home = output/'hermes-home'
    (home/'plugins').mkdir(parents=True)
    shutil.copytree(root, home/'plugins/kujo-hermes', ignore=shutil.ignore_patterns(
        '.git', '.local', '.venv', '__pycache__', 'demo', 'evidence', 'docs', '.loop-engineering'))
    settings = {'ecosystem_root': str(Path(args.sources).resolve()),
                'kujo_bin': str(Path(args.kujo).resolve()),
                'trusted_workspaces': [str(workspace)], 'profile': 'full', 'timeout_seconds': 60}
    (home/'config.yaml').write_text(json.dumps({'plugins': {'enabled': ['kujo-hermes'],
        'isolation': 'in_process', 'entries': {'kujo-hermes': {'settings': settings}}},
        'approvals': {'mode': 'manual', 'timeout': 30}}))
    os.environ.update(HERMES_HOME=str(home), HERMES_BUNDLED_PLUGINS=str(home/'empty'),
                      HERMES_ENABLE_PROJECT_PLUGINS='0', HERMES_INTERACTIVE='1')
    from hermes_cli.plugins import get_plugin_manager, resolve_pre_tool_block
    from tools.registry import registry
    from tools.approval_context import set_hermes_interactive_context, reset_hermes_interactive_context
    from tools.terminal_tool import set_approval_callback
    approvals, calls = [], []
    decision = 'once'
    def approve(*a, **kw):
        answer = decision if args.test_decisions else input('Hermes approval (once/deny): ').strip()
        approvals.append({'choice': answer, 'mode': 'test callback' if args.test_decisions else 'interactive human'})
        return answer
    token = set_hermes_interactive_context(True)
    set_approval_callback(approve)
    manager = get_plugin_manager()
    def call(name, data):
        blocked = resolve_pre_tool_block(name, data, session_id='checkout-reproduction')
        result = {'ok': False, 'blocked': blocked} if blocked else registry.dispatch(name, data)
        if isinstance(result, str): result = json.loads(result)
        calls.append({'tool': name, 'input': data, 'result': result})
        return result
    def execute(ability, data):
        return call('kujo_execute', {'ability': ability, 'input': data, 'workspace': str(workspace)})
    def receipt(result, stage):
        parts, offset = [], 0
        while True:
            page = call('kujo_receipts', {'receipt_id': result['receipt_id'], 'offset': offset, 'limit': 12000})
            assert page['verified'], page
            parts.append(page['text'])
            offset = page['next_offset']
            if offset is None: break
        value = json.loads(''.join(parts))
        checksum = value.pop('receipt_digest')
        actual = hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()
        assert actual == checksum
        value['receipt_digest'] = checksum
        (output/(stage+'-receipt.json')).write_text(json.dumps(value, indent=2)+'\n')
        shutil.copytree(workspace, output/(stage+'-snapshot'), ignore=shutil.ignore_patterns('.git','__pycache__'))
        return value
    started = time.monotonic()
    try:
        manager.discover_and_load()
        found = call('kujo_discover', {'query': 'Eval'})
        assert any(x['id']=='kujo.eval.suite.run' for x in found['abilities'])
        spec = execute('kujo.spec.contract.validate', {'file': 'task.spec.yml'})
        assert spec['ok'] and spec['result']['structured']['valid'], spec
        receipt(spec, 'contract')
        if args.test_decisions:
            decision = 'deny'
            denied = execute('kujo.eval.suite.run', {'config': 'eval.json'})
            assert not denied['ok'] and not (workspace/'.kujo/eval').exists(), denied
            decision = 'once'
        print('BEFORE: $50 cart + 10% coupon should cost $45, not $50.99.', flush=True)
        failed = execute('kujo.eval.suite.run', {'config': 'eval.json'})
        before = receipt(failed, 'before')
        data = before['result']['structured']['data']
        assert data['passed']==2 and data['failed']==1, before
        failures = [x for x in data['test_results'] if not x['passed']]
        assert '5099 != 4500' in failures[0]['details']['stderr'], failures
        print(json.dumps({'phase':'before','passed':data['passed'],'failed':data['failed'],'receipt':failed['receipt_id']}), flush=True)
        if not args.test_decisions:
            input('Inspect the failure receipt. Press Enter to apply the disclosed one-line fixture correction. ')
        code = workspace/'checkout.py'
        text = code.read_text()
        assert 'shipping = 0 if discounted >= 5000 else 599' in text
        code.write_text(text.replace('shipping = 0 if discounted >= 5000 else 599',
                                     'shipping = 0 if subtotal_cents >= 5000 else 599'))
        print('FIX: use original subtotal for shipping eligibility. Tests remain unchanged.', flush=True)
        fixed = execute('kujo.eval.suite.run', {'config': 'eval.json'})
        after = receipt(fixed, 'after')
        data = after['result']['structured']['data']
        assert fixed['ok'] and data['passed']==3 and data['failed']==0, after
        assert (output/'before-snapshot/test_checkout.py').read_bytes()==(output/'after-snapshot/test_checkout.py').read_bytes()
        print(json.dumps({'phase':'after','passed':data['passed'],'failed':data['failed'],'receipt':fixed['receipt_id']}), flush=True)
    finally:
        manager.unload()
        reset_hermes_interactive_context(token)
        set_approval_callback(None)
    assert registry.get_entry('kujo_execute') is None
    (output/'run.json').write_text(json.dumps({'driver':'deterministic native Hermes workflow; correction applied by fixture driver, not LLM',
        'approval_mode':'test callback' if args.test_decisions else 'interactive human', 'calls':calls,
        'approvals':approvals,'duration_seconds':time.monotonic()-started,'unload_verified':True}, indent=2)+'\n')
    print('PASS: real failure, unchanged tests, real correction, independently checked receipt hashes, clean unload.', flush=True)

if __name__ == '__main__': main()
