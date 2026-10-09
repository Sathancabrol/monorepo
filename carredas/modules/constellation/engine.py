"""Moteur de la Constellation : trois lectures d'un même monde.

Inspiré de l'atlas Frontignan (`projects/_incoming/.../frontignan/atlas/`),
qui faisait déjà « trois lectures d'un même graphe : réseau (Obsidian), carte
heuristique, slides ». Ici, adapté à Carré d'As et branché sur les données
live de l'application :

- **constellation** — les objets d'intérêt (entités, concepts, compétences
  métier, acteurs, projets, risques) : l'atlas du bassin de Thau (79 nœuds,
  167 liens) augmenté des objets créés dans l'app (profils, réunions, cas).
- **planetaire** — le soleil = Carré d'As, les planètes = les modules chargés,
  les satellites = les objets qu'ils produisent. Métaphore de CosmoGraph
  (plugin Obsidian) mais rendue en 2D : des orbites, pas du WebGL.
- **agentique** — les 22 agents du système agentique, reliés quand ils
  partagent un déclencheur ou une capacité.

Un graphe = {"noeuds": [...], "liens": [...], "meta": {...}}. Chaque nœud
porte au minimum {id, label, type}. Le client fait le layout (force ou
orbital) — le serveur ne calcule que la structure.
"""

from __future__ import annotations

import json
from pathlib import Path

ICI = Path(__file__).parent
DONNEES = ICI / "data"

SYSTEMES = ("constellation", "planetaire", "agentique")

SYSTEMES_INFO = {
    "constellation": {
        "titre": "Constellation",
        "metaphore": "Ciel étoilé — style Obsidian",
        "icone": "✺",
        "resume": "Les objets d'intérêt : entités, concepts, compétences métier, "
                  "acteurs, projets, risques du bassin de Thau.",
    },
    "planetaire": {
        "titre": "Système planétaire",
        "metaphore": "Un soleil, des planètes, des satellites — style CosmoGraph",
        "icone": "🪐",
        "resume": "Carré d'As au centre, les modules en orbite, leurs objets en satellites.",
    },
    "agentique": {
        "titre": "Système agentique",
        "metaphore": "Un réseau de spécialistes",
        "icone": "⬢",
        "resume": "Les 22 agents, reliés par leurs déclencheurs et leurs capacités.",
    },
}

TYPE_COULEURS = {
    "territoire": "#2FA8C4", "commune": "#4FC3A1", "acteur": "#E4B33C",
    "projet": "#E1734F", "risque": "#D8595B", "politique": "#9B87D4",
    "ressource": "#79B36B", "futur": "#6C8AE4", "data": "#8FA3AC",
    # types ajoutés pour les objets live et le planétaire
    "module": "#C9D4E0", "soleil": "#F0D264", "satellite": "#8FA3AC",
    "agent": "#7FB3E8", "concept": "#9B87D4", "competence": "#79B36B",
    "organisation": "#E4B33C", "personne": "#E4B33C", "objet": "#8FA3AC",
}


def _charger_atlas() -> dict:
    try:
        return json.loads((DONNEES / "atlas.json").read_text(encoding="utf-8"))
    except Exception:
        return {"meta": {}, "typeColors": {}, "nodes": [], "links": [],
                "roots": [], "datasets": {}, "slides": []}


# ------------------------------------------------------- objets live (app)
def _objets_live(store) -> tuple[list[dict], list[dict]]:
    """Les objets créés dans l'application, ajoutés à la constellation.

    Chaque objet garde sa collection d'origine : on ne recopie pas les données,
    on les référence. Un lien « appartient à » les rattache à leur module.
    """
    noeuds, liens = [], []
    specs = [
        ("reunions", "session", "Réunion", "📅"),
        ("profils", "organisation", "Profil", "◍"),
        ("osintcas", "objet", "Cas OSINT", "🛰️"),
        ("prevscen", "futur", "Scénario", "◷"),
        ("agenttaches", "concept", "Exécution agent", "⬢"),
    ]
    for collection, type_, prefixe, icone in specs:
        try:
            recs = store.all(collection)
        except Exception:
            recs = []
        for r in recs[:40]:
            rid = r.get("id", "")
            if not rid:
                continue
            noeuds.append({
                "id": f"{collection}:{rid}",
                "label": (r.get("titre") or r.get("demande")
                          or r.get("nom") or rid)[:60],
                "type": type_, "tier": 4, "icon": icone,
                "collection": collection, "ref": rid,
                "sub": r.get("cree_le", "")[:10],
            })
            liens.append({"source": f"{collection}:{rid}",
                          "target": f"module:{collection}",
                          "type": "orbite", "weight": 1, "label": ""})
    return noeuds, liens


# ---------------------------------------------------------- les 3 graphes
def graphe_constellation(store) -> dict:
    """L'atlas du bassin de Thau + les objets live de l'app."""
    atlas = _charger_atlas()
    noeuds = []
    for n in atlas.get("nodes", []):
        noeuds.append({
            "id": n["id"], "label": n.get("label", n["id"]),
            "type": n.get("type", "objet"), "tier": n.get("tier", 1),
            "icon": n.get("icon", ""), "sub": n.get("sub", ""),
            "parent": n.get("parent", ""), "img": n.get("img", ""),
            "dataset": n.get("dataset", ""),
            "couleur": TYPE_COULEURS.get(n.get("type", ""), "#8FA3AC"),
        })
    liens = [{"source": l["source"], "target": l["target"],
              "type": l.get("type", "lien"), "weight": l.get("weight", 1),
              "label": l.get("label", "")} for l in atlas.get("links", [])]
    live_n, live_l = _objets_live(store)
    ids = {n["id"] for n in noeuds}
    for n in live_n:
        if n["id"] not in ids:
            noeuds.append(n)
    for l in live_l:
        if l["target"] not in ids and l["target"].startswith("module:"):
            # le nœud module est créé par le système planétaire ; on le crée ici
            # pour que le lien existe, en satellite neutre
            noeuds.append({"id": l["target"], "label": l["target"].split(":", 1)[1],
                           "type": "module", "tier": 3, "icon": "▣",
                           "couleur": TYPE_COULEURS["module"]})
            ids.add(l["target"])
        if l["source"] in ids and l["target"] in ids:
            liens.append(l)
    return {
        "noeuds": noeuds, "liens": liens,
        "meta": {
            "titre": atlas.get("meta", {}).get("titre", "Constellation"),
            "sous_titre": atlas.get("meta", {}).get("sous_titre", ""),
            "methode": atlas.get("meta", {}).get("methode", ""),
            "echelles": atlas.get("meta", {}).get("echelles", []),
            "systeme": "constellation",
            "nb_noeuds": len(noeuds), "nb_liens": len(liens),
            "couleurs": TYPE_COULEURS,
            "datasets": list((atlas.get("datasets") or {}).keys()),
        },
    }


def graphe_planetaire(store, modules) -> dict:
    """Soleil = Carré d'As · planètes = modules · satellites = leurs objets."""
    noeuds = [{"id": "carredas", "label": "Carré d'As", "type": "soleil",
               "tier": 0, "icon": "◈", "sub": "le point d'accès",
               "couleur": TYPE_COULEURS["soleil"], "rayon": 26}]
    liens = []
    # planètes : une par module actif, rayon d'orbite selon la priorité
    actifs = [m for m in modules if m.get("actif")]
    actifs.sort(key=lambda m: m.get("priorite", 50))
    for i, m in enumerate(actifs):
        pid = f"module:{m['id']}"
        noeuds.append({"id": pid, "label": m.get("titre", m["id"]),
                       "type": "module", "tier": 1, "icon": m.get("icone", "▣"),
                       "sub": m.get("resume", "")[:80],
                       "couleur": TYPE_COULEURS["module"], "orbite": i,
                       "module_id": m["id"], "version": m.get("version", "")})
        liens.append({"source": "carredas", "target": pid,
                      "type": "orbite", "weight": 1, "label": ""})
    # satellites : les objets des collections connues, rattachés à leur planète
    satellites = [
        ("reunions", "reunion", "📅"), ("profils", "profil", "◍"),
        ("osintcas", "cas", "🛰️"), ("prevscen", "scénario", "◷"),
        ("agenttaches", "exécution", "⬢"), ("cartopoints", "point", "▦"),
        ("references", "référence", "¶"),
    ]
    par_module = {"reunion": "meeting", "profil": "cognitorium",
                  "cas": "osint", "scénario": "forecast",
                  "exécution": "agents", "point": "watchtower",
                  "référence": "cognitorium"}
    for collection, type_, icone in satellites:
        try:
            recs = store.all(collection)
        except Exception:
            recs = []
        module_id = par_module.get(type_, "meeting")
        for r in recs[:25]:
            rid = r.get("id", "")
            if not rid:
                continue
            noeuds.append({"id": f"{collection}:{rid}",
                           "label": (r.get("titre") or r.get("demande")
                                     or r.get("nom") or rid)[:48],
                           "type": "satellite", "tier": 2, "icon": icone,
                           "sub": r.get("cree_le", "")[:10],
                           "couleur": TYPE_COULEURS["satellite"],
                           "planete": f"module:{module_id}",
                           "collection": collection, "ref": rid})
            liens.append({"source": f"module:{module_id}",
                          "target": f"{collection}:{rid}",
                          "type": "satellite", "weight": 1, "label": ""})
    return {
        "noeuds": noeuds, "liens": liens,
        "meta": {"titre": "Système planétaire",
                 "sous_titre": "Carré d'As au centre, les modules en orbite, "
                               "leurs objets en satellites",
                 "systeme": "planetaire",
                 "nb_noeuds": len(noeuds), "nb_liens": len(liens),
                 "couleurs": TYPE_COULEURS},
    }


def graphe_agentique(store) -> dict:
    """Les 22 agents, reliés par déclencheurs et capacités partagés."""
    try:
        from ..agents import engine as E
        agents = E.charger_agents()
    except Exception:
        agents = []
    noeuds = [{"id": f"agent:{a['id']}", "label": a["nom"], "type": "agent",
               "tier": 1, "icon": a.get("emoji", "⬢"),
               "sub": a.get("role", "")[:80],
               "couleur": TYPE_COULEURS["agent"],
               "capacites": a.get("capacites", []),
                       "sorties": a.get("sorties", []),
                       "defaut": bool(a.get("defaut"))}
              for a in agents]
    # un nœud central : l'orchestrateur
    noeuds.append({"id": "agent:orchestrator-hub", "label": "Orchestration",
                   "type": "concept", "tier": 0, "icon": "🧭",
                   "sub": "découpe, délègue, consolide",
                   "couleur": TYPE_COULEURS["concept"]})
    liens, vus = [], set()

    def _lien(a, b, label):
        k = tuple(sorted((a, b)))
        if k in vus or a == b:
            return
        vus.add(k)
        liens.append({"source": a, "target": b, "type": "coopere",
                      "weight": 1, "label": label})

    for a in agents:
        _lien("agent:orchestrator-hub", f"agent:{a['id']}", "délègue à")
        for b in agents:
            if a["id"] >= b["id"]:
                continue
            communs = set(a.get("declencheurs") or []) & set(b.get("declencheurs") or [])
            if communs:
                _lien(f"agent:{a['id']}", f"agent:{b['id']}",
                      "déclencheur commun : " + list(communs)[0][:24])
    # exécutions récentes : deux agents qui ont traité la même demande
    try:
        taches = sorted(store.all("agenttaches"),
                        key=lambda x: x.get("cree_le", ""), reverse=True)[:30]
    except Exception:
        taches = []
    demandes: dict[str, list[str]] = {}
    for t in taches:
        demandes.setdefault(t.get("demande", ""), []).append(t.get("agent", ""))
    for agents_utilises in demandes.values():
        uniques = sorted(set(agents_utilises))
        for i in range(len(uniques)):
            for j in range(i + 1, len(uniques)):
                _lien(f"agent:{uniques[i]}", f"agent:{uniques[j]}",
                      "a traité la même demande")
    return {
        "noeuds": noeuds, "liens": liens,
        "meta": {"titre": "Système agentique",
                 "sous_titre": "22 agents — reliés par déclencheurs, capacités "
                               "et demandes traitées",
                 "systeme": "agentique",
                 "nb_noeuds": len(noeuds), "nb_liens": len(liens),
                 "couleurs": TYPE_COULEURS},
    }


def graphe(systeme: str, store, modules) -> dict:
    if systeme == "planetaire":
        return graphe_planetaire(store, modules)
    if systeme == "agentique":
        return graphe_agentique(store)
    return graphe_constellation(store)


def systemes() -> list[dict]:
    return [{"id": s, **SYSTEMES_INFO[s]} for s in SYSTEMES]


def noeud_detail(g, nid: str) -> dict | None:
    for n in g["noeuds"]:
        if n["id"] == nid:
            voisins = [l for l in g["liens"]
                       if l["source"] == nid or l["target"] == nid]
            return {"noeud": n, "nb_liens": len(voisins), "liens": voisins}
    return None
