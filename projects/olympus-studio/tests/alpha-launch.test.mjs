import test from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createServer } from 'node:net';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
async function freePort() {
  const server = createServer();
  await new Promise((ok, fail) => server.once('error', fail).listen(0, '127.0.0.1', ok));
  const port = server.address().port;
  await new Promise(ok => server.close(ok));
  return port;
}
const sleep = ms => new Promise(ok => setTimeout(ok, ms));

test('alpha launch: real localhost HTTP, 12 spaces, assets and private paths', { timeout: 18000 }, async () => {
  const port = await freePort();
  const child = spawn(process.execPath, ['server.mjs'], {
    cwd: root, env: { ...process.env, OLYMPUS_PORT: String(port) },
    stdio: ['ignore', 'pipe', 'pipe']
  });
  let output = '';
  child.stdout.on('data', d => { output += d.toString(); });
  child.stderr.on('data', d => { output += d.toString(); });
  const base = `http://127.0.0.1:${port}`;
  try {
    let ready = false;
    for (let i = 0; i < 60; i++) {
      if (child.exitCode !== null) break;
      try {
        const response = await fetch(base + '/index.html', { signal: AbortSignal.timeout(500) });
        if (response.ok) { ready = true; break; }
      } catch { /* server not listening yet */ }
      await sleep(100);
    }
    assert.ok(ready, `Studio did not start: ${output}`);
    const health = await fetch(base + '/api/health');
    assert.equal(health.status, 200);
    const h = await health.json();
    assert.equal(h.ok, true);
    assert.equal(h.local, true);
    const integrations = await fetch(base + '/api/integrations');
    assert.equal(integrations.status, 200);
    const registry = await integrations.json();
    assert.equal(registry.local, true);
    assert.equal(registry.spaces.length, 12);
    for (const asset of ['/src/app.js', '/src/style.css', '/src/media-store.js']) {
      const response = await fetch(base + asset);
      assert.equal(response.status, 200, `public asset ${asset}`);
    }
    for (const privatePath of ['/server.mjs', '/package.json', '/docs/HANDOFF.md', '/.env']) {
      const response = await fetch(base + privatePath);
      assert.equal(response.status, 403, `private path ${privatePath}`);
    }
  } finally {
    child.kill();
    if (child.exitCode === null) await Promise.race([
      new Promise(ok => child.once('exit', ok)), sleep(1200)
    ]);
  }
});
