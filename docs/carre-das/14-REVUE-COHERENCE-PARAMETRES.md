# Revue de cohérence — Carré d'As, 9 octobre 2026

**Mission** : regarder si notre travail est cohérent, logique, et identifier
ce qu'on a oublié ou ce qu'on devrait rajouter dans les **paramètres de l'OS**.
À 7 jours du RDV avec l'Agglo de Thau (16 octobre 2026).

---

## 1. Ce qui est cohérent ✅

| Élément | Pourquoi c'est cohérent |
|---|---|
| **Architecture plug in/out** | 8 modules, chacun = `module.json` + `router.py`. Le cœur ne connaît aucun module par son nom. Ajout/suppression sans toucher au core. |
| **Un seul interlocuteur** | Le chat ne répond que par ☉ SOL ☉ le patron. Plus de choix d'agent exposé. Cohérent avec la demande du 9 octobre. |
| **Le système solaire live** | Les 22 agents = des planètes, l'état (travaille/repos) est lu en direct, les sous-agents = des lunes. La métaphore tient partout (chat, visu, doc). |
| **Sous-agents réutilisables** | Créés à la volée, stockés, retrouvés par similarité (pas de doublon), traçables (créé_pour, parent). |
| **Méthode Frontignan** | ✅/≈/❓ + règle `fait_non_croise` — le vocabulaire de lecture est le même dans le core, l'UI et les documents générés. |
| **Zéro dépendance / offline** | Moteur force vanilla, pas de CDN, pas de WebGL. Tient sur un poste de mairie. |
| **Tests** | 83 assertions, scénario rejouable en une commande. |
| **Config GET/PUT** | `/api/config` existe, persistée dans `.carredas-data/config.json`, défauts dans `paths.py`. |

---

## 2. Ce qui cloche ou manque ⚠️

### 2.1 Des paramètres en dur dans le code (pas dans l'OS)

| Paramètre | Où il est | Problème |
|---|---|---|
| `SEUIL_ROUTAGE = 1.0` | `agents/orchestrateur.py` | Le patron crée un sous-agent selon un seuil codé en dur. L'utilisateur ne peut pas le régler. |
| `FENETRE_VISIBILITE_S = 20` | `agents/orchestrateur.py` | Durée d'affichage d'un travail. Codée en dur. |
| `SOURCES_OFFICIELLES` (~30 motifs) | `core/admissibilite.py` | La liste des producteurs publics est dans le code. Impossible à enrichir sans redeployer. |
| Nom/emoji du patron | `orchestrateur.py` (`NOM_PATRON`) | Codé en dur. |
| Activation des modules | `module.json` (`actif`) | Pour désactiver un module, il faut éditer un fichier. Pas de paramètre utilisateur. |

### 2.2 Contradictions avec le principe « on ne parle qu'au patron »

| Endroit | Problème |
|---|---|
| `POST /api/agents/executer` | Permet d'exécuter un agent **directement**, en contournant le patron. |
| `POST /api/agents/router` | Expose le routage — utile pour l'admin, mais l'utilisateur lambda ne devrait pas choisir. |
| Chat : paramètre `agent` | Le chat accepte encore `{"agent": "..."}` — on peut forcer un agent, contre le principe. |
| Vue Agents | Montre le routage et l'exécution directe. Cohérent pour un admin, incohérent pour l'utilisateur final. |

### 2.3 Oublis

| Oubli | Pourquoi ça compte le 16 octobre |
|---|---|
| **Pas de date d'échéance dans la config** | Le RDV du 16 octobre 2026 n'est nulle part dans l'OS. Un compte à rebours, des échéances sur les actions… |
| **Pas de profil émetteur** | Les documents générés ne portent pas le nom de l'association, du territoire, des contacts. |
| **Pas de paramètre de rétention** | Les conversations, travaux, documents s'accumulent sans limite ni politique. |
| **Pas de token d'accès** | Si Laplace tourne sur Discord/téléphone, l'API est ouverte à n'importe qui sur le réseau. |
| **Collection `sessions` vide** | Résidu (la vraie collection est `reunions`). 0 fichier, à documenter ou supprimer. |
| **Pas de paramètre « mémoire à la demande »** | Pour Laplace : quand consulter la mémoire, quand ne pas la consulter. |
| **Pas de canal de déploiement** | Discord, téléphone : aucun paramètre, aucun connecteur. |
| **desktop.py / updater.py non re-vérifiés** | L'installable et la mise à jour n'ont pas été re-testés depuis les nouveaux modules. |

---

## 3. Les paramètres à rajouter dans l'OS

Proposition de structure (à ajouter dans `paths.DEFAULT_CONFIG`) :

```json
{
  "patron": {
    "nom": "SOL ☉",
    "seuil_routage": 1.0,
    "fenetre_visibilite_s": 20,
    "creer_sous_agents": true,
    "montrer_qui_a_travaille": true
  },
  "laplace": {
    "actif": true,
    "patron_url": "http://127.0.0.1:8000",
    "memoire_si_utile": true,
    "memoire_si_mot_cle": ["rappelle", "retrouve", "mémoire", "avant", "déjà"],
    "canaux": { "discord": false, "telephone": false, "web": true },
    "longueur_max_message": 2000,
    "retention_conversations_j": 90
  },
  "acces": {
    "token": "",
    "exiger_token_si_distant": true,
    "origines_autorisees": []
  },
  "admissibilite": {
    "sources_officielles": ["insee", "ign", "…"],
    "signaler_fait_non_croise": true
  },
  "objectif": {
    "date": "2026-10-16",
    "titre": "RDV Agglo de Thau",
    "compte_a_rebours": true
  },
  "profil": {
    "organisation": "",
    "contact_nom": "",
    "contact_email": ""
  },
  "modules": {
    "desactives": []
  }
}
```

### Priorité pour le 16 octobre

| Priorité | Paramètre | Pourquoi |
|---|---|---|
| **P0** | `acces.token` | Sécuriser l'API avant de brancher Discord/téléphone |
| **P0** | `patron.seuil_routage` + `fenetre_visibilite_s` | Réglables sans redeployer |
| **P0** | `objectif.date` | Le compte à rebours du 16 octobre, visible dans l'UI |
| **P1** | `laplace.*` | Toute la config de la façade multi-device |
| **P1** | `admissibilite.sources_officielles` | Enrichissable sans redeployer |
| **P1** | `profil.*` | Les documents portent le nom de l'émetteur |
| **P2** | `modules.desactives` | Activer/désactiver sans éditer de fichier |
| **P2** | rétention | Politique de nettoyage |

---

## 4. Ce qu'on corrige tout de suite (code)

1. **Lire les paramètres depuis la config** au lieu des constantes en dur
   (orchestrateur, admissibilité)
2. **Retirer le paramètre `agent` du chat** — on ne parle qu'au patron
3. **Marquer `/api/agents/executer` et `/api/agents/router` comme internes**
   (admin uniquement, ou supprimés de l'UI utilisateur)
4. **Ajouter les paramètres** dans `DEFAULT_CONFIG`
5. **Ajouter le token d'accès** (vérification si origine distante)
6. **Ajouter le mode Laplace** (endpoint léger, mémoire à la demande)

---

## 5. Ce qu'on reporte (et pourquoi)

| Reporté | Pourquoi |
|---|---|
| Bot Discord complet | Le 16 octobre, la démo passe par le web. Discord = P2, après l'échéance. |
| Notifications téléphone | Idem — un lien web mobile suffit le 16. |
| Rétention automatique | Les données tiennent sur un poste. Politique à écrire, pas à coder en urgence. |
| Nettoyage collection `sessions` | Cosmétique. Documenté ici, pas bloquant. |
