"""Routes du module Prévision.

Règle de fond : **on ne fabrique pas de chiffres**. Un indicateur dont la valeur
n'a pas été collectée reste à `null` avec l'état « à collecter » — c'est plus
utile et plus honnête qu'une estimation inventée, surtout face à une
collectivité. La note de prévision est donc construite à partir de ce qui est
réellement renseigné, et marque explicitement les trous.
"""

from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path

from ... import docsgen
from ...httpsrv import Response
from ...store import new_id

PREFIX = "/api/prevision"
ICI = Path(__file__).parent

FAMILLES = [
    {"id": "meteo", "nom": "Météo & climat", "icone": "◐",
     "question": "Que va-t-il se passer sur le terrain dans les jours qui viennent ?"},
    {"id": "social", "nom": "Social & territoire", "icone": "◉",
     "question": "Comment évoluent la population, l'emploi, la cohésion ?"},
    {"id": "geopolitique", "nom": "Géopolitique", "icone": "◭",
     "question": "Quelles tensions externes peuvent rejaillir ici ?"},
    {"id": "economie", "nom": "Économie & finances", "icone": "◈",
     "question": "Quel est l'espace budgétaire et le risque financier ?"},
    {"id": "psychologie", "nom": "Psychologie & société", "icone": "◍",
     "question": "Quel est l'état de l'opinion, du moral, de l'acceptabilité ?"},
]


def _lire(nom, defaut=None):
    p = ICI / "data" / nom
    if not p.exists():
        return defaut if defaut is not None else []
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return defaut if defaut is not None else []


def _tendance(valeurs: list) -> dict:
    if len(valeurs) < 2:
        return {"sens": "inconnue", "variation": None}
    try:
        v = [float(x) for x in valeurs if x is not None]
    except Exception:
        return {"sens": "inconnue", "variation": None}
    if len(v) < 2:
        return {"sens": "inconnue", "variation": None}
    n = max(len(v) // 3, 2)
    a = sum(v[:n]) / n
    b = sum(v[-n:]) / n
    if a == 0:
        return {"sens": "inconnue", "variation": None}
    var = round((b - a) / abs(a) * 100, 1)
    sens = "hausse" if var > 3 else ("baisse" if var < -3 else "stable")
    return {"sens": sens, "variation": var, "moyenne_recente": round(b, 2)}


def register(router, ctx):
    store = ctx["store"]
    catalogue = _lire("indicateurs.json", {"indicateurs": []})
    broadcast = ctx.get("broadcast") or (lambda *a, **k: None)

    def _indicateurs():
        """Catalogue + valeurs saisies (les saisies écrasent le catalogue)."""
        saisies = {r["id"]: r for r in store.all("prevvaleurs")}
        out = []
        for ind in catalogue.get("indicateurs", []):
            d = dict(ind)
            s = saisies.get(ind["id"])
            if s:
                d["valeur"] = s.get("valeur")
                d["serie"] = s.get("serie") or []
                d["maj_le"] = s.get("maj_le") or ""
                d["note"] = s.get("note") or d.get("note", "")
            d.setdefault("valeur", None)
            d["etat"] = "renseigné" if d.get("valeur") is not None else "à collecter"
            d["tendance"] = _tendance(d.get("serie") or [])
            out.append(d)
        return out

    @router.get(PREFIX + "/familles")
    def familles(req):
        return {"familles": FAMILLES}

    @router.get(PREFIX + "/indicateurs")
    def indicateurs(req):
        fam = req.q("famille") or ""
        out = [i for i in _indicateurs() if not fam or i.get("famille") == fam]
        return {"indicateurs": out, "total": len(out),
                "renseignes": len([i for i in out if i.get("etat") == "renseigné"])}

    @router.post(PREFIX + "/indicateurs")
    def saisir(req):
        """Enregistre une valeur (et optionnellement une série) pour un indicateur."""
        p = req.json()
        iid = p.get("id") or ""
        connu = any(i["id"] == iid for i in catalogue.get("indicateurs", []))
        if not connu:
            # indicateur ad hoc créé par l'utilisateur
            (catalogue.setdefault("indicateurs", []).append({
                "id": iid, "famille": p.get("famille") or "social",
                "nom": p.get("nom") or iid, "unite": p.get("unite") or "",
                "source": p.get("source") or "saisie manuelle",
                "url": p.get("url") or "", "licence": p.get("licence") or "interne",
                "frequence": p.get("frequence") or "ponctuelle",
                "horizon": p.get("horizon") or "", "mode": "manuel",
                "interpretation": p.get("interpretation") or "", "confiance": p.get("confiance") or "moyenne",
            }))
        rec = {"id": iid, "valeur": p.get("valeur"), "serie": p.get("serie") or [],
               "note": p.get("note") or "",
               "maj_le": _dt.datetime.now().strftime("%Y-%m-%d %H:%M")}
        store.put("prevvaleurs", iid, rec)
        broadcast("prevision", {"kind": "valeur", "id": iid, "valeur": rec["valeur"]})
        return {"valeur": rec}

    @router.delete(PREFIX + "/indicateurs/:iid")
    def effacer(req, iid):
        return {"ok": store.delete("prevvaleurs", iid)}

    # ---------------------------------------------------------------- scénarios
    @router.get(PREFIX + "/scenarios")
    def scenarios(req):
        return {"scenarios": store.all("prevscen")}

    @router.post(PREFIX + "/scenario")
    def scenario(req):
        p = req.json()
        sid = p.get("id") or new_id("scn")
        rec = {
            "id": sid, "nom": p.get("nom") or "Scénario",
            "horizon": p.get("horizon") or "12 mois",
            "hypotheses": [str(x) for x in (p.get("hypotheses") or []) if str(x).strip()],
            "probabilite": p.get("probabilite"),
            "impacts": [str(x) for x in (p.get("impacts") or []) if str(x).strip()],
            "signaux": [str(x) for x in (p.get("signaux") or []) if str(x).strip()],
            "reponse": p.get("reponse") or "",
            "cree_le": _dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        store.put("prevscen", sid, rec)
        return {"scenario": rec}

    @router.delete(PREFIX + "/scenario/:sid")
    def supprimer_scenario(req, sid):
        return {"ok": store.delete("prevscen", sid)}

    # -------------------------------------------------------- note de prévision
    @router.post(PREFIX + "/generer")
    def generer(req):
        p = req.json() or {}
        fmt = (p.get("format") or "html").lower()
        horizon = p.get("horizon") or "12 mois"
        fams = p.get("familles") or [f["id"] for f in FAMILLES]
        inds = [i for i in _indicateurs() if i.get("famille") in fams]
        scen = store.all("prevscen")

        blocs = []
        for f in FAMILLES:
            if f["id"] not in fams:
                continue
            sel = [i for i in inds if i.get("famille") == f["id"]]
            if not sel:
                continue
            blocs.append({"type": "h2", "texte": f["nom"]})
            blocs.append({"type": "p", "texte": f["question"]})
            blocs.append({"type": "table",
                          "entetes": ["Indicateur", "Valeur", "Tendance", "Source", "Confiance"],
                          "lignes": [[i.get("nom", ""),
                                      (f"{i['valeur']} {i.get('unite','')}".strip()
                                       if i.get("valeur") is not None else "à collecter"),
                                      (f"{i['tendance']['sens']}"
                                       + (f" {i['tendance']['variation']:+} %"
                                          if i["tendance"].get("variation") is not None else "")),
                                      i.get("source", ""), i.get("confiance", "")]
                                     for i in sel]})
            notes = [f"{i.get('nom')} — {i.get('note')}" for i in sel if i.get("note")]
            if notes:
                blocs.append({"type": "ul", "items": notes})

        manquants = [i for i in inds if i.get("etat") != "renseigné"]
        if manquants:
            blocs.append({"type": "h2", "texte": "Lacunes à combler"})
            blocs.append({"type": "ul", "items": [
                f"{i.get('nom')} — {i.get('source')}"
                + (f" ({i.get('url')})" if i.get("url") else "")
                for i in manquants]})

        if scen:
            blocs.append({"type": "h2", "texte": "Scénarios"})
            blocs.append({"type": "table",
                          "entetes": ["Scénario", "Horizon", "Probabilité", "Impacts", "Réponse"],
                          "lignes": [[s.get("nom", ""), s.get("horizon", ""),
                                      (f"{s['probabilite']} %" if s.get("probabilite") is not None else "—"),
                                      " ; ".join(s.get("impacts") or []) or "—",
                                      s.get("reponse") or "—"] for s in scen]})
            for s in scen:
                if s.get("signaux"):
                    blocs.append({"type": "h3", "texte": f"Signaux à surveiller — {s['nom']}"})
                    blocs.append({"type": "ul", "items": s["signaux"]})

        blocs.append({"type": "hr"})
        blocs.append({"type": "note",
                      "texte": "Document de cadrage, pas une prédiction. Les valeurs non "
                               "renseignées sont signalées comme telles : toute décision "
                               "doit s'appuyer sur des données vérifiées auprès du producteur."})

        doc = {
            "titre": f"Note de prévision — {p.get('titre') or 'Bassin de Thau'}",
            "sous_titre": f"Horizon {horizon} · lecture du {_dt.date.today():%d/%m/%Y}",
            "meta": {"Territoire": (ctx.get("config") or {}).get("territoire", {}).get("nom", ""),
                     "Indicateurs suivis": str(len(inds)),
                     "Renseignés": str(len([i for i in inds if i.get("etat") == "renseigné"])),
                     "Scénarios": str(len(scen))},
            "blocs": blocs,
        }

        # Le modèle, s'il est là, ajoute une lecture transversale — jamais des chiffres.
        if ctx.get("llm") and ctx["llm"].resolve() != "none" and p.get("narratif", True):
            texte = docsgen.to_text(doc)[:4000]
            synt = ctx["llm"].complete(
                "À partir de ces éléments, rédige 4 à 6 phrases de lecture transversale : "
                "ce qui se dessine, ce qui est incertain, ce qu'il convient de surveiller. "
                "N'invente aucun chiffre. Français administratif, sobre, sans emphase.\n\n"
                + texte,
                system="Tu écris une note de cadrage pour une collectivité française.")
            if synt:
                doc["blocs"].insert(0, {"type": "h2", "texte": "Lecture transversale"})
                doc["blocs"].insert(1, {"type": "quote", "texte": synt.strip()})

        data, mime = docsgen.render(fmt, doc)
        nom = (f"{_dt.datetime.now():%Y%m%d-%H%M%S}-prevision.{fmt}")
        chemin = store.write_blob(nom, data, "documents")
        return {"document": {"nom": nom, "fichier": str(chemin), "format": fmt,
                             "mime": mime, "taille": len(data),
                             "titre": doc["titre"]},
                "telechargement": f"/api/fichiers/{nom}"}

    # --------------------------------------------------------------- synthèse
    @router.get(PREFIX + "/tableau")
    def tableau(req):
        """Vue d'ensemble compacte pour le tableau de bord."""
        inds = _indicateurs()
        out = []
        for f in FAMILLES:
            sel = [i for i in inds if i.get("famille") == f["id"]]
            out.append({
                "famille": f["id"], "nom": f["nom"],
                "total": len(sel),
                "renseignes": len([i for i in sel if i.get("etat") == "renseigné"]),
                "alertes": len([i for i in sel
                                if i.get("tendance", {}).get("sens") == "hausse"
                                and (i.get("seuil_alerte") is not None
                                     and isinstance(i.get("valeur"), (int, float))
                                     and i["valeur"] > i["seuil_alerte"])]),
            })
        return {"tableau": out,
                "scenarios": len(store.all("prevscen")),
                "couverture": round(100 * len([i for i in inds if i.get("etat") == "renseigné"])
                                    / max(len(inds), 1))}
