// Local verification helper; Node and already-installed Chromium are dev tools only.
import {spawn} from 'node:child_process';
import {writeFile, mkdir} from 'node:fs/promises';
import path from 'node:path';

const root = process.cwd();
const report = path.resolve(process.argv[2] || 'runs/first-integration/report.html');
const output = path.resolve(process.argv[3] || 'docs/evidence/browser');
await mkdir(output, {recursive:true});
const chrome = process.env.EARTH_CHROMIUM;
if (!chrome) throw new Error('Set EARTH_CHROMIUM to an existing Chromium executable.');
const child = spawn(chrome, ['--headless','--disable-dev-shm-usage','--no-first-run','--no-default-browser-check',
 '--remote-debugging-port=0','--remote-debugging-address=127.0.0.1', '--user-data-dir='+path.join(root,'.cache/browser-profile-cdp')],
 {stdio:['ignore','ignore','pipe'],env:{...process.env,TMPDIR:path.join(root,'.t')}});
let next = 0, stderr='';
const pending=new Map();
const endpoint=await new Promise((resolve,reject)=>{
 const timer=setTimeout(()=>reject(new Error('No Chromium endpoint: '+stderr)),15000);
 child.stderr.on('data',x=>{stderr+=x;const m=stderr.match(/DevTools listening on (ws:\/\/[^\s]+)/);if(m){clearTimeout(timer);resolve(m[1]);}});
 child.on('exit',(code,signal)=>{clearTimeout(timer);reject(new Error('Chromium exited '+code+'/'+signal+': '+stderr));});
});
const socket=new WebSocket(endpoint);
await new Promise((resolve,reject)=>{socket.addEventListener('open',resolve,{once:true});socket.addEventListener('error',reject,{once:true});});
socket.addEventListener('message',event=>{
 const msg=JSON.parse(event.data);
 if(msg.id && pending.has(msg.id)){const {resolve,reject,timer}=pending.get(msg.id);clearTimeout(timer);pending.delete(msg.id);msg.error?reject(new Error(JSON.stringify(msg.error))):resolve(msg.result);}
});
const call=(method,params={},sessionId)=>new Promise((resolve,reject)=>{
 const id=++next;const timer=setTimeout(()=>{pending.delete(id);reject(new Error('CDP timeout '+method+': '+stderr));},15000);
 pending.set(id,{resolve,reject,timer});socket.send(JSON.stringify({id,method,params,...(sessionId?{sessionId}:{})}));
});
try {
 const {targetId}=await call('Target.createTarget',{url:'about:blank'});
 const {sessionId}=await call('Target.attachToTarget',{targetId,flatten:true});
 const command=(m,p)=>call(m,p,sessionId);
 await command('Page.enable');
 const evidence=[];
 for (const [name,width,height,scale] of [['desktop',1440,1000,1],['phone',390,844,1],['narrow',320,780,1],['zoom',720,900,2]]) {
  await command('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:false});
  await command('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:'reduce'}]});
  await command('Page.navigate',{url:'file://'+report});
  await new Promise(resolve=>setTimeout(resolve,180));
  const evaluate=async expression=>{const result=await command('Runtime.evaluate',{expression,returnByValue:true});if(result.exceptionDetails)throw new Error(JSON.stringify(result.exceptionDetails));return result.result.value;};
  await evaluate(`document.body.style.zoom=${scale}`);
  const layout=await evaluate(`({title:document.title,width:innerWidth,bodyWidth:document.documentElement.scrollWidth,headings:[...document.querySelectorAll('h1,h2')].map(x=>x.textContent),scripts:document.scripts.length,remoteResources:[...document.querySelectorAll('[src],link[href]')].map(x=>x.src||x.href).filter(x=>/^https?:/.test(x)),tables:[...document.querySelectorAll('table')].map(x=>({caption:!!x.caption,headers:x.querySelectorAll('th').length})),charts:[...document.querySelectorAll('svg')].map(x=>({role:x.getAttribute('role'),title:!!x.querySelector('title'),desc:!!x.querySelector('desc')}))})`);
  const focus=[];
  for(let i=0;i<8;i++){
   await command('Input.dispatchKeyEvent',{type:'keyDown',key:'Tab',code:'Tab',windowsVirtualKeyCode:9});
   await command('Input.dispatchKeyEvent',{type:'keyUp',key:'Tab',code:'Tab',windowsVirtualKeyCode:9});
   focus.push(await evaluate(`({tag:document.activeElement.tagName,text:document.activeElement.textContent.trim().slice(0,60),outline:getComputedStyle(document.activeElement).outlineStyle})`));
  }
  await evaluate('scrollTo(0,0)');
  const {data}=await command('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});
  await writeFile(path.join(output,name+'.png'),Buffer.from(data,'base64'));
  for (const [section,index] of [['comparison',0],['trajectory',1],['accounting',2]]) {
   await evaluate(`(document.getElementById('${section}') || document.querySelectorAll('h2')[${index}] || document.querySelector('h1')).scrollIntoView()`);
   const screenshot=await command('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});
   await writeFile(path.join(output,name+'-'+section+'.png'),Buffer.from(screenshot.data,'base64'));
  }
  const scrollCheck=await evaluate(`(()=>{const x=document.querySelector('.table-scroll,.table-wrap');x.focus();x.scrollLeft=0;return {before:x.scrollLeft,max:x.scrollWidth-x.clientWidth}})()`);
  for(let i=0;i<4;i++) {
   await command('Input.dispatchKeyEvent',{type:'keyDown',key:'ArrowRight',code:'ArrowRight',windowsVirtualKeyCode:39});
   await command('Input.dispatchKeyEvent',{type:'keyUp',key:'ArrowRight',code:'ArrowRight',windowsVirtualKeyCode:39});
  }
  await new Promise(resolve=>setTimeout(resolve,150));
  scrollCheck.after=await evaluate(`document.querySelector('.table-scroll,.table-wrap').scrollLeft`);
  layout.keyboardTableScroll=scrollCheck;
  layout.minimumChartLabelPx=await evaluate(`Math.min(...[...document.querySelectorAll('.chart svg text')].map(x=>x.getBoundingClientRect().height))`);
  if(layout.bodyWidth>layout.width+1 || layout.scripts || layout.remoteResources.length || layout.tables.some(x=>!x.caption||!x.headers))throw new Error('Report structure/reflow check failed: '+JSON.stringify(layout));
  if(layout.minimumChartLabelPx && layout.minimumChartLabelPx<12)throw new Error('Chart label too small');
  evidence.push({name,width,height,scale,layout,focus});
 }
 await writeFile(path.join(output,'checks.json'),JSON.stringify({observer:'automated Chromium CDP; no human observation',evidence},null,2));
 console.log(JSON.stringify(evidence.map(x=>({name:x.name,width:x.layout.width,bodyWidth:x.layout.bodyWidth,scripts:x.layout.scripts,remoteResources:x.layout.remoteResources.length,charts:x.layout.charts.length})),null,2));
} finally {socket.close();child.kill('SIGTERM');}
