import test from 'node:test';
import assert from 'node:assert/strict';
import { STUDIO_SPACES, validateStudioEvent, createStudioEventBus } from '../src/studio-events.js';
const event = (overrides = {}) => ({type:'xr.gesture',source:'XR',timestamp:1730000000000,payload:{gesture:'snap',confidence:0.9},...overrides});
test('12 spaces and validated XR to EDIT event delivery', () => {
  assert.equal(STUDIO_SPACES.length,12);
  const bus=createStudioEventBus(), received=[];
  const stop=bus.subscribe('xr.gesture',e=>received.push(e));
  const published=bus.publish(event());
  assert.deepEqual(received,[published]);
  stop(); bus.publish(event()); assert.equal(received.length,1);
});
test('reject malformed and oversized events before delivery',()=>{
  const bus=createStudioEventBus(); let calls=0; bus.subscribe('*',()=>calls++);
  for (const e of [event({source:'OTHER'}),event({type:'unknown'}),event({timestamp:NaN}),event({payload:null}),event({payload:{blob:'x'.repeat(65537)}})]) assert.throws(()=>bus.publish(e));
  assert.equal(calls,0);
});
test('payload snapshot is detached from caller mutations',()=>{
  const payload={gesture:'snap'}; const e=validateStudioEvent(event({payload})); payload.gesture='changed';
  assert.equal(e.payload.gesture,'snap'); assert.ok(Object.isFrozen(e));
});
