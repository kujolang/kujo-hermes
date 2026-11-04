#!/usr/bin/env python3
"""Real Hermes loader, registry, approval gate, tools and unload. No mocked tools.
A test-only CLI callback supplies human decisions deterministically.
Run with --interactive to answer the actual approval prompts yourself.
"""
import argparse,json,os,pathlib,shutil,sys,tempfile,time
p=argparse.ArgumentParser(); p.add_argument('--sources',required=True); p.add_argument('--kujo',required=True); p.add_argument('--interactive',action='store_true'); p.add_argument('--live-model'); p.add_argument('--output',default='evidence/hermes-e2e.json'); p.add_argument('--isolation',default='in_process',choices=['in_process','host']); args=p.parse_args()
root=pathlib.Path(__file__).resolve().parents[1]; source=pathlib.Path(args.sources).resolve(); binary=pathlib.Path(args.kujo).resolve()
with tempfile.TemporaryDirectory(prefix='kujo-hermes-host-e2e-') as temp:
 home=pathlib.Path(temp); workspace=home/'workspace'; workspace.mkdir(); (workspace/'README.md').write_text('# Real Hermes engineering fixture\n')
 shutil.copytree(root/'agent',workspace/'agent'); shutil.copy(source/'spec/examples/basic.spec.yml',workspace/'task.spec.yml')
 (workspace/'eval.json').write_text(json.dumps({'name':'hermes-e2e','tests':[{'name':'README exists','check':'file_exists','params':{'path':'README.md'}}]}))
 (workspace/'loop.yml').write_text('objective: "Hermes real workflow"\nmax_iterations: 1\neval_gates:\n  - id: readme\n    command: "test -f README.md"\n    required: true\ncommit:\n  enabled: false\n')
 (home/'plugins').mkdir(); shutil.copytree(root,home/'plugins/kujo-hermes',ignore=shutil.ignore_patterns('.git','__pycache__','.venv','.local','evidence'))
 settings={'ecosystem_root':str(source),'kujo_bin':str(binary),'trusted_workspaces':[str(workspace)],'profile':'full','timeout_seconds':30}
 # JSON is a YAML subset. No dependency on the plugin's config parser.
 (home/'config.yaml').write_text(json.dumps({'plugins':{'enabled':['kujo-hermes'],'isolation':args.isolation,'entries':{'kujo-hermes':{'settings':settings}}},'approvals':{'mode':'manual','timeout':10}}))
 os.environ.update({'HERMES_HOME':str(home),'HERMES_BUNDLED_PLUGINS':str(home/'empty'),'HERMES_ENABLE_PROJECT_PLUGINS':'0','HERMES_INTERACTIVE':'1'})
 from hermes_cli.plugins import get_plugin_manager,resolve_pre_tool_block
 from tools.registry import registry
 from tools.approval_context import set_hermes_interactive_context,reset_hermes_interactive_context
 token=set_hermes_interactive_context(True)
 from tools.terminal_tool import set_approval_callback
 approvals=[]
 def human_decision(*a,**kw):
  decision=(home/'decision').read_text().strip()
  approvals.append({'decision':decision,'description':str(a)})
  return decision
 set_approval_callback(human_decision)
 manager=get_plugin_manager(); start=time.perf_counter(); manager.discover_and_load(); startup_ms=(time.perf_counter()-start)*1000
 results=[]
 def call(name,data,decision='once'):
  if args.interactive and name=='kujo_execute' and data.get('ability') in ('kujo.scout.repository.inspect','kujo.eval.suite.run','kujo.workflows.loop.run'):
   decision=input('Approval decision for '+data['ability']+' (once/deny): ').strip()
  (home/'decision').write_text(decision)
  blocked=resolve_pre_tool_block(name,data,session_id='hermes-real-test')
  if blocked: result={'ok':False,'blocked':blocked}
  else:
   result=registry.dispatch(name,data)
   if isinstance(result,str): result=json.loads(result)
  results.append({'tool':name,'args':data,'result':result}); return result
 discovered=call('kujo_discover',{'limit':100}); assert discovered['total']==51,discovered
 assert registry.get_entry('kujo_execute') is not None
 def execute(id,data={},decision='once'): return call('kujo_execute',{'ability':id,'input':data,'workspace':str(workspace)},decision)
 denied=execute('kujo.scout.repository.inspect',decision='deny'); assert not denied['ok']
 assert not (workspace/'.kujo/scout').exists()
 # The tools run through the actual host registration and gate, including a multi-step workflow.
 for id,data in [('kujo.scout.repository.inspect',{}),('kujo.packwrite.pack.summary',{}),('kujo.spec.contract.validate',{'file':'task.spec.yml'}),('kujo.eval.suite.run',{'config':'eval.json'}),('kujo.shipcheck.repository.scan',{}),('kujo.workflows.loop.run',{'config':'loop.yml'})]:
  result=execute(id,data); print(id,result.get('status'),result.get('receipt_id'),flush=True); assert result['ok'],result
  structured=result.get('result',{}).get('structured',{})
  if id=='kujo.packwrite.pack.summary': assert structured['phase_count']==7
  if id=='kujo.spec.contract.validate': assert structured['valid'] is True
  if id=='kujo.eval.suite.run': assert structured['data']['passed']==1 and structured['data']['failed']==0
  if id=='kujo.shipcheck.repository.scan': assert structured['tool']=='shipcheck' and structured['summary']['gate_passed']==0
  if id=='kujo.scout.repository.inspect': assert list((workspace/'.kujo/scout').rglob('scan_manifest.json'))
  if id=='kujo.workflows.loop.run': assert 'Verdict: success' in result['result']['stdout']
  receipt=call('kujo_receipts',{'receipt_id':result['receipt_id'],'limit':12000}); assert receipt['verified']
 failed=execute('kujo.spec.contract.validate',{'file':'missing.spec.yml'}); assert not failed['ok']
 if args.live_model:
  from run_agent import AIAgent
  agent=AIAgent(model=args.live_model,base_url='http://127.0.0.1:11434/v1',api_key='local-placeholder',provider='custom',api_mode='chat_completions',enabled_toolsets=['kujo'],max_iterations=8,quiet_mode=True,skip_context_files=True,skip_memory=True,skip_background_review=True,max_tokens=1800,run_budget_seconds=120)
  response=agent.run_conversation('Use the native Kujo tools to discover ShipCheck, inspect its schema, run it on '+str(workspace)+', then retrieve its receipt. Report the actual release blockers and receipt ID. Do not invoke other tools.')
  public_response={k:v for k,v in response.items() if k in ('final_response','messages','api_calls','completed','failed','partial','turn_exit_reason','model','provider','input_tokens','output_tokens')}
  public_response['messages']=[{k:v for k,v in m.items() if k not in ('reasoning','reasoning_content')} for m in response.get('messages',[])]
  (root/'evidence/live-hermes-model.json').write_text(json.dumps({'model':args.live_model,'response':public_response},indent=2,default=str)+'\n')
  messages=response.get('messages',[]) if isinstance(response,dict) else []
  calls=[c.get('function',{}).get('name') for m in messages for c in m.get('tool_calls',[])]
  for m in messages:
   for c in m.get('tool_calls',[]):
    if c.get('function',{}).get('name')=='tool_call':
     calls.extend(x['name'] for x in json.loads(c['function']['arguments'])['calls'])
  assert 'kujo_execute' in calls and 'kujo_receipts' in calls, calls
  tool_results=[json.loads(m['content']) for m in messages if m.get('role')=='tool']
  assert any(x.get('verified') is True and x.get('total_chars',0)>100 for x in tool_results)
  assert any(x.get('ability_id')=='kujo.shipcheck.repository.scan' and x.get('ok') for x in tool_results)
 manager.unload(); assert registry.get_entry('kujo_execute') is None
 reset_hermes_interactive_context(token)
 set_approval_callback(None)
 artifact={'hermes_source':str(pathlib.Path(__import__('hermes_cli.plugins',fromlist=['']).__file__).parents[1]),'isolation':args.isolation,'startup_ms':startup_ms,'approval_mode':'manual interactive transport' if args.interactive else 'test-only deterministic CLI human callback through real Hermes approval gate','approvals':approvals,'results':results,'unload_verified':True}
 pathlib.Path(args.output).write_text(json.dumps(artifact,indent=2)+'\n')
 print('PASS real Hermes load, discovery, denial, approval, canonical workflow, receipts, failure, unload')
