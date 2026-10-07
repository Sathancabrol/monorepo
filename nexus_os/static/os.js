/* NEXUS·OS — mission control. Vanilla JS, URLs relatives (montable sous /os/). */
"use strict";

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const esc = (s) => String(s ?? "").replace(/[&<>"]/g,
  (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const nf = (n) => (n ?? 0).toLocaleString("fr-FR");
const clip = (s, n = 220) => (s = String(s ?? ""), s.length > n ? s.slice(0, n) + "…" : s);

const S = {
  agents: [], skills: [], models: [], providers: [], harnesses: [], board: [],
  agent: "orchestrator", mode: "orchestré", crew: new Set(), approval: "smart",
  es: null, status: null, skillFilter: "", agentFilter: "", harness: "claude-code",
  harnessAgent: "orchestrator", filePath: "",
};

/* ───────────────────────────── API ───────────────────────────── */
async function api(path, opts = {}) {
  const res = await fetch(path, {
    headers: opts.body ? { "Content-Type": "application/json" } : {}, ...opts,
  });
  if (!res.ok) {
    let d = res.statusText;
    try { d = (await res.json()).detail || d; } catch {}
    throw new Error(`${res.status} ${d}`);
  }
  return res.json();
}
const post = (p, body) => api(p, { method: "POST", body: JSON.stringify(body ?? {}) });

/* ───────────────────────── navigation ───────────────────────── */
function show(v) {
  $$(".view").forEach((x) => x.classList.toggle("active", x.id === `view-${v}`));
  $$(".rail-btn").forEach((b) => b.classList.toggle("active", b.dataset.view === v));
  ({ control: loadControl, agents: loadAgents, skills: loadSkills, harness: loadHarness,
     mcp: loadMcp, instincts: loadInstincts, tasks: loadTasks, evals: loadEvals,
     plugins: loadPlugins,
     router: loadRouter, logs: loadLogs, files: () => loadFiles(""), memory: loadMemory,
     board: loadBoard }[v] || (() => {}))();
}
$$(".rail-btn").forEach((b) => b.addEventListener("click", () => show(b.dataset.view)));
$$("[data-goto]").forEach((b) => b.addEventListener("click", () => show(b.dataset.goto)));

/* ───────────────────────── télémétrie ───────────────────────── */
async function loadStatus() {
  S.status = await api("api/status");
  const st = S.status, live = st.mode_info.mode === "live";
  const tel = $("#tel-mode");
  tel.innerHTML = `<i class="dot ${live ? "on" : "off"}"></i><b>${live ? "LIVE" : "HORS-LIGNE"}</b>`;
  tel.title = live ? st.mode_info.providers_ready.join(", ") : "moteur local déterministe";
  $("#tel-models").innerHTML = `modèles <b>${st.mode_info.models_ready}/${st.mode_info.models_total}</b>`;
  $("#tel-agents").innerHTML = `agents <b>${st.runtime.agents}</b>`;
  $("#tel-skills").innerHTML = `compétences <b>${st.runtime.skills}</b>`;
  $("#tel-mem").innerHTML = `mémoire <b>${st.runtime.memory_items}</b>`;
  $("#tel-shell").innerHTML = `shell <b>${st.flags.shell ? "on" : "off"}</b>`;
  try {
    const cx = await api("api/context");
    $("#tel-ctx").innerHTML = cx.references
      ? `contexte <b>−${nf(cx.tokens_saved)}t</b>` : `contexte <b>inline</b>`;
    $("#tel-ctx").title = cx.references
      ? `${cx.references} résultat(s) référencé(s), ${(cx.ratio * 100).toFixed(1)} % du volume hors contexte`
      : "aucun résultat n'a dépassé le seuil de référencement";
  } catch {}
  $("#k-mode").textContent = live ? "LIVE" : "OFFLINE";
  $("#k-mode-d").textContent = live ? st.mode_info.providers_ready.join(", ")
    : "aucune clé API — moteur local";
  $("#k-agents").textContent = st.runtime.agents;
  $("#k-agents-d").textContent = `${st.runtime.skills} compétences · ${st.runtime.tools} outils`;
  $("#k-runs").textContent = nf(st.runtime.db.runs);
  $("#k-runs-d").textContent = `${st.runtime.db.runs_ok} terminées`;
  $("#k-tokens").textContent = nf(st.runtime.db.tokens_total);
  $("#k-tokens-d").textContent = `${nf(st.runtime.db.messages)} messages`;
}

/* ──────────────────── MISSION CONTROL ──────────────────── */
async function loadControl() {
  await Promise.all([loadStatus(), loadAgents(), loadRuns(), loadBoard(), loadArtifacts()]);
}

async function loadRuns() {
  const runs = await api("api/runs?limit=12");
  $("#runs-count").textContent = `${runs.length} affichées`;
  $("#recent-runs").innerHTML = runs.map((r) => `
    <div class="runrow">
      <span class="dot ${r.status === "done" ? "on" : "off"}"></span>
      <span class="t" title="${esc(r.task)}">${esc(clip(r.task, 70))}</span>
      <span class="m">${esc(r.agent_id)}</span>
      <span class="m">${r.steps}é · ${nf(r.tokens)}t · ${r.duration_ms}ms</span>
    </div>`).join("") || `<div class="empty">Aucune exécution — lance une tâche.</div>`;
}

async function loadArtifacts() {
  const runs = await api("api/runs?limit=25");
  const arts = [...new Set(runs.flatMap((r) => r.phases ? [] : []))];
  const list = [];
  for (const r of runs) {
    const raw = r.result || "";
    const m = raw.match(/workspace\/[\w./-]+/g) || [];
    m.forEach((x) => { if (!list.includes(x)) list.push(x); });
  }
  arts.push(...list);
  $("#art-count").textContent = `${list.length}`;
  $("#recent-arts").innerHTML = list.slice(0, 12).map((a) => `
    <div class="item" data-art="${esc(a)}"><div class="n">${esc(a.replace("workspace/", ""))}</div></div>`
  ).join("") || `<div class="empty">Aucun artefact produit.</div>`;
  $$("[data-art]").forEach((el) => el.addEventListener("click", () => {
    show("files"); openFile(el.dataset.art.replace(/^workspace\//, ""));
  }));
}

async function loadFleet() {
  $("#fleet-count").textContent = `${S.agents.length}`;
  $("#fleet").innerHTML = S.agents.map((a) => `
    <div class="agent-row" data-agent="${esc(a.id)}">
      <span class="emo">${esc(a.emoji)}</span>
      <span><div class="nm">${esc(a.name)}</div><div class="rl">${esc(a.role)}</div></span>
      <span class="st badge ${a.source === "user" ? "acc" : ""}">${esc(a.source)}</span>
    </div>`).join("");
  $$("#fleet [data-agent]").forEach((el) => el.addEventListener("click", () => {
    S.agent = el.dataset.agent; show("console"); $("#run-agent").value = S.agent;
  }));
  const sel = $("#qc-agent-sel");
  sel.innerHTML = S.agents.map((a) =>
    `<option value="${esc(a.id)}"${a.id === "orchestrator" ? " selected" : ""}>${esc(a.emoji)} ${esc(a.name)}</option>`).join("");
  $("#qc-agent").textContent = "orchestrateur par défaut";
  $("#b-agent").innerHTML = S.agents.map((a) =>
    `<option value="${esc(a.id)}">${esc(a.emoji)} ${esc(a.name)}</option>`).join("");
}

/* ───────────────────────── AGENTS ───────────────────────── */
const DOMAINS = {
  "code & qualité": ["coder", "reviewer", "qa", "devops", "architect"],
  "contenu & langue": ["writer", "translator", "teacher", "videomaker"],
  "données & territoire": ["analyst", "geo", "archivist"],
  "enquête & décision": ["researcher", "osint", "jurist", "pm"],
  "méta": ["orchestrator", "builder", "promptsmith", "designer", "pilot", "coach"],
};
const domainOf = (id) => Object.keys(DOMAINS).find((d) => DOMAINS[d].includes(id)) || "autre";

async function loadAgents() {
  if (!S.agents.length) S.agents = await api("api/agents");
  await loadFleet();
  $("#agents-sub").textContent =
    `${S.agents.length} agents · ${S.agents.filter((a) => a.source === "user").length} créés par toi`;
  $("#agent-filters").innerHTML = Object.keys(DOMAINS).map((d) =>
    `<button class="chip${S.agentFilter === d ? " on" : ""}" data-f="${esc(d)}">${esc(d)}</button>`).join("");
  $$("#agent-filters [data-f]").forEach((b) => b.addEventListener("click", () => {
    S.agentFilter = S.agentFilter === b.dataset.f ? "" : b.dataset.f; loadAgents();
  }));
  renderAgentGrid();

  // sélecteurs de la console
  $("#run-agent").innerHTML = S.agents.map((a) =>
    `<option value="${esc(a.id)}"${a.id === S.agent ? " selected" : ""}>${esc(a.emoji)} ${esc(a.name)} — ${esc(a.role)}</option>`).join("");
  $("#crew-picker").innerHTML = S.agents.filter((a) => a.id !== "orchestrator").map((a) =>
    `<button class="chip${S.crew.has(a.id) ? " on" : ""}" data-c="${esc(a.id)}">${esc(a.emoji)} ${esc(a.name)}</button>`).join("");
  $$("#crew-picker [data-c]").forEach((b) => b.addEventListener("click", () => {
    const id = b.dataset.c;
    S.crew.has(id) ? S.crew.delete(id) : S.crew.add(id);
    b.classList.toggle("on", S.crew.has(id));
  }));
  $("#h-agent").innerHTML = S.agents.map((a) =>
    `<option value="${esc(a.id)}"${a.id === S.harnessAgent ? " selected" : ""}>${esc(a.emoji)} ${esc(a.name)}</option>`).join("");
}

function renderAgentGrid() {
  const q = ($("#agent-search")?.value || "").toLowerCase();
  const rows = S.agents.filter((a) =>
    (!S.agentFilter || domainOf(a.id) === S.agentFilter) &&
    (!q || `${a.name} ${a.role} ${a.description} ${a.skills.join(" ")}`.toLowerCase().includes(q)));
  $("#agent-grid").innerHTML = rows.map((a) => `
    <div class="agent-card">
      <div class="top">
        <span class="emo">${esc(a.emoji)}</span>
        <div><div class="nm">${esc(a.name)}</div><div class="rl">${esc(a.role)}</div></div>
      </div>
      <div class="ds">${esc(a.description)}</div>
      <div class="chips">
        ${a.skills.map((s) => `<span class="pill s">${esc(s)}</span>`).join("")}
        ${a.tools.slice(0, 5).map((t) => `<span class="pill t">${esc(t)}</span>`).join("")}
        ${a.tools.length > 5 ? `<span class="pill">+${a.tools.length - 5}</span>` : ""}
      </div>
      <div class="chips">
        <span class="pill ${a.source === "user" ? "b" : ""}">${esc(a.source)}</span>
        <span class="pill">${esc(a.autonomy)}</span>
        <span class="pill">${esc(domainOf(a.id))}</span>
      </div>
      <div class="lc">${esc(a.lifecycle.join(" → "))}</div>
      <div class="acts">
        <button class="sm primary" data-run="${esc(a.id)}">Ouvrir</button>
        <button class="sm" data-spec="${esc(a.id)}">Spec</button>
        <button class="sm" data-exp="${esc(a.id)}">Exporter</button>
        ${a.source === "user" ? `<button class="sm danger" data-del="${esc(a.id)}">Suppr.</button>` : ""}
      </div>
    </div>`).join("") || `<div class="empty">Aucun agent ne correspond.</div>`;

  $$("[data-run]").forEach((b) => b.addEventListener("click", () => {
    S.agent = b.dataset.run; show("console"); $("#run-agent").value = S.agent;
  }));
  $$("[data-spec]").forEach((b) => b.addEventListener("click", async () => {
    const d = await api(`api/agents/${b.dataset.spec}`);
    dialog(`${d.spec.emoji} ${d.spec.name} — spec exportable`, d.markdown);
  }));
  $$("[data-exp]").forEach((b) => b.addEventListener("click", () => {
    S.harnessAgent = b.dataset.exp; show("harness");
  }));
  $$("[data-del]").forEach((b) => b.addEventListener("click", async () => {
    if (!confirm(`Supprimer l'agent ${b.dataset.del} ?`)) return;
    await fetch(`api/agents/${b.dataset.del}`, { method: "DELETE" });
    S.agents = []; await Promise.all([loadAgents(), loadStatus()]);
  }));
}
$("#agent-search")?.addEventListener("input", renderAgentGrid);

/* ───────────────────────── CONSOLE ───────────────────────── */
const SUGGESTIONS = [
  "Audite la structure de nexus_os et produis un diagramme d'architecture",
  "Fais la revue de sécurité de nexus_os/tools.py",
  "Rédige la page d'accueil de NEXUS·OS : promesse, preuve, mécanisme, objection, action",
  "Crée un agent qui relit les contrats et extrait les clauses risquées",
  "Compare le routeur de NEXUS·OS à OmniRoute et liste les écarts",
  "Cartographie les 9 projets du monorepo et leurs dépendances",
  "Analyse la consommation de tokens du jour et dis ce qu'elle ne permet pas de conclure",
];
$("#suggestions").innerHTML = SUGGESTIONS.map((s) =>
  `<div class="item" data-sugg><div class="d">${esc(s)}</div></div>`).join("");
$$("[data-sugg]").forEach((el) => el.addEventListener("click", () => {
  $("#run-task").value = el.querySelector(".d").textContent;
}));

function pick(group, key, attr) {
  $$(`#${group} .chip`).forEach((b) => b.addEventListener("click", () => {
    $$(`#${group} .chip`).forEach((x) => x.classList.remove("on"));
    b.classList.add("on"); S[key] = b.dataset[attr];
  }));
}
pick("mode-picker", "mode", "mode");
pick("approval-picker", "approval", "approval");

function evNode(cls, tag, body, who = "") {
  const d = document.createElement("div");
  d.className = `ev ${cls}`;
  d.innerHTML = `<div class="hd"><span class="tag">${esc(tag)}</span>` +
    (who ? `<span class="who">${esc(who)}</span>` : "") + `</div><div class="bd">${esc(body)}</div>`;
  return d;
}

function renderEvent(e) {
  const box = $("#stream");
  const push = (cls, tag, body, who) => {
    box.appendChild(evNode(cls, tag, body, who)); box.scrollTop = box.scrollHeight;
  };
  /* En mode parallèle, chaque événement porte `agent_id` : c'est lui qui prime
     sur le nom du modèle ou de la phase, sinon on ne sait plus qui travaille. */
  const who = e.agent_id || e.model || "";
  switch (e.type) {
    case "run_start":
      if (!e.depth) {
        $("#plan").innerHTML = e.phases.map((p, i) =>
          `<div class="step" data-p="${esc(p)}"><span class="ix">${i + 1}</span>${esc(p)}</div>`).join("");
        $("#plan-meta").textContent = `${e.agent.name} · ${e.phases.length} phases`;
      }
      push("phase", e.depth ? "sous-agent" : "démarrage",
        `${e.agent.emoji} ${e.agent.name} — ${e.task}`,
        `${e.mode} · approbation ${e.approval}`);
      break;
    case "pipeline_step":
      push("phase", `étape ${e.index}/${e.total}`, `agent : ${e.agent_id}`);
      break;
    case "routing":
      push("route", "routage", e.candidates.map((c) => `${c.emoji} ${c.name} — ${c.score}`).join("\n")
        + (e.chosen ? `\n→ délégué à ${e.chosen.name}` : "\n→ traité par l'orchestrateur"));
      break;
    case "phase": {
      $$(".step").forEach((s) => {
        if (s.dataset.p === e.phase) s.className = "step now";
        else if (s.classList.contains("now")) s.className = "step done";
      });
      push("phase", `phase ${e.index}/${e.total} · ${e.phase}`, e.title, who);
      break;
    }
    case "thinking":
      if (e.text?.trim()) push(e.depth > 0 ? "think sub" : "think", "raisonnement",
        clip(e.text, 900), `${e.model} · ${e.mode}`);
      break;
    case "tool_call":
      push("tool", "outil", `${e.name}(${clip(JSON.stringify(e.args), 300)})`, who);
      break;
    case "tool_result":
      push(e.ok ? "ok" : "err", `${e.name} ${e.ok ? "→" : "✗"}`, clip(e.result, 1400), who);
      break;
    case "approval_required":
      push("approval", "autorisation requise",
        `${e.name} — ${e.reason} (mode ${e.mode}).\nRelance avec cet outil autorisé pour continuer.`);
      break;
    case "artifact":
      push("ok", "artéfact", e.path);
      break;
    case "context_reference":
      push("route", "contexte",
        `${e.name} : ${nf(e.chars)} caractères sortis du contexte ` +
        `≈ ${nf(e.saved_tokens)} tokens économisés`, who);
      break;
    case "instincts_learned":
      push("ok", "appris",
        `${e.count} instinct(s) déduit(s) de cette exécution :\n` +
        (e.rules || []).map((r) => `- ${r}`).join("\n"));
      break;
    case "agent_created":
      push("ok", "agent créé", `${e.agent.emoji} ${e.agent.name} (${e.agent.id})\n` +
        (e.rationale || []).join("\n"));
      break;
    case "handoff":
      push("route", "délégation", `→ ${e.to} : ${clip(e.task, 160)}`);
      break;
    case "consolidation":
      push("route", "consolidation", `retour de ${e.from}`);
      break;
    case "message":
      push(e.depth > 0 ? "msg sub" : "msg",
        `réponse · confiance : ${e.confidence || "—"}`,
        e.depth > 0 ? clip(e.text, 700) + "…" : e.text,
        [who, e.model].filter(Boolean).join(" · "));
      break;
    case "error":
      push("err", "erreur", e.message);
      break;
    case "run_end":
      push("phase", "fin",
        `${e.steps} étapes · ${nf(e.tokens)} tokens · ${e.duration_ms} ms · ${e.mode}` +
        (e.artifacts?.length ? `\nartéfacts : ${e.artifacts.join(", ")}` : ""),
        e.agent_id || "");
      break;
    case "result":
      if (e.runs) push("phase", "terminé", `${e.runs.length} agents exécutés`);
      break;
    case "log":
      push("think", "log", e.message);
      break;
  }
}

function stream(url) {
  $("#btn-stop").disabled = false;
  $("#run-status").textContent = "en cours";
  $("#run-status").className = "badge acc";
  $("#stream-meta").innerHTML = `<i class="dot busy"></i> flux ouvert`;
  const es = new EventSource(url);
  S.es = es;
  const done = (label) => {
    es.close(); S.es = null; $("#btn-stop").disabled = true;
    $("#run-status").textContent = label; $("#run-status").className = "badge";
    $("#stream-meta").textContent = "flux fermé";
    loadStatus(); loadRuns(); loadArtifacts();
  };
  es.onmessage = (m) => {
    let e; try { e = JSON.parse(m.data); } catch { return; }
    if (e.type === "stream_close") return done("terminé");
    renderEvent(e);
  };
  es.onerror = () => done("interrompu");
}

function task() {
  const t = $("#run-task").value.trim();
  if (!t) { alert("Écris une tâche."); return ""; }
  return t;
}
function launch() {
  const t = task(); if (!t) return;
  const ap = `approval=${S.approval}`;
  let url;
  if (S.mode === "orchestré") {
    url = `api/run?task=${encodeURIComponent(t)}&agent=orchestrator&${ap}`;
  } else if (S.mode === "sequentiel") {
    S.agent = $("#run-agent").value;
    url = `api/run?task=${encodeURIComponent(t)}&agent=${encodeURIComponent(S.agent)}&${ap}`;
  } else {
    if (S.crew.size < 2) { alert("Choisis au moins 2 agents dans l'équipe."); return; }
    const ids = [...S.crew].join(",");
    url = `api/${S.mode === "parallele" ? "parallel" : "pipeline"}?task=${encodeURIComponent(t)}` +
      `&${S.mode === "parallele" ? "agents_list" : "agents_chain"}=${encodeURIComponent(ids)}&${ap}`;
  }
  $("#stream").innerHTML = ""; $("#plan").innerHTML = "";
  $("#plan-meta").textContent = S.mode;
  stream(url);
}
$("#btn-run").addEventListener("click", launch);
$("#btn-stop").addEventListener("click", () => S.es?.close());
$("#btn-clear").addEventListener("click", () => { $("#stream").innerHTML = ""; $("#plan").innerHTML = ""; });

$("#qc-run").addEventListener("click", () => {
  const t = $("#qc-task").value.trim(); if (!t) { alert("Écris une tâche."); return; }
  show("console"); $("#run-task").value = t; launch();
});
$("#qc-route").addEventListener("click", async () => {
  const t = $("#qc-task").value.trim(); if (!t) return;
  const r = await post("api/route", { task: t });
  $("#qc-hint").innerHTML = "<b>Qui doit traiter&nbsp;?</b><br>" + r.ranking
    .map((c) => `${esc(c.emoji)} ${esc(c.name)} — ${c.score}`).join("<br>")
    + (r.suggested ? `<br>→ <b>${esc(r.suggested.name)}</b>` : "");
});

/* ───────────────────────── CRÉATEUR ───────────────────────── */
async function loadModelOptions() {
  S.models = await api("api/models");
  $("#c-model").innerHTML = '<option value="">routeur automatique</option>' +
    S.models.map((m) => `<option value="${esc(m.id)}">${esc(m.provider_name)} — ${esc(m.label)}${m.free ? " (gratuit)" : ""}</option>`).join("");
}
$("#btn-draft").addEventListener("click", async () => {
  const description = $("#c-desc").value.trim();
  if (!description) { alert("Décris le métier de l'agent."); return; }
  $("#c-msg").textContent = "génération…"; $("#c-engine").textContent = "…";
  try {
    const r = await post("api/agents/draft", {
      description, name: $("#c-name").value.trim(), model: $("#c-model").value,
      autonomy: $("#c-autonomy").value, use_llm: $("#c-llm").checked });
    $("#c-spec").value = JSON.stringify(r.spec, null, 2);
    $("#c-rationale").innerHTML = r.rationale.map((x) => `<li>${esc(x)}</li>`).join("") +
      `<li>recette : ${esc(r.test_recipe)}</li>`;
    $("#c-engine").textContent = `moteur ${r.engine}`;
    $("#c-engine").className = `badge ${r.engine === "live" ? "ok" : "warn"}`;
    $("#c-msg").textContent = "Brouillon prêt — modifiable, puis enregistrer.";
    $("#btn-save").disabled = false;
  } catch (e) { $("#c-msg").textContent = "échec : " + e.message; }
});
$("#btn-save").addEventListener("click", async () => {
  let spec;
  try { spec = JSON.parse($("#c-spec").value); }
  catch (e) { return $("#c-msg").textContent = "JSON invalide : " + e.message; }
  try {
    const r = await api("api/agents", { method: "POST", body: JSON.stringify(spec) });
    $("#c-msg").textContent = `enregistré : ${r.agent.id}`;
    S.agents = []; await Promise.all([loadAgents(), loadStatus()]);
  } catch (e) { $("#c-msg").textContent = "échec : " + e.message; }
});

/* ───────────────────────── TABLEAU ───────────────────────── */
async function loadBoard() {
  S.board = await api("api/board");
  $("#board-count").textContent = `${S.board.count}`;
  $("#b-col").innerHTML = S.board.columns.map((c) => `<option>${esc(c)}</option>`).join("");
  $("#board").innerHTML = S.board.columns.map((c) => {
    const items = S.board.items.filter((i) => i.column === c);
    return `<div class="col"><h3>${esc(c)} <span>${items.length}</span></h3>` +
      (items.map((i) => `<div class="task"><div class="t">${esc(i.title)}</div>
        <div class="m">${esc(i.agent || "—")} · ${esc(i.id)}
        ${c !== "terminé" ? `<button class="sm" data-done="${esc(i.id)}">✓</button>` : ""}
        <button class="sm danger" data-rm="${esc(i.id)}">✕</button></div></div>`).join("")
        || `<div class="empty" style="padding:10px;font-size:11.5px">vide</div>`) + `</div>`;
  }).join("");
  $("#mini-board").innerHTML = S.board.columns.map((c) => {
    const n = S.board.items.filter((i) => i.column === c).length;
    return `<div class="item"><div class="n">${esc(c)}</div><div class="m">${n} tâche(s)</div></div>`;
  }).join("");
  $$("[data-done]").forEach((b) => b.addEventListener("click", () =>
    post("api/board", { action: "done", task_id: b.dataset.done }).then(loadBoard)));
  $$("[data-rm]").forEach((b) => b.addEventListener("click", () =>
    post("api/board", { action: "remove", task_id: b.dataset.rm }).then(loadBoard)));
}
$("#b-add").addEventListener("click", async () => {
  const title = $("#b-title").value.trim(); if (!title) return;
  await post("api/board", { action: "add", title, agent: $("#b-agent").value,
    column: $("#b-col").value });
  $("#b-title").value = ""; loadBoard();
});

/* ──────────────────────── COMPÉTENCES ──────────────────────── */
async function loadSkills() {
  S.skills = await api("api/skills");
  $("#skills-count").textContent = `${S.skills.length}`;
  $("#skill-list").innerHTML = S.skills.map((s) => `
    <div class="item" data-skill="${esc(s.name)}">
      <div class="n">${esc(s.name)}</div><div class="d">${esc(s.description)}</div>
      <div class="m">${esc(s.tags.join(", "))} · ${esc(s.source)} · ${esc(s.tools.join(", ") || "sans outil")}</div>
    </div>`).join("");
  $$("[data-skill]").forEach((el) => el.addEventListener("click", async () => {
    const s = await api(`api/skills/${el.dataset.skill}`);
    $("#skill-title").textContent = s.name;
    $("#skill-src").textContent = s.source;
    $("#skill-body").textContent = s.body;
  }));
  if (S.skills[0]) $$("[data-skill]")[0].click();
}

/* ───────────────────────── HARNESS ───────────────────────── */
async function loadHarness() {
  if (!S.agents.length) await loadAgents();
  S.harnesses = await api("api/harnesses");
  $("#h-count").textContent = `${S.harnesses.length} cibles`;
  $("#harness-list").innerHTML = S.harnesses.map((h) => `
    <div class="item${h.id === S.harness ? " on" : ""}" data-h="${esc(h.id)}"
         style="${h.id === S.harness ? "border-color:var(--acc)" : ""}">
      <div class="n">${esc(h.name)}</div>
      <div class="d">${esc(h.description)}</div>
      <div class="m">${esc(h.filename.replace("{id}", "…"))} · ${esc(h.kind)}</div>
    </div>`).join("");
  $$("[data-h]").forEach((el) => el.addEventListener("click", () => {
    S.harness = el.dataset.h; loadHarness();
  }));
  renderHarnessPreview();
}
async function renderHarnessPreview(save = false) {
  const r = await api(`api/agents/${S.harnessAgent}/harness/${S.harness}${save ? "?save=true" : ""}`);
  $("#h-file").innerHTML = `fichier cible : <code>${esc(r.filename)}</code> · ${nf(r.bytes)} octets` +
    (r.saved_to ? ` · <span class="yes">écrit dans ${esc(r.saved_to)}</span>` : "");
  $("#h-body").textContent = r.content;
}
$("#h-agent").addEventListener("change", (e) => { S.harnessAgent = e.target.value; renderHarnessPreview(); });
$("#h-save").addEventListener("click", () => renderHarnessPreview(true));

/* ───────────────────────── MCP ───────────────────────── */
async function loadMcp() {
  const [m, cx] = await Promise.all([api("api/mcp"), api("api/context")]);
  $("#mcp-proto").textContent = m.protocol_version;
  $("#mcp-count").textContent = m.count;
  $("#mcp-count-d").textContent = m.count ? `${m.enabled} actif(s) · stateless` : "aucun serveur connecté";
  $("#mcp-list-n").textContent = `${m.count}`;
  $("#mcp-saved").textContent = nf(cx.tokens_saved);
  $("#mcp-saved-d").textContent = cx.references
    ? `${cx.references} référence(s) · ${(cx.ratio * 100).toFixed(1)} % du volume hors contexte`
    : "rien au-dessus du seuil pour l'instant";
  const remote = (await api("api/tools")).filter((t) => t.name.startsWith("mcp__"));
  $("#mcp-tools").textContent = remote.length;
  $("#mcp-list").innerHTML = m.servers.map((sv) => `
    <div class="item" data-srv="${esc(sv.name)}">
      <div class="n">${esc(sv.name)} ${sv.enabled ? "" : "(inactif)"}</div>
      <div class="d">${esc(sv.description || sv.url)}</div>
      <div class="m">${esc(sv.url)}${sv.auth_env ? ` · clé ${esc(sv.auth_env)}` : ""}</div>
      <div class="row" style="margin-top:6px">
        <button class="sm primary" data-probe="${esc(sv.name)}">Sonder</button>
        <button class="sm danger" data-drop="${esc(sv.name)}">Retirer</button>
      </div>
    </div>`).join("") || `<div class="empty">Aucun serveur — ajoute-en un à gauche.</div>`;
  $$("[data-probe]").forEach((b) => b.addEventListener("click", () => probeServer(b.dataset.probe)));
  $$("[data-drop]").forEach((b) => b.addEventListener("click", async () => {
    if (!confirm(`Retirer le serveur ${b.dataset.drop} ?`)) return;
    await fetch(`api/mcp/${encodeURIComponent(b.dataset.drop)}`, { method: "DELETE" });
    loadMcp();
  }));
}
async function probeServer(name) {
  $("#mcp-probe-state").textContent = "sonde…";
  $("#mcp-probe-out").textContent = "connexion…";
  try {
    const r = await api(`api/mcp/${encodeURIComponent(name)}/probe`);
    $("#mcp-probe-state").textContent = r.status;
    $("#mcp-probe-state").className = `badge ${r.status === "ok" ? "ok" : "err"}`;
    const lines = [`${r.name} — ${r.url}`, `état : ${r.status}`];
    if (r.error) lines.push(`erreur : ${r.error}`);
    if (r.card) lines.push(r.card.error ? `Server Card : ${r.card.error}`
      : `Server Card : ${r.card.name} v${r.card.version} — ` +
        `capacités ${Object.keys(r.card.capabilities || {}).join(", ") || "aucune"}`);
    if (r.discover) lines.push(`protocole : ${r.discover.protocol_version}\nserveur : ` +
      `${JSON.stringify(r.discover.server_info)}\ncapacités : ` +
      Object.keys(r.discover.capabilities || {}).join(", "));
    lines.push(`outils (${r.tools.length}) :`);
    r.tools.forEach((t) => lines.push(`  - mcp__${r.name}__${t.name} — ${t.description}`));
    $("#mcp-probe-out").textContent = lines.join("\n");
  } catch (e) {
    $("#mcp-probe-state").textContent = "échec";
    $("#mcp-probe-out").textContent = e.message;
  }
}
$("#mcp-add").addEventListener("click", async () => {
  const name = $("#mcp-name").value.trim(), url = $("#mcp-url").value.trim();
  if (!name || !url) { $("#mcp-msg").textContent = "nom et URL requis"; return; }
  try {
    await post("api/mcp", { name, url, description: $("#mcp-desc").value.trim(),
                            auth_env: $("#mcp-auth").value.trim() });
    $("#mcp-msg").textContent = `${name} ajouté`;
    $("#mcp-name").value = $("#mcp-url").value = $("#mcp-desc").value = $("#mcp-auth").value = "";
    await loadMcp(); probeServer(name);
  } catch (e) { $("#mcp-msg").textContent = "échec : " + e.message; }
});
$("#mcp-probe-all").addEventListener("click", async () => {
  const m = await api("api/mcp");
  if (!m.servers.length) { $("#mcp-msg").textContent = "aucun serveur à sonder"; return; }
  const out = $("#mcp-probe-out");
  out.textContent = "";
  for (const sv of m.servers) {
    out.textContent += `── ${sv.name} ──\n`;
    const box = $("#mcp-probe-out");
    await probeServer(sv.name);
    out.textContent += box.textContent + "\n\n";
  }
});

/* ──────────────────────── INSTINCTS ──────────────────────── */
async function loadInstincts() {
  if (!S.agents.length) S.agents = await api("api/agents");
  const sel = $("#ins-agent");
  if (sel.options.length <= 1) {
    sel.innerHTML = '<option value="">tous les agents</option>' +
      S.agents.map((a) => `<option value="${esc(a.id)}">${esc(a.emoji)} ${esc(a.name)}</option>`).join("");
  }
  const r = await api("api/instincts");
  $("#ins-count").textContent = `${r.count}`;
  $("#ins-list").innerHTML = r.items.map((i) => `
    <div class="item"><div class="n">${esc(i.rule)}</div>
      <div class="m">${i.agent_id ? esc(i.agent_id) : "tous les agents"} ·
        ${i.hits} renforcement(s) · confiance ${i.confidence.toFixed(2)} ·
        ${esc(i.source)} · ${esc((i.triggers || []).join(", ") || "sans déclencheur")}
        <button class="sm danger" data-forget="${esc(i.id)}">oublier</button></div></div>`).join("")
    || `<div class="empty">Aucun instinct appris. Lance des exécutions : l'OS en déduit.</div>`;
  $$("[data-forget]").forEach((b) => b.addEventListener("click", async () => {
    await fetch(`api/instincts/${b.dataset.forget}`, { method: "DELETE" });
    loadInstincts();
  }));
}
$("#ins-add").addEventListener("click", async () => {
  const rule = $("#ins-rule").value.trim();
  if (!rule) { $("#ins-msg").textContent = "règle requise"; return; }
  try {
    await post("api/instincts", { rule, triggers: $("#ins-triggers").value,
                                  agent_id: $("#ins-agent").value });
    $("#ins-msg").textContent = "enregistré";
    $("#ins-rule").value = $("#ins-triggers").value = "";
    loadInstincts();
  } catch (e) { $("#ins-msg").textContent = "échec : " + e.message; }
});
$("#ins-test").addEventListener("click", async () => {
  const task = $("#ins-task").value.trim();
  if (!task) { $("#ins-preview").textContent = "écris une tâche à tester"; return; }
  const r = await api(`api/instincts?task=${encodeURIComponent(task)}` +
                      `&agent=${encodeURIComponent($("#ins-agent").value)}`);
  $("#ins-preview").textContent = r.injected
    ? r.items.slice(0, r.injected).map((i) =>
        `- ${i.rule}  [score agent ${i.agent_id || "tous"} · ${i.hits}×]`).join("\n")
    : "rien ne serait injecté pour cette tâche — aucun déclencheur ne correspond.";
});

/* ─────────────────── TÂCHES ASYNCHRONES ─────────────────── */
let _tkTimer = null, _tkSel = "";

async function loadTasks() {
  if (!S.agents.length) S.agents = await api("api/agents");
  const sel = $("#tk-agent");
  if (!sel.options.length) {
    sel.innerHTML = S.agents.map((a) =>
      `<option value="${esc(a.id)}"${a.id === "orchestrator" ? " selected" : ""}>${esc(a.emoji)} ${esc(a.name)}</option>`).join("");
  }
  await refreshTasks();
  clearInterval(_tkTimer);
  _tkTimer = setInterval(() => { if ($("#tk-poll").checked) refreshTasks(); }, 2500);
}
async function refreshTasks() {
  const r = await api("api/tasks?limit=25");
  const by = r.summary.by_state;
  $("#tk-count").textContent = r.summary.count;
  $("#tk-states").textContent = Object.entries(by).filter(([, v]) => v)
    .map(([k, v]) => `${k} ${v}`).join(" · ") || "aucune";
  $("#tk-running").textContent = r.summary.running;
  $("#tk-kinds").textContent = Object.keys(by).length;
  $("#tk-list").innerHTML = r.items.map((t) => `
    <div class="item${t.id === _tkSel ? " on" : ""}" data-t="${esc(t.id)}">
      <div class="n">${esc(t.task.slice(0, 70))}</div>
      <div class="m">${esc(t.agent_id)} · <b class="${t.state === "completed" ? "yes" : t.state === "failed" ? "no" : ""}">${esc(t.state)}</b>
        · ${esc(t.id)} · ${t.duration_ms} ms</div>
      <div class="row" style="margin-top:6px">
        <button class="sm primary" data-open="${esc(t.id)}">Ouvrir</button>
        ${["working", "input_required"].includes(t.state) ? `<button class="sm danger" data-cancel="${esc(t.id)}">Annuler</button>` : ""}
        ${t.state === "input_required" ? `<button class="sm" data-ok="${esc(t.id)}">Autoriser</button>` : ""}
      </div>
    </div>`).join("") || `<div class="empty">Aucune tâche lancée.</div>`;
  $$("[data-open]").forEach((b) => b.addEventListener("click", () => { _tkSel = b.dataset.open; openTask(_tkSel); }));
  $$("[data-cancel]").forEach((b) => b.addEventListener("click", async () => {
    await fetch(`api/tasks/${b.dataset.cancel}/cancel`, { method: "POST" }); refreshTasks();
  }));
  $$("[data-ok]").forEach((b) => b.addEventListener("click", async () => {
    const r = await post(`api/tasks/${b.dataset.ok}/approve`, {});
    _tkSel = r.superseded_by; openTask(_tkSel); refreshTasks();
  }));
}
async function openTask(id) {
  const t = await api(`api/tasks/${id}?tail=60`);
  $("#tk-detail-state").textContent = t.state;
  $("#tk-detail-state").className = `badge ${t.state === "completed" ? "ok" : t.state === "failed" ? "err" : "acc"}`;
  const lines = [
    `tâche : ${t.task}`,
    `agent : ${t.agent_id} · approbation ${t.approval}`,
    `état : ${t.state} · ${t.duration_ms} ms`,
    `étapes ${t.progress.steps} · ${nf(t.progress.tokens)} tokens · ${t.progress.events} événements`,
    t.progress.artifacts.length ? `artéfacts : ${t.progress.artifacts.join(", ")}` : "",
    t.progress.pending_tools.length ? `en attente d'autorisation : ${t.progress.pending_tools.join(", ")}` : "",
    t.error ? `erreur : ${t.error}` : "",
    "", "── derniers événements ──",
    ...t.events.map((e) => `${e.type}${e.name ? " " + e.name : ""}` +
      (e.ok === false ? " ✗" : "")).slice(-25),
    "", "── résultat ──", t.result || "(pas encore)",
  ];
  $("#tk-detail").textContent = lines.filter(Boolean).join("\n");
}
$("#tk-submit").addEventListener("click", async () => {
  const task = $("#tk-task").value.trim();
  if (!task) { $("#tk-msg").textContent = "tâche requise"; return; }
  try {
    const r = await post("api/tasks", { task, agent_id: $("#tk-agent").value,
                                        approval: $("#tk-approval").value });
    $("#tk-msg").textContent = `lancée : ${r.id}`;
    _tkSel = r.id; $("#tk-task").value = "";
    await refreshTasks(); openTask(r.id);
  } catch (e) { $("#tk-msg").textContent = "échec : " + e.message; }
});
$("#tk-refresh").addEventListener("click", refreshTasks);

/* ───────────────────────── BARÈME ───────────────────────── */
async function loadEvals() {
  if (!S.agents.length) S.agents = await api("api/agents");
  const sel = $("#ev-agent");
  if (sel.options.length <= 1) {
    sel.innerHTML = '<option value="">tous les agents</option>' +
      S.agents.map((a) => `<option value="${esc(a.id)}">${esc(a.emoji)} ${esc(a.name)}</option>`).join("");
  }
  const r = await api("api/evals");
  $("#ev-suite-n").textContent = `${r.suite.length} cas`;
  $("#ev-suite").textContent = r.suite.map((c) => {
    const wants = [];
    if (c.produces_artifact) wants.push("artéfact");
    if (c.no_tool_failure) wants.push("aucun échec d'outil");
    if (c.confidence) wants.push(`confiance ${c.confidence}`);
    if (c.min_steps) wants.push(`≥ ${c.min_steps} étape(s)`);
    if (c.tools_used.length) wants.push(`outils ${c.tools_used.join("|")}`);
    c.mentions.forEach((m) => wants.push(`mentionne « ${m} »`));
    c.forbidden.forEach((f) => wants.push(`n'écrit pas « ${f} »`));
    return `${c.id}  [${c.agent_id}]\n  ${c.task}\n  attend : ${wants.join(" · ")}`;
  }).join("\n\n");
  paintScorecard(r.last);
}
function paintScorecard(sc) {
  if (!sc) {
    $("#ev-cases").textContent = $("#ev-passed").textContent =
      $("#ev-failed").textContent = $("#ev-ms").textContent = "—";
    $("#ev-list").innerHTML = `<div class="empty">Barème jamais joué — lance-le.</div>`;
    return;
  }
  $("#ev-cases").textContent = sc.cases;
  $("#ev-passed").textContent = sc.passed;
  $("#ev-failed").textContent = sc.failed;
  $("#ev-failed").className = `v ${sc.failed ? "err" : ""}`;
  $("#ev-ms").textContent = `${sc.duration_ms} ms`;
  $("#ev-score").textContent = `${(sc.score * 100).toFixed(0)} % · ${new Date(sc.run_at * 1000).toLocaleString("fr-FR")}`;
  $("#ev-list").innerHTML = sc.results.map((r) => `
    <div class="item"><div class="n">${r.passed ? "✓" : "✗"} ${esc(r.id)}</div>
      <div class="m">${esc(r.agent_id)} · ${r.duration_ms} ms${r.error ? " · " + esc(r.error) : ""}</div>
      <div class="m">${r.checks.map((c) =>
        `<span class="${c.ok ? "yes" : "no"}">${c.ok ? "✓" : "✗"} ${esc(c.check)}</span>`).join("  ")}</div>
      ${r.checks.filter((c) => !c.ok).map((c) => `<div class="m no">↳ ${esc(c.detail || "")}</div>`).join("")}
    </div>`).join("");
}
$("#ev-run").addEventListener("click", async () => {
  $("#ev-run").disabled = true; $("#ev-run").textContent = "en cours…";
  try {
    const sc = await post("api/evals", { agent_id: $("#ev-agent").value });
    paintScorecard(sc);
  } catch (e) { alert("échec : " + e.message); }
  $("#ev-run").disabled = false; $("#ev-run").textContent = "Jouer le barème";
});

/* ───────────────────────── PLUGINS ───────────────────────── */
async function loadPlugins() {
  const r = await api("api/plugins");
  $("#pl-count").textContent = r.count;
  $("#pl-count-d").textContent = r.broken ? `${r.broken} en erreur` : "tous valides";
  $("#pl-active").textContent = r.active;
  $("#pl-skills").textContent = r.skills;
  $("#pl-agents").textContent = r.agents;
  $("#pl-list").innerHTML = r.items.map((p) => `
    <div class="item">
      <div class="n">${esc(p.name)} <span class="m">v${esc(p.version)}</span>
        <span class="badge ${p.status === "ok" ? "ok" : p.status === "erreur" ? "err" : ""}">${esc(p.status)}</span></div>
      <div class="d">${esc(p.description)}</div>
      <div class="m">compétences ${esc(p.skills.join(", ") || "—")} · agents ${esc(p.agents.join(", ") || "—")}</div>
      <div class="m">${esc(p.path)}</div>
      ${p.problems.map((x) => `<div class="m no">· ${esc(x)}</div>`).join("")}
      <div class="row" style="margin-top:6px">
        <button class="sm" data-toggle="${esc(p.name)}" data-on="${p.enabled ? "0" : "1"}">
          ${p.enabled ? "Désactiver" : "Activer"}</button>
        <button class="sm danger" data-uninstall="${esc(p.name)}">Désinstaller</button>
      </div>
    </div>`).join("") || `<div class="empty">Aucun plugin installé.</div>`;
  $$("[data-toggle]").forEach((b) => b.addEventListener("click", async () => {
    await post(`api/plugins/${b.dataset.toggle}/toggle`, { enabled: b.dataset.on === "1" });
    await loadPlugins(); loadStatus();
  }));
  $$("[data-uninstall]").forEach((b) => b.addEventListener("click", async () => {
    if (!confirm(`Désinstaller ${b.dataset.uninstall} ?`)) return;
    await fetch(`api/plugins/${b.dataset.uninstall}?delete_files=true`, { method: "DELETE" });
    await loadPlugins(); loadStatus();
  }));
}
$("#pl-install").addEventListener("click", async () => {
  const path = $("#pl-path").value.trim();
  if (!path) { $("#pl-msg").textContent = "chemin requis"; return; }
  try {
    const r = await post("api/plugins", { path, copy: $("#pl-copy").checked });
    $("#pl-msg").textContent = `${r.plugin.name} installé`;
    $("#pl-path").value = "";
    await loadPlugins(); await loadStatus();
  } catch (e) { $("#pl-msg").textContent = "échec : " + e.message; }
});
$("#pl-sample").addEventListener("click", async () => {
  try {
    const r = await post("api/plugins/sample", {});
    $("#pl-path").value = r.path;
    $("#pl-msg").textContent = "exemple généré — installe-le";
  } catch (e) { $("#pl-msg").textContent = e.message; }
});

/* ───────────────────────── ROUTEUR ───────────────────────── */
async function loadRouter() {
  const [p, m] = await Promise.all([api("api/providers"), api("api/models")]);
  S.providers = p;
  $("#prov-count").textContent = `${p.length}`;
  $("#model-count").textContent = `${m.length}`;
  $("#provider-table").innerHTML = `<thead><tr><th>fournisseur</th><th>clé</th><th>style</th>
    <th class="num">modèles</th><th class="num">quota restant</th><th class="num">priorité</th></tr></thead>
    <tbody>${p.map((x) => `<tr><td><b>${esc(x.name)}</b><br><span class="mono" style="font-size:10.5px;color:var(--tx-4)">${esc(x.env_key || "—")}</span></td>
    <td class="${x.has_key ? "yes" : "no"}">${x.has_key ? "présente" : "absente"}</td>
    <td class="mono">${esc(x.style)}</td><td class="num">${x.models}</td>
    <td class="num">${x.quota_left === null ? "illimité" : nf(x.quota_left)}</td>
    <td class="num">${x.priority}</td></tr>`).join("")}</tbody>`;
  $("#model-table").innerHTML = `<thead><tr><th>modèle</th><th>fournisseur</th><th>état</th>
    <th class="num">contexte</th><th class="num">$/M in</th><th class="num">$/M out</th><th>capacités</th></tr></thead>
    <tbody>${m.map((x) => `<tr><td><b>${esc(x.label)}</b><br><span class="mono" style="font-size:10.5px;color:var(--tx-4)">${esc(x.id)}</span></td>
    <td>${esc(x.provider_name)}</td>
    <td class="${x.ready ? "yes" : "no"}">${x.ready ? "prêt" : (x.has_key ? "cooldown" : "pas de clé")}</td>
    <td class="num">${nf(Math.round(x.context / 1000))} k</td>
    <td class="num">${x.free ? '<span class="free">gratuit</span>' : x.price_in}</td>
    <td class="num">${x.free ? '<span class="free">gratuit</span>' : x.price_out}</td>
    <td class="mono" style="font-size:11px">${[x.vision && "vision", x.tools && "outils", x.reasoning && "raisonnement"].filter(Boolean).join(" · ") || "—"}</td></tr>`).join("")}</tbody>`;
}

/* ───────────────────────── JOURNAUX ───────────────────────── */
async function loadLogs() {
  const [runs, u] = await Promise.all([api("api/runs?limit=60"), api("api/usage")]);
  $("#logs-count").textContent = `${runs.length}`;
  $("#runs-table").innerHTML = `<thead><tr><th>agent</th><th>tâche</th><th>état</th><th>modèle</th>
    <th>mode</th><th class="num">étapes</th><th class="num">tokens</th><th class="num">ms</th><th>phases</th></tr></thead>
    <tbody>${runs.map((r) => `<tr><td class="mono">${esc(r.agent_id)}</td>
    <td>${esc(clip(r.task, 80))}</td>
    <td class="${r.status === "done" ? "yes" : "no"}">${esc(r.status)}</td>
    <td class="mono" style="font-size:11px">${esc(r.model || "—")}</td>
    <td class="mono" style="font-size:11px">${esc(r.mode || "—")}</td>
    <td class="num">${r.steps}</td><td class="num">${nf(r.tokens)}</td><td class="num">${r.duration_ms}</td>
    <td class="mono" style="font-size:10.5px;color:var(--tx-4)">${esc((r.phases || []).join(" → "))}</td></tr>`).join("")
    || '<tr><td colspan="9">aucune exécution</td></tr>'}</tbody>`;
  $("#usage-table").innerHTML = `<thead><tr><th>fournisseur</th><th>modèle</th>
    <th class="num">appels</th><th class="num">tokens</th><th class="num">erreurs</th></tr></thead>
    <tbody>${u.today.map((x) => `<tr><td>${esc(x.provider_id)}</td><td class="mono">${esc(x.model)}</td>
    <td class="num">${x.calls}</td><td class="num">${nf(x.tokens)}</td>
    <td class="num ${x.errors ? "no" : "yes"}">${x.errors}</td></tr>`).join("")
    || '<tr><td colspan="5">rien aujourd\'hui</td></tr>'}</tbody>`;
  $("#usage-total").textContent = `Total historique : ${nf(u.stats.tokens_total)} tokens · ` +
    `${u.stats.runs} exécutions (${u.stats.runs_ok} terminées) · ${u.stats.messages} messages.`;
}

/* ───────────────────────── FICHIERS ───────────────────────── */
async function loadFiles(path) {
  S.filePath = path || "";
  const res = await api(`workspace/${S.filePath}`);
  const rows = Array.isArray(res) ? res : [];
  $("#file-tree").innerHTML = (S.filePath
    ? `<div class="item" data-up><div class="n">↑ ..</div></div>` : "") +
    (rows.map((f) => `<div class="item" data-f="${esc(f.path)}" data-dir="${f.is_dir}">
      <div class="n">${f.is_dir ? "▸ " : "· "}${esc(f.name)}</div></div>`).join("")
      || `<div class="empty">Espace vide — lance une tâche.</div>`);
  $$("[data-up]").forEach((el) => el.addEventListener("click", () => {
    const i = S.filePath.lastIndexOf("/"); loadFiles(i < 0 ? "" : S.filePath.slice(0, i));
  }));
  $$("[data-f]").forEach((el) => el.addEventListener("click", () => {
    el.dataset.dir === "true" ? loadFiles(el.dataset.f) : openFile(el.dataset.f);
  }));
}
$("#f-up").addEventListener("click", () => loadFiles(""));
async function openFile(path) {
  $("#file-title").textContent = path;
  const url = `workspace/${path}`;
  if (/\.(html?|svg|pdf)$/i.test(path)) {
    $("#file-frame").src = url; $("#file-frame").style.display = "";
    $("#file-text").textContent = ""; return;
  }
  $("#file-frame").style.display = "none";
  $("#file-text").textContent = (await (await fetch(url)).text()).slice(0, 24000);
}

/* ───────────────────────── MÉMOIRE ───────────────────────── */
async function loadMemory() {
  const r = await api("api/memory?limit=80");
  $("#mem-count").textContent = `${r.count}`;
  $("#memory-list").innerHTML = r.items.map((i) => `
    <div class="item"><div class="n">[${esc(i.kind)}] ${esc(i.content)}</div>
    <div class="m">${esc(i.agent || "—")} · ${esc((i.tags || []).join(", "))} ·
    ${new Date(i.ts * 1000).toLocaleString("fr-FR")}
    <button class="sm danger" data-forget="${esc(i.id)}">oublier</button></div></div>`).join("")
    || `<div class="empty">Mémoire vide.</div>`;
  $$("[data-forget]").forEach((b) => b.addEventListener("click", async () => {
    await fetch(`api/memory/${b.dataset.forget}`, { method: "DELETE" }); loadMemory(); loadStatus();
  }));
}
$("#btn-memory").addEventListener("click", async () => {
  const content = $("#m-content").value.trim(); if (!content) return;
  await post("api/memory", { content, kind: $("#m-kind").value, tags: $("#m-tags").value });
  $("#m-content").value = ""; loadMemory(); loadStatus();
});

/* ─────────────────── palette de commandes ─────────────────── */
let palItems = [], palSel = 0;
function buildPalette() {
  const cmds = [
    { k: "vue", l: "Mission control", a: () => show("control") },
    { k: "vue", l: "Console", a: () => show("console") },
    { k: "vue", l: "Tableau des tâches", a: () => show("board") },
    { k: "vue", l: "Créateur d'agent", a: () => show("creator") },
    { k: "vue", l: "Harness & portabilité", a: () => show("harness") },
    { k: "vue", l: "Routeur de modèles", a: () => show("router") },
    { k: "vue", l: "Journaux", a: () => show("logs") },
    { k: "vue", l: "Fichiers produits", a: () => show("files") },
    { k: "vue", l: "Mémoire", a: () => show("memory") },
  ];
  const agents = S.agents.map((a) => ({ k: "agent", l: `${a.emoji} ${a.name} — ${a.role}`,
    a: () => { S.agent = a.id; show("console"); $("#run-agent").value = a.id; } }));
  const skills = S.skills.map((s) => ({ k: "skill", l: `${s.name} — ${s.description}`,
    a: () => show("skills") }));
  return [...agents, ...cmds, ...skills];
}
function filterPalette() {
  const q = $("#pal-input").value.toLowerCase();
  const all = buildPalette();
  palItems = (q ? all.filter((i) => i.l.toLowerCase().includes(q)) : all).slice(0, 40);
  palSel = 0; drawPalette();
}
function drawPalette() {
  $("#pal-list").innerHTML = palItems.map((i, n) =>
    `<div class="pal-item${n === palSel ? " sel" : ""}" data-i="${n}">
      <span class="k">${esc(i.k)}</span><span class="l">${esc(i.l)}</span></div>`).join("")
    || `<div class="empty">Rien ne correspond.</div>`;
  $$(".pal-item").forEach((el) => el.addEventListener("click", () => runPalette(+el.dataset.i)));
}
function runPalette(i) {
  const it = palItems[i]; if (!it) return;
  closePalette(); it.a();
}
function openPalette() {
  $("#palette-modal").classList.remove("hidden");
  $("#pal-input").value = ""; filterPalette(); $("#pal-input").focus();
}
function closePalette() { $("#palette-modal").classList.add("hidden"); }
$("#open-palette").addEventListener("click", openPalette);
$("#pal-input").addEventListener("input", filterPalette);
$("#pal-input").addEventListener("keydown", (e) => {
  if (e.key === "ArrowDown") { palSel = Math.min(palSel + 1, palItems.length - 1); drawPalette(); e.preventDefault(); }
  if (e.key === "ArrowUp") { palSel = Math.max(palSel - 1, 0); drawPalette(); e.preventDefault(); }
  if (e.key === "Enter") { runPalette(palSel); e.preventDefault(); }
  if (e.key === "Escape") closePalette();
});
$("#palette-modal").addEventListener("click", (e) => { if (e.target.id === "palette-modal") closePalette(); });
document.addEventListener("keydown", (e) => {
  if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") { e.preventDefault(); openPalette(); }
});

/* ───────────────────────── dialogue ───────────────────────── */
function dialog(title, body) {
  $("#dlg-title").textContent = title; $("#dlg-body").textContent = body;
  $("#dialog").classList.remove("hidden");
}
$("#dlg-close").addEventListener("click", () => $("#dialog").classList.add("hidden"));
$("#dialog").addEventListener("click", (e) => { if (e.target.id === "dialog") $("#dialog").classList.add("hidden"); });

/* ───────────────────────── démarrage ───────────────────────── */
(async function boot() {
  try {
    await Promise.all([loadStatus(), loadAgents(), loadModelOptions()]);
    await loadControl();
  } catch (e) {
    $("#stream").innerHTML = ""; $("#stream").appendChild(
      evNode("err", "démarrage", e.message));
  }
  $("#stream").appendChild(evNode("phase", "prêt",
    "NEXUS·OS en ligne. Choisis un mode d'exécution, décris la tâche, lance.\n" +
    "⌘K ouvre la palette : agents, compétences, commandes."));
})();
