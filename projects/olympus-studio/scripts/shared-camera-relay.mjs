// OLYMPUS Studio — private, in-memory camera relay for Tailscale Serve.
// This is deliberately separate from server.mjs: no privileged workstation APIs.
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const MAX_FRAME = 350_000;
const TTL_MS = 12_000;
const MAX_STREAMS = 4;
const MIN_INTERVAL_MS = 150;

function send(res, status, data, contentType = 'application/json; charset=utf-8') {
  res.writeHead(status, {
    'Content-Type': contentType,
    'Cache-Control': 'no-store',
    'X-Content-Type-Options': 'nosniff',
    'Cross-Origin-Resource-Policy': 'same-origin',
    'X-Frame-Options': 'DENY',
  });
  res.end(contentType.startsWith('application/json') ? JSON.stringify(data) : data);
}
function deny(res, code, message) { send(res, code, { error: message }); }

function sameOriginWrite(req) {
  const site = req.headers['sec-fetch-site'];
  if (site && site !== 'same-origin') return false;
  const origin = req.headers.origin;
  if (typeof origin !== 'string') return false;
  let url;
  try { url = new URL(origin); } catch { return false; }
  if (url.protocol === 'https:' && /^[a-z0-9-]+(?:\.[a-z0-9-]+)*\.ts\.net$/i.test(url.hostname)) {
    // Only reachable via the separately configured private Tailscale Serve endpoint.
    return true;
  }
  return url.protocol === 'http:' && ['localhost', '127.0.0.1'].includes(url.hostname);
}

async function readFrame(req) {
  const parts = [];
  let size = 0;
  for await (const chunk of req) {
    size += chunk.length;
    if (size > MAX_FRAME) throw new Error('Frame > 350 kB');
    parts.push(chunk);
  }
  const frame = Buffer.concat(parts);
  if (frame.length < 4 || frame[0] !== 0xff || frame[1] !== 0xd8 ||
      frame[frame.length - 2] !== 0xff || frame[frame.length - 1] !== 0xd9) {
    throw new Error('JPEG attendu');
  }
  return frame;
}

export function createSharedCameraRelay({ now = () => Date.now() } = {}) {
  const streams = new Map();
  function clean() {
    const time = now();
    for (const [id, stream] of streams) if (time - stream.updatedAt > TTL_MS) streams.delete(id);
  }
  return async function handleCamera(req, res, url) {
    if (!url.pathname.startsWith('/api/live/')) return false;
    clean();
    const id = url.searchParams.get('id') || req.headers['x-olympus-stream-id'] || '';
    const method = req.method || 'GET';

    if (method === 'GET' && url.pathname === '/api/live/streams') {
      send(res, 200, { streams: [...streams.values()].map(({ id, name, updatedAt }) => ({ id, name, ageMs: now() - updatedAt })) });
      return true;
    }
    if (method === 'GET' && url.pathname === '/api/live/frame') {
      const stream = streams.get(id);
      if (!UUID.test(id) || !stream) deny(res, 404, 'Flux indisponible');
      else send(res, 200, stream.frame, 'image/jpeg');
      return true;
    }

    if ((method === 'POST' || method === 'DELETE') && url.pathname === '/api/live/frame') {
      if (!sameOriginWrite(req)) { deny(res, 403, 'Origine interdite'); return true; }
      const key = req.headers['x-olympus-stream-key'] || '';
      if (!UUID.test(id) || !UUID.test(key)) { deny(res, 400, 'Identifiants invalides'); return true; }
      const existing = streams.get(id);
      if (existing && existing.key !== key) { deny(res, 403, 'Flux appartenant à une autre session'); return true; }
      if (method === 'DELETE') {
        if (existing) streams.delete(id);
        send(res, 200, { ok: true });
        return true;
      }
      if (!String(req.headers['content-type'] || '').startsWith('image/jpeg')) {
        deny(res, 415, 'JPEG attendu'); return true;
      }
      if (!existing && streams.size >= MAX_STREAMS) {
        deny(res, 429, 'Trop de caméras simultanées'); return true;
      }
      if (existing && now() - existing.updatedAt < MIN_INTERVAL_MS) {
        deny(res, 429, 'Cadence trop élevée'); return true;
      }
      let frame;
      try { frame = await readFrame(req); }
      catch (e) { deny(res, 413, e.message); return true; }
      const name = String(req.headers['x-olympus-device-name'] || existing?.name || 'Appareil').replace(/[\x00-\x1f<>]/g, '').slice(0, 40);
      streams.set(id, { id, key, name: name || 'Appareil', updatedAt: now(), frame });
      send(res, 200, { ok: true, id });
      return true;
    }

    deny(res, 405, 'Route caméra non autorisée');
    return true;
  };
}
