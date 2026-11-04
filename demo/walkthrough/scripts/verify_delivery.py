"""Verify the finished MP4, decode every frame, and measure its audio."""
import hashlib,json,pathlib,re,subprocess
r=pathlib.Path(__file__).resolve().parents[1];video=r/'delivery/kujo-hermes-walkthrough.mp4'
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)],text=True))
v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'],v['codec_name'],v['pix_fmt'])==(1920,1080,'h264','yuv420p')
assert v['r_frame_rate']=='30/1' and int(v['nb_frames'])==2550
assert 84.9<=float(probe['format']['duration'])<90
assert a['codec_name']=='aac' and a['sample_rate']=='48000'
decode=subprocess.run(['ffmpeg','-nostdin','-v','error','-i',str(video),'-f','null','-'],capture_output=True,text=True,check=True)
assert not decode.stderr.strip(),decode.stderr
meter=subprocess.run(['ffmpeg','-nostdin','-hide_banner','-i',str(video),'-af','loudnorm=I=-16:TP=-1.5:LRA=7:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
levels=json.loads(re.findall(r'\{\s*"input_i".*?\}',meter.stderr,re.S)[-1])
assert -20<float(levels['input_i'])<-12
assert float(levels['input_tp'])<0
result={'ok':True,'file':str(video.relative_to(r)),'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'bytes':video.stat().st_size,'duration_seconds':float(probe['format']['duration']),'width':v['width'],'height':v['height'],'fps':v['r_frame_rate'],'frames':int(v['nb_frames']),'video_codec':v['codec_name'],'audio_codec':a['codec_name'],'sample_rate':int(a['sample_rate']),'full_decode':'passed','integrated_lufs':float(levels['input_i']),'true_peak_dbtp':float(levels['input_tp']),'listening_review':False}
(r/'evidence/delivery-verification.json').write_text(json.dumps(result,indent=2)+'\n')
(r/'evidence/delivery-loudness.json').write_text(json.dumps(levels,indent=2)+'\n')
print(json.dumps(result,indent=2))
