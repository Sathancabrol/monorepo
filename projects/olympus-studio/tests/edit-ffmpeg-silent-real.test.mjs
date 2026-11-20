import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, readdirSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { editFfmpegPlan } from '../src/edit-ffmpeg-plan.js';

// Real FFmpeg smoke for the video-only fallback: do not claim an audio track.
function run(command, args, cwd) {
  const result = spawnSync(command, args, { cwd, encoding: 'utf8', timeout: 120000 });
  assert.equal(result.status, 0, result.stderr || result.error?.message || command);
  return result.stdout;
}

test('silent EDIT plan renders VP9-only WebM without altering source PNGs', { timeout: 180000 }, () => {
  const dir = mkdtempSync(join(tmpdir(), 'olympus-edit-silent-'));
  try {
    const frames = join(dir, 'frames');
    mkdirSync(frames);
    run('ffmpeg', ['-nostdin', '-v', 'error', '-f', 'lavfi', '-i',
      'color=c=blue:s=160x90:r=24:d=1', '-frames:v', '24', '-start_number', '1',
      join(frames, '%06d.png')], dir);
    const plan = editFfmpegPlan(null, 1);
    assert.equal(plan.audio, false);
    assert.equal(plan.prepare, null);
    assert.match(plan.warning, /sans son/);
    // The guide has only fixed placeholders and a known output filename.
    const args = plan.mux.replace('CHEMIN_DOSSIER_PNG', frames)
      .match(/"[^"]*"|[^\s]+/g).map(part => part.replace(/^"|"$/g, ''));
    assert.equal(args.shift(), 'ffmpeg');
    run('ffmpeg', args, dir);
    const streams = JSON.parse(run('ffprobe',
      ['-v', 'error', '-show_streams', '-of', 'json', join(dir, 'montage.webm')], dir)).streams;
    assert.equal(streams.length, 1);
    assert.equal(streams[0].codec_name, 'vp9');
    assert.equal(streams[0].codec_type, 'video');
    assert.equal(readdirSync(frames).length, 24);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});
