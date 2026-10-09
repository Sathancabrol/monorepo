# Mission M-001 — Directeur du Registre (rattachement PRODUCTION)
- statut : gate
- demandeur : Nathan
- créé le : 2026-10-09

## 1. OUTCOME
Le portail `app/` a un design modernisé et une page qui expose les données réelles du système (services, tâches, journal) — en lecture seule.

## 2. HOW
Lire `app/main.py` + `app/templates/` → proposer la nouvelle interface → éditer les templates/CSS → relancer la preview → vérifier.

## 3. TOUCH
- Modifiable : `app/templates/`, `app/static/` (s'il existe), `app/main.py` (routes de lecture uniquement).
- Interdit : toute suppression, toute écriture hors `app/`, toute donnée inventée affichée.

## 4. HUMAN-CHECK
Preview visible par Nathan + validation visuelle ; « montre sans stocker » (la page lit les fichiers, ne stocke rien).

## Journal
- 2026-10-09 : création (brouillon, en attente de feu vert).
- 2026-10-09 : feu vert Nathan → exécution. Routes lecture seule `/office` + `/api/office/state` dans `app/main.py`, template `office.html`, `office.css`, nav+accueil mis à jour. Vérifié : HTTP 200, budget réel −111,51 €, 12 services, 13 tâches, 2 missions, 7 signaux affichés. La page n'écrit rien (« montre sans stocker »). → statut gate : validation visuelle de Nathan requise.
