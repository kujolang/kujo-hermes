"""Replay real terminal states, cutting download waits; preserve source timestamps."""
import pathlib,subprocess,sys
r=pathlib.Path(__file__).resolve().parents[1]
def run(*args):subprocess.run([str(x) for x in args],cwd=r,check=True)
run(sys.executable,'scripts/cast_video.py','evidence/install.cast','--windows','[[0.3,0.3,2.6],[101.86,101.86,0.9],[122.64,122.64,1.0],[315.9,315.9,0.5]]','--output','assets/install-step.mp4')
run(sys.executable,'scripts/cast_video.py','evidence/setup.cast','--windows','[[0.2,3.2,2.1],[36.95,36.95,2.9]]','--output','assets/setup-step.mp4')
(r/'assets/install-concat.txt').write_text("file 'install-step.mp4'\nfile 'setup-step.mp4'\n")
run('ffmpeg','-nostdin','-y','-v','error','-f','concat','-safe','0','-i','assets/install-concat.txt','-c','copy','-movflags','+faststart','assets/install.mp4')
