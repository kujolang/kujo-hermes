"""Join re-rendered release scenes to the unchanged verified workflow picture."""
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
film = root/'demo/checkout-video'
subprocess.run([
    'ffmpeg', '-nostdin', '-y', '-v', 'error',
    '-i', str(root/'.local/release-intro.mp4'),
    '-i', str(root/'.local/release-original.mp4'),
    '-i', str(root/'.local/release-ending.mp4'),
    '-i', str(film/'assets/master.m4a'),
    '-filter_complex',
    '[0:v]trim=0:3.2,setpts=PTS-STARTPTS[a];'
    '[1:v]trim=3.2:54,setpts=PTS-STARTPTS[b];'
    '[2:v]trim=0:19.2,setpts=PTS-STARTPTS[c];'
    '[a][b][c]concat=n=3:v=1:a=0[v]',
    '-map', '[v]', '-map', '3:a:0', '-r', '30', '-c:v', 'libx264',
    '-preset', 'fast', '-crf', '16', '-pix_fmt', 'yuv420p',
    '-c:a', 'copy', '-movflags', '+faststart',
    str(film/'delivery/kujo-hermes-checkout.mp4')
], check=True)
subprocess.run([
    'ffmpeg', '-nostdin', '-y', '-v', 'error',
    '-i', str(film/'delivery/kujo-hermes-checkout.mp4'),
    '-vf', 'scale=480:480:flags=lanczos', '-c:v', 'libx264', '-preset', 'fast',
    '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart',
    str(film/'delivery/kujo-hermes-checkout-480p.mp4')
], check=True)
print('Release scenes joined; 1080 and 480 square exports created.')
