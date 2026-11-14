import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { inspectEditInterchangeAssets } from '../src/edit-interchange-assets.js';
import { fromEditInterchange } from '../src/edit-interchange.js';

const manifest={schema:'olympus.edit.interchange.v1',timeUnit:'seconds',duration:3,segments:[{clipId:'c1',assetId:'image1',kind:'image',timelineStart:0,duration:3,sourceIn:0,title:'Test'}],soundtrack:null};
test('interchange import preflight rejects missing media before reconstruction',()=>{
 const check=inspectEditInterchangeAssets(manifest,[]);
 assert.equal(check.ready,false);assert.deepEqual(check.missingAssetIds,['image1']);
 assert.deepEqual(fromEditInterchange(manifest).clips.map(c=>c.assetId),['image1']);
});
test('EDIT browser wiring and HTTP allowlist include interchange dependencies',async()=>{
 const [app,server]=await Promise.all([readFile(new URL('../src/app.js',import.meta.url),'utf8'),readFile(new URL('../server.mjs',import.meta.url),'utf8')]);
 assert.match(app,/id='editImportManifest'/);
 assert.match(app,/inspectEditInterchangeAssets\(manifest,state\.assets\.map/);
 assert.match(app,/await getMedia\(db,id\)/);
 assert.match(app,/fromEditInterchange\(manifest\)/);
 assert.match(app,/commitEdit\(before\)/);
 for(const path of ['/src/edit-interchange.js','/src/edit-interchange-assets.js'])assert.ok(server.includes("'"+path+"'"),path);
});
