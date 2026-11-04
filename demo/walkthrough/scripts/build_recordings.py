"""Rebuild the committed terminal clips from their original asciinema recordings."""
import pathlib,subprocess,sys,tempfile
r=pathlib.Path(__file__).resolve().parents[1]
def run(*args):subprocess.run([str(x) for x in args],cwd=r,check=True)
run(sys.executable,'scripts/cast_video.py','evidence/casts/discover.cast','--windows','[[79.5,80.2,1.8]]','--output','assets/discover.mp4')
run(sys.executable,'scripts/cast_video.py','evidence/casts/checks.cast','--windows','[[125.9,129,3]]','--output','assets/checks.mp4')
run(sys.executable,'scripts/cut_cast.py','evidence/casts/eval.cast','--windows','[[174.5,181.5,7],[220.8,223.51,2.71]]','--output','evidence/casts/approval-cut.cast')
with tempfile.TemporaryDirectory(prefix='kujo-hermes-video-') as tmp:
 gif=pathlib.Path(tmp)/'approval.gif'
 run('agg','--text-font-family','Menlo','--font-size','30','--line-height','1.1','--idle-time-limit','1000','--fps-cap','15','--last-frame-duration','0.01','evidence/casts/approval-cut.cast',gif)
 run('ffmpeg','-y','-v','error','-i',gif,'-vf','scale=1800:840:force_original_aspect_ratio=decrease,pad=1800:840:(ow-iw)/2:(oh-ih)/2:color=0x060606','-r','30','-t','9.71','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','assets/approval.mp4')
