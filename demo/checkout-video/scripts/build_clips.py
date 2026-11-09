"""Rebuild the edit from unmodified terminal recordings and explicit source windows."""
import json,pathlib,subprocess,sys
root=pathlib.Path(__file__).resolve().parents[1]
for name,edit in json.loads((root/'edits.json').read_text()).items():
 subprocess.run([sys.executable,str(root/'scripts/cast_video.py'),str(root/edit['source']),'--windows',json.dumps(edit['windows']),'--output',str(root/'assets'/('workflow-'+name+'.mp4'))],check=True)
