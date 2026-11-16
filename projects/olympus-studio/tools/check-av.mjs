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
  const bounds = stream => {
    const packets = (probe.packets || []).filter(p => p.stream_index === stream.index);
    const spans = packets.map(p => {
      const t = Number(p.pts_time ?? p.dts_time);
      const d = Number(p.duration_time ?? 0);
      return { t, end: t + d };
    }).filter(p => Number.isFinite(p.t) && Number.isFinite(p.end) && p.t >= 0);
    if (spans.length) return { start: Math.min(...spans.map(p => p.t)), end: Math.max(...spans.map(p => p.end)) };
    if (stream.start_time == null || stream.duration == null) return null;
    const start = Number(stream.start_time), duration = Number(stream.duration);
    if (!Number.isFinite(start) || !Number.isFinite(duration) || start < 0 || duration <= 0) return null;
    return { start, end: start + duration };
  };
  const vb = bounds(video), ab = bounds(audio);
  if (!vb || !ab || vb.end <= vb.start || ab.end <= ab.start)
    throw Error('Horodatages/durées de flux invalides ou absents');
  const startDrift = Math.abs(vb.start - ab.start);
  const endDrift = Math.abs(vb.end - ab.end);
  if (startDrift > maxDrift || endDrift > maxDrift)
    throw Error('Décalage A/V excessif : début ' + startDrift.toFixed(3) + ' s, fin ' + endDrift.toFixed(3) + ' s');
  return { video: video.codec_name, audio: audio.codec_name, startDrift, endDrift, threshold: maxDrift };
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const file = process.argv[2];
  if (!file) { console.error('Usage: node tools/check-av.mjs <export.webm>'); process.exitCode = 2; }
  else {
    const run = spawnSync('ffprobe', ['-v','error','-show_streams','-show_packets','-show_format','-of','json',file], { encoding:'utf8', timeout:30000, maxBuffer:4*1024*1024 });
    try {
      if (run.error || run.status !== 0) throw Error(run.error?.message || run.stderr || 'ffprobe indisponible');
      console.log(JSON.stringify(assessStreams(JSON.parse(run.stdout)),null,2));
    } catch (error) { console.error('Export non validé : '+error.message); process.exitCode = 1; }
  }
}
