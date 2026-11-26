import test from 'node:test';
import assert from 'node:assert/strict';
import {workflow,validate,makeRealityHandler} from '../reality.mjs';
const input={checkpoint:'sd_turbo.safetensors',prompt:'liquid chrome',size:320,steps:4,denoise:.5,seed:42,image:'data:image/jpeg;base64,'+Buffer.from([255,216,255,224,0,1,255,217]).toString('base64')};
test('low VRAM workflow uses one image, fixed checkpoint and CFG 1',()=>{
 const w=workflow({...input,filename:'source.jpg'});
 assert.equal(w['1'].inputs.ckpt_name,input.checkpoint);
 assert.equal(w['5'].inputs.width,320);
 assert.equal(w['7'].inputs.cfg,1);
 assert.deepEqual(w['7'].inputs.latent_image,['6',0]);
 assert.equal(w['4'].inputs.image,'source.jpg');
});
test('validation rejects malformed or expensive settings',()=>{
 assert.equal(validate(input).length,8);
 for(const patch of [{size:1024},{steps:99},{steps:2,denoise:.25},{image:'data:image/png;base64,AAAA'},{prompt:'a'.repeat(1001)},{seed:-1}]){
  assert.throws(()=>validate({...input,...patch}));
 }
});
function call(handler,method,path,data){
 return new Promise((resolve,reject)=>{
  const res={writeHead(status){this.status=status},end(body){resolve({status:this.status,data:JSON.parse(body)})}};
  handler({method},res,new URL('http://localhost'+path),async()=>data).then(handled=>{if(!handled)resolve({handled:false})},reject);
 });
}
const id='12345678-1234-1234-1234-123456789abc';
test('ComfyUI adapter completes a mocked local job, rejects unknown models',async()=>{
 const calls=[];
 const fetcher=async(url,opts)=>{
  const p=new URL(url).pathname;calls.push(p);
  if(p.includes('object_info'))return Response.json({CheckpointLoaderSimple:{input:{required:{ckpt_name:[[input.checkpoint]]}}}});
  if(p==='/upload/image'){assert.ok(opts.body instanceof FormData);return Response.json({name:'source.jpg',subfolder:''});}
  if(p==='/prompt'){assert.equal(JSON.parse(opts.body).prompt['7'].inputs.seed,42);return Response.json({prompt_id:id});}
  if(p==='/history/'+id)return Response.json({[id]:{status:{completed:true},outputs:{'9':{images:[{filename:'output.png',type:'output'}]}}}});
  if(p==='/view')return new Response(new Uint8Array([137,80,78,71]),{headers:{'content-type':'image/png'}});
  throw Error('Unexpected '+url);
 };
 const handler=makeRealityHandler({fetcher,pause:async()=>{}});
 assert.deepEqual((await call(handler,'GET','/api/reality/models')).data.models,[input.checkpoint]);
 assert.equal((await call(handler,'POST','/api/reality/frame',{...input,checkpoint:'missing'})).status,400);
 const r=await call(handler,'POST','/api/reality/frame',input);
 assert.equal(r.status,200);assert.match(r.data.image,/^data:image\/png;base64,/);
 assert.equal(calls.filter(x=>x==='/prompt').length,1);
});
test('timeout prevents duplicate jobs until the prior job is found in history',async()=>{
 let jobs=0;
 const fetcher=async(url)=>{
  const p=new URL(url).pathname;
  if(p.includes('object_info'))return Response.json({CheckpointLoaderSimple:{input:{required:{ckpt_name:[[input.checkpoint]]}}}});
  if(p==='/upload/image')return Response.json({name:'source.jpg'});
  if(p==='/prompt'){jobs++;return Response.json({prompt_id:id});}
  if(p.startsWith('/history/'))return Response.json({});
  throw Error('unexpected');
 };
 const handler=makeRealityHandler({fetcher,maxPoll:1,pause:async()=>{}});
 assert.equal((await call(handler,'POST','/api/reality/frame',input)).status,504);
 assert.equal((await call(handler,'POST','/api/reality/frame',input)).status,409);
 assert.equal(jobs,1);
});
