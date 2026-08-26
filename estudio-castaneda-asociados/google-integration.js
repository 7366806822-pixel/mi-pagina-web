(function(){
  const originalNavigate=window.navigate;
  if(typeof originalNavigate!=='function') return;

  async function renderGoogleIntegration(){
    const c=document.querySelector('#content');
    if(!c) return;
    c.innerHTML='<div class="loader">Cargando integración de calendario…</div>';
    try{
      const [{data:rows,error:e1},{count:googleCount,error:e2}]=await Promise.all([
        sb.from('calendar_integrations').select('*').eq('provider','google').limit(1),
        sb.from('events').select('id',{count:'exact',head:true}).eq('sync_origin','Google')
      ]);
      if(e1) throw e1; if(e2) throw e2;
      const x=(rows||[])[0];
      const connected=x&&x.sync_status!=='Desconectado';
      const last=x?.last_success_at||x?.last_synced_at;
      c.innerHTML=`<section class="page integration-page">
        <div class="page-head"><div><div class="eyebrow">Integraciones</div><h1>Google Calendar</h1><p>Sincronización del calendario del estudio con Google Calendar y Supabase.</p></div></div>
        <div class="integration-grid">
          <article class="table-card integration-card main-integration">
            <div class="integration-head"><div class="google-mark">G</div><div><small>CALENDARIO EXTERNO</small><h2>Google Calendar</h2><p>Calendario principal vinculado al sistema jurídico.</p></div><span class="integration-status ${connected?'ok':'off'}">${connected?'Conectado':'Desconectado'}</span></div>
            <div class="integration-meta">
              <div><span>Cuenta</span><strong>${esc(x?.account_email||'7366806822@untrm.edu.pe')}</strong></div>
              <div><span>Calendario</span><strong>${esc(x?.calendar_name||'GENERAL')}</strong></div>
              <div><span>Zona horaria</span><strong>${esc(x?.timezone||'America/Lima')}</strong></div>
              <div><span>Sincronización</span><strong>${Number(x?.sync_interval_minutes||60)} min</strong></div>
              <div><span>Última sincronización</span><strong>${last?fmtDateTime(last):'Pendiente de primera ejecución automática'}</strong></div>
              <div><span>Eventos Google en E&A</span><strong>${Number(googleCount||0)}</strong></div>
            </div>
            ${x?.last_error?`<div class="integration-error"><b>Último error</b><span>${esc(x.last_error)}</span></div>`:''}
            <div class="integration-actions">
              <button id="requestGoogleSync" class="btn btn-primary"><i data-lucide="refresh-cw"></i> Solicitar sincronización</button>
              <button id="toggleGoogleSync" class="btn ${connected?'btn-outline':'btn-primary'}"><i data-lucide="${connected?'unlink':'link'}"></i> ${connected?'Desconectar':'Reconectar'}</button>
              <a class="btn btn-outline" href="https://calendar.google.com" target="_blank" rel="noopener noreferrer"><i data-lucide="external-link"></i> Abrir Google Calendar</a>
            </div>
            <div class="integration-note"><i data-lucide="shield-check"></i><span><b>Seguridad:</b> las credenciales privadas de Google no se almacenan en el frontend público. La plataforma conserva únicamente identificadores de sincronización y metadatos operativos.</span></div>
          </article>
          <article class="table-card integration-card"><h3>Cómo funciona</h3><ol class="integration-flow"><li><b>Google Calendar</b><span>Los eventos del calendario GENERAL se incorporan a E&A sin duplicados.</span></li><li><b>Supabase</b><span>Los cambios se guardan con identificadores únicos y se distribuyen mediante Realtime.</span></li><li><b>E&A</b><span>Los eventos aparecen en Día, Semana, Mes, Agenda y panel principal.</span></li><li><b>Recordatorios</b><span>Las audiencias y actividades sincronizadas mantienen el motor interno de avisos; los eventos creados en Google pueden usar sus alertas en todos los dispositivos con esa cuenta.</span></li></ol></article>
        </div>
      </section>`;
      document.querySelector('#requestGoogleSync')?.addEventListener('click',async()=>{
        const {error}=await sb.from('calendar_integrations').update({sync_requested_at:new Date().toISOString(),updated_at:new Date().toISOString()}).eq('id',x.id);
        if(error) return toast(humanError(error),'err');
        toast('Solicitud registrada. Se procesará en la próxima sincronización automática.');
        renderGoogleIntegration();
      });
      document.querySelector('#toggleGoogleSync')?.addEventListener('click',async()=>{
        const next=connected?'Desconectado':'Conectado';
        const {error}=await sb.from('calendar_integrations').update({sync_status:next,updated_at:new Date().toISOString()}).eq('id',x.id);
        if(error) return toast(humanError(error),'err');
        toast(next==='Conectado'?'Sincronización reactivada.':'Sincronización pausada.');
        renderGoogleIntegration();
      });
      icon();
    }catch(e){
      c.innerHTML=`<section class="page"><div class="table-card empty-page"><h3>No se pudo cargar la integración</h3><p>${esc(humanError(e))}</p></div></section>`;
    }
  }

  window.navigate=function(p){
    if(p==='integrations'){
      state.page=p;
      document.querySelectorAll('#nav button').forEach(b=>b.classList.toggle('active',b.dataset.page===p));
      document.querySelector('#sidebar')?.classList.remove('open');
      renderGoogleIntegration();
      return;
    }
    return originalNavigate(p);
  };
})();