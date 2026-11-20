import test from 'node:test';
import assert from 'node:assert/strict';
import { editFfmpegPlan } from '../src/edit-ffmpeg-plan.js';

test('EDIT track parameters become explicit local FFmpeg commands', () => {
  const p=editFfmpegPlan({assetId:'audio-1',offset:.75,inPoint:.125,volume:.4,enabled:true},2.5);
  assert.equal(p.audio,true);
  assert.match(p.prepare,/--offset 0\.750000 --in-point 0\.125000 --volume 0\.400000 --duration 2\.500000/);
  assert.match(p.mux,/--audio "audio_prepare.wav"/);
  assert.match(p.prepare,/CHEMIN_AUDIO_SOURCE/);
});
test('disabled or absent audio never passes an audio argument', () => {
  for(const t of [null,{assetId:'a',enabled:false}]) {
    const p=editFfmpegPlan(t,2);
    assert.equal(p.prepare,null);
    assert.doesNotMatch(p.mux,/--audio/);
    assert.match(p.mux,/^ffmpeg -nostdin /);
    assert.match(p.mux,/-an "montage.webm"$/);
    assert.match(p.mux,/-i "CHEMIN_DOSSIER_PNG\/%06d.png"/);
    assert.doesNotMatch(p.mux,/ffmpeg_mux_fallback.py/);
  }
});
test('invalid EDIT duration and unsafe numeric audio parameters fail closed', () => {
  for(const duration of [0,NaN,Infinity,121]) assert.throws(()=>editFfmpegPlan(null,duration));
  assert.throws(()=>editFfmpegPlan({assetId:'a',offset:Infinity},2));
  assert.throws(()=>editFfmpegPlan({assetId:'a',volume:2},2));
});

test('silent export respects a fractional EDIT duration rather than exporting all PNGs', () => {
  const plan = editFfmpegPlan(null, 1.375);
  assert.match(plan.mux, /-t 1\.375000 -c:v/);
  assert.doesNotMatch(plan.mux, /--audio/);
});
