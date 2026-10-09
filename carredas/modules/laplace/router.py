"""Laplace ✳ — l'IA légère, sur tous les devices.

Elle ne travaille presque pas :
  1. elle reçoit le message (web, téléphone, Discord) ;
  2. elle détecte si la mémoire est UTILE (mots-clés de la config) ;
  3. elle transmet au patron (SOL ☉) — avec ou sans mémoire ;
  4. elle rend la réponse, formatée pour le canal.

Elle ne stocke rien localement. La mémoire vit chez le patron.
"""

from __future__ import annotations

from ...httpsrv import Response
from ..agents import engine as E
from ..agents import orchestrateur as O

PREFIX = "/api/laplace"


def _memoire_utile(texte: str, mots_cles: list[str]) -> bool:
    """La mémoire n'est consultée que si le message le justifie."""
    t = E.normaliser(texte)
    return any(E.normaliser(m) in t for m in (mots_cles or []))


def _chercher_memoire(store, texte: str, limite: int = 8) -> list[dict]:
    """Ce que le patron sait déjà sur ce sujet (travaux + conversations)."""
    t = E.normaliser(texte)
    mots = [m for m in t.split() if len(m) > 3][:6]
    out = []
    # travaux (exécutions du patron et des agents)
    for tr in sorted(store.all("agenttaches"),
                     key=lambda x: x.get("cree_le", ""), reverse=True):
        hay = E.normaliser(f"{tr.get('demande', '')} {tr.get('agent', '')}")
        if mots and sum(1 for m in mots if m in hay) >= 1:
            out.append({"type": "travail", "quand": tr.get("cree_le", ""),
                        "quoi": tr.get("demande", "")[:120],
                        "agent": tr.get("agent"),
                        "pertinence": sum(1 for m in mots if m in hay)})
    # conversations
    for m in sorted(store.all("chatmsgs"),
                    key=lambda x: x.get("cree_le", ""), reverse=True):
        if m.get("role") != "user":
            continue
        hay = E.normaliser(m.get("texte", ""))
        if mots and sum(1 for m2 in mots if m2 in hay) >= 1:
            out.append({"type": "message", "quand": m.get("cree_le", ""),
                        "quoi": m.get("texte", "")[:120],
                        "pertinence": sum(1 for m2 in mots if m2 in hay)})
    out.sort(key=lambda x: -x["pertinence"])
    return out[:limite]


def register(router, ctx):
    store = ctx["store"]
    config = ctx.get("config") or {}
    broadcast = ctx.get("broadcast") or (lambda *a, **k: None)

    def _cfg_laplace() -> dict:
        return (config.get("laplace") or {})

    @router.get(PREFIX + "/etat")
    def etat(req):
        c = _cfg_laplace()
        return {
            "nom": c.get("nom", "Laplace ✳"),
            "patron_url": c.get("patron_url", ""),
            "memoire_si_utile": c.get("memoire_si_utile", True),
            "canaux": c.get("canaux", {}),
            "patron": (config.get("patron") or {}).get("nom", "SOL ☉"),
        }

    @router.get(PREFIX + "/memoire")
    def memoire(req):
        """Consultation mémoire À LA DEMANDE (explicite)."""
        q = req.q("q") or ""
        if not q.strip():
            return Response.error("il manque le paramètre q", 400)
        return {"question": q, "resultats": _chercher_memoire(store, q),
                "total": len(_chercher_memoire(store, q))}

    @router.post(PREFIX + "/parler")
    def parler(req):
        """Parler à Laplace. Elle transmet au patron — presque sans travailler."""
        p = req.json() or {}
        texte = (p.get("texte") or p.get("message") or "").strip()
        if not texte:
            return Response.error("il manque le texte", 400)
        canal = (p.get("canal") or "web").lower()
        c = _cfg_laplace()

        # 1. la mémoire est-elle utile ? (seulement si le message le justifie)
        avec_memoire = bool(
            c.get("memoire_si_utile", True)
            and _memoire_utile(texte, c.get("memoire_si_mot_cle") or []))
        contexte: dict = {"canal": canal}
        memoire = []
        if avec_memoire:
            memoire = _chercher_memoire(store, texte)
            contexte["memoire"] = memoire
        if p.get("reunion_id"):
            s = store.get("reunions", p["reunion_id"])
            if s:
                contexte["session"] = s

        # 2. transmettre au patron (c'est lui qui travaille)
        r = O.parler(texte, contexte, store, broadcast, config=config)

        # le patron peut modifier la config (thème, fond…) : laplace applique
        modifs = r.get("config_modifs")
        if modifs:
            from ... import paths
            paths.patch_config(modifs)
            if isinstance(config, dict):
                config.clear(); config.update(paths.read_config())

        # 3. rendre compte — formaté pour le canal
        reponse = {
            "de": r["patron"]["nom"],
            "texte": r["texte_reponse"],
            "agent": r["agent"]["nom"],
            "agent_emoji": r["agent"].get("emoji", ""),
            "sous_agent_cree": bool(r.get("sous_agent")),
            "domaine": r.get("domaine"),
            "document": r.get("document"),
            "memoire_consultee": avec_memoire,
            "memoire": memoire if avec_memoire else [],
            "duree_s": r["duree_s"],
        }
        # formatage par canal (léger)
        if canal == "discord" and c.get("formater_par_canal", True):
            # Discord : markdown limité, pas de HTML
            reponse["texte"] = (reponse["texte"]
                                .replace("**", "**")  # le gras passe en Discord
                                )
        if canal == "telephone" and c.get("formater_par_canal", True):
            # téléphone : texte court, le document en lien
            if reponse.get("document"):
                reponse["texte"] += (f"\n\nDocument : {reponse['document']['nom']}")
        return reponse
