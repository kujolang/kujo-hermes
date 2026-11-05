"""Trim native screen recordings removing only the recorder’s blank bottom pad; preserve every horizontal pixel."""
import hashlib,json,pathlib,subprocess
r=pathlib.Path(__file__).resolve().parents[1];p=r/'evidence/v5-workflows/capture.json';d=json.loads(p.read_text());source=r/d['source_file']
d['presentation_crop']={'x':0,'y':0,'width':1280,'height':712,'reason':'Remove only 88 pixels of blank gray recorder padding, as in revision 4'}
d['source_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
for shot in d['shots']:
 file=r/'assets'/('workflow-'+shot['id']+'.mp4')
 subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-ss',str(shot['source_start']+.5),'-i',str(source),'-t','11.5','-vf','crop=1280:712:0:0','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(file)],check=True)
 shot['file']=str(file.relative_to(r));shot['sha256']=hashlib.sha256(file.read_bytes()).hexdigest()
p.write_text(json.dumps(d,indent=2)+'\n')
print('Built eleven distinct 1280×712 clips. Only blank recorder padding removed; no side crop, zoom, or pan.')
