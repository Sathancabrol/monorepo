/* ============================================================================
   CARRÉ D'AS — Shell (squelette navigable)
   ----------------------------------------------------------------------------
   Rôle : rendre le portail, la liste des modules, la vue d'un module, la palette
   de commandes, les réglages — et brancher l'assistant et les sons.
   Aucune dépendance externe. Fonctionne en double-clic (file://) comme servi.

   Contrat d'extension (voir docs/carre-das/01-CONTRAT-MODULE.md) :
   un module = une entrée dans shell/data/modules.json, et une zone de travail
   qui se branche dans `#slot-<id>` quand son code est prêt.
   ========================================================================== */
(function () {
  "use strict";

  const R = window.CARRE_REGISTRY || { meta: {}, doors: [], modules: [] };
  const S = { view: { kind: "portail" }, filters: new Set(["dispo", "a-porter", "a-construire"]), q: "", tab: {} };

  /* ------------------------------------------------------------ utilitaires */
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const esc = (s) => (s || "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const mod = (id) => R.modules.find((m) => m.id === id);
  const statusLabel = (s) => ({ dispo: "disponible", "a-porter": "à porter", "a-construire": "à construire" }[s] || s);
  const featureCount = (m) => m.features.length;
  const totalFeatures = () => R.modules.reduce((n, m) => n + featureCount(m), 0);
  const byStatus = (s) => R.modules.reduce((n, m) => n + m.features.filter((f) => f.s === s).length, 0);
  function sound(cue) { window.CarreSounds && CarreSounds.play(cue); }

  /* ------------------------------------------------------------------ routes */
  function go(route, opts) {
    sound("open");
    S.view = route;
    if (route.kind === "module") { S.tab[route.id] = S.tab[route.id] || 0; }
    location.hash = route.kind === "module" ? `#/module/${route.id}` : `#/${route.id || route.kind}`;
    render();
    if (!opts || !opts.silent) announce(route);
  }
  function announce(route) {
    const el = $("#view-title");
    if (el) el.focus({ preventScroll: true });
  }
  function fromHash() {
    const h = (location.hash || "").replace(/^#\/?/, "");
    if (h.startsWith("module/")) return { kind: "module", id: h.split("/")[1] };
    if (h.startsWith("door/")) return { kind: "door", id: h.split("/")[1] };
    if (h === "modules") return { kind: "modules" };
    if (h) return { kind: h };
    return { kind: "portail" };
  }

  /* ------------------------------------------------------------------ vues */
  function viewPortail() {
    const doors = R.doors.filter((d) => !["assistant", "systeme"].includes(d.id));
    const cards = doors.map((d) => {
      const mods = R.modules.filter((m) => m.door === d.id);
      const feats = mods.reduce((n, m) => n + featureCount(m), 0);
      const ready = mods.reduce((n, m) => n + m.features.filter((f) => f.s === "dispo").length, 0);
      const pct = feats ? Math.round((ready / feats) * 100) : 0;
      return `<button class="door" data-door="${esc(d.id)}" aria-label="Porte ${esc(d.label)} : ${feats} fonctionnalités">
        <span class="ic" aria-hidden="true">${d.icon}</span>
        <span class="count">${mods.length} module${mods.length > 1 ? "s" : ""}</span>
        <span class="label">${esc(d.label)}</span>
        <span class="hint">${esc(d.hint)}</span>
        <span class="bar" aria-hidden="true"><i style="width:${pct}%"></i></span>
        <span class="mono-dim">${feats} fonctionnalités · ${pct}% prêt</span>
      </button>`;
    }).join("");

    return `
    <div class="portail">
      <section class="hero">
        <span class="eyebrow">${esc(R.meta.name || "Carré d'As")} · v${esc(R.meta.version || "0")}</span>
        <h1>Le <em>portail</em> vers toutes les fonctionnalités des modules.</h1>
        <p>${esc(R.meta.subtitle || "")} — ${esc(R.meta.principle || "")}</p>
        <div class="hero-stats">
          <div class="hero-stat"><b>${R.modules.length}</b><span>modules</span></div>
          <div class="hero-stat"><b>${totalFeatures()}</b><span>fonctionnalités déclarées</span></div>
          <div class="hero-stat"><b>${byStatus("dispo")}</b><span>déjà disponibles</span></div>
          <div class="hero-stat"><b>${byStatus("a-porter")}</b><span>à porter depuis les branches</span></div>
          <div class="hero-stat"><b>${byStatus("a-construire")}</b><span>à construire</span></div>
        </div>
      </section>

      <section aria-labelledby="doors-title">
        <h2 id="doors-title" class="eyebrow" style="margin-bottom:12px">Les portes</h2>
        <div class="doors">${cards}</div>
      </section>

      <section aria-labelledby="mods-title">
        <div style="display:flex;align-items:baseline;gap:12px;margin-bottom:12px">
          <h2 id="mods-title" class="eyebrow">Tous les modules</h2>
          <button class="chip" data-go="modules">Voir en détail →</button>
        </div>
        <div class="modules">${R.modules.slice(0, 6).map(moduleCard).join("")}</div>
      </section>
    </div>`;
  }

  function moduleCard(m) {
    const shown = m.features.slice(0, 5);
    const rest = m.features.length - shown.length;
    return `<article class="module" id="mod-${esc(m.id)}">
      <header class="module-head">
        <span class="ic" aria-hidden="true">${m.icon}</span>
        <div>
          <h3>${esc(m.label)}</h3>
          <p>${esc(m.tagline)}</p>
        </div>
        <span class="tag ${topStatus(m)}">${featureCount(m)}</span>
      </header>
      <div class="module-body">
        <div class="feat-list">
          ${shown.map((f) => `<button class="feat" data-feature="${esc(m.id)}|${esc(f.n)}">
            <span class="dot ${f.s}" aria-hidden="true"></span>
            <span>${esc(f.n)}<br><span class="mono-dim">${esc(f.d)}</span></span>
            <span class="pill">${esc(f.p)}</span>
          </button>`).join("")}
          ${rest > 0 ? `<button class="feat" data-go-module="${esc(m.id)}"><span></span><span class="mono-dim">+ ${rest} autres fonctionnalités…</span><span></span></button>` : ""}
        </div>
      </div>
      <footer class="module-foot">
        <button class="chip" data-go-module="${esc(m.id)}">Ouvrir le module</button>
        <button class="chip" data-assist="ouvre ${esc(m.label)}">Demander à l'assistant</button>
      </footer>
    </article>`;
  }
  function topStatus(m) {
    const has = (s) => m.features.some((f) => f.s === s);
    if (m.features.every((f) => f.s === "dispo")) return "dispo";
    if (has("dispo")) return "a-porter";
    return "a-construire";
  }

  function viewModules() {
    const nf = norm(S.q);
    const list = R.modules.map((m) => {
      const feats = m.features.filter((f) => S.filters.has(f.s) &&
        (!nf || norm(f.n + " " + f.d + " " + f.src).includes(nf)));
      return { m, feats };
    }).filter((x) => x.feats.length || (!nf && S.filters.size === 3));

    return `
    <div class="filters" style="margin-bottom:var(--s-4)">
      <input class="input" id="q" type="search" placeholder="Filtrer les fonctionnalités…" value="${esc(S.q)}" aria-label="Filtrer">
      ${["dispo", "a-porter", "a-construire"].map((s) => `<button class="chip" data-filter="${s}" aria-pressed="${S.filters.has(s)}">${statusLabel(s)}</button>`).join("")}
      <button class="chip" data-clear>tout</button>
      <span class="mono-dim" style="margin-left:auto">${list.reduce((n, x) => n + x.feats.length, 0)} fonctionnalités affichées</span>
    </div>
    <div class="modules">
      ${list.map(({ m, feats }) => `
        <article class="module">
          <header class="module-head">
            <span class="ic" aria-hidden="true">${m.icon}</span>
            <div><h3>${esc(m.label)}</h3><p>${esc(m.desc)}</p></div>
          </header>
          <div class="module-body"><div class="feat-list">
            ${feats.map((f) => `<button class="feat" data-feature="${esc(m.id)}|${esc(f.n)}">
              <span class="dot ${f.s}" aria-hidden="true"></span>
              <span>${esc(f.n)}<br><span class="mono-dim">${esc(f.d)}</span></span>
              <span class="pill">${esc(f.p)}</span>
            </button>`).join("")}
          </div></div>
          <footer class="module-foot"><button class="chip" data-go-module="${esc(m.id)}">Ouvrir</button>
          <span class="mono-dim" style="margin:auto 0 0 auto">${m.features.length} fonctions</span></footer>
        </article>`).join("")}
    </div>`;
  }

  function viewModule(id) {
    const m = mod(id);
    if (!m) return `<div class="slot"><h2>Module inconnu</h2><p>Identifiant : <code>${esc(id)}</code></p></div>`;
    const tab = Math.min(S.tab[id] || 0, m.features.length - 1);
    const f = m.features[tab] || m.features[0];
    return `
    <div class="grid-2">
      <section>
        <div class="slot">
          <span class="eyebrow">Zone de travail du module — à brancher</span>
          <h2>${esc(f.n)}</h2>
          <p>${esc(f.d)}</p>
          <p class="mono-dim" style="margin-top:14px">
            Contrat : <code>module.json</code> · identifiant <code>${esc(m.id)}</code> ·
            point de montage <code>#slot-${esc(m.id)}</code> · statut ${statusLabel(f.s)} · palier ${esc(f.p)}
          </p>
          <p class="mono-dim">Source dans le dépôt : <code>${esc(f.src)}</code></p>
        </div>
      </section>
      <aside>
        <div class="card">
          <h3>Ce module</h3>
          <div class="kv">Nom <b>${esc(m.label)}</b></div>
          <div class="kv">Porte <b>${esc(m.door)}</b></div>
          <div class="kv">Fonctionnalités <b>${m.features.length}</b></div>
          <div class="kv">Disponibles <b>${m.features.filter((x) => x.s === "dispo").length}</b></div>
          <div class="kv">À porter <b>${m.features.filter((x) => x.s === "a-porter").length}</b></div>
          <div class="kv">À construire <b>${m.features.filter((x) => x.s === "a-construire").length}</b></div>
          <p class="mono-dim" style="margin-top:12px">${esc(m.desc)}</p>
        </div>
        <div class="card" style="margin-top:var(--s-4)">
          <h3>Provenance</h3>
          <p class="mono-dim">${esc(f.src)}</p>
          <p class="mono-dim" style="margin-top:8px">${esc(R.meta.source || "")}</p>
        </div>
      </aside>
    </div>`;
  }

  function viewDoor(id) {
    const d = R.doors.find((x) => x.id === id) || { label: id, hint: "" };
    const mods = R.modules.filter((m) => m.door === id);
    return `<p class="mono-dim" style="margin-bottom:var(--s-4)">${esc(d.hint)}</p>
    <div class="modules">${mods.map(moduleCard).join("")}</div>`;
  }

  function viewAssistant() {
    return `<div class="grid-2">
      <section class="card">
        <h3>Ce que l'assistant sait faire</h3>
        <div class="kv">Ouvrir un module <b>« ouvre le BTP »</b></div>
        <div class="kv">Chercher <b>« cherche métrés »</b></div>
        <div class="kv">Expliquer <b>« explique la décroissance »</b></div>
        <div class="kv">Faire le point <b>« où en est le projet »</b></div>
        <div class="kv">Se taire <b>« silence »</b></div>
        <p class="mono-dim" style="margin-top:12px">Mode règles par défaut : fonctionne sans réseau et sans clé. Un modèle local (Ollama) peut être branché dans les réglages — s'il est absent, il le dit.</p>
      </section>
      <aside class="card">
        <h3>Voix & sons</h3>
        <p class="mono-dim">La voix de sortie utilise la synthèse du système. L'entrée micro utilise la reconnaissance vocale du navigateur (Chrome/Edge) ; ailleurs, l'écrit fonctionne toujours.</p>
        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:12px">
          <button class="chip" data-voice="toggle">Voix : activée/désactivée</button>
          <button class="chip" data-sounds="toggle">Sons : activés/désactivés</button>
        </div>
      </aside>
    </div>`;
  }

  function viewSysteme() {
    const m = mod("systeme");
    return `
    <div class="grid-2">
      <section class="card">
        <h3>Réglages d'affichage</h3>
        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:8px">
          <button class="chip" data-set="density" data-value="comfort">Densité confort</button>
          <button class="chip" data-set="density" data-value="dense">Densité dense</button>
          <button class="chip" data-set="contrast" data-value="high">Contraste élevé</button>
          <button class="chip" data-set="motion" data-value="reduced">Mouvement réduit</button>
          <button class="chip" data-set="reset">Réinitialiser</button>
        </div>
        <h3 style="margin-top:var(--s-5)">Modèle local (optionnel)</h3>
        <p class="mono-dim">Adresse Ollama (ex. <code>http://127.0.0.1:11434</code>) et nom du modèle. Vide = mode règles seul.</p>
        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:8px">
          <input class="input" id="llm-url" placeholder="http://127.0.0.1:11434" value="">
          <input class="input" id="llm-model" placeholder="qwen3.5:9b" style="min-width:160px">
          <button class="chip" data-set="llm">Enregistrer et tester</button>
        </div>
        <p class="mono-dim" id="llm-state" style="margin-top:8px">non testé</p>
      </section>
      <aside class="card">
        <h3>Modules installables</h3>
        <div class="feat-list">
          ${R.modules.map((x) => `<div class="feat"><span class="dot ${topStatus(x)}"></span><span>${esc(x.label)}<br><span class="mono-dim">${featureCount(x)} fonctions</span></span><span class="pill">${topStatus(x) === "dispo" ? "prêt" : "à porter"}</span></div>`).join("")}
        </div>
        <p class="mono-dim" style="margin-top:12px">Contrat de module : <code>docs/carre-das/01-CONTRAT-MODULE.md</code></p>
      </aside>
    </div>${m ? "" : ""}`;
  }

  /* ------------------------------------------------------------------ rendu */
  function render() {
    const v = S.view;
    let head = "", body = "";
    if (v.kind === "portail") { head = { t: "Portail", s: "Toutes les portes, tous les modules, rien de perdu." }; body = viewPortail(); }
    else if (v.kind === "modules") { head = { t: "Tous les modules", s: "Chaque fonctionnalité indique son statut et sa source dans le dépôt." }; body = viewModules(); }
    else if (v.kind === "module") { const m = mod(v.id) || { label: v.id, tagline: "", features: [] }; head = { t: `${m.icon || ""} ${m.label}`, s: m.desc || m.tagline || "" }; body = viewModule(v.id); }
    else if (v.kind === "door") { const d = R.doors.find((x) => x.id === v.id) || { label: v.id }; head = { t: `${d.icon || ""} ${d.label}`, s: d.hint || "" }; body = viewDoor(v.id); }
    else if (v.kind === "assistant") { head = { t: "🛡 Assistant", s: "Un guide, pas un gadget : il navigue, cherche, explique, et se tait quand on le lui demande." }; body = viewAssistant(); }
    else if (v.kind === "systeme") { head = { t: "⚙ Système & réglages", s: "Modules, affichage, voix, sons, modèle local." }; body = viewSysteme(); }
    else { head = { t: "Introuvable", s: "" }; body = `<div class="slot"><h2>Vue inconnue</h2></div>`; }

    $("#view-title").innerHTML = head.t;
    $("#view-sub").textContent = head.s || "";
    $("#view-body").innerHTML = body;
    $("#view-body").scrollTop = 0;

    // onglets du module
    const tabs = $("#mod-tabs");
    if (v.kind === "module") {
      const m = mod(v.id);
      tabs.hidden = false;
      tabs.innerHTML = m.features.map((f, i) => `<button class="mod-tab" role="tab" aria-selected="${i === (S.tab[m.id] || 0)}" data-tab="${i}" title="${esc(f.src)}">${esc(f.n)}</button>`).join("");
    } else { tabs.hidden = true; tabs.innerHTML = ""; }

    const curMod = v.kind === "module" ? mod(v.id) : null;
    $$(".rail-item").forEach((b) => {
      const isDoor = !!b.dataset.door;
      let current = false;
      if (isDoor) {
        if (b.dataset.door === "accueil") current = (v.kind === "portail");
        else if (v.kind === "door") current = (b.dataset.door === v.id);
        else if (curMod) current = (b.dataset.door === curMod.door);
      } else if (b.dataset.go) {
        current = (b.dataset.go === v.kind) || (b.dataset.go === "portail" && v.kind === "portail");
      }
      b.setAttribute("aria-current", current ? "page" : "false");
    });
    updateStatus();
    $("#view-title").focus({ preventScroll: true });
  }

  function updateStatus() {
    $("#st-modules").textContent = `${R.modules.length} modules`;
    $("#st-features").textContent = `${totalFeatures()} fonctionnalités`;
    $("#st-assist").textContent = "assistant " + (window.CarreAssistant ? CarreAssistant.mode() : "—");
  }

  /* ----------------------------------------------------------------- palette */
  function paletteItems() {
    const items = [];
    R.doors.forEach((d) => items.push({ label: `${d.icon} ${d.label}`, kind: "porte", run: () => go({ kind: "door", id: d.id }) }));
    R.modules.forEach((m) => {
      items.push({ label: `${m.icon} ${m.label}`, kind: "module", run: () => go({ kind: "module", id: m.id }) });
      m.features.forEach((f) => items.push({
        label: f.n, kind: m.label, sub: f.d,
        run: () => { const i = m.features.indexOf(f); S.tab[m.id] = i; go({ kind: "module", id: m.id }); }
      }));
    });
    items.push({ label: "⚙ Réglages & densité", kind: "système", run: () => go({ kind: "systeme" }) });
    items.push({ label: "🛡 Ouvrir l'assistant", kind: "assistant", run: () => toggleAssistant(true) });
    items.push({ label: "▶ Mode présentation (plein écran)", kind: "action", run: () => document.documentElement.requestFullscreen && document.documentElement.requestFullscreen() });
    return items;
  }

  function openPalette() {
    const ov = $("#overlay");
    ov.hidden = false;
    const inp = $("#palette-input");
    inp.value = ""; renderPalette(""); inp.focus();
    sound("open");
  }
  function closePalette() { $("#overlay").hidden = true; sound("close"); }

  function renderPalette(q) {
    const nq = norm(q);
    const all = paletteItems();
    const list = nq ? all.map((i) => ({ i, s: Math.max(scoreLite(nq, i.label), scoreLite(nq, i.sub || "") * .7) }))
      .filter((x) => x.s > 20).sort((a, b) => b.s - a.s).slice(0, 40).map((x) => x.i) : all.slice(0, 40);
    $("#palette-list").innerHTML = list.length
      ? list.map((i, idx) => `<button class="palette-row" role="option" data-idx="${idx}" aria-selected="${idx === 0}">
          <span>${esc(i.label)}${i.sub ? `<br><span class="mono-dim">${esc(i.sub)}</span>` : ""}</span>
          <span class="kind">${esc(i.kind)}</span></button>`).join("")
      : `<div class="palette-row"><span class="mono-dim">Aucun résultat. Essayez « métrés », « carte », « agents »…</span></div>`;
    $$("#palette-list .palette-row").forEach((row, idx) => {
      row.onclick = () => { list[idx] && list[idx].run(); closePalette(); };
      row.onmouseenter = () => $$("#palette-list .palette-row").forEach((r) => r.setAttribute("aria-selected", "false")) || row.setAttribute("aria-selected", "true");
    });
    $("#palette-list")._items = list;
  }
  function scoreLite(q, t) {
    t = norm(t); if (!q || !t) return 0;
    if (t.includes(q)) return 90 - Math.min(30, t.length - q.length);
    const qw = q.split(" ").filter((w) => w.length > 2); if (!qw.length) return 0;
    let hit = 0; qw.forEach((w) => { if (t.includes(w)) hit++; });
    return (hit / qw.length) * 60;
  }
  function movePalette(d) {
    const rows = $$("#palette-list .palette-row");
    if (!rows.length) return;
    const cur = rows.findIndex((r) => r.getAttribute("aria-selected") === "true");
    const nxt = (cur + d + rows.length) % rows.length;
    rows.forEach((r, i) => r.setAttribute("aria-selected", String(i === nxt)));
    rows[nxt].scrollIntoView({ block: "nearest" });
  }
  function runPalette() {
    const rows = $$("#palette-list .palette-row");
    const cur = rows.find((r) => r.getAttribute("aria-selected") === "true") || rows[0];
    const items = $("#palette-list")._items || [];
    const idx = cur ? Number(cur.dataset.idx) : 0;
    if (items[idx]) items[idx].run();
    closePalette();
  }

  /* --------------------------------------------------------------- assistant */
  function toggleAssistant(force) {
    const a = $("#assistant");
    const open = force === true ? true : a.hidden;
    a.hidden = !open;
    $("#btn-assistant").classList.toggle("on", open);
    if (open) { sound("open"); $("#assist-input").focus(); }
    else sound("close");
  }

  function wireAssistant() {
    if (!window.CarreAssistant) return;
    CarreAssistant.init({
      onAction: (a) => {
        if (a.type === "module") go({ kind: "module", id: a.id });
        else if (a.type === "door") go({ kind: "door", id: a.id });
        else if (a.type === "search") { S.q = a.q; go({ kind: "modules" }); $("#q") && $("#q").focus(); }
      }
    });
    document.addEventListener("carre:mode", updateStatus);
    $("#assist-send").onclick = () => {
      const v = $("#assist-input").value.trim();
      if (!v) return;
      $("#assist-input").value = "";
      CarreAssistant.emit("me", v);
      CarreAssistant.ask(v);
    };
    $("#assist-input").addEventListener("keydown", (e) => { if (e.key === "Enter") $("#assist-send").click(); });
    $("#assist-mic").onclick = () => { sound("tick"); CarreAssistant.toggleListening(); };
    $("#assist-voice").onclick = (e) => {
      const on = !CarreAssistant.voiceOn();
      CarreAssistant.setVoiceOn(on);
      e.currentTarget.classList.toggle("on", on);
      e.currentTarget.setAttribute("aria-pressed", String(on));
    };
  }

  /* ------------------------------------------------------------------ clavier */
  function wireKeys() {
    document.addEventListener("keydown", (e) => {
      const typing = /^(INPUT|TEXTAREA)$/.test(document.activeElement.tagName);
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") { e.preventDefault(); openPalette(); return; }
      if (e.key === "Escape") {
        if (!$("#overlay").hidden) return closePalette();
        if (!$("#assistant").hidden) return toggleAssistant(false);
      }
      if ($("#overlay").hidden) {
        if (e.key === "ArrowDown" && !typing) { movePalette(1); return; }
        if (e.key === "ArrowUp" && !typing) { movePalette(-1); return; }
        if (e.key === "?" && !typing) { e.preventDefault(); openPalette(); return; }
        if (e.key === "/" && !typing) { e.preventDefault(); go({ kind: "modules" }); setTimeout(() => $("#q") && $("#q").focus(), 40); return; }
        if (e.altKey && /^[1-8]$/.test(e.key)) {
          const d = R.doors[Number(e.key) - 1]; if (d) go({ kind: "door", id: d.id });
        }
      } else {
        if (e.key === "ArrowDown") { e.preventDefault(); movePalette(1); }
        else if (e.key === "ArrowUp") { e.preventDefault(); movePalette(-1); }
        else if (e.key === "Enter") { e.preventDefault(); runPalette(); }
      }
    });
  }

  /* -------------------------------------------------------------- délégation */
  function wireClicks() {
    document.addEventListener("click", (e) => {
      const t = e.target.closest("[data-go],[data-door],[data-go-module],[data-feature],[data-filter],[data-clear],[data-set],[data-voice],[data-sounds],[data-assist],[data-tab]");
      if (!t) return;
      if (t.dataset.go) return go({ kind: t.dataset.go });
      if (t.dataset.door) return go(t.dataset.door === "accueil" ? { kind: "portail" } : { kind: "door", id: t.dataset.door });
      if (t.dataset.goModule) return go({ kind: "module", id: t.dataset.goModule });
      if (t.dataset.tab !== undefined && S.view.kind === "module") {
        S.tab[S.view.id] = Number(t.dataset.tab); sound("tick"); return render();
      }
      if (t.dataset.feature) {
        const [id, name] = t.dataset.feature.split("|");
        const m = mod(id); if (!m) return;
        const i = m.features.findIndex((f) => f.n === name);
        S.tab[id] = Math.max(0, i); return go({ kind: "module", id });
      }
      if (t.dataset.filter) {
        const s = t.dataset.filter;
        S.filters.has(s) ? S.filters.delete(s) : S.filters.add(s);
        return render();
      }
      if (t.hasAttribute("data-clear")) { S.filters = new Set(["dispo", "a-porter", "a-construire"]); S.q = ""; return render(); }
      if (t.dataset.voice) { const on = !CarreAssistant.voiceOn(); CarreAssistant.setVoiceOn(on); t.textContent = on ? "Voix : activée" : "Voix : désactivée"; return sound(on ? "confirm" : "cancel"); }
      if (t.dataset.sounds) {
        const on = !CarreSounds.isEnabled(); CarreSounds.setEnabled(on);
        t.textContent = on ? "Sons : activés" : "Sons : désactivés"; return sound(on ? "confirm" : "cancel");
      }
      if (t.dataset.assist) { toggleAssistant(true); CarreAssistant.emit("me", t.dataset.assist); CarreAssistant.ask(t.dataset.assist); return; }
      if (t.dataset.set) {
        const k = t.dataset.set, v = t.dataset.value;
        if (k === "reset") { document.documentElement.removeAttribute("data-density"); document.documentElement.removeAttribute("data-contrast"); document.documentElement.removeAttribute("data-motion"); sound("cancel"); return; }
        if (k === "llm") {
          const url = $("#llm-url").value.trim(), model = $("#llm-model").value.trim();
          const st = $("#llm-state");
          st.textContent = "test en cours…";
          CarreAssistant.setLocalModel(url ? { url, model } : null);
          CarreAssistant.probeLocalModel(url || "http://127.0.0.1:11434").then((ok) => {
            st.textContent = !url ? "aucun modèle local : mode règles seul."
              : ok ? `modèle local joignable (${model || "modèle par défaut"}).`
                   : "aucune réponse de l'adresse indiquée : l'assistant reste en mode règles.";
            sound(ok ? "confirm" : "cancel");
          });
          return;
        }
        const cur = document.documentElement.getAttribute("data-" + k);
        cur === v ? document.documentElement.removeAttribute("data-" + k) : document.documentElement.setAttribute("data-" + k, v);
        sound("tick");
      }
    });
    document.addEventListener("input", (e) => {
      if (e.target.id === "q") { S.q = e.target.value; const pos = e.target.selectionStart; render(); const q = $("#q"); if (q) { q.focus(); q.setSelectionRange(pos, pos); } }
      if (e.target.id === "palette-input") renderPalette(e.target.value);
    });
    window.addEventListener("hashchange", () => { S.view = fromHash(); render(); });
  }

  /* -------------------------------------------------------------------- boot */
  function boot() {
    S.view = fromHash();
    sound("boot");
    render();
    wireClicks(); wireKeys(); wireAssistant();
    // présentation au premier lancement (une seule fois, jamais bloquant)
    try {
      if (!localStorage.getItem("carre.visited")) {
        localStorage.setItem("carre.visited", "1");
        setTimeout(() => {
          CarreAssistant.emit("bot", `Bonjour. Je suis l'assistant de ${R.meta.name || "Carré d'As"}. Dites « aide » pour la liste, ou tapez Ctrl+K pour chercher parmi ${totalFeatures()} fonctionnalités.`);
        }, 700);
      }
    } catch (_) {}
    updateStatus();
  }

  document.addEventListener("DOMContentLoaded", boot);
  window.CarreShell = { go, openPalette, render, state: S, registry: R };
})();
