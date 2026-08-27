from pathlib import Path
import base64, gzip

p = Path('/tmp/index.html')
s = p.read_text(encoding='utf-8')
MARKER = '/* MDD_CALENDAR_PRO_V1 */'

if MARKER not in s:
    js_b64 = ''.join(Path(f'calendar_pro_js.p{i:02d}').read_text(encoding='utf-8').strip() for i in range(4))
    css_b64 = Path('calendar_pro_css.p00').read_text(encoding='utf-8').strip()
    js = gzip.decompress(base64.b64decode(js_b64)).decode('utf-8')
    css = gzip.decompress(base64.b64decode(css_b64)).decode('utf-8')

    assert '</style>' in s
    s = s.replace('</style>', css + '\n</style>', 1)

    assert 'function renderCalendar(){' in s
    s = s.replace('function renderCalendar(){', 'function renderCalendarLegacy(){', 1)

    legal_marker = '/* ===================== Legal panel ===================== */'
    assert legal_marker in s
    wrapper = ('function renderCalendar(){\n'
               '  if(window.MDDCalendarPro && typeof window.MDDCalendarPro.renderCalendar==="function") return window.MDDCalendarPro.renderCalendar();\n'
               '  return renderCalendarLegacy();\n'
               '}\n\n')
    s = s.replace(legal_marker, wrapper + legal_marker, 1)

    action_needle = 'function handleAction(el){\n  const action=el.dataset.action,id=el.dataset.id;'
    assert action_needle in s
    action_repl = ('function handleAction(el){\n'
                   '  if(window.MDDCalendarPro && typeof window.MDDCalendarPro.handleAction==="function" && window.MDDCalendarPro.handleAction(el)) return;\n'
                   '  const action=el.dataset.action,id=el.dataset.id;')
    s = s.replace(action_needle, action_repl, 1)

    assert '</body>' in s
    s = s.replace('</body>', '\n<script>\n' + js + '\n</script>\n</body>', 1)

for required in [MARKER, 'MDDCalendarPro', 'function renderCalendarLegacy(){', 'calendar-save-sync', 'cal-time-lane', 'calendar-view', 'America/Lima']:
    assert required in s, f'Falta marcador requerido: {required}'

p.write_text(s, encoding='utf-8')
