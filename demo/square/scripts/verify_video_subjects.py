"""Compare decoded square frames to each actual source; catch reused/wrong screens."""
import io,json,pathlib,subprocess
from PIL import Image,ImageChops,ImageStat,ImageDraw
r=pathlib.Path(__file__).resolve().parents[1];shots=json.loads((r/'evidence/shot-map.json').read_text());movie=r/'delivery/kujo-hermes-square.mp4'
def frame(file,t):
 duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(file)],text=True))
 t=max(0,min(t,duration-.1))
 return Image.open(io.BytesIO(subprocess.check_output(['ffmpeg','-nostdin','-v','error','-ss',str(t),'-i',str(file),'-frames:v','1','-f','image2pipe','-vcodec','png','-']))).convert('RGB')
def contained(im,w=972,h=570):
 ratio=min(w/im.width,h/im.height);im=im.resize((round(im.width*ratio),round(im.height*ratio)),Image.Resampling.LANCZOS)
 canvas=Image.new('RGB',(w,h),'#060606');canvas.paste(im,((w-im.width)//2,(h-im.height)//2));return canvas
references={s['scene']:contained(frame(r/s['source'],1)) for s in shots if s['scene']!='install'}
results=[];cards=[]
for s in shots:
 for relative in [1.0,s['duration']/2,s['duration']-.6]:
  t=s['start']+relative;actual=frame(movie,t);expected=frame(r/s['source'],relative)
  top=390 if s['scene']=='install' else 345;height=540 if s['scene']=='install' else 570
  roi=actual.crop((54,top,1026,top+height));canvas=contained(expected,h=height)
  diff=sum(ImageStat.Stat(ImageChops.difference(roi,canvas)).mean)/3
  assert diff<12,(t,s['scene'],diff)
  best=None
  if s['scene']!='install':
   distances={name:sum(ImageStat.Stat(ImageChops.difference(roi,ref)).mean)/3 for name,ref in references.items()}
   best=min(distances,key=distances.get);assert best==s['scene'],(t,'Wrong source',best,s['scene'])
  results.append({'time':round(t,4),'subject':s['scene'],'mean_pixel_difference':round(diff,4),'nearest_source':best,'passed':True})
  if relative==s['duration']/2:
   card=Image.new('RGB',(360,386),'#181818');card.paste(actual.resize((360,360)),(0,26));ImageDraw.Draw(card).text((6,6),f'{t:.2f}s {s["scene"]}',fill='white');cards.append(card)
sheet=Image.new('RGB',(1080,386*3),'#181818')
for i,card in enumerate(cards):sheet.paste(card,((i%3)*360,(i//3)*386))
sheet.save(r/'evidence/decoded-subjects.jpg');(r/'evidence/video-subject-verification.json').write_text(json.dumps({'ok':True,'checks':results,'method':'27 actual decoded frames compared with contained source images; mean RGB difference <12/255 and correct nearest distinct source for native views.'},indent=2)+'\n');print('PASS 27 decoded source-match checks')
