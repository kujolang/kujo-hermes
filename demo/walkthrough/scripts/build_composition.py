"""Build editable scenes from recorded terminal frames and the real catalog."""
import pathlib,json,html
r=pathlib.Path(__file__).resolve().parents[1];timeline=json.loads((r/'timeline.json').read_text());cues={c['cue']:c for c in timeline['cues']};(r/'compositions').mkdir(exist_ok=True)
base='''*{box-sizing:border-box}#root{position:absolute;inset:0;background:#060606;color:#f9f9f9;font-family:Inter,sans-serif;overflow:hidden}h1{position:absolute;left:96px;top:45px;margin:0;font-size:62px;font-weight:700;letter-spacing:-2px}.screen{position:absolute;left:60px;top:150px;width:1800px;height:840px;object-fit:contain}.note{position:absolute;left:96px;bottom:28px;margin:0;font-size:28px;color:#bababa}.line{position:absolute;left:96px;top:130px;width:1728px;height:2px;background:#505050}'''
def scene(name,body,css='',js='',duration=5):
 content=f'''<template><style>{base}{css}</style><div id="root" data-composition-id="{name}" data-width="1920" data-height="1080" data-duration="{duration}">{body}</div><script>const tl=gsap.timeline({{paused:true}});{js}window.__timelines=window.__timelines||{{}};window.__timelines['{name}']=tl;</script></template>'''
 (r/'compositions'/(name+'.html')).write_text(content)
# Registry logo-sting scale landing adapted to two official marks, without decorative rings.
for name,duration in [('intro',3.8),('outro',4.67)]:
 content=f'''<div class="clip" id="{name}-plate" data-start="0" data-duration="{duration}"><div class="lockup" id="{name}-logos"><img src="assets/kujo-logomark.svg" alt="Official Kujo logo"><strong>Kujo</strong><span class="times">×</span><img src="assets/hermes-logo.png" alt="Official Hermes logo"><strong>Hermes</strong></div><p class="tag" id="{name}-tag">{'Native tools. Real evidence.' if name=='intro' else 'Trust at the speed of AI'}</p><p class="url">{'Kujo Hermes · v0.1.0' if name=='intro' else 'github.com/kujolang/kujo-hermes'}</p></div>'''
 css='''#root{background:var(--paper,#f9f9f9);color:#060606}.lockup{position:absolute;left:190px;top:345px;width:1540px;height:250px;display:flex;align-items:center;justify-content:center;gap:38px}.lockup img{width:225px;height:225px;object-fit:contain}.lockup strong{font-family:Departure,monospace;font-size:112px;font-weight:400}.times{font-size:68px;color:#737373;margin:0 12px}.tag{position:absolute;left:150px;top:665px;width:1620px;text-align:center;font-size:48px;letter-spacing:-1px}.url{position:absolute;left:150px;top:825px;width:1620px;text-align:center;font-size:30px;color:#505050}'''
 js=f"tl.fromTo('#{name}-logos',{{scale:1.09}},{{scale:1,duration:.5,ease:'expo.out'}},0);tl.fromTo('#{name}-tag',{{opacity:0,y:14}},{{opacity:1,y:0,duration:.35,ease:'power3.out'}},.8);"
 # Short bounded whole-lockup offsets retain official mark proportions.
 for t in [.18,.34]:js+=f"tl.to('#{name}-logos',{{x:12,duration:.033,repeat:1,yoyo:true,ease:'steps(1)'}},{t});"
 scene(name,content,css,js,duration)
shots=[('setup','Start with your repository','doctor-0.png',3.8,12.07),('discover','Discover the right tool','discover-0.png',12.07,23.86),('request','Ask Hermes in plain English','checks-0.png',23.86,32.93),('approval','Approve what changes state','approval.mp4',32.93,42.64),('proof','Trace the result to its receipt','eval-result.png',42.64,53.79)]
for name,title,file,start,end in shots:
 duration=end-start
 body=f'<h1 id="{name}-title">{title}</h1><div class="line"></div><img class="screen clip" id="{name}-screen" data-start="0" data-duration="{duration}" src="assets/{file}" alt="Actual recorded Hermes CLI"><p class="note">Actual Hermes CLI · local Qwen3.5 4B · waiting time shortened</p>'
 js=f"tl.fromTo('#{name}-title',{{opacity:0,x:-14}},{{opacity:1,x:0,duration:.25,ease:'power3.out'}},0);"
 if name=='setup':
  body=body.replace('Actual Hermes CLI · local Qwen3.5 4B · waiting time shortened','Actual Hermes plugin doctor · six registered native tools')
  body=body.replace('<img class="screen clip"', '<img style="top:520px;height:330px;object-fit:cover;object-position:top" class="screen clip"')
  body+='<p style="position:absolute;left:150px;top:190px;font-size:48px;line-height:1.5">Install the plugin.<br>Configure your trusted repository.<br>Ask Hermes to run your checks.</p>'
 elif file.endswith('.mp4'):
  body=body.replace('<img class="screen clip"','<video muted class="screen clip"').replace('alt="Actual recorded Hermes CLI">','></video>')
 scene(name,body,js=js,duration=duration)
# Display the recorded tool response, not an unverified model paraphrase.
if (r/'evidence/discover-session.json').exists():
 data=json.loads((r/'evidence/discover-session.json').read_text())
 actual=next(json.loads(m['content']) for m in data['messages'] if m.get('tool_name')=='kujo_discover')
 wanted=['kujo.shipcheck.repository.scan','kujo.packwrite.pack.summary','kujo.spec.contract.validate','kujo.eval.suite.run']
 available={x['id']:x for x in actual['abilities']}
 rows=''.join(f'<p>{html.escape(k)}</p>' for k in wanted if k in available)
 body='<h1>Discover the right tool</h1><div class="line"></div><video muted class="screen clip" id="discovery-call" data-start="0" data-duration="1.8" src="assets/discover.mp4"></video><section class="catalog clip" id="catalog-result" data-start="1.8" data-duration="9.99"><h2>Recorded catalog result · 51 bindings</h2>'+rows+'</section><p class="note">Actual Hermes tool response · excerpt · local Qwen3.5 4B</p>'
 scene('discover',body,'.catalog{position:absolute;left:150px;top:190px}.catalog h2{font-size:40px;color:#aaa;font-weight:400;margin-bottom:65px}.catalog p{font-family:Departure,monospace;font-size:48px;margin:44px 0}',"tl.fromTo('#catalog-result p',{opacity:0,y:10},{opacity:1,y:0,duration:.25,stagger:.2},1.8);",11.79)

if (r/'evidence/checks-session.json').exists():
 data=json.loads((r/'evidence/checks-session.json').read_text())
 actual={d['ability_id']:d for m in data['messages'] if m.get('tool_name')=='kujo_execute' for d in [json.loads(m['content'])] if d.get('ok')}
 spec=actual['kujo.spec.contract.validate']['result']['structured'];pack=actual['kujo.packwrite.pack.summary']['result']['structured']
 assert spec['valid'] and not spec['errors'] and pack['ok'] and not pack['missing_files']
 body='<h1>Validate requirements and context</h1><div class="line"></div><video muted class="screen clip" id="checks-call" data-start="0" data-duration="3" src="assets/checks.mp4"></video><section class="result clip" id="checks-result" data-start="3" data-duration="6.07"><h2>Recorded tool results</h2><p>Spec: valid. Zero errors.</p><p>PackWrite: '+str(pack['phase_count'])+' phases.</p><span>No missing context files.</span></section><p class="note">Actual Kujo results through Hermes · excerpt · waiting time shortened</p>'
 scene('request',body,'.result{position:absolute;left:150px;top:200px}.result h2{font-size:40px;color:#aaa;font-weight:400;margin-bottom:65px}.result p{font-size:68px;font-weight:700;margin:45px 0}.result span{font-size:44px;color:#ccc}',"tl.fromTo('#checks-result p',{opacity:0,y:10},{opacity:1,y:0,duration:.25,stagger:.2},3);",9.07)

if (r/'evidence/receipt-verification.json').exists():
 response=json.loads((r/'evidence/receipt-verification.json').read_text());receipt=json.loads(response['text'])
 assert response['verified'] and receipt['approval']['approved'] and receipt['status']=='completed'
 result=receipt['result']['structured']['data']
 body=f'<h1>Trace the result to its receipt</h1><div class="line"></div><section class="proof"><h2>Eval: {result["passed"]} passed. {result["failed"]} failed.</h2><p class="verified">Receipt integrity verified by Kujo Hermes</p><p>Ability: {receipt["ability_id"]}</p><p>Receipt: {receipt["receipt_id"]}</p><p class="command">Command excerpt: kujo run …/eval/main.kujo --interpreter -- run … --json</p><p class="hash">SHA-256: {receipt["receipt_digest"]}</p></section><p class="note">Recorded tool response · integrity verification does not establish release readiness</p>'
 scene('proof',body,'.proof{position:absolute;left:150px;top:185px;width:1620px}.proof h2{font-size:76px;margin:25px 0 45px}.proof p{font-family:Departure,monospace;font-size:36px;margin:38px 0}.proof .verified{font-family:Inter,sans-serif;font-size:44px;color:#ddd;margin-bottom:60px}.proof .command,.proof .hash{font-size:30px;color:#bbb}',"tl.fromTo('.proof h2',{opacity:0,y:10},{opacity:1,y:0,duration:.3},0);",11.15)

# Tool families are editorial labels derived from the actual bundled catalog.
groups=[('Check the change','ShipCheck · Eval · Spec','PatchBrief · ChangeBucket · Lens'),('Understand the repository','Scout · PackWrite · Scent','RAG · Concord'),('Run and trace the work','Dispatch · Workcell · Loop','RunLedger · Watchdog · Muzzle · Howl')]
body='<h1>51 bindings. Six native tools.</h1><div class="line"></div>'
js=''
for i,(title,a,b) in enumerate(groups):
 start=i*5.05;duration=5.05 if i<2 else 5.13
 body+=f'<section class="family clip" id="family-{i}" data-start="{start}" data-duration="{duration}"><h2>{title}</h2><p>{a}</p><p>{b}</p></section>'
 js+=f"tl.fromTo('#family-{i} p',{{opacity:0,x:22}},{{opacity:1,x:0,duration:.3,stagger:.15,ease:'power3.out'}},{start+.15});"
body+='<p class="note">Included bindings · availability depends on installed tools and prerequisites</p>'
scene('breadth',body,'.family{position:absolute;left:150px;top:240px;width:1620px}.family h2{font-size:48px;color:#aaa;font-weight:400;margin:0 0 65px}.family p{font-size:66px;font-weight:700;line-height:1.35;margin:25px 0}',js,15.23)
body='<h1>Less memorizing. More verifying.</h1><div class="line"></div><div id="benefit-copy"><p>Ask for the outcome.</p><p>Run repeatable checks.</p><p>Keep the execution evidence.</p></div><p class="note">Install Kujo Hermes → configure trusted roots → ask Hermes</p>'
scene('benefit',body,'#benefit-copy{position:absolute;left:150px;top:240px}#benefit-copy p{font-size:72px;line-height:1.35;font-weight:700;margin:35px 0}',"tl.fromTo('#benefit-copy p',{opacity:0,x:25},{opacity:1,x:0,duration:.4,stagger:2.8,ease:'power3.out'},.3);",11.31)
hosts=[('intro',0,3.8)]+[(n,s,e-s) for n,_,_,s,e in shots]+[('breadth',53.79,15.23),('benefit',69.02,11.31),('outro',80.33,4.67)]
root='''<!doctype html><html lang="en" data-composition-variables='[{"id":"paper","label":"Paper color","type":"color","default":"#f9f9f9"}]'><head><meta charset="utf-8"><title>Kujo Hermes walkthrough</title><script src="assets/gsap.min.js"></script><style>@font-face{font-family:Departure;src:url('assets/DepartureMono-Regular.woff2')}*{box-sizing:border-box}html,body{margin:0;width:1920px;height:1080px;overflow:hidden;background:#060606}#root{position:relative;width:100%;height:100%}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="85" data-width="1920" data-height="1080">'''
for name,start,duration in hosts:root+=f'<div class="clip" id="{name}" data-composition-id="{name}" data-composition-src="compositions/{name}.html" data-start="{start}" data-duration="{duration}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080"></div>'
root+='<audio class="clip" id="master-audio" src="assets/master.m4a" data-start="0" data-duration="85" data-track-index="2"></audio></div><script>window.__timelines=window.__timelines||{};window.__timelines.main=gsap.timeline({paused:true});</script></body></html>'
(r/'index.html').write_text(root)
print('Built',len(hosts),'editable scenes; 85 seconds')
