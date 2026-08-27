from pathlib import Path

p=Path('/tmp/index.html')
s=p.read_text(encoding='utf-8')
MARKER='/* MDD_SUPABASE_PAGINATION_V1 */'

if MARKER not in s:
    old='''        const {data,error}=await this.client
          .from("mi_dia_a_dia_items")
          .select("item_id,payload,version,updated_at")
          .eq("workspace_id",WORKSPACE_ID).eq("store",store)
          .order("updated_at",{ascending:true});
        if(error)throw error;
        this.connected=true;this.fallback=false;
        const rows=(data||[]).map(r=>{'''
    new='''        /* MDD_SUPABASE_PAGINATION_V1 */
        const pageSize=1000;
        let offset=0,data=[];
        while(true){
          const {data:page,error}=await this.client
            .from("mi_dia_a_dia_items")
            .select("item_id,payload,version,updated_at")
            .eq("workspace_id",WORKSPACE_ID).eq("store",store)
            .order("updated_at",{ascending:true})
            .range(offset,offset+pageSize-1);
          if(error)throw error;
          const batch=page||[];
          data.push(...batch);
          if(batch.length<pageSize)break;
          offset+=pageSize;
        }
        this.connected=true;this.fallback=false;
        const rows=data.map(r=>{'''
    assert old in s, 'No se encontró la lectura Supabase original para paginar.'
    s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')
assert MARKER in s
print('Supabase pagination V1 applied')
