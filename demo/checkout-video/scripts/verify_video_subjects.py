"""Compare decoded square frames to each actual source; catch reused/wrong screens."""
import io,json,pathlib,subprocess
from PIL import Image,ImageChops,ImageStat,ImageDraw,ImageFilter
r=pathlib.Path(__file__).resolve().parents[1];shots=json.loads((r/'evidence/shot-map.json').read_text());movie=r/'delivery/kujo-hermes-checkout.mp4'
def frame(file,t):
 duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(file)],text=True))
 t=max(0,min(t,duration-.1))
 return Image.open(io.BytesIO(subprocess.check_output(['ffmpeg','-nostdin','-v','error','-ss',str(t),'-i',str(file),'-frames:v','1','-f','image2pipe','-vcodec','png','-']))).convert('RGB')
def contained(im,w=1008,h=720):
 ratio=min(w/im.width,h/im.height);im=im.resize((round(im.width*ratio),round(im.height*ratio)),Image.Resampling.LANCZOS)
 canvas=Image.new('RGB',(w,h),'#060606');canvas.paste(im,((w-im.width)//2,(h-im.height)//2));return canvas
references={s['scene']:contained(frame(r/s['source'],1)) for s in shots if s['scene']!='install'}
results=[];cards=[]
for s in shots:
 for relative in [1.0,s['duration']/2,s['duration']-.6]:
  t=s['start']+relative;actual=frame(movie,t);expected=frame(r/s['source'],relative)
  top=390 if s['scene']=='install' else 290;height=540 if s['scene']=='install' else 720
  roi=actual.crop((36,top,1044,top+height))
  # Compare low-frequency image content, not Chrome/Pillow text anti-aliasing.
  smooth_roi=roi.filter(ImageFilter.GaussianBlur(1.5))
  # A 15 fps source is held between frames by the 30 fps composition. ffmpeg
  # seeks forward; accept at most one source-frame quantization difference.
  options=[]
  for offset in [-1/15,0,1/15]:
   canvas=contained(frame(r/s['source'],relative+offset),h=height)
   # CSS centers fractional contained widths; Pillow uses integer pixels.
   for dx in [-1,0,1]:
    for dy in [-1,0,1]:
     shifted=ImageChops.offset(canvas,dx,dy)
     options.append((sum(ImageStat.Stat(ImageChops.difference(smooth_roi,shifted.filter(ImageFilter.GaussianBlur(1.5)))).mean)/3,offset,dx,dy))
  diff,source_offset,dx,dy=min(options)
  assert diff<2.5,(t,s['scene'],diff)
  best=None
  if s['scene']!='install':
   distances={name:sum(ImageStat.Stat(ImageChops.difference(roi,ref)).mean)/3 for name,ref in references.items()}
   best=min(distances,key=distances.get)
  results.append({'time':round(t,4),'subject':s['scene'],'mean_pixel_difference':round(diff,4),'nearest_source':best,'source_time_offset_seconds':source_offset,'contain_rounding_pixels':[dx,dy],'passed':True})
  if relative==s['duration']/2:
   card=Image.new('RGB',(360,386),'#181818');card.paste(actual.resize((360,360)),(0,26));ImageDraw.Draw(card).text((6,6),f'{t:.2f}s {s["scene"]}',fill='white');cards.append(card)
sheet=Image.new('RGB',(1080,386*3),'#181818')
for i,card in enumerate(cards):sheet.paste(card,((i%3)*360,(i//3)*386))
sheet.save(r/'evidence/decoded-subjects.jpg');(r/'evidence/video-subject-verification.json').write_text(json.dumps({'ok':True,'checks':results,'method':'24 actual decoded frames compared with contained source images; mean RGB difference <2.5/255 after a 1.5-pixel anti-aliasing normalization against each scene’s actual time-matched source, allowing one 15 fps source-frame quantization interval and one pixel of CSS contain rounding. Nearest static source is diagnostic only, since recordings change over time.'},indent=2)+'\n');print('PASS 24 decoded source-match checks')
