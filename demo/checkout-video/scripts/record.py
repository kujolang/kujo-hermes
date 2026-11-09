"""Record a genuine local-model Hermes session. Never applies the checkout fix."""
import argparse, json, os, pathlib, shutil, subprocess, sys
root=pathlib.Path(__file__).resolve().parents[3]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--run-dir',type=pathlib.Path,default=root/'.local/checkout-recording')
parser.add_argument('--host',type=pathlib.Path,default=root/'.local/hackathon/hermes')
parser.add_argument('--python',type=pathlib.Path)
args=parser.parse_args()
run=args.run_dir.resolve()
home=run/'home'; workspace=run/'workspace'
if not home.exists():
    shutil.copytree(root/'demo/checkout/fixture',workspace)
    subprocess.run(['git','init','-q',str(workspace)],check=True)
    subprocess.run(['git','add','.'],cwd=workspace,check=True)
    subprocess.run(['git','commit','-qm','demo: record checkout fixture before correction'],cwd=workspace,check=True)
    (home/'plugins').mkdir(parents=True)
    shutil.copytree(root,home/'plugins/kujo-hermes',ignore=shutil.ignore_patterns('.git','.local','.venv','__pycache__','demo','docs','evidence','.loop-engineering'))
    settings={'ecosystem_root':str(root/'.local/square/sources'),'kujo_bin':str(root/'.local/runtime/kujo'),'trusted_workspaces':[str(workspace)],'profile':'full','timeout_seconds':60}
    config={'_config_version':12,'sessions':{'auto_prune':False},'plugins':{'enabled':['kujo-hermes'],'isolation':'in_process','entries':{'kujo-hermes':{'settings':settings}}},'approvals':{'mode':'manual','timeout':300},'tools':{'tool_search':{'enabled':'off'}},'providers':{'checkout-local':{'api':'http://127.0.0.1:11434/v1','api_key':'local-placeholder','default_model':'qwen3.5:hermes-checkout64k','extra_body':{'reasoning_effort':'none'}}},'telemetry':{'shared_metrics':{'enabled':False,'send':False,'offer_version':2}}}
    (home/'config.yaml').write_text(json.dumps(config))
python=args.python or next(root.glob('.local/square/public-home/installs/7cc*/environments/c828*/venv/bin/python'))
host=args.host.resolve()
env=os.environ.copy();env.update(HERMES_HOME=str(home),PYTHONPATH=str(host),HERMES_BUNDLED_PLUGINS=str(home/'empty'),HERMES_ENABLE_PROJECT_PLUGINS='0',TERM='xterm-256color',COLUMNS='60',LINES='24',TERMINAL_CWD=str(workspace))
prompt=f'''Work in {workspace}. A $50 cart with a ten percent coupon costs $50.99, but free shipping must use the original subtotal. First inspect and execute kujo.spec.contract.validate with input {{"file":"task.spec.yml"}}. Then inspect and execute kujo.eval.suite.run with input {{"config":"eval.json"}}. These are Ability IDs for kujo_inspect and kujo_execute. Pass workspace to kujo_execute. Retrieve the Eval receipt using kujo_receipts. Report the actual failed check in under 70 words. STOP before changing any file; wait for my next message.'''
cmd=[str(python),str(host/'cli.py'),'--model','qwen3.5:hermes-checkout64k','--provider','checkout-local','--base_url','http://127.0.0.1:11434/v1','--api_key','local-placeholder','--toolsets','kujo,file','--reasoning','none','--max_turns','16','--run_budget','1200','--query',prompt]
raise SystemExit(subprocess.call(cmd,env=env,cwd=workspace))
