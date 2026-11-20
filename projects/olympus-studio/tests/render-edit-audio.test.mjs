import {test} from 'node:test';
import assert from 'node:assert/strict';
import {renderAudioArgs} from '../scripts/render-edit-audio.mjs';
test('FFmpeg EDIT audio: trim source IN, offset, volume and final duration',()=>{
 const args=renderAudioArgs('input.wav','out.wav',{assetId:'a',inPoint:1.5,offset:.25,volume:.4},3);
 const filter=args[args.indexOf('-filter_complex')+1];
 assert.match(filter,/atrim=start=1\.500000/);
 assert.match(filter,/volume=0\.400000/);
 assert.match(filter,/adelay=250:all=1/);
 assert.match(filter,/aresample=48000/);
 assert.match(filter,/apad=whole_len=144000/);
 assert.match(filter,/atrim=end_sample=144000/);
 assert.doesNotMatch(filter,/atrim=duration=/);
 assert.deepEqual(args.slice(-2),['-n','out.wav']);
});
test('Mute and invalid parameters are explicit; no shell commands',()=>{
 const args=renderAudioArgs('a.wav','b.wav',{assetId:'a',enabled:false,volume:.9},2);
 assert.match(args[args.indexOf('-filter_complex')+1],/volume=0\.000000/);
 assert.throws(()=>renderAudioArgs('a','a',{assetId:'a'},2),/Chemins/);
 for(const d of [0,-1,121,NaN,Infinity])assert.throws(()=>renderAudioArgs('a','b',{assetId:'a'},d),/Durée/);
 assert.throws(()=>renderAudioArgs('a','b',{assetId:'a',offset:-1},2),/Départ/);
 assert.ok(!args.includes('-shell'));
 assert.ok(!args.includes('-y'), 'Never overwrite existing output files');
});
