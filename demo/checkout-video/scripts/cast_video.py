"""Cut and replay real terminal states; edit windows are explicit source timestamps."""
import argparse,json,pathlib,subprocess,copy
import pyte
from terminal_text import replay_text
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser();p.add_argument('cast');p.add_argument('--windows',required=True,help='JSON [[source_start,source_end,screen_seconds],...]');p.add_argument('--output',required=True);a=p.parse_args()
lines=[json.loads(l) for l in pathlib.Path(a.cast).read_text().splitlines()];head=lines[0];events=[e for e in lines[1:] if e[1]=='o'];windows=json.loads(a.windows);fps=15
screen=pyte.Screen(head['width'],head['height']);stream=pyte.Stream(screen);size=min(40,round(972/(head['width']*.602)));font=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',size);cw=font.getlength('M');lh=size+2;w=1080;h=744;left=round((w-cw*head['width'])/2);top=max(24,(h-lh*head['height'])//2)
colors={'default':'#f4f4f4','black':'#060606','red':'#e77575','green':'#9fd99b','brown':'#e0c484','blue':'#9bb9df','magenta':'#c5a8d9','cyan':'#9dd9d9','white':'#e7e7e7','brightblack':'#999999','brightwhite':'#ffffff'}
def color(v):return colors.get(v,'#'+v if len(v)==6 else '#f4f4f4')
def draw():
 im=Image.new('RGB',(w,h),'#060606');d=ImageDraw.Draw(im)
 for y,line in screen.buffer.items():
  for x,c in line.items():
   if c.data.strip(): d.text((left+x*cw,top+y*lh),c.data,font=font,fill=color(c.fg))
 return im.tobytes()
cmd=['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{w}x{h}','-r',str(fps),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',a.output]
proc=subprocess.Popen(cmd,stdin=subprocess.PIPE);idx=0;last=None;buffer=None
for start,end,duration in windows:
 assert end>=start and start>=0
 for frame in range(round(duration*fps)):
  t=start+(end-start)*frame/max(1,round(duration*fps)-1)
  while idx<len(events) and events[idx][0]<=t:stream.feed(replay_text(events[idx][2]));idx+=1
  state=tuple(screen.display)
  if state!=last:buffer=draw();last=state
  proc.stdin.write(buffer)
proc.stdin.close();assert proc.wait()==0
pathlib.Path(a.output+'.edits.json').write_text(json.dumps({'source':a.cast,'windows':windows,'duration':sum(x[2] for x in windows),'note':'Actual captured terminal output. Playback is condensed; holds and cuts are editorial.'},indent=2)+'\n')
