from pathlib import Path

p = Path('/tmp/index.html')
s = p.read_text(encoding='utf-8')

MARKER = '/* MDD_GOOGLE_CALENDAR_V2 */'

css = r'''
/* MDD_GOOGLE_CALENDAR_V2 */
.google-calendar-shell{display:grid;gap:12px}
.gcal-hero{padding:20px;display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap}
.gcal-hero h2{margin:6px 0 5px;font-size:23px}.gcal-hero p{margin:0;color:var(--muted);font-size:11px;line-height:1.5}
.gcal-actions{display:flex;gap:8px;flex-wrap:wrap}.gcal-actions a{text-decoration:none;display:inline-flex;align-items:center;justify-content:center}
.gcal-status{display:inline-flex;align-items:center;gap:7px;margin-top:10px;padding:6px 9px;border:1px solid rgba(36,166,106,.26);background:var(--green-bg);color:#78dfaa;border-radius:999px;font-size:10px;font-weight:850}
.gcal-status i{width:7px;height:7px;border-radius:50%;background:var(--green);box-shadow:0 0 10px rgba(36,166,106,.6)}
.gcal-stat-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}
.gcal-stat{padding:15px}.gcal-stat span{display:block;color:var(--muted);font-size:9.5px;text-transform:uppercase;letter-spacing:.7px}.gcal-stat strong{display:block;margin-top:7px;font-size:22px}.gcal-stat small{display:block;margin-top:3px;color:#8191a4;font-size:9.5px}
.gcal-badge{display:inline-flex;align-items:center;gap:4px;border-radius:999px;padding:3px 7px;background:rgba(66,133,244,.12);color:#9fc2ff;border:1px solid rgba(66,133,244,.2);font-weight:900}
.gcal-native-note{padding:11px 13px;border:1px solid var(--line);background:rgba(59,130,246,.055);border-radius:12px;color:#aebdcd;font-size:10.5px;line-height:1.5}.gcal-native-note strong{color:#f4f7fb}
.gcal-calendar-chips{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px}.gcal-calendar-chip{font-size:9.5px;padding:5px 8px;border-radius:999px;background:rgba(255,255,255,.035);border:1px solid var(--line);color:#aebdcd}
.record-action.gcal-link{text-decoration:none;display:inline-flex;align-items:center}
.timeline-event.gcal-event,.week-event.gcal-event{box-shadow:inset 2px 0 0 #4285f4}
.calendar-event.gcal-event{box-shadow:inset 2px 0 0 #4285f4}
@media(max-width:1000px){.gcal-stat-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:620px){.gcal-stat-grid{grid-template-columns:1fr}.gcal-actions{width:100%}.gcal-actions a{flex:1 1 170px}.gcal-hero{padding:15px}}
'''

if MARKER not in s:
    style_end = '</style>'
    assert style_end in s, 'No se encontró </style> para Google Calendar V2.'
    s = s.replace(style_end, css + '\n' + style_end, 1)

    nav_needle = '{label:"Calendario", icon:"▦", special:"calendar", id:"calendar"},'
    assert nav_needle in s, 'No se encontró el ítem Calendario en NAV_GROUPS.'
    s = s.replace(nav_needle, nav_needle + '\n      {label:"Google Calendar", icon:"G", special:"googleCalendar", id:"google-calendar"},', 1)

    subtitle_needle = 'calendar:"Vista mensual de fechas, audiencias, vencimientos y publicaciones.",'
    assert subtitle_needle in s, 'No se encontró subtitleForSpecial.calendar.'
    s = s.replace(subtitle_needle, subtitle_needle + '\n    googleCalendar:"Agenda Google sincronizada y clasificada dentro de Mi Día a Día.",', 1)

    render_map_needle = 'calendar:renderCalendar,'
    assert render_map_needle in s, 'No se encontró renderMain.calendar.'
    s = s.replace(render_map_needle, render_map_needle + '\n      googleCalendar:renderGoogleCalendar,', 1)

    function_needle = 'function renderToday(){'
    assert function_needle in s, 'No se encontró renderToday.'
    google_calendar_js = r'''
const GOOGLE_CALENDAR_URL = "https://calendar.google.com/calendar/u/0/r";
const GOOGLE_CALENDAR_CREATE_URL = "https://calendar.google.com/calendar/u/0/r/eventedit";

function isGoogleRecord(r){return r?.source==="google_calendar" || !!r?.googleEventId}
function googleCalendarRecords(){return state.records.filter(isGoogleRecord)}
function recordOccursOn(r,iso){
  const start=getRecordDate(r);if(!start)return false;
  if(start===iso)return true;
  const end=r.endDate||start;
  return !!r.allDay && start<=iso && end>=iso;
}
function googleIntegration(){return state.meta.googleCalendarIntegration||{}}
function googleCalendarLabel(r){return r.googleCalendarName||"Google Calendar"}
function formatSyncStamp(v){
  if(!v)return "Pendiente";
  const d=new Date(v);return Number.isNaN(d.getTime())?String(v):d.toLocaleString("es-PE",{dateStyle:"short",timeStyle:"short"});
}
async function queueGoogleSync(id){
  const r=state.records.find(x=>x.id===id);if(!r)return;
  if(isGoogleRecord(r)){
    r.googleSyncStatus="pending_update";
  }else{
    r.googleSyncStatus="pending_create";
    r.googleCalendarId=r.googleCalendarId||"primary";
  }
  r.updatedAt=new Date().toISOString();
  await db.put("records",r);await markModified();
  renderMain();toast(isGoogleRecord(r)?"Cambio marcado para sincronizar con Google.":"Evento marcado para crear en Google Calendar.");
}
function renderGoogleCalendar(){
  const meta=googleIntegration();
  const rows=googleCalendarRecords().slice().sort(sortRecords);
  const today=localISO();
  const upcoming=rows.filter(r=>(r.endDate||getRecordDate(r)||"")>=today).slice(0,30);
  const calendars=[...new Set(rows.map(googleCalendarLabel).filter(Boolean))];
  const todayRows=rows.filter(r=>recordOccursOn(r,today));
  const pending=state.records.filter(r=>["pending_create","pending_update","pending_delete"].includes(r.googleSyncStatus)).length;
  const university=rows.filter(r=>r.area==="Universidad").length;
  const legal=rows.filter(r=>r.area==="Estudio jurídico").length;
  const connected=meta.enabled!==false;
  $("mainView").innerHTML=`
    <div class="google-calendar-shell">
      <section class="panel gcal-hero">
        <div>
          <span class="eyebrow">GOOGLE CALENDAR · INTEGRACIÓN NATIVA</span>
          <h2>Google Calendar + Mi Día a Día</h2>
          <p>Los eventos sincronizados son registros nativos: alimentan Hoy, Plan del día, Semana, Agenda, Calendario y sus módulos correspondientes.</p>
          <span class="gcal-status"><i></i>${connected?"Sincronización automática activa":"Sincronización pendiente"}</span>
        </div>
        <div class="gcal-actions">
          <a class="secondary-button" href="${GOOGLE_CALENDAR_URL}" target="_blank" rel="noopener noreferrer">Abrir Google Calendar ↗</a>
          <a class="primary-button" href="${GOOGLE_CALENDAR_CREATE_URL}" target="_blank" rel="noopener noreferrer">+ Crear en Google</a>
        </div>
      </section>
      <div class="gcal-stat-grid">
        <section class="panel gcal-stat"><span>Eventos Google</span><strong>${rows.length}</strong><small>Registros nativos sincronizados</small></section>
        <section class="panel gcal-stat"><span>Para hoy</span><strong>${todayRows.length}</strong><small>Incluye eventos de todo el día</small></section>
        <section class="panel gcal-stat"><span>Calendarios</span><strong>${calendars.length||meta.calendarsProcessed||0}</strong><small>Fuentes con eventos sincronizados</small></section>
        <section class="panel gcal-stat"><span>Pendientes de salida</span><strong>${pending}</strong><small>Crear / actualizar en Google</small></section>
      </div>
      <section class="panel section-panel">
        <div class="section-head"><div><h3>Estado de sincronización</h3><p>Zona horaria: America/Lima · Última sincronización: ${esc(formatSyncStamp(meta.lastSuccessfulSync))}</p></div></div>
        <div class="gcal-native-note"><strong>Integración segura:</strong> esta vista ya no depende de un iframe ni expone credenciales Google en GitHub. La sincronización se realiza mediante las conexiones autorizadas y Supabase. Los cambios se distribuyen por Realtime.</div>
        <div class="gcal-calendar-chips">${calendars.length?calendars.map(x=>`<span class="gcal-calendar-chip">G · ${esc(x)}</span>`).join(""):`<span class="gcal-calendar-chip">Esperando primera sincronización completa</span>`}</div>
      </section>
      <div class="grid-2">
        <section class="panel section-panel"><div class="section-head"><div><h3>Próximos eventos de Google</h3><p>Ordenados por fecha y hora.</p></div></div>${listHTML(upcoming,"No hay eventos Google próximos.")}</section>
        <section class="panel section-panel"><div class="section-head"><div><h3>Clasificación automática</h3><p>Los eventos se distribuyen según su contenido y calendario de origen.</p></div></div>${summaryPills([[university,"universidad"],[legal,"jurídicos"],[rows.filter(r=>r.area==="Creación de contenido").length,"contenido"],[rows.filter(r=>r.area==="Empresas / negocios").length,"empresa"]])}<div class="gcal-native-note">Prioridad: regla manual → calendario → título/descripción → General. Los plazos académicos permanecen en Universidad y no se confunden con plazos procesales.</div></section>
      </div>
    </div>`;
}

'''
    s = s.replace(function_needle, google_calendar_js + function_needle, 1)

    # Los eventos multidía de Google deben aparecer cada día de su intervalo.
    s = s.replace(
        'const todayR=open.filter(r=>getRecordDate(r)===t||getDueDate(r)===t);',
        'const todayR=open.filter(r=>recordOccursOn(r,t)||getDueDate(r)===t);',
        1,
    )
    s = s.replace(
        'const iso=localISO(state.plannerDate), rows=state.records.filter(r=>getRecordDate(r)===iso && r.status!=="Archivado").sort(sortRecords);',
        'const iso=localISO(state.plannerDate), rows=state.records.filter(r=>recordOccursOn(r,iso) && r.status!=="Archivado").sort(sortRecords);',
        1,
    )
    s = s.replace(
        'state.records.filter(r=>getRecordDate(r)===iso&&r.status!=="Archivado").sort(sortRecords)',
        'state.records.filter(r=>recordOccursOn(r,iso)&&r.status!=="Archivado").sort(sortRecords)',
        1,
    )
    s = s.replace(
        'const events=state.records.filter(r=>getRecordDate(r)===iso).slice(0,4);',
        'const events=state.records.filter(r=>recordOccursOn(r,iso)).sort(sortRecords).slice(0,4);',
        1,
    )
    s = s.replace(
        'state.records.filter(r=>getRecordDate(r)===iso).length>4?`<div class="record-meta">+${state.records.filter(r=>getRecordDate(r)===iso).length-4} más</div>`',
        'state.records.filter(r=>recordOccursOn(r,iso)).length>4?`<div class="record-meta">+${state.records.filter(r=>recordOccursOn(r,iso)).length-4} más</div>`',
        1,
    )

    # Hora final y marca Google en Plan del día, Semana y Calendario.
    s = s.replace(
        '<button class="timeline-event ${dueClass(r)}" data-action="${recordActionName(r)}" data-id="${esc(r.id)}"><span>${esc(r.time||r.hearingTime||hh)}</span><strong>${esc(r.title)}</strong><small>${esc(r.project||r.area||"")}</small></button>',
        '<button class="timeline-event ${dueClass(r)} ${isGoogleRecord(r)?"gcal-event":""}" data-action="${recordActionName(r)}" data-id="${esc(r.id)}"><span>${esc(r.time||r.hearingTime||hh)}${r.endTime?` – ${esc(r.endTime)}`:""}${isGoogleRecord(r)?" · G":""}</span><strong>${esc(r.title)}</strong><small>${esc(r.project||r.area||"")}</small></button>',
        1,
    )
    s = s.replace(
        '<button class="week-event ${dueClass(r)}" data-action="${recordActionName(r)}" data-id="${esc(r.id)}"><span>${esc(r.time||r.hearingTime||"Todo el día")}</span><strong>${esc(r.title)}</strong><small>${esc(r.project||r.area||"")}</small></button>',
        '<button class="week-event ${dueClass(r)} ${isGoogleRecord(r)?"gcal-event":""}" data-action="${recordActionName(r)}" data-id="${esc(r.id)}"><span>${esc(r.time||r.hearingTime||"Todo el día")}${r.endTime?` – ${esc(r.endTime)}`:""}${isGoogleRecord(r)?" · G":""}</span><strong>${esc(r.title)}</strong><small>${esc(r.project||r.area||"")}</small></button>',
        1,
    )
    s = s.replace(
        '<button class="calendar-event ${["hearing"].includes(r.type)?"legal":r.type==="deadline"?"deadline":""}" data-action="${recordActionName(r)}" data-id="${esc(r.id)}">${esc(r.time||r.hearingTime||"")} ${esc(r.title)}</button>',
        '<button class="calendar-event ${["hearing"].includes(r.type)?"legal":r.type==="deadline"?"deadline":""} ${isGoogleRecord(r)?"gcal-event":""}" data-action="${recordActionName(r)}" data-id="${esc(r.id)}">${isGoogleRecord(r)?"G · ":""}${esc(r.time||r.hearingTime||"")}${r.endTime?`–${esc(r.endTime)}`:""} ${esc(r.title)}</button>',
        1,
    )

    # Fuente y accesos Google en cada registro nativo.
    details_needle = '${details.map(x=>`<span>• ${esc(x)}</span>`).join("")}'
    assert details_needle in s, 'No se encontró metadata de recordCardHTML.'
    s = s.replace(details_needle, details_needle + '\n        ${isGoogleRecord(r)?`<span class="gcal-badge">G · ${esc(googleCalendarLabel(r))}</span>`:""}', 1)

    edit_needle = '<button class="record-action" data-action="edit" data-id="${esc(r.id)}">Editar</button>'
    assert edit_needle in s, 'No se encontró acción Editar de recordCardHTML.'
    google_actions = r'''${r.googleEventUrl?`<a class="record-action gcal-link" href="${esc(r.googleEventUrl)}" target="_blank" rel="noopener noreferrer">G Abrir</a>`:""}
         ${r.meetUrl?`<a class="record-action gcal-link" href="${esc(r.meetUrl)}" target="_blank" rel="noopener noreferrer">Meet</a>`:""}
         ${(isGoogleRecord(r)||((r.date||r.dueDate)&&["event","academic","hearing","deadline","reminder","followup"].includes(r.type)))?`<button class="record-action" data-action="queue-google" data-id="${esc(r.id)}">${isGoogleRecord(r)?"Sincronizar cambios":"Enviar a Google"}</button>`:""}
         ''' + edit_needle
    s = s.replace(edit_needle, google_actions, 1)

    action_needle = 'const action=el.dataset.action,id=el.dataset.id;'
    assert action_needle in s, 'No se encontró handleAction.'
    s = s.replace(action_needle, action_needle + '\n  if(action==="queue-google"){queueGoogleSync(id);return}', 1)

assert MARKER in s
assert 'special:"googleCalendar"' in s
assert 'googleCalendar:renderGoogleCalendar' in s
assert 'function renderGoogleCalendar()' in s
assert 'function recordOccursOn' in s
assert 'pending_create' in s
assert 'pending_update' in s
assert 'Sincronización automática activa' in s
assert 'calendar.google.com/calendar/embed' not in s
assert 'America/Lima' in s

p.write_text(s, encoding='utf-8')
