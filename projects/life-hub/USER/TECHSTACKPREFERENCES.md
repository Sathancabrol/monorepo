---
provenance: interview-mined
last_updated: 2026-10-08
source: décisions de la session 07-08/10/2026 (docs/LIFE-HUB.md, SYSTEME-COMBINE-IA.md, UI-MOBIGLAS.md)
---

# Tech Stack Preferences

## Principes non négociables
1. **Git-first** : les données vivent en fichiers markdown versionnés, lisibles par toutes les IA.
2. **Local-first** : ce qui peut tourner chez moi tourne chez moi ; le cloud se justifie.
3. **Pas de lock-in** : formats ouverts, export toujours possible, pas d'abonnement captif.
4. **Licences** : copie dans le repo = MIT/Apache/BSD avec NOTICE ; AGPL = service seulement ; jamais de code sans licence claire.
5. **Un socle, pas une collection** : un système de référence + emprunts ciblés (leçon benchmark harness).

## Stack retenu
| Domaine | Choix |
|---|---|
| Portail/API | Python FastAPI (`app/`), Jinja |
| Données de vie | markdown + yaml + git (format USER/ LifeOS) |
| Socle système | LifeOS adopté (commit upstream figé, voir NOTICE) |
| Routeur IA | endpoint OpenAI-compatible unique (proxy mince ou LiteLLM déployé) |
| Modèles locaux | Ollama (sur le futur serveur) |
| Personas | format carte Tavern v2 en markdown |
| UI | PWA maison servie par `app/` — design `UI-MOBIGLAS.md` |
| Automatisation | hooks natifs d'abord, n8n seulement si besoin lourd |
| Tâches | git Issues/Work System ; Vikunja (CalDAV) seulement si synchro téléphone requise |

## Goûts d'interface
- Sombre, une seule couleur d'accent par contexte, grille partout.
- Règle des 2 secondes par écran ; chaque raccourci mérite sa place.
- Références : mobiGlas (Star Citizen), Dead Space (diégétique), LCARS (zones couleur), Her (voix d'abord).
