#!/usr/bin/env python3
import json,pathlib,sys,tempfile
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from kujo_hermes.service import Service
from kujo_hermes.config import Config
root=pathlib.Path(__file__).resolve().parents[1]; workspace=pathlib.Path(sys.argv[1]).resolve(); binary=pathlib.Path(sys.argv[2]).resolve()
with tempfile.TemporaryDirectory() as tmp:
 service=Service(Config(ecosystem_root=str(root.parent),kujo_bin=str(binary),profile='full',trusted_workspaces=(str(workspace),)),pathlib.Path(tmp)/'state',lambda *a,**k:{'approved':True})
 results=[]
 for ability,data in [('kujo.scout.repository.inspect',{}),('kujo.packwrite.pack.summary',{}),('kujo.spec.contract.validate',{'file':'task.spec.json'}),('kujo.eval.suite.run',{'config':'eval.json'}),('kujo.shipcheck.repository.scan',{})]:
  result=service.execute(ability,data,str(workspace)); results.append(result); assert result['ok'],result
 assert results[3]['result']['structured']['data']['passed']==2
 (root/'evidence/demo-verification.json').write_text(json.dumps({'kind':'real reproducible demo commands; no video recorded','results':results},indent=2)+'\n'); service.close()
print('PASS demo repository and five canonical operations')
