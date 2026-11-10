"""Square, full-width evidence edit; one matched source per spoken subject."""
import pathlib,json,html
r=pathlib.Path(__file__).resolve().parents[1];story=json.loads((r/'story.json').read_text());voices={v['cue']:v for v in json.loads((r/'evidence/narration.json').read_text())}
D=story['duration'];intro=3.2;outro=7.2
scenes=[];start=intro;cues=[dict(voices['intro'],start=.65)]
for s in story['scenes']:
 duration=s['duration']
 assert voices[s['cue']]['duration']+.5<duration,(s['id'],voices[s['cue']]['duration'],duration)
 scenes.append(dict(s,start=round(start,4)));cues.append(dict(voices[s['cue']],start=round(start+.25,4)));start+=duration
assert abs(start-(D-outro))<.001
cues.append(dict(voices['outro'],start=D-outro+.35));timeline={'duration':D,'fps':30,'scenes':scenes,'cues':cues};(r/'timeline.json').write_text(json.dumps(timeline,indent=2)+'\n')
base='*{box-sizing:border-box}#root{position:absolute;inset:0;overflow:hidden;background:#060606;color:#f9f9f9;font-family:Inter,sans-serif}h1,p{margin:0}.headline{position:absolute;left:72px;top:112px;width:936px;font-size:61px;font-weight:600;line-height:1.12;letter-spacing:-2px}.frame{position:absolute;left:36px;top:290px;width:1008px;height:720px}.frame video{position:absolute;inset:0;width:100%;height:100%;object-fit:contain}.hint{position:absolute;left:108px;top:956px;width:864px;font-size:27px;color:#aaa}'
def compose(name,dur,body,css,js):
 (r/'compositions'/f'{name}.html').write_text(f'<template><style>{base}{css}</style><div id="root" data-composition-id="{name}" data-width="1080" data-height="1080" data-duration="{dur}">{body}</div><script>const tl=gsap.timeline({{paused:true}});{js}window.__timelines=window.__timelines||{{}};window.__timelines["{name}"]=tl;</script></template>')
manifest=[]
for s in scenes:
 name=s['id'];shot=s['shot'];source='assets/'+('install.mp4' if shot=='install' else 'approval.mp4' if shot=='approval' else f'workflow-{shot}.mp4')
 body='<h1 class="headline" data-var-text="'+name+'-title">'+html.escape(s['title']).replace('\n','<br>')+'</h1>'
 body+=f'<div class="frame"><video id="{name}-source" class="clip" muted src="{source}" data-var-src="{name}-source" data-start="0" data-duration="{s["duration"]}" data-hold="Evidence held for the matching narration"></video></div>'
 css='';body+='<div class="accent-line"></div>';css+='.accent-line{position:absolute;left:72px;top:255px;height:3px;width:150px;background:#eee;transform-origin:left center}'
 js="tl.fromTo('.headline',{y:16,opacity:0},{y:0,opacity:1,duration:.35,ease:'power3.out'},.08);tl.fromTo('.accent-line',{scaleX:0},{scaleX:1,duration:.6,ease:'power3.out'},.15);"
 if name=='pass':
  body+='<p class="scope">Same three checkout checks · tests unchanged</p>';css+='.scope{position:absolute;left:72px;top:220px;font-size:27px;color:#aaa}.accent-line{top:265px}'
 if name=='hook':
  body+='<p class="scope">Real Hermes session · waits condensed</p>';css+='.scope{position:absolute;left:72px;top:220px;font-size:27px;color:#aaa}.accent-line{top:265px}'
 if name=='install':
  body+='<p class="commands">hermes plugins install kujolang/kujo-hermes<br>hermes kujo setup --trust-workspace .</p><p class="hint">Requires Hermes + Kujo + Git · accept install prompts</p>'
  css+='.accent-line{display:none}.headline{font-size:56px;top:125px}.commands{position:absolute;left:108px;top:245px;width:864px;font-family:Departure,monospace;font-size:28px;line-height:1.8}.frame{top:390px;height:540px}.hint{font-size:29px}'
 compose(name,s['duration'],body,css,js)
 manifest.append({'scene':name,'start':s['start'],'duration':s['duration'],'cue':s['cue'],'source':source,'source_kind':'actual git diff of model edit' if name=='fix' else 'actual independent receipt verification' if name=='receipt' else 'actual checkout function capture' if name=='hook' else 'actual CLI capture' if name=='install' else 'original free local model approval' if name=='control' else 'actual local-model Hermes CLI capture','full_source_width':True})
for name,duration in [('intro',intro),('outro',outro)]:
 tag='Native tools. Real evidence.' if name=='intro' else 'Trust at the speed of AI'
 body=f'<div class="lockup" id="{name}-logos"><img src="assets/kujo-logomark.svg" alt="Official Kujo logo"><span class="times">×</span><img src="assets/hermes-logo.png" alt="Official Hermes logo"></div><h1 class="brand">Kujo Hermes</h1><p class="tag">{tag}</p>'
 if name=='outro':body+='<p class="cta">Install Kujo Hermes today.</p><p class="url">github.com/kujolang/kujo-hermes</p>'
 else:body+='<p class="version">v0.1.0 · Official release</p>'
 css='#root{background:#f9f9f9;color:#060606}.lockup{position:absolute;left:200px;top:260px;width:680px;display:flex;justify-content:center;align-items:center;gap:65px}.lockup img{width:190px;height:190px;object-fit:contain}.times{font-size:65px;color:#777}.brand{position:absolute;left:108px;top:505px;width:864px;text-align:center;font:80px Departure,monospace;letter-spacing:-3px}.tag{position:absolute;left:108px;top:635px;width:864px;text-align:center;font-size:41px;letter-spacing:-1px}.cta{position:absolute;left:108px;top:765px;width:864px;text-align:center;font-size:43px;font-weight:600}.url{position:absolute;left:108px;top:845px;width:864px;text-align:center;font:29px Departure,monospace;color:#444}.version{position:absolute;left:108px;top:820px;width:864px;text-align:center;font:28px Departure,monospace;color:#555}'
 js=f"tl.fromTo('#{name}-logos',{{scale:1.09}},{{scale:1,duration:.5,ease:'expo.out'}},0);tl.fromTo('.tag',{{opacity:0,y:14}},{{opacity:1,y:0,duration:.35,ease:'power3.out'}},.6);tl.to('#{name}-logos',{{x:12,duration:.033,repeat:1,yoyo:true,ease:'steps(1)'}},.18);"
 if name=='outro':js+="tl.fromTo('.cta',{opacity:0,y:12},{opacity:1,y:0,duration:.3,ease:'power3.out'},2.8);"
 compose(name,duration,body,css,js)
# Reuse the verified CMD transition recipe, including both bumper boundaries.
css="""@font-face{font-family:Departure;src:url('assets/DepartureMono-Regular.woff2')}*{box-sizing:border-box}html,body{margin:0;width:1080px;height:1080px;overflow:hidden;background:#060606}#root{position:relative;width:100%;height:100%}.glitch-cut{position:absolute;inset:0;z-index:20;overflow:hidden;pointer-events:none}.glitch-bar{position:absolute;left:-8%;width:116%;background:#eee;transform-origin:0 50%;opacity:0}.glitch-bar:nth-child(1){top:7%;height:7%}.glitch-bar:nth-child(2){top:23%;height:2.5%;background:#36efff}.glitch-bar:nth-child(3){top:42%;height:14%;background:#0b0b0e}.glitch-bar:nth-child(4){top:66%;height:4%;background:#ff3158}.glitch-bar:nth-child(5){top:84%;height:10%}.glitch-grid{position:absolute;inset:0;opacity:0;background-image:linear-gradient(#ffffff26 1px,transparent 1px);background-size:100% 8px}"""
root=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Kujo Hermes · Check the correction</title><script src="assets/gsap.min.js"></script><style>{css}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1080">'
for name,t,d in [('intro',0,intro)]+[(s['id'],s['start'],s['duration']) for s in scenes]+[('outro',D-outro,outro)]:
 root+=f'<div class="clip" id="{name}" data-composition-id="{name}" data-composition-src="compositions/{name}.html" data-start="{t}" data-duration="{d}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1080"></div>'
js='const tl=gsap.timeline({paused:true});'
for i,cut in enumerate([s['start'] for s in scenes]+[D-outro]):
 t=round(cut-.25,4);sel=f'#glitch-{i}'
 root+=f'<div class="clip glitch-cut" id="glitch-{i}" data-start="{t}" data-duration=".58" data-track-index="3" data-track-kind="graphics">'+''.join('<div class="glitch-bar" data-layout-ignore></div>' for _ in range(5))+'<div class="glitch-grid" data-layout-ignore></div></div>'
 js+=f"tl.fromTo('{sel} .glitch-bar',{{opacity:0,x:-220,scaleX:.28}},{{opacity:.74,x:120,scaleX:1,duration:.08,stagger:.025,ease:'steps(1)'}},{t}).to('{sel} .glitch-bar',{{x:-90,duration:.06,stagger:.018,ease:'steps(1)'}},{t+.15}).to('{sel} .glitch-bar',{{opacity:0,x:340,duration:.1,stagger:.012,ease:'power4.in'}},{t+.29}).fromTo('{sel} .glitch-grid',{{opacity:0,x:-18}},{{opacity:.5,x:18,duration:.05,repeat:5,yoyo:true,ease:'steps(1)'}},{t+.04}).to('{sel} .glitch-grid',{{opacity:0,duration:.08}},{t+.44});"
root+=f'<audio class="clip" id="master-audio" src="assets/master.m4a" data-start="0" data-duration="{D}" data-track-index="2"></audio></div><script>'+js+'window.__timelines=window.__timelines||{};window.__timelines.main=tl;</script></body></html>'
(r/'index.html').write_text(root);(r/'evidence/shot-map.json').write_text(json.dumps(manifest,indent=2)+'\n');print(D,'seconds;',len(scenes)+2,'scenes;',len(scenes)+1,'glitch transitions')
