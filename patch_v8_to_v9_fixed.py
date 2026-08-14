from pathlib import Path
src = Path('patch_v8_to_v9.py').read_text(encoding='utf-8')
src = src.replace("new_db.strip()+'\\nconst db = new AppDB();'", "new_db.strip()")
src = src.replace("cloud_pattern=r'/\\* ===================== Cloud sync shared link ===================== \\*/.*?/\\* ===================== Rendering helpers ===================== \\*/'", "cloud_pattern=r'const CLOUD_POLL_MS=4000;.*?(?=/\\* ===================== Case workspace ===================== \\*/)'" )
src = src.replace("/* ===================== Rendering helpers ===================== */'", "'")
exec(compile(src, 'patch_v8_to_v9_fixed_runtime.py', 'exec'))
