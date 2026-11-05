"""Compare decoded delivery frames with the correct canonical-evidence screen.

Checks each subject midpoint and both sides of every narration-aligned internal
cut. Pixel comparison catches stale/wrong footage even when timing metadata is
correct. Screen content stays readable; the actual UI is never reconstructed.
"""
import io,json,pathlib,subprocess
from PIL import Image,ImageChops,ImageStat,ImageDraw
r=pathlib.Path(__file__).resolve().parents[1];out=r/'evidence/v5-decoded';out.mkdir(exist_ok=True)
shots=json.loads((r/'evidence/v5-shot-map.json').read_text());movie=r/'delivery/kujo-hermes-walkthrough.mp4'
def frame(file,t):
 return Image.open(io.BytesIO(subprocess.check_output(['ffmpeg','-nostdin','-v','error','-ss',str(t),'-i',str(file),'-frames:v','1','-f','image2pipe','-vcodec','png','-']))).convert('RGB')
checks=[(s['start']+s['duration']/2,s,'midpoint') for s in shots]
for i,s in enumerate(shots):
 if s['spoken_trigger']:
  checks.extend([(s['start']-.12,shots[i-1],'before '+s['spoken_trigger']),(s['start']+.12,s,'after '+s['spoken_trigger'])])
def contained(im):
 scale=min(1660/im.width,840/im.height)
 im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
 canvas=Image.new('RGB',(1660,840),'#060606');canvas.paste(im,((1660-im.width)//2,(840-im.height)//2));return canvas
references={s['shot']:contained(frame(r/s['clip'],1)) for s in shots}
results=[];cards=[]
for t,s,kind in checks:
 actual=frame(movie,t);expected=frame(r/s['clip'],max(0,t-s['start']))
 canvas=contained(expected)
 roi=actual.crop((130,180,1790,1020));difference=sum(ImageStat.Stat(ImageChops.difference(roi,canvas)).mean)/3
 distances={name:sum(ImageStat.Stat(ImageChops.difference(roi,ref)).mean)/3 for name,ref in references.items()}
 best=min(distances,key=distances.get)
 runner_up=min(value for name,value in distances.items() if name!=s['shot'])
 assert best==s['shot'],(t,'Wrong decoded subject',best,s['shot'],distances)
 assert difference<12 and runner_up>distances[s['shot']]*1.15,(t,s['shot'],difference,runner_up)
 results.append({'time':round(t,4),'expected_subject':s['shot'],'kind':kind,'mean_pixel_difference':round(difference,4),'threshold':12,'nearest_source':best,'nearest_wrong_source_difference':round(runner_up,4),'passed':True})
 card=Image.new('RGB',(480,295),'#181818');card.paste(actual.resize((480,270)),(0,25));ImageDraw.Draw(card).text((6,5),f'{t:.2f}s {kind}: {s["shot"]}',fill='white');cards.append(card)
sheet=Image.new('RGB',(1440,295*((len(cards)+2)//3)),'#181818')
for i,card in enumerate(cards):sheet.paste(card,((i%3)*480,(i//3)*295))
sheet.save(out/'subjects-and-boundaries.jpg')
(r/'evidence/v5-video-subject-verification.json').write_text(json.dumps({'ok':True,'decoded_checks':results,'method':'Mean absolute RGB difference of full contained screen versus source clip; threshold 12/255 plus correct nearest-source classification with a 15% margin over every wrong subject'},indent=2)+'\n')
print('PASS:',len(results),'decoded subject and narration-boundary comparisons')
