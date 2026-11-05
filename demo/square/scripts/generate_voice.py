"""Generate requested Siren V4 narration; cached by text hash, never log credentials."""
import base64,hashlib,json,os,pathlib,subprocess,urllib.request,time
root=pathlib.Path(__file__).resolve().parents[1];assets=root/'assets';evidence=root/'evidence'
story=json.loads((root/'story.json').read_text())
cues=[('intro','Kujo Hermes.')]+[(s['cue'],s['text']) for s in story['scenes']]+[('outro',story['outro'])]
voice='eXpIbVcVbLo8ZJQDlDnl';model='eleven_v4'
key=os.environ.get('ELEVENLABS_API_KEY')
if not key:key=subprocess.check_output(['security','find-generic-password','-s','kujo-videoops-elevenlabs','-a','videoops','-w'],stderr=subprocess.DEVNULL,text=True).strip()
def request(path,payload=None):
 req=urllib.request.Request('https://api.elevenlabs.io/v1/'+path,data=json.dumps(payload).encode() if payload else None,headers={'xi-api-key':key,'Content-Type':'application/json'})
 return urllib.request.urlopen(req,timeout=90)
with request('user/subscription') as response:tier=json.load(response)['tier']
assert tier not in ('free','unknown'), 'Generation-time commercial rights must be verified'
assert sum(len(t) for _,t in cues)<3500
records=[]
for name,text in cues:
 payload={'text':text,'model_id':model,'voice_settings':{'stability':0.5,'similarity_boost':0.75}}
 signature=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest();file=assets/(name+'.mp3');receipt=evidence/('voice-'+name+'.json');pending=evidence/('voice-'+name+'.pending')
 if file.exists() and receipt.exists():
  old=json.loads(receipt.read_text());assert old['request_sha256']==signature;records.append(old);continue
 assert not pending.exists(),'Uncertain request; reconcile provider history before retrying'
 pending.write_text(signature)
 with request('text-to-speech/'+voice+'/with-timestamps?output_format=mp3_44100_128',payload) as response:
  result=json.load(response);audio=base64.b64decode(result['audio_base64']);request_id=response.headers.get('request-id')
  alignment=result.get('alignment') or result['normalized_alignment']
  (evidence/('alignment-'+name+'.json')).write_text(json.dumps(alignment,indent=2)+'\n')
 assert len(audio)>1000;file.write_bytes(audio)
 duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(file)],text=True))
 record={'cue':name,'text':text,'provider':'ElevenLabs','model':model,'voice_name':'Siren','voice_id':voice,'generation_tier':tier,'request_sha256':signature,'audio_sha256':hashlib.sha256(audio).hexdigest(),'duration':duration,'request_id':request_id,'authorized_by':'User requested Siren V4 narration for this walkthrough','generated_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
 receipt.write_text(json.dumps(record,indent=2)+'\n');pending.unlink();records.append(record);print(name,round(duration,2),flush=True)
(evidence/'narration.json').write_text(json.dumps(records,indent=2)+'\n')
print('Total spoken duration:',sum(r['duration'] for r in records))
