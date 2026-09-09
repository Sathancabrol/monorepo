/* NEXUS·OS — interface « bureau ». Vanilla JS, aucune dépendance, URLs relatives
   (fonctionne monté sous /os/ comme en racine). */
"use strict";

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) =>
  ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

const state = {
  agents: [], skills: [], models: [], providers: [],
  agent: "orchestrator", chain: new Set(), es: null, draft: null,
};

/* ------------------------------------------------------------------ API --- */
async function api(path, opts = {}) {
  const res = await fetch(path, {
    headers: opts.body ? { "Content-Type": "application/json" } : {},
    ...opts,
  });
  if (!res.ok) {
    let detail = res.statusText;
    try { detail = (await res.json()).detail || detail; } catch {}
    throw new Error(`${res.status} ${detail}`);
  }
  return res.json();
}

/* ------------------------------------------------------------- navigation - */
function show(view) {
  $$(".view").forEach((v) => v.classList.toggle("active", v.id === `view-${view}`));
  $$(".dock-btn").forEach((b) => b.classList.toggle("active", b.dataset.view === view));
  const loaders = { agents: loadAgents, skills: loadSkills, router: loadRouter,
                    logs: loadLogs, files: loadFiles, memory: loadMemory };
  loaders[view]?.();
}
$$(".dock-btn").forEach((b) => b.addEventListener("click", () => show(b.dataset.view)));
$$("[data-goto]").forEach((b) => b.addEventListener("click", () => show(b.dataset.goto)));

/* ---------------------------------------------------------------- statut -- */
async function loadStatus() {
  const s = await api("api/status");
  const badge = $("#mode-badge");
  const live = s.mode_info.mode === "live";
  badge.textContent = live ? "LIVE · " + (s.mode_info.providers_ready.join(", ") || "—")
                           : "HORS-LIGNE · moteur local";
  badge.className = "badge " + (live ? "badge-live" : "badge-off");
  $("#stat-models").textContent = `modèles ${s.mode_info.models_ready}/${s.mode_info.models_total}`;
  $("#stat-agents").textContent = `agents ${s.runtime.agents}`;
  $("#stat-skills").textContent = `compétences ${s.runtime.skills}`;
  $("#stat-memory").textContent = `mémoire ${s.runtime.memory_items}`;
  $("#flag-shell").textContent = `shell ${s.flags.shell ? "on" : "off"}`;
  $("#flag-shell").className = "chip chip-flag" + (s.flags.shell ? " yes" : "");
}

/* ---------------------------------------------------------------- agents -- */
async function loadAgents() {
  state.agents = await api("api/agents");
  // sélecteur de la console
  $("#run-agent").innerHTML = state.agents
    .map((a) => `<option value="${esc(a.id)}">${esc(a.emoji)} ${esc(a.name)} — ${esc(a.role)}</option>`)
    .join("");
  $("#run-agent").value = state.agent;
  // sélecteur de chaîne
  $("#chain-picker").innerHTML = state.agents
    .filter((a) => a.id !== "orchestrator")
    .map((a) => `<button class="ghost chain" data-id="${esc(a.id)}">${esc(a.emoji)} ${esc(a.name)}</button>`)
    .join("");
  $$(".chain").forEach((b) => b.addEventListener("click", () => {
    const id = b.dataset.id;
    state.chain.has(id) ? state.chain.delete(id) : state.chain.add(id);
    b.style.borderColor = state.chain.has(id) ? "var(--acc)" : "";
    b.style.color = state.chain.has(id) ? "#fff" : "";
  }));
  // cartes
  $("#agent-grid").innerHTML = state.agents.map((a) => `
    <div class="card">
      <div class="top">
        <div class="emo">${esc(a.emoji)}</div>
        <div><div class="nm">${esc(a.name)}</div><div class="rl">${esc(a.role)}</div></div>
      </div>
      <div class="ds">${esc(a.description)}</div>
      <div class="pills">
        ${a.skills.map((s) => `<span class="pill s">${esc(s)}</span>`).join("")}
        ${a.tools.slice(0, 6).map((t) => `<span class="pill t">${esc(t)}</span>`).join("")}
        ${a.tools.length > 6 ? `<span class="pill">+${a.tools.length - 6}</span>` : ""}
        <span class="pill b">${esc(a.source)}</span>
        <span class="pill">${esc(a.autonomy)}</span>
      </div>
      <div class="pills"><span class="pill">${esc(a.lifecycle.join(" → "))}</span></div>
      <div class="acts">
        <button class="primary" data-run="${esc(a.id)}">Ouvrir</button>
        <button data-md="${esc(a.id)}">Spec</button>
        ${a.source === "user" ? `<button class="danger" data-del="${esc(a.id)}">Supprimer</button>` : ""}
      </div>
    </div>`).join("");

  $$("[data-run]").forEach((b) => b.addEventListener("click", () => {
    state.agent = b.dataset.run; $("#run-agent").value = state.agent; show("console");
  }));
  $$("[data-md]").forEach((b) => b.addEventListener("click", async () => {
    const d = await api(`api/agents/${b.dataset.md}`);
    modal(`${d.spec.emoji} ${d.spec.name} — spec exportable`, d.markdown);
  }));
  $$("[data-del]").forEach((b) => b.addEventListener("click", async () => {
    if (!confirm(`Supprimer l'agent ${b.dataset.del} ?`)) return;
    await fetch(`api/agents/${b.dataset.del}`, { method: "DELETE" });
    await Promise.all([loadAgents(), loadStatus()]);
  }));
}

/* --------------------------------------------------------------- console -- */
const SUGGESTIONS = [
  "Audite la structure du dépôt et propose un diagramme d'architecture",
  "Fais la revue de sécurité de nexus_os/tools.py",
  "Rédige la page d'accueil de NEXUS·OS : promesse, preuve, mécanisme, objection, action",
  "Quelles compétences de l'OS sont réellement utilisées par les agents intégrés ?",
  "Crée un agent qui relit les contrats et extrait les clauses risquées",
  "Analyse la consommation de tokens du jour et dis-moi ce qu'elle ne permet pas de conclure",
];

function stream(url, onEvent) {
  $("#btn-stop").disabled = false;
  $("#run-status").textContent = "en cours";
  $("#run-status").className = "badge badge-run";
  const es = new EventSource(url);
  state.es = es;
  es.onmessage = (m) => {
    let ev; try { ev = JSON.parse(m.data); } catch { return; }
    if (ev.type === "stream_close") { es.close(); state.es = null;
      $("#btn-stop").disabled = true; $("#run-status").textContent = "terminé";
      $("#run-status").className = "badge"; loadStatus(); loadLogs(); return; }
    onEvent(ev);
  };
  es.onerror = () => { es.close(); state.es = null; $("#btn-stop").disabled = true;
    $("#run-status").textContent = "interrompu"; $("#run-status").className = "badge"; };
}

function evNode(cls, tag, text) {
  const d = document.createElement("div");
  d.className = `ev ${cls}`;
  d.innerHTML = `<span class="tag">${esc(tag)}</span>${esc(text)}`;
  return d;
}

function renderEvent(ev) {
  const box = $("#stream");
  const push = (cls, tag, text) => { box.appendChild(evNode(cls, tag, text));
    box.scrollTop = box.scrollHeight; };
  switch (ev.type) {
    case "run_start":
      $("#phases").innerHTML = ev.phases.map((p) => `<span class="ph" data-p="${esc(p)}">${esc(p)}</span>`).join("");
      push("ev-phase", "run", `${ev.agent.emoji} ${ev.agent.name} · ${ev.mode} · ${ev.task}`);
      break;
    case "routing":
      push("ev-route", "routage", ev.candidates
        .map((c) => `${c.emoji} ${c.name} — ${c.score}`).join("\n")
        + (ev.chosen ? `\n→ délégué à ${ev.chosen.name}` : "\n→ traité par l'orchestrateur"));
      break;
    case "phase": {
      $$(".ph").forEach((p) => { p.classList.remove("now");
        if (p.dataset.p === ev.phase) p.classList.add("now");
        else if (p.classList.contains("now")) p.classList.add("done"); });
      const el = $(`.ph[data-p="${ev.phase}"]`); if (el) el.classList.add("now");
      push("ev-phase", `phase ${ev.index}/${ev.total}`, ev.title);
      break;
    }
    case "thinking":
      if (ev.text?.trim()) push("ev-think", `${ev.model} · ${ev.mode}`, ev.text);
      break;
    case "tool_call":
      push("ev-tool", "outil", `${ev.name}(${JSON.stringify(ev.args).slice(0, 400)})`);
      break;
    case "tool_result":
      push(ev.ok ? "ev-ok" : "ev-err", `${ev.name} ${ev.ok ? "→" : "✗"}`, ev.result);
      break;
    case "artifact":
      push("ev-ok", "artefact", ev.path);
      break;
    case "agent_created":
      push("ev-ok", "agent créé", `${ev.agent.emoji} ${ev.agent.name} (${ev.agent.id})\n` +
        (ev.rationale || []).join("\n"));
      break;
    case "handoff":
      push("ev-route", "délégation", `→ ${ev.to} : ${ev.task}`);
      break;
    case "consolidation":
      push("ev-route", "consolidation", `retour de ${ev.from}`);
      break;
    case "message": {
      const label = ev.depth > 0 ? `réponse du spécialiste · ${ev.model}`
                                 : `réponse · ${ev.model}`;
      const d = evNode("ev-msg", label, ev.depth > 0
        ? ev.text.split("\n").slice(0, 8).join("\n") + "\n…" : ev.text);
      if (ev.depth > 0) d.style.opacity = ".72";
      box.appendChild(d); box.scrollTop = box.scrollHeight;
      break;
    }
    case "error":
      push("ev-err", "erreur", ev.message);
      break;
    case "run_end":
      push("ev-phase", "fin", `${ev.steps} étapes · ${ev.tokens} tokens · ${ev.duration_ms} ms · ${ev.mode}`);
      break;
    case "result":
      push("ev-phase", "chaîne terminée", `${ev.runs.length} agent(s) exécuté(s)`);
      break;
    case "log":
      push("ev-think", "log", ev.message);
      break;
  }
}

function currentTask() {
  const t = $("#run-task").value.trim();
  if (!t) { alert("Écris une tâche."); }
  return t;
}

$("#btn-run").addEventListener("click", () => {
  const task = currentTask(); if (!task) return;
  state.agent = $("#run-agent").value;
  $("#stream").innerHTML = "";
  stream(`api/run?task=${encodeURIComponent(task)}&agent=${encodeURIComponent(state.agent)}`,
    renderEvent);
});

$("#btn-pipeline").addEventListener("click", () => {
  const task = currentTask(); if (!task) return;
  if (!state.chain.size) { alert("Choisis au moins un agent dans la chaîne."); return; }
  $("#stream").innerHTML = "";
  stream(`api/pipeline?task=${encodeURIComponent(task)}&agents_chain=${encodeURIComponent([...state.chain].join(","))}`,
    renderEvent);
});

$("#btn-route").addEventListener("click", async () => {
  const task = currentTask(); if (!task) return;
  const r = await api("api/route", { method: "POST", body: JSON.stringify({ task }) });
  $("#route-hint").innerHTML = "<b>Qui doit traiter&nbsp;?</b><br>" + r.ranking
    .map((c) => `${esc(c.emoji)} ${esc(c.name)} — score ${c.score}`).join("<br>")
    + (r.suggested ? `<br>→ recommandé : <b>${esc(r.suggested.name)}</b>` : "");
});

$("#btn-stop").addEventListener("click", () => state.es?.close());
$("#suggestions").innerHTML = SUGGESTIONS.map((s) => `<button class="sugg">${esc(s)}</button>`).join("");
$$(".sugg").forEach((b) => b.addEventListener("click", () => { $("#run-task").value = b.textContent; }));

/* -------------------------------------------------------------- créateur -- */
async function loadModelOptions() {
  state.models = await api("api/models");
  $("#c-model").innerHTML = '<option value="">routeur automatique</option>' +
    state.models.filter((m) => m.ready || m.free).map((m) =>
      `<option value="${esc(m.id)}">${esc(m.provider_name)} — ${esc(m.label)}${m.free ? " (gratuit)" : ""}</option>`
    ).join("");
}

$("#btn-draft").addEventListener("click", async () => {
  const description = $("#c-desc").value.trim();
  if (!description) { alert("Décris le métier de l'agent."); return; }
  $("#c-msg").textContent = "génération…";
  try {
    const r = await api("api/agents/draft", { method: "POST", body: JSON.stringify({
      description, name: $("#c-name").value.trim(), model: $("#c-model").value,
      autonomy: $("#c-autonomy").value, use_llm: $("#c-llm").checked,
    })});
    state.draft = r.spec;
    $("#c-spec").value = JSON.stringify(r.spec, null, 2);
    $("#c-rationale").innerHTML = r.rationale.map((x) => `<li>${esc(x)}</li>`).join("") +
      `<li>moteur : <b>${esc(r.engine)}</b></li><li>${esc(r.test_recipe)}</li>`;
    $("#c-msg").textContent = "Brouillon prêt. Modifie la spec si besoin, puis enregistre.";
    $("#btn-save").disabled = false;
  } catch (e) { $("#c-msg").textContent = "échec : " + e.message; }
});

$("#btn-save").addEventListener("click", async () => {
  let spec;
  try { spec = JSON.parse($("#c-spec").value); }
  catch (e) { $("#c-msg").textContent = "JSON invalide : " + e.message; return; }
  try {
    const r = await api("api/agents", { method: "POST", body: JSON.stringify(spec) });
    $("#c-msg").textContent = `agent enregistré : ${r.agent.id}`;
    await Promise.all([loadAgents(), loadStatus()]);
  } catch (e) { $("#c-msg").textContent = "échec : " + e.message; }
});

/* ------------------------------------------------------------ compétences -- */
async function loadSkills() {
  state.skills = await api("api/skills");
  $("#skill-list").innerHTML = state.skills.map((s) => `
    <div class="item" data-skill="${esc(s.name)}">
      <div class="n">${esc(s.name)}</div>
      <div class="d">${esc(s.description)}</div>
      <div class="meta">${esc(s.tags.join(", "))} · ${esc(s.source)} · ${esc(s.tools.join(", ") || "sans outil")}</div>
    </div>`).join("");
  $$("[data-skill]").forEach((el) => el.addEventListener("click", async () => {
    const s = await api(`api/skills/${el.dataset.skill}`);
    $("#skill-title").textContent = s.name;
    $("#skill-body").textContent = s.body;
  }));
  state.skills[0] && $$("[data-skill]")[0].click();
}

/* ---------------------------------------------------------------- routeur - */
async function loadRouter() {
  const [providers, models] = await Promise.all([api("api/providers"), api("api/models")]);
  $("#provider-table").innerHTML = `<table><thead><tr>
    <th>fournisseur</th><th>clé</th><th>style</th><th>modèles</th><th>quota restant</th><th>priorité</th>
    </tr></thead><tbody>${providers.map((p) => `<tr>
      <td><b>${esc(p.name)}</b><br><span class="meta">${esc(p.env_key || "—")}</span></td>
      <td class="${p.has_key ? "yes" : "no"}">${p.has_key ? "présente" : "absente"}</td>
      <td>${esc(p.style)}</td><td>${p.models}</td>
      <td>${p.quota_left === null ? "illimité" : p.quota_left.toLocaleString("fr-FR")}</td>
      <td>${p.priority}</td></tr>`).join("")}</tbody></table>`;
  $("#model-table").innerHTML = `<table><thead><tr>
    <th>modèle</th><th>fournisseur</th><th>état</th><th>contexte</th><th>$/M in</th><th>$/M out</th><th>capacités</th>
    </tr></thead><tbody>${models.map((m) => `<tr>
      <td><b>${esc(m.label)}</b><br><span class="meta">${esc(m.id)}</span></td>
      <td>${esc(m.provider_name)}</td>
      <td class="${m.ready ? "yes" : "no"}">${m.ready ? "prêt" : (m.has_key ? "cooldown" : "pas de clé")}</td>
      <td>${(m.context / 1000).toLocaleString("fr-FR")} k</td>
      <td>${m.free ? '<span class="free">gratuit</span>' : m.price_in}</td>
      <td>${m.free ? '<span class="free">gratuit</span>' : m.price_out}</td>
      <td class="meta">${[m.vision && "vision", m.tools && "outils", m.reasoning && "raisonnement"]
        .filter(Boolean).join(", ") || "—"}</td></tr>`).join("")}</tbody></table>`;
}

/* ---------------------------------------------------------------- journaux - */
async function loadLogs() {
  const [runs, usage] = await Promise.all([api("api/runs"), api("api/usage")]);
  $("#runs-table").innerHTML = `<table><thead><tr><th>agent</th><th>tâche</th><th>état</th>
    <th>modèle</th><th>mode</th><th>étapes</th><th>tokens</th><th>ms</th><th>phases</th></tr></thead>
    <tbody>${runs.map((r) => `<tr>
      <td>${esc(r.agent_id)}</td><td>${esc((r.task || "").slice(0, 90))}</td>
      <td class="${r.status === "done" ? "yes" : "no"}">${esc(r.status)}</td>
      <td class="meta">${esc(r.model || "—")}</td><td>${esc(r.mode || "—")}</td>
      <td>${r.steps}</td><td>${r.tokens}</td><td>${r.duration_ms}</td>
      <td class="meta">${esc((r.phases || []).join(" → "))}</td></tr>`).join("")
      || '<tr><td colspan="9">aucune exécution</td></tr>'}</tbody></table>`;
  $("#usage-table").innerHTML = `<table><thead><tr><th>fournisseur</th><th>modèle</th>
    <th>appels</th><th>tokens</th><th>erreurs</th></tr></thead><tbody>
    ${usage.today.map((u) => `<tr><td>${esc(u.provider_id)}</td><td>${esc(u.model)}</td>
      <td>${u.calls}</td><td>${u.tokens.toLocaleString("fr-FR")}</td>
      <td class="${u.errors ? "no" : "yes"}">${u.errors}</td></tr>`).join("")
      || '<tr><td colspan="5">aucune consommation aujourd\'hui</td></tr>'}</tbody></table>
    <p class="note">Total historique : ${usage.stats.tokens_total.toLocaleString("fr-FR")} tokens ·
    ${usage.stats.runs} exécutions (${usage.stats.runs_ok} terminées) · ${usage.stats.messages} messages.</p>`;
}

/* ---------------------------------------------------------------- fichiers - */
async function loadFiles(path = "") {
  const res = await api(`workspace/${path}`);
  const rows = Array.isArray(res) ? res : [];
  $("#file-tree").innerHTML = (path ? `<div class="item" data-f="${esc(parentPath(path))}">
      <div class="n">..</div></div>` : "") +
    (rows.map((f) => `<div class="item" data-f="${esc(f.path)}" data-dir="${f.is_dir}">
      <div class="n">${f.is_dir ? "📁 " : "📄 "}${esc(f.name)}</div></div>`).join("")
      || '<div class="note">Espace vide — lance une tâche pour produire des artefacts.</div>');
  $$("[data-f]").forEach((el) => el.addEventListener("click", () => {
    if (el.dataset.dir === "true") return loadFiles(el.dataset.f);
    if (el.dataset.f === parentPath(path)) return loadFiles(el.dataset.f);
    openFile(el.dataset.f);
  }));
}
function parentPath(p) { const i = p.lastIndexOf("/"); return i < 0 ? "" : p.slice(0, i); }

async function openFile(path) {
  $("#file-title").textContent = path;
  const url = `workspace/${path}`;
  if (/\.(html?|svg|pdf)$/i.test(path)) {
    $("#file-frame").src = url; $("#file-frame").style.display = "";
    $("#file-text").textContent = ""; return;
  }
  $("#file-frame").style.display = "none";
  const txt = await (await fetch(url)).text();
  $("#file-text").textContent = txt.slice(0, 20000);
}

/* ----------------------------------------------------------------- mémoire - */
async function loadMemory() {
  const r = await api("api/memory?limit=60");
  $("#memory-list").innerHTML = r.items.map((i) => `<div class="item">
      <div class="n">[${esc(i.kind)}] ${esc(i.content)}</div>
      <div class="meta">${esc(i.agent || "—")} · ${esc((i.tags || []).join(", "))} ·
        ${new Date(i.ts * 1000).toLocaleString("fr-FR")}
        <button class="ghost danger" data-forget="${esc(i.id)}" style="padding:1px 7px;font-size:10px">oublier</button>
      </div></div>`).join("")
    || `<div class="note">Mémoire vide (${r.count} item).</div>`;
  $$("[data-forget]").forEach((b) => b.addEventListener("click", async () => {
    await fetch(`api/memory/${b.dataset.forget}`, { method: "DELETE" }); loadMemory(); loadStatus();
  }));
}
$("#btn-memory").addEventListener("click", async () => {
  const content = $("#m-content").value.trim();
  if (!content) return;
  await api("api/memory", { method: "POST", body: JSON.stringify({
    content, kind: $("#m-kind").value, tags: $("#m-tags").value }) });
  $("#m-content").value = ""; loadMemory(); loadStatus();
});

/* ------------------------------------------------------------------- modal - */
function modal(title, body) {
  $("#modal-title").textContent = title;
  $("#modal-body").textContent = body;
  $("#modal").classList.remove("hidden");
}
$("#modal-close").addEventListener("click", () => $("#modal").classList.add("hidden"));
$("#modal").addEventListener("click", (e) => { if (e.target.id === "modal") $("#modal").classList.add("hidden"); });

/* -------------------------------------------------------------------- boot - */
(async function boot() {
  try {
    await Promise.all([loadStatus(), loadAgents(), loadModelOptions()]);
  } catch (e) {
    $("#stream").innerHTML = `<div class="ev ev-err"><span class="tag">boot</span>${esc(e.message)}</div>`;
  }
  $("#stream").innerHTML = `<div class="ev ev-phase"><span class="tag">prêt</span>` +
    `NEXUS·OS en ligne. Choisis un agent, décris la tâche, lance.\n` +
    `Le routeur choisit le modèle ; sans clé API, le moteur local exécute quand même les outils.</div>`;
})();
