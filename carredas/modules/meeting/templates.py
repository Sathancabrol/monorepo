# -*- coding: utf-8 -*-
"""Gabarits de documents produits à partir d'une session de réunion.

Chaque gabarit rend un `doc` (voir `carredas/docsgen`) ou une liste de
diapositives. Aucun appel réseau : tout est assemblé depuis ce qui a été
capturé. C'est ce qui garantit qu'un document sort toujours, même à 23 h la
veille, sans modèle et sans connexion.
"""

from __future__ import annotations

import datetime as _dt

from . import extract

# ------------------------------------------------------------------ outils


def _joli(d: str) -> str:
    """ISO → jj/mm/aaaa ; rend la chaîne telle quelle si ce n'est pas du ISO."""
    if not d:
        return ""
    for f in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"):
        try:
            return _dt.datetime.strptime(str(d)[:19], f).strftime("%d/%m/%Y")
        except Exception:
            continue
    return str(d)


def _euro(n) -> str:
    try:
        n = float(n or 0)
    except Exception:
        return "—"
    return f"{n:,.2f} €".replace(",", " ").replace(".", ",").replace(" ", " ")


def _duree(s: dict) -> str:
    hs = [x.get("horodatage") for x in (s.get("transcript") or []) if x.get("horodatage")]
    if len(hs) < 2:
        return ""
    secs = int(max(hs) - min(hs))
    h, m = secs // 3600, (secs % 3600) // 60
    return (f"{h} h {m:02d}" if h else f"{m} min") + f" ({secs // 60} min)"


def _points_abordes(s: dict) -> list[str]:
    if s.get("sujets"):
        return [str(x) for x in s["sujets"]][:12]
    out = []
    for p in (s.get("ordre_du_jour") or []):
        out.append(str(p))
    if out:
        return out[:12]
    # repli : les phrases les plus « porteuses » du verbatim
    scored = []
    for seg in (s.get("transcript") or []):
        for ph in extract.segmenter(seg.get("texte", "")):
            kind, conf = extract._kind_of(ph)
            if conf > 0:
                scored.append((conf + (0.2 if kind == "decision" else 0), ph))
    scored.sort(reverse=True, key=lambda x: x[0])
    vus, res = set(), []
    for _, ph in scored:
        k = ph.lower()[:60]
        if k in vus:
            continue
        vus.add(k)
        res.append(extract.memo(ph))
        if len(res) >= 8:
            break
    return res


# ----------------------------------------------------------- compte rendu


def compte_rendu(s: dict) -> dict:
    meta = {
        "Date": _joli(s.get("date")),
        "Heure": s.get("heure") or "",
        "Lieu": s.get("lieu") or "—",
        "Type": s.get("type") or "réunion de travail",
    }
    if s.get("organisme"):
        meta["Organisme"] = s["organisme"]
    if s.get("participants"):
        meta["Participants"] = ", ".join(s["participants"])
    d = _duree(s)
    if d:
        meta["Durée"] = d

    blocs = []
    if s.get("contexte"):
        blocs.append({"type": "p", "texte": s["contexte"]})

    if s.get("ordre_du_jour"):
        blocs.append({"type": "h2", "texte": "Ordre du jour"})
        blocs.append({"type": "ol", "items": [str(x) for x in s["ordre_du_jour"]]})

    pts = _points_abordes(s)
    if pts:
        blocs.append({"type": "h2", "texte": "Points abordés"})
        blocs.append({"type": "ul", "items": pts})

    if s.get("decisions"):
        blocs.append({"type": "h2", "texte": "Décisions"})
        blocs.append({"type": "ol", "items": [
            f"{d.get('texte','')}"
            + (f" — {d['responsable']}" if d.get("responsable") else "")
            + (f" — échéance {_joli(d['echeance'])}" if d.get("echeance") else "")
            for d in s["decisions"]]})

    if s.get("actions"):
        blocs.append({"type": "h2", "texte": "Actions à mener"})
        blocs.append({"type": "table",
                      "entetes": ["#", "Action", "Responsable", "Échéance", "Montant", "Statut"],
                      "lignes": [[i, a.get("texte", ""), a.get("responsable") or "—",
                                  _joli(a.get("echeance")) or "—",
                                  _euro(a.get("montant")) if a.get("montant") else "—",
                                  a.get("statut") or "à faire"]
                                 for i, a in enumerate(s["actions"], 1)]})

    if s.get("risques"):
        blocs.append({"type": "h2", "texte": "Points de vigilance"})
        blocs.append({"type": "ul", "items": [r.get("texte", "") for r in s["risques"]]})

    if s.get("questions"):
        blocs.append({"type": "h2", "texte": "Questions ouvertes"})
        blocs.append({"type": "ul", "items": [q.get("texte", "") for q in s["questions"]]})

    if s.get("budget"):
        blocs.append({"type": "h2", "texte": "Enveloppe évoquée"})
        blocs.append({"type": "table",
                      "entetes": ["Poste", "Catégorie", "Qté", "Coût unitaire", "Total"],
                      "lignes": [[b.get("libelle", ""), b.get("categorie", ""),
                                  f"{b.get('quantite', 1)} {b.get('unite','')}".strip(),
                                  _euro(b.get("cout_unitaire")), _euro(b.get("total"))]
                                 for b in s["budget"]]})
        blocs.append({"type": "p", "texte": "**Total : "
                     f"{_euro(sum(float(b.get('total') or 0) for b in s['budget']))}**"})

    if s.get("planning"):
        blocs.append({"type": "h2", "texte": "Calendrier"})
        blocs.append({"type": "table",
                      "entetes": ["Tâche", "Début", "Fin", "Responsable", "Avancement"],
                      "lignes": [[t.get("label", ""), _joli(t.get("debut")), _joli(t.get("fin")),
                                  t.get("responsable") or "—",
                                  f"{int(float(t.get('avancement') or 0))} %"]
                                 for t in s["planning"]]})

    return {"titre": s.get("titre") or "Compte rendu",
            "sous_titre": "Compte rendu de réunion", "meta": meta, "blocs": blocs}


# --------------------------------------------------------- note de synthèse


def note_synthese(s: dict, objet: str = "") -> dict:
    meta = {"Date": _joli(s.get("date")), "Rédacteur": "Carré d'As",
            "Source": s.get("titre") or ""}
    if s.get("organisme"):
        meta["Structure"] = s["organisme"]
    blocs = [
        {"type": "h2", "texte": "Objet"},
        {"type": "p", "texte": objet or (s.get("contexte") or s.get("titre") or "—")},
        {"type": "h2", "texte": "Contexte"},
        {"type": "p", "texte": s.get("contexte") or
            "Réunion « " + (s.get("titre") or "") + " »" +
            (f", tenue le {_joli(s.get('date'))}" if s.get("date") else "") +
            (f" à {s['lieu']}" if s.get("lieu") else "") + "."},
        {"type": "ul", "items": _points_abordes(s) or ["—"]},
        {"type": "h2", "texte": "Analyse"},
    ]
    if s.get("decisions"):
        blocs.append({"type": "h3", "texte": "Ce qui est acté"})
        blocs.append({"type": "ul", "items": [d.get("texte", "") for d in s["decisions"]]})
    if s.get("risques"):
        blocs.append({"type": "h3", "texte": "Ce qui fait risque"})
        blocs.append({"type": "ul", "items": [r.get("texte", "") for r in s["risques"]]})
    if s.get("questions"):
        blocs.append({"type": "h3", "texte": "Ce qui reste ouvert"})
        blocs.append({"type": "ul", "items": [q.get("texte", "") for q in s["questions"]]})
    blocs.append({"type": "h2", "texte": "Propositions"})
    blocs.append({"type": "ol", "items": [a.get("texte", "") + (
        f" ({a['responsable']})" if a.get("responsable") else "")
        for a in s["actions"]] or ["Aucune action formalisée à ce stade."]})
    if s.get("budget"):
        blocs.append({"type": "h2", "texte": "Incidence financière"})
        blocs.append({"type": "p", "texte": "Montant total estimé : **" +
                     _euro(sum(float(b.get("total") or 0) for b in s["budget"])) + "**."})
    blocs.append({"type": "h2", "texte": "Suite à donner"})
    blocs.append({"type": "p", "texte": "Transmission du présent document aux participants ; "
                  "point d'étape lors de la prochaine réunion."})
    return {"titre": f"Note de synthèse — {s.get('titre') or ''}".strip(" — "),
            "sous_titre": objet or "", "meta": meta, "blocs": blocs}


# -------------------------------------------------------------- délibération

_DELIB_VUS = [
    "Vu le Code général des collectivités territoriales, notamment ses articles L. 5211-1 et suivants ;",
    "Vu les statuts de la communauté d'agglomération ;",
    "Vu le règlement intérieur du conseil communautaire ;",
    "Vu le projet de territoire et ses orientations ;",
]


def deliberation(s: dict, objet: str = "") -> dict:
    articles = []
    for i, d in enumerate(s.get("decisions") or [], 1):
        articles.append(f"Article {i} — {d.get('texte','')}"
                        + (f" Cette action est confiée à {d['responsable']}."
                           if d.get("responsable") else ""))
    for i, a in enumerate(s.get("actions") or [], len(articles) + 1):
        articles.append(f"Article {i} — {a.get('texte','')}"
                        + (f" Responsable : {a['responsable']}." if a.get("responsable") else "")
                        + (f" Échéance : {_joli(a['echeance'])}." if a.get("echeance") else ""))
    if not articles:
        articles = ["Article 1 — [à compléter : objet précis de la délibération]"]

    total = sum(float(b.get("total") or 0) for b in (s.get("budget") or []))
    blocs = [
        {"type": "p", "texte": f"**Objet :** {objet or s.get('titre') or '—'}"},
        {"type": "h2", "texte": "Exposé des motifs"},
        {"type": "p", "texte": s.get("contexte") or "[à compléter : contexte et motifs]"},
        {"type": "ul", "items": _points_abordes(s) or ["—"]},
        {"type": "h2", "texte": "Vu"},
        {"type": "ul", "items": _DELIB_VUS},
        {"type": "h2", "texte": "Considérant"},
        {"type": "ul", "items": [f"Considérant {d.get('texte','')}"
                                 for d in (s.get("decisions") or [])]
            or ["Considérant l'intérêt de l'opération pour le territoire ;"]},
        {"type": "h2", "texte": "Délibération"},
        {"type": "p", "texte": "Le conseil communautaire, après en avoir délibéré, décide :"},
        {"type": "ol", "items": articles},
    ]
    if total:
        blocs.append({"type": "p", "texte": f"La dépense correspondante est évaluée à "
                                            f"**{_euro(total)}**, imputée sur les crédits ouverts "
                                            f"au budget de l'exercice en cours."})
    if s.get("risques"):
        blocs.append({"type": "h2", "texte": "Réserves"})
        blocs.append({"type": "ul", "items": [r.get("texte", "") for r in s["risques"]]})
    blocs.append({"type": "p", "texte": f"Fait à {s.get('lieu') or 'Sète'}, le {_joli(s.get('date'))}."})
    blocs.append({"type": "note", "texte": "Projet de délibération généré automatiquement : "
                                           "à relecture et validation par le service concerné."})
    return {"titre": f"Projet de délibération — {objet or s.get('titre') or ''}",
            "sous_titre": (s.get("organisme") or "Communauté d'agglomération"),
            "meta": {"Séance du": _joli(s.get("date")), "Statut": "projet"},
            "blocs": blocs}


# ------------------------------------------------------------------- courrier


def courrier(s: dict, destinataire: str = "", objet: str = "") -> dict:
    blocs = [
        {"type": "p", "texte": f"À l'attention de {destinataire or '[destinataire]'}"},
        {"type": "p", "texte": f"**Objet :** {objet or s.get('titre') or '—'}"},
        {"type": "p", "texte": "Madame, Monsieur,"},
        {"type": "p", "texte": "À la suite de notre réunion du "
                               f"{_joli(s.get('date'))}"
                               + (f" à {s['lieu']}" if s.get("lieu") else "")
                               + ", je vous adresse les éléments arrêtés ensemble."},
    ]
    if s.get("decisions"):
        blocs.append({"type": "h2", "texte": "Décisions retenues"})
        blocs.append({"type": "ul", "items": [d.get("texte", "") for d in s["decisions"]]})
    if s.get("actions"):
        blocs.append({"type": "h2", "texte": "Prochaines étapes"})
        blocs.append({"type": "table",
                      "entetes": ["Action", "Responsable", "Échéance"],
                      "lignes": [[a.get("texte", ""), a.get("responsable") or "—",
                                  _joli(a.get("echeance")) or "—"] for a in s["actions"]]})
    blocs.append({"type": "p", "texte": "Je me tiens à votre disposition pour tout complément."})
    blocs.append({"type": "p", "texte": "Veuillez agréer, Madame, Monsieur, l'expression de mes "
                                        "salutations distinguées."})
    return {"titre": f"Courrier — {objet or s.get('titre') or ''}",
            "sous_titre": "", "meta": {"Date": _joli(s.get("date"))}, "blocs": blocs}


# ------------------------------------------------------------- diapositives


def diapositives(s: dict) -> list[dict]:
    out = [{"titre": s.get("titre") or "Réunion",
            "sous_titre": " ".join(x for x in [
                s.get("organisme") or "", _joli(s.get("date")), s.get("lieu") or ""] if x),
            "lignes": [f"{len(s.get('decisions') or [])} décision(s)",
                       f"{len(s.get('actions') or [])} action(s)",
                       f"{len(s.get('risques') or [])} point(s) de vigilance"]}]
    if s.get("contexte"):
        out.append({"titre": "Contexte", "lignes": [(s["contexte"], 1)]})
    if s.get("ordre_du_jour"):
        out.append({"titre": "Ordre du jour",
                    "lignes": [(str(x), 1) for x in s["ordre_du_jour"]]})
    pts = _points_abordes(s)
    if pts:
        out.append({"titre": "Ce qui a été abordé", "lignes": [(p, 1) for p in pts]})
    if s.get("decisions"):
        out.append({"titre": "Décisions",
                    "lignes": [(d.get("texte", "")
                                + (f" — {d['responsable']}" if d.get("responsable") else "")
                                + (f" — {_joli(d['echeance'])}" if d.get("echeance") else ""), 1)
                               for d in s["decisions"]]})
    if s.get("actions"):
        out.append({"titre": "Actions",
                    "lignes": [(a.get("texte", "")
                                + (f" → {a['responsable']}" if a.get("responsable") else "")
                                + (f" · {_joli(a['echeance'])}" if a.get("echeance") else ""), 1)
                               for a in s["actions"][:10]]})
    if s.get("risques"):
        out.append({"titre": "Points de vigilance",
                    "lignes": [(r.get("texte", ""), 1) for r in s["risques"]]})
    if s.get("budget"):
        total = sum(float(b.get("total") or 0) for b in s["budget"])
        out.append({"titre": "Enveloppe",
                    "lignes": [(f"{b.get('libelle','')} — {_euro(b.get('total'))}", 1)
                               for b in s["budget"][:8]]
                              + [(f"Total : {_euro(total)}", 1)]})
    if s.get("planning"):
        out.append({"titre": "Calendrier",
                    "lignes": [(f"{t.get('label','')} — {_joli(t.get('debut'))} → "
                                f"{_joli(t.get('fin'))}", 1) for t in s["planning"][:10]]})
    if s.get("questions"):
        out.append({"titre": "Questions ouvertes",
                    "lignes": [(q.get("texte", ""), 1) for q in s["questions"]]})
    out.append({"titre": "Prochaines étapes",
                "lignes": [(a.get("texte", ""), 1) for a in
                           (s.get("actions") or [])[:6]] or [("—", 1)]})
    return out


# ------------------------------------------------------------------- tableaux


def planning_lignes(s: dict) -> list[list]:
    rows = [[t.get("label", ""), t.get("debut", ""), t.get("fin", ""),
             t.get("responsable", ""), int(float(t.get("avancement") or 0)),
             t.get("depend", "")] for t in (s.get("planning") or [])]
    for a in (s.get("actions") or []):
        if a.get("echeance") and a.get("texte"):
            rows.append([a["texte"], "", a["echeance"], a.get("responsable", ""), 0, ""])
    return rows


def budget_lignes(s: dict) -> list[list]:
    rows = [[b.get("libelle", ""), b.get("categorie", ""), b.get("quantite", 1),
             b.get("unite", ""), b.get("cout_unitaire", 0), b.get("total", 0),
             b.get("financeur", "")] for b in (s.get("budget") or [])]
    if rows:
        rows.append(["TOTAL", "", "", "", "",
                     round(sum(float(b.get("total") or 0) for b in s["budget"]), 2), ""])
    return rows


# ------------------------------------------------------------- aiguillage

GABARITS = {
    "recap": ("Compte rendu", ["md", "html", "docx", "txt", "json"]),
    "note": ("Note de synthèse", ["md", "html", "docx", "txt", "json"]),
    "deliberation": ("Projet de délibération", ["md", "html", "docx", "txt"]),
    "courrier": ("Courrier", ["md", "html", "docx", "txt"]),
    "presentation": ("Présentation", ["pptx", "html", "json"]),
    "planning": ("Planning", ["svg", "csv", "html", "md"]),
    "budget": ("Budget", ["csv", "html", "md", "docx"]),
}


def construire(kind: str, s: dict, options: dict | None = None) -> dict:
    """Rend {'doc':…, 'diapos':…, 'entetes':…, 'lignes':…, 'taches':…} selon le gabarit."""
    o = options or {}
    if kind == "recap":
        return {"doc": compte_rendu(s)}
    if kind == "note":
        return {"doc": note_synthese(s, o.get("objet", ""))}
    if kind == "deliberation":
        return {"doc": deliberation(s, o.get("objet", ""))}
    if kind == "courrier":
        return {"doc": courrier(s, o.get("destinataire", ""), o.get("objet", ""))}
    if kind == "presentation":
        return {"doc": compte_rendu(s), "diapos": diapositives(s)}
    if kind == "planning":
        return {"taches": (s.get("planning") or []),
                "doc": {"titre": f"Planning — {s.get('titre','')}",
                        "sous_titre": "Échéancier", "meta": {"Réunion": s.get("titre", "")},
                        "blocs": [
                            {"type": "table",
                             "entetes": ["Tâche", "Début", "Fin", "Responsable", "Avancement"],
                             "lignes": planning_lignes(s)}]},
                "entetes": ["Tâche", "Début", "Fin", "Responsable", "Avancement %", "Dépend de"],
                "lignes": planning_lignes(s)}
    if kind == "budget":
        return {"doc": {"titre": f"Budget — {s.get('titre','')}",
                        "sous_titre": "Estimation des postes évoqués",
                        "meta": {"Réunion": s.get("titre", "")},
                        "blocs": [
                            {"type": "table",
                             "entetes": ["Poste", "Catégorie", "Qté", "Unité",
                                         "Coût unitaire", "Total", "Financeur"],
                             "lignes": budget_lignes(s)}]},
                "entetes": ["Poste", "Catégorie", "Quantité", "Unité",
                            "Coût unitaire", "Total", "Financeur"],
                "lignes": budget_lignes(s)}
    raise ValueError(f"gabarit inconnu : {kind}")
