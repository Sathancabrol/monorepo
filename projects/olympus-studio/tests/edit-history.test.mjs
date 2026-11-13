import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createEditHistory, snapshotEdit, recordEdit, undoEdit, redoEdit } from '../src/edit-history.js';
import { splitStoryboardAt, moveClip } from '../src/storyboard.js';
const original = { clips: [{id:'v',assetId:'source',kind:'video',inPoint:0,outPoint:4,title:'A'}], audioTrack: {assetId:'wav',volume:1,enabled:true} };
test('EDIT undo/redo preserves sources across split, reorder, title and audio', () => {
 let h=createEditHistory(), current=snapshotEdit(original.clips,original.audioTrack);
 const changes=[
  s=>({...s,clips:splitStoryboardAt(s.clips,2,'right')}),
  s=>({...s,clips:moveClip(s.clips,0,1)}),
  s=>({...s,clips:s.clips.map((c,i)=>i===0?{...c,title:'Nouveau'}:c)}),
  s=>({...s,audioTrack:{...s.audioTrack,volume:0.2}})
 ];
 for(const change of changes){const next=change(current);h=recordEdit(h,current,next);current=next;}
 const final=snapshotEdit(current.clips,current.audioTrack);
 for(let i=0;i<4;i++){const result=undoEdit(h,current);h=result.history;current=result.snapshot;}
 assert.deepEqual(current,original);
 for(let i=0;i<4;i++){const result=redoEdit(h,current);h=result.history;current=result.snapshot;}
 assert.deepEqual(current,final);
 assert.equal(current.clips[0].assetId,'source');
 assert.equal(current.clips[1].assetId,'source');
});
test('No-op does not record; new edit invalidates redo; history bounded and isolated',()=>{
 let h=createEditHistory(2),current=snapshotEdit(original.clips,original.audioTrack);
 assert.equal(recordEdit(h,current,current),h);
 for(let i=0;i<3;i++){const next={...current,clips:current.clips.map(c=>({...c,title:String(i)}))};h=recordEdit(h,current,next);current=next;}
 assert.equal(h.past.length,2);
 let u=undoEdit(h,current);h=u.history;current=u.snapshot;
 const next={...current,audioTrack:null};h=recordEdit(h,current,next);
 assert.equal(h.future.length,0);
 current.clips[0].title='mutated';
 assert.notEqual(h.past.at(-1).clips[0].title,'mutated');
 assert.throws(()=>createEditHistory(0),/Limite/);
});
