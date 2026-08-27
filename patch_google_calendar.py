from pathlib import Path

p = Path('/tmp/index.html')
s = p.read_text(encoding='utf-8')

MARKER = '/* MDD_GOOGLE_CALENDAR_V1 */'

css = r'''
/* MDD_GOOGLE_CALENDAR_V1 */
.google-calendar-shell{padding:16px;display:grid;gap:12px}
.google-calendar-toolbar{display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap}
.google-calendar-toolbar h2{margin:5px 0 0;font-size:20px}
.google-calendar-toolbar p{margin:5px 0 0;color:var(--muted);font-size:11px;line-height:1.45}
.google-calendar-actions{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.google-calendar-actions a{text-decoration:none;display:inline-flex;align-items:center;justify-content:center}
.google-calendar-info{border:1px solid var(--line);background:rgba(59,130,246,.055);border-radius:12px;padding:10px 12px;color:#aebdcd;font-size:10.5px;line-height:1.5}
.google-calendar-info strong{color:#f4f7fb}
.google-calendar-frame-wrap{overflow:hidden;border:1px solid var(--line);border-radius:14px;background:#fff;box-shadow:var(--shadow)}
.google-calendar-frame{display:block;width:100%;height:72vh;min-height:620px;border:0;background:#fff}
@media (max-width:920px){
  .google-calendar-shell{padding:12px}
  .google-calendar-toolbar{align-items:flex-start}
  .google-calendar-actions{width:100%}
  .google-calendar-actions a{flex:1 1 190px}
  .google-calendar-frame{height:68vh;min-height:520px}
}
@media (max-width:560px){
  .google-calendar-frame{height:64vh;min-height:470px}
}
'''

if MARKER not in s:
    style_end = '</style>'
    assert style_end in s, 'No se encontró </style> para Google Calendar.'
    s = s.replace(style_end, css + '\n' + style_end, 1)

    nav_needle = '{label:"Calendario", icon:"▦", special:"calendar", id:"calendar"},'
    assert nav_needle in s, 'No se encontró el ítem Calendario en NAV_GROUPS.'
    s = s.replace(
        nav_needle,
        nav_needle + '\n      {label:"Google Calendar", icon:"G", special:"googleCalendar", id:"google-calendar"},',
        1,
    )

    subtitle_needle = 'calendar:"Vista mensual de fechas, audiencias, vencimientos y publicaciones.",'
    assert subtitle_needle in s, 'No se encontró subtitleForSpecial.calendar.'
    s = s.replace(
        subtitle_needle,
        subtitle_needle + '\n    googleCalendar:"Tu calendario principal de Google integrado en el sistema.",',
        1,
    )

    render_map_needle = 'calendar:renderCalendar,'
    assert render_map_needle in s, 'No se encontró renderMain.calendar.'
    s = s.replace(
        render_map_needle,
        render_map_needle + '\n      googleCalendar:renderGoogleCalendar,',
        1,
    )

    function_needle = 'function renderToday(){'
    assert function_needle in s, 'No se encontró renderToday para insertar Google Calendar.'
    google_calendar_js = r'''
const GOOGLE_CALENDAR_URL = "https://calendar.google.com/calendar/u/0/r";
const GOOGLE_CALENDAR_CREATE_URL = "https://calendar.google.com/calendar/u/0/r/eventedit";
const GOOGLE_CALENDAR_EMBED = "https://calendar.google.com/calendar/embed?src=7366806822%40untrm.edu.pe&ctz=America%2FLima&mode=WEEK&showTitle=0&showPrint=0&showTabs=1&showCalendars=1&showTz=1";

function renderGoogleCalendar(){
  $("mainView").innerHTML=`
    <section class="panel google-calendar-shell">
      <div class="google-calendar-toolbar">
        <div>
          <span class="eyebrow">GOOGLE CALENDAR</span>
          <h2>Calendario GENERAL</h2>
          <p>Agenda principal conectada a tu cuenta de Google · Zona horaria: América/Lima.</p>
        </div>
        <div class="google-calendar-actions">
          <a class="secondary-button" href="${GOOGLE_CALENDAR_URL}" target="_blank" rel="noopener noreferrer">Abrir Google Calendar ↗</a>
          <a class="primary-button" href="${GOOGLE_CALENDAR_CREATE_URL}" target="_blank" rel="noopener noreferrer">+ Crear evento en Google</a>
        </div>
      </div>
      <div class="google-calendar-info">
        <strong>Privacidad:</strong> integrar el calendario no cambia sus permisos de Google. Solo podrán ver sus eventos las personas que ya tengan autorización en Google Calendar.
      </div>
      <div class="google-calendar-frame-wrap">
        <iframe class="google-calendar-frame" title="Google Calendar — GENERAL" src="${GOOGLE_CALENDAR_EMBED}" loading="lazy" frameborder="0" scrolling="no"></iframe>
      </div>
    </section>`;
}

'''
    s = s.replace(function_needle, google_calendar_js + function_needle, 1)

assert MARKER in s
assert 'special:"googleCalendar"' in s
assert 'googleCalendar:renderGoogleCalendar' in s
assert 'function renderGoogleCalendar()' in s
assert 'calendar.google.com/calendar/embed?src=7366806822%40untrm.edu.pe' in s
assert 'America%2FLima' in s

p.write_text(s, encoding='utf-8')
