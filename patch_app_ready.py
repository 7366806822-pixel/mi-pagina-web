from pathlib import Path

p=Path('/tmp/index.html')
s=p.read_text(encoding='utf-8')
MARKER='/* MDD_APP_READY_V1 */'
if MARKER not in s:
    old='''  renderNav();
  renderMain();
  bindEvents();
  applyPreferences();'''
    new='''  renderNav();
  renderMain();
  bindEvents();
  /* MDD_APP_READY_V1 */
  document.documentElement.dataset.appReady="1";
  applyPreferences();'''
    assert old in s, 'No se encontró la secuencia de inicialización para marcar appReady.'
    s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
assert MARKER in s
print('App readiness marker applied')
