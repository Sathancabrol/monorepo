import { test } from 'node:test';
import assert from 'node:assert/strict';
import { planEditFrames } from '../src/edit-frame-plan.js';

test('fixed-rate frames preserve trim and clip boundary without wall-clock time', () => {
  const clips = [
    {id:'still',assetId:'image-1',kind:'image',duration:1},
    {id:'movie',assetId:'video-1',kind:'video',inPoint:4,outPoint:5,title:'Cut'}
  ];
  const frames = planEditFrames(clips,4);
  assert.equal(frames.length,8);
  assert.equal(frames[0].filename,'000001.png');
  assert.equal(frames[3].assetId,'image-1');
  assert.equal(frames[4].assetId,'video-1');
  assert.equal(frames[4].sourceTime,4);
  assert.equal(frames[7].sourceTime,4.75);
  assert.equal(frames[7].time,1.75);
  assert.equal(frames[7].filename,'000008.png');
  assert.deepEqual(planEditFrames(clips,4),frames);
  assert.ok(Object.isFrozen(frames[0]));
});

test('rejects unsafe fps, duration and excessive frame count', () => {
  const clips=[{id:'a',assetId:'a',kind:'image',duration:2}];
  for(const fps of [0,61,1.5,NaN]) assert.throws(()=>planEditFrames(clips,fps),RangeError);
  assert.throws(()=>planEditFrames([],24),RangeError);
  assert.throws(()=>planEditFrames(clips,24,{maxFrames:10}),RangeError);
  assert.throws(()=>planEditFrames(clips,24,{maxSeconds:1}),RangeError);
});
