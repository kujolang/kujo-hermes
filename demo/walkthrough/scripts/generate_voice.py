"""Generate requested Siren V4 narration; cached by text hash, never log credentials."""
import base64,hashlib,json,os,pathlib,subprocess,urllib.request,time
root=pathlib.Path(__file__).resolve().parents[1];assets=root/'assets';evidence=root/'evidence'
cues=[
('intro','Kujo Hermes.'),
('setup',"Before you commit, ask Hermes to check your repository. Kujo Hermes connects the agent directly to Kujo's developer tools."),
('discover',"Start by discovering what's installed. ShipCheck checks release readiness. PackWrite organizes task context. Spec validates requirements, and Eval runs your checks."),
('request',"Here, a free local model drives Hermes. We ask it to inspect a Python project, validate its specification, and check the results."),
('approval',"Hermes loads each tool's schema when it needs it. Operations that change state require approval. You decide what runs in your trusted workspace."),
('proof',"These are real tool results. Follow the receipt to see which Ability ran, its command, and evidence hashes. Execution success doesn't automatically mean release-ready."),
('breadth',"There are fifty-one bindings across code inspection, verification, workflows, and observability. Scout, Scent, Dispatch, RunLedger, and Watchdog extend the workflow. Workcell and Lens need their own prerequisites."),
('benefit',"Less command memorization. Reusable context. Checks you can repeat, and results you can trace. Install the plugin, trust your repository, and ask Hermes."),
('outro','Kujo. Trust at the speed of AI.')]
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
 with request('text-to-speech/'+voice+'?output_format=mp3_44100_128',payload) as response:
  audio=response.read();request_id=response.headers.get('request-id')
 assert len(audio)>1000;file.write_bytes(audio)
 duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(file)],text=True))
 record={'cue':name,'text':text,'provider':'ElevenLabs','model':model,'voice_name':'Siren','voice_id':voice,'generation_tier':tier,'request_sha256':signature,'audio_sha256':hashlib.sha256(audio).hexdigest(),'duration':duration,'request_id':request_id,'authorized_by':'User requested Siren V4 narration for this walkthrough','generated_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
 receipt.write_text(json.dumps(record,indent=2)+'\n');pending.unlink();records.append(record);print(name,round(duration,2),flush=True)
(evidence/'narration.json').write_text(json.dumps(records,indent=2)+'\n')
print('Total spoken duration:',sum(r['duration'] for r in records))
