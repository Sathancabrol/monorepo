import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { setTimeout as sleep } from 'node:timers/promises';

const port=18000+Math.floor(Math.random()*6000),base='http://127.0.0.1:'+port;
let child;
before(async()=>{
 child=spawn(process.execPath,['server.mjs'],{cwd:new URL('..',import.meta.url),env:{...process.env,OLYMPUS_PORT:String(port)},stdio:'ignore'});
 let ok=false;
 for(let i=0;i<40;i++){try{const r=await fetch(base+'/');if(r.ok){ok=true;break;}}catch{}await sleep(75);}
 assert.equal(ok,true,'Le serveur HTTP doit démarrer');
});
after(()=>{if(child&&!child.killed)child.kill();});
test('Interface servie',async()=>{
 const r=await fetch(base+'/');assert.equal(r.status,200);const html=await r.text();assert.match(html,/OLYMPUS/);assert.match(html,/src\/app.js/);
});
test('Ressources locales disponibles',async()=>{
 const r=await fetch(base+'/src/app.js');assert.equal(r.status,200);assert.match(await r.text(),/function record/);
});
test('Fichier privé inaccessible',async()=>{
 const r=await fetch(base+'/.gitignore');assert.equal(r.status,403);
});
test('Diagnostic OBS/ComfyUI en lecture seule',async()=>{
 const r=await fetch(base+'/api/health');assert.equal(r.status,200);const j=await r.json();assert.equal(j.local,true);assert.ok(j.services?.obs);assert.ok(j.services?.comfyui);
});
test('Trame vidéo invalide rejetée',async()=>{const r=await fetch(base+'/api/frame',{method:'POST',headers:{'Content-Type':'image/jpeg'},body:'pas une image'});assert.equal(r.status,400);});
test('Workflow ComfyUI malformé rejeté, sans requête externe',async()=>{
 const r=await fetch(base+'/api/comfy/queue',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({prompt:{}})});assert.equal(r.status,400);
});

test('Le dossier source privé et les secrets ne sont pas exposés',async()=>{
 for(const name of ['/server.mjs','/package.json','/tests/obs-client.test.mjs','/.env','/docs/CONTRACTS.md']){
   const r=await fetch(base+name);assert.equal(r.status,403,name);
 }
});
test('Le connecteur OBS est servi comme module local',async()=>{
 const r=await fetch(base+'/src/obs-client.js');assert.equal(r.status,200);
 assert.match(await r.text(),/class OBSClient/);
});
test('Les origines distantes ne peuvent pas poster vers les moteurs locaux',async()=>{
 const r=await fetch(base+'/api/comfy/queue',{method:'POST',headers:{Origin:'https://attacker.invalid','Content-Type':'application/json'},body:JSON.stringify({prompt:{'1':{class_type:'Test',inputs:{}}}})});
 assert.equal(r.status,403);
});

test('ID de job ComfyUI invalide rejeté sans requête externe',async()=>{
 const r=await fetch(base+'/api/comfy/job?prompt_id=../../secret');assert.equal(r.status,400);
 const j=await r.json();assert.match(j.error,/UUID/);
});

test('Bibliothèque IndexedDB servie comme module et non comme fichier privé',async()=>{
 const r=await fetch(base+'/src/media-store.js');assert.equal(r.status,200);
 const code=await r.text();assert.match(code,/export function openMediaDB/);
});

test('Le module audio EDIT est servi localement mais le serveur reste fermé aux fichiers privés',async()=>{
 const r=await fetch(base+'/src/edit-audio.js');
 assert.equal(r.status,200);
 assert.match(await r.text(),/function validateEditAudioTrack/);
 const protectedFile=await fetch(base+'/docs/AUTONOMOUS_BACKLOG.md');
 assert.equal(protectedFile.status,403);
});

test('Contrats des 12 espaces : inventaire local sans faux positifs de disponibilité',async()=>{
 const r=await fetch(base+'/api/integrations');assert.equal(r.status,200);
 const j=await r.json();assert.equal(j.local,true);assert.equal(j.spaces.length,12);
 assert.equal(new Set(j.spaces.map(s=>s.space)).size,12);
 for(const s of j.spaces){
  assert.ok(s.engine&&s.transport&&s.contract&&s.status);
  assert.equal(s.operationallyVerified,false);
  assert.ok(s.reachable===null||typeof s.reachable==='boolean');
 }
 assert.equal(j.spaces.find(s=>s.space==='EDIT').status,'intermittent-av');
 assert.equal(j.spaces.find(s=>s.space==='XR').status,'not-integrated');
});

test('ComfyUI output rejects arbitrary job identifiers and indexes before upstream',async()=>{
 for(const query of ['prompt_id=../../secret&index=0','prompt_id=12345678-1234-4234-8234-123456789abc&index=../../etc','prompt_id=12345678-1234-4234-8234-123456789abc&index=-1']){
  const r=await fetch(base+'/api/comfy/output?'+query);assert.equal(r.status,400);
 }
});

test('XR event bus is served from allowlist with no remote exposure',async()=>{
 const r=await fetch(base+'/src/studio-event-bus.js');
 assert.equal(r.status,200);
 assert.match(await r.text(),/validateStudioEvent/);
 const privateTest=await fetch(base+'/tests/studio-event-bus.test.mjs');
 assert.equal(privateTest.status,403);
});


test('Every relative ES module imported by app.js is served over HTTP',async()=>{
 const response=await fetch(base+'/src/app.js');
 assert.equal(response.status,200);
 const source=await response.text();
 const imports=[...source.matchAll(/from ['"]\\.\\/([^'"]+)['"]/g)].map(match=>match[1]);
 assert.ok(imports.includes('edit-frame-renderer.js'));
 assert.ok(imports.includes('png-directory-sink.js'));
 for(const file of imports){
  const resource=await fetch(base+'/src/'+file);
  assert.equal(resource.status,200,'Missing HTTP module: '+file);
  assert.match(resource.headers.get('content-type')||'',/javascript/);
 }
 const privateResponse=await fetch(base+'/src/not-in-allowlist.js');
 assert.equal(privateResponse.status,403);
});
