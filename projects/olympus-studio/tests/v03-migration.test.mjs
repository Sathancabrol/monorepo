import { test } from 'node:test';
import assert from 'node:assert/strict';
import { migrateV03Project } from '../src/v03-migration.js';
import { importPortableAsset,mediaLayerUsable } from '../src/media-store.js';
test('Import du prototype v0.3 : géométrie, médias et annotations conservées',()=>{
 const source={app:'OLYMPUS Studio',version:'0.3',scenes:[{id:'sc1',name:'LIVE',layers:[
  {id:'ly1',type:'shape',name:'Bandeau',x:128,y:72,w:640,h:360,color:'#ffffff',visible:true},
  {id:'ly2',type:'image',name:'Test',src:'asset:a1',x:0,y:0,w:1280,h:720}
 ]}],activeScene:'sc1',assets:[{id:'a1',filename:'test.png',size:3,type:'image/png'}],
 embeddedAssets:[{id:'a1',filename:'test.png',type:'image/png',base64:'AP8B'}],
 meeting:{transcript:[{t:1,text:'Bonjour',speaker:'A'}],privateNotes:'SECRET',captionsEnabled:true},
 edit:{clips:[{id:'c1'}]},automation:{rules:[{id:'r1'}]}};
 const project=migrateV03Project(source);
 assert.equal(project.schema,2);
 assert.deepEqual(project.scenes[0].layers[0].type,'rect');
 assert.equal(project.scenes[0].layers[0].x,0.1);
 assert.equal(project.scenes[0].layers[0].y,0.1);
 assert.equal(project.scenes[0].layers[1].assetId,'a1');
 const asset=importPortableAsset(project.embeddedAssets[0]);
 assert.equal(asset.size,3);
 assert.ok(mediaLayerUsable(asset,project.scenes[0].layers[1]));
 assert.equal(project.legacyV03.meeting.privateNotes,'SECRET');
 assert.equal(project.legacyV03.edit.clips.length,1);
 assert.equal(project.legacyV03.automation.rules.length,1);
 assert.equal(project.captionsVisible,undefined);
});
test('Un fichier non v0.3 est refusé',()=>assert.throws(()=>migrateV03Project({app:'OLYMPUS Studio',version:'0.2',scenes:[]}),/incompatible/));
