#!/usr/bin/env node
// Offline alpha export verifier. Requires a locally installed FFprobe (FFmpeg).
import { spawnSync } from 'node:child_process';
import { pathToFileURL } from 'node:url';

export function assessStreams(probe, maxDrift = 0.6) {
  const streams = probe?.streams || [];
  const video = streams.find(s => s.codec_type === 'video');
  const audio = streams.find(s => s.codec_type === 'audio');
  if (!video || !audio) throw Error('Flux vidéo ou audio absent');
  if (audio.codec_name !== 'opus') throw Error('Codec audio non Opus : ' + audio.codec_name);
  const start = s => Number(s.start_time ?? 0);
  const duration = s => Number(s.duration ?? probe.format?.duration);
  const values = [start(video), start(audio), duration(video), duration(audio)];
  if (values.some(n => !Number.isFinite(n) || n < 0)) throw Error('Horodatages/durées invalides');
  const startDrift = Math.abs(start(video) - start(audio));
  const endDrift = Math.abs(start(video) + duration(video) - start(audio) - duration(audio));
  if (startDrift > maxDrift || endDrift > maxDrift)
    throw Error('Décalage A/V excessif : début ' + startDrift.toFixed(3) + ' s, fin ' + endDrift.toFixed(3) + ' s');
  return { video: video.codec_name, audio: audio.codec_name, startDrift, endDrift, threshold: maxDrift };
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const file = process.argv[2];
  if (!file) { console.error('Usage: node tools/check-av.mjs <export.webm>'); process.exitCode = 2; }
  else {
    const run = spawnSync('ffprobe', ['-v','error','-show_streams','-show_format','-of','json',file], { encoding:'utf8', timeout:30000, maxBuffer:4*1024*1024 });
    try {
      if (run.error || run.status !== 0) throw Error(run.error?.message || run.stderr || 'ffprobe indisponible');
      console.log(JSON.stringify(assessStreams(JSON.parse(run.stdout)),null,2));
    } catch (error) { console.error('Export non validé : '+error.message); process.exitCode = 1; }
  }
}
