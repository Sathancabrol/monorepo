import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createStudioEventBus,validateStudioEvent} from '../src/studio-event-bus.js';
const detection={type:'xr.detections',schemaVersion:1,source:'xray-fixture',timestampMs:100,payload:{items:[{label:'main',x:0.1,y:0.2,w:0.3,h:0.4}]}};
test('validated local detection dispatch and unsubscribe',()=>{
 const bus=createStudioEventBus(), received=[];
 const stop=bus.subscribe('xr.detections',e=>received.push(e));
 const result=bus.publish(detection);
 assert.equal(received.length,1);assert.equal(result.payload.items[0].label,'main');
 assert.ok(Object.isFrozen(result.payload.items));
 stop();bus.publish(detection);assert.equal(received.length,1);
});
test('snap gesture is explicit and does not dispatch detections',()=>{
 const bus=createStudioEventBus();let toggles=0, detections=0;
 bus.subscribe('xr.snap',()=>toggles++);bus.subscribe('xr.detections',()=>detections++);
 bus.publish({type:'xr.snap',schemaVersion:1,source:'ui-demo',timestampMs:0,payload:{action:'toggle-overlays'}});
 assert.equal(toggles,1);assert.equal(detections,0);
});
test('reject malformed or unsafe inputs before listeners',()=>{
 const bus=createStudioEventBus();let count=0;bus.subscribe('xr.detections',()=>count++);
 for(const bad of [
  {...detection,schemaVersion:2},
  {...detection,source:'https://external'},
  {...detection,timestampMs:Infinity},
  {...detection,payload:{items:[{label:'bad',x:-1,y:0,w:0.2,h:0.2}]}},
  {...detection,payload:{items:[{label:'bad',x:0.9,y:0,w:0.2,h:0.2}]}},
  {...detection,payload:{items:Array.from({length:31},()=>({x:0,y:0,w:0.1,h:0.1}))}},
  {type:'xr.snap',schemaVersion:1,source:'demo',timestampMs:0,payload:{action:'run-command'}}
 ]) assert.throws(()=>bus.publish(bad));
 assert.equal(count,0);
});
test('snapshot sanitizes detection fields and isolates caller mutation',()=>{
 const e=validateStudioEvent({...detection,payload:{items:[{...detection.payload.items[0],secret:'not forwarded'}]}});
 assert.equal('secret' in e.payload.items[0],false);
 assert.throws(()=>{e.payload.items[0].x=0.8;},TypeError);
});
