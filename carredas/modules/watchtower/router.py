"""Routes du module Cartographie (Watchtower).

Le moteur 3D complet vit déjà dans `projects/watchtower` (999 fichiers, Cesium).
Ce module est sa **tête de pont dans Carré d'As** : il tient le catalogue des
couches, les points d'observation et les annotations, et sert de contrat pour y
rebrancher la vue 3D quand elle sera prête. Les données sont dans
`data/couches.json` — modifiables sans toucher au code.
"""

from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path

from ...httpsrv import Response
from ...store import new_id

PREFIX = "/api/carto"
ICI = Path(__file__).parent


def _lire(nom: str, defaut=None):
    p = ICI / "data" / nom
    if not p.exists():
        return defaut if defaut is not None else []
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return defaut if defaut is not None else []


def register(router, ctx):
    store = ctx["store"]
    couches = _lire("couches.json", {"groupes": [], "couches": []})
    broadcast = ctx.get("broadcast") or (lambda *a, **k: None)

    @router.get(PREFIX + "/couches")
    def lister_couches(req):
        actives = set()
        etat = store.get("cartovues", "_defaut") or {}
        actives = set(etat.get("actives") or [])
        q = (req.q("q") or "").strip().lower()
        out = []
        for c in couches.get("couches", []):
            if q and q not in (c.get("nom", "") + c.get("groupe", "") +
                               c.get("source", "")).lower():
                continue
            d = dict(c)
            d["active"] = c.get("id") in actives
            out.append(d)
        return {"couches": out, "total": len(out)}

    @router.get(PREFIX + "/groupes")
    def groupes(req):
        return {"groupes": couches.get("groupes", [])}

    @router.get(PREFIX + "/couches/:cid")
    def couche(req, cid):
        for c in couches.get("couches", []):
            if c.get("id") == cid:
                return {"couche": c}
        return Response.not_found("couche inconnue")

    # ------------------------------------------------------------ vues mémorisées
    @router.get(PREFIX + "/vues")
    def vues(req):
        return {"vues": store.all("cartovues")}

    @router.post(PREFIX + "/vue")
    def sauver_vue(req):
        p = req.json()
        vid = p.get("id") or new_id("vue")
        rec = {
            "id": vid,
            "nom": p.get("nom") or "Vue sans nom",
            "centre": p.get("centre") or {"lon": 3.69, "lat": 43.40, "zoom": 11},
            "actives": p.get("actives") or [],
            "notes": p.get("notes") or "",
            "projet": p.get("projet") or "",
            "cree_le": _dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        }
        store.put("cartovues", vid, rec)
        if vid == "_defaut" or p.get("par_defaut"):
            store.put("cartovues", "_defaut", rec)
        return {"vue": rec}

    @router.delete(PREFIX + "/vue/:vid")
    def supprimer_vue(req, vid):
        return {"ok": store.delete("cartovues", vid)}

    # ------------------------------------------------------------ points / POI
    @router.get(PREFIX + "/points")
    def points(req):
        return {"points": store.all("cartopoints")}

    @router.post(PREFIX + "/points")
    def ajouter_point(req):
        p = req.json()
        if p.get("lat") is None or p.get("lon") is None:
            return Response.error("latitude et longitude obligatoires", 400)
        pid = p.get("id") or new_id("pt")
        rec = {
            "id": pid,
            "nom": p.get("nom") or "Point",
            "lon": float(p["lon"]), "lat": float(p["lat"]),
            "categorie": p.get("categorie") or "observation",
            "projet": p.get("projet") or "",
            "commune": p.get("commune") or "",
            "description": p.get("description") or "",
            "etat": p.get("etat") or "à vérifier",
            "source": p.get("source") or "saisie",
            "cree_le": _dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        }
        store.put("cartopoints", pid, rec)
        broadcast("carto", {"kind": "point", "nom": rec["nom"]})
        return {"point": rec}

    @router.delete(PREFIX + "/points/:pid")
    def supprimer_point(req, pid):
        return {"ok": store.delete("cartopoints", pid)}

    # ------------------------------------------------------------- annotations
    @router.get(PREFIX + "/annotations")
    def annotations(req):
        return {"annotations": store.all("cartoannot")}

    @router.post(PREFIX + "/annotations")
    def ajouter_annotation(req):
        p = req.json()
        aid = p.get("id") or new_id("ann")
        rec = {"id": aid, "titre": p.get("titre") or "", "texte": p.get("texte") or "",
               "point": p.get("point") or "", "auteur": p.get("auteur") or "",
               "tags": p.get("tags") or [],
               "cree_le": _dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}
        store.put("cartoannot", aid, rec)
        return {"annotation": rec}

    @router.delete(PREFIX + "/annotations/:aid")
    def supprimer_annotation(req, aid):
        return {"ok": store.delete("cartoannot", aid)}

    # --------------------------------------------------------------- diagnostic
    @router.get(PREFIX + "/territoire")
    def territoire(req):
        """Le territoire de référence + un résumé par commune."""
        cfg = ctx.get("config") or {}
        terr = cfg.get("territoire") or {}
        pts = store.all("cartopoints")
        par_commune = {}
        for p in pts:
            c = p.get("commune") or "non renseignée"
            par_commune[c] = par_commune.get(c, 0) + 1
        return {
            "territoire": terr,
            "communes_suivies": len(par_commune),
            "points_par_commune": par_commune,
            "couches_disponibles": len(couches.get("couches", [])),
            "couches_actives": len((store.get("cartovues", "_defaut") or {}).get("actives") or []),
            "moteur_3d": str((ctx.get("config") or {}).get("_moteur_3d") or
                             "projects/watchtower — Cesium"),
        }
