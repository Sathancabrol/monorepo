# S5 — Contrôle de complétude (« vérifie que tu n'as rien raté »)

**Date** : 2026-10-07 (soir) · **Déclencheur** : question utilisateur « il manque le module BTP non ? vérifie que tu n'as rien raté »
**Méthode** : re-scan complet en direct (9 dépôts, 46 branches, contenu des nouvelles branches, contenu détaillé du module BTP), croisement avec l'inventaire interne du dépôt (`docs/carre-das/07-INVENTAIRE-FONCTIONNALITES.md` + `scripts/verif-completude-repos.py`).

---

## 1. Réponse courte

| Question | Réponse |
|---|---|
| Le module BTP était-il absent de mes livrables ? | **Non — mais il était sous-décrit.** Il figurait dans 4 tableaux (audit §7, analyse D4-01, timeline ligne 5 des branches, roadmap palier 2030). Ce qui manquait : son **poids réel** (174 fichiers, 7 rapports, 28 sous-détails de prix, moteur multi-agents, dashboard 1,2 Mo) et sa **spécification cible** écrite aujourd'hui (7 piliers, 3D en 3 paliers). |
| Avais-je raté autre chose ? | **Oui — un chantier entier produit aujourd'hui entre 12 h 38 et 14 h 45 UTC**, après ma passe GitHub de la matinée : dossier « Carré d'As » (8 docs + 4 maquettes), dossier « recherche » (80 domaines, 10 chantiers P0), récupération `_incoming` (1 026 fichiers → 786 uniques), script de vérification de complétude, 2 nouvelles branches, module `mail-organizer`. |
| Cause | **Fenêtre de scan.** Mes relevés GitHub datent d'avant 12 h 38 ; les commits de l'après-midi (12:38 → 14:45) ne pouvaient pas y figurer. |
| Réparé ? | Oui : cette note + mise à jour de `SYNTHESE-TIMELINE` (17 branches, 46 au total, chronologie complétée, section modules), `ANALYSE-V1-V5` (+12 éléments → 91), `ROADMAP-2050-2026` (Carré d'As, Étape 0 en cours), `importance.json` régénéré. |

---

## 2. Ce qui manquait (liste exhaustive)

| # | Élément raté | Où il est | Pourquoi il compte | v |
|---|---|---|---|---|
| 1 | **Dossier « Carré d'As »** (00-CADRAGE, 01-CONTRAT-MODULE, 02-UI-PRINCIPES, 03-MODULE-BTP, 04-INTERFACES-3-PROPOSITIONS, 05-REPONSES, 06-ECOSYSTEME-LOCAL, 07-INVENTAIRE + 4 maquettes cliquables) | `docs/carre-das/` — branche `arena/0034230e-monorepo` | **Le nom, la cible (association), la licence, la définition du « fini » et le contrat de module de la V1** | v1 |
| 2 | **Dossier « recherche »** : brief pour agent, prompt à coller, **matrice de 80 domaines (D01→D80, priorités P0→P3)**, enrichissements et arbitrages | `docs/recherche/` — même branche | Le plan de recherche qui doit trancher l'architecture (dont bi-temporalité, PGlite vs PostgreSQL, MCP/A2A) | v1 |
| 3 | **`projects/_incoming/`** : récupération de **1 026 fichiers → 786 uniques** (240 doublons retirés, 46,2 Mo), 16 dossiers avec `_PROVENANCE.md` (dépôt, branche, SHA, écartés) | branche `arena/0034230e` | **Le travail des 17 branches n'est plus « invisible »** — il est importé et tracé | v1 |
| 4 | **`scripts/verif-completude-repos.py`** — vérifie par empreinte Git la couverture complète | idem | Contrôle rejouable de complétude (le concurrent de l'audit sur ce point) | v1 |
| 5 | **26 fichiers manquants restaurés** (25 composants proto perdus : onboarding, graphe Obsidian, CV ciblé, biais cognitifs, auth… + 1 .gitignore) | idem | Ce sont les composants **d'onboarding et de CV** — la plus grosse perte silencieuse, maintenant réparée | v1 |
| 6 | **Branche `arena/0034230e-monorepo`** (+5 commits) : carre-das + recherche + _incoming + **resync proto (12 fichiers)** + variante frontignan | nouvelle branche du 07/10 12:38→14:39 | **L'Étape 0 que je recommandais est déjà partiellement faite ici** | v1 |
| 7 | **Branche `arena/93b54a79-monorepo`** (+1) : module **`mail-organizer`** — tri d'emails par IMAP, règles configurables, extraction de pièces jointes, mode watch, **19 tests**, stdlib uniquement | nouvelle branche du 07/10 14:45 | Nouveau module réel (ingestion boîte mail) | v3 |
| 8 | **Spécification du module BTP** (03-MODULE-BTP) : 7 piliers, 3D en **3 paliers** (« assemblent, visualisent, mesurent — ne réécrivent pas un modeleur »), sync multi-comptes, modèle de données, feuille de route | `docs/carre-das/03-MODULE-BTP.md` | Le BTP passe de « branche à fusionner » à **brique forte spécifiée** | v3 |
| 9 | **Écosystème local gratuit** : modèles IA tenant dans **6 Go de VRAM** (Qwen 3.5 9B, Granite 4.2 8B pour l'extraction documentaire, Gemma 4 12B vision), Ollama, Whisper, Piper, OCR, **6 briques à créer** (routeur de modèles, cache, mode dégradé…) | `docs/carre-das/06-…` | Répond au « gratuit, local, hors ligne » avec des choix vérifiés | v3 |
| 10 | **Décisions cadrées** : cible **association loi 1901**, licence recommandée **cœur Apache-2.0/MIT + services AGPL-3.0**, RGPD/accessibilité, financement, **risque n°1 = bus factor** | `docs/carre-das/00/05` | Deux décisions ADR-009/007-like à ajouter au registre | v1 |
| 11 | **Analyse des 9 concept arts** + 3 propositions d'interface (« Le Carré », « L'Atelier », « L'Arbre ») | `04-INTERFACES…` + `maquettes/` | L'UI de la V1 a une base comparée, pas improvisée | v1 |
| 12 | **Séquence P0→P6 « expliquée en clair »** + ordre chronologique réel des travaux + politique corpus | `05-REPONSES-AUX-QUESTIONS.md` | Répond aux 7 questions du 07/10, dont la monétisation | v1 |

---

## 3. Ce que j'ai vérifié et confirmé (pas de faux positif)

| Vérification | Résultat |
|---|---|
| Dépôts du compte | **9, inchangé** (aucun dépôt nouveau, aucun renommé, 0 privé, 0 fork déclaré) |
| Branches | 46 au total ; **36 hors `main`** ; **17 avec travail non fusionné** (mon compte après les 2 nouvelles) — **identique au « 17 branches » de `07-INVENTAIRE`** ✅ |
| Branches mortes | **19**, toujours à 0 commit d'avance (leur contenu est dans `main`) |
| Commit non fusionnés | 153 → **159** (+5 de `0034230e`, +1 de `93b54a79`) |
| Drift proto | Mon audit : **25 fichiers distants absents** ; leur inventaire : **26 fichiers manquants** (25 composants + 1 `.gitignore`) → **cohérents** ✅ |
| BTP (chiffres) | **174 fichiers** = 154 documents (`documents_sources/`, 7 familles + 3 chantiers) + 9 rapports (00→08) + 5 données (JSON/CSV, SHA-256) + `engine/btp_multi_agent.py` (11,7 Ko) + `index.html` 1,2 Mo + `template.html` 1,0 Mo + matrice de traçabilité 26 Ko ✅ |
| nexus_os | « 147 tests » annoncés → **vérifié : 146 fonctions de test** sur 7 fichiers (19+21+23+4+28+35+16) + fixtures → ✅ (mon chiffre antérieur « 59 tests » venait d'un run partiel dans `CAPACITES-2026-10-07.md` : **corrigé** — nexus_os = 85 fichiers, 22 agents, ~147 tests) |
| _incoming | 16 dossiers `_PROVENANCE.md` confirmés (COGNITORIUM ×1, ETAT ×4+, monorepo ×6, proto ×1, watchtower ×2, Language-decoder ×2) ✅ |

---

## 4. Différences de comptage assumées (aucune n'est une erreur)

| Point | Mon chiffre | Leur chiffre | Explication |
|---|---|---|---|
| Fichiers `projects/` | **1 119** (9 projets, avant import) | **1 114** (8 dépôts satellites comparés) | Je compte `frontignan` et le README de `Language-decoder` ; eux comparent les 8 dépôts GitHub. Après leur import : proto 184, Language-decoder 1+51, frontignan +21, `_incoming` 786 uniques. |
| Branches avec travail | 34 hors `main` / 15 actives (matin) | 144 commits / 14 branches (doc antérieur), puis 17 branches | Périmètres et heures différents ; **nos états convergent le 07/10 au soir : 17 branches**. |
| Éléments classés v1→v5 | 79 | — (n'existait pas) | Leur apport ajoute 12 éléments → **91** après cette révision. |

---

## 5. Le BTP, correctement décrit (ce qui aurait dû y être)

**Module BTP = la brique forte de la V1** (cible `Carré d'As`) :

| Couche | Contenu réel (vérifié sur la branche) |
|---|---|
| **Corpus** | 154 documents classés en 7 familles (DCE/marchés, préparation et prix, DICT/AIPR/sécurité, exécution et CR, DOE/réception, RH/formation, plans) sur 3 chantiers réels (Barbazan, Saint-Nicolas-de-la-Grave, Pruniaux) |
| **Connaissance métier** | 9 rapports (00 synthèse → 08 BIM/IFC) dont le **schéma directeur de la chaîne chantier A→Z** |
| **Données** | inventaire JSON **avec SHA-256 par document** + CSV, synthèse chantiers et **barèmes des sous-détails de prix**, matrice de confrontation théorie / état de l'art / in-situ, ledger d'audit |
| **Applicatif** | dashboard `index.html` (1,2 Mo) : comparateur, catalogue des **28 sous-détails de prix** avec simulateur déboursé sec/marge, explorateur des 154 documents, lecteur des 7 rapports ; `engine/btp_multi_agent.py` |
| **Spécification cible** (07/10) | 7 piliers : documents/DCE (provenance par chiffre), prix/DQE/BPU/métrés, suivi de chantier, carte 2D IGN par défaut, 3D en 3 paliers (assembler, pas réécrire un modeleur), acteurs/sync multi-comptes, IA locale (Granite 4.2 pour l'extraction) |

**Conséquence de classement** : BTP reste **v3** (métier, dépend du Core), mais **monte en visibilité** : c'est la première brique dont la spécification complète existe (03-MODULE-BTP) — avec `carre-das` (v1) comme coquille.

---

## 6. Corrections appliquées (traçabilité)

| Livrable | Correction |
|---|---|
| `SYNTHESE-TIMELINE-2026-10.md` | chronologie complétée (12:38→14:45) · nouvelle section **modules** (BTP, nexus, mail-organizer, carre-das, recherche, _incoming) · tableau des branches → **17 actives** · chiffres (46 branches / 159 commits) · nom **Carré d'As** |
| `ANALYSE-V1-V5.md` | +12 éléments (§11) → **91** : répartition machine vérifiée v1=29, v2=24, v3=18, v4=10, v5=2, v0=8 |
| `audit/data/importance.json` | régénéré par `scripts/audit_importance.py` (91 éléments) |
| `ROADMAP-2050-2026.md` | palier 2026 : Étape 0 **déjà entamée** (resync proto, complétude, licence cadrée) · palier 2027 : nom **Carré d'As V1** |
| `state.json` | faits mis à jour (Carré d'As, 17 branches, 159 commits, 91 éléments) |

**Leçon pour l'audit lui-même** : une passe GitHub n'est valable qu'**horodatée** ; tout livrable doit porter l'heure de ses relevés. Ajouté à la discipline de mémoire : `audit_memory.py log` horodate déjà chaque étape — d'où l'importance de **relancer le scan avant toute fusion**.

---

## 7. Addendum — 3ᵉ passe « l'intégralité des modules » (2026-10-07, 15:20 UTC)

Déclencheur : « vérifie l'intégralité des modules, t'as raté des trucs ». Nouveau scan live + lecture des commits postérieurs (14:54 → 15:06). Registre exhaustif : **`audit/MODULES.md`**.

**Raté à la 2ᵉ passe (corrigé) :**

| Élément | Où |
|---|---|
| **`shell/`** — squelette UX/UI Carré d'As : **14 modules / 104 fonctionnalités** (62 dispo / 24 à porter / 18 à construire ; paliers V1=48, V1.5=34, V2=22), assistant JARVIS, sons Web Audio, design system du prototype `noeud neurono.html` | branche `0034230e`, commit `0ce2ddbb` (15:06) |
| Portail `index-acces.html` | commit `85e423c2` |
| **`docs/FEATURES-INVENTORY.md`** — features de tous les modules/apps + 6 lacunes | branche `93b54a79`, commit `dde1e2af` (15:03) |
| **BTP réécrit** : 21 onglets-modules + ~83 scripts ; 154 documents dédupliqués (préservés dans `_incoming`) ; branche 239→83 fichiers | branche `01a08449`, commit `1b7627b0` (14:54) |
| 5 modules ETAT récupérés d'un patch jamais appliqué (137 Ko : bias_cards, concept_details, experiment_templates, lab_endpoints, scientific_articles) | `_incoming/ETAT…` |
| `_incoming` = **859 fichiers** (brut importé 1 026, 786 uniques après dédoublonnage — trois périmètres distincts) | 16 `_PROVENANCE.md` |

**Compteurs live 15:20 UTC** : 46 branches · **18 actives** · 19 mortes · **167 commits non fusionnés** · 9 dépôts.

**Leçon** : le projet produit un lot toutes les ~20 minutes (12:38 → 15:06 : 10 commits majeurs). Toute vérification doit être horodatée, et le registre `MODULES.md` rafraîchi **avant chaque fusion**.
