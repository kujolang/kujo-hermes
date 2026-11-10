"""Bind completed media checks to the exact files that will be delivered."""
import hashlib,json,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
r=json.loads((root/'evidence/delivery-verification.json').read_text())
assert r['ok']
for result in [r,r['mobile']]:
 p=root/result['file']
 assert hashlib.sha256(p.read_bytes()).hexdigest()==result['sha256'],p
 assert result['full_decode']=='passed' and result['duration_seconds']<90
assert json.loads((root/'evidence/release-check.json').read_text())['ok']
assert json.loads((root/'evidence/video-subject-verification.json').read_text())['ok']
print('PASS: delivery hashes match the decoded, measured and source-matched files.')
