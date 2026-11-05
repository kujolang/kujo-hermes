"""Verify the real native CLI preserves policy and unrelated configuration."""
import argparse,json,os,pathlib,subprocess,tempfile
p=argparse.ArgumentParser();p.add_argument('--host',required=True);p.add_argument('--python',required=True);p.add_argument('--sources',required=True);p.add_argument('--kujo',required=True);a=p.parse_args()
root=pathlib.Path(__file__).resolve().parents[3];e=root/'demo/square/evidence'
with tempfile.TemporaryDirectory(prefix='kujo-native-setup-') as temp:
 home=pathlib.Path(temp);(home/'plugins').mkdir();(home/'plugins/kujo-hermes').symlink_to(root,target_is_directory=True)
 workspace=home/'repo';workspace.mkdir();subprocess.run(['git','init','-q',str(workspace)],check=True)
 cfg={'plugins':{'enabled':['kujo-hermes'],'isolation':'in_process','entries':{'kujo-hermes':{'settings':{'denied_abilities':['kujo.eval.suite.run'],'profile':'review','timeout_seconds':19}}}},'approvals':{'mode':'manual'},'display':{'show_reasoning':False}}
 file=home/'config.yaml';file.write_text(json.dumps(cfg));env=dict(os.environ,HERMES_HOME=str(home),PYTHONPATH=a.host,HERMES_ENABLE_PROJECT_PLUGINS='0')
 command=[a.python,'-m','hermes_cli.main','kujo','setup','--sources',str(pathlib.Path(a.sources).resolve()),'--kujo-bin',str(pathlib.Path(a.kujo).resolve()),'--trust-workspace',str(workspace)]
 before=file.read_bytes();dry=subprocess.run(command+['--dry-run'],env=env,capture_output=True,text=True);assert dry.returncode==0,dry.stderr;assert file.read_bytes()==before
 real=subprocess.run(command,env=env,capture_output=True,text=True);assert real.returncode==0,real.stderr
 # Read through the same native writer/parser runtime, not a separate YAML dependency.
 read=subprocess.check_output([a.python,'-c','import json; from hermes_cli.config import require_readable_config_before_write as read; print(json.dumps(read()))'],env=env,text=True)
 final=json.loads(read);s=final['plugins']['entries']['kujo-hermes']['settings']
 assert s['denied_abilities']==['kujo.eval.suite.run'] and s['profile']=='review' and s['timeout_seconds']==19
 assert s['trusted_workspaces']==[str(workspace.resolve())]
 assert final['approvals']==cfg['approvals'] and final['display']==cfg['display']
 repeat=subprocess.run(command,env=env,capture_output=True,text=True);assert repeat.returncode==0,repeat.stderr
 file.write_text('plugins: [not: valid\n');broken=file.read_bytes()
 invalid=subprocess.run(command+['--dry-run'],env=env,capture_output=True,text=True);assert invalid.returncode!=0;assert file.read_bytes()==broken
 (e/'setup-verification.json').write_text(json.dumps({'ok':True,'host':a.host,'tests':['actual native dry run leaves configuration unchanged','actual source setup saves exact workspace','denied Ability and existing profile preserved','unrelated native configuration preserved','pinned-source rerun succeeds','malformed config rejected without overwrite'],'test_workspace':'temporary Git fixture; removed after test'},indent=2)+'\n')
 print('PASS six native setup checks')
