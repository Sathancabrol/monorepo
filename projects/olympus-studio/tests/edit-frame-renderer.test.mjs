import test from 'node:test';
import assert from 'node:assert/strict';
import { renderEditPngFrames, seekVideoFrame } from '../src/edit-frame-renderer.js';

const clip = { id:'one', assetId:'asset', kind:'image', duration:0.5 };
function canvasMock({fail=false}={}) {
  const calls=[];
  return {
    width:320,height:180,calls,
    getContext(){return {clearRect(...args){calls.push(['clear',...args]);},drawImage(...args){calls.push(['draw',...args]);}};},
    toBlob(cb,type){calls.push(['blob',type]);cb(fail?null:new Blob(['png'],{type:'image/png'}));}
  };
}
test('PNG renderer emits fixed-rate ordered frames with source and PNG blobs', async () => {
  const canvas=canvasMock(), output=[];
  const result=await renderEditPngFrames([clip],{fps:4,canvas,resolveAsset:async id=>({id}),onFrame:async f=>output.push(f)});
  assert.deepEqual(result,{count:2,fps:4,duration:0.5});
  assert.deepEqual(output.map(f=>[f.filename,f.time,f.assetId]),[['000001.png',0,'asset'],['000002.png',0.25,'asset']]);
  assert.ok(output.every(f=>f.png.type==='image/png'));
  assert.equal(canvas.calls.filter(c=>c[0]==='draw').length,2);
});
test('PNG renderer rejects missing assets, invalid blobs and cancellation',async()=>{
  await assert.rejects(renderEditPngFrames([clip],{fps:4,canvas:canvasMock(),resolveAsset:async()=>null,onFrame:()=>{}}),/Missing media/);
  await assert.rejects(renderEditPngFrames([clip],{fps:4,canvas:canvasMock({fail:true}),resolveAsset:async()=>({}),onFrame:()=>{}}),/PNG encoding failed/);
  await assert.rejects(renderEditPngFrames([clip],{fps:4,canvas:canvasMock(),resolveAsset:async()=>({}),onFrame:()=>{},signal:{aborted:true}}),/aborted/);
  await assert.rejects(renderEditPngFrames([clip],{fps:0,canvas:canvasMock(),resolveAsset:async()=>({}),onFrame:()=>{}}),/fps/);
});
test('video frames seek to source time before drawing',async()=>{
  const calls=[];
  const clips=[{id:'v',assetId:'video',kind:'video',inPoint:1,outPoint:1.5}];
  await renderEditPngFrames(clips,{fps:4,canvas:canvasMock(),resolveAsset:async()=>({}),seek:async(_media,t)=>calls.push(t),onFrame:()=>{}});
  assert.deepEqual(calls,[1,1.25]);
});
test('seek rejects invalid timestamps',async()=>{
  await assert.rejects(seekVideoFrame({},-1),/Invalid video time/);
});
