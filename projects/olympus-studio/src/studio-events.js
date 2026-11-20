// Local-only, transport-agnostic event contract for Studio adapters.
// No implicit network, webcam or filesystem access.
export const STUDIO_SPACES = Object.freeze(['LIVE','EDIT','GENERATE','XR','AUDIO','MEETING','CAPTURE','CINEMA','AUTOMATE','GRAPHICS','LIBRARY','CONTROL']);
const TYPES = new Set(['media.imported','timeline.changed','render.started','render.finished','render.failed','xr.detection','xr.gesture','asr.segment','comfy.job','obs.status','scene.camera','agent.proposal']);
export function validateStudioEvent(event) {
  if (!event || typeof event !== 'object' || Array.isArray(event)) throw new TypeError('Event object required');
  const { type, source, timestamp, payload } = event;
  if (!TYPES.has(type)) throw new TypeError('Unknown Studio event type');
  if (!STUDIO_SPACES.includes(source)) throw new TypeError('Unknown Studio source');
  if (!Number.isSafeInteger(timestamp) || timestamp < 0) throw new TypeError('Invalid epoch timestamp');
  if (!payload || typeof payload !== 'object' || Array.isArray(payload)) throw new TypeError('Payload object required');
  const json = JSON.stringify(payload);
  if (json === undefined || json.length > 65536) throw new TypeError('Payload too large or not serializable');
  const copy = JSON.parse(json);
  return Object.freeze({ type, source, timestamp, payload: Object.freeze(copy) });
}
export function createStudioEventBus() {
  const listeners = new Map();
  return Object.freeze({
    subscribe(type, callback) {
      if (type !== '*' && !TYPES.has(type)) throw new TypeError('Unknown event subscription');
      if (typeof callback !== 'function') throw new TypeError('Callback required');
      const group = listeners.get(type) || new Set();
      group.add(callback); listeners.set(type, group);
      return () => { group.delete(callback); if (!group.size) listeners.delete(type); };
    },
    publish(input) {
      const event = validateStudioEvent(input);
      for (const callback of [...(listeners.get(event.type) || []), ...(listeners.get('*') || [])]) callback(event);
      return event;
    },
    clear() { listeners.clear(); }
  });
}
