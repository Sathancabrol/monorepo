import { test } from 'node:test';
import assert from 'node:assert/strict';
import { parseSRT, formatSRT, srtTimestamp, exportMeetingNotes } from '../src/meeting-utils.js';
test('Import et export de sous-titres SRT, temps exacts et locuteurs',()=>{
 const file='1\r\n00:00:02,120 --> 00:00:03,920\r\nIntervenant 1: Bonjour.\r\n\r\n2\r\n00:00:04,000 --> 00:00:05,125\r\nMerci pour votre venue.';
 const lines=parseSRT(file);
 assert.equal(lines.length,2);
 assert.equal(lines[0].speaker,'Intervenant 1');
 assert.equal(lines[0].t,2.12);
 assert.equal(lines[0].end,3.92);
 assert.equal(lines[1].speaker,'Intervenant');
 const again=parseSRT(formatSRT(lines));
 assert.deepEqual(again, lines);
 assert.equal(srtTimestamp(3601.004),'01:00:01,004');
});
test('Entrées invalides ignorées et export annoté comme non vérifié',()=>{
 const lines=parseSRT('1\n00:00:33,000 --> 00:00:31,000\nInvalide\n\n2\n00:00:44,100 --> 00:00:45,000\nValide');
 assert.equal(lines.length,1);
 assert.match(exportMeetingNotes(lines),/non vérifiée/);
 assert.throws(()=>parseSRT(null),/texte/);
});
