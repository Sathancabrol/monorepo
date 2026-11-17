import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { plan, streamEnd, repairArgs, verifyRepair } from '../tools/repair-av-tail.mjs';

test('detects a missing video tail without hiding its length',()=>{
 assert.deepEqual(plan(1.712,2.707),{needed:true,gap:2.707-1.712,pad:'0.995'});
});
test('does not repair aligned streams',()=>assert.equal(plan(2.669,2.677).needed,false));
test('rejects corrupt or implausibly large gaps',()=>{
 assert.throws(()=>plan(NaN,2),/Invalid/);
 assert.throws(()=>plan(1,50),/Gap over/);
});
test('uses packet end including duration',()=>{
 assert.equal(streamEnd({packets:[{pts_time:'0.2',duration_time:'0.1'},{pts_time:'1.5',duration_time:'0.04'}]}),1.54);
});

test('FFmpeg repair refuses overwrite even if output appears after preflight',()=>{
 const args=repairArgs('source.webm','repaired.webm',0.995,2.707);
 assert.ok(args.includes('-n'));
 assert.ok(!args.includes('-y'));
 assert.deepEqual(args.slice(args.indexOf('-map'),args.indexOf('-filter:v')),['-map','0:v:0','-map','0:a:0']);
 assert.equal(args.at(-1),'repaired.webm');
 assert.match(args[args.indexOf('-filter:v')+1],/stop_duration=0\.995/);
 assert.throws(()=>repairArgs('a','b',0,2),/Invalid repair duration/);
});

// The documented command must run main() on Windows and POSIX, even with a
// relative entrypoint. Without this, the CLI could exit 0 without any repair.
test('FFmpeg repair CLI actually invokes its entrypoint for relative and absolute paths',()=>{
 const root=fileURLToPath(new URL('..',import.meta.url));
 const absolute=fileURLToPath(new URL('../tools/repair-av-tail.mjs',import.meta.url));
 for(const entry of ['tools/repair-av-tail.mjs',absolute]){
  const result=spawnSync(process.execPath,[entry],{cwd:root,encoding:'utf8',timeout:10000});
  assert.equal(result.status,1,`CLI must fail on missing arguments: ${entry}`);
  assert.match(result.stderr,/Usage: node tools\/repair-av-tail\.mjs/);
 }
});

// The CLI must not claim a successful repair based only on FFmpeg exit status.
test('postflight verification rejects missing duration and excessive drift',()=>{
 assert.deepEqual(verifyRepair(2.70,2.71),{videoEnd:2.70,audioEnd:2.71,drift:2.71-2.70});
 assert.throws(()=>verifyRepair(1.9,2.7),/drift exceeds/);
 assert.throws(()=>verifyRepair(0,2.7),/Invalid repaired/);
 assert.throws(()=>verifyRepair(NaN,2.7),/Invalid repaired/);
});
