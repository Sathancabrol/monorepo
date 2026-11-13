/**
 * Shared same-tab camera lease.
 * Both "+ Webcam" and "Diffuser ma caméra" reuse a single MediaStream.
 * We only close the physical camera when the last consumer releases it.
 */
export function createCameraPool(getUserMedia = constraints => navigator.mediaDevices.getUserMedia(constraints)) {
  let source = null;
  let connecting = null;
  const owners = new Set();

  function isLive(stream) {
    return !!stream?.getVideoTracks?.().some(track => track.readyState === 'live');
  }

  async function start(preferRear) {
    // On Android, rear camera capture can fail with NotReadableError.
    // Try another camera once or twice, but never retry when permission was denied.
    const candidates = preferRear ? [
      { video: { facingMode: { ideal: 'environment' }, width: { ideal: 640 }, height: { ideal: 360 } }, audio: false },
      { video: { facingMode: { ideal: 'user' }, width: { ideal: 640 }, height: { ideal: 360 } }, audio: false },
      { video: true, audio: false },
    ] : [
      { video: { width: { ideal: 640 }, height: { ideal: 360 } }, audio: false },
      { video: true, audio: false },
    ];
    for (let i = 0; i < candidates.length; i++) {
      try { return await getUserMedia(candidates[i]); }
      catch (error) {
        if (i === candidates.length - 1 ||
            !['NotReadableError', 'NotFoundError', 'OverconstrainedError', 'AbortError'].includes(error?.name)) {
          throw error;
        }
      }
    }
    throw Error('Aucune caméra disponible');
  }

  async function acquire(owner, { preferRear = false } = {}) {
    if (typeof owner !== 'string' || !owner.trim()) throw Error('Caméra : propriétaire requis');
    if (!isLive(source)) {
      source = null;
      if (!connecting) {
        connecting = start(preferRear).then(stream => {
          source = stream;
          return stream;
        }).finally(() => { connecting = null; });
      }
      await connecting;
    }
    owners.add(owner);
    return source;
  }

  function release(owner) {
    owners.delete(owner);
    if (owners.size === 0 && source) {
      for (const track of source.getTracks()) track.stop();
      source = null;
    }
  }

  function isActive() { return isLive(source); }
  return { acquire, release, isActive };
}

const cameraPool = createCameraPool();
export const acquireCamera = cameraPool.acquire;
export const releaseCamera = cameraPool.release;
export const isCameraActive = cameraPool.isActive;
