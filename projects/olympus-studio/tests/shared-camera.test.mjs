import { test } from 'node:test';
import assert from 'node:assert/strict';
import { once } from 'node:events';
import http from 'node:http';
import { createMobilePreviewServer } from '../scripts/mobile-preview.mjs';

async function start(server) {
  server.listen(0, '127.0.0.1');
  await once(server, 'listening');
  return server.address().port;
}

const JPEG = Buffer.from([0xff, 0xd8, 0x10, 0x20, 0xff, 0xd9]);
const OWN = '8b2d559e-a1c6-4ab2-8453-d19b269a8850';
const KEY = 'd1d2d3d4-a111-4bb2-8c33-98e0228744e5';
const OTHER_KEY = 'c2c2c2c2-a111-4bb2-8c33-98e0228744e5';
const ORIGIN = 'https://nthan-pc.testtail.ts.net';

test('Camera frames can be shared between private browser sessions, with no privileged proxy forwarding', async t => {
  const upstreamRequests = [];
  const upstream = http.createServer((req, res) => {
    upstreamRequests.push(req.url);
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('studio');
  });
  const upstreamPort = await start(upstream);
  t.after(() => upstream.close());
  const server = createMobilePreviewServer({ upstreamPort });
  const port = await start(server);
  t.after(() => server.close());
  const base = 'http://127.0.0.1:' + port;
  const url = base + '/api/live/frame';
  const headers = {
    Origin: ORIGIN,
    'Sec-Fetch-Site': 'same-origin',
    'Content-Type': 'image/jpeg',
    'X-Olympus-Stream-ID': OWN,
    'X-Olympus-Stream-Key': KEY,
    'X-Olympus-Device-Name': 'Samsung',
  };

  const published = await fetch(url, { method:'POST', headers, body: JPEG });
  assert.equal(published.status, 200, await published.text());

  const list = await fetch(base+'/api/live/streams');
  assert.equal(list.status, 200);
  const data = await list.json();
  assert.equal(data.streams.length, 1);
  assert.equal(data.streams[0].name, 'Samsung');
  assert.equal(data.streams[0].key, undefined, 'Owner secret must not be returned');

  const frame = await fetch(url+'?id='+OWN);
  assert.equal(frame.status, 200);
  assert.equal(frame.headers.get('content-type'), 'image/jpeg');
  assert.deepEqual(Buffer.from(await frame.arrayBuffer()), JPEG);

  const attacker = await fetch(url, {
    method:'POST', headers:{...headers, Origin:'https://evil.example'}, body: JPEG,
  });
  assert.equal(attacker.status, 403);
  const crossSite = await fetch(url, {
    method:'POST', headers:{...headers, 'Sec-Fetch-Site':'cross-site'}, body: JPEG,
  });
  assert.equal(crossSite.status, 403);
  const stolen = await fetch(url, {
    method:'DELETE', headers:{ Origin:ORIGIN, 'X-Olympus-Stream-Key':OTHER_KEY }, // No ownership
    redirect:'manual',
  });
  assert.equal(stolen.status, 400, 'Missing camera id is never accepted');

  const wrongOwner = await fetch(url+'?id='+OWN, {
    method:'DELETE', headers:{Origin:ORIGIN,'X-Olympus-Stream-Key':OTHER_KEY},
  });
  assert.equal(wrongOwner.status, 403);
  assert.equal((await (await fetch(base+'/api/live/streams')).json()).streams.length, 1);

  const prohibited = await fetch(base+'/api/comfy/queue',{
    method:'POST',headers:{Origin:ORIGIN, 'Content-Type':'application/json'},body:'{}',
  });
  assert.equal(prohibited.status, 405);
  assert.deepEqual(upstreamRequests, [], 'No camera or denied privileged action should reach Studio');

  const stopped = await fetch(url+'?id='+OWN, {
    method:'DELETE', headers:{Origin:ORIGIN,'X-Olympus-Stream-Key':KEY},
  });
  assert.equal(stopped.status, 200);
  assert.deepEqual((await (await fetch(base+'/api/live/streams')).json()).streams, []);
});

test('Camera relay enforces frame size, format and basic upload throttle', async t => {
  const upstream = http.createServer((req,res) => res.end('local'));
  const upstreamPort = await start(upstream); t.after(() => upstream.close());
  const server = createMobilePreviewServer({ upstreamPort });
  const port = await start(server); t.after(() => server.close());
  const base = 'http://127.0.0.1:'+port;
  const header = {
    Origin:'http://localhost:'+port, 'Content-Type':'image/jpeg',
    'X-Olympus-Stream-ID':OWN, 'X-Olympus-Stream-Key':KEY,
  };
  const wrong = await fetch(base+'/api/live/frame', {
    method:'POST', headers:header, body:'not a jpeg',
  });
  assert.equal(wrong.status, 413);
  const good = await fetch(base+'/api/live/frame',{
    method:'POST',headers:header,body:JPEG,
  });
  assert.equal(good.status, 200);
  const spam = await fetch(base+'/api/live/frame',{
    method:'POST',headers:header,body:JPEG,
  });
  assert.equal(spam.status, 429);
});
