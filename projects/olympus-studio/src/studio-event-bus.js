// Local, synchronous event bus for XR fixtures and future opt-in adapters.
// No network, camera, storage or external side effects.
export function validateStudioEvent(input) {
  if (!input || typeof input !== 'object' || Array.isArray(input)) throw new TypeError('Event object required');
  const {type, timestampMs, source, payload, schemaVersion} = input;
  if (schemaVersion !== 1) throw new TypeError('Unsupported event schema');
  if (!['xr.detections','xr.snap'].includes(type)) throw new TypeError('Unsupported event type');
  if (typeof source !== 'string' || !/^[a-z0-9][a-z0-9._-]{0,63}$/i.test(source)) throw new TypeError('Invalid event source');
  if (!Number.isFinite(timestampMs) || timestampMs < 0) throw new TypeError('Invalid timestamp');
  if (!payload || typeof payload !== 'object' || Array.isArray(payload)) throw new TypeError('Invalid payload');
  if (type === 'xr.detections') {
    if (!Array.isArray(payload.items) || payload.items.length > 30) throw new TypeError('Invalid detections');
    const items = payload.items.map(d => {
      if (!d || typeof d !== 'object' || Array.isArray(d)) throw new TypeError('Invalid detection');
      const {x,y,w,h} = d;
      if (![x,y,w,h].every(v => typeof v === 'number' && Number.isFinite(v)) || x<0 || y<0 || w<=0 || h<=0 || x+w>1 || y+h>1) throw new RangeError('Detection outside normalized frame');
      return Object.freeze({label:String(d.label??'objet').slice(0,80),x,y,w,h});
    });
    return Object.freeze({type,source,timestampMs,schemaVersion,payload:Object.freeze({items:Object.freeze(items)})});
  }
  if (payload.action !== 'toggle-overlays') throw new TypeError('Unsupported gesture action');
  return Object.freeze({type,source,timestampMs,schemaVersion,payload:Object.freeze({action:'toggle-overlays'})});
}
export function createStudioEventBus() {
  const listeners = new Map();
  return Object.freeze({
    subscribe(type, callback) {
      if (!['xr.detections','xr.snap'].includes(type) || typeof callback !== 'function') throw new TypeError('Invalid subscription');
      const set = listeners.get(type) ?? new Set(); set.add(callback); listeners.set(type,set);
      return () => {set.delete(callback); if (!set.size) listeners.delete(type);};
    },
    publish(input) {
      const event = validateStudioEvent(input);
      for (const callback of [...(listeners.get(event.type)??[])]) callback(event);
      return event;
    }
  });
}
