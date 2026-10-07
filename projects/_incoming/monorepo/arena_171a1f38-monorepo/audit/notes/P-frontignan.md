# P — `frontignan`

**Audit** : fait (2026-10-07) · **Risque global** : moyen · **Maturité** : M2 `prototype` (livrable éditorial complet, pas un logiciel)
**Résumé** : dossier d'analyse territoriale de Frontignan la Peyrade (Hérault) + vision 2026-2040 : rapport 826 lignes, deck 18 slides autonome, 14 figures, 4 générateurs Python. **Projet local uniquement — pas de dépôt GitHub.**

## C1 — Identité & provenance

| Fait | Valeur | Preuve |
|---|---|---|
| Dépôt GitHub | **aucun** (`gh repo list` : 9 dépôts, pas de `frontignan`) | `gh repo list` |
| Mode d'existence | dossiers local `projects/frontignan/` committé dans `monorepo` (PR #1, 2026-09-08) | `git log`, PR #1 |
| Licence | aucune | `find` |
| Date du contenu | septembre 2026 (analyse), archive 2026-10-07 | `README.md` |

## C2 — Dépôt, branches & synchronisation

- **Aucun dépôt dédié** → pas de branches, pas de PR, pas d'historique propre : le suivi est celui de `monorepo`.
- Travail complémentaire **non fusionné** sur une branche du monorepo : `arena/01a08203-monorepo` (+1 commit) — **atlas interactif** : graphe Obsidian, carte heuristique, slides, 22 fichiers (`projects/frontignan/atlas/`).

## C3 — Structure & volumétrie

| Mesure | Valeur |
|---|---|
| Fichiers / taille | 28 / 13.6 Mo |
| LOC-code / données-doc | 3 764 / 635 |
| Livrables | `index.html` (deck 18 slides autonome), `rapport-frontignan-analyse-territoriale.md` (**826 lignes**, 249 sources citées), `vision-frontignan-2026-2040.md` (179 lignes) + versions HTML |
| Figures | 14 PNG matplotlib (`figures/`) + 2 illustrations (`visuals/`) |
| Générateurs | 4 scripts Python (`make_figures.py`, `make_figures_vision.py`, `make_html.py`, `make_deck.py`) |

## C4 — Stack & dépendances

- Python 3 + **matplotlib** + numpy (génération) ; HTML/CSS/JS pur pour le deck (aucune librairie front).
- Dépendances non déclarées (pas de `requirements.txt`).

## C5 — Fonctionnalités & modules

- Analyse : entonnoir France→ville, 11 sections, 13 fiches projets, parties prenantes, mobilités, SWOT, priorisation.
- Prospective : trajectoire 2026-2040, focale 2030 (5 conditions de succès), 3 scénarios 2040, schéma territorial.
- Deck autonome (images base64, navigation clavier, export PDF paysage via Ctrl+P).

## C6 — Données & ressources

- 16 figures + visuels (≈ 12 Mo d'images) ; sources croisées et datées (balises ✅ engagé / 📅 annoncé / 🔮 tendance / ⚠️ incertain).

## C7 — Documentation & références

- `README.md` complet (contenu, points clés, régénération) ; rapport avec **249 sources** listées ; méthode explicite (estimations propres distinguées des prévisions officielles).
- **La documentation la plus rigoureuse du monorepo côté « sources »**, alignée sur l'esprit de la synthèse Talbot (statut par affirmation).

## C8 — Tests & qualité

- **0 test**, 0 CI ; les scripts génèrent les figures de façon déterministe (non vérifié dans cette session — matplotlib non installé).

## C9 — Sécurité & secrets

- Aucun secret. Aucune donnée personnelle (données publiques, acteurs institutionnels nommés).

## C10 — Exécution & déploiement

- Consultable sans serveur : `index.html` (deck), `rapport-…html`, `vision-…html` ; preview monorepo `/preview/frontignan/` (détecté par `detect_preview_entry` via `index.html`).
- Régénération : `python scripts/make_figures.py` etc. (matplotlib requis).

## C11 — Dette technique & risques

1. **Copie unique** : pas de dépôt distant → si le monorepo est perdu/altéré, le dossier l'est aussi (pas d'historique de conception hors `monorepo`).
2. Doublons de format assumés (MD + HTML + deck) = 3 rendus à maintenir.
3. 12 Mo d'images dans Git.
4. L'atlas interactif (branche `01a08203`) n'est pas intégré.

## C12 — Maturité & complétude

**M2 `prototype`** au sens logiciel — mais **livrable éditorial terminé** (le README va jusqu'à la régénération documentée).
**Prochaine étape** : publier un dépôt dédié (ou acter le statut « local »), intégrer l'atlas de la branche.

## Findings

| # | Sévérité | Catégorie | Constat | Preuve | Recommandation |
|---|---|---|---|---|---|
| F-FR-01 | moyen | C1 | aucun dépôt GitHub dédié (copie unique) | `gh repo list` | publier ou documenter comme livrable local |
| F-FR-02 | moyen | C2 | atlas interactif non fusionné (`arena/01a08203`: 22 fichiers) | `branches.json` | fusionner l'atlas |
| F-FR-03 | faible | C4 | dépendances Python non déclarées | `scripts/` | `requirements.txt` |
| F-FR-04 | info | C6 | 12 Mo d'images versionnées | inventaire | compresser |
