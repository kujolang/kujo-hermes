"""Render actual recorded terminal cells; never generate or replace terminal text."""
import argparse,json,pathlib
import pyte
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser();p.add_argument('cast');p.add_argument('--times',nargs='*',type=float);p.add_argument('--prefix');args=p.parse_args()
path=pathlib.Path(args.cast);lines=[json.loads(x) for x in path.read_text().splitlines()];head=lines[0];events=lines[1:];screen=pyte.Screen(head['width'],head['height']);stream=pyte.Stream(screen)
font=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',30 if head['width']<=96 else 28);cw=font.getlength('M');lh=32;w=1800;h=840;left=round((w-cw*head['width'])/2);top=24
out=path.parents[2]/'assets';times=args.times or [events[-1][0]];index=0;results=[]
colors={'default':'#f4f4f4','black':'#060606','red':'#e77575','green':'#9fd99b','brown':'#e0c484','blue':'#9bb9df','magenta':'#c5a8d9','cyan':'#9dd9d9','white':'#e7e7e7','brightblack':'#999999','brightwhite':'#ffffff'}
def color(v):return colors.get(v,'#'+v if len(v)==6 else '#f4f4f4')
def save(t):
 im=Image.new('RGB',(w,h),'#060606');draw=ImageDraw.Draw(im)
 for y,line in screen.buffer.items():
  for x,c in line.items():
   if not c.data.strip():continue
   draw.text((left+x*cw,top+y*lh),c.data,font=font,fill=color(c.fg),stroke_width=0)
 name=(args.prefix or path.stem)+'-'+str(len(results))+'.png';im.save(out/name)
 results.append({'file':'assets/'+name,'capture':str(path),'raw_time':t,'text':'\n'.join(screen.display)})
for e in events:
 while index<len(times) and e[0]>times[index]:save(times[index]);index+=1
 if e[1]=='o':stream.feed(e[2])
while index<len(times):save(times[index]);index+=1
(path.parent/(path.stem+'-frames.json')).write_text(json.dumps(results,indent=2)+'\n');print(json.dumps([{k:v for k,v in x.items() if k!='text'} for x in results]))
