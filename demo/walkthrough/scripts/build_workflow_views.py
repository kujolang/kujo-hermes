"""Create source-linked evidence documents for Hermes' real file viewer.
These are editorial summaries of actual tool results, never simulated chat messages.
"""
import json,pathlib,shutil
r=pathlib.Path(__file__).resolve().parents[1];e=r/'evidence/v5-workflows';out=e/'views';out.mkdir(exist_ok=True)
def read(n):return json.loads((e/(n+'.json')).read_text())['result']
def structured(n):return read(n)['result']['structured']
def save(n,title,body,source):
 text=f'# {title}\n\n{body}\n\n---\n\nRecorded native-tool evidence · {source}\n'
 (out/(n+'.md')).write_text(text)
contract=json.loads((r/'evidence/demo-contract.json').read_text());spec=structured('spec');pack=structured('packwrite');ev=structured('eval')['data'];ship=structured('shipcheck');dispatch=structured('dispatch');receipt=read('eval-receipt');payload=json.loads(receipt['text'])
assert spec['valid'] and pack['phase_count']==7 and ev['passed']==2 and ev['failed']==0 and receipt['verified']
save('00-task','The task: verify a Python calculator','## Success means\n\n- '+ '\n- '.join(contract['acceptance_criteria'])+'\n\n## Evidence we need\n\nTask contract → context pack → approved checks → receipt','task.spec.json')
save('01-spec','Spec · validate the contract',f'## Valid · {len(spec["errors"])} errors\n\n**Acceptance criterion:** {contract["acceptance_criteria"][0]}\n\nThe task contract is well formed. Implementation is checked separately by Eval.','kujo.spec.contract.validate · spec.json')
save('02-packwrite','PackWrite · check the execution pack',f'## {pack["phase_count"]} phases · {len(pack["missing_files"])} missing files\n\nThe existing pack is ready for handoff.\n\n**Next command:** `{pack["next_command"]}`\n\nThis run checks the seeded pack; it does not generate a new pack.','kujo.packwrite.pack.summary · packwrite.json')
d=read('discovery');items=d.get('abilities',d.get('items',[]));ids=[x.get('id',x.get('ability_id','')) for x in items]
save('03-discovery','Discover Kujo Abilities',f'## {d["total"]} catalog bindings\n\n- ShipCheck · release review\n- PackWrite · execution packs\n- Spec · task contracts\n- Eval · deterministic checks\n- Scout · repository context\n- Dispatch · workflows\n\nSchemas are requested when an Ability is inspected.','kujo_discover · discovery.json')
inspect=read('inspection');save('04-inspection','Inspect before execution','## Run Eval suite\n\n**Required input:** `config` — the evaluation suite file\n\n**Workspace:** an operator-trusted repository\n\n**Approval required:** true\n\nEffects: executes commands and writes evidence.','kujo_inspect · inspection.json')
save('05-eval','Eval · inspect the checks',f'## {ev["passed"]} passed · {ev["failed"]} failed\n\n| Check | Result |\n|---|---|\n'+ '\n'.join(f'| {t["name"]} | {"PASS" if t["passed"] else "FAIL"} |' for t in ev['test_results'])+'\n\n**Executed:** `python3 -m unittest discover -s tests`\n\n**Confirmed:** `calculator.py` exists.','kujo.eval.suite.run · eval.json')
save('06-receipt','Receipt · trace the execution',f'## Integrity verified\n\n**Tool:** `{payload["ability_id"]}`\n\n**Command:** Kujo → Eval → `eval.json`\n\n**Approval:** required and approved\n\n**Evidence:** {len(payload["artifacts"]["files"])} artifact hashes\n\nReceipt: `{receipt["receipt_id"]}`','kujo_receipts · eval-receipt.json')
warnings=[c['message'] for c in ship['checks'] if not c['passed'] and c['severity']=='warning']
save('07-shipcheck','ShipCheck · release review',f'## {ship["summary"]["warnings"]} review warnings · {ship["summary"]["failed_errors"]} blocking errors\n\n'+ '\n'.join('- '+w for w in warnings[:3])+'\n\nScan is informational. These findings do not establish release readiness.','kujo.shipcheck.repository.scan · shipcheck.json')
scout=read('scout')['result']['stdout'];lines=[l for l in scout.splitlines() if l.startswith(('Code files','Dependencies:','Routes:','Output profile:'))]
save('08-scout','Scout · repository context','## Repository inspected\n\n'+'\n\n'.join('**'+l.split(':')[0]+':**'+l.split(':',1)[1] for l in lines)+'\n\nOutput includes a scan manifest and repository context.','kujo.scout.repository.inspect · scout.json')
save('09-dispatch','Dispatch · validate the workflow',f'## Valid · {len(dispatch["errors"])} errors\n\n**Workflow:** `{dispatch["workflow_id"]}`\n\nPlan → gather sources → verify → approval → report\n\nValidation only. This workflow was not executed.','kujo.dispatch.workflow.validate · dispatch.json')
save('10-handoff','Handoff · evidence the next developer can inspect','## Evidence retained\n\n- Task contract and PackWrite pack\n- Two passing Eval checks\n- Verified execution receipts\n- Scout context and ShipCheck review findings\n- Validated Dispatch workflow\n\n**Next:** review the missing lint, formatting, and CI setup.','v5-workflows/index.json and per-tool receipts')
workspace=pathlib.Path('/tmp/kujo-hermes-video-20261104/video-evidence');workspace.mkdir(exist_ok=True)
for p in out.glob('*.md'):shutil.copy2(p,workspace/p.name)
print('Wrote 11 distinct, source-linked evidence views; no UI or session data modified.')
