import { test } from 'node:test';
import assert from 'node:assert/strict';
import { exportPortableAssets, importPortableAsset, mediaLayerUsable, PORTABLE_LIMIT } from '../src/media-store.js';

test('Portabilité : image binaire de plus de 64 Ko sans perte', async () => {
  const bytes = Uint8Array.from({ length: 150003 }, (_, n) => n % 251);
  const item = { id: 'asset-10', name: 'image démo.png', type: 'image/png', blob: new Blob([bytes], { type: 'image/png' }) };
  const exported = await exportPortableAssets([item]);
  assert.equal(exported.length, 1);
  const restored = importPortableAsset(exported[0]);
  assert.equal(restored.id, item.id);
  assert.equal(restored.name, item.name);
  assert.equal(restored.blob.type, 'image/png');
  assert.deepEqual(new Uint8Array(await restored.blob.arrayBuffer()), bytes);
});
test('Portabilité : zéro média et petite image', async () => {
  assert.deepEqual(await exportPortableAssets([]), []);
  const items = await exportPortableAssets([{ id: 't', name: 't', type: 'image/png', blob: new Blob([new Uint8Array([0, 255, 1])], { type: 'image/png' }) }]);
  assert.equal(importPortableAsset(items[0]).size, 3);
});
test('Le budget de taille est appliqué avant lecture', async () => {
  await assert.rejects(exportPortableAssets([{ id:'too-large', name:'a', blob:new Blob([new Uint8Array(6)]) }], 5), /limité/);
  assert.throws(() => importPortableAsset({ id:'a', name:'b', type:'video/mp4', data_b64:'AAAA', size:99 }), /incohérente/);
  assert.throws(() => importPortableAsset({ id:'a', name:'b', type:'video/mp4', data_b64:'**', size:2 }), /base64 invalide/);
  assert.equal(PORTABLE_LIMIT, 45 * 1024 * 1024);
});
test('Association calque et média stricte', () => {
  const asset = { id:'layer-123', type:'image/png' };
  assert.equal(mediaLayerUsable(asset, { id:'layer-123', type:'image' }), true);
  assert.equal(mediaLayerUsable(asset, { id:'layer-xyz', type:'image' }), false);
  assert.equal(mediaLayerUsable(asset, { id:'layer-123', type:'video' }), false);
});
