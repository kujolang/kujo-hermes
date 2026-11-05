"""Lazy, bounded Ability discovery with canonical contract validation."""
import copy
import json
from pathlib import Path
from jsonschema import Draft202012Validator
from .vendor.ability import ability_definition_digest_v2

ROOT = Path(__file__).resolve().parent.parent
MAX_INPUT_BYTES = 65536

def validate_input_size(value):
    if len(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())>MAX_INPUT_BYTES:
        raise ValueError('Ability input exceeds 64 KiB')

def read_json(path):
    with open(path, 'rb') as f: raw = f.read(2_097_153)
    if len(raw) > 2_097_152: raise ValueError('Catalog exceeds 2 MiB')
    return json.loads(raw)

def check_schema(schema):
    # No fetching remote references during validation.
    def visit(v):
        if isinstance(v,dict):
            for k,x in v.items():
                if k in ('$ref','$dynamicRef') and (not isinstance(x,str) or not x.startswith('#')):
                    raise ValueError('External schema references are forbidden')
                visit(x)
        elif isinstance(v,list):
            for x in v: visit(x)
    visit(schema)
    Draft202012Validator.check_schema(schema)

class Catalog:
    def __init__(self, config):
        self.config=config
        self.entries=None

    def refresh(self):
        entries=read_json(ROOT/'catalog/abilities.json')
        for filename in self.config.extension_catalogs:
            extra=read_json(filename)
            if not isinstance(extra,list): raise ValueError('Extension catalog must be an array')
            for item in extra:
                item['extension']=True
            entries.extend(extra)
        if len(entries)>1000: raise ValueError('Too many Abilities')
        result={}
        for item in entries:
            d=item['definition']; digest=ability_definition_digest_v2(d)
            if not digest['ok']: raise ValueError(digest['message'])
            for key in ('input_schema','output_schema'): check_schema(d[key])
            if d['id'] in result: raise ValueError('Duplicate Ability: '+d['id'])
            if item.get('extension'):
                b=item.get('binding',{})
                if not isinstance(b.get('argv'),list) or not b['argv'] or any(not isinstance(x,str) for x in b['argv']):
                    raise ValueError('Extension requires declarative argv binding')
                if not Path(b['argv'][0]).is_absolute(): raise ValueError('Extension executable must be absolute')
            item['digest']=digest['value']; result[d['id']]=item
        self.entries=result
        return result

    def all(self):
        return self.entries if self.entries is not None else self.refresh()

    def exposed(self):
        profiles={p['id']:p for p in read_json(ROOT/'catalog/profiles.json')}
        ids=set()
        def add(name):
            p=profiles[name]
            for parent in p['extends']: add(parent)
            ids.update(p['ability_ids'])
        add('kujo.profile.'+self.config.profile)
        return {k:v for k,v in self.all().items() if (k in ids or self.config.profile=='full') and k not in self.config.denied_abilities}

    def get(self, ability):
        entries=self.exposed()
        if ability not in entries: raise PermissionError('Ability absent, denied, or outside active profile: '+ability)
        return copy.deepcopy(entries[ability])

    def inputs(self, item, supplied):
        validate_input_size(supplied)
        data=copy.deepcopy(supplied)
        if not isinstance(data,dict): raise ValueError('input must be an object')
        schema=item['definition']['input_schema']
        validator=Draft202012Validator(schema)
        validator.validate(data)
        defaulted=False
        for key, value in schema.get('properties',{}).items():
            if key not in data and isinstance(value,dict) and 'default' in value:
                data[key]=copy.deepcopy(value['default']); defaulted=True
        if defaulted:
            validate_input_size(data)
            validator.validate(data)
        return data
