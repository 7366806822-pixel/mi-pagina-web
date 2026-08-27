from pathlib import Path

p=Path('/tmp/index.html')
s=p.read_text(encoding='utf-8')
MARKER='/* MDD_MARK_MODIFIED_COMPAT_V1 */'

if MARKER not in s:
    assert 'function markModified(' not in s, 'markModified ya existe; no se aplica compatibilidad duplicada.'
    needle='const DEFAULT_PROJECT_COLORS='
    idx=s.find(needle)
    assert idx>=0, 'No se encontró punto estable para restaurar markModified.'
    helper='''/* MDD_MARK_MODIFIED_COMPAT_V1 */
async function markModified(){
  const value=new Date().toISOString();
  state.meta.lastModified=value;
  await db.put("meta",{key:"lastModified",value});
  return value;
}

'''
    s=s[:idx]+helper+s[idx:]

p.write_text(s,encoding='utf-8')
assert MARKER in s and 'async function markModified()' in s
print('markModified compatibility helper restored')
