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

# A timed event is draggable. When the user grabs its resize handle, native HTML5
# dragging can compete with the pointer-based resize interaction. Disable native
# dragging only for the duration of the resize gesture, then restore it.
old_down = 'qsa("[data-resize-id]",root).forEach(h=>h.addEventListener("pointerdown",e=>{e.stopPropagation();e.preventDefault();const event=h.closest(".cal-event-wrap"),startY=e.clientY,startH=event?.getBoundingClientRect().height||56;state.calendarResize={id:h.dataset.resizeId,occurrence:h.dataset.occurrence,startY,startH,event};document.body.classList.add("cal-resizing")}));'
new_down = 'qsa("[data-resize-id]",root).forEach(h=>h.addEventListener("pointerdown",e=>{e.stopPropagation();e.preventDefault();const event=h.closest(".cal-event-wrap"),button=h.closest("[data-cal-event]"),startY=e.clientY,startH=event?.getBoundingClientRect().height||56;if(button)button.draggable=false;state.calendarResize={id:h.dataset.resizeId,occurrence:h.dataset.occurrence,startY,startH,event,button};document.body.classList.add("cal-resizing")}));'
if old_down in s:
    s = s.replace(old_down, new_down, 1)

old_up = 'if(state.calendarResize){const r=state.calendarResize;state.calendarResize=null;document.body.classList.remove("cal-resizing");const rec=state.records.find(x=>x.id===r.id);if(rec){const start=mins(rec.time||rec.hearingTime||"09:00"),dy=e.clientY-r.startY,newEnd=start+Math.round(((r.startH+dy)/HOUR_PX*60)/SLOT_MIN)*SLOT_MIN;resizeEvent(r.id,r.occurrence,newEnd)}}'
new_up = 'if(state.calendarResize){const r=state.calendarResize;state.calendarResize=null;document.body.classList.remove("cal-resizing");if(r.button)r.button.draggable=true;const rec=state.records.find(x=>x.id===r.id);if(rec){const start=mins(rec.time||rec.hearingTime||"09:00"),dy=e.clientY-r.startY,newEnd=start+Math.round(((r.startH+dy)/HOUR_PX*60)/SLOT_MIN)*SLOT_MIN;resizeEvent(r.id,r.occurrence,newEnd)}}'
if old_up in s:
    s = s.replace(old_up, new_up, 1)

if MARKER not in s:
    assert '</body>' in s, 'No se encontró </body>.'
    s = s.replace('</body>', f'<!-- {MARKER} -->\n</body>', 1)

# These guards ensure the compatibility patch really reached the generated app.
assert 'Promise.resolve()' in s, 'No se aplicó compatibilidad markModified.'
assert 'state.calendarResize={id:h.dataset.resizeId,occurrence:h.dataset.occurrence,startY,startH,event,button}' in s, 'No se aplicó la protección de resize.'
assert 'if(r.button)r.button.draggable=true' in s, 'No se restauró draggable tras resize.'

p.write_text(s, encoding='utf-8')
print('Calendar compatibility V2 logic applied with stable marker:', len(s), 'bytes')
