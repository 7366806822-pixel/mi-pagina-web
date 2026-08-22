/* E&A — mejora profesional de calendario, agenda y recordatorios */
(function(){
  'use strict';

  const CAL_STYLE_ID='ea-calendar-pro-v3';
  const CAL_DAY_START=0;
  const CAL_DAY_END=24;
  const PX_PER_MIN=1;
  const SNAP=15;

  function injectCalendarStyles(){
    if(document.getElementById(CAL_STYLE_ID))return;
    const s=document.createElement('style');
    s.id=CAL_STYLE_ID;
    s.textContent=`
      .gcal-page{padding:18px 20px 24px;background:#f6f8fb;min-height:calc(100vh - 64px)}
      .gcal-head{display:flex;align-items:flex-start;gap:16px;margin-bottom:14px}.gcal-head>div:first-child{min-width:0}.gcal-head h1{margin:3px 0 4px;font-size:27px;letter-spacing:-.02em}.gcal-head p{margin:0;color:#68768a}.gcal-head .btn{margin-left:auto}
      .gcal-toolbar{display:grid;grid-template-columns:auto minmax(260px,1fr) auto;gap:12px;align-items:center;padding:10px 12px;background:#fff;border:1px solid #e1e7ee;border-radius:12px;box-shadow:0 2px 8px rgba(9,31,57,.04);margin-bottom:12px}
      .gcal-tabs{display:flex;gap:2px;padding:3px;border:1px solid #dbe2ea;border-radius:10px;background:#f7f9fc}.gcal-tabs button{border:0;background:transparent;color:#5e6c80;font-weight:800;font-size:11px;padding:8px 12px;border-radius:7px}.gcal-tabs button.active{background:#062844;color:#fff;box-shadow:0 3px 9px rgba(3,28,52,.16)}
      .gcal-nav{display:flex;align-items:center;justify-content:center;gap:8px;min-width:0}.gcal-nav strong{font:600 16px Georgia,serif;text-transform:capitalize;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.gcal-nav .iconbtn{margin:0}
      .gcal-actions{display:flex;gap:7px;align-items:center}.gcal-actions input{border:1px solid #d5dde7;border-radius:8px;padding:7px 9px;color:#243b55;background:#fff;min-height:36px}
      .gcal-layout{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:12px;align-items:start}.gcal-card{background:#fff;border:1px solid #e1e7ee;border-radius:12px;box-shadow:0 3px 12px rgba(9,31,57,.045);overflow:hidden}
      .gcal-month-dow{display:grid;grid-template-columns:repeat(7,1fr);border-bottom:1px solid #e7ebf0;background:#fafbfd}.gcal-month-dow span{text-align:center;padding:10px 5px;color:#6f7c8d;font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:.03em}
      .gcal-month-grid{display:grid;grid-template-columns:repeat(7,1fr);background:#e7ebf0;gap:1px}.gcal-month-empty{min-height:116px;background:#fafbfd}.gcal-month-day{position:relative;min-height:116px;background:#fff;padding:7px 6px;overflow:hidden}.gcal-month-day:hover{background:#fbfdff}.gcal-month-day.today .gcal-day-number{background:#0b66c2;color:#fff}.gcal-month-day.selected{box-shadow:inset 0 0 0 2px #dc8b13}.gcal-day-number{width:27px;height:27px;border-radius:50%;display:grid;place-items:center;font-size:11px;font-weight:800;color:#243b55}.gcal-add-day{position:absolute;right:7px;top:7px;width:25px;height:25px;border:0;border-radius:50%;background:transparent;color:#8995a5;display:none}.gcal-month-day:hover .gcal-add-day{display:grid;place-items:center}.gcal-add-day:hover{background:#edf4fb;color:#0b66c2}
      .gcal-chip{width:100%;border:0;border-left:3px solid #d88916;border-radius:5px;background:#fff6e8;color:#69430b;text-align:left;padding:4px 5px;margin-top:4px;display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:9px;font-weight:700}.gcal-chip:hover{background:#ffefd3}.gcal-chip[data-type="Audiencia"]{border-left-color:#1d6fc6;background:#eef6ff;color:#164b82}.gcal-chip[data-priority="Urgente"],.gcal-chip[data-priority="Alta"]{box-shadow:inset 0 0 0 1px rgba(196,65,65,.12)}.gcal-more{border:0;background:transparent;color:#426488;font-size:9px;font-weight:800;padding:4px 2px}
      .gcal-time-wrap{display:grid;grid-template-columns:66px minmax(0,1fr);height:650px;overflow:auto;position:relative}.gcal-time-labels{position:relative;height:1440px;border-right:1px solid #e6ebf0;background:#fafbfd}.gcal-time-label{position:absolute;left:0;right:0;transform:translateY(-7px);text-align:right;padding-right:10px;color:#7a8797;font-size:9px}.gcal-time-area{position:relative;min-width:0}.gcal-week-head{display:grid;grid-template-columns:66px repeat(7,minmax(110px,1fr));border-bottom:1px solid #e6ebf0;background:#fff;position:sticky;top:0;z-index:6}.gcal-week-head .spacer{border-right:1px solid #e6ebf0}.gcal-week-head button{border:0;border-right:1px solid #edf0f4;background:#fff;padding:8px 4px;color:#526176}.gcal-week-head button small{display:block;text-transform:uppercase;font-size:9px}.gcal-week-head button b{width:31px;height:31px;border-radius:50%;display:grid;place-items:center;margin:4px auto 0}.gcal-week-head button.today b{background:#0b66c2;color:#fff}
      .gcal-week-body{display:grid;grid-template-columns:66px repeat(7,minmax(110px,1fr));height:1440px;position:relative}.gcal-week-body .gcal-time-labels{grid-column:1}.gcal-day-col{position:relative;height:1440px;border-right:1px solid #e5eaf0;background:repeating-linear-gradient(to bottom,#fff 0,#fff 59px,#edf1f4 60px)}.gcal-day-col:hover{background:repeating-linear-gradient(to bottom,#fbfdff 0,#fbfdff 59px,#e7edf4 60px)}.gcal-day-col.selected{box-shadow:inset 0 0 0 1px rgba(220,139,19,.4)}
      .gcal-day-view{display:grid;grid-template-columns:66px minmax(0,1fr);height:650px;overflow:auto}.gcal-day-view .gcal-time-labels{height:1440px}.gcal-day-column{position:relative;height:1440px;background:repeating-linear-gradient(to bottom,#fff 0,#fff 59px,#edf1f4 60px)}
      .gcal-event-block{position:absolute;left:5px;right:5px;z-index:3;border:1px solid #c9dff6;border-left:4px solid #1d6fc6;background:#eff7ff;color:#173f68;border-radius:7px;padding:5px 7px 12px;overflow:hidden;text-align:left;cursor:grab;box-shadow:0 2px 5px rgba(19,62,104,.08)}.gcal-event-block:active{cursor:grabbing}.gcal-event-block[data-type="Vencimiento"]{border-left-color:#c73939;background:#fff2f2;color:#772e2e}.gcal-event-block[data-type="Reunión"]{border-left-color:#5f57b7;background:#f4f2ff;color:#443d83}.gcal-event-block[data-type="Diligencia"]{border-left-color:#16835f;background:#eefaf5;color:#225d49}.gcal-event-block[data-type="Tarea"]{border-left-color:#d88916;background:#fff7e9;color:#70490e}.gcal-event-block strong{display:block;font-size:10px;line-height:1.3}.gcal-event-block small{display:block;font-size:8px;opacity:.82;margin-top:2px;line-height:1.2}.gcal-resize{position:absolute;left:0;right:0;bottom:0;height:8px;cursor:ns-resize;background:linear-gradient(transparent,rgba(0,0,0,.05))}.gcal-now-line{position:absolute;left:0;right:0;height:2px;background:#d84d4d;z-index:5;pointer-events:none}.gcal-now-line:before{content:"";position:absolute;left:-4px;top:-4px;width:9px;height:9px;border-radius:50%;background:#d84d4d}
      .gcal-side{padding:14px}.gcal-side-head{display:flex;align-items:flex-start;justify-content:space-between;gap:8px;padding-bottom:10px;border-bottom:1px solid #e7ebf0}.gcal-side-head small{color:#7a8797}.gcal-side-head h3{margin:3px 0 0;font:600 17px Georgia,serif;text-transform:capitalize}.gcal-side-list{display:grid}.gcal-side-item{display:grid;grid-template-columns:72px minmax(0,1fr);gap:8px;padding:11px 0;border-bottom:1px solid #edf1f4}.gcal-side-item>span{font-size:9px;color:#a5660d;font-weight:800}.gcal-side-item button{border:0;background:transparent;text-align:left;color:inherit;padding:0}.gcal-side-item strong{display:block;font-size:11px}.gcal-side-item small{display:block;color:#768396;font-size:9px;margin-top:3px}.gcal-side-empty{padding:34px 10px;text-align:center;color:#8a96a5;font-size:11px}
      .gcal-agenda{padding:0}.gcal-agenda-group{border-bottom:1px solid #e7ebf0}.gcal-agenda-date{padding:10px 14px;background:#fafbfd;color:#3b526b;font-size:11px;font-weight:800;text-transform:capitalize}.gcal-agenda-row{width:100%;border:0;background:#fff;display:grid;grid-template-columns:105px minmax(0,1fr) 150px;gap:12px;align-items:center;text-align:left;padding:12px 14px;color:#243b55;border-top:1px solid #f0f2f5}.gcal-agenda-row:hover{background:#fbfdff}.gcal-agenda-row>span:first-child{font-size:10px;color:#a5660d;font-weight:800}.gcal-agenda-row strong{display:block;font-size:11px}.gcal-agenda-row small{display:block;color:#768396;font-size:9px;margin-top:3px}.gcal-agenda-row>span:last-child{text-align:right;color:#718094;font-size:9px}
      .gcal-quick{width:min(520px,100%)}.gcal-quick .modal-body{padding-top:14px}.gcal-quick-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}.gcal-quick-grid .col2{grid-column:1/-1}.gcal-quick-note{font-size:10px;color:#778496;margin-top:6px}.gcal-event-detail{display:grid;gap:10px}.gcal-detail-line{display:grid;grid-template-columns:130px minmax(0,1fr);gap:12px;padding:8px 0;border-bottom:1px solid #edf1f4}.gcal-detail-line b{font-size:10px;text-transform:uppercase;color:#7b8798}.gcal-detail-line span{font-size:12px;color:#263e59}.gcal-detail-actions{display:flex;justify-content:flex-end;gap:8px;margin-top:8px}
      @media(max-width:1100px){.gcal-layout{grid-template-columns:1fr}.gcal-side{order:2}.gcal-toolbar{grid-template-columns:1fr}.gcal-nav{order:-1}.gcal-tabs,.gcal-actions{justify-self:center}.gcal-week-body,.gcal-week-head{grid-template-columns:58px repeat(7,minmax(105px,1fr));min-width:800px}.gcal-time-wrap{overflow:auto}}
      @media(max-width:720px){.gcal-page{padding:12px 9px}.gcal-head{flex-direction:column}.gcal-head .btn{margin-left:0;width:100%}.gcal-tabs{width:100%;overflow:auto}.gcal-tabs button{flex:1;min-width:68px}.gcal-actions{width:100%}.gcal-actions input{flex:1;min-width:0}.gcal-month-day{min-height:82px;padding:5px 4px}.gcal-chip{font-size:8px;padding:3px}.gcal-add-day{display:none!important}.gcal-month-day .gcal-chip:nth-of-type(n+2){display:none}.gcal-week-body,.gcal-week-head{min-width:780px}.gcal-time-wrap{height:600px}.gcal-agenda-row{grid-template-columns:80px minmax(0,1fr)}.gcal-agenda-row>span:last-child{grid-column:1/-1;text-align:left;padding-left:92px}.gcal-quick-grid{grid-template-columns:1fr}.gcal-quick-grid .col2{grid-column:1}.gcal-detail-line{grid-template-columns:1fr;gap:3px}.gcal-side{padding:12px}}
    `;
    document.head.appendChild(s);
  }

  function limaDateISO(date=new Date()){
    const parts=new Intl.DateTimeFormat('en-CA',{timeZone:'America/Lima',year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(date);
    const g=t=>parts.find(p=>p.type===t)?.value||'';
    return `${g('year')}-${g('month')}-${g('day')}`;
  }
  function parseDate(s){const [y,m,d]=String(s||'').split('-').map(Number);return new Date(y,m-1,d||1,12,0,0)}
  function isoDate(d){return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`}
  function addDays(d,n){const x=new Date(d);x.setDate(x.getDate()+n);return x}
  function addMonths(d,n){const x=new Date(d);x.setMonth(x.getMonth()+n);return x}
  function monday(d){const x=new Date(d);const day=x.getDay()||7;x.setDate(x.getDate()-day+1);return x}
  function minsFromTime(v){if(!v)return 9*60;const [h,m]=String(v).slice(0,5).split(':').map(Number);return (Number(h)||0)*60+(Number(m)||0)}
  function timeFromMins(m){m=Math.max(0,Math.min(1439,Math.round(m)));return `${String(Math.floor(m/60)).padStart(2,'0')}:${String(m%60).padStart(2,'0')}:00`}
  function snapMins(m){return Math.max(0,Math.min(1439,Math.round(m/SNAP)*SNAP))}
  function durationMins(r){const s=minsFromTime(r.start_time),e=minsFromTime(r.end_time);return Math.max(SNAP,e>s?e-s:60)}
  function eventLabel(r){return `${fmtTime12(r.start_time)} ${esc(r.title||'Evento')}`}
  function viewTitle(view,d){
    if(view==='day')return d.toLocaleDateString('es-PE',{weekday:'long',day:'numeric',month:'long',year:'numeric'});
    if(view==='week'){const st=monday(d),en=addDays(st,6);return `${st.toLocaleDateString('es-PE',{day:'numeric',month:'short'})} – ${en.toLocaleDateString('es-PE',{day:'numeric',month:'short',year:'numeric'})}`}
    if(view==='agenda')return 'Agenda jurídica';
    return d.toLocaleDateString('es-PE',{month:'long',year:'numeric'});
  }

  function openQuickEvent(seed={}){
    const root=$('#modalRoot');
    const date=seed.event_date||state.calendarSelected||limaDateISO();
    const start=String(seed.start_time||'09:00:00').slice(0,5);
    const end=String(seed.end_time||timeFromMins(Math.min(1439,minsFromTime(start)+60))).slice(0,5);
    root.innerHTML=`<div class="backdrop"><section class="modal gcal-quick"><div class="modal-head"><h3>Nuevo evento</h3><button id="qClose">×</button></div><form id="qForm" class="modal-body"><div class="gcal-quick-grid"><label class="field col2"><span>Título *</span><input name="title" required autofocus placeholder="Ej. Audiencia de saneamiento"></label><label class="field"><span>Fecha</span><input name="event_date" type="date" value="${esc(date)}"></label><label class="field"><span>Tipo</span><select name="type"><option>Audiencia</option><option>Reunión</option><option>Diligencia</option><option>Vencimiento</option><option>Tarea</option><option>Otro</option></select></label><label class="field"><span>Hora de inicio</span><input name="start_time" type="time" value="${esc(start)}"></label><label class="field"><span>Hora final</span><input name="end_time" type="time" value="${esc(end)}"></label></div><div class="gcal-quick-note">Puede guardar con estos datos mínimos o abrir “Más detalles” para completar cliente, expediente, órgano jurisdiccional, responsable, modalidad, prioridad y observaciones.</div><div class="modal-actions"><button type="button" id="qDetails" class="btn btn-outline">Más detalles</button><button type="button" id="qCancel" class="btn btn-outline">Cancelar</button><button type="submit" id="qSave" class="btn btn-primary">Guardar</button></div></form></section></div>`;
    const close=()=>root.innerHTML='';
    $('#qClose').onclick=close;$('#qCancel').onclick=close;root.querySelector('.backdrop').onclick=e=>{if(e.target.classList.contains('backdrop'))close()};
    $('#qDetails').onclick=()=>{const fd=new FormData($('#qForm'));const obj=Object.fromEntries(fd.entries());obj.start_time=obj.start_time?obj.start_time+':00':'';obj.end_time=obj.end_time?obj.end_time+':00':'';close();openModal('events',obj)};
    $('#qForm').onsubmit=async e=>{e.preventDefault();const btn=$('#qSave');btn.disabled=true;btn.textContent='Guardando…';try{const fd=new FormData(e.target);const p=Object.fromEntries(fd.entries());p.start_time=p.start_time?p.start_time+':00':null;p.end_time=p.end_time?p.end_time+':00':null;Object.keys(p).forEach(k=>{if(p[k]==='')delete p[k]});await createRow('events',p);state.calendarSelected=p.event_date||state.calendarSelected;state.calendarDate=parseDate(state.calendarSelected);close();toast('Evento creado.');await renderCalendar()}catch(err){toast(humanError(err),'err');btn.disabled=false;btn.textContent='Guardar'}};
  }

  function detailValue(label,value){if(value==null||value==='')return '';return `<div class="gcal-detail-line"><b>${label}</b><span>${esc(value)}</span></div>`}
  function openCalendarEventDetails(row){
    const root=$('#modalRoot');
    root.innerHTML=`<div class="backdrop"><section class="modal"><div class="modal-head"><h3>${esc(row.title||'Evento')}</h3><button id="dClose">×</button></div><div class="modal-body"><div class="gcal-event-detail">${detailValue('Tipo',row.type)}${detailValue('Fecha',row.event_date)}${detailValue('Hora',`${fmtTime12(row.start_time)}${row.end_time?' – '+fmtTime12(row.end_time):''}`)}${detailValue('Cliente',row.client_name)}${detailValue('Caso',row.case_title)}${detailValue('Expediente',row.case_number)}${detailValue('Órgano jurisdiccional',row.court)}${detailValue('Responsable',row.responsible)}${detailValue('Modalidad',row.modality)}${detailValue('Dirección / enlace',row.location)}${detailValue('Prioridad',row.priority)}${detailValue('Estado',row.status)}${detailValue('Descripción',row.description)}${detailValue('Observaciones',row.observations)}</div><div class="gcal-detail-actions"><button id="dDelete" class="btn btn-danger">Eliminar</button><button id="dEdit" class="btn btn-primary">Editar</button></div></div></section></div>`;
    const close=()=>root.innerHTML='';$('#dClose').onclick=close;root.querySelector('.backdrop').onclick=e=>{if(e.target.classList.contains('backdrop'))close()};
    $('#dEdit').onclick=()=>{close();openModal('events',row)};
    $('#dDelete').onclick=async()=>{try{await deleteRow('events',row);close();toast('Evento eliminado.');await renderCalendar()}catch(e){toast(humanError(e),'err')}};
  }

  async function moveEvent(row,newDate,newStartMins){
    const dur=durationMins(row);const payload={event_date:newDate};
    if(Number.isFinite(newStartMins)){const s=snapMins(newStartMins);payload.start_time=timeFromMins(s);payload.end_time=timeFromMins(Math.min(1439,s+dur))}
    try{await updateRow('events',row.id,payload);toast('Evento reprogramado.');await renderCalendar()}catch(e){toast(humanError(e),'err')}
  }
  async function resizeEvent(row,newDuration){
    const s=minsFromTime(row.start_time),dur=Math.max(SNAP,snapMins(newDuration));
    try{await updateRow('events',row.id,{end_time:timeFromMins(Math.min(1439,s+dur))});toast('Duración actualizada.');await renderCalendar()}catch(e){toast(humanError(e),'err')}
  }

  function monthBody(rows,d,selected){
    const y=d.getFullYear(),m=d.getMonth(),first=new Date(y,m,1),last=new Date(y,m+1,0),blank=(first.getDay()+6)%7,parts=[];
    for(let i=0;i<blank;i++)parts.push('<div class="gcal-month-empty"></div>');
    const ym=`${y}-${String(m+1).padStart(2,'0')}`,today=limaDateISO();
    for(let n=1;n<=last.getDate();n++){
      const ds=`${ym}-${String(n).padStart(2,'0')}`;const ev=rows.filter(e=>e.event_date===ds).sort((a,b)=>String(a.start_time||'').localeCompare(String(b.start_time||'')));
      parts.push(`<div class="gcal-month-day ${ds===today?'today ':''}${ds===selected?'selected':''}" data-date="${ds}"><span class="gcal-day-number">${n}</span><button class="gcal-add-day" data-quick="${ds}" title="Nuevo evento">＋</button>${ev.slice(0,3).map(x=>`<button class="gcal-chip" draggable="true" data-event="${x.id}" data-type="${esc(x.type||'')}" data-priority="${esc(x.priority||'')}">${eventLabel(x)}</button>`).join('')}${ev.length>3?`<button class="gcal-more" data-more="${ds}">+${ev.length-3} más</button>`:''}</div>`);
    }
    return `<div class="gcal-month-dow">${['LUN','MAR','MIÉ','JUE','VIE','SÁB','DOM'].map(x=>`<span>${x}</span>`).join('')}</div><div class="gcal-month-grid">${parts.join('')}</div>`;
  }

  function timeLabels(){return Array.from({length:CAL_DAY_END-CAL_DAY_START},(_,i)=>{const h=CAL_DAY_START+i;return `<span class="gcal-time-label" style="top:${h*60*PX_PER_MIN}px">${fmtTime12(`${String(h).padStart(2,'0')}:00:00`)}</span>`}).join('')}
  function eventBlock(x){const s=minsFromTime(x.start_time),dur=durationMins(x);return `<button class="gcal-event-block" draggable="true" data-event="${x.id}" data-type="${esc(x.type||'')}" style="top:${s*PX_PER_MIN}px;height:${Math.max(28,dur*PX_PER_MIN)}px"><strong>${esc(x.title||'Evento')}</strong><small>${fmtTime12(x.start_time)}${x.end_time?' – '+fmtTime12(x.end_time):''}${x.case_number?' · Exp. '+esc(x.case_number):''}</small><span class="gcal-resize" data-resize="${x.id}"></span></button>`}
  function nowLineFor(ds){if(ds!==limaDateISO())return '';const n=new Date();const p=new Intl.DateTimeFormat('en-US',{timeZone:'America/Lima',hour:'2-digit',minute:'2-digit',hour12:false}).formatToParts(n),g=t=>Number(p.find(x=>x.type===t)?.value||0),mins=g('hour')*60+g('minute');return `<span class="gcal-now-line" style="top:${mins*PX_PER_MIN}px"></span>`}

  function weekBody(rows,d,selected){
    const st=monday(d),days=Array.from({length:7},(_,i)=>addDays(st,i));
    return `<div class="gcal-time-wrap" data-time-scroll><div style="min-width:800px"><div class="gcal-week-head"><div class="spacer"></div>${days.map(day=>{const ds=isoDate(day);return `<button data-select-date="${ds}" class="${ds===limaDateISO()?'today':''}"><small>${day.toLocaleDateString('es-PE',{weekday:'short'})}</small><b>${day.getDate()}</b></button>`}).join('')}</div><div class="gcal-week-body"><div class="gcal-time-labels">${timeLabels()}</div>${days.map(day=>{const ds=isoDate(day),ev=rows.filter(e=>e.event_date===ds);return `<div class="gcal-day-col ${ds===selected?'selected':''}" data-date="${ds}">${nowLineFor(ds)}${ev.map(eventBlock).join('')}</div>`}).join('')}</div></div></div>`;
  }
  function dayBody(rows,d){const ds=isoDate(d),ev=rows.filter(e=>e.event_date===ds);return `<div class="gcal-day-view" data-time-scroll><div class="gcal-time-labels">${timeLabels()}</div><div class="gcal-day-column" data-date="${ds}">${nowLineFor(ds)}${ev.map(eventBlock).join('')}</div></div>`}
  function agendaBody(rows,d){
    const start=isoDate(d);const filtered=rows.filter(r=>r.event_date&&r.event_date>=start).sort((a,b)=>`${a.event_date}${a.start_time||''}`.localeCompare(`${b.event_date}${b.start_time||''}`)).slice(0,120);if(!filtered.length)return '<div class="empty-page"><i data-lucide="calendar-search"></i><h3>Sin eventos próximos</h3><p>No existen actividades programadas desde esta fecha.</p></div>';
    const groups={};filtered.forEach(r=>(groups[r.event_date]??=[]).push(r));return `<div class="gcal-agenda">${Object.entries(groups).map(([ds,ev])=>`<section class="gcal-agenda-group"><div class="gcal-agenda-date">${parseDate(ds).toLocaleDateString('es-PE',{weekday:'long',day:'numeric',month:'long',year:'numeric'})}</div>${ev.map(x=>`<button class="gcal-agenda-row" data-event="${x.id}"><span>${fmtTime12(x.start_time)}</span><span><strong>${esc(x.title||'Evento')}</strong><small>${esc(x.type||'')}${x.case_number?' · Exp. '+esc(x.case_number):''}${x.responsible?' · '+esc(x.responsible):''}</small></span><span>${esc(x.status||'Programado')}</span></button>`).join('')}</section>`).join('')}</div>`;
  }
  function sideAgenda(rows,selected){const ev=rows.filter(e=>e.event_date===selected).sort((a,b)=>String(a.start_time||'').localeCompare(String(b.start_time||'')));return `<aside class="gcal-card gcal-side"><div class="gcal-side-head"><div><small>Agenda del día</small><h3>${parseDate(selected).toLocaleDateString('es-PE',{weekday:'long',day:'numeric',month:'long'})}</h3></div><button class="iconbtn" data-quick="${selected}" title="Nuevo evento">＋</button></div><div class="gcal-side-list">${ev.length?ev.map(x=>`<div class="gcal-side-item"><span>${fmtTime12(x.start_time)}</span><button data-event="${x.id}"><strong>${esc(x.title||'Evento')}</strong><small>${esc(x.type||'')}${x.case_number?' · Exp. '+esc(x.case_number):''}</small></button></div>`).join(''):'<div class="gcal-side-empty">No hay actividades programadas para esta fecha.</div>'}</div></aside>`}

  function bindCalendarInteractions(rows){
    const root=$('#content');
    root.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>{state.calendarView=b.dataset.view;renderCalendar()});
    $('#todayCal')?.addEventListener('click',()=>{state.calendarDate=parseDate(limaDateISO());state.calendarSelected=limaDateISO();renderCalendar()});
    $('#calDatePick')?.addEventListener('change',e=>{if(!e.target.value)return;state.calendarSelected=e.target.value;state.calendarDate=parseDate(e.target.value);renderCalendar()});
    $('#prevCal')?.addEventListener('click',()=>{const v=state.calendarView;state.calendarDate=v==='month'?addMonths(state.calendarDate,-1):v==='week'?addDays(state.calendarDate,-7):addDays(state.calendarDate,-1);if(v==='day')state.calendarSelected=isoDate(state.calendarDate);renderCalendar()});
    $('#nextCal')?.addEventListener('click',()=>{const v=state.calendarView;state.calendarDate=v==='month'?addMonths(state.calendarDate,1):v==='week'?addDays(state.calendarDate,7):addDays(state.calendarDate,1);if(v==='day')state.calendarSelected=isoDate(state.calendarDate);renderCalendar()});
    $('#calNew')?.addEventListener('click',()=>openQuickEvent({event_date:state.calendarSelected}));
    root.querySelectorAll('[data-quick]').forEach(b=>b.onclick=e=>{e.stopPropagation();openQuickEvent({event_date:b.dataset.quick})});
    root.querySelectorAll('[data-select-date]').forEach(b=>b.onclick=()=>{state.calendarSelected=b.dataset.selectDate;state.calendarDate=parseDate(b.dataset.selectDate);renderCalendar()});
    root.querySelectorAll('[data-more]').forEach(b=>b.onclick=e=>{e.stopPropagation();state.calendarSelected=b.dataset.more;state.calendarDate=parseDate(b.dataset.more);state.calendarView='agenda';renderCalendar()});
    root.querySelectorAll('[data-event]').forEach(b=>{b.addEventListener('click',e=>{if(e.target.closest('.gcal-resize'))return;e.stopPropagation();const row=rows.find(r=>r.id===b.dataset.event);if(row)openCalendarEventDetails(row)});b.addEventListener('dragstart',e=>{if(e.target.closest('.gcal-resize')){e.preventDefault();return}const row=rows.find(r=>r.id===b.dataset.event);if(!row)return;e.dataTransfer.setData('text/plain',row.id);e.dataTransfer.effectAllowed='move'})});

    root.querySelectorAll('.gcal-month-day').forEach(day=>{
      day.addEventListener('click',e=>{if(e.target.closest('[data-event],[data-more],[data-quick]'))return;state.calendarSelected=day.dataset.date;openQuickEvent({event_date:day.dataset.date})});
      day.addEventListener('dragover',e=>{e.preventDefault();e.dataTransfer.dropEffect='move'});
      day.addEventListener('drop',e=>{e.preventDefault();const row=rows.find(r=>r.id===e.dataTransfer.getData('text/plain'));if(row)moveEvent(row,day.dataset.date,NaN)});
    });
    root.querySelectorAll('.gcal-day-col,.gcal-day-column').forEach(col=>{
      col.addEventListener('click',e=>{if(e.target.closest('[data-event]'))return;const rect=col.getBoundingClientRect();const sc=col.closest('[data-time-scroll]');const y=e.clientY-rect.top+(sc?.scrollTop||0);const mins=snapMins(y/PX_PER_MIN);state.calendarSelected=col.dataset.date;openQuickEvent({event_date:col.dataset.date,start_time:timeFromMins(mins),end_time:timeFromMins(Math.min(1439,mins+60))})});
      col.addEventListener('dragover',e=>{e.preventDefault();e.dataTransfer.dropEffect='move'});
      col.addEventListener('drop',e=>{e.preventDefault();const row=rows.find(r=>r.id===e.dataTransfer.getData('text/plain'));if(!row)return;const rect=col.getBoundingClientRect();const sc=col.closest('[data-time-scroll]');const y=e.clientY-rect.top+(sc?.scrollTop||0);moveEvent(row,col.dataset.date,snapMins(y/PX_PER_MIN))});
    });
    root.querySelectorAll('[data-resize]').forEach(handle=>{
      handle.addEventListener('pointerdown',e=>{e.preventDefault();e.stopPropagation();const row=rows.find(r=>r.id===handle.dataset.resize);if(!row)return;const card=handle.closest('.gcal-event-block'),startY=e.clientY,startH=card.getBoundingClientRect().height,origDur=durationMins(row);card.setPointerCapture?.(e.pointerId);let newDur=origDur;const move=ev=>{const delta=ev.clientY-startY;newDur=Math.max(SNAP,snapMins((startH+delta)/PX_PER_MIN));card.style.height=`${Math.max(28,newDur*PX_PER_MIN)}px`};const up=()=>{document.removeEventListener('pointermove',move);document.removeEventListener('pointerup',up);resizeEvent(row,newDur)};document.addEventListener('pointermove',move);document.addEventListener('pointerup',up,{once:true})});
    });
    const scroller=root.querySelector('[data-time-scroll]');if(scroller&&!state.calendarScrolled){state.calendarScrolled=true;requestAnimationFrame(()=>{scroller.scrollTop=Math.max(0,(8*60-30)*PX_PER_MIN)})}
    icon();
  }

  async function enhancedRenderCalendar(){
    injectCalendarStyles();
    const c=$('#content');c.innerHTML='<div class="loader">Cargando calendario profesional…</div>';
    try{
      const rows=await getRows('events','event_date',true);state.rows.events=rows;state.calendarView=state.calendarView||'month';state.calendarSelected=state.calendarSelected||limaDateISO();state.calendarDate=state.calendarDate instanceof Date&&!Number.isNaN(state.calendarDate)?state.calendarDate:parseDate(state.calendarSelected);state.calendarScrolled=false;
      const d=state.calendarDate,view=state.calendarView,selected=state.calendarSelected;
      const body=view==='month'?monthBody(rows,d,selected):view==='week'?weekBody(rows,d,selected):view==='day'?dayBody(rows,d):agendaBody(rows,d);
      c.innerHTML=`<section class="gcal-page"><div class="gcal-head"><div><div class="eyebrow">Calendario jurídico</div><h1>Calendario y agenda</h1><p>Organización visual de audiencias, vencimientos y actividades con sincronización en tiempo real.</p></div><button id="calNew" class="btn btn-primary">＋ Nuevo evento</button></div><div class="gcal-toolbar"><div class="gcal-tabs"><button data-view="day" class="${view==='day'?'active':''}">Día</button><button data-view="week" class="${view==='week'?'active':''}">Semana</button><button data-view="month" class="${view==='month'?'active':''}">Mes</button><button data-view="agenda" class="${view==='agenda'?'active':''}">Agenda</button></div><div class="gcal-nav"><button id="prevCal" class="iconbtn" title="Anterior">‹</button><strong>${esc(viewTitle(view,d))}</strong><button id="nextCal" class="iconbtn" title="Siguiente">›</button></div><div class="gcal-actions"><input id="calDatePick" type="date" value="${esc(selected)}"><button id="todayCal" class="btn btn-outline">Hoy</button></div></div><div class="gcal-layout"><div class="gcal-card">${body}</div>${view==='agenda'?'':sideAgenda(rows,selected)}</div></section>`;
      bindCalendarInteractions(rows);
    }catch(e){c.innerHTML=`<div class="page"><div class="table-card empty-page"><h3>No se pudo cargar el calendario</h3><p>${esc(humanError(e))}</p></div></div>`;toast(humanError(e),'err')}
  }

  async function enhancedReminderEngine(){
    if(state.reminderStarted)return;state.reminderStarted=true;
    if('serviceWorker' in navigator)navigator.serviceWorker.register('./sw.js',{scope:'./'}).catch(()=>{});
    const check=async()=>{try{await sb.rpc('enqueue_upcoming_reminders')}catch(e){console.warn('Recordatorios:',e)}await loadNotifications(true)};
    await check();state.reminderTimer=setInterval(check,60000);
  }

  function hardenBranding(){
    document.title='E&A | Estudio Castañeda y Asociados';
    const ensure=(selector,attrs)=>{let el=document.querySelector(selector);if(!el){el=document.createElement(attrs.tag||'meta');document.head.appendChild(el)}Object.entries(attrs).forEach(([k,v])=>{if(k!=='tag')el.setAttribute(k,v)})};
    ensure('meta[name="description"]',{name:'description',content:'Sistema jurídico de gestión de E&A Estudio Castañeda y Asociados.'});
    ensure('meta[name="application-name"]',{name:'application-name',content:'E&A Estudio Castañeda y Asociados'});
    ensure('meta[property="og:title"]',{property:'og:title',content:'E&A | Estudio Castañeda y Asociados'});
    ensure('meta[property="og:description"]',{property:'og:description',content:'Sistema jurídico profesional de gestión de casos, audiencias, calendario y documentos.'});
    ensure('meta[name="apple-mobile-web-app-title"]',{name:'apple-mobile-web-app-title',content:'E&A Jurídico'});
    document.documentElement.setAttribute('data-brand','ea-estudio-castaneda');
  }

  hardenBranding();injectCalendarStyles();
  window.renderCalendar=enhancedRenderCalendar;
  window.setupReminderEngine=enhancedReminderEngine;
})();
