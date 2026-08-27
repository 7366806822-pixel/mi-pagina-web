const app=document.querySelector('#app');

async function boot(){
  try{
    if(typeof DecompressionStream==='undefined'){
      throw new Error('Este navegador no admite la descompresión necesaria. Actualiza Chrome, Edge, Firefox o Safari.');
    }
    const files=['g1.txt','g2.txt','g3.txt','g4.txt','g5.txt'];
    const parts=await Promise.all(files.map(async f=>{
      const r=await fetch(`./gz/${f}`,{cache:'no-store'});
      if(!r.ok) throw new Error(`No se pudo cargar ${f} (${r.status})`);
      return (await r.text()).trim();
    }));
    const b64=parts.join('');
    const bin=atob(b64);
    const bytes=new Uint8Array(bin.length);
    for(let i=0;i<bin.length;i++) bytes[i]=bin.charCodeAt(i);
    const stream=new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'));
    const source=await new Response(stream).text();
    const moduleUrl=URL.createObjectURL(new Blob([source],{type:'text/javascript'}));
    try{ await import(moduleUrl); }
    finally{ setTimeout(()=>URL.revokeObjectURL(moduleUrl),1000); }
  }catch(err){
    console.error(err);
    app.innerHTML=`<div class="boot"><div class="alert danger"><b>No se pudo iniciar la plataforma.</b><br>${String(err.message||err)}</div></div>`;
  }
}

boot();
