import { test } from 'node:test';
import assert from 'node:assert/strict';
import { toEditInterchange } from '../src/edit-interchange.js';
import { inspectEditInterchangeAssets } from '../src/edit-interchange-assets.js';

test('EDIT import preflight deduplicates split sources and includes soundtrack', () => {
  const manifest = toEditInterchange([
    {id:'a',kind:'video',assetId:'movie',inPoint:0,outPoint:1},
    {id:'b',kind:'video',assetId:'movie',inPoint:1,outPoint:2},
    {id:'c',kind:'image',assetId:'still',duration:1},
  ], {assetId:'music',offset:0,inPoint:0,volume:1,enabled:true});
  const before = JSON.stringify(manifest);
  assert.deepEqual(inspectEditInterchangeAssets(manifest, ['movie']), {
    ready:false, referencedAssetIds:['movie','still','music'],
    missingAssetIds:['still','music'], clips:3,
  });
  assert.equal(inspectEditInterchangeAssets(manifest, ['movie','still','music']).ready,true);
  assert.equal(JSON.stringify(manifest),before);
});

test('EDIT import preflight rejects invalid manifest and available IDs', () => {
  const manifest = toEditInterchange([{id:'a',kind:'image',assetId:'still',duration:1}]);
  assert.throws(() => inspectEditInterchangeAssets({...manifest,schema:'other'},[]),/schema/);
  assert.throws(() => inspectEditInterchangeAssets(manifest,['']),/asset IDs/);
  assert.throws(() => inspectEditInterchangeAssets(manifest,null),/asset IDs/);
  assert.deepEqual(inspectEditInterchangeAssets(manifest,[]).missingAssetIds,['still']);
});
