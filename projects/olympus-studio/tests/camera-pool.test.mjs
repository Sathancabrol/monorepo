import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createCameraPool } from '../src/camera-pool.js';

function fakeStream() {
  const track = { readyState:'live', stops:0, stop() {this.readyState='ended';this.stops++;} };
  return { track, getVideoTracks() {return [track];}, getTracks() {return [track];} };
}

test('Local Webcam and Diffuser ma caméra share one camera acquisition', async () => {
  const stream = fakeStream();
  let calls=0;
  const pool=createCameraPool(async()=>{calls++;return stream;});
  const local=await pool.acquire('local-webcam');
  const mobile=await pool.acquire('shared-preview',{preferRear:true});
  assert.strictEqual(local,mobile);
  assert.equal(calls,1);
  pool.release('local-webcam');
  assert.equal(stream.track.stops,0, 'Releasing the local preview must not stop sharing');
  pool.release('shared-preview');
  assert.equal(stream.track.stops,1,'Last owner releases the physical camera');
  assert.equal(pool.isActive(),false);
});

test('Concurrent capture requests use a single pending getUserMedia promise', async () => {
  let resolve;
  const pending=new Promise(r=>{resolve=r;});
  let calls=0;
  const pool=createCameraPool(async()=>{calls++;return pending;});
  const a=pool.acquire('local-webcam');
  const b=pool.acquire('shared-preview');
  const stream=fakeStream();
  resolve(stream);
  assert.strictEqual(await a,stream);
  assert.strictEqual(await b,stream);
  assert.equal(calls,1);
  pool.release('shared-preview');
  pool.release('local-webcam');
  assert.equal(stream.track.stops,1);
});

test('Android rear-camera startup failure falls back to front camera', async () => {
  const args=[];
  const stream=fakeStream();
  const pool=createCameraPool(async constraints=>{
    args.push(constraints);
    if(args.length===1)throw Object.assign(new Error('Could not start video source'),{name:'NotReadableError'});
    return stream;
  });
  assert.strictEqual(await pool.acquire('shared-preview',{preferRear:true}),stream);
  assert.equal(args[0].video.facingMode.ideal,'environment');
  assert.equal(args[1].video.facingMode.ideal,'user');
  pool.release('shared-preview');
});

test('Permission refusal is not retried on other cameras', async()=>{
  let count=0;
  const pool=createCameraPool(async()=>{
    count++;
    throw Object.assign(new Error('Permission denied'),{name:'NotAllowedError'});
  });
  await assert.rejects(pool.acquire('shared-preview',{preferRear:true}), /Permission denied/);
  assert.equal(count,1);
  assert.equal(pool.isActive(),false);
});
