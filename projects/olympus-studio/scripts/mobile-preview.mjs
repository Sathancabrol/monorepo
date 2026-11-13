/**
 * OLYMPUS Studio mobile preview gateway (read-only, Tailnet-only).
 *
 * Keep both this service and the actual Studio bound to 127.0.0.1.
 * Expose ONLY this port with "tailscale serve", never with "tailscale funnel".
 * No privileged Studio POST operations are forwarded from mobile devices.
 */
import http from 'node:http';
import { createSharedCameraRelay } from './shared-camera-relay.mjs';
import { fileURLToPath } from 'node:url';
import { resolve } from 'node:path';

const STATIC_PATHS = new Set([
  '/', '/index.html',
  '/src/style.css', '/src/app.js', '/src/media-store.js',
  '/src/meeting-utils.js', '/src/v03-migration.js',
  '/src/storyboard.js', '/src/edit-audio.js',
  '/src/obs-panel.css', '/src/obs-panel.js', '/src/obs-client.js',
  '/src/video-duration.js', '/src/shared-camera.js',
]);

function reply(res, status, message) {
  res.writeHead(status, {
    'Content-Type': 'text/plain; charset=utf-8',
    'Cache-Control': 'no-store',
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
  });
  res.end(message);
}

export function createMobilePreviewServer({ upstreamPort = 8787 } = {}) {
  if (!Number.isInteger(upstreamPort) || upstreamPort < 1 || upstreamPort > 65535) {
    throw new Error('Invalid OLYMPUS_PORT');
  }

  const handleLive = createSharedCameraRelay();
  return http.createServer((req, res) => {
    let pathname;
    try {
      pathname = new URL(req.url ?? '/', 'http://localhost').pathname;
    } catch {
      return reply(res, 400, 'Invalid URL');
    }

    if (pathname.startsWith('/api/live/')) {
      void handleLive(req, res, new URL(req.url, 'http://localhost')).catch(() => {
        if (!res.headersSent) reply(res, 500, 'Erreur caméra'); else res.destroy();
      });
      return;
    }

    if (!['GET', 'HEAD'].includes(req.method)) {
      return reply(res, 405, 'Mobile preview is read-only');
    }

    if (!STATIC_PATHS.has(pathname) && pathname !== '/api/health') {
      return reply(res, 403, 'Not available in mobile preview');
    }

    const upstream = http.request({
      hostname: '127.0.0.1',
      port: upstreamPort,
      method: req.method,
      path: req.url,
      headers: { Host: '127.0.0.1:' + upstreamPort },
    }, response => {
      const headers = {
        'Cache-Control': 'no-store',
        'X-Content-Type-Options': 'nosniff',
        'Referrer-Policy': 'no-referrer',
        'X-Frame-Options': 'DENY',
      };
      for (const key of ['content-type', 'content-length']) {
        if (response.headers[key] !== undefined) headers[key] = response.headers[key];
      }
      res.writeHead(response.statusCode ?? 502, headers);
      response.pipe(res);
    });

    upstream.setTimeout(10_000, () => upstream.destroy(new Error('Studio timeout')));
    upstream.on('error', () => {
      if (!res.headersSent) reply(res, 502, 'OLYMPUS Studio is not running on localhost');
      else res.destroy();
    });
    res.on('close', () => upstream.destroy());
    upstream.end();
  });
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const upstreamPort = Number(process.env.OLYMPUS_PORT || 8787);
  const previewPort = Number(process.env.OLYMPUS_MOBILE_PORT || 8788);
  if (!Number.isInteger(previewPort) || previewPort < 1 || previewPort > 65535) {
    throw new Error('Invalid OLYMPUS_MOBILE_PORT');
  }
  createMobilePreviewServer({ upstreamPort }).listen(previewPort, '127.0.0.1', () => {
    console.log('Mobile preview ready on http://127.0.0.1:' + previewPort);
    console.log('To make it available on your private tailnet: tailscale serve --bg ' + previewPort);
    console.log('Do NOT use tailscale funnel or router port-forwarding.');
  });
}
