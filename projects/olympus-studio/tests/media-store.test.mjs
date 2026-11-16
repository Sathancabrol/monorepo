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

// An invalid record must never yield a seemingly complete portable archive.
test('Portabilité : refuse un média manquant plutôt que produire une archive partielle', async () => {
  const good = { id: 'valid', name: 'valid.png', type: 'image/png', blob: new Blob([new Uint8Array([1, 2, 3])], { type: 'image/png' }) };
  await assert.rejects(exportPortableAssets([good, { id: 'missing-blob', name: 'lost.png' }]), /export incomplet refusé/);
  await assert.rejects(exportPortableAssets([good, null]), /export incomplet refusé/);
  await assert.rejects(exportPortableAssets([good, { id: '', name: 'empty.png', blob: good.blob }]), /export incomplet refusé/);
});


test('Portabilité : deux références du même identifiant ne peuvent pas créer une archive ambiguë', async () => {
  const blob = new Blob([new Uint8Array([1, 2, 3])], { type: 'image/png' });
  const first = { id: 'shared', name: 'first.png', type: 'image/png', blob };
  const second = { id: 'shared', name: 'second.png', type: 'image/png', blob };
  await assert.rejects(exportPortableAssets([first, second]), /dupliqué/);
  assert.equal((await exportPortableAssets([first])).length, 1);
});

test('Portabilité : restauration refuse identifiants et noms vides', () => {
  const base = { id: 'asset', name: 'photo.png', type: 'image/png', data_b64: 'AQID', size: 3 };
  for (const id of ['', '  ']) assert.throws(() => importPortableAsset({ ...base, id }), /invalide/);
  for (const name of ['', '  ']) assert.throws(() => importPortableAsset({ ...base, name }), /invalide/);
  assert.equal(importPortableAsset(base).blob.size, 3);
});


test('Portabilité : export refuse noms absents ou blancs, cohérent avec import', async () => {
  const blob = new Blob([new Uint8Array([1, 2, 3])], { type: 'image/png' });
  for (const name of [undefined, '', '  ']) {
    await assert.rejects(exportPortableAssets([{ id: 'a', name, type: 'image/png', blob }]), /export incomplet refusé/);
  }
  await assert.rejects(exportPortableAssets([{ id: '  ', name: 'valid.png', type: 'image/png', blob }]), /export incomplet refusé/);
  const archive = await exportPortableAssets([{ id: 'a', name: 'valid.png', type: 'image/png', blob }]);
  assert.equal(importPortableAsset(archive[0]).name, 'valid.png');
});
