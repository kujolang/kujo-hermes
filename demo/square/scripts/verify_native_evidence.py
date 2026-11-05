"""Assert actual host and setup results used by this release video."""
import json,pathlib
r=pathlib.Path(__file__).resolve().parents[1]
for name in ['hermes-host-e2e.json','hermes-in-process-e2e.json','hermes-python314-e2e.json']:
 d=json.loads((r/'evidence'/name).read_text());assert d['unload_verified'];assert len(d['approvals'])>=3
 results=[x['result'] for x in d['results']]
 assert any(x.get('total')==51 for x in results)
 assert sum(bool(x.get('verified')) for x in results)>=6
 assert any(x.get('blocked') for x in results)
 assert results[-1].get('ok') is False and 'missing.spec.yml' in results[-1].get('blocked','')
assert json.loads((r/'evidence/setup-verification.json').read_text())['ok']
d=json.loads((r/'evidence/public-doctor.json').read_text());assert d['ok'] and d['runtime_compatible'] and len(d['capabilities'])==51
assert 'Setup complete.' in (r/'evidence/setup.cast').read_text()
print('PASS native setup, 51 catalog bindings, three actual host workflows, permissions, receipt verification and cleanup')
