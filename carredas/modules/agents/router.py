"""Routes du module Agents.

Le système agentique n'est pas un chatbot : c'est une chaîne de production.
On lui confie une demande, elle passe par six phases traçables, et elle rend
un document. Quand elle ne sait pas, elle le dit — c'est la consigne la plus
difficile à tenir et la plus utile.
"""

from __future__ import annotations

import datetime as _dt

from ... import docsgen, log
from ...httpsrv import Response
from ...store import slug
from . import engine as E

PREFIX = "/api/agents"


def register(router, ctx):
    store = ctx["store"]
    config = ctx.get("config") or {}
    broadcast = ctx.get("broadcast") or (lambda *a, **k: None)

    def _contexte(p: dict) -> dict:
        """Le contexte réel : une session de réunion si elle est désignée."""
        out: dict = {}
        rid = (p or {}).get("reunion_id") or (p or {}).get("session")
        if rid:
            # la collection du module Réunion s'appelle « reunions »
            s = store.get("reunions", rid)
            if s:
                out["session"] = s
                out["session_id"] = rid
        return out

    @router.get(PREFIX)
    def liste(req):
        return {"agents": E.charger_agents(), "total": len(E.charger_agents()),
                "cycle": [{"id": c, "intitule": E.PHASES[c]} for c in E.CYCLE]}

    @router.get(PREFIX + "/cycle")
    def cycle(req):
        return {"cycle": [{"id": c, "intitule": E.PHASES[c]} for c in E.CYCLE]}

    @router.post(PREFIX + "/router")
    def router_agents(req):
        """Qui doit traiter cette demande ? Routage déterministe."""
        p = req.json() or {}
        texte = (p.get("texte") or p.get("demande") or "").strip()
        if not texte:
            return Response.error("il manque le texte à router", 400)
        r = E.router(texte, int(p.get("limite") or 5))
        return {
            "texte": texte,
            "resultats": [{"id": x["agent"]["id"], "nom": x["agent"]["nom"],
                           "emoji": x["agent"]["emoji"], "role": x["agent"]["role"],
                           "score": x["score"], "declencheurs": x["declencheurs"],
                           "sorties": x["agent"].get("sorties") or []} for x in r],
            "choisi": E.choisir(texte, p.get("agent"))["id"] if r else "orchestrator",
            "total": len(r),
        }

    @router.post(PREFIX + "/executer")
    def executer(req):
        """Une demande traverse les six phases et rend un document."""
        p = req.json() or {}
        demande = (p.get("demande") or p.get("texte") or "").strip()
        if not demande:
            return Response.error("il manque la demande", 400)
        contexte = _contexte(p)
        try:
            res = E.executer(demande, p.get("agent"), contexte, store)
        except Exception as exc:
            log.error("agents", f"exécution impossible : {exc}")
            return Response.error(f"exécution impossible : {exc}", 500)

        fmt = (p.get("format") or "md").lower()
        doc = res["document"]
        try:
            data, mime = docsgen.render(
                fmt, doc, taches=res.get("taches_gantt"),
                titre_gantt=doc.get("titre", "Planning"))
        except Exception as exc:
            log.error("agents", f"rendu {fmt} : {exc}")
            return Response.error(f"rendu impossible : {exc}", 500)

        horodatage = _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        nom = (f"{horodatage}-{slug(res['agent']['id'], 'agent')}-"
               f"{slug(demande[:40], 'demande')}.{fmt}")
        chemin = store.write_blob(nom, data, "documents")
        rec = {"id": nom, "nom": nom, "fichier": str(chemin), "format": fmt,
               "mime": mime, "titre": doc.get("titre", ""),
               "agent": res["agent"]["id"],
               "cree_le": _dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
               "taille": len(data)}
        log.info("agents", f"{res['agent']['id']} → {fmt} ({len(data)} o)")
        broadcast("agents", {"kind": "document", "agent": res["agent"]["id"],
                             "titre": rec["titre"], "format": fmt})
        return {"document": rec, "tache": res["tache"],
                "agent": res["agent"], "recherche": res["recherche"],
                "problemes": res["problemes"],
                "signalements": res.get("signalements", []),
                "duree_s": res["duree_s"]}

    @router.get(PREFIX + "/historique")
    def historique(req):
        return {"taches": E.historique(store), "total": len(store.all("agenttaches"))}

    # ------------------------------------------------- ☉ le patron (SOL)
    @router.get(PREFIX + "/systeme")
    def systeme(req):
        """L'état live du système solaire : qui travaille, quoi, quels sous-agents."""
        from . import orchestrateur as O
        fenetre = float(((config.get("patron") or {}).get("fenetre_visibilite_s")
                         or 20))
        return O.etat_systeme(store, fenetre_s=fenetre, config=config)

    @router.get(PREFIX + "/sousagents")
    def sousagents(req):
        from . import orchestrateur as O
        return {"sous_agents": O.lister_sous_agents(store),
                "total": len(store.all("sousagents"))}

    @router.post(PREFIX + "/parler")
    def parler(req):
        """Parler au patron. Lui seul répond — il délègue en interne."""
        from . import orchestrateur as O
        p = req.json() or {}
        texte = (p.get("texte") or p.get("demande") or "").strip()
        if not texte:
            return Response.error("il manque le texte", 400)
        contexte = _contexte(p)
        r = O.parler(texte, contexte, store, broadcast, config=config)
        return r

    @router.get(PREFIX + "/:aid")
    def detail(req, aid):
        a = E.agent(aid)
        if not a:
            return Response.not_found("agent inconnu")
        return {"agent": a}
