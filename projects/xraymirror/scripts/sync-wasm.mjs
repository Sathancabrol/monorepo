// Copies the MediaPipe wasm runtime used by the built preview into public/.
// Run after npm install when rebuilding: node scripts/sync-wasm.mjs
import { copyFile, mkdir } from 'node:fs/promises';

const source = new URL('../node_modules/@mediapipe/tasks-vision/wasm/', import.meta.url);
const target = new URL('../public/mediapipe/wasm/', import.meta.url);
await mkdir(target, { recursive: true });
for (const file of ['vision_wasm_internal.js', 'vision_wasm_internal.wasm']) {
  await copyFile(new URL(file, source), new URL(file, target));
  console.log('copied', file);
}
