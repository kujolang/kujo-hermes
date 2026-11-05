"""Approval, lifecycle and evidence boundary for the native Hermes tools."""
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
import threading
import time
import uuid
from jsonschema import Draft202012Validator
from .catalog import Catalog, validate_input_size
from .commands import plan, ENTRYPOINTS
from .process import run
from .network import watchdog

# Independent of current subprocess settings; JSON escaping can expand output sixfold.
MAX_RECEIPT_BYTES = 32 * 1024 * 1024


def encoded(value): return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def digest(value): return hashlib.sha256(encoded(value)).hexdigest()

def redact(value, secrets=()):
    if isinstance(value,dict):
        return {k:('[REDACTED]' if re.fullmatch(r'(?:access[_-]?token|refresh[_-]?token|token|password|secret|api[_-]?key|authorization)',k,re.I) else redact(v,secrets)) for k,v in value.items()}
    if isinstance(value,list): return [redact(x,secrets) for x in value]
    if isinstance(value,str):
        for secret in secrets:
            if secret: value=value.replace(secret,'[REDACTED]')
        value=re.sub(r'(?i)(bearer\s+)[\w.\-]+',r'\1[REDACTED]',value)
        value=re.sub(r'(?i)((?:api[_-]?key|token|password|secret)\s*[=:]\s*)[^\s,;]+',r'\1[REDACTED]',value)
    return value

class Service:
    def __init__(self,config,data_dir,approve=None,get_secret=None):
        self.config=config; self.catalog=Catalog(config)
        self.data_dir=Path(data_dir).resolve(); self.approve=approve; self.get_secret=get_secret or (lambda name:None)
        self.jobs={}; self.lock=threading.RLock(); self.closed=False; self.runtime_cache=None

    def directory(self):
        self.data_dir.mkdir(parents=True,exist_ok=True,mode=0o700)
        receipts=self.data_dir/'receipts'
        if receipts.is_symlink(): raise PermissionError('Receipt directory must not be a symlink')
        receipts.mkdir(exist_ok=True,mode=0o700)
        return receipts

    def availability(self,item):
        source=item.get('source'); op=item.get('operation')
        if item.get('extension'):
            ready=Path(item['binding']['argv'][0]).is_file()
        elif not source or source=='watchdog': ready=True
        elif source=='kujo': ready=shutil.which(self.config.kujo_bin) is not None
        else:
            entry={'mcp':'mcp.kujo','spec':'scripts/spec','workcell':'bin/workcell','kujo-workflows':'loop-engineering/scripts/run-workflow.sh'}.get(source,ENTRYPOINTS.get(source,''))
            ready=bool(self.config.ecosystem_root) and (Path(self.config.ecosystem_root)/source/entry).is_file()
        return {'installed':ready,'dependency':source,'note':None if ready else 'Install canonical source and configure ecosystem_root'}

    def discover(self,query='',refresh=False,offset=0,limit=25):
        if refresh: self.catalog.refresh()
        entries=self.catalog.exposed(); matches=[]
        for k,v in entries.items():
            d=v['definition']
            if query.lower() not in (k+' '+d.get('title','')+' '+d['description']).lower(): continue
            matches.append({'id':k,'title':d.get('title',k),'effects':d['effects'],'approval_required':self.privileged(v),**self.availability(v)})
        return {'profile':self.config.profile,'total':len(matches),'abilities':matches[offset:offset+limit],'next_offset':offset+limit if offset+limit<len(matches) else None}

    def inspect(self,ability):
        item=self.catalog.get(ability)
        return {'definition':item['definition'],'definition_digest':item['digest'],'binding':item.get('binding',{'source':item.get('source'),'operation':item.get('operation')}),'approval_required':self.privileged(item),**self.availability(item)}

    def privileged(self,item):
        # Extension declarations never establish read-only authority.
        return bool(item.get('extension')) or any(e['kind']!='read' for e in item['definition']['effects'])

    def environment(self,extra):
        home=self.data_dir/'home'; home.mkdir(parents=True,exist_ok=True,mode=0o700)
        env={'PATH':'/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin','HOME':str(home),'LANG':'en_US.UTF-8','TMPDIR':str(home),'NO_COLOR':'1',**extra}
        # Host secret scope only. Never read a credential file or inherit the parent environment.
        for name in self.config.secrets:
            value=self.get_secret(name)
            if value: env[name]=value
        return env

    def execute(self,ability,input,workspace,background=False):
        validate_input_size(input)
        invocation=str(uuid.uuid4()); start=int(time.time()*1000)
        item=None; record={'schema':'kujo.hermes.receipt/v1','receipt_id':invocation,'invocation_id':invocation,
            'ability_id':ability,'workspace':str(workspace),'started_at_ms':start,'host':'hermes','status':'preflight',
            'approval':{'required':False,'approved':False},'input_digest':digest(input)}
        try:
            with self.lock:
                if self.closed: raise RuntimeError('Plugin is shutting down')
                if sum(j['status']=='running' for j in self.jobs.values())>=4: raise RuntimeError('At most four active executions')
            item=self.catalog.get(ability); data=self.catalog.inputs(item,input)
            root=self.config.workspace(workspace)
            if item.get('source') and item.get('source')!='watchdog' and not item.get('extension'):
                self.check_runtime()
            argv,cwd,extra=plan(item,data,root,self.config)
            record.update({'definition_digest':item['digest'],'ability_version':item['definition']['version'],
                'effects':item['definition']['effects'],'workspace':str(root),'command':argv,'cwd':str(cwd)})
            record['request_digest']=digest({'ability':item['digest'],'input':data,'workspace':str(root),'argv':argv})
            if self.privileged(item):
                record['approval']['required']=True
                if self.approve is None: raise PermissionError('Hermes human approval API unavailable')
                reason=json.dumps({'ability':ability,'workspace':str(root),'effects':item['definition']['effects'],
                    'command':argv,'request_digest':record['request_digest']},ensure_ascii=False)
                # Unique invocation grain prevents session/always grants applying to another request.
                decision=self.approve('kujo_execute',reason,rule_key='kujo:'+invocation+':'+record['request_digest'])
                if not isinstance(decision,dict) or decision.get('approved') is not True:
                    raise PermissionError('Hermes approval denied or unavailable')
                record['approval'].update({'approved':True,'id':invocation})
            cancel=threading.Event()
            with self.lock:
                if self.closed: raise RuntimeError('Plugin shut down during approval')
                if sum(j['status']=='running' for j in self.jobs.values())>=4: raise RuntimeError('Execution capacity reached')
                # Keep only active job objects; completed results live in receipts.
                self.jobs={k:j for k,j in self.jobs.items() if j['status']=='running'}
                self.jobs[invocation]={'status':'running','cancel':cancel,'thread':None,'done':threading.Event()}
            if background:
                thread=threading.Thread(target=self._perform,args=(item,data,argv,cwd,extra,cancel,record),daemon=True)
                with self.lock:
                    self.jobs[invocation]['thread']=thread
                    thread.start()
                return {'ok':True,'status':'running','invocation_id':invocation}
            return self._perform(item,data,argv,cwd,extra,cancel,record)
        except Exception as error:
            record.update({'status':'denied' if isinstance(error,PermissionError) else 'failed','error':{'type':type(error).__name__,'message':str(error)[:8192]}})
            with self.lock:
                job=self.jobs.get(invocation)
                if job:
                    job['status']='failed'
                    job['done'].set()
            return self.finish(record)

    def _perform(self,item,data,argv,cwd,extra,cancel,record):
        secrets=[]
        try:
            env=self.environment(extra); secrets=[env[k] for k in self.config.secrets if k in env]
            # Extension bindings always execute their reviewed argv, even if they
            # carry a copied internal operation name.
            op=None if item.get('extension') else item.get('operation')
            if op=='catalog': result=self.discover(limit=100)
            elif op=='receipts': result=self.receipts(limit=data.get('limit',20))
            elif op in ('watchdog','watchdog_record'): result=watchdog(data,op=='watchdog_record',env.get('WDG_API_AUTH_TOKEN',''))
            else:
                outcome=run(argv,cwd,env,self.config.timeout_seconds,self.config.max_output_bytes,cancel)
                result=dict(outcome)
                try:
                    result['structured']=json.loads(outcome['stdout'])
                    result['stdout_digest']=hashlib.sha256(outcome['stdout'].encode()).hexdigest()
                    result.pop('stdout',None)
                except ValueError: pass
                record['status']='completed' if outcome['status']=='completed' and outcome['exit_code']==0 else ('failed' if outcome['status']=='completed' else outcome['status'])
                if record['status']!='completed': record['error']={'type':record['status'],'message':'Canonical command did not complete successfully'}
            if record['status']=='preflight': record['status']='completed'
            # Preserve command evidence even when its output violates the contract.
            record['result']=result
            Draft202012Validator(item['definition']['output_schema']).validate(result.get('structured',result))
            from .evidence import artifact_inventory
            record['artifacts']=artifact_inventory(record['workspace'],data,op)
        except Exception as error:
            record.update({'status':'failed','error':{'type':type(error).__name__,'message':str(error)[:8192]}})
        try:
            return self.finish(redact(record,secrets))
        except Exception as error:
            record['status']='failed'
            failure={'ok':False,'status':'failed','invocation_id':record['invocation_id'],
                'receipt_persisted':False,'error':{'type':type(error).__name__,
                'message':redact(str(error),secrets)[:8192]}}
            with self.lock:
                job=self.jobs.get(record['invocation_id'])
                if job: job['failure']=failure
            return failure
        finally:
            with self.lock:
                job=self.jobs.get(record['invocation_id'])
                if job:
                    job['status']=record['status']
                    job['done'].set()

    def finish(self,record):
        record['completed_at_ms']=int(time.time()*1000)
        record['duration_ms']=record['completed_at_ms']-record['started_at_ms']
        record=redact(record); record['receipt_digest']=digest(record)
        raw=encoded(record)
        if len(raw)>MAX_RECEIPT_BYTES: raise ValueError('Receipt exceeds 32 MiB storage limit')
        folder=self.directory(); path=folder/(record['receipt_id']+'.json')
        # Publish a complete fsynced file atomically, without replacing any existing
        # receipt (including symlinks). Readers never observe a partial JSON file.
        with tempfile.NamedTemporaryFile(dir=folder,prefix='.receipt-',suffix='.tmp') as f:
            f.write(raw); f.flush(); os.fsync(f.fileno())
            os.link(f.name,path)
        result={'ok':record['status']=='completed','status':record['status'],'receipt_id':record['receipt_id'],
            'receipt_digest':record['receipt_digest'],'ability_id':record['ability_id'],'error':record.get('error')}
        payload=record.get('result')
        if payload is not None:
            if len(encoded(payload))<=12000: result['result']=payload
            else: result['result']={'omitted':True,'bytes':len(encoded(payload)),'hint':'Retrieve receipt with offset/limit; evidence remains on disk'}
        return result

    def receipts(self,receipt_id=None,limit=None,offset=0):
        if limit is None: limit=12000 if receipt_id else 20
        folder=self.directory()
        if receipt_id:
            if not re.fullmatch(r'[a-f0-9-]{36}',receipt_id): raise ValueError('Invalid receipt ID')
            path=folder/(receipt_id+'.json')
            if path.is_symlink(): raise PermissionError('Receipt symlink forbidden')
            with open(path,'rb') as f: raw=f.read(MAX_RECEIPT_BYTES+1)
            if len(raw)>MAX_RECEIPT_BYTES: raise ValueError('Receipt exceeds 32 MiB storage limit')
            value=json.loads(raw); checksum=value.pop('receipt_digest')
            if digest(value)!=checksum: raise ValueError('Receipt integrity verification failed')
            value['receipt_digest']=checksum
            text=json.dumps(value,ensure_ascii=False)
            return {'receipt_id':receipt_id,'verified':True,'total_chars':len(text),'offset':offset,'text':text[offset:offset+limit],'next_offset':offset+limit if offset+limit<len(text) else None}
        paths=sorted(folder.glob('*.json'),key=lambda p:p.stat().st_mtime,reverse=True)[:limit]
        return {'receipts':[p.stem for p in paths]}

    def status(self,invocation_id,cancel=False):
        with self.lock:
            job=self.jobs.get(invocation_id)
            if job and job.get('failure'): return copy.deepcopy(job['failure'])
            if job and job['status']=='running':
                if cancel: job['cancel'].set()
                return {'invocation_id':invocation_id,'status':job['status'],'cancellation_requested':cancel}
        return self.receipts(invocation_id,12000)

    def close(self):
        with self.lock:
            self.closed=True; jobs=[j for j in self.jobs.values() if j['status']=='running']
            for job in jobs: job['cancel'].set()
        for job in jobs:
            job['done'].wait(timeout=6)

    def check_runtime(self):
        binary=shutil.which(self.config.kujo_bin)
        if not binary: raise FileNotFoundError('Install canonical Kujo >=1.6,<2 and set kujo_bin')
        stat=Path(binary).stat(); key=(binary,stat.st_mtime_ns,stat.st_size)
        if self.runtime_cache and self.runtime_cache[0]==key: return self.runtime_cache[1]
        result=run([binary,'--version'],str(self.data_dir.parent),{'PATH':'/usr/bin:/bin'},5,8192,threading.Event())
        version=result['stdout'].strip(); match=re.search(r'(\d+)\.(\d+)\.(\d+)',version)
        if result['status']!='completed' or result['exit_code']!=0 or not match or not (1,6,0)<=tuple(map(int,match.groups()))<(2,0,0):
            raise RuntimeError('Unsupported Kujo runtime: '+version+'; expected >=1.6,<2')
        self.runtime_cache=(key,version)
        return version

    def doctor(self):
        binary=shutil.which(self.config.kujo_bin); version=None; compatible=False
        if binary:
            outcome=run([binary,'--version'],str(self.data_dir.parent),{'PATH':'/usr/bin:/bin'},5,8192,threading.Event())
            version=outcome['stdout'].strip(); m=re.search(r'(\d+)\.(\d+)\.(\d+)',version)
            compatible=bool(outcome['status']=='completed' and outcome['exit_code']==0 and m and (1,6,0)<=tuple(map(int,m.groups()))<(2,0,0))
        return {'ok':compatible,'runtime':binary,'runtime_version':version,'runtime_compatible':compatible,
            'profile':self.config.profile,'trusted_workspaces':list(self.config.trusted_workspaces),
            'capabilities':[{'id':k,**self.availability(v)} for k,v in self.catalog.all().items()],
            'receipt_directory':str(self.data_dir/'receipts'),'telemetry':'off; only explicit watchdog Ability calls send data'}
