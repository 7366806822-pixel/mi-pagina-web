const { chromium, devices } = require('playwright');
const URL='https://7366806822-pixel.github.io/mi-pagina-web/';
const id='e2e_'+Date.now();
const base={id,type:'task',title:'E2E Realtime creación',area:'Estudio jurídico',priority:'Alta',status:'Pendiente',date:'',time:'',dueDate:'',project:'',context:'',tags:'e2e',notes:'prueba automática',nextAction:'',responsible:'',createdAt:new Date().toISOString(),updatedAt:new Date().toISOString()};
(async()=>{
 const browser=await chromium.launch({headless:true});
 const desktop=await browser.newContext({viewport:{width:1440,height:1000}});
 const mobile=await browser.newContext({...devices['Pixel 7']});
 const a=await desktop.newPage(), b=await mobile.newPage();
 const errors=[]; for(const p of [a,b])p.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
 try{
  await Promise.all([a.goto(URL,{waitUntil:'domcontentloaded'}),b.goto(URL,{waitUntil:'domcontentloaded'})]);
  await Promise.all([a.waitForFunction(()=>typeof db!=='undefined'&&db.client&&typeof state!=='undefined',{timeout:30000}),b.waitForFunction(()=>typeof db!=='undefined'&&db.client&&typeof state!=='undefined',{timeout:30000})]);
  await Promise.all([a.waitForFunction(()=>db.realtimeReady===true,{timeout:45000}),b.waitForFunction(()=>db.realtimeReady===true,{timeout:45000})]);
  await a.evaluate(async r=>{await db.put('records',r)},base);
  await b.waitForFunction(x=>state.records.some(r=>r.id===x&&r.title==='E2E Realtime creación'),id,{timeout:20000}); console.log('CREATE_REALTIME_OK');
  await a.evaluate(async x=>{const r=(await db.all('records')).find(v=>v.id===x);r.title='E2E Realtime edición';r.priority='Urgente';r.updatedAt=new Date().toISOString();await db.put('records',r)},id);
  await b.waitForFunction(x=>state.records.some(r=>r.id===x&&r.title==='E2E Realtime edición'&&r.priority==='Urgente'),id,{timeout:20000}); console.log('EDIT_REALTIME_OK');
  const fresh=await browser.newContext({viewport:{width:1365,height:900}}),c=await fresh.newPage(); await c.goto(URL,{waitUntil:'domcontentloaded'}); await c.waitForFunction(()=>typeof db!=='undefined'&&db.client&&db.realtimeReady===true,{timeout:45000}); await c.waitForFunction(x=>state.records.some(r=>r.id===x&&r.title==='E2E Realtime edición'),id,{timeout:20000}); await fresh.close(); console.log('REOPEN_PERSISTENCE_OK');
  await a.evaluate(async x=>{await db.delete('records',x)},id); await b.waitForFunction(x=>!state.records.some(r=>r.id===x),id,{timeout:20000}); console.log('DELETE_REALTIME_OK');
  if(!b.viewportSize()||b.viewportSize().width>500)throw new Error('Mobile viewport not applied');
  const brand=await b.locator('body').innerText(); if(!brand.includes('MI DÍA A DÍA'))throw new Error('Main interface not visible on mobile');
  console.log('CHROME_DESKTOP_MOBILE_OK');
  if(errors.some(x=>/failed to fetch/i.test(x)))throw new Error('Detected Failed to fetch: '+errors.join(' | ')); console.log('E2E_REALTIME_ALL_OK');
 }finally{try{await a.evaluate(async x=>{if(typeof db!=='undefined')await db.delete('records',x)},id)}catch{} await browser.close()}
})().catch(e=>{console.error(e);process.exit(1)});
