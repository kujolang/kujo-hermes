"""Preserve an actual completed Eval run before its artifacts are overwritten."""
import argparse,json,pathlib,shutil
p=argparse.ArgumentParser();p.add_argument('stage',choices=['before','after']);a=p.parse_args()
root=pathlib.Path(__file__).resolve().parents[3];run=root/'.local/checkout-recording';out=root/'demo/checkout-video/evidence/run';out.mkdir(exist_ok=True)
records=[]
for path in (run/'home/plugin-data/kujo-hermes').rglob('*.json'):
 try:v=json.loads(path.read_text())
 except ValueError:continue
 if v.get('ability')=='kujo.eval.suite.run' or v.get('ability_id')=='kujo.eval.suite.run': records.append((path,v))
if not records:raise SystemExit('No actual Eval receipt yet')
path,v=max(records,key=lambda x:x[1].get('completed_at_ms',0))
expected=(2,1) if a.stage=='before' else (3,0)
data=v['result']['structured']['data'];assert (data['passed'],data['failed'])==expected,data
shutil.copy2(path,out/(a.stage+'-receipt.json'))
shutil.copytree(run/'workspace',out/(a.stage+'-snapshot'),ignore=shutil.ignore_patterns('.git','__pycache__'))
print(a.stage,v['receipt_id'],expected)
