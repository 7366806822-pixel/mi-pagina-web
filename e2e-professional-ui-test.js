const { chromium, devices } = require('playwright');
const URL='https://7366806822-pixel.github.io/mi-pagina-web/';

(async()=>{
  const browser=await chromium.launch({headless:true});
  const errors=[];
  try{
    const desktop=await browser.newContext({viewport:{width:1440,height:900}});
    const page=await desktop.newPage();
    page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
    await page.goto(URL,{waitUntil:'domcontentloaded'});
    await page.waitForFunction(()=>document.documentElement.dataset.ui==='professional-v1',{timeout:30000});
    await page.waitForFunction(()=>document.getElementById('liveClock')?.textContent.trim().length>0,{timeout:10000});

    const desktopCheck=await page.evaluate(()=>{
      const clock=document.querySelector('.live-date');
      const date=document.getElementById('todayDateBadge');
      const time=document.getElementById('liveClock');
      const topbar=document.querySelector('.topbar');
      const panel=document.querySelector('.panel');
      return {
        tz:clock?.dataset.timezone,
        aria:clock?.getAttribute('aria-label')||'',
        date:date?.textContent||'',
        time:time?.textContent||'',
        clockDisplay:getComputedStyle(clock).display,
        clockHeight:clock?.getBoundingClientRect().height||0,
        topbarHeight:topbar?.getBoundingClientRect().height||0,
        panelRadius:panel?parseFloat(getComputedStyle(panel).borderRadius):0,
        noOverflow:document.documentElement.scrollWidth<=window.innerWidth+2,
        clockSource:typeof updateClock==='function'?updateClock.toString():'',
        proTimer:!!window.__mddProStatusTimer
      };
    });
    if(desktopCheck.tz!=='America/Lima')throw new Error('Clock timezone dataset is not America/Lima');
    if(!desktopCheck.aria.includes('Hora actual en Lima'))throw new Error('Clock accessibility label missing');
    if(!desktopCheck.date||!desktopCheck.time)throw new Error('Realtime date/time is empty');
    if(!/[ap]\.?\s*m\.?/i.test(desktopCheck.time))throw new Error('12-hour a.m./p.m. clock format missing: '+desktopCheck.time);
    if(!desktopCheck.clockSource.includes('America/Lima'))throw new Error('updateClock does not use explicit America/Lima timezone');
    if(desktopCheck.clockHeight<40||desktopCheck.topbarHeight<70)throw new Error('Premium topbar/clock sizing not applied');
    if(desktopCheck.panelRadius<8)throw new Error('Professional panel design not applied');
    if(!desktopCheck.noOverflow)throw new Error('Unexpected desktop horizontal overflow');
    if(!desktopCheck.proTimer)throw new Error('Realtime status synchronizer not initialized');
    console.log('PRO_UI_DESKTOP_OK');

    await page.locator('#globalAddBtn').click();
    await page.waitForFunction(()=>document.getElementById('recordOverlay')?.classList.contains('open'));
    await page.locator('#cancelRecordBtn').click();
    console.log('PRIMARY_ACTION_PRESERVED_OK');

    const mobile=await browser.newContext({...devices['Pixel 7']});
    const m=await mobile.newPage();
    m.on('console',x=>{if(x.type()==='error')errors.push(x.text())});
    await m.goto(URL,{waitUntil:'domcontentloaded'});
    await m.waitForFunction(()=>document.documentElement.dataset.ui==='professional-v1',{timeout:30000});
    const mobileCheck=await m.evaluate(()=>{
      const clock=document.querySelector('.live-date');
      const add=document.getElementById('globalAddBtn');
      return {
        width:window.innerWidth,
        scrollWidth:document.documentElement.scrollWidth,
        clockVisible:!!clock&&getComputedStyle(clock).display!=='none'&&clock.getBoundingClientRect().width>0,
        clockWidth:clock?.getBoundingClientRect().width||0,
        addW:add?.getBoundingClientRect().width||0,
        bodyText:document.body.innerText
      };
    });
    if(!mobileCheck.clockVisible)throw new Error('Realtime clock is not visible on mobile');
    if(mobileCheck.clockWidth>120)throw new Error('Mobile clock is not compact');
    if(mobileCheck.scrollWidth>mobileCheck.width+2)throw new Error(`Mobile horizontal overflow ${mobileCheck.scrollWidth}/${mobileCheck.width}`);
    if(mobileCheck.addW<36)throw new Error('Mobile primary action touch target too small');
    if(!mobileCheck.bodyText.includes('MI DÍA A DÍA'))throw new Error('System identity missing on mobile');
    console.log('PRO_UI_MOBILE_OK');

    const relevant=errors.filter(x=>!/favicon|Failed to load resource.*404/i.test(x));
    if(relevant.length)throw new Error('Console errors: '+relevant.join(' | '));
    console.log('PROFESSIONAL_UI_ALL_OK');
    await mobile.close();
    await desktop.close();
  } finally {
    await browser.close();
  }
})().catch(e=>{console.error(e);process.exit(1)});
