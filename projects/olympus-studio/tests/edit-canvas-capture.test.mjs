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
 assert.match(draw,/const marker=\+\+editorCaptureFrame/);
 assert.match(draw,/for\(let tile=0;tile<64;tile\+\+\)/);
 assert.match(draw,/const value=\(marker\*37\+x\*71\+y\*43\+\(x\*y\*17\)\)&255/);
 assert.doesNotMatch(draw,/\(\+\+editorCaptureFrame\)%2/, 'two-state marker aliases after dropped frames');
 assert.doesNotMatch(draw,/Math\.floor\(now\/32\)%2/, 'capture marker must not alias on repeated timestamps');
 assert.match(draw,/context\.fillRect\(canvas\.width-96\+x\*12,canvas\.height-96\+y\*12,12,12\)/);
 assert.ok(draw.indexOf('context.fillRect(canvas.width-96+x*12') < draw.indexOf('editorVideoCaptureTrack?.requestFrame?.()'));
});

// The browser encoder may coalesce requestFrame() samples under load.
// A paced stream is required as a fallback for uninterrupted A/V timestamps.
test('EDIT export uses paced canvas capture instead of manual-only frames', () => {
 const source=readFileSync(new URL('../src/app.js',import.meta.url),'utf8');
 const start=source.indexOf('async function exportEditorWebM(');
 const end=source.indexOf('function draw(){',start);
 assert.ok(start>=0 && end>start);
 const exportBody=source.slice(start,end);
 assert.ok(exportBody.includes('stream=canvas.captureStream(24)'), 'paced 24 fps capture must be enabled');
 assert.ok(!exportBody.includes('canvas.captureStream(0)'), 'manual-only capture must not regress');
});
