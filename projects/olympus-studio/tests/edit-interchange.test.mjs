import { test } from 'node:test';
import assert from 'node:assert/strict';
import { toEditInterchange } from '../src/edit-interchange.js';

test('Interchange preserves shared source, split positions and independent audio', () => {
  const clips = [
    { id:'left', assetId:'video', kind:'video', inPoint:2, outPoint:3, title:'A' },
    { id:'right', assetId:'video', kind:'video', inPoint:3, outPoint:5, title:'B' },
    { id:'still', assetId:'photo', kind:'image', duration:1.5 },
  ];
  const audio = { assetId:'sound', offset:0.5, inPoint:1, volume:0.4, enabled:true };
  const original = JSON.stringify({ clips, audio });
  const manifest = toEditInterchange(clips,audio);
  assert.equal(manifest.schema,'olympus.edit.interchange.v1');
  assert.equal(manifest.duration,4.5);
  assert.deepEqual(manifest.segments.map(s=>s.timelineStart),[0,1,3]);
  assert.deepEqual(manifest.segments.map(s=>s.assetId),['video','video','photo']);
  assert.deepEqual(manifest.segments.map(s=>s.sourceIn),[2,3,0]);
  assert.equal(manifest.soundtrack.offset,0.5);
  assert.equal(JSON.stringify({ clips, audio }),original);
  assert.equal(JSON.parse(JSON.stringify(manifest)).segments[1].title,'B');
});
test('Interchange rejects invalid timing and duplicate IDs', () => {
  assert.throws(()=>toEditInterchange(null),/array/);
  assert.throws(()=>toEditInterchange([{id:'x',assetId:'v',kind:'video',inPoint:2,outPoint:1}]),/timing/);
  assert.throws(()=>toEditInterchange([{id:'x',assetId:'v',kind:'video',inPoint:2,outPoint:4},{id:'x',assetId:'w',kind:'image',duration:1}]),/Duplicate/);
  assert.throws(()=>toEditInterchange([{id:'x',assetId:'',kind:'image',duration:1}]),/clip/);
});
