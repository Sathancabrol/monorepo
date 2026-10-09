# Mission M-001 — Directeur du Registre (rattachement PRODUCTION)
- statut : brouillon
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
