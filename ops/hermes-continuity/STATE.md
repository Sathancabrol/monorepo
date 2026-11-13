# État de la reprise Hermes

Dernière mise à jour : 2026-11-14 (état documentaire non validé sur la machine).

| Élément | État / preuve |
| --- | --- |
| Gateway Windows | Ancien diagnostic : actif ; revalidation requise |
| OpenRouter gratuit | 429 auparavant ; quotas à revalider |
| Gemini `gemini-3.8-flash` | Test antérieur positif ; fallback non validé |
| Ollama Qwen3 4B | Serveur antérieurement OK ; tool_calls non validés |
| Redmi / Samsung via Termux | Serveurs locaux antérieurement OK ; routage Hermes non validé |
| Profils / sessions | `default`, `cronos`, `cronoslocal` ; isolation confirmée par conception Hermes |
| Test d'une vraie tâche autonome | NON EFFECTUÉ |

## À renseigner après chaque intervention
- Date, modèle réellement utilisé, profil, URL d'inférence masquée si sensible.
- Objectif précis.
- Fichiers modifiés et sauvegardes.
- Commandes et tests, avec résultats OK/KO.
- Blocages et prochaine opération autonome (une seule, explicite).
- Validation de la reprise sur Discord/Telegram ou cron, si concerné.

**Aucun correctif local n'a été exécuté par la création de ce dossier GitHub.**
