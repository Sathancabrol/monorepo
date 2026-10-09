"""SOL ☉ — le patron. L'unique interlocuteur.

Tu ne parles pas aux agents. Tu parles au patron. Lui analyse, délègue,
surveille, rend compte — et quand la tâche dépasse le périmètre des 22
agents, il crée un **sous-agent** spécialisé à la volée.

Inspiré du système `cosmos/` (SOL ☉ orchestrateur, Laplace ✳ façade,
Métatron ✦ création d'agents) — adapté, pas recopié. La différence avec
cosmos/ : ici tout est déterministe, sans LLM, sans budget, offline.

Flux :
    VOUS → ☉ SOL (analyse) → délègue à l'agent compétent
                              │ travaille (6 phases, journalisé)
                              └─ si hors périmètre → crée un SOUS-AGENT
            → SOL rend compte + propose le document
"""

from __future__ import annotations

import datetime as _dt

from ... import docsgen
from ...store import new_id, slug
from . import engine as E

# seuil de routage : en dessous, le patron considère que la tâche
# dépasse le périmètre des agents connus → il crée un sous-agent
SEUIL_ROUTAGE = 1.0

# un travail reste visible ce délai après sa fin (pour que l'humain le voie)
FENETRE_VISIBILITE_S = 20

NOM_PATRON = "SOL ☉"
EMOJI_PATRON = "☉"


def _maintenant() -> str:
    return _dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def _secondes(iso: str) -> float:
    try:
        return (_dt.datetime.now()
                - _dt.datetime.strptime(iso, "%Y-%m-%dT%H:%M:%S")).total_seconds()
    except Exception:
        return 999999.0


# ------------------------------------------------------------- sous-agents
def creer_sous_agent(parent_id: str, domaine: str, tache: str, store,
                     demande: str = "") -> dict:
    """Crée un sous-agent spécialisé — une « lune » autour de sa planète mère.

    Réutilisable : si un sous-agent couvre déjà ce domaine pour ce parent,
    on le réactive plutôt que d'en recréer un.
    """
    parent = E.agent(parent_id)
    domaine_n = E.normaliser(domaine)[:40]
    mots_domaine = set(domaine_n.split())
    # réutilisation : même parent + domaine proche (au moins 40 % de mots communs)
    for s in store.all("sousagents"):
        if s.get("parent") != parent_id:
            continue
        mots = set((s.get("domaine") or "").split())
        if not mots or not mots_domaine:
            continue
        communs = len(mots & mots_domaine)
        if communs / max(1, len(mots | mots_domaine)) >= 0.4:
            s["reactive_le"] = _maintenant()
            s["nb_utilisations"] = s.get("nb_utilisations", 1) + 1
            store.put("sousagents", s["id"], s)
            return s
    sid = new_id("sous")
    nom = f"{parent['nom'] if parent else 'Agent'} · {domaine[:28]}"
    spec = {
        "id": sid,
        "nom": nom,
        "emoji": "☾",
        "parent": parent_id,
        "domaine": domaine_n,
        "role": f"Spécialiste du domaine « {domaine} » — créé par le patron "
                f"pour une tâche hors périmètre des agents connus.",
        "tache": tache[:200],
        "cree_pour": demande[:200],
        "cree_le": _maintenant(),
        "reactive_le": _maintenant(),
        "nb_utilisations": 1,
        "nb_taches": 0,
        "nb_reussites": 0,
    }
    store.put("sousagents", sid, spec)
    return spec


def lister_sous_agents(store) -> list[dict]:
    return sorted(store.all("sousagents"),
                  key=lambda s: s.get("cree_le", ""), reverse=True)


# ------------------------------------------------------------- état live
def etat_systeme(store, limite_travaux: int = 30) -> dict:
    """L'état du système en temps réel : qui travaille, quoi, quels sous-agents.

    Un travail est « en cours » s'il a commencé il y a moins de
    FENETRE_VISIBILITE_S secondes — comme ça l'humain voit les planètes
    s'activer même si l'exécution est rapide.
    """
    # travaux récents (collection agenttaches = exécutions du moteur)
    travaux = []
    for t in sorted(store.all("agenttaches"),
                    key=lambda x: x.get("cree_le", ""), reverse=True)[:limite_travaux]:
        age = _secondes(t.get("cree_le", ""))
        travaux.append({
            "id": t.get("id"), "agent": t.get("agent"),
            "demande": t.get("demande", "")[:80],
            "cree_le": t.get("cree_le"),
            "age_s": round(age, 1),
            "en_cours": age < FENETRE_VISIBILITE_S,
            "duree_s": t.get("duree_s", 0),
            "phases": len(t.get("phases") or []),
            "problemes": t.get("problemes", 0),
        })
    # travaux des sous-agents (mêmes phases, agent = id du sous-agent)
    agents_qui_travaillent = {t["agent"] for t in travaux if t["en_cours"]}

    # état de chaque agent
    agents = []
    for a in E.charger_agents():
        recents = [t for t in travaux if t["agent"] == a["id"]]
        en_cours = [t for t in recents if t["en_cours"]]
        agents.append({
            "id": a["id"], "nom": a["nom"], "emoji": a.get("emoji", "⬢"),
            "role": a.get("role", "")[:70],
            "etat": "travaille" if en_cours else "repos",
            "nb_travaux_visibles": len(en_cours),
            "nb_total": len(recents),
            "dernier_travail": recents[0]["cree_le"] if recents else None,
            "sous_agents": sum(1 for s in store.all("sousagents")
                               if s.get("parent") == a["id"]),
        })

    sous_agents = lister_sous_agents(store)
    return {
        "patron": {"nom": NOM_PATRON, "emoji": EMOJI_PATRON,
                   "role": "Orchestrateur — analyse, délègue, surveille, rend compte"},
        "agents": agents,
        "travaux": travaux,
        "travaux_en_cours": [t for t in travaux if t["en_cours"]],
        "sous_agents": sous_agents,
        "sous_agents_actifs": sum(1 for s in sous_agents
                                  if _secondes(s.get("reactive_le", "")) < FENETRE_VISIBILITE_S),
        "maintenant": _maintenant(),
    }


# ------------------------------------------------------------- le patron
def parler(texte: str, contexte: dict, store, broadcast=None) -> dict:
    """Tu parles au patron. Lui seul répond.

    1. analyse la demande (routage déterministe)
    2. si le routage est faible → crée un sous-agent spécialisé
    3. délègue (exécute les 6 phases)
    4. rend compte : qui a travaillé, ce qui a été produit, ce qui bloque
    """
    texte = (texte or "").strip()
    routes = E.router(texte, 3)
    meilleur = routes[0] if routes else None
    log: list[dict] = []

    def _e(event, detail, **extra):
        log.append({"event": event, "detail": detail, "quand": _maintenant(), **extra})
        if broadcast:
            broadcast("agents", {"kind": "orchestrateur", "event": event,
                                 "detail": detail, **extra})

    _e("recu", f"demande reçue : « {texte[:60]} »")

    # 1. analyse
    agent_choisi = E.choisir(texte)
    score = meilleur["score"] if meilleur else 0.0
    domaine = (meilleur["declencheurs"][0] if meilleur and meilleur["declencheurs"]
               else texte[:40])
    _e("analyse", f"domaine détecté : « {domaine} » (score {score})")

    # 2. hors périmètre ? → sous-agent
    sous_agent = None
    if score < SEUIL_ROUTAGE:
        sous_agent = creer_sous_agent(
            agent_choisi["id"], domaine, texte, store, demande=texte)
        _e("sous_agent_cree", f"☾ {sous_agent['nom']} "
             f"(parent : {agent_choisi['nom']})", sous_agent=sous_agent["id"])
        # le sous-agent hérite du rôle du parent et exécute à sa place
        agent_choisi = {"id": sous_agent["id"], "nom": sous_agent["nom"],
                        "emoji": "☾", "role": sous_agent["role"],
                        "cycle": E.agent(sous_agent["parent"]).get("cycle", [])
                        if E.agent(sous_agent["parent"]) else [],
                        "capacites": ["documents"], "sorties": ["document"],
                        "sous_agent": True}
    else:
        _e("delegue", f"→ {agent_choisi['emoji']} {agent_choisi['nom']}")

    # 3. délègue (exécution des 6 phases)
    res = E.executer(texte, agent_choisi["id"], contexte or {}, store)
    t = res["tache"]
    _e("travail_fini", f"{agent_choisi['nom']} a rendu son travail "
       f"({t['caracteres']} caractères)", tache=t["id"])

    # si c'était un sous-agent, crédite ses stats
    if sous_agent:
        sous_agent["nb_taches"] = sous_agent.get("nb_taches", 0) + 1
        if not res["problemes"]:
            sous_agent["nb_reussites"] = sous_agent.get("nb_reussites", 0) + 1
        store.put("sousagents", sous_agent["id"], sous_agent)

    # 4. rend compte — le patron parle
    lignes = [f"☉ **{NOM_PATRON}** — j'ai analysé votre demande "
              f"(domaine : « {domaine} »)."]
    if sous_agent:
        lignes.append(f"Aucun agent ne couvrait ce domaine : j'ai **créé un "
                      f"spécialiste** — ☾ {sous_agent['nom']} "
                      f"(sous-agent de {E.agent(sous_agent['parent'])['nom']}). "
                      f"Il a pris le relais.")
    else:
        lignes.append(f"J'ai **délégué à {agent_choisi['emoji']} "
                      f"{agent_choisi['nom']}** — {agent_choisi.get('role', '')}")
    lignes.append(f"Le travail s'est déroulé en **{len(t['phases'])} phases** "
                  f"({res['duree_s']} s).")
    r = res["recherche"]
    if r["outils"] or r["sources"]:
        lignes.append(f"Il a mobilisé **{len(r['outils'])} outil(s)** et "
                      f"**{len(r['sources'])} source(s)** des registres locaux.")
    else:
        lignes.append("Aucun outil ni source du registre local ne correspondait "
                      "— il n'a rien inventé.")
    if res["problemes"]:
        lignes.append(f"⚠ **{len(res['problemes'])} point(s) bloquant(s)** "
                      "signalé(s) par la revue d'admissibilité.")
    if res.get("signalements"):
        lignes.append(f"{len(res['signalements'])} signalement(s) à vérifier "
                      "(source unique, donnée manquante).")
    doc = res["document"]
    data, mime = docsgen.render("md", doc, taches=res.get("taches_gantt"),
                                titre_gantt=doc.get("titre", "Document"))
    horodatage = _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    nom = (f"{horodatage}-sol-{slug(texte[:36], 'demande')}.md")
    chemin = store.write_blob(nom, data, "documents")
    document = {"nom": nom, "taille": len(data), "mime": mime,
                "titre": doc.get("titre", "")}
    lignes.append(f"**Livrable** : « {document['titre']} » — `{nom}`.")
    _e("rendu_compte", f"livrable proposé : {nom}")

    return {
        "patron": {"nom": NOM_PATRON, "emoji": EMOJI_PATRON},
        "texte_reponse": "\n\n".join(lignes),
        "agent": res["agent"], "agent_choisi_par_le_patron": agent_choisi["id"],
        "sous_agent": sous_agent, "domaine": domaine, "score_routage": round(score, 2),
        "routes_analysees": [{"id": r["agent"]["id"], "nom": r["agent"]["nom"],
                              "score": r["score"]} for r in routes],
        "tache": t, "phases": t["phases"],
        "recherche": res["recherche"],
        "problemes": res["problemes"], "signalements": res.get("signalements", []),
        "document": document, "journal": log, "duree_s": res["duree_s"],
    }
