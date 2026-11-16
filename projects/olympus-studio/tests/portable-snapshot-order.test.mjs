import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

// Regression guard for the UI entry point: dbReady may be pending for seconds.
// A snapshot after that await would capture edits made while IndexedDB opens.
test('Portable snapshots timeline and media references before awaiting IndexedDB', () => {
  const app = readFileSync(new URL('../src/app.js', import.meta.url), 'utf8');
  const start = app.indexOf('async function savePortableProject()');
  const end = app.indexOf('async function restoreLayerMedia()', start);
  assert.ok(start >= 0 && end > start, 'Portable export function exists');
  const body = app.slice(start, end);
  const snapshot = body.indexOf('snapshotPortableProject(projectPayload(),referencedAssetIds)');
  const dbWait = body.indexOf('await dbReady');
  assert.ok(snapshot >= 0 && dbWait >= 0 && snapshot < dbWait,
    'project and media IDs must be frozen before any IndexedDB await');
});
