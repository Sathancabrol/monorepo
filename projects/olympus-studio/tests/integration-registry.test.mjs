import test from 'node:test';
import assert from 'node:assert/strict';
import { SPACE_INTEGRATIONS, integrationSnapshot } from '../src/integration-registry.js';

const expected = ['LIVE','EDIT','GENERATE','XR','AUDIO','MEETING','CAPTURE','CINEMA','AUTOMATE','GRAPHICS','LIBRARY','CONTROL'];

test('twelve spaces have unique and nonempty source-to-contract records', () => {
  assert.deepEqual(SPACE_INTEGRATIONS.map(row=>row.space), expected);
  for (const row of SPACE_INTEGRATIONS) {
    for (const field of ['engine','transport','contract','status']) {
      assert.equal(typeof row[field], 'string');
      assert.ok(row[field].trim(), row.space+' missing '+field);
    }
  }
});
test('availability probes never claim integration was end-to-end verified', () => {
  const rows=integrationSnapshot({obs:true,comfyui:true});
  assert.equal(rows.length,12);
  assert.equal(rows.find(row=>row.space==='LIVE').reachable,true);
  assert.equal(rows.find(row=>row.space==='GENERATE').reachable,true);
  assert.ok(rows.every(row=>row.operationallyVerified===false));
  assert.ok(rows.filter(row=>!['LIVE','GENERATE'].includes(row.space)).every(row=>row.reachable===null));
});
test('unavailable endpoints remain unavailable without inferring capability', () => {
  const rows=integrationSnapshot({obs:false,comfyui:false});
  assert.equal(rows.find(row=>row.space==='LIVE').reachable,false);
  assert.equal(rows.find(row=>row.space==='GENERATE').reachable,false);
  assert.ok(rows.every(row=>row.operationallyVerified===false));
});
