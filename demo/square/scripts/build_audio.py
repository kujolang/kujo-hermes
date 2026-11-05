"""Mix measured Siren cues, existing Kujo music, and original CMD transition SFX."""
import json,pathlib,subprocess
r=pathlib.Path(__file__).resolve().parents[1];timeline=json.loads((r/'timeline.json').read_text());cues=timeline['cues'];cmd=['ffmpeg','-nostdin','-y','-hide_banner'];filters=[]
for i,c in enumerate(cues):
 cmd+=['-i',str(r/'assets'/(c['cue']+'.mp3'))]
 filters.append(f'[{i}:a]aresample=48000,adelay={round(c["start"]*1000)}:all=1[v{i}]')
cmd+=['-stream_loop','-1','-i',str(r/'assets/music-original.wav')]
filters.append(f'[{len(cues)}:a]aresample=48000,atrim=0:88,volume=0.065,afade=t=in:d=1,afade=t=out:st=85:d=3[music]')
labels=[f'v{i}' for i in range(len(cues))]+['music']
for k,s in enumerate(timeline['scenes']+[{'start':80.8}]):
 i=len(cues)+1+k;source=['001','002','005'][k%3];cmd+=['-i',str(r/'assets'/f'cmd-sfx-{source}.mp3')]
 delay=round((s['start']-.19)*1000)
 filters.append(f'[{i}:a]aresample=48000,atrim=0:0.7,asetpts=PTS-STARTPTS,afade=t=out:st=0.38:d=0.32,volume=0.13,adelay={delay}:all=1[s{k}]');labels.append(f's{k}')
filters.append(''.join(f'[{x}]' for x in labels)+f'amix=inputs={len(labels)}:duration=longest:normalize=0,atrim=0:88,loudnorm=I=-16:TP=-1.5:LRA=7[mix]')
cmd+=['-filter_complex',';'.join(filters),'-map','[mix]','-c:a','aac','-b:a','192k','-ar','48000',str(r/'assets/master.m4a')]
subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=(r/'evidence/audio-mix.log').open('w'))
print('Mixed original Siren takes and ten CMD sound transitions; 88 seconds.')
