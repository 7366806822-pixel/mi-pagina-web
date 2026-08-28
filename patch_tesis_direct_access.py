from pathlib import Path
import re
import sys

path = Path(sys.argv[1] if len(sys.argv) > 1 else '/tmp/tesis-source.js')
s = path.read_text(encoding='utf-8')
original = s

# Replace the visible email/password flow with a server-managed, passwordless session.
# The service-role credential stays inside the Supabase Edge Function and is never shipped to the browser.
pattern = re.compile(
    r"async function init\(\)\{.*?\n\}\n\nfunction renderAuth\(mode='login'\)\{.*?\n\}\n\nasync function ensureProject\(\)\{",
    re.S,
)
replacement = r'''let automaticSessionPromise=null;
async function requestDirectSession(){
  const response=await fetch(`${SUPABASE_URL}/functions/v1/tesis-direct-session`,{
    method:'POST',
    headers:{
      'apikey':SUPABASE_KEY,
      'content-type':'application/json',
      'x-tesis-client':'tesis-untrm-direct-v1'
    },
    body:'{}',
    cache:'no-store'
  });
  let payload={};
  try{payload=await response.json();}catch{}
  if(!response.ok||!payload?.token_hash)throw new Error('No se pudo obtener la sesión directa del servidor.');
  const {data,error}=await sb.auth.verifyOtp({token_hash:payload.token_hash,type:'email'});
  if(error)throw new Error(`No se pudo validar la sesión directa: ${error.message}`);
  const session=data?.session||null;
  const user=data?.user||session?.user||null;
  if(!session||!user)throw new Error('Supabase no devolvió una sesión directa válida.');
  state.session=session;
  state.user=user;
  return session;
}

async function ensureAutomaticSession(){
  if(automaticSessionPromise)return automaticSessionPromise;
  automaticSessionPromise=(async()=>{
    const {data:current,error:sessionError}=await sb.auth.getSession();
    if(sessionError)console.warn('No se pudo recuperar la sesión previa:',sessionError);
    if(current?.session){
      state.session=current.session;
      state.user=current.session.user||null;
      return current.session;
    }
    return await requestDirectSession();
  })();
  try{return await automaticSessionPromise;}finally{automaticSessionPromise=null;}
}

function renderAccessError(error){
  const message=error?.message||String(error||'Error de conexión');
  app.innerHTML=`<div class="boot"><div class="card pad" style="max-width:620px;margin:auto"><div class="crest">TJ</div><h2>No se pudo conectar con el servicio de datos</h2><p class="muted">${esc(message)}</p><button class="btn primary" id="retryDirectAccess">Reintentar</button></div></div>`;
  const retry=document.querySelector('#retryDirectAccess');
  if(retry)retry.onclick=()=>location.reload();
}

async function recoverAutomaticSession(){
  try{
    await ensureAutomaticSession();
    await ensureProject();
    renderShell();
  }catch(error){
    console.error(error);
    renderAccessError(error);
  }
}

async function init(){
  await ensureAutomaticSession();
  await ensureProject();
  renderShell();
  sb.auth.onAuthStateChange((_event,session)=>{
    state.session=session;
    state.user=session?.user||null;
    if(!state.user)setTimeout(()=>recoverAutomaticSession(),0);
  });
  window.addEventListener('hashchange',()=>{state.route=routeFromHash();if(state.user)renderMain();});
  if('serviceWorker' in navigator){navigator.serviceWorker.register('./sw.js').catch(()=>{});}
}

function renderAuth(){
  app.innerHTML='<div class="boot"><div class="spinner"></div><p>Cargando plataforma…</p></div>';
}

async function ensureProject(){'''
s, count = pattern.subn(replacement, s, count=1)
if count != 1:
    raise SystemExit(f'ERROR: auth flow replacement count={count}')

old_footer = '''<div class="sidebar-foot"><div class="user-mini"><div class="avatar">${esc((state.user.email||'U')[0].toUpperCase())}</div><div class="meta"><strong>${esc(state.user.user_metadata?.display_name||'Tesista')}</strong><span>${esc(state.user.email||'')}</span></div><button class="btn ghost sm" id="logout" title="Cerrar sesión">↪</button></div></div>'''
new_footer = '''<div class="sidebar-foot"><div class="user-mini"><div class="avatar">TJ</div><div class="meta"><strong>Tesista</strong><span>Acceso directo</span></div></div></div>'''
if old_footer not in s:
    raise SystemExit('ERROR: sidebar auth footer not found')
s = s.replace(old_footer, new_footer, 1)

old_logout = "  document.querySelector('#logout').onclick=()=>sb.auth.signOut();\n"
if old_logout not in s:
    raise SystemExit('ERROR: logout binding not found')
s = s.replace(old_logout, '', 1)

s = s.replace('<b>Autenticación</b><br><span class="muted">Supabase Auth activo.</span>', '<b>Acceso directo</b><br><span class="muted">Sesión técnica gestionada por servidor, sin correo ni contraseña visibles.</span>')
s = s.replace('<b>Row Level Security</b><br><span class="muted">Cada usuario accede solo a sus propios datos.</span>', '<b>Row Level Security</b><br><span class="muted">Los datos continúan protegidos por auth.uid() y políticas RLS.</span>')

for forbidden in ['signInWithPassword','signInAnonymously','id="authForm"','Correo electrónico','Crear cuenta segura','title="Cerrar sesión"','SUPABASE_SERVICE_ROLE_KEY']:
    if forbidden in s:
        raise SystemExit(f'ERROR: forbidden login/secret artifact remains: {forbidden}')
for required in ['tesis-direct-session','verifyOtp','ensureAutomaticSession','renderShell();','Acceso directo']:
    if required not in s:
        raise SystemExit(f'ERROR: required direct-access marker missing: {required}')

path.write_text(s, encoding='utf-8')
print(f'Patched thesis direct access: {len(original)} -> {len(s)} bytes')
