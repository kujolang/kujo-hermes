"""Export visible Hermes messages and tool calls, excluding private reasoning."""
import hashlib,json,pathlib,sqlite3
root=pathlib.Path(__file__).resolve().parents[3];home=root/'.local/checkout-recording/home';out=root/'demo/checkout-video/evidence'
conn=sqlite3.connect(f'file:{home}/state.db?mode=ro',uri=True);conn.row_factory=sqlite3.Row
columns=[x[1] for x in conn.execute('pragma table_info(messages)')]
allowed=[x for x in ['session_id','role','content','tool_calls','tool_call_id','tool_name','timestamp'] if x in columns]
active=conn.execute('select session_id from messages order by rowid desc limit 1').fetchone()[0]
rows=[dict(row) for row in conn.execute('select '+','.join(allowed)+' from messages order by rowid') if row['role']!='system' and row['session_id']==active]
(out/'visible-session.json').write_text(json.dumps({'model':'qwen3.5:hermes-checkout64k (Qwen3.5 4B, local Ollama)','session_id':active,'hermes_commit':'2bd378ed1b8d6bf2192cb26e0a55ff3091e6bd19','messages':rows},indent=2)+'\n')
print('Exported',len(rows),'visible messages')
