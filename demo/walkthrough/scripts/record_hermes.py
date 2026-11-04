"""Launch the actual Hermes CLI; asciinema records the PTY, including approval prompts."""
import argparse,os,pathlib,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('shot',choices=['discover','checks','eval']);p.add_argument('--host',default='/tmp/kujo-hermes-host');p.add_argument('--python',default='/Users/robertdevore/.hermes/hermes-agent/venv/bin/python');args=p.parse_args()
root=pathlib.Path(__file__).resolve().parents[3];workspace=pathlib.Path('/tmp/kujo-hermes-video-20261104').resolve()
queries={
'discover':'Call kujo_discover with limit 50 and no query filter. From the returned catalog, list the Ability IDs for ShipCheck, PackWrite summary, Spec validate and Eval run. Keep the reply under 70 words.',
'checks':f'Validate my specification and summarize my task context in {workspace}. Call kujo_inspect with ability=kujo.spec.contract.validate, then kujo_execute with ability=kujo.spec.contract.validate, input={{"file":"task.spec.json"}}, workspace={workspace}. Next call kujo_inspect with ability=kujo.packwrite.pack.summary, then kujo_execute with that ability, input={{}}, workspace={workspace}. These are Ability IDs, not tool names. Report actual validation and phase count in under 80 words.',
'eval':f'Run my checks in {workspace}. First call kujo_inspect with ability=kujo.eval.suite.run. Then call kujo_execute with ability=kujo.eval.suite.run, input={{"config":"eval.json"}}, workspace={workspace}. Wait for human approval. Retrieve the returned receipt_id with kujo_receipts. Report passed and failed test counts and whether the receipt verified in under 90 words.'}
env=os.environ.copy();env.update(HERMES_HOME=str(root/'.local/video/home'),PYTHONPATH=args.host,TERM='xterm-256color',COLUMNS='100',LINES='24')
command=[args.python,args.host+'/cli.py','--model','qwen3.5:hermes-demo','--provider','local-demo','--base_url','http://127.0.0.1:11434/v1','--api_key','local-placeholder','--toolsets','kujo','--ignore_rules','--reasoning','none','--max_turns','12','--run_budget','600','--query',queries[args.shot],'--oneshot']
if args.shot=='eval': command.remove('--oneshot')
raise SystemExit(subprocess.call(command,env=env,cwd=workspace))
