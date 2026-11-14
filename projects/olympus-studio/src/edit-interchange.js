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
  return validateEditInterchange({
    schema: 'olympus.edit.interchange.v1',
    timeUnit: 'seconds',
    duration: cursor,
    segments,
    soundtrack: audioTrack ? validateEditAudioTrack(audioTrack) : null,
  });
}

/**
 * Validate an untrusted interchange document before handing it to an adapter.
 * This is metadata only: never resolve asset IDs as filesystem paths.
 */
export function validateEditInterchange(manifest) {
  if (!manifest || typeof manifest !== 'object' || Array.isArray(manifest) ||
      manifest.schema !== 'olympus.edit.interchange.v1' ||
      manifest.timeUnit !== 'seconds' || !Array.isArray(manifest.segments) ||
      manifest.segments.length > 10000) {
    throw new Error('Invalid interchange schema');
  }
  const finite = value => typeof value === 'number' && Number.isFinite(value);
  let cursor = 0;
  const ids = new Set();
  const segments = manifest.segments.map(segment => {
    if (!segment || typeof segment !== 'object' || Array.isArray(segment) ||
        !['image', 'video'].includes(segment.kind) ||
        typeof segment.clipId !== 'string' || !segment.clipId.trim() || segment.clipId.length > 256 ||
        typeof segment.assetId !== 'string' || !segment.assetId.trim() || segment.assetId.length > 256 ||
        typeof segment.title !== 'string' || segment.title.length > 4096 ||
        !finite(segment.timelineStart) || !finite(segment.duration) ||
        !finite(segment.sourceIn) || segment.sourceIn < 0 || segment.sourceIn > 86400 ||
        (segment.kind === 'video' && !Number.isFinite(segment.sourceIn + segment.duration)) ||
        (segment.kind === 'image' && segment.sourceIn !== 0) ||
        segment.duration <= 0 || segment.duration > 36000 ||
        Math.abs(segment.timelineStart - cursor) > 0.001 ||
        ids.has(segment.clipId)) {
      throw new Error('Invalid interchange segment');
    }
    ids.add(segment.clipId);
    cursor += segment.duration;
    if (!Number.isFinite(cursor) || cursor > 86400) {
      throw new Error('Interchange duration exceeds limit');
    }
    return {
      clipId: segment.clipId, assetId: segment.assetId, kind: segment.kind,
      timelineStart: cursor - segment.duration, duration: segment.duration,
      sourceIn: segment.sourceIn, title: segment.title,
    };
  });
  if (!finite(manifest.duration) || Math.abs(manifest.duration - cursor) > 0.001) {
    throw new Error('Invalid interchange total duration');
  }
  return {
    schema: 'olympus.edit.interchange.v1',
    timeUnit: 'seconds',
    duration: cursor,
    segments,
    soundtrack: manifest.soundtrack == null ? null : validateEditAudioTrack(manifest.soundtrack),
  };
}


/**
 * Reconstruct editable storyboard metadata from a validated interchange manifest.
 * Media bytes remain in the local asset store; this function never opens paths.
 * The returned objects are detached from the untrusted input.
 */
export function fromEditInterchange(manifest) {
  const safe = validateEditInterchange(manifest);
  const clips = safe.segments.map(segment => ({
    id: segment.clipId,
    assetId: segment.assetId,
    kind: segment.kind,
    title: segment.title,
    duration: segment.duration,
    inPoint: segment.kind === 'video' ? segment.sourceIn : 0,
    outPoint: segment.kind === 'video' ? segment.sourceIn + segment.duration : 0,
  }));
  return {
    clips,
    audioTrack: safe.soundtrack,
  };
}
