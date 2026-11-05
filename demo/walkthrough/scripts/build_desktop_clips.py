"""Rebuild the desktop clips from the captured official Hermes UI."""
import pathlib,json,hashlib,subprocess
r=pathlib.Path(__file__).resolve().parents[1]
d=json.loads((r/'evidence/desktop-capture.json').read_text())
source=r/d['source_file']
assert hashlib.sha256(source.read_bytes()).hexdigest()==d['source_sha256']
for c in d['clips']:
 subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-ss',str(c['source_start']),'-i',str(source),'-t',str(c['duration']),'-vf','tpad=stop_mode=clone:stop_duration=3','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(r/c['file'])],check=True)
