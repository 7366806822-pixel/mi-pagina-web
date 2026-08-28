from pathlib import Path

p = Path('/tmp/index.html')
s = p.read_text(encoding='utf-8')

MARKER = 'MDD_CALENDAR_MARKMODIFIED_COMPAT_V1'

# Calendar PRO from an older layer can still call markModified() after db.put().
# Supabase persistence is already completed by db.put(), so preserve markModified
# when it exists and safely no-op when the current data layer does not expose it.
s = s.replace(
    'await markModified();',
    'await (typeof markModified==="function"?markModified():Promise.resolve());'
)

if MARKER not in s:
    assert '</body>' in s, 'No se encontró </body>.'
    s = s.replace('</body>', f'<!-- {MARKER} -->\n</body>', 1)

p.write_text(s, encoding='utf-8')
print('Calendar markModified compatibility applied:', len(s), 'bytes')
