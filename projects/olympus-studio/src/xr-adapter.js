// Explicit adapter for X-Ray Mirror JSON detections. No camera/network access.
// Caller owns transport and must opt in to forwarding each sample.
export function createXRayAdapter(bus, { clock = Date.now } = {}) {
  if (!bus || typeof bus.publish !== 'function') throw new TypeError('Studio event bus required');
  return Object.freeze({
    ingest(sample) {
      if (!sample || typeof sample !== 'object' || Array.isArray(sample)) throw new TypeError('XR sample object required');
      const kind = sample.kind;
      if (kind !== 'gesture' && kind !== 'detection') throw new TypeError('Unsupported XR sample kind');
      const timestamp = sample.timestamp ?? clock();
      if (!Number.isSafeInteger(timestamp) || timestamp < 0) throw new TypeError('Invalid XR timestamp');
      const confidence = sample.confidence;
      if (confidence !== undefined && (!Number.isFinite(confidence) || confidence < 0 || confidence > 1)) throw new TypeError('Invalid confidence');
      const name = sample.name;
      if (typeof name !== 'string' || !/^[a-zA-Z0-9_-]{1,64}$/.test(name)) throw new TypeError('Invalid XR name');
      // Never forward raw camera frames, biometric arrays or unknown fields.
      const payload = { name, ...(confidence === undefined ? {} : { confidence }) };
      return bus.publish({ type: kind === 'gesture' ? 'xr.gesture' : 'xr.detection', source: 'XR', timestamp, payload });
    }
  });
}
