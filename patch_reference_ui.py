from pathlib import Path

p = Path('/tmp/index.html')
s = p.read_text(encoding='utf-8')

MARKER = '/* MDD_REFERENCE_UI_V2 */'

css = r'''
<style>
/* MDD_REFERENCE_UI_V2 */
:root{
  --ref-bg:#020812;
  --ref-bg-2:#030b17;
  --ref-panel:#061426;
  --ref-panel-2:#081a30;
  --ref-panel-3:#0a1e36;
  --ref-line:rgba(38,151,255,.28);
  --ref-line-soft:rgba(78,156,227,.14);
  --ref-blue:#087cff;
  --ref-blue-2:#00a8ff;
  --ref-cyan:#23d8ff;
  --ref-cyan-soft:rgba(35,216,255,.16);
  --ref-gold:#f2bd3d;
  --ref-gold-2:#ffd86a;
  --ref-text:#f6f9fd;
  --ref-muted:#8191a8;
  --ref-green:#2bd987;
  --ref-red:#ff4d62;
  --ref-shadow:0 18px 55px rgba(0,0,0,.34);
  --ref-glow:0 0 24px rgba(0,123,255,.13);
}
html[data-ui="reference-v2"]{color-scheme:dark}
html[data-ui="reference-v2"] body{
  background:#020812;
  color:var(--ref-text);
  font-family:Inter,Manrope,"Segoe UI",Roboto,system-ui,-apple-system,sans-serif;
  letter-spacing:.002em;
}
html[data-ui="reference-v2"] #graphBg{
  opacity:1!important;
  background:
    radial-gradient(circle at 74% 9%,rgba(0,126,255,.10),transparent 29%),
    radial-gradient(circle at 7% 42%,rgba(0,194,255,.055),transparent 25%),
    radial-gradient(circle at 56% 82%,rgba(0,98,220,.06),transparent 32%),
    linear-gradient(145deg,#01060d 0%,#020914 42%,#03101f 100%)!important;
}
html[data-ui="reference-v2"] #graphBg::before{
  content:"";position:absolute;inset:0;pointer-events:none;opacity:.28;
  background-image:
    linear-gradient(rgba(35,216,255,.028) 1px,transparent 1px),
    linear-gradient(90deg,rgba(35,216,255,.022) 1px,transparent 1px);
  background-size:42px 42px;
  mask-image:linear-gradient(to bottom,rgba(0,0,0,.35),transparent 80%);
}

/* MARCA / SIDEBAR — referencia azul noche + dorado */
html[data-ui="reference-v2"] .sidebar{
  background:linear-gradient(180deg,rgba(1,9,20,.99),rgba(2,12,25,.985))!important;
  border-right:1px solid rgba(45,141,229,.18)!important;
  box-shadow:14px 0 44px rgba(0,0,0,.24),inset -1px 0 rgba(0,140,255,.035)!important;
}
html[data-ui="reference-v2"] .brand-block{
  min-height:82px;padding:16px 15px!important;
  background:linear-gradient(180deg,rgba(7,27,50,.42),rgba(1,9,20,0))!important;
  border-bottom:1px solid rgba(45,141,229,.12);
}
html[data-ui="reference-v2"] .brand-mark{
  position:relative;width:48px!important;height:54px!important;border-radius:0!important;
  clip-path:polygon(50% 0,92% 22%,92% 75%,50% 100%,8% 75%,8% 22%);
  background:linear-gradient(145deg,#ffdc72,#bc7e0f)!important;
  color:var(--ref-gold-2)!important;font-size:16px!important;font-weight:900!important;
  display:grid!important;place-items:center!important;isolation:isolate;
  box-shadow:0 0 22px rgba(242,189,61,.22)!important;
}
html[data-ui="reference-v2"] .brand-mark::before{
  content:"";position:absolute;inset:2px;z-index:-1;
  clip-path:inherit;background:linear-gradient(145deg,#061629,#010812 78%);
}
html[data-ui="reference-v2"] .brand-title{font-size:14px!important;font-weight:850!important;letter-spacing:1px!important;color:#fff!important}
html[data-ui="reference-v2"] .brand-pro{
  color:#bde6ff!important;background:linear-gradient(180deg,rgba(10,112,255,.36),rgba(4,59,141,.35))!important;
  border:1px solid rgba(38,151,255,.52)!important;box-shadow:0 0 12px rgba(0,112,255,.12);
}
html[data-ui="reference-v2"] .brand-subtitle{color:#8294aa!important;font-size:9.5px!important}
html[data-ui="reference-v2"] .sidebar-scroll{padding:11px 9px 18px!important}
html[data-ui="reference-v2"] .nav-group-toggle{color:#8392a7!important;font-size:9px!important;font-weight:800!important;letter-spacing:1.3px!important}
html[data-ui="reference-v2"] .nav-item{
  min-height:40px!important;border:1px solid transparent!important;border-radius:8px!important;
  color:#b7c3d2!important;background:transparent!important;
}
html[data-ui="reference-v2"] .nav-item:hover{
  color:#f5faff!important;background:rgba(4,75,144,.18)!important;
  border-color:rgba(35,216,255,.08)!important;
}
html[data-ui="reference-v2"] .nav-item.active{
  color:#fff!important;
  background:linear-gradient(100deg,rgba(0,112,255,.32),rgba(0,63,150,.13) 78%,rgba(0,213,255,.035))!important;
  border-color:rgba(0,139,255,.52)!important;
  box-shadow:inset 3px 0 0 #0d94ff,0 0 18px rgba(0,112,255,.12)!important;
}
html[data-ui="reference-v2"] .nav-ico{color:#7fbfff!important;filter:drop-shadow(0 0 5px rgba(0,144,255,.22))}
html[data-ui="reference-v2"] .nav-item.active .nav-ico{color:#bdeaff!important;filter:drop-shadow(0 0 7px rgba(35,216,255,.45))}
html[data-ui="reference-v2"] .nav-badge{background:#061c33!important;border:1px solid rgba(0,132,255,.26)!important;color:#a8c4df!important}
html[data-ui="reference-v2"] .sidebar-footer{
  margin:8px!important;border:1px solid rgba(0,130,255,.24)!important;border-radius:8px!important;
  background:linear-gradient(90deg,rgba(0,77,142,.18),rgba(0,26,55,.28))!important;color:#b8c6d6!important;
  box-shadow:0 0 16px rgba(0,110,255,.06)!important;
}
html[data-ui="reference-v2"] .sidebar-footer .status-dot{background:var(--ref-green)!important;box-shadow:0 0 12px rgba(43,217,135,.72)!important}

/* TOPBAR tipo centro de control */
html[data-ui="reference-v2"] .topbar{
  height:94px!important;
  grid-template-columns:minmax(220px,.72fr) minmax(320px,1.25fr) auto!important;
  gap:18px!important;padding:0 22px!important;
  background:linear-gradient(180deg,rgba(1,8,18,.985),rgba(2,12,25,.97))!important;
  border-bottom:1px solid rgba(26,116,202,.22)!important;
  box-shadow:0 12px 38px rgba(0,0,0,.22),inset 0 -1px rgba(0,166,255,.025)!important;
  backdrop-filter:blur(22px)!important;
}
html[data-ui="reference-v2"] .topbar-left h1{font-size:20px!important;font-weight:820!important;color:#fff!important;letter-spacing:-.28px!important}
html[data-ui="reference-v2"] .topbar-left p{font-size:10px!important;color:#7f8da2!important}
html[data-ui="reference-v2"] .global-search-wrap{max-width:760px!important}
html[data-ui="reference-v2"] .global-search{
  height:44px!important;border-radius:9px!important;
  background:linear-gradient(180deg,rgba(7,22,39,.86),rgba(4,15,29,.92))!important;
  border:1px solid rgba(85,134,185,.22)!important;color:#edf6ff!important;
  box-shadow:inset 0 1px rgba(255,255,255,.018)!important;
}
html[data-ui="reference-v2"] .global-search:focus{
  border-color:rgba(0,146,255,.7)!important;
  box-shadow:0 0 0 3px rgba(0,125,255,.10),0 0 20px rgba(0,125,255,.08)!important;
}
html[data-ui="reference-v2"] .global-search-wrap kbd{border-color:rgba(61,115,165,.22)!important;background:#071422!important;color:#72869c!important}
html[data-ui="reference-v2"] .topbar-actions{gap:9px!important}

/* RELOJ DIGITAL tecnológico inspirado en la referencia suministrada */
html[data-ui="reference-v2"] .live-date.mdd-digital-clock{
  position:relative!important;width:180px!important;min-width:180px!important;height:78px!important;
  padding:4px 10px 5px!important;border-radius:13px!important;overflow:hidden!important;
  display:grid!important;grid-template-rows:12px 1fr 13px!important;align-items:center!important;gap:1px!important;
  border:1px solid rgba(35,216,255,.58)!important;
  background:
    radial-gradient(circle at 50% 55%,rgba(0,126,255,.10),transparent 60%),
    linear-gradient(180deg,#020913 0%,#01060c 100%)!important;
  box-shadow:
    0 0 0 1px rgba(0,80,150,.55),
    inset 0 0 0 2px rgba(6,30,54,.88),
    inset 0 0 22px rgba(0,99,180,.13),
    0 0 22px rgba(0,164,255,.12)!important;
}
html[data-ui="reference-v2"] .live-date.mdd-digital-clock::before{
  content:""!important;position:absolute!important;inset:5px!important;margin:0!important;width:auto!important;height:auto!important;border-radius:9px!important;
  background:
    linear-gradient(90deg,transparent,rgba(35,216,255,.8),transparent) top/72% 1px no-repeat,
    linear-gradient(90deg,transparent,rgba(0,135,255,.45),transparent) bottom/78% 1px no-repeat!important;
  box-shadow:none!important;pointer-events:none!important;
}
html[data-ui="reference-v2"] .live-date.mdd-digital-clock::after{display:none!important}
html[data-ui="reference-v2"] .clock-tech-day{
  position:relative;z-index:2;text-align:center;color:#18d4ff;font-size:7.6px;font-weight:900;
  letter-spacing:1.45px;text-transform:uppercase;text-shadow:0 0 8px rgba(35,216,255,.52);
}
html[data-ui="reference-v2"] .clock-tech-time{
  position:relative;z-index:2;display:flex;align-items:center;justify-content:center;height:43px;gap:2px;
  color:#f7fbff;font-variant-numeric:tabular-nums;
}
html[data-ui="reference-v2"] .clock-segment-group{display:flex;align-items:center;gap:1px;height:40px;color:#f6f9ff}
html[data-ui="reference-v2"] .clock-segment-group.clock-seconds{color:#1bd7ff}
html[data-ui="reference-v2"] .mdd-seg-digit{width:20px;height:38px;display:block;overflow:visible;filter:drop-shadow(0 0 3px currentColor)}
html[data-ui="reference-v2"] .mdd-seg-digit .seg{fill:currentColor;opacity:.055;transition:opacity .08s linear}
html[data-ui="reference-v2"] .mdd-seg-digit .seg.on{opacity:.98}
html[data-ui="reference-v2"] .clock-colon{width:6px;height:30px;position:relative;flex:none;opacity:.92}
html[data-ui="reference-v2"] .clock-colon::before,html[data-ui="reference-v2"] .clock-colon::after{
  content:"";position:absolute;left:2px;width:3px;height:3px;border-radius:50%;background:#e8f7ff;box-shadow:0 0 5px rgba(85,206,255,.62)
}
html[data-ui="reference-v2"] .clock-colon::before{top:9px}html[data-ui="reference-v2"] .clock-colon::after{bottom:8px}
html[data-ui="reference-v2"] .clock-colon.cyan::before,html[data-ui="reference-v2"] .clock-colon.cyan::after{background:#20d8ff}
html[data-ui="reference-v2"] .clock-tech-date{
  position:relative;z-index:2;text-align:center;color:#f0f6fb;font-size:7.5px;font-weight:850;letter-spacing:1px;
  text-shadow:0 0 6px rgba(255,255,255,.15);
}
html[data-ui="reference-v2"] .mdd-sr-only{
  position:absolute!important;width:1px!important;height:1px!important;padding:0!important;margin:-1px!important;overflow:hidden!important;
  clip:rect(0,0,0,0)!important;white-space:nowrap!important;border:0!important;
}

/* ACCIONES de topbar */
html[data-ui="reference-v2"] .notification-button,
html[data-ui="reference-v2"] .cloud-button,
html[data-ui="reference-v2"] .topbar .icon-button{
  height:42px!important;min-width:42px!important;border-radius:9px!important;
  background:linear-gradient(180deg,rgba(8,24,43,.92),rgba(3,13,25,.95))!important;
  border:1px solid rgba(77,132,185,.23)!important;color:#dbe7f3!important;
  box-shadow:inset 0 1px rgba(255,255,255,.018)!important;
}
html[data-ui="reference-v2"] .notification-button:hover,
html[data-ui="reference-v2"] .cloud-button:hover,
html[data-ui="reference-v2"] .topbar .icon-button:hover{border-color:rgba(0,155,255,.44)!important;background:#071b31!important}
html[data-ui="reference-v2"] .notification-badge{background:var(--ref-red)!important;box-shadow:0 0 10px rgba(255,77,98,.28)!important}
html[data-ui="reference-v2"] .cloud-button.realtime-online{
  color:#70efae!important;border-color:rgba(43,217,135,.25)!important;background:rgba(14,83,59,.18)!important;
}
html[data-ui="reference-v2"] .cloud-button.realtime-online::first-letter{color:var(--ref-green)}
html[data-ui="reference-v2"] #globalAddBtn,
html[data-ui="reference-v2"] .topbar .primary-button{
  min-height:42px!important;border-radius:9px!important;padding:10px 17px!important;
  background:linear-gradient(180deg,#087cff,#045bd7)!important;border:1px solid rgba(46,158,255,.78)!important;color:#fff!important;
  box-shadow:0 0 22px rgba(0,112,255,.22),inset 0 1px rgba(255,255,255,.16)!important;
  font-weight:800!important;
}
html[data-ui="reference-v2"] #globalAddBtn:hover,
html[data-ui="reference-v2"] .topbar .primary-button:hover{background:linear-gradient(180deg,#1590ff,#0768e8)!important;box-shadow:0 0 26px rgba(0,139,255,.28)!important}

/* SUPERFICIES / PANELES */
html[data-ui="reference-v2"] .main-view{padding:20px 22px 96px!important}
html[data-ui="reference-v2"] .panel{
  position:relative;border-radius:11px!important;
  background:linear-gradient(145deg,rgba(5,19,36,.965),rgba(4,15,29,.965))!important;
  border:1px solid rgba(21,112,201,.36)!important;
  box-shadow:var(--ref-shadow),inset 0 1px rgba(77,173,255,.025),0 0 20px rgba(0,105,205,.035)!important;
}
html[data-ui="reference-v2"] .panel::before{
  content:"";position:absolute;left:14px;right:14px;top:-1px;height:1px;pointer-events:none;
  background:linear-gradient(90deg,transparent,rgba(35,216,255,.34),transparent);opacity:.55;
}
html[data-ui="reference-v2"] .section-panel{padding:17px!important}
html[data-ui="reference-v2"] .section-head h3{color:#f5f8fc!important;font-weight:800!important}
html[data-ui="reference-v2"] .section-head p{color:#7f91a7!important}
html[data-ui="reference-v2"] .eyebrow{color:var(--ref-gold)!important;text-shadow:0 0 8px rgba(242,189,61,.12)!important}

/* HERO / CENTRO DE CONTROL */
html[data-ui="reference-v2"] .hero-main{
  position:relative;overflow:hidden;min-height:190px!important;padding:25px 28px!important;
  background:
    radial-gradient(circle at 78% 53%,rgba(0,125,255,.17),transparent 21%),
    linear-gradient(110deg,rgba(3,20,39,.98) 0%,rgba(3,16,31,.95) 58%,rgba(1,11,23,.96) 100%)!important;
  border-color:rgba(0,125,238,.42)!important;
}
html[data-ui="reference-v2"] .hero-main::before{
  content:"";position:absolute;inset:0;pointer-events:none;opacity:.34;
  background:
    radial-gradient(circle at 78% 54%,transparent 0 50px,rgba(20,196,255,.32) 51px 52px,transparent 53px 72px,rgba(0,116,255,.20) 73px 74px,transparent 75px),
    linear-gradient(90deg,transparent 72%,rgba(0,169,255,.06) 72% 72.4%,transparent 72.4% 80%,rgba(0,169,255,.045) 80% 80.2%,transparent 80%);
}
html[data-ui="reference-v2"] .hero-main::after{
  content:"⚖";position:absolute;right:8.5%;top:50%;transform:translateY(-50%);
  color:#21d8ff;font-family:"Times New Roman",serif;font-size:74px;line-height:1;
  text-shadow:0 0 8px #0b8fff,0 0 22px rgba(0,159,255,.72),0 0 52px rgba(0,100,255,.28);
  opacity:.9;pointer-events:none;
}
html[data-ui="reference-v2"] .hero-main h2{position:relative;z-index:2;color:#fff!important;font-size:26px!important;font-weight:850!important;max-width:72%}
html[data-ui="reference-v2"] .hero-main p{position:relative;z-index:2;color:#a4b2c2!important;max-width:68%}
html[data-ui="reference-v2"] .hero-main .button-row,html[data-ui="reference-v2"] .hero-main .hero-actions{position:relative;z-index:2}

/* MÉTRICAS / TARJETAS */
html[data-ui="reference-v2"] .mini-stat,
html[data-ui="reference-v2"] .summary-pill{
  background:linear-gradient(145deg,rgba(6,22,41,.94),rgba(3,14,27,.96))!important;
  border:1px solid rgba(31,105,176,.32)!important;
  box-shadow:inset 0 1px rgba(255,255,255,.02)!important;
}
html[data-ui="reference-v2"] .mini-stat strong{color:#fff!important;font-weight:850!important}
html[data-ui="reference-v2"] .mini-stat span{color:#8fa1b6!important}

/* REGISTROS */
html[data-ui="reference-v2"] .record-card{border-bottom-color:rgba(68,118,165,.16)!important}
html[data-ui="reference-v2"] .record-card:hover{background:linear-gradient(90deg,rgba(0,101,194,.055),transparent)!important}
html[data-ui="reference-v2"] .record-title{color:#f4f8fc!important;font-weight:780!important}
html[data-ui="reference-v2"] .record-notes{color:#8193a8!important}
html[data-ui="reference-v2"] .record-meta{color:#73869b!important}
html[data-ui="reference-v2"] .record-action{
  background:linear-gradient(180deg,rgba(8,26,45,.92),rgba(4,15,28,.92))!important;
  border:1px solid rgba(92,139,184,.25)!important;color:#d3deea!important;
}
html[data-ui="reference-v2"] .record-action:hover{border-color:rgba(0,155,255,.46)!important;color:#fff!important;background:#071e36!important}
html[data-ui="reference-v2"] .record-action.danger,html[data-ui="reference-v2"] .danger-button{
  background:rgba(100,16,30,.18)!important;border-color:rgba(255,77,98,.42)!important;color:#ff7181!important;
}

/* BOTONES GLOBALES */
html[data-ui="reference-v2"] .primary-button{
  background:linear-gradient(180deg,#087cff,#045bd7)!important;border-color:rgba(50,157,255,.68)!important;color:#fff!important;
  box-shadow:0 0 16px rgba(0,112,255,.12),inset 0 1px rgba(255,255,255,.12)!important;
}
html[data-ui="reference-v2"] .primary-button:hover{background:linear-gradient(180deg,#1290ff,#0868e5)!important}
html[data-ui="reference-v2"] .secondary-button{
  background:linear-gradient(180deg,rgba(9,27,46,.9),rgba(4,16,30,.94))!important;
  border-color:rgba(82,132,181,.27)!important;color:#d1dce8!important;
}
html[data-ui="reference-v2"] .secondary-button:hover{border-color:rgba(0,151,255,.48)!important;background:#071d35!important;color:#fff!important}
html[data-ui="reference-v2"] button:focus-visible,
html[data-ui="reference-v2"] a:focus-visible,
html[data-ui="reference-v2"] input:focus-visible,
html[data-ui="reference-v2"] select:focus-visible,
html[data-ui="reference-v2"] textarea:focus-visible{outline:2px solid #16bfff!important;outline-offset:2px!important}

/* FORMULARIOS / MODALES */
html[data-ui="reference-v2"] .field-control,
html[data-ui="reference-v2"] input:not([type="checkbox"]):not([type="radio"]),
html[data-ui="reference-v2"] select,
html[data-ui="reference-v2"] textarea{
  background:linear-gradient(180deg,rgba(7,23,40,.94),rgba(3,14,27,.96))!important;
  border-color:rgba(72,126,178,.28)!important;color:#eef6fd!important;
}
html[data-ui="reference-v2"] .field-control:focus,
html[data-ui="reference-v2"] input:focus,
html[data-ui="reference-v2"] select:focus,
html[data-ui="reference-v2"] textarea:focus{
  border-color:rgba(0,153,255,.68)!important;box-shadow:0 0 0 3px rgba(0,139,255,.09),0 0 15px rgba(0,139,255,.045)!important;
}
html[data-ui="reference-v2"] .overlay{background:rgba(0,4,10,.78)!important;backdrop-filter:blur(7px)!important}
html[data-ui="reference-v2"] .drawer,
html[data-ui="reference-v2"] .workspace-modal,
html[data-ui="reference-v2"] .confirm-dialog,
html[data-ui="reference-v2"] .cal-editor-card,
html[data-ui="reference-v2"] .cal-day-pop{
  background:linear-gradient(145deg,#07182a,#03101e)!important;border-color:rgba(0,139,255,.34)!important;
  box-shadow:0 30px 90px rgba(0,0,0,.48),0 0 28px rgba(0,117,255,.06)!important;
}
html[data-ui="reference-v2"] .toast,html[data-ui="reference-v2"] .search-panel,html[data-ui="reference-v2"] .notification-popover{
  background:#06182b!important;border-color:rgba(0,139,255,.30)!important;box-shadow:0 22px 60px rgba(0,0,0,.42)!important;
}

/* CALENDAR PRO — solo visual */
html[data-ui="reference-v2"] .cal-app,
html[data-ui="reference-v2"] .google-calendar-shell{--cal-line:rgba(38,116,190,.22)!important}
html[data-ui="reference-v2"] .cal-shell,
html[data-ui="reference-v2"] .cal-main,
html[data-ui="reference-v2"] .cal-sidebar,
html[data-ui="reference-v2"] .cal-toolbar{
  background:linear-gradient(145deg,rgba(5,19,36,.97),rgba(3,14,27,.97))!important;
  border-color:rgba(20,108,197,.32)!important;
}
html[data-ui="reference-v2"] .cal-event,
html[data-ui="reference-v2"] .cal-month-event,
html[data-ui="reference-v2"] .cal-agenda-event{box-shadow:0 0 14px rgba(0,112,255,.07)!important}
html[data-ui="reference-v2"] .cal-now-line{background:#21d8ff!important;box-shadow:0 0 8px rgba(35,216,255,.65)!important}

/* Responsive */
@media(max-width:1280px){
  html[data-ui="reference-v2"] .topbar{grid-template-columns:minmax(190px,.62fr) minmax(250px,1fr) auto!important;gap:11px!important;padding:0 15px!important}
  html[data-ui="reference-v2"] .live-date.mdd-digital-clock{width:158px!important;min-width:158px!important;height:70px!important}
  html[data-ui="reference-v2"] .mdd-seg-digit{width:17px;height:34px}
  html[data-ui="reference-v2"] .clock-segment-group{height:35px}
}
@media(max-width:980px){
  html[data-ui="reference-v2"] .topbar{height:76px!important;grid-template-columns:minmax(0,1fr) auto!important;padding:0 11px!important}
  html[data-ui="reference-v2"] .topbar-center{display:none!important}
  html[data-ui="reference-v2"] .topbar-left p{display:none!important}
  html[data-ui="reference-v2"] .live-date.mdd-digital-clock{width:130px!important;min-width:130px!important;height:58px!important;grid-template-rows:9px 1fr 10px!important;padding:3px 7px!important}
  html[data-ui="reference-v2"] .clock-tech-day{font-size:6px!important}
  html[data-ui="reference-v2"] .clock-tech-time{height:31px!important;gap:1px!important}
  html[data-ui="reference-v2"] .mdd-seg-digit{width:14px!important;height:28px!important}
  html[data-ui="reference-v2"] .clock-segment-group{height:29px!important}
  html[data-ui="reference-v2"] .clock-colon{width:4px!important;height:24px!important}
  html[data-ui="reference-v2"] .clock-colon::before,html[data-ui="reference-v2"] .clock-colon::after{left:1px!important;width:2px!important;height:2px!important}
  html[data-ui="reference-v2"] .clock-tech-date{font-size:6px!important;letter-spacing:.55px!important}
  html[data-ui="reference-v2"] .hero-main h2,html[data-ui="reference-v2"] .hero-main p{max-width:80%}
}
@media(max-width:680px){
  html[data-ui="reference-v2"] .topbar{height:68px!important;padding:0 8px!important;gap:5px!important}
  html[data-ui="reference-v2"] .topbar-left h1{font-size:15px!important;max-width:125px!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  html[data-ui="reference-v2"] .topbar-actions{gap:4px!important}
  html[data-ui="reference-v2"] .live-date.mdd-digital-clock{width:104px!important;min-width:104px!important;height:50px!important;border-radius:9px!important;padding:2px 5px!important}
  html[data-ui="reference-v2"] .clock-tech-day{font-size:5px!important;letter-spacing:.7px!important}
  html[data-ui="reference-v2"] .clock-tech-time{height:26px!important}
  html[data-ui="reference-v2"] .mdd-seg-digit{width:11px!important;height:23px!important;filter:drop-shadow(0 0 2px currentColor)}
  html[data-ui="reference-v2"] .clock-segment-group{height:24px!important;gap:0!important}
  html[data-ui="reference-v2"] .clock-colon{width:3px!important;height:20px!important}
  html[data-ui="reference-v2"] .clock-tech-date{font-size:5px!important;letter-spacing:.25px!important}
  html[data-ui="reference-v2"] .notification-button{height:38px!important;min-width:38px!important}
  html[data-ui="reference-v2"] .cloud-button{display:none!important}
  html[data-ui="reference-v2"] #globalAddBtn{width:38px!important;min-width:38px!important;padding:0!important;font-size:0!important}
  html[data-ui="reference-v2"] #globalAddBtn::before{content:"+";font-size:21px!important;color:#fff}
  html[data-ui="reference-v2"] .main-view{padding:14px 10px 88px!important}
  html[data-ui="reference-v2"] .hero-main{min-height:170px!important;padding:18px!important}
  html[data-ui="reference-v2"] .hero-main h2{font-size:21px!important;max-width:100%!important;padding-right:36px}
  html[data-ui="reference-v2"] .hero-main p{max-width:100%!important;padding-right:28px}
  html[data-ui="reference-v2"] .hero-main::after{right:12px!important;top:28px!important;transform:none!important;font-size:38px!important;opacity:.34!important}
}
@media(max-width:390px){
  html[data-ui="reference-v2"] .live-date.mdd-digital-clock{width:94px!important;min-width:94px!important}
  html[data-ui="reference-v2"] .mdd-seg-digit{width:10px!important}
  html[data-ui="reference-v2"] .topbar-left h1{max-width:102px!important}
}
@media(prefers-reduced-motion:reduce){
  html[data-ui="reference-v2"] *,html[data-ui="reference-v2"] *::before,html[data-ui="reference-v2"] *::after{transition-duration:.01ms!important;animation-duration:.01ms!important;animation-iteration-count:1!important}
}
</style>
'''

if MARKER not in s:
    assert '</head>' in s, 'No se encontró </head>.'
    s = s.replace('</head>', css + '\n</head>', 1)

# Compatibilidad mínima del Calendar PRO: el guardado real ya lo realiza db.put().
# Si una versión antigua intenta llamar a markModified inexistente, no debe abortar el flujo.
s = s.replace(
    'await db.put("records",r);await markModified();',
    'await db.put("records",r);if(typeof markModified==="function")await markModified();',
    1
)

# Reloj real de Lima con precisión de segundos. Se mantiene un único temporizador del sistema.
start = s.find('function updateClock(){')
end_marker = '\nfunction getRecordDate(r){'
end = s.find(end_marker, start)
assert start >= 0 and end > start, 'No se encontró updateClock existente.'
new_clock = r'''function updateClock(){
  const now=new Date();
  const parts=new Intl.DateTimeFormat("es-PE",{
    timeZone:"America/Lima",weekday:"long",day:"2-digit",month:"2-digit",year:"numeric",
    hour:"2-digit",minute:"2-digit",second:"2-digit",hour12:true
  }).formatToParts(now);
  const get=t=>parts.find(x=>x.type===t)?.value||"";
  const day=get("weekday").toUpperCase();
  const dd=get("day"),mm=get("month"),yyyy=get("year");
  const hh=get("hour").padStart(2,"0"),mi=get("minute").padStart(2,"0"),ss=get("second").padStart(2,"0");
  const dp=(get("dayPeriod")||"").toLowerCase().replace(/\s/g,"");
  const period=/p/.test(dp)?"p. m.":"a. m.";
  const dateText=`${day} ${dd}/${mm}/${yyyy}`;
  const timeText=`${hh}:${mi}:${ss} ${period}`;
  const dateEl=$("todayDateBadge"),timeEl=$("liveClock"),wrap=document.querySelector(".live-date");
  if(dateEl)dateEl.textContent=dateText;
  if(timeEl)timeEl.textContent=timeText;
  const dayEl=$("clockDay"),dateOut=$("clockDate");
  if(dayEl)dayEl.textContent=day;
  if(dateOut)dateOut.textContent=`${dd} / ${mm} / ${yyyy}`;
  if(window.MDDReferenceClock?.render){
    window.MDDReferenceClock.render("clockHour",hh,false);
    window.MDDReferenceClock.render("clockMinute",mi,false);
    window.MDDReferenceClock.render("clockSecond",ss,true);
  }
  if(wrap){
    wrap.setAttribute("aria-label",`Hora actual en Lima: ${day}, ${dd}/${mm}/${yyyy}, ${timeText}`);
    wrap.title="Hora actual · America/Lima";
    wrap.dataset.timezone="America/Lima";
    wrap.dataset.clockSecond=ss;
  }
}'''
s = s[:start] + new_clock + s[end:]

# La capa previa actualiza cada 15 s; la referencia requiere segundos en vivo.
if 'updateClock();setInterval(updateClock,15000);updateCloudUI();' in s:
    s = s.replace('updateClock();setInterval(updateClock,15000);updateCloudUI();','updateClock();setInterval(updateClock,1000);updateCloudUI();',1)
elif 'updateClock();setInterval(updateClock,30000);updateCloudUI();' in s:
    s = s.replace('updateClock();setInterval(updateClock,30000);updateCloudUI();','updateClock();setInterval(updateClock,1000);updateCloudUI();',1)
else:
    raise AssertionError('No se encontró el temporizador único de updateClock().')

runtime = r'''
<script>
/* MDD_REFERENCE_UI_V2_JS */
(()=>{
  'use strict';
  const MAP={
    '0':['a','b','c','d','e','f'],'1':['b','c'],'2':['a','b','g','e','d'],'3':['a','b','c','d','g'],
    '4':['f','g','b','c'],'5':['a','f','g','c','d'],'6':['a','f','g','e','c','d'],'7':['a','b','c'],
    '8':['a','b','c','d','e','f','g'],'9':['a','b','c','d','f','g']
  };
  const P={
    a:'7,2 33,2 38,7 33,11 7,11 2,7',
    b:'34,8 39,12 39,33 34,37 30,32 30,14',
    c:'34,40 39,44 39,65 34,70 30,65 30,46',
    d:'7,67 33,67 38,72 33,76 7,76 2,72',
    e:'2,44 7,40 11,46 11,65 7,70 2,65',
    f:'2,12 7,8 11,14 11,32 7,37 2,33',
    g:'7,34 32,34 37,39 32,43 7,43 2,39'
  };
  function digitSvg(value){
    const on=new Set(MAP[String(value)]||[]);
    return `<svg class="mdd-seg-digit" viewBox="0 0 41 78" aria-hidden="true">${Object.entries(P).map(([k,pts])=>`<polygon class="seg ${on.has(k)?'on':''}" points="${pts}"></polygon>`).join('')}</svg>`;
  }
  function render(id,value){
    const el=document.getElementById(id);if(!el)return;
    const v=String(value||'00').padStart(2,'0').slice(-2);
    if(el.dataset.value===v)return;
    el.dataset.value=v;el.innerHTML=digitSvg(v[0])+digitSvg(v[1]);
  }
  window.MDDReferenceClock={render};

  function enhanceClock(){
    const clock=document.querySelector('.live-date');if(!clock)return;
    if(!clock.classList.contains('mdd-digital-clock')){
      clock.classList.add('mdd-digital-clock');
      clock.innerHTML=`
        <div class="clock-tech-day" id="clockDay">—</div>
        <div class="clock-tech-time" aria-hidden="true">
          <span class="clock-segment-group" id="clockHour"></span>
          <span class="clock-colon"></span>
          <span class="clock-segment-group" id="clockMinute"></span>
          <span class="clock-colon cyan"></span>
          <span class="clock-segment-group clock-seconds" id="clockSecond"></span>
        </div>
        <div class="clock-tech-date" id="clockDate">-- / -- / ----</div>
        <strong id="todayDateBadge" class="mdd-sr-only"></strong>
        <span id="liveClock" class="mdd-sr-only"></span>`;
    }
    clock.dataset.timezone='America/Lima';
    if(typeof updateClock==='function')updateClock();
  }
  function enhanceReferenceUI(){
    document.documentElement.dataset.ui='reference-v2';
    document.documentElement.dataset.reference='user-supplied-dark-blue-clock';
    enhanceClock();
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',enhanceReferenceUI,{once:true});
  else enhanceReferenceUI();
})();
</script>
'''
if '/* MDD_REFERENCE_UI_V2_JS */' not in s:
    assert '</body>' in s, 'No se encontró </body>.'
    s = s.replace('</body>', runtime + '\n</body>', 1)

p.write_text(s, encoding='utf-8')
print('Reference UI V2 applied:', len(s), 'bytes')
