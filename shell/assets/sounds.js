/* ============================================================================
   CARRÉ D'AS — Sons d'interface (`sounds.js`)
   Objectif : des sons de retour, discrets, **synthétisés localement** :
   aucun fichier à télécharger, aucune licence à gérer, fonctionne hors ligne.

   Inspiration et alternative « fichiers » : le pack **uisfx** (romainsimon/uisfx)
   — code MIT, audio dédié au domaine public (CC0), dont la personnalité
   « scifi » (« Clean holographic pings and restrained digital shimmer ») est
   exactement le registre recherché. Pour l'utiliser :
     1) déposer les fichiers dans  shell/assets/sfx/  (ex. sfx/scifi/open.mp3)
     2) appeler  CarreSounds.loadPack("scifi")
   → si les fichiers sont absents, on retombe automatiquement sur la synthèse.
   ========================================================================== */
(function () {
  "use strict";

  const CUES = ["boot", "open", "close", "tick", "confirm", "cancel", "error", "ping", "sweep"];

  // Recettes de synthèse (oscillateur + enveloppe) — accordées sur la palette Void/Plasticity
  const RECIPES = {
    boot:    { type: "sine",     f0: 220,  f1: 660,  dur: .55, gain: .16, sweep: true },
    open:    { type: "triangle", f0: 520,  f1: 880,  dur: .16, gain: .10, sweep: true },
    close:   { type: "triangle", f0: 720,  f1: 380,  dur: .16, gain: .09, sweep: true },
    tick:    { type: "square",   f0: 1200, f1: 1200, dur: .035, gain: .035 },
    confirm: { type: "sine",     f0: 880,  f1: 1320, dur: .22, gain: .11, sweep: true },
    cancel:  { type: "sine",     f0: 440,  f1: 260,  dur: .20, gain: .10, sweep: true },
    error:   { type: "sawtooth", f0: 200,  f1: 140,  dur: .32, gain: .10 },
    ping:    { type: "sine",     f0: 1760, f1: 1760, dur: .30, gain: .07, decay: true },
    sweep:   { type: "sine",     f0: 300,  f1: 1500, dur: .40, gain: .07, sweep: true }
  };

  let ctx = null, master = null, enabled = true, volume = 0.5, pack = null;

  function ensure() {
    if (ctx) return ctx;
    const AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return null;
    ctx = new AC();
    master = ctx.createGain();
    master.gain.value = volume;
    master.connect(ctx.destination);
    return ctx;
  }

  function synth(cue) {
    const c = ensure(); if (!c) return;
    if (c.state === "suspended") c.resume();
    const r = RECIPES[cue] || RECIPES.tick;
    const t0 = c.currentTime;
    const osc = c.createOscillator();
    const g = c.createGain();
    osc.type = r.type;
    osc.frequency.setValueAtTime(r.f0, t0);
    if (r.sweep && r.f1 !== r.f0) osc.frequency.exponentialRampToValueAtTime(r.f1, t0 + r.dur);
    g.gain.setValueAtTime(0.0001, t0);
    g.gain.exponentialRampToValueAtTime(r.gain, t0 + 0.012);
    g.gain.exponentialRampToValueAtTime(0.0001, t0 + r.dur);
    osc.connect(g); g.connect(master);
    osc.start(t0); osc.stop(t0 + r.dur + 0.03);
  }

  function file(cue) {
    if (!pack) return null;
    const a = new Audio(`assets/sfx/${pack}/${cue}.mp3`);
    a.volume = volume;
    return a;
  }

  const CarreSounds = {
    /** Jouer un son. `cue` ∈ CUES. Ne jette jamais (le son n'est pas critique). */
    play(cue) {
      if (!enabled) return;
      try {
        const a = file(cue);
        if (a && pack) { a.play().catch(() => synth(cue)); return; }
        synth(cue);
      } catch (_) { /* silencieux */ }
    },
    /** Activer/désactiver tous les sons (réglage utilisateur). */
    setEnabled(v) { enabled = !!v; CarreSounds.persist(); },
    isEnabled() { return enabled; },
    setVolume(v) { volume = Math.max(0, Math.min(1, v)); if (master) master.gain.value = volume; CarreSounds.persist(); },
    /** Charger un pack de fichiers (optionnel) : déposer les .mp3 dans assets/sfx/<pack>/. */
    loadPack(name) { pack = name; CarreSounds.persist(); },
    loadPackIfPresent() {
      // si un pack a été mémorisé et que le premier fichier est joignable, on l'utilise
      try {
        const saved = JSON.parse(localStorage.getItem("carre.sounds") || "{}");
        if (saved.pack) {
          const probe = new Audio(`assets/sfx/${saved.pack}/tick.mp3`);
          probe.addEventListener("canplaythrough", () => { pack = saved.pack; }, { once: true });
          probe.addEventListener("error", () => { pack = null; }, { once: true });
        }
      } catch (_) {}
    },
    persist() {
      try { localStorage.setItem("carre.sounds", JSON.stringify({ enabled, volume, pack })); } catch (_) {}
    },
    restore() {
      try {
        const s = JSON.parse(localStorage.getItem("carre.sounds") || "{}");
        if (typeof s.enabled === "boolean") enabled = s.enabled;
        if (typeof s.volume === "number") volume = s.volume;
      } catch (_) {}
    },
    cues: CUES
  };

  CarreSounds.restore();
  CarreSounds.loadPackIfPresent();
  window.CarreSounds = CarreSounds;
})();
