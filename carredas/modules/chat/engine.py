"""Moteur du chat : une conversation avec les agents.

Un message n'est pas envoyé à un chatbot générique : il est **routé** vers un
agent (moteur déterministe du module agents), qui **exécute** la demande et
produit une réponse structurée :

    {"agent": ..., "reponse": "...", "phases": [...], "document": {...},
     "recherche": {...}, "problemes": [...]}

Le chat garde l'historique des conversations et des messages. Il ne prétend
jamais savoir : si aucun agent ne correspond, c'est l'orchestrateur qui
répond, et il le dit.
"""

from __future__ import annotations

import datetime as _dt

from ..agents import engine as E


def _maintenant() -> str:
    return _dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def nouvelle_conversation(store, titre: str = "") -> dict:
    from ...store import new_id
    cid = new_id("chat")
    conv = {"id": cid, "titre": titre or "Nouvelle conversation",
            "cree_le": _maintenant(), "maj_le": _maintenant(),
            "nb_messages": 0}
    store.put("chatconv", cid, conv)
    return conv


def conversations(store) -> list[dict]:
    out = sorted(store.all("chatconv"),
                 key=lambda c: c.get("maj_le", ""), reverse=True)
    for c in out:
        c["nb_messages"] = sum(1 for m in store.all("chatmsgs")
                               if m.get("conversation") == c["id"])
    return out


def conversation(store, cid: str) -> dict | None:
    return store.get("chatconv", cid)


def messages(store, cid: str) -> list[dict]:
    return sorted((m for m in store.all("chatmsgs")
                   if m.get("conversation") == cid),
                  key=lambda m: m.get("cree_le", ""))


def _reponse_texte(demande: str, res: dict) -> str:
    """Un texte lisible, honnête, qui dit ce qui a été fait — et ce qui ne l'a pas été."""
    a = res["agent"]
    t = res["tache"]
    lignes = [f"{a['emoji']} **{a['nom']}** a pris la demande."]
    phases_ok = sum(1 for p in t["phases"] if p["statut"] == "ok")
    lignes.append(f"{phases_ok}/{len(t['phases'])} phases déroulées "
                  f"en {res['duree_s']} s.")
    r = res["recherche"]
    if r["outils"] or r["sources"]:
        lignes.append(f"J'ai trouvé {len(r['outils'])} outil(s) et "
                      f"{len(r['sources'])} source(s) dans les registres locaux.")
    else:
        lignes.append("Aucun outil ni source du registre local ne correspond — "
                      "je ne produis que ce qui est vérifiable.")
    if res["problemes"]:
        lignes.append(f"⚠ {len(res['problemes'])} point(s) bloquant(s) signalé(s) "
                      "par la revue d'admissibilité.")
    if res.get("signalements"):
        lignes.append(f"{len(res['signalements'])} signalement(s) à vérifier "
                      "(source unique, donnée manquante).")
    doc = res.get("document")
    if doc:
        lignes.append(f"Document produit : « {doc.get('titre', 'document')} ».")
    return "\n\n".join(lignes)


def envoyer(store, cid: str, texte: str, agent_id: str | None = None,
            contexte: dict | None = None, produire: bool = True) -> dict:
    """Envoie un message : routage → exécution → réponse structurée."""
    from ...store import new_id
    from ... import docsgen
    from ...store import slug
    import datetime as _dt2

    conv = conversation(store, cid)
    if not conv:
        return {}
    texte = (texte or "").strip()
    if not texte:
        return {}

    # routage (pour savoir qui répond, même sans exécution)
    routes = E.router(texte, 3)
    choisi = E.choisir(texte, agent_id)

    msg = {"id": new_id("msg"), "conversation": cid, "role": "user",
           "texte": texte, "agent_choisi": choisi["id"],
           "routes": [{"id": r["agent"]["id"], "nom": r["agent"]["nom"],
                       "score": r["score"]} for r in routes],
           "cree_le": _maintenant()}
    store.put("chatmsgs", msg["id"], msg)

    reponse: dict = {"role": "agent", "agent": choisi["id"],
                     "nom": choisi["nom"], "emoji": choisi.get("emoji", "⬢")}
    if produire:
        try:
            res = E.executer(texte, agent_id, contexte or {}, store)
            reponse["texte_reponse"] = _reponse_texte(texte, res)
            reponse["phases"] = res["tache"]["phases"]
            reponse["recherche"] = res["recherche"]
            reponse["problemes"] = res["problemes"]
            reponse["signalements"] = res.get("signalements", [])
            reponse["duree_s"] = res["duree_s"]
            # le document produit par l'agent, s'il y en a un
            doc = res["document"]
            data, mime = docsgen.render("md", doc, taches=res.get("taches_gantt"),
                                        titre_gantt=doc.get("titre", "Document"))
            horodatage = _dt2.datetime.now().strftime("%Y%m%d-%H%M%S")
            nom = (f"{horodatage}-chat-{slug(choisi['id'], 'agent')}-"
                   f"{slug(texte[:36], 'msg')}.md")
            chemin = store.write_blob(nom, data, "documents")
            reponse["document"] = {"nom": nom, "taille": len(data), "mime": mime,
                                   "titre": doc.get("titre", "")}
        except Exception as exc:
            reponse["texte_reponse"] = (f"L'exécution a échoué : {exc}. "
                                        "Je ne produis pas de résultat dans ce cas.")
            reponse["erreur"] = str(exc)
    else:
        reponse["texte_reponse"] = _reponse_texte(texte, {
            "agent": choisi, "tache": {"phases": []}, "recherche": {"outils": [], "sources": []},
            "problemes": [], "signalements": [], "duree_s": 0, "document": None})

    reponse.update({"id": new_id("msg"), "conversation": cid,
                    "cree_le": _maintenant()})
    store.put("chatmsgs", reponse["id"], reponse)

    conv["maj_le"] = _maintenant()
    conv["nb_messages"] = conv.get("nb_messages", 0) + 2
    if conv.get("titre", "") in ("", "Nouvelle conversation"):
        conv["titre"] = texte[:60]
    store.put("chatconv", cid, conv)
    return reponse


def supprimer(store, cid: str) -> bool:
    if not conversation(store, cid):
        return False
    for m in store.all("chatmsgs"):
        if m.get("conversation") == cid:
            store.delete("chatmsgs", m["id"])
    store.delete("chatconv", cid)
    return True
