#!/usr/bin/env python3
"""Exercise optional real browser/container tooling; report exact external blockers."""
import argparse,http.server,json,pathlib,sys,tempfile,threading
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from kujo_hermes.config import Config
from kujo_hermes.service import Service
p=argparse.ArgumentParser(); p.add_argument('--sources',required=True); p.add_argument('--kujo',required=True); p.add_argument('--browser-cache'); args=p.parse_args()
sources=pathlib.Path(args.sources).resolve(); root=pathlib.Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='kujo-hermes-optional-') as temp:
 workspace=pathlib.Path(temp)/'repo'; workspace.mkdir()
 import shutil,subprocess
 shutil.copy(sources/'workcell/examples/hello/workcell.json',workspace/'workcell.json')
 (workspace/'.gitignore').write_text('.lens/\n.workcell/\n')
 (workspace/'index.html').write_text('<!doctype html><html lang="en"><head><title>Hermes fixture</title></head><body><main><h1>Real browser evidence</h1></main></body></html>')
 for command in [['git','init','-q'],['git','add','.'],['git','-c','user.name=Test','-c','user.email=test@example.invalid','commit','-qm','fixture']]: subprocess.run(command,cwd=workspace,check=True)
 class Handler(http.server.SimpleHTTPRequestHandler):
  def __init__(self,*a,**kw): super().__init__(*a,directory=str(workspace),**kw)
  def log_message(self,*a): pass
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler); thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
 # Explicit operator browser-cache path, passed through the configured environment seam.
 cfg=Config(ecosystem_root=str(sources),kujo_bin=str(pathlib.Path(args.kujo).resolve()),trusted_workspaces=(str(workspace),),profile='full',timeout_seconds=45,secrets=('PLAYWRIGHT_BROWSERS_PATH',) if args.browser_cache else ())
 service=Service(cfg,pathlib.Path(temp)/'state',lambda *a,**k:{'approved':True},lambda name:args.browser_cache)
 results=[]
 try:
  for id,data in [('kujo.lens.page.check',{'url':'http://127.0.0.1:'+str(server.server_port)}),('kujo.workcell.runtime.doctor',{}),('kujo.workcell.definition.run',{'file':'workcell.json'})]:
   result=service.execute(id,data,str(workspace));results.append(result); print(id,result['status'],flush=True)
   if result['ok'] and id=='kujo.lens.page.check':
    receipt=json.loads(service.receipts(result['receipt_id'],12000)['text'])
    assert receipt['artifacts']['files'],'Real Lens must leave hashed artifacts'
 finally: server.shutdown();server.server_close();service.close()
 (root/'evidence/optional-tools.json').write_text(json.dumps({'kind':'real Lens browser and Workcell engine checks; external blockers retained','results':results},indent=2)+'\n')
