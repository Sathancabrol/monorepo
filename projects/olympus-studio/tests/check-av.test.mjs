import { test } from 'node:test';
import assert from 'node:assert/strict';
import { assessStreams } from '../tools/check-av.mjs';
const fixture = (audioStart=0,audioDuration=2) => ({format:{duration:'2'},streams:[
 {codec_type:'video',codec_name:'vp8',start_time:'0',duration:'2'},
 {codec_type:'audio',codec_name:'opus',start_time:String(audioStart),duration:String(audioDuration)}
]});
test('A/V: flux Opus alignés acceptés',()=>assert.equal(assessStreams(fixture()).endDrift,0));
test('A/V: décalage supérieur au seuil rejeté',()=>assert.throws(()=>assessStreams(fixture(0,2.7)),/Décalage/));
test('A/V: absence audio rejetée',()=>assert.throws(()=>assessStreams({streams:[]}),/absent/));
test('A/V: métadonnées invalides rejetées',()=>assert.throws(()=>assessStreams(fixture(0,-1)),/invalides/));
