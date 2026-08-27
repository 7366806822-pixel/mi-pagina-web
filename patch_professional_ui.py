from pathlib import Path

p = Path('/tmp/index.html')
s = p.read_text(encoding='utf-8')

MARKER = '/* MDD_PRO_UI_V1 */'

css = r'''
<style>
/* MDD_PRO_UI_V1 */
:root{
  --bg:#07111f;
  --bg2:#0a1828;
  --panel:rgba(15,29,46,.94);
  --panel-solid:#101d2d;
  --panel-2:#13263a;
  --panel-3:#172c42;
  --text:#f7f9fc;
  --muted:#aab4c3;
  --line:rgba(196,211,227,.12);
  --blue:#3b82f6;
  --blue2:#2463a6;
  --gold:#d2b46c;
  --gold2:#c5a15a;
  --green:#24a66a;
  --red:#ed5b52;
  --orange:#e8a43c;
  --shadow:0 12px 34px rgba(0,0,0,.18);
  --radius:12px;
  --sidebar:286px;
}
html{color-scheme:dark}
body{letter-spacing:.005em;background:#07111f}
button,input,select,textarea{transition:border-color .16s ease,background-color .16s ease,color .16s ease,box-shadow .16s ease,transform .16s ease,opacity .16s ease}
button:active{transform:translateY(1px)}
button:disabled{opacity:.5;cursor:not-allowed;transform:none!important}

/* Fondo sobrio */
#graphBg{opacity:.58;background:
 radial-gradient(circle at 12% 0%,rgba(36,99,166,.13),transparent 33%),
 radial-gradient(circle at 88% 7%,rgba(210,180,108,.055),transparent 26%),
 linear-gradient(145deg,#06101d 0%,#081725 50%,#0a1c2e 100%)}

/* Sidebar */
.sidebar{background:rgba(5,17,30,.965);border-right:1px solid rgba(196,211,227,.10);box-shadow:10px 0 30px rgba(0,0,0,.08)}
.brand-block{padding:17px 13px 15px;gap:10px;background:linear-gradient(180deg,rgba(255,255,255,.018),transparent)}
.brand-mark{width:38px;height:38px;border-radius:9px;font-size:13px;letter-spacing:.5px;background:linear-gradient(135deg,#d2b46c,#e5cd91);box-shadow:0 8px 20px rgba(210,180,108,.13)}
.brand-title{font-size:13px;font-weight:800;letter-spacing:.72px}
.brand-pro{color:var(--gold);font-size:9px;border:1px solid rgba(210,180,108,.22);padding:2px 5px;border-radius:999px;margin-left:4px}
.brand-subtitle{font-size:10px;color:#8494a7}
.sidebar-scroll{padding:10px 8px 16px}
.nav-group{margin-bottom:9px}
.nav-group-toggle{font-size:9px;letter-spacing:1.15px;font-weight:750;color:#77899d;padding:11px 9px 6px}
.nav-group-toggle:hover{color:#acb8c7}
.nav-group-items{gap:2px}
.nav-item{min-height:38px;padding:8px 10px;border-radius:8px;font-size:11.5px;color:#b8c5d3;grid-template-columns:23px minmax(0,1fr) auto}
.nav-item:hover{background:rgba(59,130,246,.07);color:#edf4fb}
.nav-item.active{background:linear-gradient(90deg,rgba(59,130,246,.13),rgba(59,130,246,.055));color:#fff;box-shadow:inset 2px 0 0 var(--gold)}
.nav-ico{color:#83a7cc;font-size:14px}
.nav-item.active .nav-ico{color:#b8d6f5}
.nav-badge{font-size:8.5px;background:rgba(255,255,255,.055);color:#90a0b2}
.sidebar-footer{background:rgba(255,255,255,.012);font-size:9.5px;color:#7f90a4}
.sidebar-footer .status-dot{width:6px;height:6px;box-shadow:0 0 8px rgba(36,166,106,.48)}

/* Topbar premium */
.topbar{height:82px;grid-template-columns:minmax(215px,.72fr) minmax(280px,1.15fr) auto;gap:15px;padding:0 20px;background:rgba(6,16,29,.93);border-bottom:1px solid rgba(196,211,227,.10);backdrop-filter:blur(20px);box-shadow:0 8px 28px rgba(0,0,0,.09)}
.topbar-left h1{font-size:19px;font-weight:780;letter-spacing:-.18px}
.topbar-left p{font-size:10px;color:#8292a5;max-width:440px}
.global-search-wrap{max-width:720px;margin:0 auto;width:100%}
.global-search{height:42px;border-color:rgba(196,211,227,.11);background:rgba(255,255,255,.035);border-radius:9px;padding-left:39px;color:#f4f7fb}
.global-search:hover{border-color:rgba(143,180,219,.22);background:rgba(255,255,255,.045)}
.global-search:focus{border-color:rgba(59,130,246,.42);box-shadow:0 0 0 3px rgba(59,130,246,.10)}
.global-search-wrap kbd{font-size:8.5px;color:#8191a4;background:rgba(255,255,255,.03)}
.topbar-actions{gap:7px;white-space:nowrap}

/* Reloj real de Lima */
.live-date{position:relative;min-width:154px;height:54px;padding:7px 12px 7px 38px;border:1px solid rgba(196,211,227,.11);border-radius:10px;background:linear-gradient(145deg,rgba(19,38,58,.82),rgba(12,27,43,.82));display:grid;align-content:center;gap:1px;box-shadow:inset 0 1px 0 rgba(255,255,255,.025)}
.live-date::before{content:"";position:absolute;left:13px;top:50%;width:8px;height:8px;margin-top:-4px;border-radius:50%;background:var(--green);box-shadow:0 0 0 4px rgba(36,166,106,.08),0 0 11px rgba(36,166,106,.32)}
.live-date::after{content:"EN VIVO";position:absolute;left:28px;top:7px;font-size:6.8px;font-weight:800;letter-spacing:.75px;color:#67ca96;transform:translateX(-1px)}
.live-date strong{display:block;margin-top:8px;font-size:8.7px;line-height:1;text-transform:uppercase;letter-spacing:.72px;color:#8ea0b4;font-weight:750}
.live-date span{display:block;font-size:16.5px;line-height:1.1;color:#f7f9fc;font-weight:780;letter-spacing:-.2px}

.notification-button,.cloud-button,.topbar .icon-button{height:40px;min-width:40px;border-radius:9px;background:rgba(255,255,255,.03);border-color:rgba(196,211,227,.11)}
.notification-button:hover,.cloud-button:hover,.topbar .icon-button:hover{background:rgba(255,255,255,.06);border-color:rgba(196,211,227,.18)}
.cloud-button{padding:9px 11px;font-size:10px;box-shadow:none}
.cloud-button.realtime-online{color:#82d9ac;border-color:rgba(36,166,106,.20);background:rgba(36,166,106,.07)}
.cloud-button.realtime-connecting{color:#e8c277;border-color:rgba(232,164,60,.18);background:rgba(232,164,60,.055)}
.cloud-button.realtime-offline{color:#ef8a84;border-color:rgba(237,91,82,.18);background:rgba(237,91,82,.055)}
.topbar .primary-button,#globalAddBtn{min-height:40px;padding:9px 14px;border-radius:9px;background:#286cae;border-color:rgba(115,170,224,.20);box-shadow:0 8px 20px rgba(36,99,166,.16);font-size:10.5px}
.topbar .primary-button:hover,#globalAddBtn:hover{background:#3079bd;filter:none}

/* Superficie y jerarquía */
.main-view{padding:20px 21px 92px}
.panel{border-radius:12px;border:1px solid rgba(196,211,227,.105);background:rgba(14,29,46,.93);box-shadow:var(--shadow);backdrop-filter:blur(10px)}
.section-panel{padding:16px}
.section-head{margin-bottom:10px}
.section-head h3{font-size:13.5px;font-weight:760;letter-spacing:-.08px}
.section-head p{font-size:10px;color:#8292a5;line-height:1.45}
.hero-main{padding:21px;min-height:170px}
.hero-main h2{font-size:27px;font-weight:780;letter-spacing:-.45px}
.hero-main p{font-size:12px;color:#97a6b7}
.eyebrow{font-size:8.5px;letter-spacing:1.25px;font-weight:800;color:#d5ba79}
.mini-stat{padding:15px}.mini-stat span{font-size:9px}.mini-stat strong{font-size:23px;font-weight:780}
.summary-pill{padding:6px 9px;font-size:9.5px;background:rgba(255,255,255,.025);border-color:rgba(196,211,227,.10)}

/* Botones */
.primary-button,.secondary-button,.danger-button{border-radius:9px;padding:9px 13px;font-weight:730;font-size:10.5px;box-shadow:none}
.primary-button{background:#286cae;border-color:rgba(102,160,218,.18)}
.primary-button:hover{background:#3079bd;filter:none}
.secondary-button{background:rgba(255,255,255,.025);border-color:rgba(196,211,227,.11);color:#cbd6e2}
.secondary-button:hover{background:rgba(255,255,255,.055);border-color:rgba(196,211,227,.17)}
.danger-button{background:rgba(237,91,82,.09);border-color:rgba(237,91,82,.20);color:#ef958f}
.compact{padding:7px 9px;font-size:9.5px}
.icon-button{border-radius:9px}
.link-button{color:#8eb7df;font-size:10px}

/* Formularios */
.field-label{font-size:9.8px;color:#9eacbb;font-weight:700}
.field-control{min-height:40px;border-radius:8px;border-color:rgba(196,211,227,.11);background:rgba(255,255,255,.033);padding:9px 10px;color:#eef4fa}
.field-control:hover{border-color:rgba(143,180,219,.20)}
.field-control:focus{border-color:rgba(59,130,246,.42);box-shadow:0 0 0 3px rgba(59,130,246,.09);background:rgba(255,255,255,.043)}
textarea.field-control{line-height:1.5}
.dynamic-block{border-radius:10px;border-color:rgba(196,211,227,.10);background:rgba(255,255,255,.018)}
.dynamic-block h4{font-size:10px;font-weight:780;color:#cfb472}
.inline-error{border-radius:8px}

/* Registros */
.record-card{padding:12px 0;gap:10px}
.record-title{font-size:12px;font-weight:760}
.record-notes{font-size:10.3px;color:#91a0b1}
.record-meta{font-size:9.3px}
.record-action{border-radius:7px;padding:6px 8px;font-size:9px;background:rgba(255,255,255,.025)}
.tag,.priority{font-size:8.7px}

/* Modales y overlays */
.overlay{background:rgba(2,8,15,.72);backdrop-filter:blur(5px)}
.drawer,.workspace-modal,.confirm-dialog{border-color:rgba(196,211,227,.13);box-shadow:0 28px 80px rgba(0,0,0,.35)}
.drawer-header,.workspace-modal-header{background:rgba(255,255,255,.012)}
.confirm-dialog{border-radius:12px}

/* Search / notificaciones / toast */
.search-panel,.notification-popover{background:#0c1b2c;border-color:rgba(196,211,227,.12);border-radius:10px;box-shadow:0 20px 50px rgba(0,0,0,.28)}
.search-result{border-radius:7px}
.search-result:hover{background:rgba(59,130,246,.07)}
.notification-badge{background:#d9544c;border-color:#07111f;font-size:8px}
.toast{border-radius:9px;border:1px solid rgba(196,211,227,.12);background:#102236;box-shadow:0 18px 45px rgba(0,0,0,.26)}

/* Calendario: solo lenguaje visual, conserva la lógica Calendar PRO */
.cal-app,.google-calendar-shell{--cal-line:rgba(196,211,227,.095)}
.cal-shell,.cal-main,.cal-sidebar,.cal-toolbar,.cal-editor-card,.cal-day-pop{border-color:rgba(196,211,227,.10)!important}
.cal-toolbar{box-shadow:0 8px 25px rgba(0,0,0,.07)}
.cal-event,.cal-month-event,.cal-agenda-event{border-radius:6px!important;box-shadow:none!important}
.cal-now-line{filter:saturate(.9)}

/* Estados vacíos */
.empty-state{padding:29px 15px;font-size:10.5px;color:#738397}
.empty-state strong{font-size:11.5px;color:#aebbc9}

/* Responsive */
@media(max-width:1180px){
  .topbar{grid-template-columns:minmax(190px,.7fr) minmax(220px,1fr) auto;padding:0 15px;gap:10px}
  .live-date{min-width:132px;padding-left:33px;padding-right:9px}
  .live-date span{font-size:14.5px}
  .cloud-button{max-width:105px;overflow:hidden;text-overflow:ellipsis}
}
@media(max-width:920px){
  .topbar{height:70px;grid-template-columns:minmax(0,1fr) auto;padding:0 12px}
  .topbar-center{display:none}
  .topbar-left h1{font-size:17px}
  .topbar-left p{display:none}
  .live-date{min-width:91px;height:43px;padding:5px 9px 5px 28px;border-radius:9px}
  .live-date::before{left:11px;width:7px;height:7px}
  .live-date::after{display:none}
  .live-date strong{font-size:7px;margin-top:0;letter-spacing:.35px;white-space:nowrap}
  .live-date span{font-size:12.5px;white-space:nowrap}
  .cloud-button{display:none}
  .main-view{padding:15px 13px 88px}
}
@media(max-width:620px){
  .topbar{height:64px;padding:0 9px;gap:6px}
  .topbar-left{gap:6px}.topbar-left h1{font-size:15px;max-width:145px}
  .topbar-actions{gap:5px}
  .live-date{min-width:76px;height:39px;padding:5px 7px 5px 22px}
  .live-date::before{left:8px;width:6px;height:6px;margin-top:-3px}
  .live-date strong{font-size:6.5px}.live-date span{font-size:11.5px}
  .notification-button{height:38px;min-width:38px}
  #globalAddBtn{min-width:38px;width:38px;padding:0;font-size:0}
  #globalAddBtn::before{content:"+";font-size:21px;font-weight:500}
  .panel{border-radius:10px}
  .section-panel{padding:13px}
  .hero-main{padding:16px}.hero-main h2{font-size:22px}
  .grid-2,.grid-3{grid-template-columns:1fr!important}
  .form-grid{grid-template-columns:1fr}
  .form-grid .full,.field-span-2{grid-column:1!important}
  .primary-button,.secondary-button,.danger-button{min-height:40px}
}
@media(prefers-reduced-motion:reduce){
  *,*::before,*::after{scroll-behavior:auto!important;transition-duration:.01ms!important;animation-duration:.01ms!important;animation-iteration-count:1!important}
}
</style>
'''

if MARKER not in s:
    assert '</head>' in s, 'No se encontró </head>.'
    s = s.replace('</head>', css + '\n</head>', 1)

# Reemplazar SOLO el reloj existente; conserva el único interval de init().
start = s.find('function updateClock(){')
end_marker = '\nfunction getRecordDate(r){'
end = s.find(end_marker, start)
assert start >= 0 and end > start, 'No se encontró updateClock existente.'
new_clock = r'''function updateClock(){
  const now=new Date();
  const dateFmt=new Intl.DateTimeFormat("es-PE",{timeZone:"America/Lima",weekday:"short",day:"2-digit",month:"short"});
  const timeFmt=new Intl.DateTimeFormat("es-PE",{timeZone:"America/Lima",hour:"numeric",minute:"2-digit",hour12:true});
  const dateText=dateFmt.format(now).replace(/,/g,"").replace(/\./g,"").toUpperCase();
  const timeText=timeFmt.format(now).replace(/\s*a\.\s*m\./i," a. m.").replace(/\s*p\.\s*m\./i," p. m.");
  const dateEl=$("todayDateBadge"),timeEl=$("liveClock"),wrap=dateEl?.closest(".live-date");
  if(dateEl)dateEl.textContent=dateText;
  if(timeEl)timeEl.textContent=timeText;
  if(wrap){wrap.setAttribute("aria-label",`Hora actual en Lima: ${dateText}, ${timeText}`);wrap.title="Hora actual · America/Lima";}
}'''
s = s[:start] + new_clock + s[end:]

# Mayor precisión sin crear un segundo temporizador de reloj.
s = s.replace('updateClock();setInterval(updateClock,30000);updateCloudUI();','updateClock();setInterval(updateClock,15000);updateCloudUI();',1)

runtime = r'''
<script>
/* MDD_PRO_UI_V1_JS */
(()=>{
  'use strict';
  function syncRealtimeBadge(){
    const b=document.getElementById('cloudBtn');
    if(!b)return;
    b.classList.remove('realtime-online','realtime-connecting','realtime-offline');
    let cls='realtime-connecting',label='◌ Conectando';
    try{
      if(typeof db!=='undefined' && db.realtimeReady===true){cls='realtime-online';label='● Tiempo real'}
      else if(!navigator.onLine){cls='realtime-offline';label='● Sin conexión'}
    }catch(_){ }
    b.classList.add(cls);
    b.textContent=label;
    b.setAttribute('aria-label',label.replace('●','').replace('◌','').trim());
  }
  function enhanceProfessionalUI(){
    document.documentElement.dataset.ui='professional-v1';
    const clock=document.querySelector('.live-date');
    if(clock)clock.dataset.timezone='America/Lima';
    syncRealtimeBadge();
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',enhanceProfessionalUI,{once:true});
  else enhanceProfessionalUI();
  if(!window.__mddProStatusTimer)window.__mddProStatusTimer=setInterval(syncRealtimeBadge,5000);
  window.addEventListener('online',syncRealtimeBadge,{passive:true});
  window.addEventListener('offline',syncRealtimeBadge,{passive:true});
})();
</script>
'''
if '/* MDD_PRO_UI_V1_JS */' not in s:
    assert '</body>' in s, 'No se encontró </body>.'
    s = s.replace('</body>', runtime + '\n</body>', 1)

p.write_text(s, encoding='utf-8')
print('Professional UI V1 applied:', len(s), 'bytes')
