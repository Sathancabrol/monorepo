// OLYMPUS Studio — video metadata for non-destructive EDIT trims.
// Browser metadata is advisory until confirmed by the actual media element.
// No source media bytes are modified.
import { trimVideoClip } from './storyboard.js';

export function finiteVideoDuration(value) {
  const valueNumber = Number(value);
  return Number.isFinite(valueNumber) && valueNumber >= 0.1 ? valueNumber : null;
}

export function readVideoDuration(video, timeoutMs = 5000) {
  if (!video || typeof video.addEventListener !== 'function') {
    return Promise.reject(new Error('Source vidéo invalide'));
  }
  const immediate = finiteVideoDuration(video.duration);
  if (immediate !== null) return Promise.resolve(immediate);
  return new Promise((resolve, reject) => {
    let finished = false;
    let timer;
    const cleanup = () => {
      video.removeEventListener('loadedmetadata', check);
      video.removeEventListener('durationchange', check);
      video.removeEventListener('error', onError);
      clearTimeout(timer);
    };
    const done = (value, error) => {
      if (finished) return;
      finished = true;
      cleanup();
      if (error) reject(error);
      else resolve(value);
    };
    const check = () => {
      const duration = finiteVideoDuration(video.duration);
      if (duration !== null) done(duration);
    };
    const onError = () => done(null, new Error('Impossible de lire les métadonnées vidéo'));
    video.addEventListener('loadedmetadata', check);
    video.addEventListener('durationchange', check);
    video.addEventListener('error', onError);
    timer = setTimeout(() => done(null, new Error('Durée vidéo inconnue : métadonnées non disponibles')), timeoutMs);
    // A metadata event can arrive between initial inspection and listener registration.
    check();
  });
}

export function initialClipDuration(knownSourceDuration, preferredSeconds = 5) {
  const duration = finiteVideoDuration(knownSourceDuration);
  if (duration === null) return preferredSeconds;
  return Math.min(preferredSeconds, duration);
}

export function trimWithinVideoDuration(clip, start, end, knownSourceDuration) {
  const updated = trimVideoClip(clip, start, end);
  const source = finiteVideoDuration(knownSourceDuration);
  if (source !== null && updated.outPoint > source + 0.001) {
    throw new Error('OUT (' + updated.outPoint.toFixed(2) + ' s) dépasse la durée source (' + source.toFixed(2) + ' s)');
  }
  return updated;
}

export function setClipDuration(clip, seconds, knownSourceDuration) {
  const duration = Number(seconds);
  if (!Number.isFinite(duration) || duration < 0.1 || duration > 3600) {
    throw new Error('Durée invalide (0,1 à 3600 s)');
  }
  if (clip?.kind === 'video') {
    const start = Number(clip.inPoint) || 0;
    return trimWithinVideoDuration(clip, start, start + duration, knownSourceDuration);
  }
  if (clip?.kind === 'image') return { ...clip, duration };
  throw new Error('Type de clip non pris en charge');
}
