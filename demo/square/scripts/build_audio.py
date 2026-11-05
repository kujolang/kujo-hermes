"""Mix measured Siren cues, existing Kujo music, and original CMD transition SFX."""
import json,pathlib,subprocess,re
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
filters.append(''.join(f'[{x}]' for x in labels)+f'amix=inputs={len(labels)}:duration=longest:normalize=0,atrim=0:88[mix]')
cmd+=['-filter_complex',';'.join(filters),'-map','[mix]','-c:a','pcm_s16le','-ar','48000',str(r/'assets/mix-unmastered.wav')]
subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=(r/'evidence/audio-mix.log').open('w'))
raw=r/'assets/mix-unmastered.wav'
analysis=subprocess.run(['ffmpeg','-nostdin','-hide_banner','-i',str(raw),'-af','loudnorm=I=-16:TP=-2:LRA=7:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
measured=json.loads(re.findall(r'\{\s*"input_i".*?\}',analysis.stderr,re.S)[-1])
filter=f"loudnorm=I=-16:TP=-2:LRA=7:measured_I={measured['input_i']}:measured_TP={measured['input_tp']}:measured_LRA={measured['input_lra']}:measured_thresh={measured['input_thresh']}:offset={measured['target_offset']}:linear=true"
subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-i',str(raw),'-af',filter,'-ar','48000','-c:a','aac','-b:a','192k',str(r/'assets/master.m4a')],check=True)
(r/'evidence/audio-mastering.json').write_text(json.dumps({'method':'Two-pass EBU R128; -16 LUFS, -2 dBTP pre-encode target; exact master remuxed into delivery','first_pass':measured,'second_pass_filter':filter},indent=2)+'\n')
print('Mixed and mastered original-speed Siren cues and ten CMD transitions; 88 seconds.')
