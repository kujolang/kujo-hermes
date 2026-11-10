"""Check the prepared submission's candidate, media and evidence without posting."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import yaml

root = Path(__file__).resolve().parents[1]
catalog = yaml.safe_load((root/'submission/kujo-hermes.yaml').read_text())
manifest = yaml.safe_load((root/'plugin.yaml').read_text())
assert re.fullmatch('[a-f0-9]{40}', catalog['sha'])
assert catalog['version'] == manifest['version'] == '0.1.0'
assert catalog['requires_hermes'] == manifest['requires_hermes']
for name in ('provides_tools', 'provides_hooks', 'provides_middleware', 'requires_env'):
    assert catalog['capabilities'].get(name, []) == manifest.get(name, [])
ci = json.loads((root/'submission/evidence/candidate-ci.json').read_text())
assert ci['candidate'] == catalog['sha'] and ci['conclusion'] == 'success'
assert len(ci['jobs']) == 3 and all(job['conclusion'] == 'success' for job in ci['jobs'])
assert catalog['repo'] == 'https://github.com/kujolang/kujo-hermes'
assert not subprocess.check_output(['git', 'diff', 'v0.1.0', catalog['sha'], '--', 'kujo_hermes', 'catalog', 'plugin.yaml', 'pyproject.toml'], cwd=root)
video = root/'demo/checkout-video'
report = json.loads((video/'evidence/delivery-verification.json').read_text())
for record in (report, report['mobile']):
    assert record['duration_seconds'] < 90
    assert hashlib.sha256((video/record['file']).read_bytes()).hexdigest() == record['sha256']
    assert record['full_decode'] == 'passed'
provenance = json.loads((root/'demo/square/evidence/installation-provenance.json').read_text())
assert provenance['hermes_version'] == '0.22.7'
assert json.loads((video/'evidence/video-subject-verification.json').read_text())['ok']
assert json.loads((video/'evidence/release-check.json').read_text())['ok']
result = {'ok': True, 'candidate': catalog['sha'], 'release': 'v0.1.0', 'runtime_matches_release': True, 'video_seconds': report['duration_seconds'], 'mobile_sha256': report['mobile']['sha256'], 'installation_footage': 'Earlier successful native recording; release candidate verified separately in CI', 'external_submission': 'Not sent; catalog PR, X post and form require authorization', 'listening_review': report['listening_review']}
(root/'submission/verification.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
