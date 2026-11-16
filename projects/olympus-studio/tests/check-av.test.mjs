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

test('A/V: WebM sans stream.duration utilise les timestamps des paquets', () => {
  const probe = {format:{format_name:'matroska,webm',duration:'2'},streams:[
    {index:0,codec_type:'video',codec_name:'vp8'},
    {index:1,codec_type:'audio',codec_name:'opus'}
  ],packets:[
    {stream_index:0,pts_time:'0',duration_time:'0.04'},
    {stream_index:0,pts_time:'1.96',duration_time:'0.04'},
    {stream_index:1,pts_time:'0.02',duration_time:'0.02'},
    {stream_index:1,pts_time:'1.98',duration_time:'0.02'}
  ]};
  assert.ok(assessStreams(probe).endDrift < 0.01);
  probe.packets[3].pts_time = '2.7';
  assert.throws(() => assessStreams(probe), /Décalage/);
});
test('A/V: durée globale ne masque pas les durées de flux absentes', () =>
  assert.throws(() => assessStreams({format:{duration:'2'},streams:[
    {codec_type:'video',codec_name:'vp8',start_time:'0'},
    {codec_type:'audio',codec_name:'opus',start_time:'0'}
  ]}), /invalides/));
test('A/V: codec vidéo incompatible rejeté', () =>
  assert.throws(() => assessStreams({format:{duration:'2'},streams:[
    {codec_type:'video',codec_name:'h264',start_time:'0',duration:'2'},
    {codec_type:'audio',codec_name:'opus',start_time:'0',duration:'2'}
  ]}), /Codec vidéo/));
