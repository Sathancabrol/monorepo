# 🔍 AUDIT COMPLET DES ACTIFS — « on a déjà ça ? » OUI.

> **Date** : 2026-10-08 · **Périmètre** : monorepo (9 repos fusionnés), GitHub, Notion, Linear, Drive, Gmail/Calendar/Docs.
> **Verdict** : le système n'est pas à construire de zéro — il est **déjà produit à ~70 %**, éparpillé. Le travail restant est de l'**assembler en offres**, pas de l'inventer.

---

## 1. 📦 L'inventaire (tout ce qui existe déjà)

### Monorepo / GitHub (9 repos, voir `data/github_inventory.json`)
| Actif | Ce que c'est | Maturité | Valeur |
|---|---|---|---|
| **app/** | Portail « fusion » : /repos, /monorepo, /api/fs, /preview — navigateur + preview de TOUS les repos | ✅ tourne | **coquille produit / UI** (le futur mobiGlas) |
| **reaserch-engine** | Moteur de recherche autonome : question → planning → evidence → claims → contradiction → synthèse → vérification | v0.1 testé | **l'usine** qui a produit tout le reste |
| **frontignan** | Rapport d'analyse territoriale Frontignan (249 sources, 13 fiches projets, 14 figures matplotlib) + vision 2026-2040 + **deck 18 slides autonome** | ✅ livrable pro | **produit fini** « intelligence territoriale » |
| **proto-cognitorium** | Dossier 337 fichiers : **271 fiches ROME France Travail** + Formacode + DDL SQLite 12 tables + ~12 générations de maquettes + UML | prototype avancé | **produit fini** « matching emploi/compétences » |
| **HCSM** | Human Cognitive State Model — cadre scientifique v0.1.1 (PROPOSED), spec Cognition Hub | cadre écrit | crédibilité méthodologique |
| **COGNITORIUM** | Écosystème + visuels | embryon | marque du produit |
| **watchtower** | Fork God's Eye View : globe 3D, CARTO/OSM, **commandes vocales FR**, HUD — mode gratuit sans clé | ✅ tourne | **couche carto/géo** des offres |
| **docs chantier (main)** | 220 fichiers marché construction + synthèse Talbot | archive | preuve du domaine BTP |
| **mail-organizer** | Tri/archivage sans suppression, 19 tests | ✅ expédié | preuve « opérateur IA » + micro-offre |
| **animation-chronos** | « Ferrofluid consciousness vessel » (TS/Vite) | démo | visuel de marque Cognitorium |
| **docs/** (monorepo) | 14 docs de décision (dont le présent audit) | ✅ | méthode documentée |

### Sites connectés
| Site | Contenu trouvé | Lecture |
|---|---|---|
| **Notion** | « Budget mensuel » + « Liste de tâches hebdo » (templates), DB Revenus/Dépenses (valeurs d'exemple), People | tentative d'orga perso d'août 2026 → **pont vers USER/** (budget réel = tableur, pas Notion) |
| **Drive** | **Le vrai gisement Cognitorium** : dossier « Polsia - Cognitorium et Mnéoterr », « Slack Cognitrum », prompts AI Studio (« Cognitarium City : Frontignan 2026 », « Interface Cognitorium : Graphe Cognitif », « Personal Cognitive Profile Design », « Conception Du Parcours D'Onboarding »), **OpenBCI Research Collection**, « Vision Pilot 1.2.mp4 », slides « Panorama des Types de Représentation », « Collaborer avec le futur - sources » | archive de production du produit — à référencer depuis PROJECTS |
| **Linear** | Vide | kanban disponible pour les offres / Outsider |
| **Gmail/Calendar/Docs** | Connectés ; tri + filtres actifs ; docs de méthode livrés | tuyauterie du Life Hub |

## 2. 🧵 Le fil que l'audit révèle : COGNITORIUM est LE produit

Ce que je croyais être des projets épars est **un seul produit à trois têtes** :

```
COGNITORIUM
├── HCSM            → le modèle (état cognitif humain, évidentiel, temporel)
├── proto-cognitorium → le moteur : 271 fiches ROME + Formacode + SQLite + maquettes
├── Cognitarium City  → l'application territoriale (Frontignan 2026)
├── OpenBCI           → la piste capteurs (mesure réelle)
├── Vision Pilot 1.2  → la démo vidéo
└── frontignan        → la preuve grandeur nature (analyse territoriale sourcée)
```

**Et il répond pile au moment** : Nathan est inscrit à France Travail ; le gisement de données est celui de France Travail (ROME/Formacode) ; les acheteurs potentiels (conseillers, missions locales, organismes de formation, cabinets de design urbain, agglos) sont **dans son voisinage immédiat (Sète/Thau)**.

## 3. 🎯 Les 3 offres assemblées à partir de l'existant

| # | Offre | Actifs déjà là (démonstration immédiate) | Premier client probable | Premier test (7 j, 0 €) |
|---|---|---|---|---|
| **O1 — Matching emploi/compétences** « Cognitorium Emploi » | proto-cognitorium (ROME+Formacode+DDL+maquettes), HCSM, parcours d'onboarding designé | **Son propre conseiller France Travail** (il est dedans), missions locales Sète/Thau | RDV conseiller avec la maquette + 1 page « ce que ça change pour l'accompagnement » |
| **O2 — Intelligence territoriale** | frontignan (rapport 249 sources + deck 18 slides + 14 figures), reaserch-engine, watchtower | L'équipe de design urbaine destinataire du rapport Frontignan (le rapport dit « destinataire : équipe de design de services »), agglo, cabinets d'urbanisme | Envoyer le deck existant tel quel à 3 destinataires réels |
| **O3 — IA pour chantiers BTP** | dossier chantier 220 fichiers, synthèse Talbot, méthode de tri | Réseau Sobeca, petites entreprises TP | 1 démo « dossier lu par l'IA » (le plan initial, toujours valable) |

**Socle commun** : app/ (vitrine), reaserch-engine (usine), méthode docs (crédibilité), UI-MOBIGLAS (habillage), Life Hub (organisation interne).

## 4. 🧭 Recommandation d'ordre

1. **O1 d'abord** : test gratuit via son propre conseiller FT, aligné avec sa situation (cumul ARE + activité), et le produit est le plus avancé techniquement (données + DDL + maquettes).
2. **O2 en parallèle** : le deck existe déjà — l'envoyer ne coûte rien et Frontignan est à 7 km de chez lui.
3. **O3 en réserve** : plancher BTP si O1/O2 ne donnent rien à J+30.
4. **Ne RIEN reconstruire** : chaque offre part d'un artefact existant ; si un test demande du code neuf, c'est un signal de mauvaise offre.

## 5. ⚙️ Mises à jour faites dans la foulée
- `USER/PROJECTS.md` : Cognitorium reconnu comme produit n°1 ; Notion/Drive/Linear cartographiés.
- `USER/TELOS/MISSION.md` : pistes A reclassées O1/O2/O3 avec les actifs réels.
- `USER/TELOS/CURRENT_STATE/CREATIVE.md` : le fil Cognitorium documenté.

---
*Source de l'audit : lecture directe du monorepo (README, inventaire github), Notion search, Linear projects, Drive list (40 fichiers) — 08/10/2026.*
