"""Optional loopback Watchdog transport; no automatic telemetry."""
import json
import urllib.request
from urllib.parse import urlsplit
import uuid
import datetime
import hashlib

def loopback_url(value):
    p=urlsplit(value)
    if p.scheme!='http' or p.hostname not in ('127.0.0.1','::1') or p.username or p.password or p.query or p.fragment:
        raise ValueError('Use literal loopback HTTP without credentials, query or fragment')
    return p.scheme+'://'+p.netloc

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs): raise ValueError('Redirects forbidden')

def watchdog(data,record=False,token=''):
    base=loopback_url(data.get('url','http://127.0.0.1:7700')); body=None
    if record:
        rid=str(uuid.uuid4()); now=datetime.datetime.now(datetime.timezone.utc).isoformat()
        body={'schema_version':'watchdog.telemetry.v2','batch_id':'kujo-hermes:'+rid,'sent_at':now,
            'producer':{'name':'kujo-hermes','version':'0.1.0','adapter_id':'kujo.hermes.native','adapter_version':'0.1.0','original_schema':'kujo.ability/v1'},
            'records':[{'record_id':rid,'record_type':'event','trace_id':hashlib.sha256(data.get('run_id',rid).encode()).hexdigest()[:32],
            'observed_at':now,'kind':'internal','name':data['name'],'status':data.get('status','ok'),
            'source':{'application.name':'kujo-hermes','harness.name':'hermes'},'references':[], 'attributes':{},'content':[],
            'privacy':{'content_mode':'off','policy_version':'watchdog.privacy.v1','transformations':['metadata_only']}}]}
    req=urllib.request.Request(base+('/telemetry/v2/batches' if record else '/healthz'),data=json.dumps(body).encode() if body else None,
        headers={'Content-Type':'application/json',**({'Authorization':'Bearer '+token} if token else {})})
    with urllib.request.build_opener(NoRedirect).open(req,timeout=5) as response:
        raw=response.read(65537)
        if len(raw)>65536: raise ValueError('Watchdog response exceeds limit')
        return {'status':response.status,'body':json.loads(raw)}
