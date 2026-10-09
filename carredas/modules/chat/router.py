"""Routes du chat — parler aux agents."""

from __future__ import annotations

from ...httpsrv import Response
from . import engine as E

PREFIX = "/api/chat"


def register(router, ctx):
    store = ctx["store"]
    broadcast = ctx.get("broadcast") or (lambda *a, **k: None)

    @router.get(PREFIX + "/conversations")
    def liste(req):
        return {"conversations": E.conversations(store)}

    @router.post(PREFIX + "/conversations")
    def creer(req):
        p = req.json() or {}
        return {"conversation": E.nouvelle_conversation(store, p.get("titre") or "")}

    @router.get(PREFIX + "/conversations/:id")
    def detail(req, id):
        conv = E.conversation(store, id)
        if not conv:
            return Response.not_found("conversation inconnue")
        return {"conversation": conv, "messages": E.messages(store, id)}

    @router.post(PREFIX + "/conversations/:id/messages")
    def envoyer(req, id):
        conv = E.conversation(store, id)
        if not conv:
            return Response.not_found("conversation inconnue")
        p = req.json() or {}
        texte = (p.get("texte") or p.get("message") or "").strip()
        if not texte:
            return Response.error("il manque le texte du message", 400)
        contexte = {}
        if p.get("reunion_id"):
            s = store.get("reunions", p["reunion_id"])
            if s:
                contexte["session"] = s
        r = E.envoyer(store, id, texte, p.get("agent"), contexte,
                      produire=p.get("produire", True), broadcast=broadcast)
        if not r:
            return Response.error("message vide", 400)
        return {"message": r, "conversation": E.conversation(store, id)}

    @router.delete(PREFIX + "/conversations/:id")
    def supprimer(req, id):
        return {"ok": E.supprimer(store, id)}
