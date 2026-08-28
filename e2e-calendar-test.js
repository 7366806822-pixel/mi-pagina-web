const { chromium, devices } = require('playwright');
const URL='https://7366806822-pixel.github.io/mi-pagina-web/';
const title='E2E Calendar '+Date.now();
(async()=>{
 const browser=await chromium.launch({headless:true});
 const desktop=await browser.newContext({viewport:{width:1440,height:1000}});
 const page=await desktop.newPage();
 const errors=[]; page.on('pageerror',e=>errors.push(e.message)); page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
 let id='';
 try{
  await page.goto(URL,{waitUntil:'domcontentloaded'});
  await page.waitForFunction(()=>document.documentElement.dataset.appReady==='1'&&typeof state!=='undefined'&&typeof db!=='undefined'&&window.MDDCalendarPro&&typeof navItemBySpecial==='function'&&typeof navigate==='function',{timeout:60000});
  console.log('APP_EVENT_BINDING_READY_OK');
  await page.evaluate(()=>{const it=navItemBySpecial('calendar');if(!it)throw new Error('Calendar navigation config not found');navigate(it)});
  await page.locator('.cal-app').waitFor({state:'visible'});
  for(const view of ['day','week','month','agenda']){await page.locator(`[data-action="calendar-view"][data-view="${view}"]`).click();await page.waitForFunction(v=>state.calendarView===v,view,{timeout:10000});console.log('VIEW_'+view.toUpperCase()+'_OK')}
  await page.locator('[data-action="calendar-today"]').click();await page.locator('[data-action="calendar-view"][data-view="day"]').click();
  await page.locator('[data-action="calendar-new"]').first().click();await page.locator('#calendarEditorOverlay.open').waitFor();
  const today=await page.evaluate(()=>localISO());
  await page.locator('#calTitle').fill(title);await page.locator('#calStartDate').fill(today);await page.locator('#calEndDate').fill(today);await page.locator('#calStartTime').fill('13:00');await page.locator('#calEndTime').fill('14:00');
  await page.locator('[data-action="calendar-more-options"]').click();await page.locator('#calRecurrence').selectOption('weekly');await page.locator('[data-action="calendar-save"]').click();
  await page.waitForFunction(t=>state.records.some(r=>r.title===t),title,{timeout:20000});
  id=await page.evaluate(t=>state.records.find(r=>r.title===t)?.id||'',title);if(!id)throw new Error('Calendar event was not created in state');
  await page.waitForTimeout(2500);
  const saveDiag=await page.evaluate(async x=>({overlayOpen:document.getElementById('calendarEditorOverlay')?.classList.contains('open')||false,runtimeErrors:state.runtimeErrors.slice(-4),persisted:(await db.all('records')).some(r=>r.id===x),record:state.records.find(r=>r.id===x)||null}),id);
  console.log('CAL_SAVE_DIAG '+JSON.stringify(saveDiag));
  if(!saveDiag.persisted)throw new Error('Calendar event did not persist to Supabase. '+JSON.stringify(saveDiag.runtimeErrors));
  if(saveDiag.overlayOpen)throw new Error('Calendar editor stayed open after confirmed Supabase persistence. '+JSON.stringify(saveDiag.runtimeErrors));
  const saved=saveDiag.record;if(saved.time!=='13:00'||saved.endTime!=='14:00'||saved.recurrence!=='weekly')throw new Error('Event fields not persisted correctly');console.log('CREATE_PERSISTENCE_RECURRENCE_OK');

  await page.locator('[data-action="calendar-view"][data-view="week"]').click();await page.locator('[data-action="calendar-next"]').click();
  const recurringEv=page.locator(`[data-cal-event][data-id="${id}"]`).first();await recurringEv.waitFor({state:'visible',timeout:10000});
  const occurrence=await recurringEv.getAttribute('data-occurrence');if(!occurrence||occurrence===today)throw new Error('Future recurrence did not render');console.log('RECURRENCE_RENDER_OK');
  const lane=page.locator(`[data-cal-time-lane="${occurrence}"]`);await recurringEv.dragTo(lane,{targetPosition:{x:120,y:56*15}});await page.waitForTimeout(1000);
  const baseAfter=await page.evaluate(x=>state.records.find(r=>r.id===x),id);const child=await page.evaluate(([x,d])=>state.records.find(r=>r.parentRecurringId===x&&r.recurrenceExceptionDate===d),[id,occurrence]);
  if(!child||!Array.isArray(baseAfter.recurrenceExDates)||!baseAfter.recurrenceExDates.includes(occurrence))throw new Error('Recurring drag did not create a safe exception');console.log('DRAG_DROP_RECURRING_EXCEPTION_OK');
  await page.evaluate(d=>{state.calendarDate=new Date(d+'T12:00:00');state.calendarView='day';renderCalendar()},occurrence);
  const childEl=page.locator(`[data-cal-event][data-id="${child.id}"]`).first();await childEl.waitFor({state:'visible'});

  const resizeDiag=await page.evaluate(async childId=>{
    const ev=document.querySelector(`[data-cal-event][data-id="${childId}"]`);
    const h=ev?.querySelector('[data-resize-id]');
    const wrap=ev?.closest('.cal-event-wrap');
    const before=state.records.find(r=>r.id===childId);
    if(!ev||!h||!wrap||!before)return {error:'resize DOM unavailable'};
    const hb=h.getBoundingClientRect();
    const y=hb.top+Math.max(1,hb.height/2);
    const mk=(type,clientY,buttons=0)=>new PointerEvent(type,{bubbles:true,cancelable:true,pointerId:77,pointerType:'mouse',isPrimary:true,button:0,buttons,clientX:hb.left+Math.max(1,hb.width/2),clientY});
    h.dispatchEvent(mk('pointerdown',y,1));
    const down={active:!!state.calendarResize,startY:state.calendarResize?.startY,startH:state.calendarResize?.startH,draggable:ev.draggable};
    document.dispatchEvent(mk('pointermove',y+56,1));
    const during={active:!!state.calendarResize,inlineHeight:wrap.style.height};
    document.dispatchEvent(mk('pointerup',y+56,0));
    await new Promise(r=>setTimeout(r,1400));
    const after=state.records.find(r=>r.id===childId);
    const persisted=(await db.all('records')).find(r=>r.id===childId);
    return {before:{time:before.time,endTime:before.endTime},down,during,after:after?{time:after.time,endTime:after.endTime}:null,persisted:persisted?{time:persisted.time,endTime:persisted.endTime}:null,runtimeErrors:state.runtimeErrors.slice(-4),error:null};
  },child.id);
  console.log('RESIZE_DIAG '+JSON.stringify(resizeDiag));
  if(resizeDiag.error)throw new Error(resizeDiag.error);
  if(!resizeDiag.down.active)throw new Error('Resize pointerdown did not activate Calendar resize state');
  const resized=await page.evaluate(x=>state.records.find(r=>r.id===x),child.id);const toMin=t=>{const [h,m]=t.split(':').map(Number);return h*60+m};
  if(toMin(resized.endTime)-toMin(resized.time)<105)throw new Error('Resize did not extend event duration: '+JSON.stringify(resizeDiag));
  if(!resizeDiag.persisted||resizeDiag.persisted.endTime!==resized.endTime)throw new Error('Resize was not persisted to Supabase: '+JSON.stringify(resizeDiag));
  console.log('RESIZE_OK');

  await page.locator('#calendarSearch').fill(title);await page.locator(`[data-cal-event][data-id="${child.id}"]`).first().click();await page.locator('#calendarEditorOverlay.open').waitFor();await page.locator('#calLocation').fill('E2E ubicación temporal');await page.locator('[data-action="calendar-save"]').click();
  await page.waitForFunction(x=>state.records.some(r=>r.id===x&&r.location==='E2E ubicación temporal'),child.id,{timeout:20000});await page.waitForTimeout(1500);
  const editDiag=await page.evaluate(async x=>({open:document.getElementById('calendarEditorOverlay')?.classList.contains('open')||false,persisted:(await db.all('records')).some(r=>r.id===x&&r.location==='E2E ubicación temporal'),errs:state.runtimeErrors.slice(-4)}),child.id);if(editDiag.open||!editDiag.persisted)throw new Error('Calendar edit completion failed '+JSON.stringify(editDiag));console.log('SEARCH_EDIT_OK');

  const mobile=await browser.newContext({...devices['Pixel 7']});const mp=await mobile.newPage();await mp.goto(URL,{waitUntil:'domcontentloaded'});await mp.waitForFunction(()=>document.documentElement.dataset.appReady==='1'&&window.MDDCalendarPro&&typeof state!=='undefined'&&typeof navItemBySpecial==='function'&&typeof navigate==='function',{timeout:60000});await mp.evaluate(()=>navigate(navItemBySpecial('calendar')));await mp.locator('.cal-app').waitFor();await mp.locator('[data-action="calendar-view"][data-view="agenda"]').click();const mobileBox=await mp.locator('.cal-app').boundingBox();if(!mobileBox||mobileBox.width>500)throw new Error('Calendar mobile layout is not constrained');console.log('MOBILE_RESPONSIVE_OK');await mobile.close();
  if(errors.length)throw new Error('Browser errors: '+errors.join(' | '));console.log('CALENDAR_PRO_E2E_ALL_OK');
 } finally {
  try{await page.evaluate(async ([t,base])=>{const rows=await db.all('records');for(const r of rows.filter(r=>r.title===t||r.parentRecurringId===base))await db.delete('records',r.id);const trash=await db.all('trash');for(const r of trash.filter(r=>r.title===t||r.parentRecurringId===base))await db.delete('trash',r.id)},[title,id])}catch{}
  await browser.close();
 }
})().catch(e=>{console.error(e);process.exit(1)});
