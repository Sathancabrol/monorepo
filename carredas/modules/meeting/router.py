"""Routes HTTP du module Réunion."""

from __future__ import annotations

import datetime as _dt
import json
import re

from ... import docsgen, log
from ...httpsrv import Response
from ...store import slug
from . import engine as E
from .templates import GABARITS, construire

PREFIX = "/api/meeting"


def canonique(store, config=None):
    """Décisions et actions de toutes les réunions, en forme canonique."""
    from ...core import canonical
    out = []
    for s in store.all("reunions"):
        for d in (s.get("decisions") or []):
            out.append(canonical.depuis_decision(d, s.get("id", "")))
        for a in (s.get("actions") or []):
            out.append(canonical.depuis_action(a, s.get("id", "")))
    return out


def register(router, ctx):
    store = ctx["store"]
    eng = E.MeetingEngine(store, ctx.get("llm"), ctx.get("config"))
    ctx.setdefault("engines", {})["meeting"] = eng
    broadcast = ctx.get("broadcast") or (lambda *a, **k: None)
    eng.on_event(lambda rec: broadcast("meeting", rec))

    def _s(req, sid):
        s = eng.get(sid)
        if not s:
            return None, Response.not_found("session inconnue")
        return s, None

    # ------------------------------------------------------------- sessions
    @router.post(PREFIX)
    def creer(req):
        p = req.json()
        if not (p.get("titre") or "").strip():
            p["titre"] = "Réunion du " + _dt.date.today().strftime("%d/%m/%Y")
        return {"session": eng.creer(p)}

    @router.get(PREFIX)
    def lister(req):
        return {"sessions": eng.liste()}

    @router.get(PREFIX + "/gabarits")
    def gabarits(req):
        return {"gabarits": [{"id": k, "titre": v[0], "formats": v[1]}
                             for k, v in GABARITS.items()]}

    @router.get(PREFIX + "/:id")
    def lire(req, id):
        s, err = _s(req, id)
        return err or {"session": s}

    @router.put(PREFIX + "/:id")
    def maj(req, id):
        s, err = _s(req, id)
        if err:
            return err
        return {"session": eng.maj(id, req.json())}

    @router.delete(PREFIX + "/:id")
    def supprimer(req, id):
        return {"ok": eng.supprimer(id)}

    @router.post(PREFIX + "/:id/statut")
    def statut(req, id):
        p = req.json()
        s = eng.statut(id, p.get("statut") or "")
        if not s:
            return Response.error("statut invalide", 400)
        return {"session": s}

    # -------------------------------------------------------------- temps réel
    @router.post(PREFIX + "/:id/segment")
    def segment(req, id):
        s, err = _s(req, id)
        if err:
            return err
        p = req.json()
        return eng.pousser(id, p.get("texte", ""), p.get("locuteur", ""),
                           p.get("source") or "voix",
                           enrichir=(p.get("enrichir", True) is not False))

    @router.post(PREFIX + "/:id/note")
    def note(req, id):
        s, err = _s(req, id)
        if err:
            return err
        return eng.noter(id, (req.json() or {}).get("texte", ""))

    @router.get(PREFIX + "/:id/suggestions")
    def suggestions(req, id):
        return {"suggestions": eng.suggestions(id, req.q("statut", "attente"))}

    @router.post(PREFIX + "/:id/suggestion/:sid/accepter")
    def accepter(req, id, sid):
        item = eng.accepter(id, sid, req.json())
        if not item:
            return Response.not_found("suggestion inconnue")
        return {"item": item, "session": eng.get(id)}

    @router.post(PREFIX + "/:id/suggestion/:sid/refuser")
    def refuser(req, id, sid):
        return {"ok": eng.refuser(id, sid)}

    @router.post(PREFIX + "/:id/item")
    def ajouter_item(req, id):
        p = req.json()
        item = eng.ajouter_item(id, p.get("kind") or "action", p)
        if not item:
            return Response.error("type d'élément inconnu", 400)
        return {"item": item, "session": eng.get(id)}

    @router.put(PREFIX + "/:id/item/:kind/:iid")
    def modifier_item(req, id, kind, iid):
        it = eng.modifier_item(id, kind, iid, req.json())
        return {"item": it, "session": eng.get(id)} if it else Response.not_found("élément inconnu")

    @router.delete(PREFIX + "/:id/item/:kind/:iid")
    def supprimer_item(req, id, kind, iid):
        return {"ok": eng.supprimer_item(id, kind, iid)}

    # --------------------------------------------------------- budget/planning
    @router.post(PREFIX + "/:id/budget")
    def ajouter_budget(req, id):
        rec = eng.ajouter_budget(id, req.json())
        return {"ligne": rec, "session": eng.get(id)} if rec else Response.not_found("session inconnue")

    @router.delete(PREFIX + "/:id/budget/:bid")
    def supprimer_budget(req, id, bid):
        return {"ok": eng.supprimer_budget(id, bid)}

    @router.post(PREFIX + "/:id/planning")
    def ajouter_tache(req, id):
        rec = eng.ajouter_tache(id, req.json())
        return {"tache": rec, "session": eng.get(id)} if rec else Response.not_found("session inconnue")

    @router.delete(PREFIX + "/:id/planning/:tid")
    def supprimer_tache(req, id, tid):
        return {"ok": eng.supprimer_tache(id, tid)}

    # ------------------------------------------------------------- génération
    @router.post(PREFIX + "/:id/generer")
    def generer(req, id):
        s, err = _s(req, id)
        if err:
            return err
        p = req.json()
        kind = (p.get("gabarit") or p.get("kind") or "recap")
        if kind not in GABARITS:
            return Response.error(f"gabarit inconnu : {kind}", 400)
        formats = GABARITS[kind][1]
        fmt = (p.get("format") or p.get("fmt") or formats[0]).lower()
        if fmt not in formats:
            return Response.error(f"format {fmt} non disponible pour {kind}", 400)
        try:
            built = construire(kind, s, p.get("options") or {})
        except Exception as exc:
            return Response.error(f"construction impossible : {exc}", 500)

        doc = built.get("doc") or {"titre": s.get("titre", ""), "blocs": []}
        try:
            data, mime = docsgen.render(
                fmt, doc, diapos=built.get("diapos"),
                entetes=built.get("entetes"), lignes=built.get("lignes"),
                taches=built.get("taches"), titre_gantt=f"Planning — {s.get('titre','')}")
        except Exception as exc:
            log.error("meeting", f"rendu {kind}/{fmt} : {exc}")
            return Response.error(f"rendu impossible : {exc}", 500)

        horodatage = _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        nom = f"{horodatage}-{slug(s.get('titre', 'reunion') or 'reunion', 'reunion')[:40]}-{kind}.{fmt}"
        chemin = store.write_blob(nom, data, "documents")
        rec = {"id": nom, "nom": nom, "fichier": str(chemin), "format": fmt,
               "mime": mime, "gabarit": kind,
               "titre": doc.get("titre") or s.get("titre", ""),
               "cree_le": _dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
               "taille": len(data)}
        eng.ajouter_document(id, rec)
        log.info("meeting", f"{kind}.{fmt} généré ({len(data)} o) pour {id}")
        broadcast("meeting", {"kind": "document", "session": id,
                              "titre": rec["titre"], "format": fmt})
        return {"document": rec, "telechargement": f"/api/fichiers/{nom}"}

    @router.get(PREFIX + "/:id/documents")
    def documents(req, id):
        s, err = _s(req, id)
        return err or {"documents": s.get("documents") or []}

    @router.get(PREFIX + "/:id/export")
    def exporter(req, id):
        """Session complète en JSON : sauvegarde, reprise, transfert."""
        s, err = _s(req, id)
        if err:
            return err
        return Response.json(s, 200) if req.q("telecharger") else {"session": s}

    # ----------------------------------------------------------- flux (SSE)
    @router.get(PREFIX + "/:id/stream")
    def stream(req, emit, id):
        s = eng.get(id)
        titre = (s or {}).get("titre", "")
        emit("ouvert", {"session": id, "titre": titre})
        import time as _t
        try:
            for _ in range(3600):  # ~1 h de maintien
                _t.sleep(1)
                emit("ping", {"n": _})
        except Exception:
            pass

    # ------------------------------------------------- analyse à la volée
    @router.get(PREFIX + "/:id/resume")
    def resume(req, id):
        """Résumé instantané : pour l'affichage pendant la réunion."""
        s, err = _s(req, id)
        if err:
            return err
        return {
            "statut": s.get("statut"),
            "compteur": s.get("compteur") or {},
            "decisions": len(s.get("decisions") or []),
            "actions": len(s.get("actions") or []),
            "risques": len(s.get("risques") or []),
            "questions": len(s.get("questions") or []),
            "en_attente": len([x for x in (s.get("suggestions") or [])
                               if x.get("statut") == "attente"]),
            "budget_total": eng.total_budget(s),
            "documents": len(s.get("documents") or []),
            "duree": (s.get("transcript") or [{}])[0].get("t", ""),
        }

    @router.post(PREFIX + "/:id/analyser")
    def analyser(req, id):
        """Force un passage du modèle sur tout le verbatim (bouton « Analyser »)."""
        s, err = _s(req, id)
        if err:
            return err
        if not ctx.get("llm") or ctx["llm"].resolve() == "none":
            return Response.error("aucun modèle disponible : l'extraction "
                                  "déterministe reste active", 503)
        eng._enrichir_llm(id)
        return {"suggestions": eng.suggestions(id), "session": eng.get(id)}
