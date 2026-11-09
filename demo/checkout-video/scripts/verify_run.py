"""Check genuine model routing, unchanged checks and independently hashed results."""
import hashlib,json,pathlib,subprocess
root=pathlib.Path(__file__).resolve().parents[3];film=root/'demo/checkout-video';e=film/'evidence'
subprocess.run(['python3',str(root/'demo/checkout/verify.py'),str(e/'run')],check=True)
contract=json.loads((e/'run/contract-receipt.json').read_text());claimed=contract.pop('receipt_digest')
assert hashlib.sha256(json.dumps(contract,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()==claimed
assert contract['ability_id']=='kujo.spec.contract.validate' and contract['result']['structured']['valid']
s=json.loads((e/'visible-session.json').read_text());calls=[];results=[]
for m in s['messages']:
 if m.get('tool_calls'):
  value=m['tool_calls'];calls.extend(json.loads(value) if isinstance(value,str) else value)
 if m['role']=='tool':
  try:results.append(json.loads(m['content']))
  except (ValueError,TypeError):pass
functions=[c['function'] for c in calls];names=[f['name'] for f in functions]
assert any(r.get('ability_id')=='kujo.spec.contract.validate' and r.get('result',{}).get('structured',{}).get('valid') is True for r in results)
assert 'patch' in names or 'write_file' in names, 'Model must actually edit code'
for f in functions:
 if f['name'] in ('patch','write_file'):
  assert 'test_checkout.py' not in f['arguments'], 'Model must not rewrite tests'
ids=[json.loads((e/'run'/f'{stage}-receipt.json').read_text())['receipt_id'] for stage in ['before','after']]
retrieved=[json.loads(f['arguments']).get('receipt_id') for f in functions if f['name']=='kujo_receipts']
assert set(ids)<=set(retrieved), 'Model must retrieve both actual receipts'
assert 'kujo_discover' in names
before=(e/'run/before-snapshot/checkout.py').read_text();after=(e/'run/after-snapshot/checkout.py').read_text()
assert before!=after, 'Model must change the implementation; behavior is checked by the actual Eval receipts'
report={'ok':True,'model':s['model'],'session_id':s['session_id'],'native_tool_names':sorted(set(names)),'tool_call_count':len(calls),'receipts':ids,'actual_model_edit':True,'tests_unchanged':True,'independent_receipt_and_artifact_verification':True,'cast_sha256':hashlib.sha256((e/'checkout.cast').read_bytes()).hexdigest()}
(e/'run-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
