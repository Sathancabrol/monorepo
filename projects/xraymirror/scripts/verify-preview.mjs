// End-to-end asset smoke test: resolves index.html, its JS/CSS and the wasm
// runtime exactly like a browser would, relative to the app's base URL.
import { readFile } from 'node:fs/promises';
import { extname, join, normalize } from 'node:path';

const base = process.argv[2] || 'http://127.0.0.1:8123/preview/xraymirror/dist/';
const failures = [];

async function get(url) {
  const response = await fetch(url, { redirect: 'follow' });
  const buffer = Buffer.from(await response.arrayBuffer());
  return { status: response.status, contentType: response.headers.get('content-type'), buffer, url: response.url };
}

const index = await get(base.endsWith('/') ? base : `${base}/`);
if (index.status !== 200) failures.push(`index ${index.status}`);
if (!index.contentType?.includes('text/html')) failures.push(`index content-type ${index.contentType}`);
const html = index.buffer.toString('utf8');
const refs = [...html.matchAll(/(?:src|href)="([^"]+)"/g)]
  .map((match) => match[1])
  .filter((ref) => ref.startsWith('./'));
console.log(`index ${index.status} ${index.contentType} — ${refs.length} refs`);

for (const ref of refs) {
  const url = new URL(ref, index.url).href;
  const asset = await get(url);
  const expected =
    ref.endsWith('.js') ? 'javascript' : ref.endsWith('.css') ? 'text/css' : 'application/octet-stream';
  const ok = asset.status === 200 && (asset.contentType ?? '').includes(expected);
  console.log(`${ok ? 'OK ' : 'FAIL'} ${asset.status} ${asset.buffer.length} ${asset.contentType} ${ref}`);
  if (!ok) failures.push(ref);
}

const wasmUrl = new URL('./mediapipe/wasm/vision_wasm_internal.wasm', index.url).href;
const wasm = await get(wasmUrl);
const wasmOk = wasm.status === 200 && wasm.contentType === 'application/wasm' && wasm.buffer.subarray(0, 4).toString() === '\0asm';
console.log(`${wasmOk ? 'OK ' : 'FAIL'} ${wasm.status} ${wasm.buffer.length} wasm magic=${wasm.buffer.subarray(0, 4)}`);
if (!wasmOk) failures.push('wasm');

const loader = await get(new URL('./mediapipe/wasm/vision_wasm_internal.js', index.url).href);
console.log(`${loader.status === 200 ? 'OK ' : 'FAIL'} ${loader.status} ${loader.contentType} wasm loader`);

if (failures.length) {
  console.error('FAILURES:', failures);
  process.exit(1);
}
console.log('preview assets: all good');
