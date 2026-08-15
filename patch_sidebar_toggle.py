from pathlib import Path

p = Path('/tmp/index.html')
s = p.read_text(encoding='utf-8')

CSS_MARKER = '/* MDD_SIDEBAR_REVERSIBLE_V1 */'
JS_MARKER = '/* MDD_SIDEBAR_REVERSIBLE_V1_JS */'

fix_css = r'''
/* MDD_SIDEBAR_REVERSIBLE_V1 */
/* El botón de contraer permanece disponible cuando el menú está cerrado. */
@media (min-width:921px){
  .brand-block{position:relative}
  .sidebar-collapsed .sidebar-collapse{
    display:inline-grid!important;
    position:absolute;
    right:-14px;
    top:23px;
    z-index:125;
    width:28px;
    min-width:28px;
    height:28px;
    border-radius:999px!important;
    border-color:rgba(196,211,227,.24);
    background:#13263a;
    color:#dce7f2;
    box-shadow:0 8px 24px rgba(0,0,0,.30);
  }
  .sidebar-collapsed .sidebar-collapse:hover{
    background:#1a3550;
    color:#fff;
    border-color:rgba(143,180,219,.42);
  }
  .sidebar-collapsed .sidebar-collapse:focus-visible{
    box-shadow:0 0 0 3px rgba(59,130,246,.28),0 8px 24px rgba(0,0,0,.30);
  }
}
@media (max-width:920px){
  .sidebar-collapsed .sidebar-collapse{display:none!important}
}
'''

fix_js = r'''

/* MDD_SIDEBAR_REVERSIBLE_V1_JS */
(() => {
  'use strict';
  const SIDEBAR_KEY = 'mdd_sidebar_collapsed';
  const btn = document.getElementById('sidebarCollapse');
  if (!btn) return;

  const isDesktop = () => window.matchMedia('(min-width: 921px)').matches;

  const syncSidebarButton = () => {
    const collapsed = document.body.classList.contains('sidebar-collapsed') && isDesktop();
    btn.textContent = collapsed ? '›' : '‹';
    btn.setAttribute('aria-label', collapsed ? 'Expandir menú' : 'Contraer menú');
    btn.setAttribute('aria-expanded', collapsed ? 'false' : 'true');
    btn.setAttribute('aria-controls', 'sidebar');
    btn.title = (collapsed ? 'Expandir menú' : 'Contraer menú') + ' · Alt+M';
  };

  const toggleSidebarFallback = () => {
    if (!isDesktop()) return;
    document.body.classList.toggle('sidebar-collapsed');
    try {
      localStorage.setItem(
        SIDEBAR_KEY,
        document.body.classList.contains('sidebar-collapsed') ? '1' : '0'
      );
    } catch (_) {}
    syncSidebarButton();
  };

  const observer = new MutationObserver(syncSidebarButton);
  observer.observe(document.body, {attributes:true, attributeFilter:['class']});
  window.addEventListener('resize', syncSidebarButton, {passive:true});

  document.addEventListener('keydown', (e) => {
    if (e.altKey && !e.ctrlKey && !e.metaKey && String(e.key).toLowerCase() === 'm') {
      e.preventDefault();
      toggleSidebarFallback();
    }
  });

  syncSidebarButton();
})();
'''

if CSS_MARKER not in s:
    needle = '</style>'
    assert needle in s, 'No se encontró </style> para aplicar el arreglo del menú lateral.'
    s = s.replace(needle, fix_css + '\n' + needle, 1)

if JS_MARKER not in s:
    needle = '\n</script>\n</body>'
    assert needle in s, 'No se encontró el cierre del script principal.'
    s = s.replace(needle, fix_js + '\n</script>\n</body>', 1)

assert CSS_MARKER in s
assert JS_MARKER in s
assert 'display:inline-grid!important' in s
assert "collapsed ? '›' : '‹'" in s
assert "'Expandir menú' : 'Contraer menú'" in s
assert "String(e.key).toLowerCase() === 'm'" in s

p.write_text(s, encoding='utf-8')
