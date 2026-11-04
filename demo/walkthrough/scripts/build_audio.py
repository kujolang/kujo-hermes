"""Mix cached narration with the original Kujo ambient bed; retain exact timings."""
import json,pathlib,subprocess
r=pathlib.Path(__file__).resolve().parents[1];cues=json.loads((r/'timeline.json').read_text())['cues'];cmd=['ffmpeg','-y','-hide_banner'];filters=[]
for i,c in enumerate(cues):
 cmd+=['-i',str(r/'assets'/(c['cue']+'.mp3'))]
 filters.append(f'[{i}:a]aresample=48000,adelay={round(c["start"]*1000)}:all=1[v{i}]')
cmd+=['-stream_loop','-1','-i',str(r/'assets/music-original.wav')]
filters.append(f'[{len(cues)}:a]aresample=48000,atrim=0:85,volume=0.065,afade=t=in:d=1,afade=t=out:st=82:d=3[music]')
filters.append(''.join(f'[v{i}]' for i in range(len(cues)))+f'[music]amix=inputs={len(cues)+1}:duration=longest:normalize=0,atrim=0:85,loudnorm=I=-16:TP=-1.5:LRA=7[mix]')
cmd+=['-filter_complex',';'.join(filters),'-map','[mix]','-c:a','aac','-b:a','192k','-ar','48000',str(r/'assets/master.m4a')]
subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=(r/'evidence/audio-mix.log').open('w'))
