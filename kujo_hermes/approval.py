"""Hermes public hook approval bridge. Observations cannot mint remote Kujo approvals."""
import json
import threading
import time
import uuid
from .commands import plan
from .service import digest

class ApprovalGate:
    def __init__(self,service):
        self.service=service; self.pending={}; self.grants={}; self.lock=threading.Lock()

    def pre_tool(self,tool_name,args,**kwargs):
        if tool_name!='kujo_execute': return None
        try:
            item=self.service.catalog.get(args['ability'])
            data=self.service.catalog.inputs(item,args['input'])
            root=self.service.config.workspace(args['workspace'])
            argv,cwd,extra=plan(item,data,root,self.service.config)
            if not self.service.privileged(item): return None
            request=digest({'ability':item['digest'],'input':data,'workspace':str(root),'argv':argv})
            key='kujo:'+str(uuid.uuid4())+':'+request
            with self.lock:
                now=time.monotonic()
                self.pending={k:v for k,v in self.pending.items() if now-v[1]<300}
                self.grants={k:v for k,v in self.grants.items() if now-v<300}
                if len(self.pending)>=100: raise RuntimeError('Too many pending approvals')
                self.pending['plugin_rule:'+key]=(request,now)
            return {'action':'approve','rule_key':key,'message':json.dumps({'ability':args['ability'],'workspace':str(root),'effects':item['definition']['effects'],'command':argv,'request_digest':request})}
        except Exception as error:
            return {'action':'block','message':'Kujo preflight: '+str(error)}

    def response(self,pattern_key='',choice='',decided_by='',**kwargs):
        with self.lock:
            pending=self.pending.pop(pattern_key,None)
            if pending and time.monotonic()-pending[1]<300 and choice in ('once','session','always') and decided_by!='aux_llm':
                self.grants[(pending[0],pattern_key)]=time.monotonic()

    def consume(self,tool,reason,**kwargs):
        request=json.loads(reason)['request_digest']
        with self.lock:
            for key,created in list(self.grants.items()):
                if time.monotonic()-created>=300: self.grants.pop(key); continue
                if key[0]==request:
                    self.grants.pop(key)
                    return {'approved':True}
        return {'approved':False,'message':'No matching, unexpired human Hermes approval'}
