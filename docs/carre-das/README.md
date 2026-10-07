# Carré d'As — dossier de cadrage

**Carré d'As** est le nom retenu pour **l'application** : la première itération fonctionnelle, installable et utilisable de **Cognitorium** (le système global). Cible : **association** (loi 1901). Ordre : **Windows d'abord, navigateur ensuite**. Architecture : **un shell + des modules plug in / plug out**.

## Contenu

| Fichier | Objet |
|---|---|
| **`00-CADRAGE-CARRE-D-AS.md`** | Le cadrage de la V1 : ce que le nom change, ce que la cible association implique (licence, RGPD, accessibilité, financement), la définition du « fini » installable, **le gisement déjà écrit dans les branches**, l'architecture shell + modules, le contenu de la V1, la séquence de réalisation, les risques, les décisions à prendre |
| **`01-CONTRAT-MODULE.md`** | Le contrat qui rend un module **plug in/out** : manifeste (`module.json`), cycle de vie sans redémarrage, permissions « rien par défaut », bus d'événements, points d'extension d'interface, propriété des données, versionnement, critères d'acceptation |
| **`02-UI-PRINCIPES-ET-INSPIRATIONS.md`** | L'interface : 5 règles non négociables, structure du shell (rail, zone de travail, panneaux, dock, palette), écrans de la V1, 10 règles d'affordance vérifiables, inspirations des branches et de l'extérieur, anti-patterns, indicateurs à mesurer |
| **`03-MODULE-BTP.md`** | La brique BTP : ce qui existe déjà (154 documents, 7 rapports, 28 sous-détails de prix), les 7 piliers, la décision 3D en trois paliers, la synchronisation multi-comptes, le modèle de données, la feuille de route, les risques |
| **`04-INTERFACES-3-PROPOSITIONS.md`** | Analyse des **9 concept arts retrouvés** (ADN commun, divergences, ce qu'on retire) + **3 propositions d'interface** comparées et recommandation : V1 « Le Carré » (accueil), V2 « L'Atelier » (travail), V3 « L'Arbre » (exploration) |
| **`maquettes/`** | Les maquettes **cliquables**, autonomes (aucune dépendance) : `index.html` (comparateur) · `v1-le-carre.html` · `v2-l-atelier.html` · `v3-l-arbre.html` |
| **`05-REPONSES-AUX-QUESTIONS.md`** | Réponses aux 7 points du 2026-10-07 : **licence sous l'angle monétisation** (association + open core + CLA), **séquence P0→P6 expliquée en clair**, **ordre chronologique réel des travaux** (retrouvé sur GitHub + Drive), **corpus conservé dans Git** (proposition retirée et remplacée par une politique) |
| **`06-ECOSYSTEME-LOCAL-GRATUIT.md`** | L'écosystème libre et hors ligne : **modèles IA locaux** tenant dans 6 Go de VRAM, écosystème « prepper » (Kiwix, Project NOMAD, pimaps, Organic Maps, ODK/Kobo), **cartes et fiches ID**, précautions de licence, **liste des 6 briques à créer** |

| **`07-INVENTAIRE-FONCTIONNALITES.md`** | **Rien ne manque** : contrôle fichier par fichier des 9 dépôts (1 114 fichiers) et de leurs **17 branches non fusionnées**, récupération de tout ce qui manquait, et **matrice « quel dépôt apporte quelle fonctionnalité → quel module de Carré d'As »** |
| **`08-SQUELETTE-UX-UI.md`** | Le **squelette d'interface** : design system repris du prototype d'origine (Void/Plasticity/Transfer), structure du shell, 8 portes / 14 modules / **104 fonctionnalités**, assistant (voix, orbe, guidage), sons, mode d'emploi pour brancher un module |
| **`../../shell/`** | **Le squelette, en code** : `index.html` (template) + `assets/` (tokens, structure, registre, shell, assistant, sons) + `data/modules.json` + `tools/` (générateur et contrôle) |
| **`../../scripts/verif-completude-repos.py`** | Le contrôle rejouable : vérifie par **empreinte Git** que tout le contenu des dépôts et de leurs branches est présent dans le monorepo |
| **`../../projects/_incoming/`** | Le travail des branches, rangé par dépôt et par branche, **avec un `_PROVENANCE.md`** (dépôt, branche, commit, fichiers) dans chaque dossier |

**Rappel des livrables antérieurs** : `00` à `03` sont commités (`df13086`) ; `04` à `08`, les maquettes et le squelette sont postérieurs.

## À lire avec

- `../recherche/` — le brief à donner à un agent de recherche (85 domaines, 10 chantiers P0), mis à jour des décisions du 2026-10-07.
- `../../projects/COGNITORIUM/docs/constitution/` — la gouvernance d'origine (vision, principes, ADR).
- `../../projects/watchtower/audit/` — le registre d'outils, les coûts, les licences.

## Statut

`ANALYSE` — rien n'est implémenté. Toute proposition de ce dossier doit être validée avant d'écrire du code. Les faits issus de l'extérieur sont datés et sourcés ; les propositions sont marquées comme telles.
