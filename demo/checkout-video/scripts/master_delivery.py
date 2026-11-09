"""Keep the final file's audio identical to the measured composition master."""
import pathlib,subprocess,tempfile,os
r=pathlib.Path(__file__).resolve().parents[1];movie=r/'delivery/kujo-hermes-checkout.mp4'
with tempfile.TemporaryDirectory(prefix='kujo-square-master-',dir=movie.parent) as directory:
 output=pathlib.Path(directory)/'mastered.mp4'
 subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-i',str(movie),'-i',str(r/'assets/master.m4a'),'-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',str(output)],check=True)
 os.replace(output,movie)
print('Remuxed exact measured master; video stream unchanged.')
