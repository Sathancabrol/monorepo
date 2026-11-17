import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

function run(command, args) {
  const result = spawnSync(command, args, { encoding: 'utf8', timeout: 120000, maxBuffer: 16 * 1024 * 1024 });
  assert.equal(result.status, 0, `${command}: ${result.error?.message || result.stderr?.slice(-1200)}`);
  return result.stdout;
}
function available(command) {
  const result = spawnSync(command, ['-version'], { encoding: 'utf8', timeout: 10000 });
  return result.status === 0;
}
function ends(path) {
  const json = JSON.parse(run('ffprobe', ['-v','error','-show_streams','-show_packets','-of','json',path]));
  const streams = json.streams.filter(s => ['audio','video'].includes(s.codec_type));
  assert.equal(streams.length, 2);
  const result = {};
  for (const stream of streams) {
    const packets = json.packets.filter(p => p.stream_index === stream.index);
    assert.ok(packets.length > 0, `missing ${stream.codec_type} packets`);
    result[stream.codec_type] = Math.max(...packets.map(p => Number(p.pts_time) + Number(p.duration_time || 0)));
  }
  return result;
}

test('repair-av-tail repairs a real short-video/long-audio WebM without touching source', {
  skip: !available('ffmpeg') || !available('ffprobe') ? 'FFmpeg/FFprobe unavailable' : false,
  timeout: 180000,
}, () => {
  const dir = mkdtempSync(join(tmpdir(), 'olympus-av-repair-'));
  try {
    const video = join(dir, 'video.webm');
    const audio = join(dir, 'audio.webm');
    const input = join(dir, 'input.webm');
    const output = join(dir, 'output.webm');
    run('ffmpeg', ['-hide_banner','-loglevel','error','-f','lavfi','-i','testsrc2=size=160x90:rate=24:duration=1','-c:v','libvpx','-an',video]);
    run('ffmpeg', ['-hide_banner','-loglevel','error','-f','lavfi','-i','sine=frequency=440:duration=2','-c:a','libopus','-vn',audio]);
    run('ffmpeg', ['-hide_banner','-loglevel','error','-i',video,'-i',audio,'-map','0:v:0','-map','1:a:0','-c','copy',input]);
    const before = ends(input);
    assert.ok(before.audio - before.video > 0.7, JSON.stringify(before));
    const repaired = spawnSync(process.execPath, ['tools/repair-av-tail.mjs',input,output], {
      encoding: 'utf8', timeout: 120000, cwd: new URL('..', import.meta.url).pathname
    });
    assert.equal(repaired.status, 0, repaired.stderr);
    const after = ends(output);
    assert.ok(Math.abs(after.audio - after.video) < 0.20, JSON.stringify({before,after}));
    assert.ok(after.audio > 1.8 && after.video > 1.8);
    // Source remains byte-identical in timing; output is distinct.
    assert.deepEqual(ends(input), before);
  } finally {
    rmSync(dir, {recursive:true, force:true});
  }
});
