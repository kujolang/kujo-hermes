#!/usr/bin/env python3
"""Optional real service verification, with owned temporary processes and state."""
import argparse,json,os,pathlib,signal,socket,subprocess,sys,tempfile,time,urllib.request
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from kujo_hermes.config import Config
from kujo_hermes.service import Service
p=argparse.ArgumentParser(); p.add_argument('--sources',required=True); p.add_argument('--kujo',required=True); args=p.parse_args()
sources=pathlib.Path(args.sources).resolve(); binary=str(pathlib.Path(args.kujo).resolve()); results=[]
with tempfile.TemporaryDirectory(prefix='kujo-hermes-services-') as temp:
 root=pathlib.Path(temp); workspace=root/'repo'; workspace.mkdir(); (workspace/'index.html').write_text('<!doctype html><html lang="en"><title>Hermes fixture</title><h1>Real Lens verification</h1></html>')
 with socket.socket() as s: s.bind(('127.0.0.1',0)); port=s.getsockname()[1]
 env={'PATH':'/usr/local/bin:/usr/bin:/bin','HOME':str(root),'WDG_HOST':'127.0.0.1','WDG_PORT':str(port),'WDG_DB_PATH':str(root/'watchdog.db'),'WDG_API_AUTH_MODE':'off'}
 with open(root/'watchdog.log','w') as log:
  server=subprocess.Popen([binary,'run',str(sources/'watchdog/dashboard_server.kujo'),'--interpreter'],cwd=sources/'watchdog',env=env,stdout=log,stderr=log,start_new_session=True)
  service=Service(Config(ecosystem_root=str(sources),kujo_bin=binary,trusted_workspaces=(str(workspace),),profile='full'),root/'state',lambda *a,**k:{'approved':True})
  try:
   for i in range(50):
    try:
     with urllib.request.urlopen('http://127.0.0.1:'+str(port)+'/healthz',timeout=1) as r:
      if r.status==200: break
    except Exception: time.sleep(.1)
   for id,data in [('kujo.watchdog.service.health',{'url':'http://127.0.0.1:'+str(port)}),('kujo.watchdog.telemetry.record',{'url':'http://127.0.0.1:'+str(port),'name':'hermes-real-verification'})]:
    result=service.execute(id,data,str(workspace)); results.append(result); print(id,result,flush=True)
  finally:
   if server.poll() is None:
    try: os.killpg(server.pid,signal.SIGKILL)
    except PermissionError: server.kill()
   server.wait(); service.close()
 pathlib.Path('evidence/watchdog-startup.txt').write_text((root/'watchdog.log').read_text())
 pathlib.Path('evidence/service-tools.json').write_text(json.dumps({'kind':'real canonical Watchdog service; no mock server','results':results},indent=2)+'\n')
 if not all(r['ok'] for r in results): sys.exit(1)
