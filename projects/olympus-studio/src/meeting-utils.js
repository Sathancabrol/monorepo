// OLYMPUS Studio — deterministic subtitle import/export; no ASR or external APIs.
export function parseSRT(source) {
  if (typeof source !== 'string') throw new Error('SRT doit être un texte');
  const blocks = source.replace(/^\uFEFF/, '').replace(/\r\n?/g, '\n').trim().split(/\n\s*\n/);
  const entries = [];
  const timePattern = /(\d{2}):(\d{2}):(\d{2})[,\.](\d{3})/;
  const parseTime = value => {
    const m = value.match(new RegExp('^'+timePattern.source+'$'));
    if (!m) return NaN;
    const [, h, min, sec, ms] = m;
    if (+min > 59 || +sec > 59) return NaN;
    return +h * 3600 + +min * 60 + +sec + +ms / 1000;
  };
  for (const block of blocks.slice(0, 10000)) {
    const lines = block.split('\n').map(s=>s.trim()).filter(Boolean);
    const stampAt = lines.findIndex(s => s.includes('-->'));
    if (stampAt < 0) continue;
    const stamp = lines[stampAt].match(/^(\d{2}:\d{2}:\d{2}[,.]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[,.]\d{3})/);
    if (!stamp) continue;
    const start = parseTime(stamp[1]), end = parseTime(stamp[2]);
    if (!Number.isFinite(start) || !Number.isFinite(end) || end <= start) continue;
    const line = lines.slice(stampAt+1).join(' ').slice(0,4000);
    if (!line) continue;
    const speakerMatch = line.match(/^([^:]{1,60}):\s+(.+)$/);
    entries.push({ t: start, end, speaker: speakerMatch ? speakerMatch[1].trim() : 'Intervenant', text: speakerMatch ? speakerMatch[2] : line, verified: false, source: 'srt-import' });
  }
  return entries.sort((a,b)=>a.t-b.t);
}
export function srtTimestamp(seconds) {
  const ms = Math.max(0,Math.round(Number(seconds||0)*1000));
  const h = Math.floor(ms / 3600000), min = Math.floor((ms % 3600000)/60000), sec=Math.floor((ms%60000)/1000), rest=ms%1000;
  return [h,min,sec].map(n=>String(n).padStart(2,'0')).join(':')+','+String(rest).padStart(3,'0');
}
export function formatSRT(entries) {
  return entries.map((item, index) => (index+1)+'\n'+srtTimestamp(item.t)+' --> '+srtTimestamp(item.end ?? item.t+3)+'\n'+(item.speaker ? item.speaker+': ' : '')+item.text+'\n').join('\n');
}
export function exportMeetingNotes(entries) {
  const rows = entries.map(item => '- **'+srtTimestamp(item.t).replace(',','.')+'** — '+String(item.speaker || 'Intervenant').replace(/\*/g,'')+': '+String(item.text||'').replace(/\n/g,' '));
  return '# Compte rendu de réunion (transcription non vérifiée)\n\n'+rows.join('\n')+'\n\n> Export automatique des segments, pas une validation des décisions ou des faits.\n';
}
