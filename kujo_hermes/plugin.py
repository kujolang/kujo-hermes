"""Only this module knows Hermes APIs."""
import json
from pathlib import Path
from jsonschema import Draft202012Validator
from .config import Config
from .service import Service, redact

STRING={'type':'string','minLength':1,'maxLength':4096}
TOOLS={
 'kujo_discover':('Find Kujo engineering Abilities: ShipCheck, PackWrite, Eval, Spec, Scout, Workcell, Loop and more. Returns compact metadata; inspect a selected Ability before execution.',{'query':{'type':'string','maxLength':200},'refresh':{'type':'boolean'},'offset':{'type':'integer','minimum':0},'limit':{'type':'integer','minimum':1,'maximum':100}},[]),
 'kujo_inspect':('Get one canonical Kujo Ability input/output schema, effects, identity and installation status.',{'ability':STRING},['ability']),
 'kujo_execute':('Execute a discovered Kujo Ability in an operator-trusted workspace. Mutations require Hermes approval; no approval boolean is accepted. Returns a verifiable receipt. Use background for long tasks.',{'ability':STRING,'input':{'type':'object'},'workspace':STRING,'background':{'type':'boolean'}},['ability','input','workspace']),
 'kujo_status':('Inspect an execution or request cancellation, including child process cleanup.',{'invocation_id':STRING,'cancel':{'type':'boolean'}},['invocation_id']),
 'kujo_receipts':('List recent execution receipts or retrieve a hash-verified receipt in bounded pages. limit is characters for a receipt, count when listing.',{'receipt_id':STRING,'limit':{'type':'integer','minimum':1,'maximum':12000},'offset':{'type':'integer','minimum':0}},[]),
 'kujo_doctor':('Check Kujo runtime compatibility, installed sources, profile, workspace trust and receipt storage without running repository tasks.',{},[]),
}

def register(ctx):
    from plugins.plugin_storage import plugin_data_dir
    from agent.secret_scope import get_secret
    values={k:ctx.get_config(k,v.default if v.default is not None else None) for k,v in Config.__dataclass_fields__.items()}
    service=Service(Config.parse(values),plugin_data_dir('kujo-hermes'),get_secret=get_secret)
    from .approval import ApprovalGate
    gate=ApprovalGate(service)
    service.approve=gate.consume
    ctx.register_hook('pre_tool_call',gate.pre_tool)
    ctx.register_hook('post_approval_response',gate.response)
    for name,(description,properties,required) in TOOLS.items():
        params={'type':'object','properties':properties,'required':required,'additionalProperties':False}
        operation=getattr(service, name.removeprefix('kujo_'))
        def handler(args, _operation=operation, _params=params, **kwargs):
            try:
                Draft202012Validator(_params).validate(args)
                if _operation.__name__=='receipts' and 'receipt_id' not in args and args.get('limit',20)>50:
                    raise ValueError('Receipt listing limit cannot exceed 50')
                return json.dumps(_operation(**args),ensure_ascii=False)
            except Exception as error:
                return json.dumps({'ok':False,'error':{'type':type(error).__name__,'message':redact(str(error))}})
        ctx.register_tool(name=name,toolset='kujo',schema={'name':name,'description':description,'parameters':params},handler=handler)
    ctx.register_command('kujo',lambda raw: json.dumps(service.doctor() if raw.strip()=='doctor' else service.discover()),description='Kujo catalog or doctor')
    ctx.register_skill('kujo-engineering', Path(__file__).resolve().parent.parent / 'skills/kujo-engineering/SKILL.md', description='Kujo engineering tools and verified workflows')
    ctx.on_unload(service.close)
