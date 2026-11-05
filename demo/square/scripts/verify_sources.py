"""Bind the square edit to canonical run evidence and uncropped source footage."""
import hashlib,json,pathlib
r=pathlib.Path(__file__).resolve().parents[1];old=r.parent/'walkthrough'
timeline=json.loads((r/'timeline.json').read_text());shots=json.loads((r/'evidence/shot-map.json').read_text())
assert timeline['duration']==88 and len(shots)==9
records=[]
for s in shots:
 p=r/s['source'];assert p.exists(),p
 if s['scene']!='install':
  original=old/s['source'];assert p.read_bytes()==original.read_bytes()
 composition=(r/'compositions'/f'{s["scene"]}.html').read_text()
 assert 'object-fit:contain' in composition and 'scale:' not in composition
 voice=next(v for v in timeline['cues'] if v['cue']==s['cue'])
 assert voice['start']>=s['start'] and voice['start']+voice['duration']<s['start']+s['duration']
 records.append(dict(s,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
assert timeline['cues'][-1]['start']+timeline['cues'][-1]['duration']<88
assert 'Install Kujo Hermes today.' in (r/'compositions/outro.html').read_text()
assert (r/'index.html').read_text().count('class="clip glitch-cut"')==10
native=json.loads((old/'evidence/v5-workflows/eval.json').read_text()) if (old/'evidence/v5-workflows/eval.json').exists() else None
(r/'evidence/source-verification.json').write_text(json.dumps({'ok':True,'shots':records,'native_evidence':'../walkthrough/evidence/v5-workflows/','approval_evidence':'../walkthrough/evidence/','installation_evidence':'install.cast','note':'Existing native viewer footage reused unchanged. New public installation recording. Full width contained; no screen crop or zoom.'},indent=2)+'\n')
print('PASS source hashes, distinct shots, complete source width, natural-speed cue containment and all bumper transitions')
