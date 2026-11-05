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
root=(r/'index.html').read_text();assert root.count('class="clip glitch-cut"')==9
subprocess.run(['python3',str(r/'scripts/verify_evidence.py')],check=True)
print('PASS: unchanged bumper sources, non-overlapping natural-speed narration, real check details, ten artifact hashes, nine CMD gates including both bumper boundaries, no contest copy.')

for cut in (3.8,80.33): assert f'data-start="{round(cut-.25,4)}"' in root
for sc in t['scenes']:
 body=(r/'compositions'/(sc['id']+'.html')).read_text()
 assert '<div class="rail">' not in body and '<p class="foot">' not in body and '<p class="eyebrow">' not in body

desktop=json.loads((r/'evidence/desktop-capture.json').read_text())
for clip in desktop['clips']:
 assert hashlib.sha256((r/clip['file']).read_bytes()).hexdigest()==clip['sha256']
assert hashlib.sha256((r/desktop['source_file']).read_bytes()).hexdigest()==desktop['source_sha256']

# Preserve every horizontal source pixel: no per-shot zoom/pan or cover crop.
for sc in t['scenes']:
 if sc['id']=='context': continue
 body=(r/'compositions'/(sc['id']+'.html')).read_text()
 assert 'inset:0;width:100%;height:100%;object-fit:contain' in body
 assert 'object-fit:fill' not in body and 'scale:' not in body
 assert "tl.fromTo('.desktop-frame video'" not in body
assert desktop['presentation_crop']['x']==0 and desktop['presentation_crop']['width']==1280
print('PASS: all seven recording scenes fit their complete source width without zoom or side cropping.')

for clip in desktop['clips']:
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','json',str(r/clip['file'])]))
 assert probe['streams'][0]['width']==1280 and probe['streams'][0]['height']==712
