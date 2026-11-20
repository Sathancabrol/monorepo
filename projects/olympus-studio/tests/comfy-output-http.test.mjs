// Integration test: real Studio HTTP proxy against a synthetic loopback ComfyUI server.
// No cloud, real ComfyUI installation, Windows or GPU required.
import {test} from 'node:test';
import assert from 'node:assert/strict';
import http from 'node:http';
import net from 'node:net';
import {spawn} from 'node:child_process';
import {once} from 'node:events';
import {setTimeout as delay} from 'node:timers/promises';

const id='12345678-1234-4234-8234-123456789abc';
const png=Buffer.from('89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4890000000b49444154789c636000020000050001a5f645400000000049454e44ae426082','hex');
const history={ [id]: {status:{completed:true,status_str:'success'},outputs:{'3':{images:[{filename:'fixture.png',subfolder:'renders',type:'output'}]}}} };
const listen=(server,port)=>new Promise((resolve,reject)=>{server.once('error',reject);server.listen(port,'127.0.0.1',resolve)});
const close=server=>new Promise(resolve=>server.close(resolve));
async function freePort(){const s=net.createServer();await listen(s,0);const port=s.address().port;await close(s);return port;}
test('ComfyUI completed output traverses the real HTTP gateway with verified bytes', {timeout:30000}, async t=>{
 const mock=http.createServer((req,res)=>{
  const u=new URL(req.url,'http://127.0.0.1');
  if(u.pathname==='/history/'+id){res.setHeader('Content-Type','application/json');return res.end(JSON.stringify(history));}
  if(u.pathname==='/view'){
   assert.equal(u.searchParams.get('filename'),'fixture.png');
   assert.equal(u.searchParams.get('subfolder'),'renders');
   assert.equal(u.searchParams.get('type'),'output');
   res.setHeader('Content-Type','image/png');return res.end(png);
  }
  res.writeHead(404);res.end();
 });
 try{await listen(mock,8188);}catch(e){if(e.code==='EADDRINUSE'){t.skip('Port ComfyUI 8188 occupied; do not interfere with existing service');return;}throw e;}
 const port=await freePort();
 const child=spawn(process.execPath,['server.mjs'],{cwd:new URL('..',import.meta.url),env:{...process.env,OLYMPUS_PORT:String(port)},stdio:'ignore'});
 try{
  let ready=false;
  for(let i=0;i<70;i++){if(child.exitCode!==null)throw Error('Studio exited');try{const r=await fetch('http://127.0.0.1:'+port+'/api/health');if(r.ok){ready=true;break;}}catch{}await delay(100);}
  assert.ok(ready,'Studio HTTP server did not start');
  const base='http://127.0.0.1:'+port+'/api/comfy/output?prompt_id='+id+'&index=';
  const response=await fetch(base+'0');
  assert.equal(response.status,200);
  assert.equal(response.headers.get('content-type'),'image/png');
  assert.deepEqual(Buffer.from(await response.arrayBuffer()),png);
  const missing=await fetch(base+'1');
  assert.equal(missing.status,502,'Out-of-range output must not be served');
  const invalid=await fetch(base+'../../etc');
  assert.equal(invalid.status,400,'Invalid index must be rejected before upstream fetch');
 }finally{child.kill();await close(mock);}
});
