"""Moteur des agents : routage, cycle de vie, exécution.

Adapté de `nexus_os` (branche `arena/01a08385-monorepo` — 22 agents, 59 tests
au vert). Deux choix délibérés, qui s'expliquent par l'échéance :

1. **Le routage est déterministe.** nexus_os sait appeler un modèle pour
   choisir ; ici on marque les déclencheurs par mots-clés et on pondère par
   spécificité. Ça fonctionne sans clé, sans réseau, et surtout c'est
   **reproductible** — la même demande donne le même agent, ce qui est une
   qualité quand un tiers doit pouvoir revérifier.

2. **Chaque phase du cycle fait quelque chose de réel.** Un cycle qui se
   contente d'afficher « étape 2/6 » est une décoration. Ici :
   `plan` découpe, `recherche` interroge les registres locaux, `production`
   fabrique un document avec `docsgen`, `revue` passe les affirmations au
   crible des règles d'admissibilité, `vérification` mesure le résultat,
   `mémoire` consigne l'exécution.
"""

from __future__ import annotations

import datetime as _dt
import json
import re
import unicodedata
from pathlib import Path

ICI = Path(__file__).parent
DONNEES = ICI / "data"

CYCLE = ("plan", "recherche", "production", "revue", "verification", "memoire")

PHASES = {
    "plan": "Découper la demande et désigner qui fait quoi",
    "recherche": "Chercher dans les registres locaux avant de produire",
    "production": "Fabriquer le document",
    "revue": "Passer les affirmations au crible de l'admissibilité",
    "verification": "Mesurer ce qui a été produit",
    "memoire": "Consigner l'exécution",
}


# --------------------------------------------------------------- utilitaires
def _sans_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s or "")
                   if unicodedata.category(c) != "Mn")


def normaliser(texte: str) -> str:
    """Minuscules, sans accents, sans ponctuation : la clé du routage."""
    t = _sans_accents(texte or "").lower()
    return re.sub(r"[^a-z0-9œæ'’ ]+", " ", t).strip()


def _maintenant() -> str:
    return _dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def charger_agents() -> list[dict]:
    try:
        return json.loads((DONNEES / "agents.json").read_text(encoding="utf-8"))["agents"]
    except Exception:
        return []


def agent(agent_id: str) -> dict | None:
    for a in charger_agents():
        if a["id"] == agent_id:
            return a
    return None


# ------------------------------------------------------------------- routage
def router(texte: str, limite: int = 5) -> list[dict]:
    """Qui doit traiter cette demande ?

    Pondération : un déclencheur long (« résume la réunion ») vaut plus qu'un
    mot court (« note »), parce qu'il est plus spécifique. Un déclencheur en
    début de phrase vaut un peu plus aussi — on formule souvent son besoin au
    début.
    """
    t = normaliser(texte)
    mots = set(t.split())
    if not t:
        return []
    out = []
    for a in charger_agents():
        score, marques = 0.0, []
        for d in (a.get("declencheurs") or []):
            nd = normaliser(d)
            if not nd:
                continue
            if nd in t:
                # spécificité : nombre de mots du déclencheur
                poids = 1.0 + (len(nd.split()) - 1) * 0.6
                if t.startswith(nd):
                    poids += 0.5
                score += poids
                marques.append(d)
            elif nd in mots:
                score += 0.4
                marques.append(d)
        if score > 0:
            out.append({"agent": a, "score": round(score, 2),
                        "declencheurs": marques})
    out.sort(key=lambda x: -x["score"])
    return out[:limite]


def choisir(texte: str, agent_id: str | None = None) -> dict:
    """L'agent désigné, ou le meilleur, ou l'orchestrateur en dernier recours."""
    if agent_id:
        a = agent(agent_id)
        if a:
            return a
    r = router(texte, 1)
    if r:
        return r[0]["agent"]
    return next((a for a in charger_agents() if a.get("defaut")), charger_agents()[0])


# ------------------------------------------------------- phase : plan
def _plan(demande: str, a: dict, contexte: dict) -> tuple[list[str], dict]:
    """Découpe en étapes. Utilise le réel quand il existe."""
    etapes = [f"{a['emoji']} {a['nom']} prend la demande : « {demande.strip()} »"]
    session = contexte.get("session")
    if session:
        if session.get("decisions"):
            etapes.append(f"Reprend les {len(session['decisions'])} décisions déjà actées")
        if session.get("actions"):
            etapes.append(f"Reprend les {len(session['actions'])} actions déjà extraites")
    for phase in (a.get("cycle") or []):
        if phase in PHASES:
            etapes.append(f"{phase} — {PHASES[phase]}")
    return etapes, {"agent": a["id"], "etapes": len(etapes)}


# -------------------------------------------------- phase : recherche
def _chercher(termes: list[str]) -> dict:
    """Interroge les registres locaux. Ne sort jamais de la machine."""
    outils, sources = [], []
    try:
        from ..osint.registries import fusionner
        reg = fusionner()
        for o in reg.get("outils", []):
            champs = " ".join(str(o.get(k, "")) for k in
                              ("nom", "description", "usage", "categorie")).lower()
            if any(t in champs for t in termes):
                outils.append({"id": o.get("id"), "nom": o.get("nom"),
                               "licence": o.get("licence"),
                               "registre": o.get("registre")})
    except Exception:
        pass
    src_path = ICI.parent / "watchtower" / "data" / "sources.json"
    try:
        reg = json.loads(src_path.read_text(encoding="utf-8"))
        for s in reg.get("sources", []):
            champs = " ".join(str(s.get(k, "")) for k in
                              ("nom", "contenu", "domaine", "licence")).lower()
            if any(t in champs for t in termes):
                sources.append({"id": s.get("id"), "nom": s.get("nom"),
                                "acces": s.get("acces"), "usage": s.get("usage"),
                                "licence": s.get("licence")})
    except Exception:
        pass
    # on n'affiche que ce qui est utilisable par une collectivité en premier
    sources.sort(key=lambda s: (s.get("usage") != "oui", s.get("nom", "")))
    return {"outils": outils[:8], "sources": sources[:8],
            "termes": termes,
            "vide": not outils and not sources}


# ------------------------------------------------- phase : production
def _doc_generique(demande, a, recherche, contexte, etapes) -> dict:
    blocs: list[dict] = [
        {"type": "h2", "texte": "Demande"},
        {"type": "p", "texte": demande.strip()},
        {"type": "h2", "texte": "Qui traite"},
        {"type": "kv", "items": [
            ["Agent", f"{a['emoji']} {a['nom']}"],
            ["Rôle", a.get("role", "")],
            ["Sortie attendue", ", ".join(a.get("sorties") or []) or "—"],
        ]},
        {"type": "h2", "texte": "Étapes"},
        {"type": "ol", "items": etapes},
    ]
    session = contexte.get("session")
    if session:
        if session.get("decisions"):
            blocs += [{"type": "h2", "texte": "Décisions reprises"},
                      {"type": "ul", "items": [d.get("texte", "")
                                               for d in session["decisions"]]}]
        if session.get("actions"):
            blocs += [{"type": "h2", "texte": "Actions reprises"},
                      {"type": "table",
                       "entetes": ["Action", "Responsable", "Échéance"],
                       "lignes": [[x.get("texte", ""), x.get("responsable") or "—",
                                   x.get("echeance") or "—"] for x in session["actions"]]}]
    if recherche["outils"]:
        blocs += [{"type": "h2", "texte": "Outils trouvés dans les registres"},
                  {"type": "table",
                   "entetes": ["Outil", "Licence", "Registre"],
                   "lignes": [[o["nom"], o.get("licence") or "—",
                               o.get("registre") or "—"] for o in recherche["outils"]]}]
    if recherche["sources"]:
        blocs += [{"type": "h2", "texte": "Sources de données mobilisables"},
                  {"type": "table",
                   "entetes": ["Source", "Accès", "Usage collectivité", "Licence"],
                   "lignes": [[s["nom"], s.get("acces") or "—",
                               {"oui": "oui", "condition": "sous condition",
                                "non": "NON COMMERCIAL"}.get(s.get("usage"), "?"),
                               s.get("licence") or "—"] for s in recherche["sources"]]}]
    if recherche["vide"]:
        blocs.append({"type": "note",
                      "texte": "Aucun outil ni source du registre local ne correspond "
                               "à cette demande. Rien n'a été inventé pour combler : "
                               "c'est une information, pas un échec."})
    return {"titre": f"{a['emoji']} {a['nom']} — {demande.strip()[:70]}",
            "sous_titre": a.get("role", ""),
            "meta": {"Produit le": _maintenant(),
                     "Agent": f"{a['id']} · v{a.get('version', '1.0')}"},
            "blocs": blocs}


def _doc_planning(demande, a, recherche, contexte, etapes) -> tuple[dict, list]:
    """Planning : les actions réelles de la réunion, ou un phasage par défaut."""
    session = contexte.get("session")
    taches = []
    if session and session.get("actions"):
        for i, x in enumerate(session["actions"], 1):
            taches.append({
                "id": i, "titre": x.get("texte", "")[:60],
                "debut": x.get("echeance") or "", "fin": "",
                "responsable": x.get("responsable") or "—",
                "avancement": 0,
            })
    if not taches:
        for i, etape in enumerate(etapes[:5], 1):
            taches.append({"id": i, "titre": etape[:60], "debut": "", "fin": "",
                           "responsable": "—", "avancement": 0})
    doc = _doc_generique(demande, a, recherche, contexte, etapes)
    doc["titre"] = f"📋 Planning — {demande.strip()[:70]}"
    doc["blocs"] = [
        {"type": "h2", "texte": "Phasage"},
        {"type": "table",
         "entetes": ["#", "Tâche", "Responsable", "Échéance", "Avancement"],
         "lignes": [[t["id"], t["titre"], t["responsable"], t["debut"] or "à fixer",
                     f"{t['avancement']} %"] for t in taches]},
        {"type": "note",
         "texte": "Le diagramme de Gantt est produit séparément au format .svg."},
    ] + doc["blocs"][4:]
    return doc, taches


def _doc_budget(demande, a, recherche, contexte, etapes) -> dict:
    """Budget : on ne sort que des montants réellement présents."""
    session = contexte.get("session")
    lignes, total = [], 0.0
    for x in ((session or {}).get("actions") or []):
        m = x.get("montant")
        if isinstance(m, (int, float)) and m:
            lignes.append([x.get("texte", "")[:60], x.get("responsable") or "—",
                           f"{m:,.0f}".replace(",", " "), "€"])
            total += float(m)
    doc = _doc_generique(demande, a, recherche, contexte, etapes)
    doc["titre"] = f"📊 Budget — {demande.strip()[:70]}"
    if lignes:
        doc["blocs"] = [
            {"type": "h2", "texte": "Postes chiffrés"},
            {"type": "table",
             "entetes": ["Poste", "Responsable", "Montant", "Unité"], "lignes": lignes},
            {"type": "h2", "texte": "Total"},
            {"type": "kv", "items": [["Total des postes connus",
                                      f"{total:,.0f}".replace(",", " ") + " €"],
                                     ["Postes sans montant",
                                      str(len([x for x in ((session or {}).get('actions') or [])
                                               if not x.get('montant')]))]]},
        ] + doc["blocs"][4:]
    else:
        doc["blocs"] = [
            {"type": "note",
             "texte": "Aucun montant chiffré n'a été trouvé dans les éléments de la "
                      "réunion. Ce document ne fabrique pas de budget à leur place : "
                      "renseignez les montants, il se remplira."},
        ] + doc["blocs"][4:]
    return doc


PRODUCTEURS = {"pm": _doc_planning, "analyst": _doc_budget}


# ------------------------------------------------------------- exécution
def executer(demande: str, agent_id: str | None, contexte: dict, store) -> dict:
    """Une demande traverse les six phases. Chacune laisse une trace."""
    from ... import docsgen
    from ...core import admissibilite
    from ...store import new_id

    t0 = _dt.datetime.now()
    demande = (demande or "").strip()
    contexte = contexte or {}
    a = choisir(demande, agent_id)
    journal: list[dict] = []

    def phase(nom):
        def _f(statut, detail, **extra):
            journal.append({"phase": nom, "intitule": PHASES.get(nom, nom),
                            "statut": statut, "detail": detail, **extra})
        return _f

    # --- plan
    p = phase("plan")
    etapes, meta_plan = _plan(demande, a, contexte)
    p("ok", f"{len(etapes)} étapes", **meta_plan)

    # --- recherche
    p = phase("recherche")
    termes = [m for m in normaliser(demande).split()
              if len(m) > 3][:6] or normaliser(demande).split()[:3]
    # les graines de l'agent complètent une demande trop pauvre en termes
    for g in (a.get("cherche") or []):
        ng = normaliser(g)
        if ng and ng not in termes:
            termes.append(ng)
    recherche = _chercher(termes)
    p("ok" if not recherche["vide"] else "vide",
      f"{len(recherche['outils'])} outil(s), {len(recherche['sources'])} source(s)")

    # --- production
    p = phase("production")
    producteur = PRODUCTEURS.get(a["id"])
    taches = []
    if producteur:
        res = producteur(demande, a, recherche, contexte, etapes)
        doc, taches = (res if isinstance(res, tuple) else (res, []))
    else:
        doc = _doc_generique(demande, a, recherche, contexte, etapes)
    p("ok", f"{len(doc['blocs'])} blocs")

    # --- revue : les affirmations passent au crible.
    #     On distingue ce qui BLOQUE de ce qui se SIGNALE. Une ligne de
    #     tableau reprise d'une réunion est « inconnue » par nature : c'est un
    #     signalement, pas une faute. Les confondre rendrait la revue inutile.
    p = phase("revue")
    bloquants, signalements = [], []
    for b in doc["blocs"]:
        if b.get("type") != "table":
            continue
        for lig in (b.get("lignes") or []):
            rec = {"id": "doc", "type": "ligne", "source": "session",
                   "status": "unknown", "label": " ".join(str(x) for x in lig)[:120]}
            _, pr = admissibilite.admissible(rec)
            for x in pr:
                (bloquants if x["gravite"] == "bloquant" else signalements).append(x)
    problems = bloquants
    p("ok" if not bloquants else "bloque",
      f"{len(bloquants)} bloquant(s), {len(signalements)} signalement(s)",
      bloquants=len(bloquants), signalements=len(signalements))

    # --- vérification : on mesure
    p = phase("verification")
    md = docsgen.to_markdown(doc)
    p("ok", f"{len(md)} caractères, {len(taches)} tâche(s)",
      caracteres=len(md))

    # --- mémoire
    p = phase("memoire")
    tid = new_id("agt")
    duree = (_dt.datetime.now() - t0).total_seconds()
    trace = {"id": tid, "demande": demande, "agent": a["id"],
             "termes": termes, "phases": journal,
             "caracteres": len(md), "duree_s": round(duree, 3),
             "cree_le": _maintenant(), "taches": len(taches),
             "problemes": len(problems), "signalements": len(signalements),
             "outils": len(recherche["outils"]), "sources": len(recherche["sources"])}
    try:
        store.put("agenttaches", tid, trace)
        p("ok", f"consigné sous {tid}")
    except Exception as exc:
        p("echec", str(exc))

    return {"tache": trace, "agent": a, "document": doc, "taches_gantt": taches,
            "recherche": recherche, "problemes": problems,
            "signalements": signalements, "duree_s": round(duree, 3)}


def historique(store, limite: int = 20) -> list[dict]:
    out = sorted(store.all("agenttaches"),
                 key=lambda x: x.get("cree_le", ""), reverse=True)
    return out[:limite]
