"""Build the benefits-led edit from verified recordings and measured narration.

Intro/outro are deliberately preserved. Editorial panels never impersonate Hermes.
The stepped slice gates adapt the user's CMD film (mcp@01a4f51).
"""
import json, pathlib, html
r=pathlib.Path(__file__).resolve().parents[1]
story=json.loads((r/'story.json').read_text())
voices={v['cue']:v for v in json.loads((r/'evidence/narration.json').read_text())}
spare=(80.33-3.8-sum(voices[s['cue']]['duration'] for s in story['scenes']))/8
assert spare>.5, 'Shorten narration; do not rush the voice to fit.'
start=3.8; scenes=[];cues=[dict(voices['intro'],start=.7)]
for s in story['scenes']:
 duration=voices[s['cue']]['duration']+spare
 scenes.append(dict(s,start=round(start,4),duration=round(duration,4)))
 cues.append(dict(voices[s['cue']],start=round(start+.3,4)));start+=duration
cues.append(dict(voices['outro'],start=80.33))
(r/'timeline.json').write_text(json.dumps({'duration':85,'fps':30,'cues':cues,'scenes':scenes},indent=2)+'\n')
receipt=json.loads(json.loads((r/'evidence/receipt-verification.json').read_text())['text'])
contract=json.loads((r/'evidence/demo-contract.json').read_text());criterion=html.escape(contract['acceptance_criteria'][0])
data=receipt['result']['structured']['data'];assert data['passed']==2 and data['failed']==0
base='''*{box-sizing:border-box}#root{position:absolute;inset:0;background:#060606;color:#f9f9f9;font-family:Inter,sans-serif;overflow:hidden}h1,h2,p{margin:0}.stage{position:absolute;inset:0}.eyebrow{position:absolute;left:130px;top:106px;font-size:32px;color:#bdbdbd}.title{position:absolute;left:130px;top:164px;font-size:78px;letter-spacing:-2.5px;line-height:1.12}.foot{position:absolute;left:130px;bottom:55px;font-size:28px;color:#aaa}.rail{position:absolute;left:130px;top:926px;width:1660px;display:flex;justify-content:space-between;font-family:Departure,monospace;font-size:29px;color:#9a9a9a}.rail span{padding-bottom:18px;border-bottom:3px solid #444}.rail .active{color:white;border-color:white}.paper{background:#f9f9f9;color:#090909}.muted{color:#bdbdbd}.mono{font-family:Departure,monospace}.rule{height:2px;background:#555}.row{font-size:48px}.check{font-family:Departure,monospace}'''
def rail(active):
 return '<div class="rail">'+''.join(f'<span class="{"active" if n<=active else ""}">{v}</span>' for n,v in enumerate(['Task','Context','Permission','Checks','Receipt']))+'</div>'
def panel(s,body,css,js,active=0,foot='Recorded evidence · editorial view · waiting time shortened'):
 name=s['id'];dur=s['duration'];
 out=f'''<template><style>{base}{css}</style><div id="root" data-composition-id="{name}" data-width="1920" data-height="1080" data-duration="{dur}"><div class="stage" id="{name}-stage">{body}</div>{rail(active)}<p class="foot">{foot}</p></div><script>const tl=gsap.timeline({{paused:true}});{js}window.__timelines=window.__timelines||{{}};window.__timelines['{name}']=tl;</script></template>'''
 (r/'compositions'/(name+'.html')).write_text(out)
def head(eye,title):return f'<p class="eyebrow">{eye}</p><h1 class="title">{title}</h1>'
def reveal(sel,t,x=0):return f"tl.fromTo('{sel}',{{opacity:0,x:{x}}},{{opacity:1,x:0,duration:.38,ease:'power4.out'}},{t});"
for s in scenes:
 n=s['id'];d=s['duration']
 if n=='question':
  b=head('You live in Hermes.','Make every run explainable.')+'<div id="question-prompt"><p>Before I commit,<br>what can I verify?</p><span>Example request to Hermes</span></div><div id="question-answers"><p id="q-ran">What ran?</p><p id="q-passed">What passed?</p><p id="q-approved">What did I approve?</p></div>'
  css='#question-prompt{position:absolute;left:130px;top:345px;width:860px;padding:55px 50px;border-left:6px solid white;background:#171717}#question-prompt p{font-size:70px;line-height:1.18;letter-spacing:-2px}#question-prompt span{display:block;font-size:28px;color:#aaa;margin-top:55px}#question-answers{position:absolute;left:1100px;top:375px}#question-answers p{font-size:46px;margin:0 0 62px}'
  js="tl.fromTo('#question-prompt',{scale:.96,x:-50},{scale:1,x:0,duration:.6,ease:'expo.out'},.08);"+reveal('#q-ran',3.4,20)+reveal('#q-passed',4.8,20)+reveal('#q-approved',6,20)
  panel(s,b,css,js,0,'Kujo Hermes · native developer tools and execution evidence')
 elif n=='context':
  b=head('Start with the task.','Give the work a clear contract.')+'<section id="contract"><p class="mono">Python demo repository</p><h2>Spec</h2><p class="statement">'+criterion+'</p><p id="contract-ok" class="status">VALID · 0 ERRORS</p></section><div id="handoff-arrow">→</div><section id="pack"><h2>PackWrite</h2><p class="statement">Execution context</p><div class="phase-track">'+''.join(f'<span id="phase-{i}">{i+1}</span>' for i in range(7))+'</div><p id="pack-ok" class="status">7 PHASES · NO MISSING FILES</p></section>'
  css='#contract{position:absolute;left:130px;top:345px;width:700px;padding:42px;background:#f9f9f9;color:#090909}#contract .mono{font-size:29px;margin-bottom:30px}#contract h2,#pack h2{font-size:70px;letter-spacing:-2px}.statement{font-size:40px;margin-top:18px}.status{font-family:Departure,monospace;font-size:28px;margin-top:45px}#handoff-arrow{position:absolute;left:887px;top:494px;font-size:80px}#pack{position:absolute;left:1030px;top:390px;width:760px}.phase-track{display:flex;gap:14px;margin-top:30px}.phase-track span{width:70px;height:58px;border-bottom:3px solid white;font-size:32px;text-align:center;padding-top:5px}'
  js="tl.fromTo('#contract',{x:-50,opacity:0},{x:0,opacity:1,duration:.5,ease:'expo.out'},.15);"+reveal('#contract-ok',3.1)+reveal('#handoff-arrow',4.2)+reveal('#pack',4.5,25)+''.join(reveal(f'#phase-{i}',5.2+i*.18) for i in range(7))+reveal('#pack-ok',7)
  panel(s,b,css,js,1)
 elif n=='routing':
  b=head('Ask for the outcome.','Stay in the Hermes conversation.')+'<div class="route-source" id="route-source"><strong>Hermes</strong><p>Discover → inspect → execute</p><span>Six native tools</span></div><div id="route-wire"></div><section id="ability"><p class="mono">Kujo Ability</p><h2>Eval</h2><p>Run the repository checks</p><div id="schema"><span>workspace</span><span>arguments</span><span>approval policy</span></div></section><p id="route-note">51 catalog bindings. Schemas loaded when needed.</p>'
  css='.route-source{position:absolute;left:130px;top:370px;width:755px;height:270px;padding:40px;background:#f9f9f9;color:#080808}.route-source strong{font-size:76px;letter-spacing:-2px}.route-source p{font-size:35px;margin-top:15px}.route-source span{font-size:28px;display:block;margin-top:23px}#route-wire{position:absolute;left:885px;top:505px;width:145px;height:4px;background:white;transform-origin:left}#ability{position:absolute;left:1070px;top:350px;width:720px}#ability .mono{font-size:28px;color:#bcbcbc}#ability h2{font-size:92px;margin-top:12px}#ability p:not(.mono){font-size:38px;margin-top:12px}#schema{display:flex;gap:20px;flex-wrap:wrap;margin-top:35px}#schema span{font-size:28px;border-bottom:2px solid #666;padding-bottom:12px}#route-note{position:absolute;left:130px;top:770px;font-size:43px;color:#ccc}'
  js=reveal('#route-source',.15,-35)+"tl.fromTo('#route-wire',{scaleX:0},{scaleX:1,duration:.45,ease:'power2.inOut'},2);"+reveal('#ability',2.3,30)+reveal('#schema',4.6)+reveal('#route-note',6)
  panel(s,b,css,js,1,'Catalog and routing explained · included bindings depend on installed prerequisites')
 elif n=='control':
  b=head('Your workspace. Your decision.','Approve this run in Hermes.')+f'<div id="approval-crop"><video muted class="clip" id="approval-recording" data-start="0" data-duration="{d}" src="assets/approval.mp4"></video></div><p id="control-callout">Eval runs commands and writes evidence.</p>'
  css='#approval-crop{position:absolute;left:130px;top:295px;width:1660px;height:500px;overflow:hidden}#approval-recording{position:absolute;width:2100px;height:980px;left:-24px;top:-15px;object-fit:fill}#control-callout{position:absolute;left:130px;top:825px;font-size:37px;color:#ccc}'
  js="tl.fromTo('#approval-crop',{scale:.96},{scale:1,duration:.55,ease:'expo.out'},.05);"+reveal('#control-callout',3.8)
  panel(s,b,css,js,2,'Actual Hermes approval · local Qwen3.5 4B · waiting time shortened')
 elif n=='checks':
  b=head('Permission becomes a recorded run.','See exactly what passed.')+'<section id="suite"><div id="test-one"><span>✓</span><h2>Unit test</h2><p class="mono">python3 -m unittest discover -s tests</p></div><div id="test-two"><span>✓</span><h2>Implementation exists</h2><p class="mono">calculator.py</p></div></section><div id="counts"><strong>2 / 2</strong><p>checks passed</p><span>0 failed</span></div>'
  css='#suite{position:absolute;left:130px;top:345px;width:1030px}#suite>div{position:relative;padding:28px 0 34px 75px;border-bottom:2px solid #444;margin-bottom:30px}#suite span{position:absolute;left:0;top:30px;font-size:52px}#suite h2{font-size:52px;letter-spacing:-1px}#suite p{font-size:29px;margin-top:23px;color:#bdbdbd}#counts{position:absolute;left:1270px;top:390px}#counts strong{font-size:130px;font-family:Departure,monospace;font-weight:400;letter-spacing:-10px}#counts p{font-size:43px;margin-top:20px}#counts>span{display:block;font-size:32px;margin-top:30px;color:#bdbdbd}'
  js=reveal('#test-one',.6,-25)+reveal('#test-two',3.1,-25)+"tl.fromTo('#counts',{opacity:0,scale:.9},{opacity:1,scale:1,duration:.5,ease:'expo.out'},4.8);"
  panel(s,b,css,js,3,'Actual Eval results · passing these checks does not establish release readiness')
 elif n=='evidence':
  b=head('The result stays attached to its evidence.','Open the receipt. Trace the run.')+'<section id="receipt"><div id="receipt-top"><span class="mono">EXECUTION RECEIPT</span><strong>Eval</strong></div><div id="receipt-command" class="receipt-row"><span>Command</span><p class="mono">kujo run …/eval/main.kujo … --json</p></div><div id="receipt-permission" class="receipt-row"><span>Approval</span><p>Required · approved</p></div><div id="receipt-hash" class="receipt-row"><span>Evidence</span><p>10 artifact hashes · SHA-256</p></div></section><div id="verified"><span>✓</span><h2>Integrity<br>verified</h2><p>Match the receipt<br>to this execution.</p></div><p id="receipt-id" class="mono">'+html.escape(receipt['receipt_id'])+'</p>'
  css='#receipt{position:absolute;left:130px;top:315px;width:1050px;background:#f9f9f9;color:#090909;padding:34px 40px}#receipt-top{display:flex;justify-content:space-between;align-items:center;border-bottom:2px solid #aaa;padding-bottom:25px}#receipt-top span{font-size:28px}#receipt-top strong{font-size:48px}.receipt-row{padding-top:24px;display:flex;gap:30px;align-items:baseline}.receipt-row>span{font-size:29px;width:170px}.receipt-row p{font-size:34px}.receipt-row .mono{font-size:28px}#verified{position:absolute;left:1270px;top:365px}#verified>span{font-size:60px}#verified h2{font-size:65px;line-height:1.04;margin:18px 0 28px;letter-spacing:-1px}#verified p{font-size:32px;line-height:1.4;color:#bbb}#receipt-id{position:absolute;left:170px;top:785px;font-size:29px;color:#aaa}'
  js="tl.fromTo('#receipt',{y:40,opacity:0},{y:0,opacity:1,duration:.5,ease:'expo.out'},.1);"+reveal('#receipt-command',2.0)+reveal('#receipt-permission',3.3)+reveal('#receipt-hash',4.6)+reveal('#verified',6.7,20)+reveal('#receipt-id',7.4)
  panel(s,b,css,js,4,'Actual receipt fields · command abbreviated · integrity is not a guarantee of correctness')
 elif n=='tools':
  b=head('Extend the same workflow.','One integration. A wider toolbox.')+'<div id="tool-stage">'
  groups=[('ShipCheck','Check release readiness','Eval · Spec · PatchBrief · ChangeBucket · Lens'),('Scout','Find repository context','PackWrite · Scent · RAG · Concord'),('Dispatch','Run and trace workflows','Workcell · Loop · RunLedger · Watchdog')]
  js=''
  for i,(tool,benefit,more) in enumerate(groups):
   t=i*d/3
   b+=f'<div class="clip tool-page" id="tool-page-{i}" data-start="{t}" data-duration="{d/3}"><div class="tool-copy"><h2>{tool}</h2><p>{benefit}</p><span>{more}</span></div></div>'
   js+=f"tl.fromTo('#tool-page-{i} .tool-copy',{{x:100,opacity:0}},{{x:0,opacity:1,duration:.45,ease:'expo.out'}},{t+.1});"
  b+='</div><p id="tools-note">Discover what is installed. Inspect what it can do.</p>'
  css='#tool-stage{position:absolute;left:130px;top:350px;width:1660px;height:420px}.tool-page{position:absolute;inset:0}.tool-copy h2{font-size:126px;letter-spacing:-5px}.tool-copy p{font-size:56px;margin-top:22px}.tool-copy span{display:block;font-size:32px;color:#bbb;margin-top:45px}#tools-note{position:absolute;left:130px;top:822px;font-size:35px;color:#bbb}'
  panel(s,b,css,js,4,'Included tools, not additional demo runs · each retains its dependencies and permissions')
 else:
  b=head('For developers who work inside Hermes.','Keep the speed. Keep the evidence.')+'<div id="handoff"><p class="mono">A handoff the next developer can inspect</p><div id="handoff-line-one"><span>Task</span><strong>Contract + context</strong></div><div id="handoff-line-two"><span>Run</span><strong>Permission + checks</strong></div><div id="handoff-line-three"><span>Evidence</span><strong>Verified receipt</strong></div></div><p id="payoff-end">Accountability inside Hermes.</p>'
  css='#handoff{position:absolute;left:130px;top:325px;width:1660px}#handoff>p{font-size:30px;color:#bdbdbd;margin-bottom:40px}#handoff>div{display:flex;gap:80px;border-bottom:1px solid #555;padding:17px 0}#handoff span{font-size:36px;width:220px;color:#bbb}#handoff strong{font-size:46px;font-weight:500}#payoff-end{position:absolute;left:130px;top:805px;font-size:50px}'
  js=reveal('#handoff',.1)+reveal('#handoff-line-one',.5,-20)+reveal('#handoff-line-two',2.2,-20)+reveal('#handoff-line-three',4.1,-20)+reveal('#payoff-end',6.7)
  panel(s,b,css,js,4,'Install Kujo Hermes · configure trusted roots · bring your repository')
# Original bumper compositions are intentionally untouched.
hosts=[('intro',0,3.8)]+[(s['id'],s['start'],s['duration']) for s in scenes]+[('outro',80.33,4.67)]
# Five stepped slice gates from the actual CMD film. A subdued chromatic accent
# appears only at seams; stable reading frames remain monochrome.
gates=[s['start'] for s in scenes[1:]]
css='''@font-face{font-family:Departure;src:url('assets/DepartureMono-Regular.woff2')}*{box-sizing:border-box}html,body{margin:0;width:1920px;height:1080px;overflow:hidden;background:#060606}#root{position:relative;width:100%;height:100%}.glitch-cut{position:absolute;inset:0;z-index:20;overflow:hidden;pointer-events:none}.glitch-bar{position:absolute;left:-8%;width:116%;background:#eee;transform-origin:0 50%;opacity:0}.glitch-bar:nth-child(1){top:7%;height:7%}.glitch-bar:nth-child(2){top:23%;height:2.5%;background:#36efff}.glitch-bar:nth-child(3){top:42%;height:14%;background:#0b0b0e}.glitch-bar:nth-child(4){top:66%;height:4%;background:#ff3158}.glitch-bar:nth-child(5){top:84%;height:10%}.glitch-grid{position:absolute;inset:0;opacity:0;background-image:linear-gradient(#ffffff26 1px,transparent 1px);background-size:100% 8px}'''
root=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Kujo Hermes · Accountability inside Hermes</title><script src="assets/gsap.min.js"></script><style>{css}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="85" data-width="1920" data-height="1080">'
for name,t,d in hosts:root+=f'<div class="clip" id="{name}" data-composition-id="{name}" data-composition-src="compositions/{name}.html" data-start="{t}" data-duration="{d}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080"></div>'
js='const tl=gsap.timeline({paused:true});'
for i,cut in enumerate(gates):
 t=round(cut-.25,4);sel=f'#glitch-{i}'
 root+=f'<div class="clip glitch-cut" id="glitch-{i}" data-start="{t}" data-duration=".58" data-track-index="3" data-track-kind="graphics">'+''.join('<div class="glitch-bar" data-layout-ignore></div>' for _ in range(5))+'<div class="glitch-grid" data-layout-ignore></div></div>'
 js+=f"tl.fromTo('{sel} .glitch-bar',{{opacity:0,x:-220,scaleX:.28}},{{opacity:.74,x:120,scaleX:1,duration:.08,stagger:.025,ease:'steps(1)'}},{t}).to('{sel} .glitch-bar',{{x:-90,duration:.06,stagger:.018,ease:'steps(1)'}},{t+.15}).to('{sel} .glitch-bar',{{opacity:0,x:340,duration:.1,stagger:.012,ease:'power4.in'}},{t+.29}).fromTo('{sel} .glitch-grid',{{opacity:0,x:-18}},{{opacity:.5,x:18,duration:.05,repeat:5,yoyo:true,ease:'steps(1)'}},{t+.04}).to('{sel} .glitch-grid',{{opacity:0,duration:.08}},{t+.44});"
root+='<audio class="clip" id="master-audio" src="assets/master.m4a" data-start="0" data-duration="85" data-track-index="2"></audio></div><script>'+js+'window.__timelines=window.__timelines||{};window.__timelines.main=tl;</script></body></html>'
(r/'index.html').write_text(root)
print('Built 10 scenes; preserved bumpers; 7 CMD-style glitch seams; 85 seconds.')
for s in scenes:print(s['id'],s['start'],s['duration'])
