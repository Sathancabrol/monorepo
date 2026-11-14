import {test} from 'node:test';
import assert from 'node:assert/strict';
import {validateEditAudioTrack, audioAtTimeline} from '../src/edit-audio.js';
import {referencedAssetIds} from '../src/storyboard.js';

test('Une piste audio est non destructive, avec valeurs initiales sûres',()=>{
  const raw={assetId:'soundtrack',name:'Voix'};
  const t=validateEditAudioTrack(raw);
  assert.deepEqual(t,{assetId:'soundtrack',name:'Voix',offset:0,inPoint:0,volume:1,enabled:true});
  assert.equal(raw.offset,undefined);
  assert.deepEqual(validateEditAudioTrack({...t,volume:0,enabled:false}).volume,0);
  for(const changes of [{assetId:''},{offset:-1},{offset:Infinity},{inPoint:-1},{volume:1.1},{volume:NaN}])
    assert.throws(()=>validateEditAudioTrack({...t,...changes}),/invalide|manquant/);
});
test('Placement global, point IN, fin de source et piste coupée',()=>{
  const t=validateEditAudioTrack({assetId:'a',offset:5,inPoint:2,volume:.5});
  assert.equal(audioAtTimeline(t,0,20).active,false);
  assert.equal(audioAtTimeline(t,5,20).sourceTime,2);
  assert.equal(audioAtTimeline(t,9.5,20).sourceTime,6.5);
  assert.equal(audioAtTimeline(t,23,20).active,false);
  assert.equal(audioAtTimeline({...t,enabled:false},6,20).active,false);
  assert.equal(audioAtTimeline(t,6,null).active,true);
  assert.equal(audioAtTimeline(t,NaN,20).active,false);
});
test('Le projet portable n’oublie pas la piste audio et ne duplique pas les médias',()=>{
  const scenes=[{layers:[{type:'image',id:'image1',assetId:'photo'}]}];
  const clips=[{assetId:'film'},{assetId:'film'}];
  const audio=validateEditAudioTrack({assetId:'voice'});
  assert.deepEqual(referencedAssetIds(scenes,clips,audio),['photo','film','voice']);
  const restored=validateEditAudioTrack(JSON.parse(JSON.stringify(audio)));
  assert.deepEqual(restored,audio);
  assert.deepEqual(referencedAssetIds([],[],{assetId:'film'}),['film']);
});
