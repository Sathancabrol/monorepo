# S4 — Documents externes (connecteurs) — périmètre « hors dépôt »

**Mesuré** : 2026-10-07 · **Connecteurs interrogés** : Google Drive, Notion, Linear, Gmail
**But** : retrouver les documents de ressources / de suivi liés aux projets qui vivent hors du dépôt.

## 1. Google Drive — 13 fichiers examinés (requêtes : noms de projets, « audit », « chantier »)

| Fichier | Type | Date | Taille | Lien projet | Statut |
|---|---|---|---:|---|---|
| `Interface Cognitorium : Graphe Cognitif` | prompt Google AI Studio | 2026-07-31 | **68,5 Mo** | `proto-cognitorium` (origine AI Studio) | contenu non extractible (binaire > 25 Mo) |
| `Cognitarium City : Frontignan 2026` | prompt Google AI Studio | 2026-07-28 | **13,2 Mo** | `frontignan` (deck / atlas « Cognitarium City ») | contenu non extractible (binaire) |
| `Page de garde - suivi chantier.xls` | Excel | 2022-06-03 | — | racine — dossier de chantier | non lu (antérieur au monorepo) |
| `Les modèles d'horloge interne en psychologie du temps_Droit-Volet et Wearden.pdf` | PDF | 2018-06-15 | — | `ETAT-DE-LART-PSYCHOLOGIE` (sources amont) | référencé, non repris dans le dépôt |
| `protocole2enentier.pdf`, `7- QRGeneral Modifie nouveau protocole.pdf` | PDF | 2018-05-18 | — | sources amont (protocoles psy) | hors dépôt |
| `Auditory-attention-focusing-the-searchlight-_2007_…pdf` | PDF | 2018-06-15 | — | source psy citée par `HCSM`/`ETAT` | hors dépôt |
| 2 fichiers audio + 4 autres mp3 | audio | 2013–2022 | — | hors périmètre | n/a |

**Ce qui compte** : les **deux prompts AI Studio** sont les matrices de `proto-cognitorium` et de `frontignan`. Ils sont volumineux (68,5 + 13,2 Mo) et **n'existent que dans Drive** — ni sauvegarde, ni versionnage dans le dépôt. Les PDF psychologie (2018) sont des **sources amont non cartographiées** par les projets.

## 2. Notion — 0 document de projet

Recherche « Cognitorium » → 0 résultat. Espace Notion = pages de modèle (« Bienvenue », « Liste de tâches hebdomadaire », « Budget mensuel ») + bases « People/Revenus/Dépenses ». Aucun contenu projet → **les projets ne sont pas documentés dans Notion**. (Scopes/données perso non audités — hors périmètre.)

## 3. Linear — espace `cognitorium` créé le jour de l'audit, aucun suivi réel

- Teams : 1 — `Cognitorium` (clé `COG`), créée le 2026-10-07 12:05 UTC.
- Issues : 4, toutes générées par l'onboarding Linear (`COG-1` Get familiar with Linear → `COG-4` Set up your teams), 0 assignée, 0 projet, 0 cycle.
- Projets Linear : 0.

→ **Le suivi n'est pas encore amorcé** ; l'outil est prêt mais vide (aucune migration des tâches, qui restent dans `ROADMAP`s markdown).

## 4. Gmail — 3 messages pertinents (aucune pièce jointe projet)

| Message | Expéditeur | Date | Contenu utile |
|---|---|---|---|
| `Cognitorium est en ligne` | Polsia `<system@polsia.com>` | 2026-09-20 | **page d'accueil « Cognitorium » en ligne** (politique : « éclairer les territoires par la donnée, le terrain et le vécu ») ; service à **20 $/mois**, travail annoncé « en attente de démarrage » |
| `Une piste pour Cognitorium` | Polsia | 2026-10-01 | relance commerciale : cibler « équipes techniques » ou « élus » |
| `1 new project available to import` | Vercel | 2026-09-06 | projet Vercel à importer — non lié, ignoré |

→ Constat : il existe une **vitrine publique « Cognitorium » hébergée par Polsia** (≈ 20 $/mois, non mentionnée dans le dépôt ni dans la synthèse) et un appel à trancher la cible (technique/élus). À intégrer à la gouvernance et au budget.

## 5. Findings externes

| # | Sévérité | Catégorie | Constat | Preuve | Recommandation |
|---|---|---|---|---|---|
| F-EX-01 | moyen | C6 | 2 prompts AI Studio (85 Mo) matrices de `proto-cognitorium` et `frontignan` hors dépôt, sans sauvegarde ni lien | Drive IDs `1pipzTWd…`, `1Kh6KN20…` | exporter/archiver OU documenter le lien dans les README |
| F-EX-02 | moyen | C1 | vitrine Polsia « Cognitorium » (20 $/mois) absente du dépôt et de la synthèse | Gmail 2026-09-20 | décision : la garder, l'intégrer ou l'arrêter |
| F-EX-03 | faible | C7 | sources psychologie 2018 (Droit-Volet & Wearden, protocoles) hors dépôt, non citées par `HCSM`/`ETAT` | Drive | ajouter au registre de sources |
| F-EX-04 | info | C2 | espace Linear `cognitorium` créé, 0 tâche réelle ; suivi encore 100 % markdown | API Linear | migrer ou assumer |

## 6. Limites

- Drive : recherche par nom uniquement ; les prompts AI Studio (`application/vnd.google-makersuite.prompt`) ne sont pas extractibles en texte — seul le nom/la taille/la date sont exploitables.
- Gmail : recherche limitée aux 7 mots-clés du périmètre ; aucune pièce jointe rattachée aux projets.
- Notion/Linear : comptes quasi vides → conclusion « pas de matière projet », pas « rien à examiner ».
