import { test } from 'node:test';
import assert from 'node:assert/strict';
import { assessStreams } from '../tools/check-av.mjs';
const fixture = (audioStart=0,audioDuration=2) => ({format:{duration:'2'},streams:[
 {codec_type:'video',codec_name:'vp8',start_time:'0',duration:'2'},
 {codec_type:'audio',codec_name:'opus',start_time:String(audioStart),duration:String(audioDuration)}
]});
test('A/V: flux Opus alignés acceptés',()=>assert.equal(assessStreams(fixture()).endDrift,0));
test('A/V: décalage supérieur au seuil rejeté',()=>assert.throws(()=>assessStreams(fixture(0,2.7)),/Décalage/));
test('A/V: absence audio rejetée',()=>assert.throws(()=>assessStreams({streams:[]}),/flux vidéo/));
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

test('A/V: longues captures FFprobe sans dépassement de pile', () => {
  const packets = [];
  for (let i = 0; i < 150000; i++) {
    packets.push({stream_index:0,pts_time:String(i * 0.02),duration_time:'0.02'});
    packets.push({stream_index:1,pts_time:String(i * 0.02),duration_time:'0.02'});
  }
  const result = assessStreams({format:{format_name:'matroska,webm'},streams:[
    {index:0,codec_type:'video',codec_name:'vp8'},
    {index:1,codec_type:'audio',codec_name:'opus'}
  ],packets});
  assert.equal(result.startDrift, 0);
  assert.equal(result.endDrift, 0);
});

test('A/V CLI: ffprobe JSON > 4 MiB reste analysable', async (t) => {
  if (process.platform === 'win32') return t.skip('Executable mock POSIX only');
  const { mkdtempSync, writeFileSync, chmodSync, rmSync } = await import('node:fs');
  const { tmpdir } = await import('node:os');
  const { join, delimiter } = await import('node:path');
  const { spawnSync } = await import('node:child_process');
  const dir = mkdtempSync(join(tmpdir(), 'olympus-ffprobe-'));
  try {
    const fake = join(dir, 'ffprobe');
    writeFileSync(fake, '#!/usr/bin/env node\n' +
      'process.stdout.write(JSON.stringify({format:{format_name:"matroska,webm"},streams:[' +
      '{codec_type:"video",codec_name:"vp8",start_time:"0",duration:"2"},' +
      '{codec_type:"audio",codec_name:"opus",start_time:"0",duration:"2"}],' +
      'padding:"x".repeat(5*1024*1024)}));\n');
    chmodSync(fake, 0o755);
    const result = spawnSync(process.execPath, [new URL('../tools/check-av.mjs', import.meta.url).pathname, 'fixture.webm'], {
      encoding: 'utf8', timeout: 30000, env: { ...process.env, PATH: dir + delimiter + process.env.PATH }
    });
    assert.equal(result.status, 0, result.stderr);
    assert.match(result.stdout, /"endDrift": 0/);
  } finally { rmSync(dir, {recursive:true, force:true}); }
});
