import {test} from 'node:test';
import assert from 'node:assert/strict';
import {selectComfyOutput,validComfyBytes,MAX_COMFY_BYTES} from '../src/comfy-output.js';
const id='12345678-1234-4234-8234-123456789abc';
const history=(item,completed=true)=>({[id]:{status:{completed,status_str:'success'},outputs:{'3':{images:[item]}}}});
test('ComfyUI only imports completed, enumerated output files',()=>{
 const item={filename:'render.png',subfolder:'renders/2026',type:'output'};
 assert.deepEqual(selectComfyOutput(history(item),id,0),{...item,mime:'image/png'});
 assert.throws(()=>selectComfyOutput(history(item,false),id,0),/non terminé/);
 assert.throws(()=>selectComfyOutput(history(item),id,1),/introuvable/);
 assert.throws(()=>selectComfyOutput(history(item),'../../etc',0),/invalide/);
});
test('No traversal, absolute paths, input files or unsupported formats',()=>{
 for(const item of [
  {filename:'../secret.png',subfolder:'',type:'output'},
  {filename:'secret.png',subfolder:'../private',type:'output'},
  {filename:'secret.png',subfolder:'/root',type:'output'},
  {filename:'secret.png',subfolder:'',type:'input'},
  {filename:'script.html',subfolder:'',type:'output'}
 ])assert.throws(()=>selectComfyOutput(history(item),id,0));
 assert.equal(selectComfyOutput(history({filename:'safe.webp'}),id,0).subfolder,'');
});
test('Media signature and byte limit reject spoofed and oversized output',()=>{
 assert.equal(validComfyBytes(Buffer.from([137,80,78,71,13,10,26,10,0]),'image/png'),true);
 assert.equal(validComfyBytes(Buffer.from('<html>malicious</html>'),'image/png'),false);
 assert.equal(validComfyBytes(Buffer.alloc(MAX_COMFY_BYTES+1),'image/png'),false);
 assert.equal(validComfyBytes(Buffer.from([26,69,223,163,0]),'video/webm'),true);
});
