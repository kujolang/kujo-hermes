"""Check the real host's stored tool results; no mocked execution or exit-code-only proof."""
import hashlib,json,pathlib
r=pathlib.Path(__file__).resolve().parents[1]
def results(shot,name):
 d=json.loads((r/'evidence'/(shot+'-session.json')).read_text())
 cast=r/'evidence/casts'/(shot+'.cast')
 assert hashlib.sha256(cast.read_bytes()).hexdigest()==d['source_cast_sha256']
 return [json.loads(m['content']) for m in d['messages'] if m.get('tool_name')==name]
catalog=results('discover','kujo_discover');assert any(d['total']==51 for d in catalog)
ids={a['id'] for d in catalog for a in d['abilities']}
assert {'kujo.shipcheck.repository.scan','kujo.spec.contract.validate','kujo.eval.suite.run','kujo.packwrite.pack.summary'}<=ids
for shot in ('checks','eval'):
 for d in results(shot,'kujo_execute'):
  assert not d.get('error'),d
  assert d.get('ok') is not False,d
print('Catalog and actual execution envelopes verified.')
checks={d['ability_id']:d['result']['structured'] for d in results('checks','kujo_execute')}
assert set(checks)=={'kujo.spec.contract.validate','kujo.packwrite.pack.summary'}
assert checks['kujo.spec.contract.validate']=={'valid':True,'errors':[],'warnings':[]}
assert checks['kujo.packwrite.pack.summary']['phase_count']==7
assert checks['kujo.packwrite.pack.summary']['missing_files']==[]
verified=results('eval','kujo_receipts');assert verified and verified[-1]['verified'] is True
assert json.loads((r/'evidence/receipt-verification.json').read_text())==verified[-1]
receipt=json.loads(verified[-1]['text']);checksum=receipt.pop('receipt_digest')
assert hashlib.sha256(json.dumps(receipt,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()==checksum
assert receipt['ability_id']=='kujo.eval.suite.run'
assert receipt['approval']['required'] and receipt['approval']['approved']
assert receipt['status']=='completed'
data=receipt['result']['structured']['data']
assert (data['passed'],data['failed'],data['total'])==(2,0,2)
assert all(test['passed'] for test in data['test_results'])
assert receipt['command'][1]=='run' and receipt['command'][2].endswith('/eval/main.kujo')
assert 'allowed once' in (r/'evidence/casts/eval.cast').read_text()
for path in (r/'evidence/receipts').glob('*.json'):
 d=json.loads(path.read_text());sha=d.pop('receipt_digest')
 assert hashlib.sha256(json.dumps(d,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()==sha
print('PASS: 51 bindings; Spec valid; PackWrite 7 phases; approved Eval 2/2; native receipt retrieval and all receipt hashes verified.')
