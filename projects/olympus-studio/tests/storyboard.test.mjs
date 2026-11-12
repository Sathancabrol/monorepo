import { test } from 'node:test';
import assert from 'node:assert/strict';
import { clipDuration, storyboardDuration, locateClip, moveClip, validateClip, referencedAssetIds } from '../src/storyboard.js';
test('Timeline séquentielle : durée et recherche de source',()=>{
 const clips=[
  {id:'a',assetId:'a',kind:'image',duration:2},
  {id:'b',assetId:'b',kind:'video',inPoint:4,outPoint:9},
  {id:'c',assetId:'c',kind:'image',duration:3},
 ];
 assert.equal(clipDuration(clips[1]),5);
 assert.equal(storyboardDuration(clips),10);
 assert.equal(locateClip(clips,0).index,0);
 assert.equal(locateClip(clips,3).index,1);
 assert.equal(locateClip(clips,3).sourceTime,5);
 assert.equal(locateClip(clips,7).index,2);
 assert.equal(locateClip(clips,10),null);
});
test('Déplacement et validation sans mutation',()=>{
 const clips=[{id:'a'},{id:'b'},{id:'c'}];
 const moved=moveClip(clips,0,1);
 assert.equal(moved[0].id,'b');
 assert.equal(clips[0].id,'a');
 assert.equal(moveClip(clips,0,-1)[0].id,'a');
 assert.equal(validateClip({id:'a',assetId:'x',kind:'image',duration:4}).duration,4);
 assert.throws(()=>validateClip({id:'x',assetId:'y',kind:'gif'}),/invalide/);
});

test('Projet portable réunit médias des scènes et clips EDIT',()=>{
 const scenes=[{layers:[{id:'layer-1',type:'image',assetId:'asset-A'},{id:'layer-2',type:'rect'}]}];
 const clips=[{assetId:'asset-B'},{assetId:'asset-A'}];
 assert.deepEqual(referencedAssetIds(scenes,clips),['asset-A','asset-B']);
});
