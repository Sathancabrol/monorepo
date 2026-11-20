import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, readdirSync, rmSync, statSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { spawnSync } from 'node:child_process';
import { editFfmpegPlan } from '../src/edit-ffmpeg-plan.js';

// Execute the real EDIT guide commands against generated media, not copied CLI logic.
// This verifies FFmpeg on the CI host; it is not a Windows/OBS validation.
const root = resolve(import.meta.dirname, '..');
function run(bin, args, cwd) {
  const r = spawnSync(bin, args, { cwd, encoding: 'utf8', timeout: 120000 });
  assert.equal(r.status, 0, [bin, ...args, r.stderr, r.error?.message].join(' '));
  return r.stdout;
}
function argv(command) {
  return (command.match(/"[^"]*"|[^\s]+/g) ?? []).map(s =>
    s.startsWith('"') && s.endsWith('"') ? s.slice(1, -1) : s);
}
test('EDIT plan commands prepare WAV and mux PNG into VP9/Opus with measured sync', { timeout: 180000 }, () => {
  const dir = mkdtempSync(join(tmpdir(), 'olympus-edit-plan-'));
  try {
    const frames = join(dir, 'frames');
    mkdirSync(frames);
    run('ffmpeg', ['-nostdin','-v','error','-f','lavfi','-i','color=c=blue:s=160x90:r=24:d=1.5',
      '-frames:v','36','-start_number','1',join(frames,'%06d.png')], dir);
    const source = join(dir, 'source.wav');
    run('ffmpeg', ['-nostdin','-v','error','-f','lavfi','-i',
      'sine=frequency=440:sample_rate=48000:duration=2','-c:a','pcm_s16le',source], dir);
    const plan = editFfmpegPlan({assetId:'synthetic-audio',enabled:true,offset:0.5,inPoint:0.25,volume:0.6},1.5);
    assert.equal(plan.audio, true);
    const prepare = argv(plan.prepare.replace('CHEMIN_AUDIO_SOURCE', source)
      .replace('tools/prepare_edit_audio.py',join(root,'tools','prepare_edit_audio.py')));
    const mux = argv(plan.mux.replace('CHEMIN_DOSSIER_PNG', frames)
      .replace('tools/ffmpeg_mux_fallback.py',join(root,'tools','ffmpeg_mux_fallback.py')));
    run('python', prepare.slice(1), dir);
    assert.ok(statSync(join(dir,'audio_prepare.wav')).size > 1000);
    const output = run('python', mux.slice(1), dir);
    assert.match(output, /"end_delta_s"/);
    const report = JSON.parse(output.trim().split('\n').at(-1));
    assert.ok(Math.abs(report.end_delta_s) <= 0.2, JSON.stringify(report));
    const streams = JSON.parse(run('ffprobe',['-v','error','-show_streams','-of','json',join(dir,'montage.webm')],dir)).streams;
    assert.ok(streams.some(s => s.codec_name === 'vp9' && s.codec_type === 'video'));
    assert.ok(streams.some(s => s.codec_name === 'opus' && s.codec_type === 'audio'));
    assert.equal(readdirSync(frames).length,36);
    assert.ok(statSync(source).size > 1000);
  } finally {
    rmSync(dir,{recursive:true,force:true});
  }
});
