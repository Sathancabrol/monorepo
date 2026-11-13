import { test } from 'node:test';
import assert from 'node:assert/strict';
import http from 'node:http';
import { once } from 'node:events';
import { createMobilePreviewServer } from '../scripts/mobile-preview.mjs';

async function start(server) {
  server.listen(0, '127.0.0.1');
  await once(server, 'listening');
  return server.address().port;
}

test('Mobile preview exposes only static files and a read-only health check', async t => {
  const upstreamRequests = [];
  const upstream = http.createServer((req, res) => {
    upstreamRequests.push({ url: req.url, method: req.method, host: req.headers.host });
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('studio-ok');
  });
  const upstreamPort = await start(upstream);
  t.after(() => upstream.close());

  const proxy = createMobilePreviewServer({ upstreamPort });
  const port = await start(proxy);
  t.after(() => proxy.close());
  const base = 'http://127.0.0.1:' + port;

  const home = await fetch(base + '/');
  assert.equal(home.status, 200);
  assert.equal(await home.text(), 'studio-ok');
  assert.equal(upstreamRequests[0].host, '127.0.0.1:' + upstreamPort);

  const js = await fetch(base + '/src/app.js');
  assert.equal(js.status, 200);
  const cameraPool = await fetch(base + '/src/camera-pool.js');
  assert.equal(cameraPool.status, 200);
  const health = await fetch(base + '/api/health');
  assert.equal(health.status, 200);

  for (const path of ['/server.mjs', '/api/comfy/job', '/obs', '/.env']) {
    const res = await fetch(base + path);
    assert.equal(res.status, 403, path);
  }

  const post = await fetch(base + '/api/comfy/queue', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: '{}',
  });
  assert.equal(post.status, 405);
  assert.equal(upstreamRequests.length, 3, 'Forbidden requests must never reach Studio');
});
