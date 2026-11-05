/** Record real evidence files in the official Hermes Desktop webapp.
 * Uses visible native controls, never injected chat messages or DOM replacement.
 * Run from repo root. The authenticated browser state stays in ignored .local/.
 */
const {chromium}=require(process.env.PLAYWRIGHT_MODULE || '/Users/robertdevore/.hermes/hermes-agent/node_modules/playwright');
const fs=require('fs'),cp=require('child_process'),path=require('path');
let browser;
(async()=>{
const root=process.cwd(),out=path.join(root,'demo/walkthrough'),proof=path.join(out,'evidence/v5-workflows');
browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
const context=await browser.newContext({viewport:{width:1280,height:800},storageState:'.local/video/webapp-state.json',recordVideo:{dir:'.local/video/v5-capture',size:{width:1280,height:800}}});
const page=await context.newPage(),epoch=Date.now();page.setDefaultTimeout(20000);
const log=cp.execFileSync('/Users/robertdevore/.hermes/hermes-agent/venv/bin/python',['-m','hermes_cli.main','webapp','--skip-build','--no-open'],{cwd:'/tmp/kujo-hermes-host',env:{...process.env,HERMES_HOME:root+'/.local/video/home',PYTHONPATH:'/tmp/kujo-hermes-host'},encoding:'utf8'});
await page.goto(log.match(/http:\/\/127\.0\.0\.1:9128\S+/g).at(-1));
await page.getByText('Run eval suite and report receipt results',{exact:true}).first().waitFor({timeout:60000});
if(await page.getByRole('button',{name:'Show sidebar',exact:true}).count()) await page.getByRole('button',{name:'Show sidebar',exact:true}).click();
await page.getByRole('button',{name:'Run eval suite and report receipt results',exact:true}).click();
await page.waitForTimeout(2000);
if(await page.getByRole('button',{name:'Hide sidebar',exact:true}).count()) await page.getByRole('button',{name:'Hide sidebar',exact:true}).click();
console.log('Session selected');
// Reset stale pane placement, then dock the first evidence file beside the chat tab.
await page.getByRole('button',{name:'Layout editor',exact:true}).click();
await page.getByRole('button',{name:'Reset',exact:true}).click();
await page.getByRole('button',{name:'Done',exact:true}).click();
await page.waitForTimeout(1000);
if(!(await page.getByText('00-task.md',{exact:true}).count())) await page.getByText('video-evidence',{exact:true}).last().click();
await page.getByText('00-task.md',{exact:true}).last().dblclick();
await page.getByText('00-task.md',{exact:true}).first().dragTo(page.getByText('Run eval suite and report receipt results',{exact:true}).first());
if(await page.getByRole('button',{name:'Hide sidebar',exact:true}).count()) await page.getByRole('button',{name:'Hide sidebar',exact:true}).click();
if(await page.getByRole('button',{name:'Hide right sidebar',exact:true}).count()) await page.getByRole('button',{name:'Hide right sidebar',exact:true}).click();
const files=fs.readdirSync(proof+'/views').filter(x=>x.endsWith('.md')).sort(),shots=[];
let previous='00-task.md';
for(const file of files){
 if(previous!==file){
  await page.getByRole('button',{name:'Show right sidebar',exact:true}).click();
  await page.getByText(file,{exact:true}).last().dblclick();
  await page.getByRole('button',{name:'Hide right sidebar',exact:true}).click();
  const old=page.getByText(previous,{exact:true}).first().locator('../../..');
  await old.hover();await old.getByRole('button',{name:'Close',exact:true}).click();
 }
 await page.getByText(file,{exact:true}).first().click();
 await page.getByRole('button',{name:'PREVIEW',exact:true}).click();
 await page.getByRole('heading',{level:1}).waitFor();
 await page.mouse.move(1230,760);await page.waitForTimeout(1500);
 const start=(Date.now()-epoch)/1000;
 await page.screenshot({path:proof+'/'+file.replace('.md','.png'),timeout:60000});
 const text=await page.locator('body').innerText();
 shots.push({id:file.replace('.md',''),source_start:start,duration:12,view:'evidence/v5-workflows/views/'+file,visible_text:text});
 console.log('CAPTURE',file,start.toFixed(2));
 await page.waitForTimeout(12000);previous=file;
}
await context.storageState({path:'.local/video/webapp-state.json'});
const video=page.video();await context.close();await video.saveAs(out+'/assets/workflows-source.webm');await browser.close();
fs.writeFileSync(proof+'/capture.json',JSON.stringify({host:'Official Hermes Desktop webapp v0.22.7',mode:'Operator-driven native results, viewed as source-linked Markdown files; not model-generated chat',width:1280,height:800,source_file:'assets/workflows-source.webm',shots},null,2)+'\n');
})().catch(async e=>{console.error(e.message);if(browser) await browser.close();process.exitCode=1;});
