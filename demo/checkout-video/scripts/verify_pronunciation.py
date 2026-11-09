"""Check applied pronunciation controls and soundtrack integrity, not audible speech."""
import hashlib
import json
import pathlib
import subprocess

root = pathlib.Path(__file__).resolve().parents[1]
rule = json.loads((root / 'pronunciation.json').read_text())
timeline = json.loads((root / 'timeline.json').read_text())
changed = []
for cue in timeline['cues']:
    if rule['word'] not in cue['text']:
        continue
    assert cue['model'] == rule['model']
    assert cue['speech_text'] == cue['text'].replace(rule['word'], rule['spoken'])
    audio = root / 'assets' / (cue['cue'] + '.mp3')
    assert hashlib.sha256(audio.read_bytes()).hexdigest() == cue['audio_sha256']
    assert cue['start'] + cue['duration'] < timeline['duration']
    changed.append(cue['cue'])
assert set(changed) == {'intro', 'show-hook', 'show-fix', 'show-install', 'outro'}
for current, following in zip(timeline['cues'], timeline['cues'][1:]):
    assert current['start'] + current['duration'] <= following['start']
captions = (root / 'delivery/kujo-hermes-checkout.vtt').read_text()
assert captions.count('Hermes') == 5 and rule['spoken'] not in captions


def stream_hash(path, stream):
    return subprocess.check_output([
        'ffmpeg', '-nostdin', '-v', 'error', '-i', str(path), '-map', stream,
        '-c', 'copy', '-f', 'hash', '-hash', 'sha256', '-'
    ], text=True).strip()


master = stream_hash(root / 'assets/master.m4a', '0:a:0')
remux = json.loads((root / 'evidence/pronunciation-remux.json').read_text())
for video in remux['videos']:
    path = root / video['file']
    assert stream_hash(path, '0:v:0') == video['before_video_sha256']
    assert stream_hash(path, '0:a:0') == master
print('PASS: five explicit HER-meez inputs; canonical captions; no cue overlaps;')
print('both exact updated AAC masters installed; original video streams preserved.')
print('This verifies synthesis inputs and files, not a human listening judgment.')
