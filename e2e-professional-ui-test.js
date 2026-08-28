const { chromium, devices } = require('playwright');
const URL='https://7366806822-pixel.github.io/mi-pagina-web/';

(async()=>{
  const browser=await chromium.launch({headless:true});
  const errors=[];
  try{
    const desktop=await browser.newContext({viewport:{width:1440,height:900}});
    const page=await desktop.newPage();
    page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
    page.on('pageerror',e=>errors.push(e.message));
    await page.goto(URL,{waitUntil:'domcontentloaded'});
    await page.waitForFunction(()=>document.documentElement.dataset.ui==='reference-v2'&&document.documentElement.dataset.appReady==='1',{timeout:60000});
    await page.waitForFunction(()=>document.querySelector('.live-date.mdd-digital-clock')&&document.getElementById('clockSecond')?.dataset.value?.length===2&&document.querySelector('.panel'),{timeout:20000});

    const desktopCheck=await page.evaluate(()=>{
      const clock=document.querySelector('.live-date.mdd-digital-clock');
      const date=document.getElementById('todayDateBadge');
      const time=document.getElementById('liveClock');
      const day=document.getElementById('clockDay');
      const visibleDate=document.getElementById('clockDate');
      const sec=document.getElementById('clockSecond');
      const topbar=document.querySelector('.topbar');
      const panel=document.querySelector('.panel');
      const brand=document.querySelector('.brand-mark');
      const parts=new Intl.DateTimeFormat('es-PE',{timeZone:'America/Lima',weekday:'long',day:'2-digit',month:'2-digit',year:'numeric'}).formatToParts(new Date());
      const get=t=>parts.find(x=>x.type===t)?.value||'';
      return {
        ui:document.documentElement.dataset.ui,
        ref:document.documentElement.dataset.reference,
        tz:clock?.dataset.timezone,
        aria:clock?.getAttribute('aria-label')||'',
        hiddenDate:date?.textContent||'',
        hiddenTime:time?.textContent||'',
        day:day?.textContent||'',
        visibleDate:visibleDate?.textContent||'',
        second:sec?.dataset.value||'',
        expectedDay:get('weekday').toUpperCase(),
        expectedDate:`${get('day')} / ${get('month')} / ${get('year')}`,
        clockDisplay:getComputedStyle(clock).display,
        clockHeight:clock?.getBoundingClientRect().height||0,
        clockWidth:clock?.getBoundingClientRect().width||0,
        clockBorder:getComputedStyle(clock).borderColor,
        topbarHeight:topbar?.getBoundingClientRect().height||0,
        panelRadius:panel?parseFloat(getComputedStyle(panel).borderRadius):0,
        panelBg:panel?getComputedStyle(panel).backgroundImage:'',
        panelColor:panel?getComputedStyle(panel).backgroundColor:'',
        panelBorder:panel?getComputedStyle(panel).borderColor:'',
        brandClip:brand?getComputedStyle(brand).clipPath:'none',
        noOverflow:document.documentElement.scrollWidth<=window.innerWidth+2,
        clockSource:typeof updateClock==='function'?updateClock.toString():'',
        proTimer:!!window.__mddProStatusTimer,
        segCount:clock?.querySelectorAll('.mdd-seg-digit').length||0
      };
    });
    if(desktopCheck.ui!=='reference-v2')throw new Error('Reference UI V2 is not active');
    if(desktopCheck.ref!=='user-supplied-dark-blue-clock')throw new Error('Reference UI identity marker missing');
    if(desktopCheck.tz!=='America/Lima')throw new Error('Clock timezone dataset is not America/Lima');
    if(!desktopCheck.aria.includes('Hora actual en Lima'))throw new Error('Clock accessibility label missing');
    if(desktopCheck.day!==desktopCheck.expectedDay)throw new Error(`Live weekday mismatch ${desktopCheck.day}/${desktopCheck.expectedDay}`);
    if(desktopCheck.visibleDate!==desktopCheck.expectedDate)throw new Error(`Live date mismatch ${desktopCheck.visibleDate}/${desktopCheck.expectedDate}`);
    if(!/^\d{2}:\d{2}:\d{2}\s+[ap]\.\s*m\.$/i.test(desktopCheck.hiddenTime))throw new Error('HH:MM:SS a.m./p.m. format missing: '+desktopCheck.hiddenTime);
    if(!desktopCheck.clockSource.includes('America/Lima')||!desktopCheck.clockSource.includes('second:"2-digit"'))throw new Error('updateClock does not explicitly use Lima seconds');
    if(desktopCheck.clockHeight<60||desktopCheck.clockWidth<145||desktopCheck.topbarHeight<84)throw new Error('Reference topbar/digital clock sizing not applied');
    if(desktopCheck.segCount<6)throw new Error('Seven-segment visual digits were not rendered');
    if(desktopCheck.brandClip==='none')throw new Error('Gold shield brand model not applied');
    if(desktopCheck.panelRadius<8)throw new Error('Reference panel radius not applied');
    if(!desktopCheck.panelBg.includes('gradient')&&!/rgb\((?:0|[1-9]|1\d|2\d),\s*(?:0|[1-9]|1\d|2\d),\s*(?:0|[1-9]|1\d|2\d)\)/.test(desktopCheck.panelColor))throw new Error(`Reference dark panel design not applied: ${desktopCheck.panelBg} / ${desktopCheck.panelColor}`);
    if(!desktopCheck.noOverflow)throw new Error('Unexpected desktop horizontal overflow');
    if(!desktopCheck.proTimer)throw new Error('Realtime status synchronizer not initialized');

    const secondBefore=desktopCheck.second;
    await page.waitForTimeout(1250);
    const secondAfter=await page.locator('#clockSecond').getAttribute('data-value');
    if(!secondAfter||secondAfter===secondBefore)throw new Error(`Clock seconds did not advance: ${secondBefore} -> ${secondAfter}`);
    console.log('REFERENCE_CLOCK_LIMA_SECONDS_OK');
    console.log('REFERENCE_UI_DESKTOP_OK');

    await page.locator('#globalAddBtn').click();
    await page.waitForFunction(()=>document.getElementById('recordOverlay')?.classList.contains('open'));
    await page.locator('#cancelRecordBtn').click();
    console.log('PRIMARY_ACTION_PRESERVED_OK');

    const mobile=await browser.newContext({...devices['Pixel 7']});
    const m=await mobile.newPage();
    m.on('console',x=>{if(x.type()==='error')errors.push(x.text())});
    m.on('pageerror',e=>errors.push(e.message));
    await m.goto(URL,{waitUntil:'domcontentloaded'});
    await m.waitForFunction(()=>document.documentElement.dataset.ui==='reference-v2'&&document.documentElement.dataset.appReady==='1'&&document.querySelector('.live-date.mdd-digital-clock'),{timeout:60000});
    await m.waitForFunction(()=>document.getElementById('clockSecond')?.dataset.value?.length===2,{timeout:10000});
    const mobileCheck=await m.evaluate(()=>{
      const clock=document.querySelector('.live-date.mdd-digital-clock');
      const add=document.getElementById('globalAddBtn');
      return {
        width:window.innerWidth,
        scrollWidth:document.documentElement.scrollWidth,
        clockVisible:!!clock&&getComputedStyle(clock).display!=='none'&&clock.getBoundingClientRect().width>0,
        clockWidth:clock?.getBoundingClientRect().width||0,
        clockHeight:clock?.getBoundingClientRect().height||0,
        second:document.getElementById('clockSecond')?.dataset.value||'',
        date:document.getElementById('clockDate')?.textContent||'',
        addW:add?.getBoundingClientRect().width||0,
        addH:add?.getBoundingClientRect().height||0,
        bodyText:document.body.innerText
      };
    });
    if(!mobileCheck.clockVisible)throw new Error('Reference realtime clock is not visible on mobile');
    if(mobileCheck.clockWidth>135||mobileCheck.clockHeight>62)throw new Error(`Mobile clock is not compact ${mobileCheck.clockWidth}x${mobileCheck.clockHeight}`);
    if(!/^\d{2}$/.test(mobileCheck.second)||!mobileCheck.date.includes('/'))throw new Error('Mobile live seconds/date missing');
    if(mobileCheck.scrollWidth>mobileCheck.width+2)throw new Error(`Mobile horizontal overflow ${mobileCheck.scrollWidth}/${mobileCheck.width}`);
    if(mobileCheck.addW<36||mobileCheck.addH<36)throw new Error('Mobile primary action touch target too small');
    if(!mobileCheck.bodyText.includes('MI DÍA A DÍA'))throw new Error('System identity missing on mobile');
    console.log('REFERENCE_UI_MOBILE_OK');

    const relevant=errors.filter(x=>!/favicon|Failed to load resource.*404/i.test(x));
    if(relevant.length)throw new Error('Console errors: '+relevant.join(' | '));
    console.log('REFERENCE_UI_ALL_OK');
    await mobile.close();
    await desktop.close();
  } finally {
    await browser.close();
  }
})().catch(e=>{console.error(e);process.exit(1)});
