/* ============================================================================
   CARRÉ D'AS — Assistant (« JARVIS ») : guidage vocal et visuel
   ----------------------------------------------------------------------------
   Principes (hérités du projet) :
     · sans clé, il fonctionne : le mode « règles » ne dépend d'aucun service ;
     · il ne fait rien sans trace : chaque action est annoncée et journalisée ;
     · le micro et la voix sont optionnels et désactivables en un clic ;
     · s'il y a un modèle local (Ollama), il l'utilise ; sinon il le dit.

   Référence d'inspiration (MIT) : adewaskar/jarvis — assistant navigateur,
   visage holographique, mot de réveil, barge-in, mode dégradé.
   ========================================================================== */
(function () {
  "use strict";

  const state = {
    mode: "idle",            // idle · listening · thinking · speaking
    voiceOn: true,
    micAvailable: false,
    recognition: null,
    listening: false,
    voice: null,
    llm: null,               // {url, model} si l'utilisateur en a configuré un
    log: [],
    onAction: null           // callback fourni par le shell (navigation, recherche)
  };

  /* ----------------------------------------------------------- utilitaires */
  const norm = (s) => (s || "")
    .toString().toLowerCase()
    .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
    .replace(/['\u2019]/g, " ")          // c'est → c est
    .replace(/[^a-z0-9\s-]/g, " ")
    .replace(/\s+/g, " ").trim();

  /** Similarité simple : inclusion + recouvrement de mots. */
  function score(query, text) {
    const q = norm(query), t = norm(text);
    if (!q) return 0;
    if (t === q) return 100;
    if (t.includes(q)) return 80 - Math.min(20, t.length - q.length);
    const qw = q.split(" ").filter((w) => w.length > 2);
    if (!qw.length) return 0;
    const tw = new Set(t.split(" "));
    let hit = 0;
    qw.forEach((w) => { if (tw.has(w) || t.includes(w)) hit++; });
    return (hit / qw.length) * 60;
  }

  function registry() { return window.CARRE_REGISTRY || { modules: [], doors: [] }; }

  function allFeatures() {
    const out = [];
    registry().modules.forEach((m) => m.features.forEach((f) => out.push({ m, f })));
    return out;
  }

  /* --------------------------------------------------------------- moteur */
  const RULES = [
    {
      // « ouvre le module BTP », « va sur la carte », « montre-moi les documents »
      test: (q) => /^\s*(ouvre|ouvrir|va|aller|affiche|afficher|montre|montrer|voir|navigue|module)\b/.test(q),
      run: (q) => {
        // on retire les verbes et articles pour ne comparer que le nom du module
        const wanted = q.replace(/\b(ouvre|ouvrir|va|aller|affiche|afficher|montre|montrer|voir|navigue|module|sur|les|des|du|le|la|moi|un|une|au|aux)\b/g, " ").replace(/\s+/g, " ").trim();
        const base = wanted || q;
        const cands = registry().modules.map((m) => ({ m, s: Math.max(score(base, m.label), score(base, m.id), score(base, m.tagline || "")) }));
        const doorCands = (registry().doors || []).map((d) => ({ m: { id: d.id, label: d.label, icon: d.icon, features: [] }, s: score(base, d.label), door: true }));
        const best = cands.concat(doorCands).sort((a, b) => b.s - a.s)[0];
        if (!best || best.s < 30) return { say: "Je n'ai pas reconnu de module. Essayez « ouvre le BTP », « ouvre la carte », « montre les agents »." };
        state.onAction && state.onAction({ type: best.door ? "door" : "module", id: best.m.id });
        const n = best.m.features ? best.m.features.length : 0;
        return { say: `J'ouvre ${best.m.label}.${n ? ` ${n} fonctionnalités dans ce module.` : ""}`, action: "navigate" };
      }
    },
    {
      // « cherche », « trouve », « où est la décroissance ? »
      test: (q) => /\b(cherche|chercher|trouve|trouver|ou est|où est|recherche|qui fait|quoi fait)\b/.test(q),
      run: (q) => {
        const wanted = q.replace(/\b(cherche|chercher|trouve|trouver|ou est|recherche|qui fait|quoi fait)\b/g, " ").trim();
        const hits = allFeatures()
          .map((x) => ({ ...x, s: rankFeature(wanted, x.f) }))
          .filter((x) => x.s >= 14)
          .sort((a, b) => b.s - a.s).slice(0, 4);
        if (!hits.length) return { say: `Rien trouvé pour « ${wanted || q} ». Il y a ${allFeatures().length} fonctionnalités : demandez par exemple « cherche métrés ».` };
        state.onAction && state.onAction({ type: "search", q: wanted });
        const lines = hits.map((h) => `${h.f.n} (${h.m.label})`).join(" ; ");
        return { say: `${hits.length} résultat${hits.length > 1 ? "s" : ""} : ${lines}.`, hits, action: "search" };
      }
    },
    {
      // « où en est le projet », « état », « combien de modules »
      test: (q) => /\b(etat|où en est|ou en est|avancement|combien|bilan|statut)\b/.test(q),
      run: () => {
        const ms = registry().modules;
        const feats = allFeatures();
        const by = { dispo: 0, "a-porter": 0, "a-construire": 0 };
        feats.forEach((x) => by[x.f.s] = (by[x.f.s] || 0) + 1);
        return {
          say: `${ms.length} modules, ${feats.length} fonctionnalités : ${by.dispo} déjà disponibles, ${by["a-porter"]} à porter depuis les branches, ${by["a-construire"]} à construire. Aucune fonctionnalité n'est perdue : chacune indique sa source.`,
          action: "status"
        };
      }
    },
    {
      // « qu'est-ce que le contrat de module », « explique… »
      test: (q) => /\b(explique|qu est ce que|kesako|késako|c est quoi|definition|comment marche|pourquoi)\b/.test(q),
      run: (q) => {
        const wanted = q.replace(/\b(explique|expliquer|qu est ce que|kesako|c est quoi|ca veut dire quoi|definition|comment marche|pourquoi)\b/g, " ")
          .replace(/\b(le|la|les|un|une|des|du|de|d|l)\b/g, " ").replace(/\s+/g, " ").trim();
        const hits = allFeatures()
          .map((x) => ({ ...x, s: rankFeature(wanted, x.f) }))
          .filter((x) => x.s >= 40).sort((a, b) => b.s - a.s).slice(0, 3);
        if (!hits.length) return { say: "Je peux expliquer chaque fonctionnalité listée dans le registre. Demandez par exemple « explique la synchronisation »." };
        state.onAction && state.onAction({ type: "search", q: wanted });
        const h = hits[0];
        return { say: `${h.f.n}, dans le module ${h.m.label}. ${h.f.d} Source : ${h.f.src}. Statut : ${statusLabel(h.f.s)}.`, hits, action: "explain" };
      }
    },
    {
      // commandes de confort
      test: (q) => /\b(silence|stop|arrete|tais toi|chut|pause)\b/.test(q),
      run: () => { stopSpeaking(); return { say: "", silent: true }; }
    },
    {
      test: (q) => /\b(aide|aide moi|que peux tu|commandes|help)\b/.test(q),
      run: () => ({
        say: "Je peux : ouvrir un module (« ouvre le BTP »), chercher une fonctionnalité (« cherche métrés »), expliquer (« explique la décroissance »), faire le point (« où en est le projet »), et lire à voix haute. Le micro ne s'active que si vous le demandez.",
        action: "help"
      })
    }
  ];


  /** Classement d'une fonctionnalité : le nom pèse plus que la description. */
  function rankFeature(q, f) {
    const STOP = /^(le|la|les|de|du|des|un|une|au|aux|et|ou|en|sur|pour|avec|dans|que|qui|est)$/;
    const qw = norm(q).split(" ").filter((w) => w.length > 1 && !STOP.test(w));
    if (!qw.length) return 0;
    const nw = norm(f.n).split(/[\s()—·,]+/).filter(Boolean);
    const dw = norm(f.d).split(/[\s()—·,]+/).filter(Boolean);
    const stem = (w) => w.slice(0, Math.max(4, w.length - 1));   // tolère le pluriel/majuscule
    let s = 0;
    qw.forEach((w) => {
      const st = stem(w);
      if (nw.some((x) => x.startsWith(st))) s += 40;             // le nom contient le mot
      else if (nw.some((x) => x.startsWith(w.slice(0, 4)))) s += 18;
      else if (dw.some((x) => x.startsWith(st))) s += 14;         // la description le contient
    });
    return s;
  }

  function statusLabel(s) {
    return ({ dispo: "disponible", "a-porter": "à porter depuis les branches", "a-construire": "à construire" })[s] || s;
  }

  function reason(q) {
    const nq = norm(q);
    for (const r of RULES) if (r.test(nq)) return r.run(nq);
    // réponse par défaut : recherche floue globale
    const hits = allFeatures().map((x) => ({ ...x, s: rankFeature(nq, x.f) }))
      .filter((x) => x.s >= 40).sort((a, b) => b.s - a.s).slice(0, 3);
    if (hits.length) {
      state.onAction && state.onAction({ type: "search", q });
      return { say: `Je comprends « ${q} » comme une recherche. ${hits.map((h) => `${h.f.n} (${h.m.label})`).join(" ; ")}.`, hits, action: "search" };
    }
    return { say: "Je n'ai pas compris. Dites « aide » pour voir ce que je sais faire, ou tapez Ctrl+K pour chercher." };
  }

  /* ---------------------------------------------------------------- parole */
  function pickVoice() {
    if (!("speechSynthesis" in window)) return null;
    const vs = speechSynthesis.getVoices();
    if (!vs.length) return null;
    return vs.find((v) => /^fr/i.test(v.lang) && /google|amelie|thomas|audrey|marie/i.test(v.name))
        || vs.find((v) => /^fr/i.test(v.lang)) || vs[0];
  }
  function stopSpeaking() {
    try { window.speechSynthesis && speechSynthesis.cancel(); } catch (_) {}
    setMode("idle");
  }
  function speak(text) {
    if (!text) return;
    if (!state.voiceOn || !("speechSynthesis" in window)) { setMode("idle"); return; }
    stopSpeaking();
    const u = new SpeechSynthesisUtterance(text);
    if (!state.voice) state.voice = pickVoice();
    if (state.voice) { u.voice = state.voice; u.lang = state.voice.lang || "fr-FR"; } else { u.lang = "fr-FR"; }
    u.rate = 1.02; u.pitch = 1.0; u.volume = 1;
    u.onstart = () => setMode("speaking");
    u.onend = () => setMode("idle");
    u.onerror = () => setMode("idle");
    try { speechSynthesis.speak(u); } catch (_) { setMode("idle"); }
  }

  /* -------------------------------------------------------------- écoute */
  function initMic() {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) { state.micAvailable = false; return; }
    state.micAvailable = true;
    const r = new SR();
    r.lang = "fr-FR"; r.continuous = false; r.interimResults = false; r.maxAlternatives = 1;
    r.onstart = () => { state.listening = true; setMode("listening"); };
    r.onend = () => { state.listening = false; if (state.mode === "listening") setMode("idle"); };
    r.onerror = (e) => {
      state.listening = false; setMode("idle");
      if (e && (e.error === "not-allowed" || e.error === "service-not-allowed")) {
        emit("bot", "Le micro est refusé par le navigateur. Vous pouvez toujours écrire — ou cliquer sur le micro pour redemander l'autorisation.");
      }
    };
    r.onresult = (ev) => {
      const txt = ev.results[0][0].transcript;
      emit("me", txt);
      ask(txt);
    };
    state.recognition = r;
  }
  function toggleListening() {
    if (!state.micAvailable) { initMic(); }
    if (!state.recognition) {
      emit("bot", "Ce navigateur ne propose pas la reconnaissance vocale (Chrome/Edge le font). L'écrit fonctionne partout — c'est le mode garanti.");
      return;
    }
    try {
      if (state.listening) { state.recognition.stop(); }
      else { stopSpeaking(); state.recognition.start(); }
    } catch (_) { /* déjà démarré */ }
  }

  /* ------------------------------------------------------------ dialogue */
  function emit(who, text, opts) {
    state.log.push({ who, text, t: Date.now() });
    const el = document.getElementById("assist-log");
    if (el) {
      const d = document.createElement("div");
      d.className = "msg " + (who === "me" ? "me" : "bot");
      d.innerHTML = opts && opts.html ? text : escapeHtml(text).replace(/« ([^»]+) »/g, "« <b>$1</b> »");
      el.appendChild(d);
      el.scrollTop = el.scrollHeight;
    }
    if (who !== "me") document.dispatchEvent(new CustomEvent("carre:assist", { detail: { text } }));
  }
  function escapeHtml(s) { return (s || "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])); }

  /** Point d'entrée : on demande quelque chose à l'assistant. */
  async function ask(text) {
    if (!text || !text.trim()) return;
    setMode("thinking");
    const q = text.trim();
    let answer = null;

    // 1) modèle local si configuré (et joignable)
    if (state.llm && state.llm.url) {
      try {
        const ms = registry().modules.map((m) => `${m.label} (${m.features.length})`).join(", ");
        const res = await fetch(`${state.llm.url.replace(/\/$/, "")}/api/chat`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            model: state.llm.model || "llama3.2",
            stream: false,
            messages: [
              { role: "system", content: `Tu es l'assistant de Carré d'As, une application locale. Modules : ${ms}. Réponds en français, en 2 phrases maximum, sans inventer de fonctionnalité.` },
              { role: "user", content: q }
            ]
          })
        });
        if (res.ok) {
          const j = await res.json();
          const msg = (j.message && j.message.content) || j.response;
          if (msg) answer = { say: msg.trim(), action: "llm" };
        }
      } catch (_) { /* on retombe sur les règles, sans bruit */ }
    }

    // 2) moteur de règles (toujours disponible, hors ligne)
    if (!answer) answer = reason(q);

    if (answer.say) emit("bot", answer.say);
    if (answer.say) speak(answer.say);
    else setMode("idle");
    return answer;
  }

  function setMode(m) {
    state.mode = m;
    document.querySelectorAll(".orb").forEach((o) => o.setAttribute("data-state", m));
    document.querySelectorAll(".wave").forEach((w) => w.setAttribute("data-on", m === "listening" || m === "speaking" ? "1" : "0"));
    document.dispatchEvent(new CustomEvent("carre:mode", { detail: m }));
  }

  window.CarreAssistant = {
    init(opts) {
      state.onAction = (opts && opts.onAction) || null;
      initMic();
      if ("speechSynthesis" in window) {
        speechSynthesis.onvoiceschanged = () => { state.voice = pickVoice(); };
        state.voice = pickVoice();
      }
      try { const s = JSON.parse(localStorage.getItem("carre.assistant") || "{}"); if (s.llm) state.llm = s.llm; if (typeof s.voiceOn === "boolean") state.voiceOn = s.voiceOn; } catch (_) {}
      return this;
    },
    ask,
    emit,
    speak,
    stopSpeaking,
    toggleListening,
    micAvailable: () => state.micAvailable,
    mode: () => state.mode,
    setVoiceOn(v) { state.voiceOn = !!v; if (!v) stopSpeaking(); try { localStorage.setItem("carre.assistant", JSON.stringify({ llm: state.llm, voiceOn: state.voiceOn })); } catch (_) {} },
    voiceOn: () => state.voiceOn,
    /** Configurer un modèle local (Ollama). Sans cela, l'assistant marche quand même. */
    setLocalModel(cfg) { state.llm = cfg; try { localStorage.setItem("carre.assistant", JSON.stringify({ llm: cfg, voiceOn: state.voiceOn })); } catch (_) {} },
    /**
     * Vérifie sincèrement si un modèle local répond.
     * @returns {Promise<boolean>}
     */
    async probeLocalModel(url = "http://127.0.0.1:11434") {
      try {
        const r = await fetch(`${url.replace(/\/$/, "")}/api/tags`, { method: "GET" });
        return r.ok;
      } catch (_) { return false; }
    }
  };
})();
