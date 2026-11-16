#!/usr/bin/env node
// Offline alpha export verifier. Requires a locally installed FFprobe (FFmpeg).
import { spawnSync } from 'node:child_process';
import { pathToFileURL } from 'node:url';

export function assessStreams(probe, maxDrift = 0.6) {
  if (!Number.isFinite(maxDrift) || maxDrift < 0) throw Error('Seuil de décalage invalide');
  const streams = probe?.streams || [];
  const videos = streams.filter(s => s.codec_type === 'video');
  const audios = streams.filter(s => s.codec_type === 'audio');
  if (videos.length !== 1 || audios.length !== 1) throw Error('Un flux vidéo et un flux audio exactement sont requis');
  const [video] = videos;
  const [audio] = audios;
  if (!['vp8', 'vp9', 'av1'].includes(video.codec_name)) throw Error('Codec vidéo WebM non reconnu : ' + video.codec_name);
  if (audio.codec_name !== 'opus') throw Error('Codec audio non Opus : ' + audio.codec_name);
  if (probe.format?.format_name && !probe.format.format_name.split(',').includes('matroska') &&
      !probe.format.format_name.split(',').includes('webm'))
    throw Error('Conteneur non WebM/Matroska');
  const start = s => Number(s.start_time);
  // Never substitute container duration for a missing stream duration: that
  // silently produces a false zero-drift result when one stream ends early.
  const duration = s => Number(s.duration);
  const values = [start(video), start(audio), duration(video), duration(audio)];
  if (values.some(n => !Number.isFinite(n) || n < 0) ||
      video.start_time == null || audio.start_time == null ||
      video.duration == null || audio.duration == null ||
      duration(video) === 0 || duration(audio) === 0)
    throw Error('Horodatages/durées de flux invalides ou absents');
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
