import test from 'node:test';
import assert from 'node:assert/strict';
import { editFfmpegPlan } from '../src/edit-ffmpeg-plan.js';

// Regression coverage for the guide's two mutually exclusive export routes.
// This does not claim a Windows/OBS or browser media export.
test('audio guide keeps EDIT timing and volume in its preparation command', () => {
  const p = editFfmpegPlan({assetId:'local-wav', enabled:true, offset:1.25, inPoint:0.375, volume:0.6}, 3.125);
  assert.equal(p.audio, true);
  assert.match(p.prepare, /--offset 1\.250000(?:\s|$)/);
  assert.match(p.prepare, /--in-point 0\.375000(?:\s|$)/);
  assert.match(p.prepare, /--volume 0\.600000(?:\s|$)/);
  assert.match(p.prepare, /--duration 3\.125000(?:\s|$)/);
  assert.match(p.mux, /--audio "audio_prepare\.wav"/);
  assert.match(p.mux, /--av-report/);
  assert.doesNotMatch(p.mux, /-an "montage\.webm"/);
});
test('silent route cannot reference a prepared audio file and uses bounded video', () => {
  const p = editFfmpegPlan({assetId:'local-wav', enabled:false}, 3.125);
  assert.equal(p.audio, false);
  assert.equal(p.prepare, null);
  assert.doesNotMatch(p.mux, /audio_prepare|--audio|ffmpeg_mux_fallback/);
  assert.match(p.mux, /-t 3\.125000/);
  assert.match(p.mux, /-an "montage\.webm"$/);
});
test('audio guide rejects invalid source metadata and does not interpolate media names into shell commands', () => {
  assert.throws(() => editFfmpegPlan({assetId:' '}, 2));
  const p = editFfmpegPlan({assetId:'"; echo injected; #', name:'unsafe " name', offset:0}, 2);
  assert.doesNotMatch(p.prepare + p.mux, /echo injected|unsafe/);
  assert.match(p.prepare, /CHEMIN_AUDIO_SOURCE/);
});
