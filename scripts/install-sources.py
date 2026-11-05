#!/usr/bin/env python3
"""Explicit, source-only dependency installation. Never executes downloaded code."""
import argparse,json,pathlib,subprocess,shutil,tempfile
p=argparse.ArgumentParser(description=__doc__); p.add_argument('--destination',required=True); p.add_argument('--only',nargs='*'); p.add_argument('--dry-run',action='store_true'); args=p.parse_args()
root=pathlib.Path(__file__).resolve().parents[1]
lock=json.loads((root/'catalog/sources.lock.json').read_text())
known={item['name'] for item in lock['sources']}
if args.only and set(args.only)-known: p.error('Unknown source: '+str(set(args.only)-known))
destination=pathlib.Path(args.destination).expanduser().resolve()
for item in lock['sources']:
 if args.only and item['name'] not in args.only: continue
 target=destination/item['name']; print(item['name'],item['commit'],target,flush=True)
 if args.dry_run: continue
 if target.is_symlink(): raise SystemExit("Refusing symlink source destination: "+str(target))
 if target.exists():
  actual=subprocess.check_output(['git','-C',str(target),'rev-parse','HEAD'],text=True).strip()
  dirty=subprocess.check_output(['git','-C',str(target),'status','--porcelain'],text=True).strip()
  if actual!=item['commit'] or dirty: raise SystemExit('Refusing to overwrite changed or differently pinned source: '+str(target))
  continue
 destination.mkdir(parents=True,exist_ok=True)
 staging=pathlib.Path(tempfile.mkdtemp(prefix='.'+item['name']+'-',dir=destination))
 try:
  subprocess.run(['git','init','-q',str(staging)],check=True)
  subprocess.run(['git','-C',str(staging),'remote','add','origin',item['repository']],check=True)
  subprocess.run(['git','-C',str(staging),'fetch','--depth','1','origin',item['commit']],check=True,timeout=300)
  subprocess.run(['git','-C',str(staging),'checkout','--detach','FETCH_HEAD'],check=True)
  actual=subprocess.check_output(['git','-C',str(staging),'rev-parse','HEAD'],text=True).strip()
  if actual!=item['commit']: raise SystemExit('Source commit verification failed')
  if target.exists(): raise SystemExit('Source destination appeared during fetch; refusing to replace it')
  staging.rename(target)
 finally:
  if staging.exists(): shutil.rmtree(staging)
print('Sources ready. Install the official Kujo runtime separately; set ecosystem_root and kujo_bin in Hermes settings.')
