"""Routes de la Constellation — trois lectures d'un même monde."""

from __future__ import annotations

from ...httpsrv import Response
from . import engine as E

PREFIX = "/api/constellation"


def register(router, ctx):
    store = ctx["store"]
    # ATTENTION : ctx["modules"] est REMPLACÉ par le serveur APRÈS
    # l'enregistrement de tous les modules. Il ne faut JAMAIS capturer la
    # liste ici — la lire à chaque requête, sinon on lit une liste morte.
    def modules():
        return ctx.get("modules") or []

    @router.get(PREFIX)
    def liste_systemes(req):
        out = []
        for s in E.systemes():
            g = E.graphe(s["id"], store, modules())
            out.append({**s, "nb_noeuds": g["meta"]["nb_noeuds"],
                        "nb_liens": g["meta"]["nb_liens"]})
        return {"systemes": out, "total": len(out)}

    @router.get(PREFIX + "/systemes")
    def systemes(req):
        return {"systemes": E.systemes()}

    @router.get(PREFIX + "/graphe")
    def graphe(req):
        systeme = (req.q("systeme") or "constellation").lower()
        if systeme not in E.SYSTEMES:
            return Response.error(
                f"système inconnu : {systeme} (attendu : {', '.join(E.SYSTEMES)})", 400)
        type_filtre = req.q("type")
        g = E.graphe(systeme, store, modules())
        if type_filtre:
            g["noeuds"] = [n for n in g["noeuds"] if n.get("type") == type_filtre]
            ids = {n["id"] for n in g["noeuds"]}
            g["liens"] = [l for l in g["liens"]
                          if l["source"] in ids and l["target"] in ids]
            g["meta"]["nb_noeuds"] = len(g["noeuds"])
            g["meta"]["nb_liens"] = len(g["liens"])
        return g

    @router.get(PREFIX + "/noeud/:id")
    def noeud(req, id):
        systeme = (req.q("systeme") or "constellation").lower()
        g = E.graphe(systeme, store, modules())
        d = E.noeud_detail(g, id)
        if not d:
            return Response.not_found("nœud inconnu")
        return d

    @router.get(PREFIX + "/dataset/:key")
    def dataset(req, key):
        """Un jeu de données de l'atlas (chiffré, sourcé)."""
        atlas = E._charger_atlas()
        ds = (atlas.get("datasets") or {}).get(key)
        if not ds:
            return Response.not_found("jeu de données inconnu")
        return {"key": key, **ds}
