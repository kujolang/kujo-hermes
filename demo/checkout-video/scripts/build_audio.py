"""Mix measured voice cues, existing Kujo music, and original CMD transition SFX."""
import json,pathlib,subprocess,re
r=pathlib.Path(__file__).resolve().parents[1];timeline=json.loads((r/'timeline.json').read_text());cues=timeline['cues'];D=timeline['duration'];cmd=['ffmpeg','-nostdin','-y','-hide_banner'];filters=[]
for i,c in enumerate(cues):
 cmd+=['-i',str(r/'assets'/(c['cue']+'.mp3'))]
 filters.append(f'[{i}:a]aresample=48000,adelay={round(c["start"]*1000)}:all=1[v{i}]')
music=r/'assets/showcase-music.mp3'
music_duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(music)],text=True))
cmd+=['-i',str(music)]
# Explicit gain envelopes leave the groove audible between voice cues.
envelope='0.75'
for c in cues:
 a=max(0,c['start']-.2);b=c['start']+c['duration']+.3
 envelope+=f'-0.40*min(1,max(0,(t-{a:.3f})/0.2))*min(1,max(0,({b:.3f}-t)/0.3))'
filters.append(f"[{len(cues)}:a]atempo={music_duration/D},aresample=48000,loudnorm=I=-19:TP=-4:LRA=8,volume='{envelope}':eval=frame,apad,atrim=0:{D},afade=t=in:d=0.15,afade=t=out:st={D-2}:d=2[music]")
labels=[f'v{i}' for i in range(len(cues))]+['music']
for k,s in enumerate(timeline['scenes']+[{'start':D-7.2}]):
 i=len(cues)+1+k;source=['001','002','005'][k%3];cmd+=['-i',str(r/'assets'/f'cmd-sfx-{source}.mp3')]
 delay=round((s['start']-.19)*1000)
 filters.append(f'[{i}:a]aresample=48000,atrim=0:0.7,asetpts=PTS-STARTPTS,afade=t=out:st=0.38:d=0.32,volume=0.10,adelay={delay}:all=1[s{k}]');labels.append(f's{k}')
filters.append(''.join(f'[{x}]' for x in labels)+f'amix=inputs={len(labels)}:duration=longest:normalize=0,atrim=0:{D}[mix]')
cmd+=['-filter_complex',';'.join(filters),'-map','[mix]','-c:a','pcm_s16le','-ar','48000',str(r/'assets/mix-unmastered.wav')]
subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=(r/'evidence/audio-mix.log').open('w'))
raw=r/'assets/mix-unmastered.wav'
analysis=subprocess.run(['ffmpeg','-nostdin','-hide_banner','-i',str(raw),'-af','loudnorm=I=-16:TP=-2:LRA=7:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
measured=json.loads(re.findall(r'\{\s*"input_i".*?\}',analysis.stderr,re.S)[-1])
filter=f"loudnorm=I=-16:TP=-2:LRA=7:measured_I={measured['input_i']}:measured_TP={measured['input_tp']}:measured_LRA={measured['input_lra']}:measured_thresh={measured['input_thresh']}:offset={measured['target_offset']}:linear=true"
subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-i',str(raw),'-af',filter,'-ar','48000','-c:a','aac','-b:a','192k',str(r/'assets/master.m4a')],check=True)
(r/'evidence/audio-mastering.json').write_text(json.dumps({'method':'Two-pass EBU R128; -16 LUFS, -2 dBTP pre-encode target; exact master remuxed into delivery','first_pass':measured,'second_pass_filter':filter},indent=2)+'\n')
print('Mixed original-speed narration, rhythmic music and CMD transitions;',D,'seconds.')
