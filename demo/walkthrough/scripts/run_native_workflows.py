"""Capture real operator-driven Hermes registry calls; preserve native approval prompts.
Run under the real Hermes Python environment with PYTHONPATH pointing at its source.
These are actual canonical executions, not mocked model messages or GUI history.
"""
import json,os,pathlib,sys,time,shutil
root=pathlib.Path(__file__).resolve().parents[3]
workspace=pathlib.Path('/tmp/kujo-hermes-video-20261104').resolve()
os.environ.update(HERMES_HOME=str(root/'.local/video/home'),HERMES_INTERACTIVE='1',HERMES_ENABLE_PROJECT_PLUGINS='0')
from hermes_cli.plugins import get_plugin_manager,resolve_pre_tool_block
from tools.registry import registry
from tools.approval_context import set_hermes_interactive_context,reset_hermes_interactive_context
out=root/'demo/walkthrough/evidence/v5-workflows';out.mkdir(exist_ok=True)
shutil.copy(root.parent/'dispatch/examples/workflows/custom-review.json',workspace/'review-workflow.json')
token=set_hermes_interactive_context(True);manager=get_plugin_manager();manager.discover_and_load()
records=[]
def call(label,name,args):
 print('\n'+label+' — '+name,flush=True)
 blocked=resolve_pre_tool_block(name,args,session_id='kujo-hermes-video-v5')
 if blocked: raise RuntimeError(blocked)
 result=registry.dispatch(name,args)
 if isinstance(result,str):result=json.loads(result)
 record={'label':label,'tool':name,'arguments':args,'result':result,'capture_mode':'operator-driven actual Hermes native registry; no model simulation','captured_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
 (out/(label+'.json')).write_text(json.dumps(record,indent=2)+'\n');records.append(record)
 print(json.dumps({'ok':result.get('ok'),'status':result.get('status'),'receipt_id':result.get('receipt_id'),'verified':result.get('verified')},indent=2),flush=True)
 return result
try:
 call('discovery','kujo_discover',{'limit':100})
 call('inspection','kujo_inspect',{'ability':'kujo.eval.suite.run'})
 for label,ability,data in [('spec','kujo.spec.contract.validate',{'file':'task.spec.json'}),('packwrite','kujo.packwrite.pack.summary',{}),('shipcheck','kujo.shipcheck.repository.scan',{}),('dispatch','kujo.dispatch.workflow.validate',{'workflow_file':'review-workflow.json'}),('scout','kujo.scout.repository.inspect',{}),('eval','kujo.eval.suite.run',{'config':'eval.json'})]:
  result=call(label,'kujo_execute',{'ability':ability,'input':data,'workspace':str(workspace)})
  assert result.get('ok'),result
  receipt=call(label+'-receipt','kujo_receipts',{'receipt_id':result['receipt_id'],'limit':12000});assert receipt.get('verified')
finally:
 manager.unload();reset_hermes_interactive_context(token)
 (out/'index.json').write_text(json.dumps({'records':[r['label'] for r in records],'workspace':str(workspace),'host':'Hermes v0.22.7','unload_completed':True},indent=2)+'\n')
