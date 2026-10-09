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

# Les valeurs par défaut — surclassées par la config de l'OS
# (patron.seuil_routage, patron.fenetre_visibilite_s, patron.nom…)
SEUIL_ROUTAGE_DEFAUT = 1.0
FENETRE_VISIBILITE_DEFAUT = 20
NOM_PATRON_DEFAUT = "SOL ☉"
EMOJI_PATRON_DEFAUT = "☉"


def _cfg_patron(config: dict | None) -> dict:
    """La section `patron` de la config, avec les défauts."""
    p = ((config or {}).get("patron") or {})
    return {
        "nom": p.get("nom") or NOM_PATRON_DEFAUT,
        "emoji": p.get("emoji") or EMOJI_PATRON_DEFAUT,
        "seuil_routage": float(p.get("seuil_routage", SEUIL_ROUTAGE_DEFAUT)),
        "fenetre_visibilite_s": float(p.get("fenetre_visibilite_s",
                                             FENETRE_VISIBILITE_DEFAUT)),
        "creer_sous_agents": bool(p.get("creer_sous_agents", True)),
    }


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
    # le sous-agent a aussi sa mémoire : dossier + fiche + rôle
    E.generer_fiche_sous_agent(store, spec)
    return spec


def lister_sous_agents(store) -> list[dict]:
    return sorted(store.all("sousagents"),
                  key=lambda s: s.get("cree_le", ""), reverse=True)


# ------------------------------------------------------------- état live
def etat_systeme(store, limite_travaux: int = 30,
                 fenetre_s: float = FENETRE_VISIBILITE_DEFAUT,
                 config: dict | None = None) -> dict:
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
            "en_cours": age < fenetre_s,
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
    cfg = _cfg_patron(config)
    return {
        "patron": {"nom": cfg["nom"], "emoji": cfg["emoji"],
                   "role": "Orchestrateur — analyse, délègue, surveille, rend compte"},
        "agents": agents,
        "travaux": travaux,
        "travaux_en_cours": [t for t in travaux if t["en_cours"]],
        "sous_agents": sous_agents,
        "sous_agents_actifs": sum(1 for s in sous_agents
                                  if _secondes(s.get("reactive_le", "")) < fenetre_s),
        "maintenant": _maintenant(),
    }


# ------------------------------------------------- personnalisation (UI)
# Le patron gère l'apparence — comme SOL gère l'interface dans cosmos/.
# « Change le thème », « mets un fond bleu », « crée un thème sunset » :
# le patron applique directement, en moins d'une minute, sans déléguer.

THEMES_CONNUS = {
    "nuit": "nuit", "night": "nuit", "sombre": "nuit", "dark": "nuit",
    "jour": "jour", "day": "jour", "clair": "jour", "light": "jour",
    "océan": "ocean", "ocean": "ocean", "mer": "ocean", "bleu": "ocean",
    "forêt": "foret", "foret": "foret", "vert": "foret", "forest": "foret",
    "sépia": "sepia", "sepia": "sepia", "chaud": "sepia",
}
MOTS_PERSONNALISATION = (
    "thème", "theme", "fond", "couleur", "apparence", "arrière-plan",
    "background", "clair", "sombre", "dark", "light", "océan", "forêt",
    "sépia", "personnalise", "personnalise", "customise", "customize",
    "change le thème", "change le fond", "couleur de fond",
)


def detecter_personnalisation(texte: str) -> dict | None:
    """Extrait une demande de personnalisation (thème / fond / couleurs).

    Retourne les modifications de config à appliquer, ou None si ce n'est
    pas une demande de personnalisation.
    """
    t = E.normaliser(texte)
    if not any(E.normaliser(m) in t for m in MOTS_PERSONNALISATION):
        return None
    modifs: dict = {"ui": {}}
    resume = []

    # 1. un thème prédéfini ?
    theme_trouve = None
    for mot, theme in THEMES_CONNUS.items():
        if E.normaliser(mot) in t:
            theme_trouve = theme
            break

    # 2. une couleur hex ? (fond ou accent)
    import re as _re
    hexas = _re.findall(r"#([0-9a-fA-F]{6})\b", texte)
    hexas = [f"#{h.lower()}" for h in hexas]

    # 3. création d'un thème personnalisé ? (« crée un thème sunset … »)
    m_creer = _re.search(r"(?:cr[ée]e|cr[ée]er|nouveau|fait) (?:un |le )?th[èe]me (?:appel[ée] )?['\"]?([a-z0-9_-]+)",
                         t)
    if m_creer and hexas:
        nom = m_creer.group(1)
        # le fond = première couleur, l'accent = deuxième (ou première)
        fond = hexas[0]
        accent = hexas[1] if len(hexas) > 1 else hexas[0]
        # jeu de variables dérivé du fond (approche sombre)
        modifs["ui"]["themes"] = {nom: {
            "nom": nom.capitalize(),
            "fond": fond,
            "variables": {
                "--bg": fond, "--bg-elev": _eclaircir(fond, 8),
                "--panel": _eclaircir(fond, 14), "--panel-2": _eclaircir(fond, 18),
                "--line": _eclaircir(fond, 30), "--line-2": _eclaircir(fond, 24),
                "--tx": "#E8E8F0", "--tx-2": "#A8A8C4",
                "--dim": "#8A8AA8", "--dim-2": "#4A4A6A",
                "--ac": accent, "--ac-dim": _assombrir(accent, 40),
                "--warn": "#FFB020", "--bad": "#FF3366",
                "--ok": "#3DDC97", "--info": "#4A90D9",
            }}}
        modifs["ui"]["theme"] = nom
        resume.append(f"thème « {nom} » créé (fond {fond}, accent {accent}) et appliqué")
    elif theme_trouve:
        modifs["ui"]["theme"] = theme_trouve
        resume.append(f"thème « {theme_trouve} » appliqué")
    elif hexas:
        # « mets un fond #0A1E38 » → fond custom
        modifs["ui"]["fond"] = hexas[0]
        resume.append(f"fond personnalisé appliqué ({hexas[0]})")
    elif "d[ée]grad" in t or "dégradé" in t or "gradient" in t:
        modifs["ui"]["fond"] = "linear-gradient(160deg, #050508 0%, #0A1E38 100%)"
        resume.append("fond en dégradé appliqué")
    else:
        return None

    return {"modifs": modifs, "resume": " · ".join(resume)}


def _eclaircir(hexcol: str, pct: int) -> str:
    """Éclaircit une couleur hex de pct % (approche simple)."""
    try:
        h = hexcol.lstrip("#")
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
        f = 1 + pct / 100
        return "#%02x%02x%02x" % (min(255, int(r * f)),
                                  min(255, int(g * f)), min(255, int(b * f)))
    except Exception:
        return hexcol


def _assombrir(hexcol: str, pct: int) -> str:
    try:
        h = hexcol.lstrip("#")
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
        f = 1 - pct / 100
        return "#%02x%02x%02x" % (max(0, int(r * f)),
                                  max(0, int(g * f)), max(0, int(b * f)))
    except Exception:
        return hexcol


# ------------------------------------------------------------- le patron
def parler(texte: str, contexte: dict, store, broadcast=None,
           config: dict | None = None) -> dict:
    """Tu parles au patron. Lui seul répond.

    1. analyse la demande (routage déterministe)
    2. si le routage est faible → crée un sous-agent spécialisé
    3. délègue (exécute les 6 phases)
    4. rend compte : qui a travaillé, ce qui a été produit, ce qui bloque
    """
    texte = (texte or "").strip()
    cfg = _cfg_patron(config)
    log: list[dict] = []

    def _e(event, detail, **extra):
        log.append({"event": event, "detail": detail, "quand": _maintenant(), **extra})
        if broadcast:
            broadcast("agents", {"kind": "orchestrateur", "event": event,
                                 "detail": detail, **extra})

    _e("recu", f"demande reçue : « {texte[:60]} »")

    # 0. PERSONNALISATION : le patron gère l'apparence lui-même
    #    (thème, fond, couleurs) — pas de délégation, application immédiate.
    perso = detecter_personnalisation(texte)
    if perso:
        _e("personnalisation", perso["resume"])
        lignes = [f"{cfg['emoji']} **{cfg['nom']}** — j'applique votre demande "
                  f"d'apparence : {perso['resume']}."]
        lignes.append("C'est fait — le changement est visible immédiatement. "
                      "Dites-moi si vous validez, ou demandez un ajustement.")
        return {
            "patron": {"nom": cfg["nom"], "emoji": cfg["emoji"]},
            "texte_reponse": "\n\n".join(lignes),
            "personnalisation": True,
            "config_modifiee": True,
            "config_modifs": perso["modifs"],
            "agent": {"id": "sol", "nom": cfg["nom"], "emoji": cfg["emoji"],
                      "role": "Le patron applique lui-même"},
            "agent_choisi_par_le_patron": "sol",
            "sous_agent": None, "domaine": "apparence",
            "routes_analysees": [], "tache": {"phases": []},
            "phases": [],
            "recherche": {"outils": [], "sources": []},
            "problemes": [], "signalements": [],
            "document": None, "journal": log, "duree_s": 0,
        }

    routes = E.router(texte, 3)
    meilleur = routes[0] if routes else None

    # 1. analyse
    agent_choisi = E.choisir(texte)
    score = meilleur["score"] if meilleur else 0.0
    domaine = (meilleur["declencheurs"][0] if meilleur and meilleur["declencheurs"]
               else texte[:40])
    _e("analyse", f"domaine détecté : « {domaine} » (score {score})")

    # 2. hors périmètre ? → sous-agent (seuil réglable dans l'OS).
    #    Deux cas : le routage est vraiment faible (score sous le seuil),
    #    ou le meilleur match est un faux ami — le début de la demande est
    #    un vrai domaine que l'agent ne couvre pas (« qualité de l'air » ≠ relecteur).
    sous_agent = None
    agent_reel = E.agent(agent_choisi["id"])
    inattendu = False
    if agent_reel and meilleur and meilleur["declencheurs"]:
        t_n = E.normaliser(texte)
        declencheur = E.normaliser(meilleur["declencheurs"][0])
        if declencheur in t_n:
            isole = t_n.replace(declencheur, "")
            mots = [m for m in isole.split() if len(m) > 4]
            causes = " ".join(E.normaliser(
                " ".join(agent_reel.get("declencheurs") or [])))
            inattendu = bool(mots and sum(1 for m in mots if m in causes) == 0)

    doit_creer = ((score < cfg["seuil_routage"])
                  or (score <= 1.0 and inattendu)) \
                 and cfg["creer_sous_agents"]
    if doit_creer:
        # le domaine = le texte de la demande tronqué (précis, retrouvable),
        # pas le mot-clé — sinon tous les sous-agents s'appelleraient « qualité »
        domaine_sous = texte[:60]
        sous_agent = creer_sous_agent(
            agent_choisi["id"], domaine_sous, texte, store, demande=texte)
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
    res = E.executer(texte, agent_choisi["id"], contexte or {}, store,
                     config=config)
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
    lignes = [f"{cfg['emoji']} **{cfg['nom']}** — j'ai analysé votre demande "
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
        "patron": {"nom": cfg["nom"], "emoji": cfg["emoji"]},
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
