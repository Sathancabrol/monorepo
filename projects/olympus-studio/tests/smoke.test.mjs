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
