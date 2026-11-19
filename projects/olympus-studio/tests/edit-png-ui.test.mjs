import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

// Wiring regression: the existing Node suite cannot grant a browser directory permission.
const app = readFileSync(new URL('../src/app.js', import.meta.url), 'utf8');
test('EDIT exposes an explicit user-gesture PNG export, without implicit filesystem access', () => {
  assert.match(app, /pngSequenceButton\.id='editPngSequence'/);
  assert.match(app, /pngSequenceButton\.onclick=exportEditorPngSequence/);
  assert.match(app, /await window\.showDirectoryPicker\(\{mode:'readwrite'\}\)/);
  assert.match(app, /renderEditPngFrames\(clips,/);
  assert.match(app, /onFrame:sink/);
  assert.match(app, /editorExportPreparing=true/);
  assert.match(app, /finally\{editorExportPreparing=false;\}/);
  assert.match(app, /aucun encodage automatique/);
});
