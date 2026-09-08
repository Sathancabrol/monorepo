/* =========================================================================
   atlas.js — Atlas interactif Frontignan
   Trois lectures d'un même graphe : réseau (Obsidian), carte heuristique, slides.
   Zéro dépendance externe.
   ========================================================================= */
(function () {
  'use strict';
  const C = window.Charts;
  const NS = 'http://www.w3.org/2000/svg';
  const $ = s => document.querySelector(s);
  const $$ = s => Array.from(document.querySelectorAll(s));

  function h(tag, attrs, kids) {
    const n = document.createElement(tag);
    if (attrs) for (const k in attrs) {
      if (attrs[k] === null || attrs[k] === undefined) continue;
      if (k === 'class') n.className = attrs[k];
      else if (k === 'html') n.innerHTML = attrs[k];
      else if (k === 'text') n.textContent = attrs[k];
      else if (k.startsWith('on')) n.addEventListener(k.slice(2), attrs[k]);
      else n.setAttribute(k, attrs[k]);
    }
    (kids || []).forEach(k => k && n.appendChild(typeof k === 'string' ? document.createTextNode(k) : k));
    return n;
  }
  function sel(tag, attrs) {
    const n = document.createElementNS(NS, tag);
    if (attrs) for (const k in attrs) if (attrs[k] !== null && attrs[k] !== undefined) n.setAttribute(k, attrs[k]);
    return n;
  }
  const fmt = (v, k) => C.fmt(v, k);

  /* ====================== état ====================== */
  const S = {
    data: null, byId: {}, adj: {},
    mode: 'graph',
    tiers: new Set([0, 1, 2, 3, 4]),
    types: new Set(),
    linkTypes: new Set(),
    layout: 'force',
    selected: null, hovered: null,
    view: { x: 0, y: 0, k: 1 },
    mindView: { x: 0, y: 0, k: 1 },
    mindShape: 'radial', mindRoot: 'frontignan', collapsed: new Set(), mindDepth: 3,
    slide: 0,
    dataset: 'communes', dataVar: 'nvm',
    opts: { images: true, labels: true, edgeLabels: true, charge: 1150, dist: 140,
      mindImages: true, mindFacts: true },
  };
  S.opts.edgeLabels = false;

  const LINK_STYLE = {
    gouverne: { c: '#9b87d4', d: null, lab: 'gouverne' },
    finance: { c: '#e2b04a', d: null, lab: 'finance' },
    dessert: { c: '#2fa8c4', d: '5 4', lab: 'dessert' },
    coopere: { c: '#37c9b0', d: null, lab: 'coopère' },
    tension: { c: '#d8595b', d: '2 4', lab: 'tension' },
    depend: { c: '#7794a0', d: '4 3', lab: 'dépend de' },
    expose: { c: '#d8595b', d: null, lab: 'exposé à' },
    produit: { c: '#79b36b', d: null, lab: 'produit' },
    compose: { c: '#3a6b78', d: null, lab: 'compose' },
  };
  const TYPE_LABEL = {
    territoire: 'Territoire', commune: 'Commune', acteur: 'Acteur', projet: 'Projet',
    risque: 'Risque', politique: 'Politique publique', ressource: 'Ressource',
    futur: 'Prospective', data: 'Données',
  };

  /* ====================== chargement ====================== */
  fetch('data/atlas.json')
    .then(r => { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(init)
    .catch(err => {
      document.body.appendChild(h('div', { class: 'toast',
        text: 'Impossible de charger data/atlas.json (' + err.message +
          ') — ouvrez la page via un serveur HTTP, pas en file://' }));
    });

  function init(data) {
    S.data = data;
    data.nodes.forEach(n => { S.byId[n.id] = n; S.types.add(n.type); });
    Object.keys(LINK_STYLE).forEach(t => S.linkTypes.add(t));
    data.links.forEach(l => {
      (S.adj[l.source] = S.adj[l.source] || []).push({ o: l.target, l, dir: 'out' });
      (S.adj[l.target] = S.adj[l.target] || []).push({ o: l.source, l, dir: 'in' });
    });
    $('#brandSub').textContent = `${data.nodes.length} nœuds · ${data.links.length} liens · ${
      Object.keys(data.datasets).length} jeux de données · INSEE 2023-2026`;
    buildFilters();
    buildGraph();
    buildMindControls();
    buildSlides();
    buildDataView();
    wireGlobal();
    openNode('frontignan', false);
    layoutGraph(true);
  }

  /* ====================== filtres & légende ====================== */
  function buildFilters() {
    const tierNames = S.data.meta.echelles;
    const tf = $('#tierFilters'); tf.innerHTML = '';
    tierNames.forEach((name, i) => {
      const c = h('div', { class: 'chip', 'data-tier': i, onclick: () => {
        S.tiers.has(i) ? S.tiers.delete(i) : S.tiers.add(i);
        c.classList.toggle('off', !S.tiers.has(i));
        applyFilters();
      } }, [h('span', { class: 'sw', style: `background:${['#e2b04a', '#2fa8c4', '#37c9b0', '#79b36b', '#9b87d4'][i]}` }),
        h('span', { text: name })]);
      tf.appendChild(c);
    });
    const yf = $('#typeFilters'); yf.innerHTML = '';
    Object.keys(TYPE_LABEL).forEach(t => {
      const c = h('div', { class: 'chip', onclick: () => {
        S.types.has(t) ? S.types.delete(t) : S.types.add(t);
        c.classList.toggle('off', !S.types.has(t));
        applyFilters();
      } }, [h('span', { class: 'sw', style: `background:${S.data.typeColors[t]}` }),
        h('span', { text: TYPE_LABEL[t] })]);
      yf.appendChild(c);
    });
    const lf = $('#linkFilters'); lf.innerHTML = '';
    Object.keys(LINK_STYLE).forEach(t => {
      const c = h('div', { class: 'chip', onclick: () => {
        S.linkTypes.has(t) ? S.linkTypes.delete(t) : S.linkTypes.add(t);
        c.classList.toggle('off', !S.linkTypes.has(t));
        applyFilters();
      } }, [h('span', { class: 'sw', style: `background:${LINK_STYLE[t].c}` }),
        h('span', { text: LINK_STYLE[t].lab })]);
      lf.appendChild(c);
    });
    const lg = html => { $('#legend').innerHTML = html; $('#legendMind').innerHTML = html; };
    lg('<h3>Lecture</h3>' + Object.keys(LINK_STYLE).map(t =>
      `<div class="lg"><i style="background:${LINK_STYLE[t].c}"></i>${LINK_STYLE[t].lab}</div>`).join('') +
      '<div class="lg" style="margin-top:10px;color:#7794a0">Taille du nœud = nombre de liens</div>');
  }

  function visibleNode(n) { return S.tiers.has(n.tier) && S.types.has(n.type); }
  function visibleLink(l) {
    return S.linkTypes.has(l.type) && visibleNode(S.byId[l.source]) && visibleNode(S.byId[l.target]);
  }

  /* ====================== GRAPHE ====================== */
  const G = { svg: null, root: null, gLinks: null, gLabels: null, gNodes: null, nodes: [], links: [],
    sim: null, raf: null, alpha: 1, W: 1200, H: 800 };

  function buildGraph() {
    G.svg = $('#graph');
    G.svg.innerHTML = '';
    const defs = sel('defs');
    G.svg.appendChild(defs);
    G.defs = defs;
    G.root = sel('g', { id: 'gr-root' });
    G.svg.appendChild(G.root);
    G.gRings = sel('g'); G.root.appendChild(G.gRings);
    G.gLinks = sel('g', { 'stroke-linecap': 'round' }); G.root.appendChild(G.gLinks);
    G.gEdgeLabels = sel('g'); G.root.appendChild(G.gEdgeLabels);
    G.gNodes = sel('g'); G.root.appendChild(G.gNodes);

    G.nodes = S.data.nodes.map(n => Object.assign({}, n, {
      x: 0, y: 0, vx: 0, vy: 0,
      r: Math.min(34, 13 + Math.sqrt(n.degree || 1) * 4.2) * (n.tier === 0 ? 1.7 : 1),
    }));
    G.map = {}; G.nodes.forEach(n => G.map[n.id] = n);
    G.links = S.data.links.map(l => Object.assign({}, l, { s: G.map[l.source], t: G.map[l.target] }));

    // placement initial : anneaux par échelle
    const byTier = {};
    G.nodes.forEach(n => (byTier[n.tier] = byTier[n.tier] || []).push(n));
    Object.keys(byTier).forEach(tier => {
      const arr = byTier[tier], R = [0, 210, 420, 620, 800][tier] || 300;
      arr.forEach((n, i) => {
        const a = (i / arr.length) * Math.PI * 2 + tier;
        n.x = Math.cos(a) * R + (Math.random() - .5) * 40;
        n.y = Math.sin(a) * R * .78 + (Math.random() - .5) * 40;
      });
    });

    renderGraphElements();
    wireGraphInteraction();
    startSim(1);
  }

  function renderGraphElements() {
    G.gLinks.innerHTML = ''; G.gNodes.innerHTML = ''; G.gEdgeLabels.innerHTML = '';
    G.defs.innerHTML = '';

    G.links.forEach(l => {
      const st = LINK_STYLE[l.type] || LINK_STYLE.compose;
      l.el = sel('line', { class: 'link', stroke: st.c, 'stroke-width': 0.7 + l.weight * 0.32,
        'stroke-opacity': .38, 'stroke-dasharray': st.d });
      G.gLinks.appendChild(l.el);
      if (l.label) {
        l.lab = sel('text', { class: 'linklabel' });
        l.lab.textContent = l.label;
        G.gEdgeLabels.appendChild(l.lab);
      }
    });

    G.nodes.forEach(n => {
      const g = sel('g', { class: 'node', 'data-id': n.id });
      n.el = g;
      const r = n.r;
      g.appendChild(sel('circle', { class: 'halo', r: r + 9, fill: 'none', stroke: n.color,
        'stroke-width': 2, 'stroke-opacity': .5 }));
      g.appendChild(sel('circle', { class: 'bg', r: r, fill: '#0d1f25', stroke: n.color,
        'stroke-width': n.tier === 0 ? 3 : 1.8, 'stroke-opacity': .95 }));
      if (n.img) {
        const cid = 'clip-' + n.id;
        const cp = sel('clipPath', { id: cid });
        cp.appendChild(sel('circle', { r: r - 2.5 }));
        G.defs.appendChild(cp);
        const im = sel('image', { href: n.img, x: -(r - 2.5), y: -(r - 2.5), width: (r - 2.5) * 2,
          height: (r - 2.5) * 2, preserveAspectRatio: 'xMidYMid slice', 'clip-path': `url(#${cid})`,
          opacity: .92 });
        im.setAttributeNS('http://www.w3.org/1999/xlink', 'href', n.img);
        g.appendChild(im);
        n.imgEl = im;
      } else {
        const t = sel('text', { 'text-anchor': 'middle', y: r * 0.36, 'font-size': r * 0.95 });
        t.textContent = n.icon || '•';
        g.appendChild(t);
        n.iconEl = t;
      }
      const lbl = sel('text', { class: 'lbl', y: r + 15 });
      lbl.textContent = n.label;
      g.appendChild(lbl); n.lblEl = lbl;
      if (n.acteur) {
        const s2 = sel('text', { class: 'sublbl', y: r + 26 });
        s2.textContent = n.famille;
        g.appendChild(s2); n.subEl = s2;
      }
      G.gNodes.appendChild(g);
    });
    applyFilters();
  }

  function applyFilters() {
    if (!G.nodes) return;
    G.nodes.forEach(n => {
      const v = visibleNode(n);
      n.hidden = !v;
      if (n.el) n.el.style.display = v ? '' : 'none';
      if (n.lblEl) n.lblEl.style.display = S.opts.labels ? '' : 'none';
      if (n.imgEl) n.imgEl.style.display = S.opts.images ? '' : 'none';
      if (n.imgEl && !S.opts.images && !n.iconEl) { /* rien */ }
    });
    G.links.forEach(l => {
      const v = visibleLink(l);
      l.hidden = !v;
      if (l.el) l.el.style.display = v ? '' : 'none';
      if (l.lab) l.lab.style.display = (v && S.opts.edgeLabels) ? '' : 'none';
    });
    const nv = G.nodes.filter(n => !n.hidden).length, lv = G.links.filter(l => !l.hidden).length;
    $('#graphMeta').textContent = `${nv} nœuds · ${lv} liens affichés · glisser pour déplacer, molette pour zoomer`;
    startSim(0.35);
  }

  /* ---- simulation de forces (Verlet amortie, O(n²) assumé pour ~80 nœuds) ---- */
  function startSim(alpha) {
    G.alpha = Math.max(G.alpha || 0, alpha);
    if (!G.raf) tick();
  }
  function tick() {
    const nodes = G.nodes.filter(n => !n.hidden);
    const links = G.links.filter(l => !l.hidden);
    const k = S.opts.charge, dist = S.opts.dist;
    // répulsion
    for (let i = 0; i < nodes.length; i++) {
      const a = nodes[i];
      for (let j = i + 1; j < nodes.length; j++) {
        const b = nodes[j];
        let dx = b.x - a.x, dy = b.y - a.y;
        let d2 = dx * dx + dy * dy;
        if (d2 < 1) { d2 = 1; dx = (Math.random() - .5); dy = (Math.random() - .5); }
        const d = Math.sqrt(d2);
        const minD = a.r + b.r + 14;
        let f = k / d2;
        if (d < minD) f += (minD - d) * 0.045;      // collision douce
        const fx = (dx / d) * f, fy = (dy / d) * f;
        a.vx -= fx; a.vy -= fy; b.vx += fx; b.vy += fy;
      }
    }
    // ressorts
    links.forEach(l => {
      const a = l.s, b = l.t;
      const dx = b.x - a.x, dy = b.y - a.y;
      const d = Math.sqrt(dx * dx + dy * dy) || 1;
      const target = dist + (a.r + b.r) * 0.9 - l.weight * 6;
      const f = (d - target) * 0.012 * (0.5 + l.weight * 0.14);
      const fx = (dx / d) * f, fy = (dy / d) * f;
      a.vx += fx; a.vy += fy; b.vx -= fx; b.vy -= fy;
    });
    // forces de disposition
    nodes.forEach(n => {
      if (S.layout === 'rings') {
        const R = [0, 250, 470, 660, 830][n.tier] || 300;
        const d = Math.sqrt(n.x * n.x + n.y * n.y) || 1;
        const f = (d - R) * 0.035;
        n.vx -= (n.x / d) * f; n.vy -= (n.y / d) * f;
        n.vx -= n.x * 0.0004; n.vy -= n.y * 0.0004;
      } else if (S.layout === 'cluster') {
        const types = Object.keys(TYPE_LABEL);
        const i = types.indexOf(n.type);
        const a = (i / types.length) * Math.PI * 2;
        const cx = Math.cos(a) * 470, cy = Math.sin(a) * 370;
        n.vx += (cx - n.x) * 0.006; n.vy += (cy - n.y) * 0.006;
      } else {
        n.vx -= n.x * 0.0016; n.vy -= n.y * 0.0016;
        if (n.tier === 0) { n.vx -= n.x * 0.03; n.vy -= n.y * 0.03; }
      }
      if (n.fixed) { n.vx = 0; n.vy = 0; }
    });
    // intégration
    const damp = 0.82;
    nodes.forEach(n => {
      if (n.fixed) return;
      n.vx *= damp; n.vy *= damp;
      const max = 18;
      n.vx = Math.max(-max, Math.min(max, n.vx));
      n.vy = Math.max(-max, Math.min(max, n.vy));
      n.x += n.vx * G.alpha; n.y += n.vy * G.alpha;
    });
    drawGraph();
    G.alpha *= 0.988;
    if (G.alpha > 0.02) G.raf = requestAnimationFrame(tick);
    else { G.raf = null; G.alpha = 0; }
  }

  function drawGraph() {
    G.nodes.forEach(n => { if (!n.hidden) n.el.setAttribute('transform', `translate(${n.x.toFixed(1)},${n.y.toFixed(1)})`); });
    G.links.forEach(l => {
      if (l.hidden) return;
      l.el.setAttribute('x1', l.s.x); l.el.setAttribute('y1', l.s.y);
      l.el.setAttribute('x2', l.t.x); l.el.setAttribute('y2', l.t.y);
      if (l.lab && S.opts.edgeLabels) {
        l.lab.setAttribute('x', (l.s.x + l.t.x) / 2);
        l.lab.setAttribute('y', (l.s.y + l.t.y) / 2 - 3);
      }
    });
  }

  function applyView() {
    G.root.setAttribute('transform', `translate(${S.view.x},${S.view.y}) scale(${S.view.k})`);
  }
  function fitGraph() {
    const nodes = G.nodes.filter(n => !n.hidden);
    if (!nodes.length) return;
    const xs = nodes.map(n => n.x), ys = nodes.map(n => n.y);
    const minX = Math.min.apply(null, xs) - 90, maxX = Math.max.apply(null, xs) + 90;
    const minY = Math.min.apply(null, ys) - 90, maxY = Math.max.apply(null, ys) + 90;
    const r = G.svg.getBoundingClientRect();
    const k = Math.min(r.width / (maxX - minX), r.height / (maxY - minY), 1.5);
    S.view.k = k;
    S.view.x = r.width / 2 - ((minX + maxX) / 2) * k;
    S.view.y = r.height / 2 - ((minY + maxY) / 2) * k;
    applyView();
  }
  function layoutGraph(fit) { startSim(1); if (fit) setTimeout(fitGraph, 700); }

  function wireGraphInteraction() {
    const svgEl = G.svg;
    let panning = false, dragNode = null, last = null;

    svgEl.addEventListener('pointerdown', e => {
      const g = e.target.closest ? e.target.closest('.node') : null;
      last = { x: e.clientX, y: e.clientY };
      if (g) {
        dragNode = G.map[g.getAttribute('data-id')];
        dragNode.fixed = true;
        svgEl.setPointerCapture(e.pointerId);
      } else {
        panning = true; svgEl.classList.add('dragging');
        svgEl.setPointerCapture(e.pointerId);
      }
    });
    svgEl.addEventListener('pointermove', e => {
      const g = e.target.closest ? e.target.closest('.node') : null;
      if (!dragNode && !panning) {
        const id = g && g.getAttribute('data-id');
        if (id !== S.hovered) { S.hovered = id; highlight(id); showTip(id, e); }
        else if (id) showTip(id, e);
        return;
      }
      if (!last) return;
      const dx = e.clientX - last.x, dy = e.clientY - last.y;
      last = { x: e.clientX, y: e.clientY };
      if (dragNode) {
        dragNode.x += dx / S.view.k; dragNode.y += dy / S.view.k;
        dragNode.moved = (dragNode.moved || 0) + Math.abs(dx) + Math.abs(dy);
        drawGraph(); startSim(0.25);
      } else if (panning) {
        S.view.x += dx; S.view.y += dy; applyView();
      }
    });
    const end = e => {
      if (dragNode) {
        if ((dragNode.moved || 0) < 4) openNode(dragNode.id);
        dragNode.fixed = false; dragNode.moved = 0; dragNode = null; startSim(0.3);
      }
      panning = false; last = null; svgEl.classList.remove('dragging');
    };
    svgEl.addEventListener('pointerup', end);
    svgEl.addEventListener('pointercancel', end);
    svgEl.addEventListener('pointerleave', () => { $('#graphTip').hidden = true; S.hovered = null; highlight(null); });
    svgEl.addEventListener('wheel', e => {
      e.preventDefault();
      const r = svgEl.getBoundingClientRect();
      const mx = e.clientX - r.left, my = e.clientY - r.top;
      const f = e.deltaY < 0 ? 1.12 : 1 / 1.12;
      const nk = Math.max(0.18, Math.min(3.4, S.view.k * f));
      S.view.x = mx - (mx - S.view.x) * (nk / S.view.k);
      S.view.y = my - (my - S.view.y) * (nk / S.view.k);
      S.view.k = nk; applyView();
    }, { passive: false });

    $('#zoomIn').onclick = () => { S.view.k = Math.min(3.4, S.view.k * 1.25); applyView(); };
    $('#zoomOut').onclick = () => { S.view.k = Math.max(0.18, S.view.k / 1.25); applyView(); };
    $('#zoomFit').onclick = fitGraph;
    $('#btnReheat').onclick = () => { startSim(1); };
    $$('#layoutSeg button').forEach(b => b.onclick = () => {
      $$('#layoutSeg button').forEach(x => x.classList.remove('is-on'));
      b.classList.add('is-on'); S.layout = b.dataset.layout; drawRings(); startSim(1);
      setTimeout(fitGraph, 800);
    });
    $('#optImages').onchange = e => { S.opts.images = e.target.checked; applyFilters(); };
    $('#optLabels').onchange = e => { S.opts.labels = e.target.checked; applyFilters(); };
    $('#optEdgeLabels').onchange = e => { S.opts.edgeLabels = e.target.checked; applyFilters(); };
    $('#optCharge').oninput = e => { S.opts.charge = +e.target.value; startSim(0.6); };
    $('#optDist').oninput = e => { S.opts.dist = +e.target.value; startSim(0.6); };
    drawRings();
  }

  function drawRings() {
    G.gRings.innerHTML = '';
    if (S.layout !== 'rings') return;
    const R = [0, 250, 470, 660, 830];
    S.data.meta.echelles.forEach((name, i) => {
      if (!i) return;
      G.gRings.appendChild(sel('circle', { r: R[i], fill: 'none', stroke: '#1b3640',
        'stroke-dasharray': '3 7' }));
      const t = sel('text', { class: 'ring-label', x: 0, y: -R[i] - 10, 'text-anchor': 'middle' });
      t.textContent = name;
      G.gRings.appendChild(t);
    });
  }

  function highlight(id) {
    if (!id) {
      G.nodes.forEach(n => n.el.classList.remove('hi', 'dim'));
      G.links.forEach(l => { l.el.setAttribute('stroke-opacity', .38); l.el.classList.remove('dim'); });
      return;
    }
    const near = new Set([id]);
    (S.adj[id] || []).forEach(a => near.add(a.o));
    G.nodes.forEach(n => {
      n.el.classList.toggle('hi', near.has(n.id));
      n.el.classList.toggle('dim', !near.has(n.id));
    });
    G.links.forEach(l => {
      const on = l.source === id || l.target === id;
      l.el.setAttribute('stroke-opacity', on ? .95 : .07);
      if (l.lab) l.lab.style.opacity = on ? 1 : .1;
    });
  }

  function showTip(id, e) {
    const tip = $('#graphTip');
    if (!id) { tip.hidden = true; return; }
    const n = S.byId[id];
    const facts = (n.facts || []).slice(0, 3)
      .map(f => `<div><span class="k">${f.k} :</span> ${f.v}</div>`).join('');
    tip.innerHTML = `<b>${n.label}</b><div class="k">${TYPE_LABEL[n.type]} · ${n.tierLabel}</div>` +
      (n.sub ? `<div style="margin:4px 0 6px">${n.sub}</div>` : '') + facts +
      `<div class="k" style="margin-top:6px">${(S.adj[id] || []).length} liens — cliquer pour ouvrir</div>`;
    tip.hidden = false;
    const r = G.svg.getBoundingClientRect();
    let x = e.clientX - r.left + 16, y = e.clientY - r.top + 14;
    if (x + 300 > r.width) x -= 320;
    if (y + 160 > r.height) y -= 170;
    tip.style.left = x + 'px'; tip.style.top = y + 'px';
  }

  /* ====================== CARTE HEURISTIQUE ====================== */
  const M = { svg: null, root: null };
  function buildMindControls() {
    M.svg = $('#mind');
    const rootSel = $('#mindRoot');
    const candidates = S.data.nodes.filter(n => (n.children || []).length).sort((a, b) => a.label.localeCompare(b.label));
    candidates.forEach(n => rootSel.appendChild(h('option', { value: n.id, text: n.label })));
    rootSel.value = 'frontignan';
    rootSel.onchange = () => { S.mindRoot = rootSel.value; drawMind(); };
    $$('#mindSeg button').forEach(b => b.onclick = () => {
      $$('#mindSeg button').forEach(x => x.classList.remove('is-on'));
      b.classList.add('is-on'); S.mindShape = b.dataset.mind; drawMind();
    });
    $('#mindDepth').oninput = e => { S.mindDepth = +e.target.value; drawMind(); };
    $('#mindExpand').onclick = () => { S.collapsed.clear(); drawMind(); };
    $('#mindCollapse').onclick = () => {
      S.collapsed.clear();
      const root = S.byId[S.mindRoot];
      (root.children || []).forEach(c => S.collapsed.add(c));
      drawMind();
    };
    $('#mindImages').onchange = e => { S.opts.mindImages = e.target.checked; drawMind(); };
    $('#mindFacts').onchange = e => { S.opts.mindFacts = e.target.checked; drawMind(); };
    $('#mZoomIn').onclick = () => { S.mindView.k *= 1.2; applyMindView(); };
    $('#mZoomOut').onclick = () => { S.mindView.k /= 1.2; applyMindView(); };
    $('#mZoomFit').onclick = () => drawMind();

    let panning = false, last = null;
    M.svg.addEventListener('pointerdown', e => {
      if (e.target.closest && e.target.closest('.node')) return;
      panning = true; last = { x: e.clientX, y: e.clientY }; M.svg.classList.add('dragging');
      M.svg.setPointerCapture(e.pointerId);
    });
    M.svg.addEventListener('pointermove', e => {
      if (!panning || !last) return;
      S.mindView.x += e.clientX - last.x; S.mindView.y += e.clientY - last.y;
      last = { x: e.clientX, y: e.clientY }; applyMindView();
    });
    ['pointerup', 'pointercancel', 'pointerleave'].forEach(ev =>
      M.svg.addEventListener(ev, () => { panning = false; last = null; M.svg.classList.remove('dragging'); }));
    M.svg.addEventListener('wheel', e => {
      e.preventDefault();
      const r = M.svg.getBoundingClientRect();
      const mx = e.clientX - r.left, my = e.clientY - r.top;
      const f = e.deltaY < 0 ? 1.12 : 1 / 1.12;
      const nk = Math.max(0.2, Math.min(3, S.mindView.k * f));
      S.mindView.x = mx - (mx - S.mindView.x) * (nk / S.mindView.k);
      S.mindView.y = my - (my - S.mindView.y) * (nk / S.mindView.k);
      S.mindView.k = nk; applyMindView();
    }, { passive: false });
  }
  function applyMindView() {
    if (M.root) M.root.setAttribute('transform',
      `translate(${S.mindView.x},${S.mindView.y}) scale(${S.mindView.k})`);
  }

  function mindTree(id, depth) {
    const n = S.byId[id];
    const node = { id, n, depth, children: [] };
    if (depth >= S.mindDepth || S.collapsed.has(id)) { node.folded = (n.children || []).length > 0; return node; }
    (n.children || []).forEach(c => {
      if (!visibleNode(S.byId[c])) return;
      node.children.push(mindTree(c, depth + 1));
    });
    return node;
  }

  function drawMind() {
    if (!M.svg) return;
    M.svg.innerHTML = '';
    const defs = sel('defs'); M.svg.appendChild(defs);
    M.root = sel('g'); M.svg.appendChild(M.root);
    const gL = sel('g'); const gN = sel('g');
    M.root.appendChild(gL); M.root.appendChild(gN);
    const tree = mindTree(S.mindRoot, 0);

    // 1. positions
    let leafIndex = 0;
    const leaves = [];
    (function count(t) {
      if (!t.children.length) { t.leaf = leafIndex++; leaves.push(t); return 1; }
      let s = 0; t.children.forEach(c => s += count(c));
      t.leaf = (t.children[0].leaf + t.children[t.children.length - 1].leaf) / 2;
      return s;
    })(tree);
    const nLeaves = Math.max(1, leafIndex);
    const radial = S.mindShape === 'radial';
    const rect = M.svg.getBoundingClientRect();
    const maxR = Math.min(rect.width, rect.height) * 0.42;

    (function place(t) {
      if (radial) {
        const a = (t.leaf / nLeaves) * Math.PI * 2 - Math.PI / 2;
        const r = t.depth * (maxR / Math.max(1, S.mindDepth)) * 1.15;
        t.x = Math.cos(a) * r; t.y = Math.sin(a) * r; t.a = a;
      } else {
        t.x = t.depth * 260;
        t.y = t.leaf * 62 - (nLeaves * 62) / 2;
      }
      t.children.forEach(place);
    })(tree);

    // 2. liens
    (function links(t) {
      t.children.forEach(c => {
        const d = radial
          ? `M${t.x},${t.y} C${t.x + (c.x - t.x) * .45},${t.y + (c.y - t.y) * .1} ${
            t.x + (c.x - t.x) * .55},${c.y} ${c.x},${c.y}`
          : `M${t.x},${t.y} C${t.x + 90},${t.y} ${c.x - 90},${c.y} ${c.x},${c.y}`;
        gL.appendChild(sel('path', { d, fill: 'none', stroke: c.n.color, 'stroke-opacity': .38,
          'stroke-width': Math.max(1, 3.4 - c.depth * 0.7) }));
        links(c);
      });
    })(tree);

    // 3. nœuds
    (function nodes(t) {
      const n = t.n;
      const r = t.depth === 0 ? 44 : Math.max(15, 34 - t.depth * 6);
      const g = sel('g', { class: 'node', 'data-id': n.id, transform: `translate(${t.x},${t.y})` });
      g.appendChild(sel('circle', { class: 'halo', r: r + 7, fill: 'none', stroke: n.color, 'stroke-opacity': .45 }));
      g.appendChild(sel('circle', { r, fill: '#0d1f25', stroke: n.color, 'stroke-width': t.depth === 0 ? 3 : 2 }));
      if (n.img && S.opts.mindImages) {
        const cid = 'mclip-' + n.id;
        const cp = sel('clipPath', { id: cid });
        cp.appendChild(sel('circle', { r: r - 2.5 }));
        defs.appendChild(cp);
        const im = sel('image', { x: -(r - 2.5), y: -(r - 2.5), width: (r - 2.5) * 2, height: (r - 2.5) * 2,
          preserveAspectRatio: 'xMidYMid slice', 'clip-path': `url(#${cid})`, opacity: .92, href: n.img });
        im.setAttributeNS('http://www.w3.org/1999/xlink', 'href', n.img);
        g.appendChild(im);
      } else {
        const ic = sel('text', { 'text-anchor': 'middle', y: r * .34, 'font-size': r * .9 });
        ic.textContent = n.icon || '•';
        g.appendChild(ic);
      }
      if (t.folded) {
        g.appendChild(sel('circle', { cx: r * .72, cy: -r * .72, r: 8, fill: '#e2b04a' }));
        const p = sel('text', { x: r * .72, y: -r * .72 + 3.5, 'text-anchor': 'middle', 'font-size': 11,
          fill: '#06171b', 'font-weight': 700 });
        p.textContent = (S.byId[n.id].children || []).length;
        g.appendChild(p);
      }
      const right = radial ? Math.cos(t.a || 0) >= -0.001 : true;
      const lx = t.depth === 0 ? 0 : (right ? r + 9 : -(r + 9));
      const anchor = t.depth === 0 ? 'middle' : (right ? 'start' : 'end');
      const ly = t.depth === 0 ? r + 20 : 4;
      const lbl = sel('text', { class: 'lbl', x: lx, y: ly, 'text-anchor': anchor,
        'font-size': t.depth === 0 ? 14 : Math.max(10, 13 - t.depth) });
      lbl.textContent = n.label;
      g.appendChild(lbl);
      if (S.opts.mindFacts && n.facts && n.facts.length && t.depth > 0) {
        const s2 = sel('text', { class: 'sublbl', x: lx, y: ly + 12, 'text-anchor': anchor });
        s2.textContent = n.facts[0].k + ' : ' + n.facts[0].v;
        g.appendChild(s2);
      }
      g.addEventListener('click', ev => {
        ev.stopPropagation();
        if ((S.byId[n.id].children || []).length && ev.shiftKey === false && t.depth > 0) {
          S.collapsed.has(n.id) ? S.collapsed.delete(n.id) : S.collapsed.add(n.id);
          drawMind();
        }
        openNode(n.id);
      });
      g.addEventListener('dblclick', ev => {
        ev.stopPropagation();
        if ((S.byId[n.id].children || []).length) {
          S.mindRoot = n.id; $('#mindRoot').value = n.id; S.collapsed.clear(); drawMind();
        }
      });
      gN.appendChild(g);
      t.children.forEach(nodes);
    })(tree);

    // 4. cadrage
    const bb = M.root.getBBox();
    const k = Math.min(rect.width / (bb.width + 180), rect.height / (bb.height + 140), 1.35);
    S.mindView.k = k;
    S.mindView.x = rect.width / 2 - (bb.x + bb.width / 2) * k;
    S.mindView.y = rect.height / 2 - (bb.y + bb.height / 2) * k;
    applyMindView();
  }

  /* ====================== PANNEAU ====================== */
  function openNode(id, scroll) {
    const n = S.byId[id];
    if (!n) return;
    S.selected = id;
    G.nodes && G.nodes.forEach(x => x.el && x.el.classList.toggle('sel', x.id === id));
    const p = $('#panel'), body = $('#panelBody');
    p.hidden = false;
    body.innerHTML = '';

    const hero = h('div', { class: 'p-hero' });
    if (n.img) hero.appendChild(h('img', { src: n.img, alt: n.label, loading: 'lazy' }));
    else hero.appendChild(h('div', { class: 'glyph', text: n.icon || '◈',
      style: `background:linear-gradient(140deg,${n.color}33,transparent)` }));
    body.appendChild(hero);

    const head = h('div', { class: 'p-head' }, [
      h('div', { class: 'p-badges' }, [
        h('span', { class: 'badge type', text: TYPE_LABEL[n.type] || n.type,
          style: `background:${n.color}` }),
        h('span', { class: 'badge', text: n.tierLabel }),
        h('span', { class: 'badge', text: (S.adj[id] || []).length + ' liens' }),
      ]),
      h('h2', { text: n.label }),
      n.sub ? h('p', { class: 'sub', text: n.sub }) : null,
    ]);
    body.appendChild(head);

    const b = h('div', { class: 'p-body' });
    if (n.txt) b.appendChild(h('p', { class: 'txt', text: n.txt }));
    if (n.facts && n.facts.length) {
      b.appendChild(h('div', { class: 'facts' },
        n.facts.map(f => h('div', { class: 'fact' }, [
          h('div', { class: 'k', text: f.k }), h('div', { class: 'v', text: String(f.v) })]))));
    }
    if (n.bul && n.bul.length) {
      b.appendChild(h('h4', { class: 'sec', text: 'Ce qu\'il faut en retenir' }));
      b.appendChild(h('ul', { class: 'bul' }, n.bul.map(x => h('li', { text: x }))));
    }
    if (n.data && S.data.datasets[n.data]) {
      b.appendChild(h('h4', { class: 'sec', text: 'Données & statistiques' }));
      renderDataset(b, n.data, { compact: true, focusVar: defaultVarFor(n) });
    }
    // relations
    const rel = (S.adj[id] || []).slice().sort((a, b) => b.l.weight - a.l.weight);
    if (rel.length) {
      b.appendChild(h('h4', { class: 'sec', text: `Connexions (${rel.length})` }));
      const box = h('div', { class: 'rel' });
      rel.forEach(a => {
        const o = S.byId[a.o];
        const st = LINK_STYLE[a.l.type] || LINK_STYLE.compose;
        box.appendChild(h('a', { onclick: () => { openNode(a.o); focusNode(a.o); } }, [
          h('span', { class: 'rdot', style: `background:${o.color}` }),
          h('span', { text: o.label }),
          h('span', { class: 'rtype', text: (a.dir === 'out' ? '→ ' : '← ') + (a.l.label || st.lab) }),
        ]));
      });
      b.appendChild(box);
    }
    if (n.src && n.src.length) {
      b.appendChild(h('h4', { class: 'sec', text: 'Sources' }));
      n.src.forEach(s => b.appendChild(h('div', { class: 'src', html:
        `<a href="${s.u}" target="_blank" rel="noopener">${s.t}</a> — ${s.d}` })));
    }
    body.appendChild(b);
    if (scroll !== false) body.scrollTop = 0;
  }

  function defaultVarFor(n) {
    if (n.id === 'revenus') return 'nvm';
    if (n.id === 'emploi') return 'tcho';
    if (n.type === 'commune' || n.id === 'sam') return 'pop';
    return null;
  }
  function focusNode(id) {
    const n = G.map[id];
    if (!n || S.mode !== 'graph') return;
    const r = G.svg.getBoundingClientRect();
    S.view.k = Math.max(S.view.k, 0.85);
    S.view.x = r.width / 2 - n.x * S.view.k;
    S.view.y = r.height / 2 - n.y * S.view.k;
    applyView();
    highlight(id);
  }

  /* ====================== RENDU DES JEUX DE DONNÉES ====================== */
  function statGrid(st, o) {
    o = o || {};
    const f = o.fmt || '1';
    const items = [
      ['n', fmt(st.n, 'int')], ['moyenne', fmt(st.moyenne, f)], ['médiane', fmt(st.mediane, f)],
      ['écart-type σ', fmt(st.ecart_type, f)], ['CV', fmt(st.cv, '1') + ' %'],
      ['étendue R', fmt(st.etendue, f)], ['min', fmt(st.min, f)], ['max', fmt(st.max, f)],
      ['Q1', fmt(st.q1, f)], ['Q3', fmt(st.q3, f)], ['IQR', fmt(st.iqr, f)],
      ['asymétrie', fmt(st.asymetrie, '2')],
    ];
    if (st.moyenne_ponderee !== undefined) items.push(['moy. pondérée', fmt(st.moyenne_ponderee, f)]);
    if (st.ic95_bas !== undefined) items.push(['IC 95 % de la moyenne', fmt(st.ic95_bas, f) + ' – ' + fmt(st.ic95_haut, f)]);
    const g = h('div', { class: 'statgrid' }, items.map(([k, v]) =>
      h('div', { class: 'stat' }, [h('div', { class: 'k', text: k }), h('div', { class: 'v', text: v })])));
    if (st.frontignan !== undefined) {
      g.appendChild(h('div', { class: 'stat hl' }, [
        h('div', { class: 'k', text: 'Frontignan' }),
        h('div', { class: 'v', text: fmt(st.frontignan, f) })]));
      g.appendChild(h('div', { class: 'stat hl' }, [
        h('div', { class: 'k', text: 'z-score' }),
        h('div', { class: 'v', text: (st.z_frontignan > 0 ? '+' : '') + fmt(st.z_frontignan, '2') + ' σ' })]));
      g.appendChild(h('div', { class: 'stat hl' }, [
        h('div', { class: 'k', text: 'rang' }),
        h('div', { class: 'v', text: st.rang_frontignan + ' / ' + st.rang_sur })]));
    }
    return g;
  }

  function wrapChart(title, sub, svgEl) {
    return h('div', { class: 'chart-wrap' }, [
      title ? h('div', { class: 'chart-title', text: title }) : null,
      sub ? h('p', { class: 'chart-sub', text: sub }) : null,
      svgEl,
    ]);
  }

  function renderDataset(container, key, o) {
    o = o || {};
    const d = S.data.datasets[key];
    if (!d) return;
    const compact = !!o.compact;

    if (key === 'communes') {
      const varKey = o.focusVar || S.dataVar || 'nvm';
      const field = d.fields.find(f => f.key === varKey) || d.fields[1];
      const st = d.stats[field.key];
      const rows = d.rows.map(r => ({ label: r.nom, value: r[field.key], me: r.code === '34108' }));
      container.appendChild(h('p', { class: 'note', text: d.note }));
      container.appendChild(statGrid(st, { fmt: field.fmt }));
      container.appendChild(wrapChart(
        field.label + (field.unit ? ' (' + field.unit + ')' : ''),
        'Bande claire = moyenne ± 1 écart-type · trait or = médiane · trait vert = moyenne',
        C.ranked(rows, { stats: st, fmt: field.fmt, unit: '' })));
      container.appendChild(wrapChart('Distribution (boîte à moustaches)',
        `n = ${st.n} · IQR = ${fmt(st.iqr, field.fmt)} · étendue R = ${fmt(st.etendue, field.fmt)}` +
        (st.n_atypiques ? ` · ${st.n_atypiques} valeur(s) atypique(s) au sens de Tukey` : ''),
        C.box(st, { points: rows, fmt: field.fmt })));
      if (!compact) {
        container.appendChild(wrapChart('Histogramme',
          'Répartition des 14 communes ; racine carrée du nombre d’observations pour le nombre de classes',
          C.histogram(rows.map(r => r.value).filter(v => v !== null), st, { fmt: field.fmt })));
        const fro = d.rows.find(r => r.code === '34108');
        container.appendChild(wrapChart('Profil normalisé de Frontignan (z-scores)',
          'Écart à la moyenne intercommunale, exprimé en écarts-types',
          C.zprofile(Object.keys(fro.z).map(k => {
            const f2 = d.fields.find(x => x.key === k) || { label: k, fmt: '1' };
            return { label: f2.label, z: fro.z[k], raw: fmt(fro[k], f2.fmt) };
          }))));
        d.correlations.forEach(cr => {
          const fx = d.fields.find(f => f.key === cr.x), fy = d.fields.find(f => f.key === cr.y);
          if (Math.abs(cr.r) < 0.35) return;
          container.appendChild(wrapChart(cr.label,
            `Pearson r = ${fmt(cr.r, '3')} · R² = ${fmt(cr.r2, '3')} · Spearman ρ = ${fmt(cr.rho, '3')}` +
            ` · ${cr.significatif ? 'liaison significative (|t| > 2,16)' : 'liaison non significative'}`,
            C.scatter(d.rows.map(r => ({ x: r[cr.x], y: r[cr.y], label: r.nom, me: r.code === '34108' })),
              { fit: cr, rho: cr.rho, xfmt: fx.fmt, yfmt: fy.fmt, xlabel: fx.label, ylabel: fy.label,
                labelAll: true })));
        });
        container.appendChild(wrapChart('Matrice de corrélation (Pearson)',
          'Bleu = corrélation positive, or = corrélation négative ; intensité proportionnelle à |r|',
          C.corrMatrix(d.matrix.keys, d.matrix.labels, d.matrix.values)));
        container.appendChild(wrapChart('Concentration de la population (courbe de Lorenz)',
          `Indice de Gini = ${fmt(d.concentration.gini_population, '3')} pour la population et ` +
          `${fmt(d.concentration.gini_emplois, '3')} pour les emplois : le bassin est très polarisé par Sète.`,
          C.lorenz(d.concentration.lorenz, d.concentration.gini_population)));
        container.appendChild(dataTable(d));
      }
      return;
    }

    if (key === 'echelles') {
      const rows = d.rows;
      container.appendChild(wrapChart('Croissance annuelle moyenne 2017-2023',
        'Le bassin de Thau croît deux fois moins vite que la métropole voisine',
        C.ranked(rows.map(r => ({ label: r.nom, value: r.tvam, me: r.id === 'frontignan' })),
          { fmt: '2', unit: '%/an' })));
      container.appendChild(wrapChart('Niveau de vie médian (€/UC, Filosofi 2023)',
        'Frontignan se situe 5,2 % sous la France métropolitaine et au-dessus de son agglomération',
        C.ranked(rows.map(r => ({ label: r.nom, value: r.nvm, me: r.id === 'frontignan' })),
          { fmt: 'int', unit: '€' })));
      container.appendChild(wrapChart('Taux de pauvreté et de chômage par échelle', '',
        C.grouped(rows.map(r => r.nom), [
          { nom: 'Pauvreté (%)', vals: rows.map(r => r.pauv) },
          { nom: 'Chômage 15-64 (%)', vals: rows.map(r => r.tcho) }], { fmt: '1' })));
      if (!compact) container.appendChild(dataTable(d));
      return;
    }

    if (key === 'pop_serie') {
      const st = d.stats;
      container.appendChild(h('div', { class: 'statgrid' }, [
        ['population 1968', fmt(d.valeurs[0], 'int')], ['population 2023', fmt(d.valeurs[d.valeurs.length - 1], 'int')],
        ['gain total', '+' + fmt(st.gain_total, 'int')], ['TCAM 1968-2023', fmt(st.tcam_total, '2') + ' %/an'],
        ['pente 1999-2023', '+' + fmt(st.pente_annuelle, '1') + ' hab./an'], ['R² de la tendance', fmt(st.r2_tendance, '3')],
      ].map(([k, v]) => h('div', { class: 'stat' }, [h('div', { class: 'k', text: k }), h('div', { class: 'v', text: v })]))));
      container.appendChild(wrapChart('Population municipale 1968 → 2023, projection linéaire 2030-2040',
        'Prolongement de la tendance 1999-2023 (moindres carrés) : projection de travail, pas une prévision INSEE',
        C.line(d.annees, d.valeurs, {
          proj: [{ x: 2030, y: st.proj_2030 }, { x: 2040, y: st.proj_2040 }],
          mark: [{ x: 2007, label: 'pic puis stagnation' }],
        })));
      container.appendChild(wrapChart('Taux de croissance annuel moyen par période intercensitaire',
        'La rupture de 2007-2017 (−0,3 puis 0,0 %/an) explique la prudence des projections du SCoT',
        C.ranked(d.periodes.map(p => ({ label: p.de + '-' + p.a, value: p.tcam })), { fmt: '2', unit: '%/an' })));
      return;
    }

    if (key === 'ages') {
      container.appendChild(wrapChart('Structure par âge : 2012, 2017, 2023 (%)',
        'Les 55 ans et plus passent de 33,8 % à 40,4 % de la population en onze ans',
        C.grouped(d.classes, [
          { nom: '2023', vals: d.an2023 }, { nom: '2017', vals: d.an2017 }, { nom: '2012', vals: d.an2012 }],
          { fmt: '1', unit: ' %' })));
      container.appendChild(wrapChart('Évolution 2012 → 2023 (points de %)', '',
        C.ranked(d.classes.map((c, i) => ({ label: c, value: d.stats.delta_2012_2023[i] })), { fmt: '1' })));
      return;
    }

    if (key === 'mobilites') {
      container.appendChild(wrapChart('Modes de déplacement domicile-travail (RP2023)',
        `${d.actifs} actifs occupés · ${d.hors_commune} % travaillent hors de la commune`,
        C.donut(d.modes, d.parts, { center: '80 %', centerSub: 'voiture' })));
      container.appendChild(h('div', { class: 'statgrid' }, [
        ['emplois sur place', fmt(d.stats.emplois, 'int')], ['actifs occupés', fmt(d.stats.actifs, 'int')],
        ['emplois / actif', fmt(d.stats.ratio_emploi_actif, '2')],
      ].map(([k, v]) => h('div', { class: 'stat' }, [h('div', { class: 'k', text: k }), h('div', { class: 'v', text: v })]))));
      return;
    }

    if (key === 'climat') {
      container.appendChild(tableFrom(['Indicateur', 'Aujourd’hui', '2050', '2100'],
        d.lignes.map(l => [l.k, l.now, l.h2050, l.h2100])));
      container.appendChild(h('div', { class: 'src', html:
        `<a href="${d.source.u}" target="_blank" rel="noopener">${d.source.t}</a> — ${d.source.d}` }));
      return;
    }

    if (key === 'submersion') {
      container.appendChild(wrapChart('Dommages estimés sur le bassin de Thau (M€)',
        'Part de Frontignan : 33 % à aléa décennal, 26 % à aléa centennal',
        C.ranked(d.scenarios.map(s => ({ label: s.k, value: s.bassin })), { fmt: '1', unit: 'M€' })));
      container.appendChild(wrapChart('Part des dommages supportée par Frontignan (%)', '',
        C.stacked([{ k: 'Frontignan (Q10)', v: 33 }, { k: '13 autres communes', v: 67 }])));
      container.appendChild(h('p', { class: 'note', text: d.note }));
      return;
    }

    if (key === 'municipales') {
      container.appendChild(wrapChart('Municipales du 15 mars 2026 — 1ᵉʳ tour',
        `${fmt(d.stats.exprimes, 'int')} suffrages exprimés · ${fmt(d.stats.inscrits, 'int')} inscrits · abstention ${d.stats.abstention} %`,
        C.ranked(d.listes.map(l => ({ label: l.k.split('—')[0].trim().slice(0, 22), value: l.pct,
          me: l.sieges === 27 })), { fmt: '2', unit: '%' })));
      container.appendChild(tableFrom(['Liste', 'Voix', '%', 'Sièges'],
        d.listes.map(l => [l.k, fmt(l.voix, 'int'), fmt(l.pct, '2'), l.sieges])));
      return;
    }

    if (key === 'finances') {
      container.appendChild(wrapChart('Frontignan vs moyenne de strate (20-50 000 hab.), comptes 2024',
        'Écart en % à droite ; rouge = au-dessus de la strate, vert = en dessous',
        C.compare(d.indicateurs)));
      const b = d.budget;
      container.appendChild(wrapChart('Budget principal de la Ville (M€)',
        b.note, C.grouped(b.annees.map(String), [
          { nom: 'Fonctionnement', vals: b.fonctionnement }, { nom: 'Investissement', vals: b.investissement }],
          { fmt: '1', unit: ' M€' })));
      container.appendChild(h('p', { class: 'note',
        text: `Part moyenne de l'investissement : ${b.stats.part_invest_moy} % du budget total ; ` +
          `budget moyen sur 4 exercices : ${fmt(b.stats.moyenne, '1')} M€ (médiane ${fmt(b.stats.mediane, '1')} M€, ` +
          `σ = ${fmt(b.stats.ecart_type, '1')}).` }));
      return;
    }

    if (key === 'secteurs') {
      container.appendChild(wrapChart(d.label,
        'Frontignan se distingue par une industrie deux fois plus présente que la moyenne du bassin',
        C.grouped(d.labels, d.series, { fmt: '1', unit: ' %' })));
      return;
    }

    if (key === 'projets') {
      container.appendChild(h('div', { class: 'statgrid' }, [
        ['projets suivis', d.rows.length], ['coûts identifiés', fmt(d.stats.total_identifie, '1') + ' M€'],
        ['par habitant', fmt(d.stats.par_habitant, 'int') + ' €'],
        ['coût médian', fmt(d.stats.mediane, '1') + ' M€'],
        ['coût moyen', fmt(d.stats.moyenne, '1') + ' M€'],
        ['non chiffrés', d.stats.non_chiffres],
      ].map(([k, v]) => h('div', { class: 'stat' }, [h('div', { class: 'k', text: k }), h('div', { class: 'v', text: String(v) })]))));
      container.appendChild(wrapChart('Calendrier des projets (2012-2035)',
        'Couleur = statut : vert livré · bleu engagé · or annoncé · rouge incertain · violet tendance',
        C.gantt(d.rows, { now: 2026 })));
      if (!compact) {
        container.appendChild(tableFrom(['Projet', 'Statut', 'Coût', 'Période', 'Maîtrise d’ouvrage'],
          d.rows.map(r => [r.nom, r.statut, r.cout ? fmt(r.cout, '1') + ' M€' : '❓', r.debut + '-' + r.fin, r.moa])));
      }
      return;
    }

    if (key === 'acteurs') {
      const st = d.stats;
      container.appendChild(h('p', { class: 'note', text: d.note }));
      container.appendChild(wrapChart('Matrice influence × intérêt',
        `${d.rows.length} acteurs · influence moyenne ${fmt(st.influence.moyenne, '2')} (médiane ${
          fmt(st.influence.mediane, '1')}, σ ${fmt(st.influence.ecart_type, '2')}) · corrélation influence/intérêt r = ${
          fmt(st.correlation.r, '2')}`,
        C.quadrant(d.rows.map(a => ({ x: a.influence, y: a.interet, label: a.nom, famille: a.famille, id: a.id })))));
      container.appendChild(wrapChart('Priorité d’engagement (influence × intérêt)', '',
        C.ranked(d.rows.slice().sort((a, b) => b.priorite - a.priorite).slice(0, 14)
          .map(a => ({ label: a.nom.length > 26 ? a.nom.slice(0, 25) + '…' : a.nom, value: a.priorite })),
          { fmt: '0' })));
      const fam = st.familles;
      container.appendChild(tableFrom(['Famille', 'Acteurs', 'Influence moy.', 'Intérêt moy.'],
        Object.keys(fam).map(k => [k, fam[k].n, fmt(fam[k].influence_moy, '2'), fmt(fam[k].interet_moy, '2')])));
      if (!compact) {
        container.appendChild(tableFrom(['Acteur', 'Famille', 'Infl.', 'Int.', 'Posture recommandée'],
          d.rows.slice().sort((a, b) => b.priorite - a.priorite)
            .map(a => [a.nom, a.famille, a.influence, a.interet, a.posture])));
      }
      return;
    }

    if (key === 'scenarios') {
      container.appendChild(wrapChart('Probabilité subjective des scénarios 2040',
        'Estimation d’analyste destinée à être discutée, pas une prévision',
        C.stacked(d.rows.map(s => ({ k: s.nom, v: s.proba })))));
      container.appendChild(tableFrom(['Scénario', 'Population 2040', 'Emplois', 'Moteur', 'Risque'],
        d.rows.map(s => [s.nom, s.pop2040, s.emplois, s.moteur, s.risque])));
      container.appendChild(h('h4', { class: 'sec', text: 'Cinq conditions de succès à 2030' }));
      container.appendChild(tableFrom(['Condition', 'Cible', 'État'],
        d.conditions.map(c => [c.k, c.cible, c.etat])));
      return;
    }

    if (key === 'conditions') {
      container.appendChild(tableFrom(['Condition', 'Cible', 'État', 'Poids'],
        d.rows.map(c => [c.k, c.cible, c.etat, c.poids + '/5'])));
      return;
    }

    if (key === 'jalons') {
      container.appendChild(tableFrom(['Année', 'Jalon', 'Statut'], d.rows.map(j => [j.an, j.k, j.type])));
      return;
    }

    if (key === 'swot') {
      const grid = h('div', { class: 'cards' });
      [['Forces', d.forces, '#79b36b'], ['Faiblesses', d.faiblesses, '#d8595b'],
        ['Opportunités', d.opportunites, '#2fa8c4'], ['Menaces', d.menaces, '#e2b04a']]
        .forEach(([t, arr, c]) => grid.appendChild(h('div', { class: 'card',
          style: `border-color:${c}55` }, [
          h('h3', { text: t + ' (' + arr.length + ')', style: `color:${c}` }),
          h('ul', { class: 'bul' }, arr.map(x => h('li', { text: x }))),
        ])));
      container.appendChild(grid);
      return;
    }

    if (key === 'recos') {
      container.appendChild(wrapChart('Priorisation impact × faisabilité',
        `Score moyen ${fmt(d.stats.score.moyenne, '1')} · médiane ${fmt(d.stats.score.mediane, '1')} · σ ${
          fmt(d.stats.score.ecart_type, '2')}`,
        C.quadrant(d.items.map(r => ({ x: r.faisabilite, y: r.impact, label: r.id + ' ' + r.nom,
          famille: 'Institutionnel' })))));
      container.appendChild(tableFrom(['#', 'Recommandation', 'Impact', 'Faisabilité', 'Horizon', 'KPI'],
        d.items.map(r => [r.id, r.nom, '★'.repeat(r.impact), '★'.repeat(r.faisabilite), r.horizon, r.kpi])));
      return;
    }
  }

  function tableFrom(headers, rows) {
    const t = h('table', { class: 'tbl' }, [
      h('thead', null, [h('tr', null, headers.map(x => h('th', { text: x })))]),
      h('tbody', null, rows.map(r => h('tr', null, r.map((c, i) =>
        h('td', { class: i && typeof c === 'number' ? 'num' : '', text: String(c) }))))),
    ]);
    return h('div', { class: 'table-scroll' }, [t]);
  }

  function dataTable(d) {
    let sortKey = 'pop', asc = false;
    const wrap = h('div', { class: 'table-scroll' });
    function draw() {
      wrap.innerHTML = '';
      const rows = d.rows.slice().sort((a, b) => {
        const va = a[sortKey], vb = b[sortKey];
        if (typeof va === 'string') return asc ? va.localeCompare(vb) : vb.localeCompare(va);
        return asc ? (va ?? -1) - (vb ?? -1) : (vb ?? -1) - (va ?? -1);
      });
      const t = h('table', { class: 'tbl' }, [
        h('thead', null, [h('tr', null, d.fields.map(f => h('th', {
          text: f.label + (f.unit ? ' (' + f.unit + ')' : ''),
          title: 'Trier',
          onclick: () => { asc = (sortKey === f.key) ? !asc : false; sortKey = f.key; draw(); },
        })))]),
        h('tbody', null, rows.map(r => h('tr', { class: r.code === '34108' ? 'me' : '' },
          d.fields.map(f => h('td', { class: f.type === 'text' ? '' : 'num',
            text: f.type === 'text' ? r[f.key] : fmt(r[f.key], f.fmt) }))))),
      ]);
      wrap.appendChild(t);
    }
    draw();
    return wrap;
  }

  /* ====================== SLIDES ====================== */
  function buildSlides() {
    const deck = $('#deck');
    deck.innerHTML = '';
    S.data.slides.forEach((sl, i) => deck.appendChild(renderSlide(sl, i)));
    $('#slideCount').textContent = '1 / ' + S.data.slides.length;
    deck.addEventListener('scroll', () => {
      const i = Math.round(deck.scrollTop / (deck.clientHeight || 1));
      S.slide = Math.max(0, Math.min(S.data.slides.length - 1, i));
      $('#slideCount').textContent = (S.slide + 1) + ' / ' + S.data.slides.length;
      $('#deckBar').style.width = ((S.slide + 1) / S.data.slides.length * 100) + '%';
    });
    $('#prevSlide').onclick = () => gotoSlide(S.slide - 1);
    $('#nextSlide').onclick = () => gotoSlide(S.slide + 1);
    $('#slideGrid').onclick = () => { setMode('graph'); };
  }
  function gotoSlide(i) {
    const deck = $('#deck');
    i = Math.max(0, Math.min(S.data.slides.length - 1, i));
    deck.scrollTo({ top: i * deck.clientHeight, behavior: 'smooth' });
  }

  function renderSlide(sl, i) {
    const s = h('section', { class: 'slide' + (sl.kind === 'cover' ? ' cover' : '') });
    const node = sl.node ? S.byId[sl.node] : null;
    s.appendChild(h('div', { class: 'kicker',
      text: sl.kind === 'cover' ? 'Atlas territorial · septembre 2026' : `${i} — ${sl.title}` }));
    s.appendChild(h('h2', { text: sl.kind === 'cover' ? sl.title : sl.title }));
    if (sl.subtitle) s.appendChild(h('p', { class: 'lead', text: sl.subtitle }));
    if (sl.text) s.appendChild(h('p', { class: 'lead', text: sl.text }));

    if (sl.kind === 'cover') {
      if (node && node.img) s.appendChild(h('img', { class: 'cover-img', src: node.img, alt: node.label }));
      const m = S.data.meta;
      s.appendChild(h('div', { class: 'kpis', style: 'max-width:900px' }, [
        ['24 136', 'habitants (2023)'], ['14', 'communes du bassin de Thau'],
        ['11 ha', 'de friche restituée en 2026'], ['25 M€', 'pour la gare et le PEM'],
      ].map(([b, t]) => h('div', { class: 'kpi' }, [h('b', { text: b }), h('span', { text: t })]))));
      s.appendChild(h('p', { class: 'lead', style: 'color:#7794a0;font-size:13px',
        text: `${m.nb_noeuds} nœuds · ${m.nb_liens} liens · généré le ${m.genere_le}` }));
      return s;
    }

    const cols = h('div', { class: 'cols' + (sl.kind === 'stats' || sl.kind === 'stakeholders' ? ' one' : '') });
    const left = h('div');
    const right = h('div');

    if (sl.kind === 'funnel') {
      const rows = S.data.datasets.echelles.rows;
      left.appendChild(wrapChart('Population et croissance par échelle', '',
        C.ranked(rows.map(r => ({ label: r.nom, value: r.tvam, me: r.id === 'frontignan' })),
          { fmt: '2', unit: '%/an' })));
      right.appendChild(h('div', { class: 'kpis' }, rows.slice(0, 6).map(r => h('div', { class: 'kpi' }, [
        h('b', { text: fmt(r.pop, 'int') }), h('span', { text: r.nom + ' · ' + r.niveau })]))));
    } else if (sl.kind === 'node' && node) {
      if (node.img) left.appendChild(h('img', { src: node.img, alt: node.label,
        style: 'width:100%;border-radius:14px;border:1px solid #1f3c46' }));
      const facts = (node.facts || []).slice(0, 6);
      left.appendChild(h('div', { class: 'kpis' }, facts.map(f =>
        h('div', { class: 'kpi' }, [h('b', { text: String(f.v) }), h('span', { text: f.k })]))));
      const fig = h('div', { class: 'slide-figure' });
      renderDataset(fig, sl.data, { compact: true });
      right.appendChild(fig);
      if (node.bul && node.bul.length) {
        right.appendChild(h('ul', { class: 'bul', style: 'margin-top:14px' },
          node.bul.map(b => h('li', { text: b }))));
      }
    } else {
      const fig = h('div', { class: 'slide-figure' });
      renderDataset(fig, sl.data, { compact: sl.kind !== 'stats' });
      left.appendChild(fig);
    }
    cols.appendChild(left);
    if (right.childNodes.length) cols.appendChild(right);
    s.appendChild(cols);
    return s;
  }

  /* ====================== VUE DONNÉES ====================== */
  function buildDataView() {
    const list = $('#datasetList');
    const labels = {
      communes: 'Les 14 communes', echelles: 'Entonnoir des échelles', pop_serie: 'Population 1968-2023',
      ages: 'Structure par âge', mobilites: 'Mobilités', secteurs: 'Secteurs d’activité',
      finances: 'Finances communales', projets: 'Portefeuille de projets', acteurs: 'Acteurs',
      municipales: 'Municipales 2026', submersion: 'Submersion', climat: 'Climat 2050',
      scenarios: 'Scénarios 2040', jalons: 'Jalons 2026-2040', swot: 'SWOT', recos: 'Recommandations',
    };
    Object.keys(labels).forEach(k => {
      if (!S.data.datasets[k]) return;
      list.appendChild(h('div', { class: k === S.dataset ? 'is-on' : '', text: labels[k],
        onclick: e => {
          $$('#datasetList div').forEach(d => d.classList.remove('is-on'));
          e.target.classList.add('is-on');
          S.dataset = k; drawDataView();
        } }));
    });
    const sel2 = $('#dataVar');
    S.data.datasets.communes.fields.filter(f => f.type !== 'text').forEach(f =>
      sel2.appendChild(h('option', { value: f.key, text: f.label })));
    sel2.value = S.dataVar;
    sel2.onchange = () => { S.dataVar = sel2.value; drawDataView(); };
    drawDataView();
  }
  function drawDataView() {
    const w = $('#dataWrap');
    const d = S.data.datasets[S.dataset];
    w.innerHTML = '';
    w.appendChild(h('h2', { text: d.label || S.dataset }));
    const srcs = (d.sources || []).map(s => `<a href="${s.u}" target="_blank" rel="noopener">${s.t}</a> (${s.d})`).join(' · ');
    w.appendChild(h('p', { class: 'sub', html: (d.note || '') + (srcs ? '<br>' + srcs : '') }));
    $('#dataVar').parentElement.style.opacity = (S.dataset === 'communes') ? 1 : .35;
    const f = S.data.datasets.communes.fields.find(x => x.key === S.dataVar);
    $('#dataVarHint').textContent = (S.dataset === 'communes' && f)
      ? 'Indicateur analysé : ' + f.label + (f.unit ? ' (' + f.unit + ')' : '')
      : 'Sélecteur actif sur le jeu « Les 14 communes ».';
    renderDataset(w, S.dataset, { compact: false, focusVar: S.dataVar });
  }

  /* ====================== NAVIGATION GLOBALE ====================== */
  function setMode(m) {
    S.mode = m;
    document.body.dataset.mode = m;
    $$('.modes .mode').forEach(b => {
      const on = b.dataset.mode === m;
      b.classList.toggle('is-on', on);
      b.setAttribute('aria-selected', on ? 'true' : 'false');
    });
    $$('.view').forEach(v => v.classList.remove('is-on'));
    $('#view-' + m).classList.add('is-on');
    if (m === 'mind') drawMind();
    if (m === 'graph') { startSim(0.4); }
    if (m === 'data') drawDataView();
  }

  function wireGlobal() {
    $$('.modes .mode').forEach(b => b.onclick = () => setMode(b.dataset.mode));
    $('#panelClose').onclick = () => { $('#panel').hidden = true; S.selected = null; highlight(null); };

    const search = $('#search'), sug = $('#suggest');
    let selIdx = -1, results = [];
    function runSearch() {
      const q = search.value.trim().toLowerCase();
      if (!q) { sug.hidden = true; return; }
      results = S.data.nodes.filter(n =>
        n.label.toLowerCase().includes(q) ||
        (n.sub || '').toLowerCase().includes(q) ||
        (n.txt || '').toLowerCase().includes(q)).slice(0, 12);
      sug.innerHTML = '';
      results.forEach((n, i) => sug.appendChild(h('div', { class: i === selIdx ? 'sel' : '',
        onclick: () => { pick(n.id); } }, [
        h('span', { class: 'rdot', style: `width:9px;height:9px;border-radius:50%;background:${n.color}` }),
        h('span', { text: n.label }),
        h('span', { class: 't', text: TYPE_LABEL[n.type] }),
      ])));
      sug.hidden = !results.length;
    }
    function pick(id) {
      sug.hidden = true; search.value = '';
      openNode(id);
      if (S.mode === 'graph') focusNode(id);
      if (S.mode === 'mind') { const n = S.byId[id]; if ((n.children || []).length) { S.mindRoot = id; $('#mindRoot').value = id; drawMind(); } }
    }
    search.addEventListener('input', () => { selIdx = -1; runSearch(); });
    search.addEventListener('keydown', e => {
      if (e.key === 'ArrowDown') { selIdx = Math.min(results.length - 1, selIdx + 1); runSearch(); e.preventDefault(); }
      else if (e.key === 'ArrowUp') { selIdx = Math.max(0, selIdx - 1); runSearch(); e.preventDefault(); }
      else if (e.key === 'Enter' && results[Math.max(0, selIdx)]) pick(results[Math.max(0, selIdx)].id);
      else if (e.key === 'Escape') { sug.hidden = true; search.blur(); }
    });
    document.addEventListener('click', e => { if (!e.target.closest('.search-wrap')) sug.hidden = true; });

    document.addEventListener('keydown', e => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') return;
      if (e.key === '/') { e.preventDefault(); search.focus(); }
      else if (e.key === '1') setMode('graph');
      else if (e.key === '2') setMode('mind');
      else if (e.key === '3') setMode('slides');
      else if (e.key === '4') setMode('data');
      else if (e.key === 'Escape') { $('#panel').hidden = true; highlight(null); }
      else if (S.mode === 'slides') {
        if (['ArrowRight', 'ArrowDown', 'PageDown', ' '].includes(e.key)) { e.preventDefault(); gotoSlide(S.slide + 1); }
        if (['ArrowLeft', 'ArrowUp', 'PageUp'].includes(e.key)) { e.preventDefault(); gotoSlide(S.slide - 1); }
        if (e.key === 'Home') gotoSlide(0);
        if (e.key === 'End') gotoSlide(S.data.slides.length - 1);
      }
    });
    window.addEventListener('resize', () => { if (S.mode === 'mind') drawMind(); });
  }
})();
