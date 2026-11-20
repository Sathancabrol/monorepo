// Browser-side deterministic EDIT PNG adapter. No MediaRecorder or wall-clock timing.
// Caller supplies an asset resolver; output is a bounded ordered sequence of PNG Blobs.
import { planEditFrames } from './edit-frame-plan.js';

function waitForEvent(target, event, timeoutMs) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => { cleanup(); reject(new Error('Video seek timeout')); }, timeoutMs);
    const onReady = () => { cleanup(); resolve(); };
    const onError = () => { cleanup(); reject(new Error('Video seek failed')); };
    function cleanup() { clearTimeout(timer); target.removeEventListener(event, onReady); target.removeEventListener('error', onError); }
    target.addEventListener(event, onReady, { once: true });
    target.addEventListener('error', onError, { once: true });
  });
}

export async function seekVideoFrame(video, seconds, timeoutMs = 5000) {
  if (!Number.isFinite(seconds) || seconds < 0) throw new RangeError('Invalid video time');
  if (video.readyState >= 2 && Math.abs(video.currentTime - seconds) < 0.0005) return;
  const pending = waitForEvent(video, 'seeked', timeoutMs);
  video.currentTime = seconds;
  await pending;
  if (video.readyState < 2) throw new Error('Video frame not decoded');
}

export async function renderEditPngFrames(clips, {
  fps = 24, canvas, resolveAsset, onFrame, signal,
  maxFrames = 7200, maxSeconds = 120, seek = seekVideoFrame
} = {}) {
  if (!canvas || typeof canvas.getContext !== 'function' || typeof canvas.toBlob !== 'function')
    throw new TypeError('Canvas with PNG export required');
  if (typeof resolveAsset !== 'function' || typeof onFrame !== 'function')
    throw new TypeError('Asset resolver and frame sink required');
  const frames = planEditFrames(clips, fps, { maxFrames, maxSeconds });
  const ctx = canvas.getContext('2d');
  if (!ctx || !canvas.width || !canvas.height) throw new Error('Invalid Canvas');
  // Resolve every distinct source before writing the first frame. A missing source
  // must not leave an apparently valid, truncated PNG sequence in the sink.
  const sources = new Map();
  for (const frame of frames) {
    if (signal?.aborted) throw new Error('Frame export aborted');
    const key = JSON.stringify([frame.kind, frame.assetId]);
    if (sources.has(key)) continue;
    const media = await resolveAsset(frame.assetId, frame.kind);
    if (!media) throw new Error('Missing media: ' + frame.assetId);
    sources.set(key, media);
  }
  for (const frame of frames) {
    if (signal?.aborted) throw new Error('Frame export aborted');
    const media = sources.get(JSON.stringify([frame.kind, frame.assetId]));
    if (frame.kind === 'video') await seek(media, frame.sourceTime);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(media, 0, 0, canvas.width, canvas.height);
    // Match the EDIT preview title overlay in exported frames (not LIVE).
    const title = frame.title;
    if (typeof title === 'string' && title.length) {
      ctx.fillStyle = 'rgba(0,0,0,.65)';
      ctx.fillRect(20, canvas.height - 95, canvas.width - 40, 65);
      ctx.font = 'bold 38px Segoe UI,Arial';
      ctx.fillStyle = '#fff';
      ctx.fillText(title, 34, canvas.height - 55, canvas.width - 80);
    }
    const png = await new Promise((resolve, reject) => {
      canvas.toBlob(blob => blob?.type === 'image/png' && blob.size > 0
        ? resolve(blob) : reject(new Error('PNG encoding failed')), 'image/png');
    });
    await onFrame({ ...frame, png });
  }
  return { count: frames.length, fps, duration: frames.length / fps };
}
