import test from 'node:test';
import assert from 'node:assert/strict';
import { plan, streamEnd, repairArgs } from '../tools/repair-av-tail.mjs';

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
 assert.equal(args.at(-1),'repaired.webm');
 assert.match(args[args.indexOf('-filter:v')+1],/stop_duration=0\.995/);
 assert.throws(()=>repairArgs('a','b',0,2),/Invalid repair duration/);
});
