// OLYMPUS Studio neutral interchange manifest v1.
// References are logical IDs, never filesystem paths or embedded source bytes.
import { clipDuration } from './storyboard.js';
import { validateEditAudioTrack } from './edit-audio.js';

export function toEditInterchange(clips, audioTrack = null) {
  if (!Array.isArray(clips)) throw new TypeError('Clips must be an array');
  let cursor = 0;
  const segments = clips.map(clip => {
    if (!clip || !['image', 'video'].includes(clip.kind) ||
        typeof clip.id !== 'string' || !clip.id.trim() ||
        typeof clip.assetId !== 'string' || !clip.assetId.trim()) {
      throw new Error('Invalid interchange clip');
    }
    const duration = clipDuration(clip);
    const sourceIn = clip.kind === 'video' ? Number(clip.inPoint ?? 0) : 0;
    if (!Number.isFinite(duration) || duration <= 0 ||
        !Number.isFinite(sourceIn) || sourceIn < 0 ||
        (clip.kind === 'video' && (!Number.isFinite(Number(clip.outPoint)) ||
         Math.abs(Number(clip.outPoint) - sourceIn - duration) > 0.001))) {
      throw new Error('Invalid interchange timing');
    }
    const segment = {
      clipId: clip.id, assetId: clip.assetId, kind: clip.kind,
      timelineStart: cursor, duration, sourceIn,
      title: String(clip.title ?? ''),
    };
    cursor += duration;
    return segment;
  });
  if (new Set(segments.map(s => s.clipId)).size !== segments.length) {
    throw new Error('Duplicate interchange clip IDs');
  }
  return {
    schema: 'olympus.edit.interchange.v1',
    timeUnit: 'seconds',
    duration: cursor,
    segments,
    soundtrack: audioTrack ? validateEditAudioTrack(audioTrack) : null,
  };
}
