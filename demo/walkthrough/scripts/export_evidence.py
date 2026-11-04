"""Export visible messages and tool evidence only; exclude private reasoning and credentials."""
import argparse, hashlib, json, pathlib, re, sqlite3
p=argparse.ArgumentParser();p.add_argument('shot',choices=['discover','checks','eval']);args=p.parse_args()
r=pathlib.Path(__file__).resolve().parents[1];repo=r.parents[1]
cast=r/'evidence/casts'/(args.shot+'.cast')
records=[json.loads(line) for line in cast.read_text().splitlines()]
text=''.join(event[2] for event in records[1:] if event[1]=='o')
ids=re.findall(r'local-[0-9a-f]{64}',text);assert ids,'Recording must finish before export'
session=ids[-1]
c=sqlite3.connect(f'file:{repo}/.local/video/home/state.db?mode=ro',uri=True)
rows=c.execute('SELECT role,content,tool_name,tool_calls FROM messages WHERE session_id=? ORDER BY id',(session,)).fetchall()
messages=[]
for role,content,name,calls in rows:
 if role=='system':continue
 item={'role':role,'content':content}
 if name:item['tool_name']=name
 if calls:item['tool_calls']=json.loads(calls)
 messages.append(item)
assert messages
out={'session_id':session,'host':'Hermes v0.22.7','model':'local qwen3.5:hermes-demo (Qwen3.5 4B)','source_cast_sha256':hashlib.sha256(cast.read_bytes()).hexdigest(),'messages':messages}
(r/'evidence'/(args.shot+'-session.json')).write_text(json.dumps(out,indent=2)+'\n')
print(args.shot,session,len(messages),'visible messages exported')
