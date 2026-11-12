import http from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { join, resolve, extname, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import net from 'node:net';

const ROOT = resolve(fileURLToPath(new URL('.', import.meta.url)));
const HOST = '127.0.0.1'; // No LAN or cloud exposure by default.
const PORT = Number(process.env.OLYMPUS_PORT || 8787);
const types = {'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json; charset=utf-8','.svg':'image/svg+xml','.png':'image/png','.ico':'image/x-icon'};
// Serve only the Studio UI files. Never expose .env, source maps, tests or server code.
const STATIC_FILES = new Set(['/index.html','/src/style.css','/src/app.js','/src/obs-panel.css','/src/obs-panel.js','/src/obs-client.js']);
const ORIGINS = new Set(['http://127.0.0.1:'+PORT,'http://localhost:'+PORT]);

function json(res,status,data){res.writeHead(status,{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store','X-Content-Type-Options':'nosniff'});res.end(JSON.stringify(data));}
function tcpCheck(port){return new Promise(done=>{const sock=net.createConnection({host:HOST,port});let settled=false;function finish(ok){if(!settled){settled=true;sock.destroy();done(ok);}}sock.setTimeout(800);sock.once('connect',()=>finish(true));sock.once('timeout',()=>finish(false));sock.once('error',()=>finish(false));});}
async function comfyCheck(){try{const r=await fetch('http://127.0.0.1:8188/system_stats',{signal:AbortSignal.timeout(1300)});return r.ok;}catch{return false;}}
async function bodyJson(req){let body='';for await(const chunk of req){body+=chunk;if(body.length>1024*1024)throw new Error('Payload > 1 MiB');}return JSON.parse(body);}

let lastJpeg=null;
const viewers=new Set();
function sendFrame(res,bytes){
 try{
  if(res.destroyed){viewers.delete(res);return;}
  res.write('--frame\r\nContent-Type: image/jpeg\r\nContent-Length: '+bytes.length+'\r\n\r\n');
  res.write(bytes);res.write('\r\n');
 }catch{viewers.delete(res);}
}
async function readImage(req){
 const chunks=[];let length=0;
 for await(const chunk of req){length+=chunk.length;if(length>2*1024*1024)throw Error('Image trop volumineuse');chunks.push(chunk);}
 return Buffer.concat(chunks);
}

async function handle(req,res){
 const url=new URL(req.url,'http://127.0.0.1');
 // Reject cross-origin writes and rebinding attempts before privileged local actions.
 if (!['127.0.0.1:'+PORT,'localhost:'+PORT].includes(req.headers.host)) return json(res,403,{error:'Hôte interdit'});
 if (req.method === 'POST' && req.headers.origin && !ORIGINS.has(req.headers.origin)) return json(res,403,{error:'Origine interdite'});

 if(req.method==='GET'&&url.pathname==='/obs'){
  res.writeHead(200,{'Content-Type':'multipart/x-mixed-replace; boundary=frame','Cache-Control':'no-cache, no-store','Connection':'keep-alive','X-Content-Type-Options':'nosniff'});
  viewers.add(res);req.once('close',()=>viewers.delete(res));
  if(lastJpeg)sendFrame(res,lastJpeg);
  return;
 }
 if(req.method==='POST'&&url.pathname==='/api/frame'){
  if(!String(req.headers['content-type']||'').startsWith('image/jpeg'))return json(res,415,{error:'JPEG attendu'});
  try{const bytes=await readImage(req);if(bytes.length<8||bytes[0]!==255||bytes[1]!==216)return json(res,400,{error:'JPEG invalide'});
  lastJpeg=bytes;for(const viewer of viewers)sendFrame(viewer,bytes);return json(res,200,{received:bytes.length,viewers:viewers.size});}
  catch(e){return json(res,413,{error:String(e.message)});}
 }

 if(req.method==='GET'&&url.pathname==='/api/health'){const [obs,comfy]=await Promise.all([tcpCheck(4455),comfyCheck()]);return json(res,200,{ok:true,local:true,services:{obs:{port:4455,reachable:obs,controlled:false},comfyui:{port:8188,reachable:comfy}},note:'Disponibilité réseau ≠ moteur configuré ou vérifié'});}
 if(req.method==='POST'&&url.pathname==='/api/comfy/queue'){
   let data;try{data=await bodyJson(req);}catch(e){return json(res,400,{error:'JSON invalide ou trop volumineux'});}
   const prompt=data?.prompt; if(!prompt||typeof prompt!=='object'||Array.isArray(prompt)||Object.keys(prompt).length===0){return json(res,400,{error:'Attendu : {prompt: workflow_API_JSON}'});}
   try{const response=await fetch('http://127.0.0.1:8188/prompt',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({prompt,client_id:'olympus-studio'}),signal:AbortSignal.timeout(5000)});const out=await response.text();try{return json(res,response.status,JSON.parse(out));}catch{return json(res,502,{error:'Réponse ComfyUI invalide',detail:out.slice(0,500)});}}
   catch(e){return json(res,502,{error:'ComfyUI local inaccessible',detail:String(e.message).slice(0,180)});}
 }
 if(req.method==='GET'&&url.pathname==='/api/comfy/job'){
  const id=url.searchParams.get('prompt_id')||'';
  if(!/^[a-f0-9-]{36}$/i.test(id))return json(res,400,{error:'prompt_id UUID invalide'});
  try{
   const upstream=await fetch('http://127.0.0.1:8188/history/'+encodeURIComponent(id),{signal:AbortSignal.timeout(5000)});
   if(!upstream.ok)return json(res,502,{error:'Historique ComfyUI inaccessible',code:upstream.status});
   const history=await upstream.json(),job=history?.[id];
   if(!job)return json(res,200,{prompt_id:id,status:'queued_or_running',outputs:[]});
   const info=job.status||{};
   const outputs=[];
   for(const value of Object.values(job.outputs||{})){
    for(const kind of ['images','videos','gifs','audio']){
     if(!Array.isArray(value?.[kind]))continue;
     for(const item of value[kind]){
      if(!item||typeof item.filename!=='string')continue;
      outputs.push({kind,filename:item.filename,subfolder:String(item.subfolder||''),type:String(item.type||'output')});
     }
    }
   }
   const status=info.status_str==='error'?'failed':info.completed===true?'completed':'known';
   return json(res,200,{prompt_id:id,status,outputs:outputs.slice(0,250)});
  }catch(e){return json(res,502,{error:'Suivi ComfyUI indisponible',detail:String(e.message).slice(0,140)});}
 }
 if(req.method!=='GET'&&req.method!=='HEAD')return json(res,405,{error:'Méthode interdite'});
 const pathname=url.pathname==='/'?'/index.html':decodeURIComponent(url.pathname);
 const full=resolve(ROOT,'.'+pathname);
 if(full!==ROOT && !full.startsWith(ROOT+sep))return json(res,403,{error:'Accès refusé'});
 if(!STATIC_FILES.has(pathname))return json(res,403,{error:'Ressource privée'});
 try{const s=await stat(full);if(!s.isFile())return json(res,404,{error:'Introuvable'});const bytes=await readFile(full);res.writeHead(200,{'Content-Type':types[extname(full)]||'application/octet-stream','X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer','Cache-Control':'no-store'});res.end(req.method==='HEAD'?undefined:bytes);}
 catch{return json(res,404,{error:'Introuvable'});}
}
const server=http.createServer((req,res)=>{handle(req,res).catch(e=>json(res,500,{error:'Erreur serveur',detail:String(e.message)}));});
server.listen(PORT,HOST,()=>console.log('OLYMPUS Studio : http://'+HOST+':'+PORT+' (local uniquement)'));
