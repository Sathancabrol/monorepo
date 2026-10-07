# Carré d'As — dossier de cadrage

**Carré d'As** est le nom retenu pour **l'application** : la première itération fonctionnelle, installable et utilisable de **Cognitorium** (le système global). Cible : **association** (loi 1901). Ordre : **Windows d'abord, navigateur ensuite**. Architecture : **un shell + des modules plug in / plug out**.

## Contenu

| Fichier | Objet |
|---|---|
| **`00-CADRAGE-CARRE-D-AS.md`** | Le cadrage de la V1 : ce que le nom change, ce que la cible association implique (licence, RGPD, accessibilité, financement), la définition du « fini » installable, **le gisement déjà écrit dans les branches**, l'architecture shell + modules, le contenu de la V1, la séquence de réalisation, les risques, les décisions à prendre |
| **`01-CONTRAT-MODULE.md`** | Le contrat qui rend un module **plug in/out** : manifeste (`module.json`), cycle de vie sans redémarrage, permissions « rien par défaut », bus d'événements, points d'extension d'interface, propriété des données, versionnement, critères d'acceptation |
| **`02-UI-PRINCIPES-ET-INSPIRATIONS.md`** | L'interface : 5 règles non négociables, structure du shell (rail, zone de travail, panneaux, dock, palette), écrans de la V1, 10 règles d'affordance vérifiables, inspirations des branches et de l'extérieur, anti-patterns, indicateurs à mesurer |
| **`03-MODULE-BTP.md`** | La brique BTP : ce qui existe déjà (154 documents, 7 rapports, 28 sous-détails de prix), les 7 piliers, la décision 3D en trois paliers, la synchronisation multi-comptes, le modèle de données, la feuille de route, les risques |

## À lire avec

- `../recherche/` — le brief à donner à un agent de recherche (85 domaines, 10 chantiers P0), mis à jour des décisions du 2026-10-07.
- `../../projects/COGNITORIUM/docs/constitution/` — la gouvernance d'origine (vision, principes, ADR).
- `../../projects/watchtower/audit/` — le registre d'outils, les coûts, les licences.

## Statut

`ANALYSE` — rien n'est implémenté. Toute proposition de ce dossier doit être validée avant d'écrire du code. Les faits issus de l'extérieur sont datés et sourcés ; les propositions sont marquées comme telles.
