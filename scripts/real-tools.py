#!/usr/bin/env python3
"""Real canonical CLI verification. Approval callback is a test seam, not Hermes E2E."""
import argparse, json, pathlib, shutil, subprocess, sys, tempfile, time
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from kujo_hermes.config import Config
from kujo_hermes.service import Service
p=argparse.ArgumentParser(); p.add_argument('--sources',required=True); p.add_argument('--kujo',required=True); p.add_argument('--output',default='evidence/real-tools.json'); args=p.parse_args()
root=pathlib.Path(__file__).resolve().parents[1]; sources=pathlib.Path(args.sources).resolve()
with tempfile.TemporaryDirectory(prefix='kujo-hermes-real-') as temp:
 workspace=pathlib.Path(temp)/'repo'; workspace.mkdir()
 for name,text in {'README.md':'# Hermes integration fixture\n','LICENSE':'MIT\n','VERSION':'0.1.0\n','CHANGELOG.md':'# Changes\n','hello.kujo':'print("Hello Hermes")\n','failure.log':'Example failure without secrets\n'}.items(): (workspace/name).write_text(text)
 shutil.copytree(root/'agent',workspace/'agent')
 shutil.copy(sources/'spec/examples/basic.spec.yml',workspace/'task.spec.yml')
 shutil.copy(sources/'dispatch/examples/workflows/plugin-echo.json',workspace/'workflow.json')
 (workspace/'eval.json').write_text(json.dumps({'name':'hermes-real','tests':[{'name':'readme exists','check':'file_exists','params':{'path':'README.md'}},{'name':'output value','check':'output_contains','params':{'command':'printf verified-hermes','expected':'verified-hermes'}}]}))
 (workspace/'loop.yml').write_text('objective: "Verify Hermes integration"\nmax_iterations: 1\nmax_no_progress: 1\neval_gates:\n  - id: fixture\n    command: "test -f README.md"\n    required: true\ncommit:\n  enabled: false\n  push: false\n')
 for command in [['git','init','-q'],['git','add','.'],['git','-c','user.name=Kujo Test','-c','user.email=test@example.invalid','commit','-qm','fixture']]: subprocess.run(command,cwd=workspace,check=True)
 (workspace/'README.md').write_text('# Hermes integration fixture\n\nChange for review.\n')
 shutil.copy(sources/'workcell/examples/hello/workcell.json',workspace/'workcell.json')
 shutil.copy(sources/'tribunal/examples/product-decision.md',workspace/'decision.md')
 shutil.copy(sources/'lens/examples/flows/login.json',workspace/'lens-flow.json')
 (workspace/'example.txt').write_text('hello')
 (workspace/'howl.json').write_text(json.dumps({'project':{'name':'Hermes'},'cards':[{'id':'hello','title':'Hello','file':'example.txt','language':'text'}]}))
 (workspace/'kennel.toml').write_text('[package]\nname = "hermes-fixture"\nversion = "0.1.0"\n[dependencies]\n')
 (workspace/'redact-policy.yaml').write_text('schemaVersion: redact-policy/v1\nname: hermes-test\nperson_names: role-preserve\ncompany_names: placeholder\ncustomer_names: placeholder\nproduct_names: placeholder\nemails: placeholder\nphone_numbers: remove\npayment_details: remove\napi_keys: remove\ndomains: placeholder\nexact_dates: date-generalize\nmoney_amounts: range\nlaunch_strategy: generalize\npreserve_task_structure: true\nwrite_entity_map: false\nai_assist: false\n')
 (workspace/'.muzzle/manifests').mkdir(parents=True)
 (workspace/'.muzzle/workflows').mkdir(parents=True)
 shutil.copy(sources/'muzzle/examples/build-check/manifests/build-check.json',workspace/'.muzzle/manifests/build-check.json')
 shutil.copy(sources/'muzzle/examples/build-check/workflows/build-check.sh',workspace/'.muzzle/workflows/build-check.sh')
 for product in ('dossier','versionseal'):
  result=subprocess.run([str(pathlib.Path(args.kujo).resolve()),'run',str(sources/product/(product+'.kujo')),'--interpreter','--','init','--state',str(workspace/('.'+product)),'--json'],cwd=workspace,capture_output=True,text=True)
  assert result.returncode==0,result.stdout+result.stderr
 subprocess.run([str(pathlib.Path(args.kujo).resolve()),'run',str(sources/'fence/fence.kujo'),'--interpreter','--','init'],cwd=workspace,capture_output=True,check=True)
 (workspace/'examples/research-report/sources').mkdir(parents=True)
 (workspace/'examples/research-report/sources/source.md').write_text('Hermes native workflow evidence.')
 (workspace/'knowledge').mkdir(); (workspace/'knowledge/hermes.md').write_text('Kujo Hermes validates repository specifications and preserves execution receipts.')
 (workspace/'simple-workflow.json').write_text(json.dumps({'id':'hermes-timestamp','name':'Hermes timestamp','input_schema':{'type':'dict'},'tools':['timestamp_tool'],'steps':[{'id':'stamp','name':'Timestamp','type':'tool','tool_name':'timestamp_tool','input_from':['input'],'output_key':'stamp'},{'id':'report','name':'Report','type':'report','input_from':['stamp'],'output_key':'final_output'}],'output_schema':{'type':'dict'}}))
 config=Config(ecosystem_root=str(sources),kujo_bin=str(pathlib.Path(args.kujo).resolve()),trusted_workspaces=(str(workspace),),profile='full',timeout_seconds=45)
 service=Service(config,pathlib.Path(temp)/'state',lambda *a,**kw:{'approved':True})
 calls=[('kujo.ability.catalog.list',{}),('kujo.shipcheck.repository.scan',{}),('kujo.patchbrief.changes.summarize',{}),('kujo.changebucket.changes.measure',{}),('kujo.spec.contract.validate',{'file':'task.spec.yml'}),('kujo.packwrite.pack.validate',{}),('kujo.packwrite.pack.summary',{}),('kujo.eval.suite.run',{'config':'eval.json'}),('kujo.scout.repository.inspect',{}),('kujo.scent.context.pack',{'task':'Inspect integration','dry_run':True}),('kujo.concord.artifacts.scan',{}),('kujo.dispatch.workflow.validate',{'workflow_file':'workflow.json'}),('kujo.casefile.failure.capture',{'log_file':'failure.log'}),('kujo.runledger.runs.start',{'provider':'local','model':'test','task':'Hermes verification'}),('kujo.runledger.runs.report',{}),('kujo.workflows.loop.run',{'config':'loop.yml'}),('kujo.runtime.version.inspect',{}),('kujo.runtime.source.check',{'file':'hello.kujo'}),('kujo.runtime.source.run',{'file':'hello.kujo'}),('kujo.ability.receipts.list',{})]
 calls.extend([
 ('kujo.hermes.lint.execute',{'file':'hello.kujo'}),
 ('kujo.hermes.format.execute',{'file':'hello.kujo'}),
 ('kujo.hermes.lsp.diagnostics.execute',{'file':'hello.kujo'}),
 ('kujo.hermes.lsp.complete.execute',{'file':'hello.kujo','line':1,'column':3}),
 ('kujo.hermes.mcp.make.execute',{}),
 ('kujo.fence.architecture.check',{}),
 ('kujo.rag.knowledge.ingest',{'ingest_path':'knowledge'}),
 ('kujo.rag.knowledge.query',{'question':'What does Kujo Hermes validate?'}),
 ('kujo.dispatch.workflow.run',{'topic':'Hermes evidence','workflow_file':'simple-workflow.json'}),
 ('kujo.kennel.project.validate',{}),('kujo.kennel.dependencies.install',{}),
 ('kujo.redact.document.scan',{'file':'example.txt','policy':'redact-policy.yaml'}),
 ('kujo.redact.document.sanitize',{'file':'example.txt','policy':'redact-policy.yaml','output_file':'sanitized.txt'}),
 ('kujo.versionseal.records.validate',{}),('kujo.tribunal.proposal.validate',{'file':'decision.md'}),
 ('kujo.tribunal.review.mock',{'file':'decision.md','panel':'executioner-only'}),
 ('kujo.dossier.records.validate',{}),('kujo.dossier.records.report',{}),
 ('kujo.howl.showcase.validate',{}),('kujo.howl.showcase.render',{'format':'html'}),
 ('kujo.lens.flow.validate',{'flow_file':'lens-flow.json'}),
 ('kujo.workcell.definition.validate',{'file':'workcell.json'}),
 ('kujo.workcell.definition.inspect',{'file':'workcell.json'}),
 ('kujo.muzzle.workflow.run',{'workflow':'build-check'})])
 results=[]
 for ability,data in calls:
  result=service.execute(ability,data,str(workspace)); results.append(result)
  print(ability,result['status'],json.dumps(result.get('error')),flush=True)
  if result['ok']:
   structured=result.get('result',{}).get('structured',{})
   if ability=='kujo.shipcheck.repository.scan': assert structured['tool']=='shipcheck' and len(structured['checks'])>0
   if ability=='kujo.packwrite.pack.summary': assert structured['phase_count']==7
   if ability=='kujo.spec.contract.validate': assert structured['valid'] is True
   if ability=='kujo.eval.suite.run': assert structured['data']['passed']==2 and structured['data']['failed']==0
   if ability=='kujo.patchbrief.changes.summarize': assert any(f['path']=='README.md' for f in structured['files'])
   if ability=='kujo.scout.repository.inspect': assert list((workspace/'.kujo/scout').rglob('scan_manifest.json'))
   if ability=='kujo.workflows.loop.run': assert 'Verdict: success' in result['result']['stdout']
  if result['ok'] and ability=='kujo.runledger.runs.start':
   import re
   match=re.search(r'Started run:\s*(\S+)',result['result']['stdout'])
   if match: results.append(service.execute('kujo.runledger.runs.finish',{'run_id':match.group(1),'status':'pass','verdict':'Verified'},str(workspace)))
 for r in results:
  receipt=service.receipts(r['receipt_id'],12000); assert receipt['verified']
 artifact={'kind':'real canonical CLI integration; explicit test approval callback','runtime':service.doctor()['runtime_version'],'results':results,'all_receipts_verified':True}
 pathlib.Path(args.output).write_text(json.dumps(artifact,indent=2)+'\n')
 service.close()
 if not all(r['ok'] for r in results): sys.exit(1)
