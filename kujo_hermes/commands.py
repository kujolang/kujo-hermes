"""Hermes-owned routing to canonical CLIs; no host-plugin imports."""
from pathlib import Path
import json
import re
import shutil
from .config import contained

# Canonical entrypoints, verified against source checkouts (docs/provenance.json).
ENTRYPOINTS={name:name+'.kujo' for name in ('scout','scent','patchbrief','changebucket','shipcheck','fence','dispatch','runledger','concord','casefile','muzzle','kennel','redact','versionseal','packwrite','tribunal','dossier','howl','lens')}
ENTRYPOINTS.update({'eval':'main.kujo','rag':'main.kujo'})
PATH_FIELDS={'file','config','workflow_file','flow_file','manifest','prompt_file','log_file','policy','state_dir','ledger_dir','output_dir','output_file','audit_dir','storage_dir','ingest_path'}
OUTPUT_FIELDS={'output_dir','output_file','audit_dir','storage_dir','ledger_dir'}

def plan(item, data, workspace, config):
    source=item.get('source'); op=item.get('operation'); d=dict(data)
    cwd=Path(contained(workspace,d.get('path','.'),True))
    for key in PATH_FIELDS & d.keys():
        d[key]=contained(cwd,d[key],key not in OUTPUT_FIELDS)
    root=Path(config.ecosystem_root)/source if source else None
    binary=shutil.which(config.kujo_bin)
    if item.get('extension'):
        # Each token expands one named field; never a shell or format expression.
        argv=[]
        for token in item['binding']['argv']:
            if re.fullmatch(r'\{[a-z_]+\}',token):
                key=token[1:-1]
                if key=='workspace': value=str(cwd)
                else: value=d[key]
                if isinstance(value,(dict,list)): value=json.dumps(value,separators=(',',':'))
                argv.append(str(value))
            else: argv.append(token)
        if not Path(argv[0]).is_file(): raise FileNotFoundError('Missing extension executable')
        return argv,cwd,{}
    if op in ('catalog','receipts','watchdog','watchdog_record'): return [],cwd,{}
    if not binary: raise FileNotFoundError('Kujo runtime missing: install Kujo >=1.6,<2 and configure kujo_bin')
    env={'KUJO':binary,'KUJO_BIN':binary}
    def val(key,default=None): return str(d.get(key,default))
    def opt(key,flag): return [flag,val(key)] if key in d else []
    def toggle(key,flag,default=False): return [flag] if d.get(key,default) else []
    def output(key,default): return d.get(key,contained(cwd,default))
    args=[]
    if op=='scout': args=[str(cwd),'-o',output('output_dir','.kujo/scout')]+toggle('quick','--quick',True)
    elif op=='scent': args=['pack','--task',d['task'],'--budget',val('budget',12000),'--target','generic','--json']+(['--dry-run'] if d.get('dry_run') else ['--out',contained(cwd,'.kujo/scent'),'--format','both'])
    elif op=='patchbrief': args=['summarize','--format',val('format','json')]
    elif op=='changebucket': args=['--json','--repo',str(cwd),'--base',val('base','HEAD')]+opt('max_files','--max-files')+opt('max_churn','--max-churn')
    elif op=='shipcheck': args=['scan','--dir',str(cwd),'--format','json']
    elif op=='fence': args=['check','--format','json']+toggle('changed_only','--changed-only')+toggle('baseline','--baseline')
    elif op=='spec':
        entry=root/'scripts/spec'
        if not entry.is_file(): raise FileNotFoundError('Missing canonical spec/scripts/spec')
        return ['/bin/bash',str(entry),'validate',d['file'],'--json']+toggle('strict','--strict'),cwd,env
    elif op=='eval': args=['run',d['config'],'--output-dir',output('output_dir','.kujo/eval'),'--json']
    elif op=='runledger': args=['report']+opt('task','--task')
    elif op=='runledger_start': args=['start','--provider',d['provider'],'--model',d['model'],'--task',d['task'],'--repo',str(cwd),'--ledger',output('ledger_dir','.runledger')]+opt('prompt_file','--prompt')
    elif op=='runledger_finish': args=['finish',d['run_id'],'--status',d['status'],'--verdict',d['verdict'],'--repo',str(cwd),'--ledger',output('ledger_dir','.runledger')]+opt('notes','--notes')
    elif op=='dispatch': args=['validate','--workflow-file',str(Path(d['workflow_file']).relative_to(cwd)),'--json']
    elif op=='dispatch_run':
        value=json.loads(d.get('input_json','{}'))
        if not isinstance(value,dict): raise ValueError('input_json must encode an object')
        # Canonical Dispatch consent remains in force; no --yes or prompt bypass.
        args=['run',d['topic'],'--workflow-file',str(Path(d['workflow_file']).relative_to(cwd)),'--input-json',json.dumps(value),'--output-root',output('output_dir','.kujo/dispatch'),'--non-interactive']
    elif op=='rag': args=['query','--question',d['question'],'--namespace',val('namespace','default')]
    elif op=='rag_ingest': args=['ingest','--path',d['ingest_path'],'--namespace',val('namespace','default'),'--recursive',str(d.get('recursive',True)).lower()]
    elif op=='concord': args=['scan','--dir',str(cwd),'--format','json']
    elif op=='casefile': args=['capture','--name',val('name','hermes-failure'),'--from-log',d['log_file'],'--output-dir',output('output_dir','.casefile/cases'),'--format','json']+opt('notes','--notes')
    elif op=='muzzle':
        env['MUZZLE_ROOT']=str(root)
        if d.get('approve_network'): raise PermissionError('Network approval must be granted through canonical Muzzle policy, not an agent boolean')
        args=['run',d['workflow'],*d.get('args',[]),'--json','--policy','enforce','--validate-args']
    elif op=='kennel_validate': args=['validate','--project-dir',str(cwd)]
    elif op=='kennel_install': args=['install','--project-dir',str(cwd)]+toggle('allow_mutable_ref','--allow-mutable-ref')
    elif op in ('redact_scan','redact_sanitize'):
        args=[op.split('_')[1],d['file'],'--policy',d['policy'],'--audit-dir',output('audit_dir','.redact')]
        if op=='redact_sanitize': args+=['--out',d['output_file'],'--fail-on-risk',val('fail_on_risk','high')]
    elif op=='versionseal_validate': args=['validate','--state',(d['state_dir'] if 'state_dir' in d else contained(cwd,'.versionseal',True)),'--json']+opt('record_id','--id')
    elif op in ('packwrite_validate','packwrite_summary'):
        args=[op.split('_')[1],'--output',str(Path(output('output_dir','agent')).relative_to(cwd)),'--json']+opt('config','--config')
    elif op=='packwrite_init': args=['init',d['prompt_file'],'--provider',d['provider'],'--model',d['model'],'--output',str(Path(output('output_dir','agent')).relative_to(cwd))]+opt('config','--config')+toggle('overwrite','--overwrite')
    elif op=='tribunal_validate': args=['validate',d['file'],'--json']
    elif op=='tribunal_review': args=['review',d['file'],'--panel',val('panel','fast-two-model'),'--mock','--storage-dir',output('storage_dir','.tribunal')]
    elif op in ('dossier_validate','dossier_report'):
        args=[op.split('_')[1],'--state',(d['state_dir'] if 'state_dir' in d else contained(cwd,'.dossier',True)),'--json']
        if op=='dossier_report': args+=['--limit',val('limit',100)]
    elif op=='howl_validate': args=['validate','--manifest',(d['manifest'] if 'manifest' in d else contained(cwd,'howl.json',True))]
    elif op=='howl_render': args=['render','--manifest',(d['manifest'] if 'manifest' in d else contained(cwd,'howl.json',True)),'--out',output('output_dir','dist/howl'),'--format',val('format','all')]
    elif op=='lens_flow_validate': args=['flow',d['flow_file'],'--validate','--json']; cwd=root
    elif op=='lens_check':
        from .network import loopback_url
        if not d.get('allow_external'): loopback_url(d['url'])
        args=['check',d['url'],'--out',output('output_dir','.lens/runs/hermes'),'--json','--timeout',val('timeout_seconds',30)]+toggle('quick','--quick',True)+toggle('html','--html',True)+toggle('allow_external','--allow-external'); cwd=root
    elif op.startswith('workcell_'):
        entry=root/'bin/workcell'
        args=[op.split('_')[1]]
        if 'file' in d: args+=['--file',d['file']]
        if op=='workcell_run': args+=['--repo',str(cwd),'--no-pull','--summary']
        elif op=='workcell_inspect': args+=['--summary']
        if not entry.is_file(): raise FileNotFoundError('Missing workcell/bin/workcell')
        return [str(entry),*args],cwd,env
    elif op=='loop':
        entry=root/'loop-engineering/scripts/run-workflow.sh'
        if not entry.is_file(): raise FileNotFoundError('Missing canonical Loop harness')
        return ['/bin/bash',str(entry),'--config',d['config']],cwd,env
    elif op=='runtime_version': return [binary,'--version'],cwd,env
    elif op=='runtime_check': return [binary,'check',d['file']],cwd,env
    elif op=='runtime_run': return [binary,'run',d['file'],'--interpreter'],cwd,env
    else: raise ValueError('No verified canonical binding for '+str(op))
    entry=root/ENTRYPOINTS[source]
    if not entry.is_file(): raise FileNotFoundError('Missing canonical source: '+str(entry)+'; configure ecosystem_root or run scripts/install-sources.py')
    return [binary,'run',str(entry),'--interpreter','--',*args],cwd,env
