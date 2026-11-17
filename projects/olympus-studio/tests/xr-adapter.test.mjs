import test from 'node:test';
import assert from 'node:assert/strict';
import { createStudioEventBus } from '../src/studio-events.js';
import { createXRayAdapter } from '../src/xr-adapter.js';

test('XR gesture fixture crosses adapter into Studio bus without network', () => {
  const bus=createStudioEventBus(), received=[];
  bus.subscribe('xr.gesture', e=>received.push(e));
  const adapter=createXRayAdapter(bus, {clock:()=>1730000000000});
  const result=adapter.ingest({kind:'gesture',name:'finger_snap',confidence:0.95,frame:'private-image'});
  assert.equal(result.timestamp,1730000000000);
  assert.deepEqual(received,[result]);
  assert.deepEqual(result.payload,{name:'finger_snap',confidence:0.95});
  assert.equal(JSON.stringify(result).includes('private-image'),false);
});
test('XR detections preserve explicit timestamps and never execute actions',()=>{
  const bus=createStudioEventBus(); let count=0;
  bus.subscribe('xr.detection',()=>count++);
  const adapter=createXRayAdapter(bus);
  adapter.ingest({kind:'detection',name:'person',timestamp:1730000000001});
  assert.equal(count,1);
});
test('XR adapter rejects invalid data before bus delivery',()=>{
  const bus=createStudioEventBus(); let count=0;
  bus.subscribe('*',()=>count++);
  const adapter=createXRayAdapter(bus);
  for (const bad of [null,{}, {kind:'gesture',name:'snap',confidence:2},{kind:'gesture',name:'snap',timestamp:-1},{kind:'gesture',name:'<script>'},{kind:'video',name:'snap'}]) assert.throws(()=>adapter.ingest(bad));
  assert.equal(count,0);
});
