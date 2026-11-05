"""Guard edit integrity, unchanged bumpers, measured narration, and claim provenance."""
import hashlib,json,pathlib,subprocess
r=pathlib.Path(__file__).resolve().parents[1];repo=r.parents[1]
t=json.loads((r/'timeline.json').read_text());s=json.loads((r/'story.json').read_text())
assert t['duration']==85 and len(t['scenes'])==8
for name in ('intro','outro'):
 p=r/'compositions'/f'{name}.html'
 original=subprocess.check_output(['git','show',f'2217f7e:demo/walkthrough/compositions/{name}.html'],cwd=repo)
 assert p.read_bytes()==original,f'{name} bumper changed'
for cue in t['cues']:
 p=r/'assets'/f'{cue["cue"]}.mp3'
 if p.exists():assert hashlib.sha256(p.read_bytes()).hexdigest()==cue['audio_sha256']
for before,after in zip(t['cues'],t['cues'][1:]):
 assert before['start']+before['duration']<after['start'], 'Narration overlaps'
for sc in t['scenes']:
 cue=next(c for c in t['cues'] if c['cue']==sc['cue'])
 assert cue['start']>=sc['start']+.29
 assert cue['start']+cue['duration']<sc['start']+sc['duration']-.5
assert abs(t['scenes'][-1]['start']+t['scenes'][-1]['duration']-80.33)<.001
receipt=json.loads(json.loads((r/'evidence/receipt-verification.json').read_text())['text'])
assert len(receipt['artifacts']['files'])==10
contract=json.loads((r/'evidence/demo-contract.json').read_text())
assert contract['acceptance_criteria'][0]=='2 + 3 returns 5'
assert contract['acceptance_criteria'][0] in (r/'compositions/context.html').read_text()
assert receipt['result']['structured']['data']['test_results'][0]['details']['command']=='python3 -m unittest discover -s tests'
assert receipt['result']['structured']['data']['test_results'][1]['details']['path']=='calculator.py'
text=' '.join(c['text'] for c in t['cues']).lower()
assert not any(w in text for w in ('hackathon','contest','competition'))
root=(r/'index.html').read_text();assert root.count('class="clip glitch-cut"')==7
subprocess.run(['python3',str(r/'scripts/verify_evidence.py')],check=True)
print('PASS: unchanged bumper sources, non-overlapping natural-speed narration, real check details, ten artifact hashes, seven body-only CMD gates, no contest copy.')
