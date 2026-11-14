import { test } from 'node:test';
import assert from 'node:assert/strict';
import { toEditInterchange, validateEditInterchange } from '../src/edit-interchange.js';

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

test('Interchange validation accepts a round trip and removes unknown properties', () => {
  const original = toEditInterchange([{id:'one',assetId:'asset',kind:'image',duration:2,title:'Hi'}]);
  const parsed = validateEditInterchange({...original, unexpected:'ignored'});
  assert.deepEqual(parsed,original);
  assert.equal(Object.hasOwn(parsed,'unexpected'),false);
});
test('Interchange validation rejects gaps, overlaps, duplicates and nonfinite numbers', () => {
  const original = toEditInterchange([
    {id:'one',assetId:'asset',kind:'image',duration:2},
    {id:'two',assetId:'asset',kind:'image',duration:3},
  ]);
  const changed = (field,value,index=1) => {
    const copy = structuredClone(original);
    copy.segments[index][field] = value;
    return copy;
  };
  assert.throws(()=>validateEditInterchange(changed('timelineStart',2.5)),/segment/);
  assert.throws(()=>validateEditInterchange(changed('timelineStart',1.5)),/segment/);
  assert.throws(()=>validateEditInterchange(changed('clipId','one')),/segment/);
  assert.throws(()=>validateEditInterchange(changed('duration',Infinity)),/segment/);
  assert.throws(()=>validateEditInterchange({...original,duration:6}),/total duration/);
  assert.throws(()=>validateEditInterchange({...original,schema:'unknown'}),/schema/);
});


test('Generated interchange enforces the same 24-hour bound as imported manifests', () => {
  // storyboard.clipDuration caps each individual clip at 10 hours.
  // Exercise the 24-hour manifest limit with multiple valid clips.
  const clips = [36000, 36000, 14401].map((duration, index) => ({
    id: 'part-' + index, assetId: 'still', kind: 'image', duration,
  }));
  assert.throws(() => toEditInterchange(clips), /limit/);
  const valid = toEditInterchange(clips.map((clip, index) =>
    index === 2 ? {...clip, duration: 14400} : clip));
  assert.deepEqual(validateEditInterchange(valid),valid);
});

test('Imported image segments cannot specify a video-only source offset', () => {
  const valid = toEditInterchange([{id:'still',assetId:'photo',kind:'image',duration:2}]);
  const invalid = structuredClone(valid);
  invalid.segments[0].sourceIn = 10;
  assert.throws(() => validateEditInterchange(invalid), /segment/);
});

test('Interchange rejects oversized untrusted identifiers and titles', () => {
  const valid = toEditInterchange([{id:'clip',assetId:'photo',kind:'image',duration:2,title:'ok'}]);
  for (const [field, value] of [
    ['clipId', 'c'.repeat(257)],
    ['assetId', 'a'.repeat(257)],
    ['title', 't'.repeat(4097)],
  ]) {
    const invalid = structuredClone(valid);
    invalid.segments[0][field] = value;
    assert.throws(() => validateEditInterchange(invalid), /segment/);
  }
  assert.throws(() => toEditInterchange([
    {id:'clip',assetId:'photo',kind:'image',duration:2,title:'t'.repeat(4097)},
  ]), /segment/);
  assert.deepEqual(validateEditInterchange(valid), valid);
});

test('Interchange normalizes sub-millisecond timeline rounding for downstream adapters', () => {
  const valid = toEditInterchange([
    {id:'a',assetId:'asset',kind:'image',duration:1.25},
    {id:'b',assetId:'asset',kind:'image',duration:2.5},
  ]);
  const rounded = structuredClone(valid);
  rounded.segments[1].timelineStart += 0.0005;
  const normalized = validateEditInterchange(rounded);
  assert.equal(normalized.segments[1].timelineStart, 1.25);
  assert.equal(rounded.segments[1].timelineStart, 1.2505);
  assert.deepEqual(normalized, valid);
  rounded.segments[1].timelineStart = 1.252;
  assert.throws(() => validateEditInterchange(rounded), /segment/);
});

test('Imported segments obey the same ten-hour per-clip bound as the storyboard', () => {
  const valid = toEditInterchange([{id:'still',assetId:'photo',kind:'image',duration:36000}]);
  assert.deepEqual(validateEditInterchange(valid), valid);
  const oversized = structuredClone(valid);
  oversized.segments[0].duration = 36001;
  oversized.duration = 36001;
  assert.throws(() => validateEditInterchange(oversized), /segment/);
  const video = toEditInterchange([{id:'video',assetId:'movie',kind:'video',inPoint:0,outPoint:36000}]);
  video.segments[0].duration = 36001;
  video.duration = 36001;
  assert.throws(() => validateEditInterchange(video), /segment/);
});
