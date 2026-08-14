from pathlib import Path
p=Path('/tmp/index.html')
s=p.read_text(encoding='utf-8')
method='\n  subscribeRealtime(){\n    if(!this.client||this.channel)return;\n    this.channel=this.client.channel("mdd-shared-"+WORKSPACE_ID)\n      .on("postgres_changes",{\n        event:"*",schema:"public",table:"mi_dia_a_dia_items",\n        filter:`workspace_id=eq.${WORKSPACE_ID}`\n      },evt=>{\n        try{\n          const row=evt.new && Object.keys(evt.new).length?evt.new:evt.old;\n          if(!row||row.workspace_id!==WORKSPACE_ID)return;\n          const store=row.store,id=String(row.item_id||"");\n          if(!["records","trash","meta"].includes(store)||!id)return;\n          if(evt.eventType==="DELETE"){\n            this.versions.delete(this.key(store,id));\n            this._cacheDelete(store,id);\n            if(typeof state!=="undefined"){\n              if(store==="meta"){if(state.meta)delete state.meta[id]}\n              else state[store]=(state[store]||[]).filter(x=>String(x.id)!==id);\n            }\n          }else{\n            const obj=row.payload||{};\n            this.versions.set(this.key(store,id),Number(row.version||1));\n            this._cachePut(store,obj);\n            if(typeof state!=="undefined"){\n              if(store==="meta"){\n                state.meta=state.meta||{};state.meta[id]=obj.value;\n              }else{\n                state[store]=state[store]||[];\n                const i=state[store].findIndex(x=>String(x.id)===id);\n                const normalized=store==="records"&&typeof normRecord==="function"?normRecord(obj):obj;\n                if(i>=0)state[store][i]=normalized;else state[store].push(normalized);\n              }\n            }\n          }\n          if(typeof renderNav==="function")renderNav();\n          if(typeof renderMain==="function")renderMain();\n          if(typeof updateCloudUI==="function")updateCloudUI();\n        }catch(e){console.warn("Evento Realtime no aplicado",e)}\n      })\n      .subscribe(status=>{\n        this.connected=status==="SUBSCRIBED"||this.connected;\n      });\n  }\n'
needle='  async all(store){'
assert needle in s
s=s.replace(needle, method+'\n'+needle, 1)
needle2='    window.addEventListener("online",()=>this.flushQueue().catch(()=>{}));\n'
assert needle2 in s
s=s.replace(needle2, needle2+'    this.subscribeRealtime();\n', 1)
p.write_text(s,encoding='utf-8')
assert 'postgres_changes' in s
assert 'subscribeRealtime()' in s
