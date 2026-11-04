#!/usr/bin/env python3
"""Optional live PackWrite generation through the native execution service."""
import argparse,json,pathlib,sys,tempfile
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from kujo_hermes.config import Config
from kujo_hermes.service import Service
p=argparse.ArgumentParser();p.add_argument('--sources',required=True);p.add_argument('--kujo',required=True);p.add_argument('--model',required=True);args=p.parse_args()
root=pathlib.Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='kujo-hermes-packwrite-live-') as tmp:
 workspace=pathlib.Path(tmp)/'repo'; workspace.mkdir(); (workspace/'MEGA_PROMPT.md').write_text((root/'MEGA_PROMPT.md').read_text())
 cfg=Config(ecosystem_root=str(pathlib.Path(args.sources).resolve()),kujo_bin=str(pathlib.Path(args.kujo).resolve()),trusted_workspaces=(str(workspace),),profile='full',timeout_seconds=240)
 service=Service(cfg,pathlib.Path(tmp)/'state',lambda *a,**k:{'approved':True})
 result=service.execute('kujo.packwrite.pack.init',{'prompt_file':'MEGA_PROMPT.md','provider':'local','model':args.model},str(workspace))
 print(json.dumps(result,indent=2),flush=True)
 artifact={'kind':'live model generation through canonical PackWrite; test-only approval callback','model':args.model,'result':result}
 if result['ok']:
  assert (workspace/'agent/MASTER.md').is_file()
  verified=service.execute('kujo.packwrite.pack.validate',{},str(workspace)); assert verified['ok'],verified
  artifact['validation']=verified
 (root/'evidence/live-packwrite.json').write_text(json.dumps(artifact,indent=2)+'\n');service.close()
 if not result['ok']: sys.exit(1)
