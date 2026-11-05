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
assert contract['acceptance_criteria'][0] in (r/'evidence/v5-workflows/views/01-spec.md').read_text()
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
 body=(r/'compositions'/(sc['id']+'.html')).read_text()
 assert 'inset:0;width:100%;height:100%;object-fit:contain' in body
 assert 'object-fit:fill' not in body and 'scale:' not in body
 assert "tl.fromTo('.desktop-frame video'" not in body
assert desktop['presentation_crop']['x']==0 and desktop['presentation_crop']['width']==1280
print('PASS: all eight recording scenes fit their complete source width without zoom or side cropping.')

for clip in desktop['clips']:
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','json',str(r/clip['file'])]))
 assert probe['streams'][0]['width']==1280 and probe['streams'][0]['height']==712

# Every spoken subject gets its own full-width recording and canonical proof.
capture=json.loads((r/'evidence/v5-workflows/capture.json').read_text())
shots=json.loads((r/'evidence/v5-shot-map.json').read_text())
assert len(shots)==11 and len({x['clip'] for x in shots})==11
assert hashlib.sha256((r/capture['source_file']).read_bytes()).hexdigest()==capture['source_sha256']
for clip in capture['shots']:
 assert hashlib.sha256((r/clip['file']).read_bytes()).hexdigest()==clip['sha256']
 view=(r/clip['view']).read_text();assert view.splitlines()[0][2:] in clip['visible_text']
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','json',str(r/clip['file'])]))
 assert probe['streams'][0]['width']==1280 and probe['streams'][0]['height']==712
for shot in shots:
 assert shot['clip'] in (r/'compositions'/(shot['scene']+'.html')).read_text()
 if shot['spoken_trigger']:
  alignment=json.loads((r/'evidence'/('alignment-'+shot['cue']+'.json')).read_text())
  index=''.join(alignment['characters']).index(shot['spoken_trigger'])
  cue=next(c for c in t['cues'] if c['cue']==shot['cue'])
  assert abs(shot['start']-(cue['start']+alignment['character_start_times_seconds'][index]-.08))<.002
for name in ['spec','packwrite','eval','shipcheck','scout','dispatch']:
 record=json.loads((r/'evidence/v5-workflows'/(name+'.json')).read_text())
 assert record['result']['ok'] and record['tool']=='kujo_execute'
 receipt=json.loads((r/'evidence/v5-workflows'/(name+'-receipt.json')).read_text())['result']
 assert receipt['verified'] and receipt['receipt_id']==record['result']['receipt_id']
assert 'This workflow was not executed' in (r/'evidence/v5-workflows/views/09-dispatch.md').read_text()
print('PASS: eleven unique full-screen views, six actual canonical runs and verified receipts, phrase-aligned cuts, truthful Dispatch validation.')
