import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtempSync, readFileSync, readdirSync, rmSync, statSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const command = (bin,args,cwd) => spawnSync(bin,args,{cwd,encoding:'utf8',timeout:120000,maxBuffer:8*1024*1024});
const available = ['ffmpeg','ffprobe'].every(bin=>command(bin,['-version']).status===0);

test('FFmpeg tail repair selects first A/V tracks in a multi-audio WebM', {skip:!available,timeout:120000},()=>{
 const dir=mkdtempSync(join(tmpdir(),'olympus-multitrack-'));
 try {
  const input=join(dir,'source.webm'), output=join(dir,'repaired.webm');
  const generate=command('ffmpeg',['-hide_banner','-loglevel','error','-nostdin','-f','lavfi','-i','color=c=blue:s=160x90:r=24:d=1','-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=2','-f','lavfi','-i','sine=frequency=880:sample_rate=48000:duration=2','-map','0:v:0','-map','1:a:0','-map','2:a:0','-c:v','libvpx','-b:v','200k','-c:a','libopus','-y',input],dir);
  assert.equal(generate.status,0,generate.stderr);
  const original=readFileSync(input);
  const repair=command(process.execPath,['tools/repair-av-tail.mjs',input,output],root);
  assert.equal(repair.status,0,repair.stderr);
  const report=JSON.parse(repair.stdout);
  assert.ok(report.verified.drift<=0.2,JSON.stringify(report));
  const probe=command('ffprobe',['-v','error','-show_streams','-of','json',output],dir);
  assert.equal(probe.status,0,probe.stderr);
  const streams=JSON.parse(probe.stdout).streams;
  assert.equal(streams.filter(s=>s.codec_type==='video').length,1);
  assert.equal(streams.filter(s=>s.codec_type==='audio').length,1);
  assert.deepEqual(readFileSync(input),original,'source must remain unchanged');
  assert.ok(statSync(output).size>0);
 } finally { rmSync(dir,{recursive:true,force:true}); }
});
