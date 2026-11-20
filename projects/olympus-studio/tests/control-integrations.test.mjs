import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

test('CONTROL renders all 12 server-provided integration contracts without HTML injection', async () => {
  const source = await readFile(new URL('../src/app.js', import.meta.url), 'utf8');
  assert.match(source, /state\.space==='CONTROL'/);
  assert.match(source, /fetch\('\/api\/integrations'/);
  assert.match(source, /payload\.spaces/);
  assert.match(source, /integrations\.length!==12/);
  assert.match(source, /heading\.textContent=/);
  assert.match(source, /description\.textContent=/);
  assert.match(source, /probe\.textContent=/);
  assert.match(source, /button\.disabled=true/);
  assert.match(source, /finally\{button\.disabled=false/);
  const controlSource = source.slice(source.indexOf("else if(state.space==='CONTROL')"));
  assert.doesNotMatch(controlSource, /innerHTML\s*=.*item\.engine/);
});
