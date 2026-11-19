// Deterministic EDIT frame schedule for the local FFmpeg PNG sequence adapter.
// Pure planning only: no MediaRecorder, wall clock or browser-specific state.
import { storyboardDuration, locateClip } from './storyboard.js';

export function planEditFrames(clips, fps = 24, { maxSeconds = 120, maxFrames = 7200 } = {}) {
  if (!Number.isInteger(fps) || fps < 1 || fps > 60) throw new RangeError('fps must be an integer from 1 to 60');
  const duration = storyboardDuration(clips);
  if (!Number.isFinite(duration) || duration <= 0 || duration > maxSeconds) throw new RangeError('invalid storyboard duration');
  const count = Math.ceil(duration * fps);
  if (count > maxFrames) throw new RangeError('too many frames');
  return Array.from({ length: count }, (_, index) => {
    const time = index / fps;
    const located = locateClip(clips, Math.min(time, Math.max(0, duration - 0.000001)));
    if (!located) throw new Error('timeline gap at frame ' + index);
    return Object.freeze({
      filename: String(index + 1).padStart(6, '0') + '.png',
      index,
      time,
      assetId: located.clip.assetId,
      kind: located.clip.kind,
      sourceTime: located.sourceTime,
      title: located.clip.title || ''
    });
  });
}
