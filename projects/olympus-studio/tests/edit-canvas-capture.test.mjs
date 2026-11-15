import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';

// Structural guard; actual A/V duration and Opus content are checked by
// browser_edit_export_e2e.py with ffprobe in the dedicated CI workflow.
test('EDIT redraw changes capture-only pixels before requesting a video frame', () => {
 const source=readFileSync(new URL('../src/app.js',import.meta.url),'utf8');
 const start=source.indexOf('function drawEditor(now)');
 const end=source.indexOf('let editorExportPreparing=false;',start);
 assert.ok(start>=0 && end>start);
 const draw=source.slice(start,end);
 assert.match(draw,/editorRecorder\?\.state==='recording'/);
 assert.match(draw,/const marker=\(\+\+editorCaptureFrame\)%2/);
 assert.doesNotMatch(draw,/Math\.floor\(now\/32\)%2/, 'capture marker must not alias on repeated timestamps');
 assert.match(draw,/context\.fillRect\(canvas\.width-8,canvas\.height-8,8,8\)/);
 assert.ok(draw.indexOf('context.fillRect(canvas.width-8') < draw.indexOf('editorVideoCaptureTrack?.requestFrame?.()'));
});
