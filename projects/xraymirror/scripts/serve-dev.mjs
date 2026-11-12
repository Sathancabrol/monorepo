// Zero-dependency dev preview server (fallback when Vite is unavailable).
// Serves the built dist/ on 0.0.0.0 with correct MIME types, including wasm.
import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { extname, join, normalize } from 'node:path';

const root = new URL('../dist/', import.meta.url).pathname;
const port = Number(process.env.PORT || 4173);
const types = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.wasm': 'application/wasm',
  '.json': 'application/json',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.task': 'application/octet-stream',
  '.tflite': 'application/octet-stream',
};

createServer(async (req, res) => {
  let url = decodeURIComponent((req.url || '/').split('?')[0]);
  if (url.endsWith('/')) url += 'index.html';
  const file = normalize(join(root, url));
  if (!file.startsWith(root)) {
    res.writeHead(400);
    return res.end('bad path');
  }
  try {
    const info = await stat(file);
    if (info.isDirectory()) throw new Error('directory');
    const data = await readFile(file);
    res.writeHead(200, {
      'content-type': types[extname(file)] || 'application/octet-stream',
      'content-length': data.length,
      'cache-control': 'no-store',
    });
    res.end(data);
  } catch {
    res.writeHead(404, { 'content-type': 'text/plain' });
    res.end('not found');
  }
}).listen(port, '0.0.0.0', () => {
  console.log(`xraymirror dist on http://0.0.0.0:${port}`);
});
