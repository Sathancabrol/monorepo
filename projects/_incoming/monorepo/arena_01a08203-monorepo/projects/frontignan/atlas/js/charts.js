/* =========================================================================
   charts.js — mini-bibliothèque de graphiques SVG, sans dépendance.
   Toutes les fonctions renvoient un élément <svg> prêt à insérer.
   ========================================================================= */
(function (global) {
  'use strict';
  const NS = 'http://www.w3.org/2000/svg';

  function el(tag, attrs, kids) {
    const n = document.createElementNS(NS, tag);
    if (attrs) for (const k in attrs) {
      if (attrs[k] === null || attrs[k] === undefined) continue;
      n.setAttribute(k, attrs[k]);
    }
    (kids || []).forEach(k => n.appendChild(k));
    return n;
  }
  function txt(x, y, s, cls, extra) {
    const t = el('text', Object.assign({ x, y, class: cls || 'lbl' }, extra || {}));
    t.textContent = s;
    return t;
  }
  function svg(w, h, cls) {
    return el('svg', { class: 'chart ' + (cls || ''), viewBox: `0 0 ${w} ${h}`, width: '100%',
      preserveAspectRatio: 'xMidYMid meet' });
  }

  /* ---------------- formats ---------------- */
  const NB = new Intl.NumberFormat('fr-FR');
  function fmt(v, kind) {
    if (v === null || v === undefined || Number.isNaN(v)) return '—';
    switch (kind) {
      case 'int': return NB.format(Math.round(v));
      case '0': return NB.format(Math.round(v));
      case '1': return NB.format(Math.round(v * 10) / 10);
      case '2': return NB.format(Math.round(v * 100) / 100);
      case '3': return NB.format(Math.round(v * 1000) / 1000);
      case 'pct': return (Math.round(v * 10) / 10).toLocaleString('fr-FR') + ' %';
      case 'eur': return NB.format(Math.round(v)) + ' €';
      case 'sign': return (v > 0 ? '+' : '') + (Math.round(v * 100) / 100).toLocaleString('fr-FR');
      default:
        if (Math.abs(v) >= 1000) return NB.format(Math.round(v));
        return NB.format(Math.round(v * 100) / 100);
    }
  }
  function nice(max) {
    if (max <= 0) return 1;
    const p = Math.pow(10, Math.floor(Math.log10(max)));
    const r = max / p;
    const steps = [1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10];
    for (let i = 0; i < steps.length; i++) if (r <= steps[i] + 1e-9) return steps[i] * p;
    return 10 * p;
  }

  /* ---------------- 1. barres classées ---------------- */
  function ranked(rows, o) {
    o = o || {};
    const data = rows.slice().sort((a, b) => (b.value ?? -Infinity) - (a.value ?? -Infinity));
    const rowH = o.rowH || 21, padL = o.padL || 132, padR = 56, top = 16;
    const w = 620, h = top + data.length * rowH + 28;
    const s = svg(w, h);
    const vals = data.map(d => d.value).filter(v => v !== null && v !== undefined);
    const lo = Math.min(0, Math.min.apply(null, vals));
    const hi = Math.max.apply(null, vals);
    const max = nice(hi - lo) + (lo < 0 ? -lo : 0);
    const x0 = padL, xw = w - padL - padR;
    const sc = v => x0 + ((v - lo) / (max || 1)) * xw;

    // bandes de référence : moyenne ± 1 écart-type
    if (o.stats && o.stats.ecart_type) {
      const a = sc(o.stats.moyenne - o.stats.ecart_type), b = sc(o.stats.moyenne + o.stats.ecart_type);
      s.appendChild(el('rect', { class: 'band', x: Math.max(x0, a), y: top - 6,
        width: Math.max(2, Math.min(b, x0 + xw) - Math.max(x0, a)), height: data.length * rowH + 6 }));
    }
    data.forEach((d, i) => {
      const y = top + i * rowH;
      s.appendChild(txt(padL - 8, y + 12, d.label, 'lbl', { 'text-anchor': 'end' }));
      if (d.value === null || d.value === undefined) {
        s.appendChild(txt(x0 + 4, y + 12, 'secret statistique', 'lbl', { 'font-style': 'italic' }));
        return;
      }
      const bw = Math.max(1.5, sc(d.value) - sc(lo));
      s.appendChild(el('rect', { class: 'bar' + (d.me ? ' me' : ''), x: sc(lo), y: y + 3.5,
        width: bw, height: rowH - 8, rx: 3 }));
      s.appendChild(txt(sc(d.value) + 6, y + 12, fmt(d.value, o.fmt) + (o.unit ? ' ' + o.unit : ''), 'val'));
    });
    const bottom = top + data.length * rowH;
    if (o.stats) {
      [['mediane', 'ref', 'médiane'], ['moyenne', 'ref2', 'moyenne']].forEach(([k, cls, lab]) => {
        const v = o.stats[k];
        if (v === undefined || v === null) return;
        s.appendChild(el('line', { class: cls, x1: sc(v), x2: sc(v), y1: top - 8, y2: bottom + 4 }));
        s.appendChild(txt(sc(v), bottom + 18, lab + ' ' + fmt(v, o.fmt), 'lbl',
          { 'text-anchor': 'middle', fill: cls === 'ref' ? '#e2b04a' : '#37c9b0' }));
      });
    }
    return s;
  }

  /* ---------------- 2. boîte à moustaches ---------------- */
  function box(stats, o) {
    o = o || {};
    const w = 620, h = 150, padL = 42, padR = 42, y0 = 62;
    const s = svg(w, h);
    const lo = stats.min, hi = stats.max, span = (hi - lo) || 1;
    const sc = v => padL + ((v - lo) / span) * (w - padL - padR);
    s.appendChild(el('line', { class: 'ax', x1: padL, x2: w - padR, y1: y0 + 34, y2: y0 + 34 }));
    // moustaches
    s.appendChild(el('line', { class: 'ax', x1: sc(lo), x2: sc(hi), y1: y0, y2: y0, stroke: '#2a5461' }));
    [lo, hi].forEach(v => s.appendChild(el('line', { class: 'ax', x1: sc(v), x2: sc(v),
      y1: y0 - 10, y2: y0 + 10, stroke: '#2a5461' })));
    // boîte
    s.appendChild(el('rect', { x: sc(stats.q1), y: y0 - 17, width: Math.max(2, sc(stats.q3) - sc(stats.q1)),
      height: 34, rx: 4, fill: '#2fa8c433', stroke: '#2fa8c4' }));
    s.appendChild(el('line', { x1: sc(stats.mediane), x2: sc(stats.mediane), y1: y0 - 17, y2: y0 + 17,
      stroke: '#e2b04a', 'stroke-width': 2.4 }));
    s.appendChild(el('circle', { cx: sc(stats.moyenne), cy: y0, r: 4, fill: '#37c9b0' }));
    // points individuels
    (o.points || []).forEach(p => {
      if (p.value === null || p.value === undefined) return;
      s.appendChild(el('circle', { class: 'pt' + (p.me ? ' me' : ''), cx: sc(p.value), cy: y0 + 26 + (p.me ? 0 : 0),
        r: p.me ? 5 : 3, opacity: p.me ? 1 : .5 }));
      if (p.me) {
        s.appendChild(txt(sc(p.value), y0 + 48, p.label + ' ' + fmt(p.value, o.fmt), 'val',
          { 'text-anchor': 'middle', fill: '#e2b04a' }));
      }
    });
    const marks = [['min', lo], ['Q1', stats.q1], ['méd.', stats.mediane], ['Q3', stats.q3], ['max', hi]];
    marks.forEach(([k, v]) => {
      s.appendChild(txt(sc(v), y0 - 26, k, 'lbl', { 'text-anchor': 'middle' }));
      s.appendChild(txt(sc(v), 20, fmt(v, o.fmt), 'val', { 'text-anchor': 'middle' }));
    });
    return s;
  }

  /* ---------------- 3. nuage de points + régression ---------------- */
  function scatter(pointsIn, o) {
    o = o || {};
    const points = (pointsIn || []).filter(p =>
      p && p.x !== null && p.x !== undefined && p.y !== null && p.y !== undefined);
    const w = 620, h = 380, padL = 62, padB = 52, padT = 18, padR = 18;
    const s = svg(w, h);
    if (!points.length) return s;
    const xs = points.map(p => p.x), ys = points.map(p => p.y);
    const xlo = Math.min.apply(null, xs), xhi = Math.max.apply(null, xs);
    const ylo = Math.min.apply(null, ys), yhi = Math.max.apply(null, ys);
    const xspan = (xhi - xlo) || 1, yspan = (yhi - ylo) || 1;
    const sx = v => padL + ((v - xlo + xspan * .06) / (xspan * 1.12)) * (w - padL - padR);
    const sy = v => h - padB - ((v - ylo + yspan * .08) / (yspan * 1.16)) * (h - padB - padT);
    for (let i = 0; i <= 4; i++) {
      const y = padT + (h - padB - padT) * i / 4;
      s.appendChild(el('line', { class: 'grid', x1: padL, x2: w - padR, y1: y, y2: y }));
      const v = ylo + yspan * 1.16 * (1 - i / 4) - yspan * .08;
      s.appendChild(txt(padL - 8, y + 3.5, fmt(v, o.yfmt), 'lbl', { 'text-anchor': 'end' }));
    }
    s.appendChild(el('line', { class: 'ax', x1: padL, x2: w - padR, y1: h - padB, y2: h - padB }));
    for (let i = 0; i <= 4; i++) {
      const v = xlo + xspan * (i / 4);
      s.appendChild(txt(sx(v), h - padB + 16, fmt(v, o.xfmt), 'lbl', { 'text-anchor': 'middle' }));
    }
    if (o.fit) {
      const a = o.fit.ordonnee, b = o.fit.pente;
      const x1 = xlo - xspan * .04, x2 = xhi + xspan * .04;
      s.appendChild(el('line', { class: 'fit', x1: sx(x1), y1: sy(a + b * x1), x2: sx(x2), y2: sy(a + b * x2) }));
    }
    points.forEach(p => {
      s.appendChild(el('circle', { class: 'pt' + (p.me ? ' me' : ''), cx: sx(p.x), cy: sy(p.y),
        r: p.me ? 6.5 : 4.5, opacity: p.me ? 1 : .8 }));
      if (p.me || o.labelAll) {
        s.appendChild(txt(sx(p.x) + 9, sy(p.y) + 4, p.label, 'lbl',
          { fill: p.me ? '#e2b04a' : '#7794a0', 'font-weight': p.me ? 600 : 400 }));
      }
    });
    if (o.xlabel) s.appendChild(txt(w / 2, h - 8, o.xlabel, 'lbl', { 'text-anchor': 'middle' }));
    if (o.ylabel) {
      const t = txt(0, 0, o.ylabel, 'lbl', { 'text-anchor': 'middle',
        transform: `translate(14,${(h - padB) / 2}) rotate(-90)` });
      s.appendChild(t);
    }
    if (o.fit) {
      const r = o.fit.r, r2 = o.fit.r2;
      s.appendChild(txt(w - padR, padT + 10,
        `r = ${fmt(r, '3')}   R² = ${fmt(r2, '3')}   n = ${o.fit.n}`, 'val',
        { 'text-anchor': 'end', fill: '#e2b04a' }));
      if (o.rho !== undefined && o.rho !== null) {
        s.appendChild(txt(w - padR, padT + 26, `ρ (Spearman) = ${fmt(o.rho, '3')}`, 'val',
          { 'text-anchor': 'end', fill: '#7794a0' }));
      }
    }
    return s;
  }

  /* ---------------- 4. série temporelle ---------------- */
  function line(xs, ys, o) {
    o = o || {};
    const w = 620, h = 300, padL = 58, padB = 40, padT = 22, padR = 22;
    const s = svg(w, h);
    const allY = ys.concat(o.proj ? o.proj.map(p => p.y) : []);
    const ylo = 0, yhi = Math.max.apply(null, allY) * 1.08;
    const xlo = xs[0], xhi = (o.proj && o.proj.length ? o.proj[o.proj.length - 1].x : xs[xs.length - 1]);
    const sx = v => padL + ((v - xlo) / ((xhi - xlo) || 1)) * (w - padL - padR);
    const sy = v => h - padB - ((v - ylo) / ((yhi - ylo) || 1)) * (h - padB - padT);
    for (let i = 0; i <= 4; i++) {
      const y = padT + (h - padB - padT) * i / 4;
      s.appendChild(el('line', { class: 'grid', x1: padL, x2: w - padR, y1: y, y2: y }));
      s.appendChild(txt(padL - 8, y + 3.5, fmt(yhi * (1 - i / 4), 'int'), 'lbl', { 'text-anchor': 'end' }));
    }
    const d = xs.map((x, i) => `${i ? 'L' : 'M'}${sx(x)},${sy(ys[i])}`).join(' ');
    s.appendChild(el('path', { d: d + ` L${sx(xs[xs.length - 1])},${sy(0)} L${sx(xs[0])},${sy(0)} Z`,
      fill: 'url(#gradA)', opacity: .18 }));
    const defs = el('defs');
    const g = el('linearGradient', { id: 'gradA', x1: 0, y1: 0, x2: 0, y2: 1 });
    g.appendChild(el('stop', { offset: '0%', 'stop-color': '#2fa8c4' }));
    g.appendChild(el('stop', { offset: '100%', 'stop-color': '#2fa8c4', 'stop-opacity': 0 }));
    defs.appendChild(g); s.appendChild(defs);
    s.appendChild(el('path', { d, fill: 'none', stroke: '#2fa8c4', 'stroke-width': 2.2 }));
    if (o.proj && o.proj.length) {
      const last = { x: xs[xs.length - 1], y: ys[ys.length - 1] };
      const pd = [`M${sx(last.x)},${sy(last.y)}`].concat(o.proj.map(p => `L${sx(p.x)},${sy(p.y)}`)).join(' ');
      s.appendChild(el('path', { d: pd, fill: 'none', stroke: '#e2b04a', 'stroke-width': 1.8,
        'stroke-dasharray': '5 4' }));
      o.proj.forEach(p => {
        s.appendChild(el('circle', { cx: sx(p.x), cy: sy(p.y), r: 4, fill: '#e2b04a' }));
        s.appendChild(txt(sx(p.x), sy(p.y) - 10, fmt(p.y, 'int'), 'val',
          { 'text-anchor': 'middle', fill: '#e2b04a' }));
      });
    }
    xs.forEach((x, i) => {
      s.appendChild(el('circle', { cx: sx(x), cy: sy(ys[i]), r: 3.2, fill: '#0b1417',
        stroke: '#2fa8c4', 'stroke-width': 1.6 }));
      if (i % (o.every || 1) === 0) {
        s.appendChild(txt(sx(x), h - padB + 16, x, 'lbl', { 'text-anchor': 'middle' }));
      }
    });
    if (o.mark) {
      o.mark.forEach(m => {
        s.appendChild(el('line', { class: 'ref', x1: sx(m.x), x2: sx(m.x), y1: padT, y2: h - padB }));
        s.appendChild(txt(sx(m.x) + 4, padT + 11, m.label, 'lbl', { fill: '#e2b04a' }));
      });
    }
    return s;
  }

  /* ---------------- 5. barres groupées ---------------- */
  function grouped(labels, series, o) {
    o = o || {};
    const w = 620, padL = 150, padR = 60, top = 26;
    const gap = 8, bh = 13;
    const rowH = series.length * bh + gap + 8;
    const h = top + labels.length * rowH + 14;
    const s = svg(w, h);
    const max = nice(Math.max.apply(null, series.flatMap(se => se.vals)));
    const sc = v => (v / max) * (w - padL - padR);
    const colors = ['#e2b04a', '#2fa8c4', '#79b36b', '#9b87d4', '#d8595b'];
    series.forEach((se, k) => {
      s.appendChild(el('rect', { x: padL + k * 108, y: 6, width: 9, height: 9, rx: 2, fill: colors[k % 5] }));
      s.appendChild(txt(padL + k * 108 + 13, 14.5, se.nom, 'lbl'));
    });
    labels.forEach((lab, i) => {
      const y = top + i * rowH;
      s.appendChild(txt(padL - 8, y + rowH / 2 - 2, lab, 'lbl', { 'text-anchor': 'end' }));
      series.forEach((se, k) => {
        const v = se.vals[i];
        s.appendChild(el('rect', { x: padL, y: y + k * bh, width: Math.max(1, sc(v)), height: bh - 2,
          rx: 2, fill: colors[k % 5], opacity: k === 0 ? .95 : .62 }));
        s.appendChild(txt(padL + sc(v) + 5, y + k * bh + 9.5, fmt(v, o.fmt || '1') + (o.unit || ''), 'val',
          { 'font-size': 9.5 }));
      });
    });
    return s;
  }

  /* ---------------- 6. anneau ---------------- */
  function donut(labels, parts, o) {
    o = o || {};
    const w = 620, h = 240, cx = 118, cy = 120, r = 84, ri = 50;
    const s = svg(w, h);
    const colors = ['#2fa8c4', '#e2b04a', '#79b36b', '#9b87d4', '#d8595b', '#37c9b0'];
    let a0 = -Math.PI / 2;
    const total = parts.reduce((a, b) => a + b, 0);
    parts.forEach((p, i) => {
      const a1 = a0 + (p / total) * Math.PI * 2;
      const large = (a1 - a0) > Math.PI ? 1 : 0;
      const d = [
        `M${cx + r * Math.cos(a0)},${cy + r * Math.sin(a0)}`,
        `A${r},${r} 0 ${large} 1 ${cx + r * Math.cos(a1)},${cy + r * Math.sin(a1)}`,
        `L${cx + ri * Math.cos(a1)},${cy + ri * Math.sin(a1)}`,
        `A${ri},${ri} 0 ${large} 0 ${cx + ri * Math.cos(a0)},${cy + ri * Math.sin(a0)}`, 'Z'].join(' ');
      s.appendChild(el('path', { d, fill: colors[i % colors.length], opacity: i === 0 ? .95 : .8 }));
      const y = 26 + i * 24;
      s.appendChild(el('rect', { x: 250, y: y - 9, width: 10, height: 10, rx: 2, fill: colors[i % colors.length] }));
      s.appendChild(txt(268, y, labels[i], 'lbl', { 'font-size': 12 }));
      s.appendChild(txt(600, y, fmt(p, '1') + ' %', 'val', { 'text-anchor': 'end' }));
    });
    if (o.center) {
      s.appendChild(txt(cx, cy - 2, o.center, 'val', { 'text-anchor': 'middle', 'font-size': 20, fill: '#fff' }));
      s.appendChild(txt(cx, cy + 16, o.centerSub || '', 'lbl', { 'text-anchor': 'middle' }));
    }
    return s;
  }

  /* ---------------- 7. matrice pouvoir / intérêt ---------------- */
  function quadrant(points, o) {
    o = o || {};
    const w = 620, h = 480, pad = 58;
    const s = svg(w, h);
    const sx = v => pad + ((v - 0.5) / 5) * (w - pad * 1.4);
    const sy = v => h - pad - ((v - 0.5) / 5) * (h - pad * 1.5);
    s.appendChild(el('rect', { x: sx(3.5), y: pad * .6, width: sx(5.5) - sx(3.5), height: sy(3.5) - pad * .6,
      fill: '#2fa8c414' }));
    [1, 2, 3, 4, 5].forEach(v => {
      s.appendChild(el('line', { class: 'grid', x1: sx(v), x2: sx(v), y1: pad * .6, y2: h - pad }));
      s.appendChild(el('line', { class: 'grid', x1: pad, x2: w - pad * .4, y1: sy(v), y2: sy(v) }));
      s.appendChild(txt(sx(v), h - pad + 16, v, 'lbl', { 'text-anchor': 'middle' }));
      s.appendChild(txt(pad - 8, sy(v) + 4, v, 'lbl', { 'text-anchor': 'end' }));
    });
    s.appendChild(el('line', { class: 'ref', x1: sx(3.5), x2: sx(3.5), y1: pad * .6, y2: h - pad }));
    s.appendChild(el('line', { class: 'ref', x1: pad, x2: w - pad * .4, y1: sy(3.5), y2: sy(3.5) }));
    const quads = [['Co-construire', sx(4.6), sy(5.3)], ['Tenir informés', sx(4.6), sy(1.1)],
      ['Écouter activement', sx(1.5), sy(5.3)], ['Surveiller', sx(1.5), sy(1.1)]];
    quads.forEach(([k, x, y]) => s.appendChild(txt(x, y, k, 'lbl',
      { 'text-anchor': 'middle', fill: '#e2b04a', 'font-size': 10.5, 'letter-spacing': 1 })));
    const famColor = { 'Institutionnel': '#2fa8c4', 'Économique': '#e2b04a', 'Société civile': '#79b36b' };
    // décalage anti-superposition
    const seen = {};
    points.forEach(p => {
      const key = p.x + '|' + p.y;
      const k = seen[key] = (seen[key] || 0) + 1;
      const ang = (k - 1) * 1.15, rad = (k - 1) ? 11 + (k - 1) * 3.2 : 0;
      const cx = sx(p.x) + Math.cos(ang) * rad, cy = sy(p.y) + Math.sin(ang) * rad;
      const g = el('g', { class: 'qpt', 'data-id': p.id || '' });
      g.appendChild(el('circle', { cx, cy, r: 6.5, fill: famColor[p.famille] || '#8fa3ac', opacity: .9 }));
      const t = txt(cx + 10, cy + 3.5, p.label.length > 26 ? p.label.slice(0, 25) + '…' : p.label, 'lbl',
        { 'font-size': 9.5 });
      g.appendChild(t);
      s.appendChild(g);
    });
    s.appendChild(txt(w / 2, h - 14, 'Influence (capacité à décider ou bloquer) →', 'lbl',
      { 'text-anchor': 'middle' }));
    s.appendChild(txt(0, 0, "Intérêt (intensité de l'enjeu) →", 'lbl',
      { 'text-anchor': 'middle', transform: `translate(16,${h / 2}) rotate(-90)` }));
    return s;
  }

  /* ---------------- 8. frise / gantt ---------------- */
  function gantt(rows, o) {
    o = o || {};
    const w = 620, padL = 190, padR = 30, top = 26, rowH = 22;
    const h = top + rows.length * rowH + 26;
    const s = svg(w, h);
    const y0 = Math.min.apply(null, rows.map(r => r.debut));
    const y1 = Math.max.apply(null, rows.map(r => r.fin));
    const sx = v => padL + ((v - y0) / ((y1 - y0) || 1)) * (w - padL - padR);
    const colors = { 'livré': '#79b36b', 'engagé': '#2fa8c4', 'annoncé': '#e2b04a',
      'incertain': '#d8595b', 'tendance': '#9b87d4' };
    for (let y = Math.ceil(y0 / 2) * 2; y <= y1; y += 2) {
      s.appendChild(el('line', { class: 'grid', x1: sx(y), x2: sx(y), y1: top - 6, y2: h - 24 }));
      s.appendChild(txt(sx(y), h - 8, y, 'lbl', { 'text-anchor': 'middle' }));
    }
    if (o.now) {
      s.appendChild(el('line', { class: 'ref', x1: sx(o.now), x2: sx(o.now), y1: top - 10, y2: h - 24 }));
      s.appendChild(txt(sx(o.now), top - 14, 'aujourd’hui', 'lbl', { 'text-anchor': 'middle', fill: '#e2b04a' }));
    }
    rows.forEach((r, i) => {
      const y = top + i * rowH;
      s.appendChild(txt(padL - 8, y + 13, r.nom.length > 30 ? r.nom.slice(0, 29) + '…' : r.nom, 'lbl',
        { 'text-anchor': 'end' }));
      s.appendChild(el('rect', { x: sx(r.debut), y: y + 4, width: Math.max(4, sx(r.fin) - sx(r.debut)),
        height: rowH - 10, rx: 4, fill: colors[r.statut] || '#8fa3ac', opacity: .85 }));
      if (r.cout) {
        s.appendChild(txt(sx(r.fin) + 6, y + 13, fmt(r.cout, '1') + ' M€', 'val', { 'font-size': 9.5 }));
      }
    });
    return s;
  }

  /* ---------------- 9. courbe de Lorenz ---------------- */
  function lorenz(points, giniVal, o) {
    o = o || {};
    const w = 420, h = 330, pad = 46;
    const s = svg(w, h);
    const sx = v => pad + v * (w - pad * 1.4);
    const sy = v => h - pad - v * (h - pad * 1.5);
    s.appendChild(el('line', { class: 'ax', x1: pad, x2: w - pad * .4, y1: h - pad, y2: h - pad }));
    s.appendChild(el('line', { class: 'ax', x1: pad, x2: pad, y1: pad * .6, y2: h - pad }));
    s.appendChild(el('line', { class: 'grid', x1: sx(0), y1: sy(0), x2: sx(1), y2: sy(1) }));
    const d = points.map((p, i) => `${i ? 'L' : 'M'}${sx(p.x)},${sy(p.y)}`).join(' ');
    s.appendChild(el('path', { d: d + ` L${sx(1)},${sy(0)} Z`, fill: '#2fa8c422' }));
    s.appendChild(el('path', { d, fill: 'none', stroke: '#2fa8c4', 'stroke-width': 2 }));
    points.forEach(p => p.label && s.appendChild(el('circle', { cx: sx(p.x), cy: sy(p.y), r: 2.6, fill: '#e2b04a' })));
    s.appendChild(txt(w / 2, h - 12, 'part cumulée des communes', 'lbl', { 'text-anchor': 'middle' }));
    s.appendChild(txt(0, 0, 'part cumulée de la population', 'lbl',
      { 'text-anchor': 'middle', transform: `translate(14,${h / 2}) rotate(-90)` }));
    s.appendChild(txt(sx(.06), sy(.9), 'Gini = ' + fmt(giniVal, '3'), 'val', { fill: '#e2b04a', 'font-size': 13 }));
    return s;
  }

  /* ---------------- 10. histogramme ---------------- */
  function histogram(values, stats, o) {
    o = o || {};
    const w = 620, h = 260, padL = 46, padB = 42, padT = 18, padR = 18;
    const s = svg(w, h);
    const k = o.bins || Math.max(4, Math.round(Math.sqrt(values.length)));
    const lo = stats.min, hi = stats.max, step = (hi - lo) / k || 1;
    const bins = new Array(k).fill(0);
    values.forEach(v => { const i = Math.min(k - 1, Math.floor((v - lo) / step)); bins[i]++; });
    const maxN = Math.max.apply(null, bins);
    const sx = i => padL + (i / k) * (w - padL - padR);
    const sy = n => h - padB - (n / maxN) * (h - padB - padT);
    bins.forEach((n, i) => {
      s.appendChild(el('rect', { x: sx(i) + 1.5, y: sy(n), width: (w - padL - padR) / k - 3,
        height: h - padB - sy(n), rx: 2, class: 'bar' }));
      if (n) s.appendChild(txt(sx(i) + (w - padL - padR) / (2 * k), sy(n) - 5, n, 'val',
        { 'text-anchor': 'middle', 'font-size': 9.5 }));
    });
    for (let i = 0; i <= k; i++) {
      s.appendChild(txt(sx(i), h - padB + 15, fmt(lo + i * step, o.fmt), 'lbl',
        { 'text-anchor': 'middle', 'font-size': 9 }));
    }
    const scv = v => padL + ((v - lo) / (hi - lo || 1)) * (w - padL - padR);
    [['mediane', '#e2b04a', 'médiane'], ['moyenne', '#37c9b0', 'moyenne']].forEach(([kk, c, lab]) => {
      const v = stats[kk];
      s.appendChild(el('line', { x1: scv(v), x2: scv(v), y1: padT, y2: h - padB, stroke: c,
        'stroke-width': 1.4, 'stroke-dasharray': '4 3' }));
      s.appendChild(txt(scv(v) + 4, padT + 10, lab, 'lbl', { fill: c, 'font-size': 9.5 }));
    });
    return s;
  }

  /* ---------------- 11. profil de z-scores ---------------- */
  function zprofile(items, o) {
    o = o || {};
    const w = 620, padL = 168, padR = 60, top = 14, rowH = 24;
    const h = top + items.length * rowH + 22;
    const s = svg(w, h);
    const mid = padL + (w - padL - padR) / 2;
    const half = (w - padL - padR) / 2;
    const maxAbs = Math.max(2, Math.max.apply(null, items.map(i => Math.abs(i.z))));
    s.appendChild(el('line', { class: 'ax', x1: mid, x2: mid, y1: top - 4, y2: h - 20 }));
    [-2, -1, 1, 2].forEach(t => {
      const x = mid + (t / maxAbs) * half;
      s.appendChild(el('line', { class: 'grid', x1: x, x2: x, y1: top - 4, y2: h - 20 }));
      s.appendChild(txt(x, h - 6, (t > 0 ? '+' : '') + t + 'σ', 'lbl', { 'text-anchor': 'middle', 'font-size': 9 }));
    });
    items.forEach((it, i) => {
      const y = top + i * rowH;
      const x = mid + (it.z / maxAbs) * half;
      s.appendChild(txt(padL - 8, y + 14, it.label, 'lbl', { 'text-anchor': 'end' }));
      s.appendChild(el('rect', { x: Math.min(mid, x), y: y + 5, width: Math.max(2, Math.abs(x - mid)),
        height: 12, rx: 3, fill: it.z >= 0 ? '#2fa8c4' : '#e2b04a', opacity: .9 }));
      s.appendChild(txt(x + (it.z >= 0 ? 6 : -6), y + 15,
        (it.z > 0 ? '+' : '') + fmt(it.z, '2') + ' σ  ·  ' + it.raw, 'val',
        { 'text-anchor': it.z >= 0 ? 'start' : 'end', 'font-size': 9.5 }));
    });
    return s;
  }

  /* ---------------- 12. comparaison à une référence ---------------- */
  function compare(items, o) {
    o = o || {};
    const w = 620, padL = 210, padR = 74, top = 14, rowH = 26;
    const h = top + items.length * rowH + 12;
    const s = svg(w, h);
    const max = nice(Math.max.apply(null, items.flatMap(i => [i.v, i.ref])));
    const sc = v => (v / max) * (w - padL - padR);
    items.forEach((it, i) => {
      const y = top + i * rowH;
      s.appendChild(txt(padL - 8, y + 15, it.k, 'lbl', { 'text-anchor': 'end' }));
      s.appendChild(el('rect', { x: padL, y: y + 4, width: Math.max(2, sc(it.v)), height: 9, rx: 2,
        fill: '#e2b04a' }));
      s.appendChild(el('rect', { x: padL, y: y + 15, width: Math.max(2, sc(it.ref)), height: 7, rx: 2,
        fill: '#2fa8c4', opacity: .7 }));
      s.appendChild(txt(padL + Math.max(sc(it.v), sc(it.ref)) + 6, y + 15,
        (it.ecart_pct > 0 ? '+' : '') + fmt(it.ecart_pct, '1') + ' %', 'val',
        { 'font-size': 10, fill: it.ecart_pct > 0 ? '#d8595b' : '#79b36b' }));
    });
    s.appendChild(el('rect', { x: padL, y: 0, width: 9, height: 6, rx: 1, fill: '#e2b04a' }));
    s.appendChild(txt(padL + 13, 6, 'Frontignan', 'lbl', { 'font-size': 9.5 }));
    s.appendChild(el('rect', { x: padL + 82, y: 0, width: 9, height: 6, rx: 1, fill: '#2fa8c4' }));
    s.appendChild(txt(padL + 95, 6, 'moyenne de strate', 'lbl', { 'font-size': 9.5 }));
    return s;
  }

  /* ---------------- 13. matrice de corrélation ---------------- */
  function corrMatrix(keys, labels, values) {
    const n = keys.length, cell = 34, padL = 150, padT = 118;
    const w = padL + n * cell + 16, h = padT + n * cell + 16;
    const s = svg(w, h);
    labels.forEach((lab, i) => {
      s.appendChild(txt(padL - 8, padT + i * cell + cell / 2 + 4, lab, 'lbl',
        { 'text-anchor': 'end', 'font-size': 10 }));
      s.appendChild(txt(0, 0, lab, 'lbl', { 'font-size': 10,
        transform: `translate(${padL + i * cell + cell / 2 + 4},${padT - 8}) rotate(-58)` }));
    });
    for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
      const v = values[i][j];
      const c = v === null ? '#16323a' : (v >= 0
        ? `rgba(47,168,196,${Math.abs(v).toFixed(2)})`
        : `rgba(226,176,74,${Math.abs(v).toFixed(2)})`);
      s.appendChild(el('rect', { x: padL + j * cell, y: padT + i * cell, width: cell - 2, height: cell - 2,
        rx: 3, fill: c, stroke: '#0b1417' }));
      if (v !== null && Math.abs(v) >= 0.3) {
        s.appendChild(txt(padL + j * cell + cell / 2 - 1, padT + i * cell + cell / 2 + 3.5,
          (v > 0 ? '' : '−') + Math.abs(v).toFixed(2).slice(1), 'val',
          { 'text-anchor': 'middle', 'font-size': 9, fill: Math.abs(v) > .6 ? '#04161b' : '#cfe3e8' }));
      }
    }
    return s;
  }

  /* ---------------- 14. barres empilées horizontales (parts) ---------------- */
  function stacked(items, o) {
    o = o || {};
    const w = 620, h = 74;
    const s = svg(w, h);
    const total = items.reduce((a, b) => a + b.v, 0);
    const colors = ['#2fa8c4', '#e2b04a', '#79b36b', '#9b87d4', '#d8595b', '#37c9b0'];
    let x = 0;
    items.forEach((it, i) => {
      const bw = (it.v / total) * w;
      s.appendChild(el('rect', { x, y: 10, width: Math.max(1, bw - 1.5), height: 26, rx: 3,
        fill: colors[i % colors.length], opacity: .9 }));
      if (bw > 44) {
        s.appendChild(txt(x + bw / 2, 27, fmt(it.v, o.fmt || '1') + (o.unit || ' %'), 'val',
          { 'text-anchor': 'middle', 'font-size': 10, fill: '#04161b' }));
      }
      s.appendChild(el('rect', { x, y: 46, width: 8, height: 8, rx: 2, fill: colors[i % colors.length] }));
      s.appendChild(txt(x + 12, 53.5, it.k, 'lbl', { 'font-size': 9.5 }));
      x += bw;
    });
    return s;
  }

  global.Charts = { el, txt, svg, fmt, ranked, box, scatter, line, grouped, donut, quadrant,
    gantt, lorenz, histogram, zprofile, compare, corrMatrix, stacked };
})(window);
