#!/usr/bin/env python3
"""Rebuild evidence-linked catalog and organization inventory from local canonical sources."""
import argparse,json,pathlib,subprocess
p=argparse.ArgumentParser(); p.add_argument('--sources',required=True); args=p.parse_args()
root=pathlib.Path(__file__).resolve().parents[1]; sources=pathlib.Path(args.sources).resolve()
abilities=json.loads((root/'catalog/abilities.json').read_text()); evidence=json.loads((root/'evidence/real-tools.json').read_text())
tested={r['ability_id']:r for r in evidence['results']}
proof={k:'evidence/real-tools.json' for k in tested}
for filename in ('service-tools.json','optional-tools.json','live-packwrite.json'):
 path=root/'evidence'/filename
 if path.exists():
  extra=json.loads(path.read_text())
  for result in extra.get('results',[extra.get('result')] if extra.get('result') else []):
   tested[result['ability_id']]=result; proof[result['ability_id']]='evidence/'+filename
rows=[]
for item in abilities:
 d=item['definition']; result=tested.get(d['id'])
 rows.append({**item,'source_repository':'https://github.com/kujolang/'+item['source'] if item.get('source') else 'https://github.com/kujolang/kujo-hermes',
 'dependencies':['Kujo >=1.6,<2','canonical '+item['source']+' source'] if item.get('source') else ['Python jsonschema'],
 'approval_required':any(e['kind']!='read' for e in d['effects']),
 'hermes_surface':'kujo_inspect + kujo_execute',
 'verification':'real canonical CLI passed' if result and result['ok'] else 'real canonical CLI failed: '+str(result.get('error')) if result else 'binding implemented; not certified in this environment',
 'test_evidence':proof[d['id']] if result else 'tests/test_core.py (routing boundary only)'})
(root/'docs/ability-inventory.json').write_text(json.dumps(rows,indent=2)+'\n')
lines=['# Supported Ability inventory','', 'Exact schemas, effects, dependencies and evidence: [machine-readable inventory](ability-inventory.json). All execution uses `kujo_execute`; schema inspection is on demand. `ok` reports execution success, not release readiness. Untested bindings are not certified.','', '| Ability | Canonical source / operation | Approval | Evidence |','|---|---|---|---|']
for x in rows: lines.append('| '+x['definition']['id']+' | '+str(x.get('source') or 'native')+' / '+x['operation']+' | '+('human' if x['approval_required'] else 'read policy')+' | '+x['verification']+' |')
(root/'docs/abilities.md').write_text('\n'.join(lines)+'\n')
org=json.loads((root/'docs/organization.json').read_text()); inventory=[]; definitions=[]
for repo in org:
 name=repo['name']; checkout=sources/name; entry={**repo,'url':'https://github.com/kujolang/'+name}
 if not (checkout/'.git').exists():
  entry.update({'inspection':'GitHub organization metadata; no canonical local checkout','integration':'No inferred executable interface; operator-reviewed binding required'})
 else:
  entry['commit']=subprocess.check_output(['git','-C',str(checkout),'rev-parse','HEAD'],text=True).strip()
  paths=subprocess.check_output(['git','-C',str(checkout),'ls-files'],text=True).splitlines()
  entry['interfaces']=[x for x in paths if (x.startswith('bin/') or x in ('README.md','package.json','kennel.toml','ability-pack.json') or x.endswith('abilities/registry.json'))][:35]
  entry['integration']='Direct Hermes binding' if any(a.get('source')==name for a in abilities) else 'Library/application/site or unbound tool; no speculative execution adapter'
  for rel in paths:
   if not rel.endswith('.json') or any(part.lower() in ('node_modules','vendor','tests','examples','fixtures','demo','demos','dist','artifacts','evidence','.loop-engineering','kennel_packages') for part in pathlib.Path(rel).parts): continue
   file=checkout/rel
   if not file.is_file() or file.stat().st_size>2_000_000: continue
   try: value=json.loads(file.read_text())
   except (ValueError,UnicodeError): continue
   def scan(v):
    if isinstance(v,dict):
     if v.get('schema')=='kujo.ability/v1': definitions.append({'repository':name,'path':rel,'commit':entry['commit'],'definition':v,'available_in_hermes':v.get('id') in {a['definition']['id'] for a in abilities}})
     else:
      for x in v.values(): scan(x)
    elif isinstance(v,list):
     for x in v: scan(x)
   scan(value)
 inventory.append(entry)
(root/'docs/ecosystem-inventory.json').write_text(json.dumps({'scope':'All organization repositories returned by gh repo list on 2026-11-04; tracked non-fixture JSON definitions in available primary checkouts. Not a claim of a global production registry.','repositories':inventory,'canonical_definitions':definitions},indent=2)+'\n')
print(len(rows),'Hermes abilities;',len(inventory),'organization repositories;',len(definitions),'non-fixture definition occurrences')
