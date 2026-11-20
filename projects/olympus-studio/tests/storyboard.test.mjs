import { test } from 'node:test';
import assert from 'node:assert/strict';
import { clipDuration, storyboardDuration, locateClip, moveClip, validateClip, referencedAssetIds, trimVideoClip, splitVideoClip, splitStoryboardAt } from '../src/storyboard.js';
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

test('IN/OUT non destructif conserve le fichier et le titre',()=>{
 const initial=validateClip({id:'v1',assetId:'original',kind:'video',name:'Interview',inPoint:0,outPoint:12,title:'Bonjour'});
 const trimmed=trimVideoClip(initial,2.5,8.25);
 assert.equal(trimmed.inPoint,2.5);
 assert.equal(trimmed.outPoint,8.25);
 assert.ok(Math.abs(clipDuration(trimmed)-5.75)<1e-8);
 assert.equal(trimmed.assetId,'original');
 assert.equal(trimmed.title,'Bonjour');
 assert.equal(initial.inPoint,0);
 assert.equal(initial.outPoint,12);
 assert.throws(()=>trimVideoClip(initial,8,7),/invalide/);
 assert.throws(()=>trimVideoClip(initial,3,3.05),/invalide/);
 assert.throws(()=>trimVideoClip(initial,-1,4),/invalide/);
 assert.throws(()=>trimVideoClip(initial,0,Infinity),/invalide/);
});
test('Division de clip conserve le temps total, la référence et les sources',()=>{
 const clip=validateClip({id:'clipA',assetId:'file-123',kind:'video',name:'Vidéo',inPoint:3,outPoint:10,title:'Titre'});
 const [a,b]=splitVideoClip(clip,2,'clipB');
 assert.equal(a.id,'clipA');assert.equal(b.id,'clipB');
 assert.equal(a.inPoint,3);assert.equal(a.outPoint,5);
 assert.equal(b.inPoint,5);assert.equal(b.outPoint,10);
 assert.equal(a.assetId,b.assetId);
 assert.equal(a.title,b.title);
 assert.equal(clip.outPoint,10);
 assert.equal(clipDuration(a)+clipDuration(b),7);
 assert.throws(()=>splitVideoClip(clip,0.01,'other'),/bord/);
 assert.throws(()=>splitVideoClip(clip,6.99,'other'),/bord/);
 assert.throws(()=>splitVideoClip(clip,3,'clipA'),/Identifiant/);
});
test('Division au curseur global et réouverture par JSON',()=>{
 const clips=[
   validateClip({id:'img',assetId:'a',kind:'image',duration:4}),
   validateClip({id:'vid',assetId:'b',kind:'video',inPoint:7,outPoint:13}),
   validateClip({id:'other',assetId:'c',kind:'image',duration:2}),
 ];
 const before=storyboardDuration(clips);
 const split=splitStoryboardAt(clips,6,'right');
 assert.equal(split.length,4);
 assert.equal(split[1].inPoint,7);
 assert.equal(split[1].outPoint,9);
 assert.equal(split[2].inPoint,9);
 assert.equal(split[2].outPoint,13);
 assert.equal(storyboardDuration(split),before);
 assert.deepEqual(split.map(x=>x.assetId),['a','b','b','c']);
 assert.equal(locateClip(split,7).sourceTime,10);
 const recovered=JSON.parse(JSON.stringify(split)).map(validateClip);
 assert.deepEqual(recovered.map(x=>x.inPoint),split.map(x=>x.inPoint));
 assert.equal(storyboardDuration(recovered),before);
 assert.throws(()=>splitStoryboardAt(clips,1,'new'),/vidéos/);
 assert.throws(()=>splitStoryboardAt(clips,before,'new'),/Aucun clip/);
});
