"""Replace both delivery soundtracks while proving the video streams stay exact."""
import hashlib
import json
import os
import pathlib
import subprocess
import tempfile

root = pathlib.Path(__file__).resolve().parents[1]
master = root / 'assets/master.m4a'


def video_hash(path):
    return subprocess.check_output([
        'ffmpeg', '-nostdin', '-v', 'error', '-i', str(path),
        '-map', '0:v:0', '-c', 'copy', '-f', 'hash', '-hash', 'sha256', '-'
    ], text=True).strip()


records = []
for name in ['kujo-hermes-checkout.mp4', 'kujo-hermes-checkout-480p.mp4']:
    movie = root / 'delivery' / name
    before = video_hash(movie)
    with tempfile.TemporaryDirectory(prefix='kujo-audio-', dir=movie.parent) as directory:
        output = pathlib.Path(directory) / name
        subprocess.run([
            'ffmpeg', '-nostdin', '-y', '-v', 'error', '-i', str(movie),
            '-i', str(master), '-map', '0:v:0', '-map', '1:a:0',
            '-c', 'copy', '-movflags', '+faststart', str(output)
        ], check=True)
        after = video_hash(output)
        assert before == after, 'Video changed during soundtrack replacement'
        os.replace(output, movie)
    records.append({'file': str(movie.relative_to(root)), 'before_video_sha256': before,
                    'after_video_sha256': after, 'video_unchanged': True})
(root / 'evidence/pronunciation-remux.json').write_text(json.dumps({
    'master_sha256': hashlib.sha256(master.read_bytes()).hexdigest(),
    'videos': records, 'method': 'Stream-copy video and AAC master; no picture re-encode.'
}, indent=2) + '\n')
print('PASS: both video streams unchanged; updated soundtracks installed.')
