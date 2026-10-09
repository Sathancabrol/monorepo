# Laplace ✳ — l'IA légère, sur tous tes devices

**Date** : 9 octobre 2026 · **Référence** : `cosmos/laplace.py` (ETAT-DE-LART-PSYCHOLOGIE)
— *« Laplace ✳ — interlocuteur principal (remplace SOL en façade) »*.
Même idée, adaptée : **Laplace ne travaille presque pas**.

---

## 1. La séparation des rôles

| | ☉ SOL — le patron | ✳ Laplace — la façade |
|---|---|---|
| **Où ça tourne** | La machine principale (ton serveur Carré d'As) | Partout : ordi, téléphone, Discord |
| **Poids** | Lourd : mémoire, 22 agents, documents, registres | **Léger : un client HTTP** |
| **Travail** | Analyse, délègue, produit, rend compte | **Transmet et rend compte. Presque rien d'autre.** |
| **Mémoire** | La tient, la consulte, l'enrichit | **La consulte seulement si utile** |
| **Règle** | *Le patron ne délègue jamais dans le vide* | *Laplace ne cherche jamais sans raison* |

```
  TÉLÉPHONE / DISCORD / NAVIGATEUR
        │  (client léger)
        ▼
  ✳ LAPLACE — reçoit, transmet, rend compte
        │  HTTP (token)
        ▼
  ☉ SOL — le patron (machine principale)
    analyse → délègue → produit → rend compte
        │
        ▼
  ✳ LAPLACE — rend le résultat à l'utilisateur
```

**Pourquoi cette séparation** : le téléphone n'a pas la mémoire, pas les
registres, pas les agents. Il n'a pas besoin. Il a besoin de **parler au
patron** et de **relire le résultat**. Laplace fait exactement ça, et rien
de plus.

---

## 2. Ce que Laplace ne fait presque pas

| Elle ne fait PAS | Pourquoi |
|---|---|
| ❌ Analyser la demande en profondeur | C'est le patron qui analyse |
| ❌ Choisir un agent | C'est le patron qui délègue |
| ❌ Produire un document | C'est le patron et ses agents |
| ❌ Lire toute la mémoire à chaque message | **Seulement si utile** |
| ❌ Stocker quoi que ce soit localement | La mémoire vit chez le patron |

| Elle fait | Quand |
|---|---|
| ✅ Recevoir le message | Toujours |
| ✅ Le transmettre au patron | Toujours |
| ✅ Rendre la réponse | Toujours |
| ✅ **Consulter la mémoire** | **Seulement si le message le justifie** |
| ✅ Vérifier la cohérence de l'échange | Si activé (`laplace.verifier_coherence`) |
| ✅ tronquer / formater pour le device | Téléphone (écran petit), Discord (markdown limité) |

---

## 3. « Chercher la mémoire seulement si utile »

La mémoire n'est pas un réflexe. C'est un **coût** (temps, pertinence,
bruit). Laplace consulte la mémoire du patron **uniquement** quand le message
contient un mot-clé de rappel, ou quand l'utilisateur demande explicitement
un historique.

```json
"laplace": {
  "memoire_si_utile": true,
  "memoire_si_mot_cle": ["rappelle", "retrouve", "mémoire", "avant", "déjà",
                          "historique", "dernier", "précédemment"],
  "memoire_si_demande_explicite": true
}
```

| Le message… | Laplace consulte la mémoire ? |
|---|---|
| « Rédige le compte rendu » | ❌ Non — le patron travaille, la mémoire n'aiderait pas |
| « Rappelle-moi ce qu'on a décidé mardi » | ✅ Oui — mot-clé « rappelle » |
| « On avait parlé de la Frange Sud, retrouve » | ✅ Oui — mot-clé « retrouve » |
| « Quel est l'historique de ce dossier ? » | ✅ Oui — demande explicite |

**Implémentation** : Laplace envoie au patron un flag
`avec_memoire: true/false`. Le patron ne joint la mémoire au contexte que
si le flag est levé. **La mémoire n'est jamais dans la réponse par défaut.**

---

## 4. Les canaux (devices)

| Canal | Forme | Statut le 16 octobre |
|---|---|---|
| **Web (navigateur)** | L'app Carré d'As elle-même | ✅ Déjà là — c'est le chat avec le patron |
| **Téléphone** | Même app, responsive (l'UI tient sur mobile) | ✅ À vérifier (test responsive) |
| **Discord** | Bot ou webhook qui relaie vers `/api/laplace/parler` | 🔲 P2 — après l'échéance |
| **Autre device** | N'importe quel client HTTP avec le token | 🔲 Le token rend ça possible |

**Le token** (`acces.token` dans la config) : sans lui, n'importe qui sur le
réseau peut parler au patron. Avec lui, seuls les devices autorisés
s'enregistrent. Laplace le porte, le patron le vérifie.

---

## 5. La cohérence — Laplace vérifie

Laplace a un rôle de **vigie** : elle regarde si l'échange est cohérent.
C'est léger, côté patron (pas côté device) :

| Vérification | Comment |
|---|---|
| La réponse répond-elle à la demande ? | Le patron le fait (phase revue) |
| Y a-t-il des contradictions dans la conversation ? | Laplace compare avec les 3 derniers échanges (mémoire de session, pas mémoire longue) |
| A-t-on oublié une suite ? | Laplace détecte les actions ouvertes sans échéance |

Paramètre : `laplace.verifier_coherence: true`.

---

## 6. Paramètres (dans l'OS)

```json
"laplace": {
  "actif": true,
  "nom": "Laplace ✳",
  "patron_url": "http://127.0.0.1:8000",
  "memoire_si_utile": true,
  "memoire_si_mot_cle": ["rappelle", "retrouve", "mémoire", "avant", "déjà"],
  "verifier_coherence": true,
  "formater_par_canal": true,
  "canaux": { "web": true, "discord": false, "telephone": true },
  "longueur_max_message": 2000,
  "retention_conversations_j": 90
}
```

---

## 7. Ce qu'on implémente maintenant

| Pièce | Où |
|---|---|
| Paramètres `laplace`, `patron`, `acces`, `objectif`, `profil`, `admissibilite`, `modules` | `paths.DEFAULT_CONFIG` |
| Le patron lit `patron.seuil_routage` et `patron.fenetre_visibilite_s` | `orchestrateur.py` (plus de constantes en dur) |
| L'admissibilité lit `admissibilite.sources_officielles` | `core/admissibilite.py` |
| Le chat retire le paramètre `agent` | `modules/chat` |
| `POST /api/laplace/parler` — transmet au patron, mémoire si utile | `modules/chat/router.py` (ou route core) |
| Vérification du token si origine distante | `server.py` (middleware léger) |
| Vue Système : exposer les nouveaux paramètres | `ui/app.js` |
| Compte à rebours 16 octobre | `ui/app.js` (accueil) |

**Ce qu'on reporte** : bot Discord complet, notifications push — après le 16.
