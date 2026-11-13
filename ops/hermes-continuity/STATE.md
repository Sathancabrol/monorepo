# Hermes / Chronos — état observé le 14 novembre 2026

Source : sortie PowerShell communiquée par l'utilisateur (pas d'accès direct à Windows).

| Composant | Observation | Verdict |
| --- | --- | --- |
| Hermes | v0.23.1+4388.g415fa33 ; git ; Python 3.14.9 ; OpenAI SDK 2.54.0 ; 3 commits derrière upstream | Démarre ; pas de mise à jour automatique |
| Gateway Windows | Hermes_Gateway enregistrée et active, PID 1940 | Service OK selon dernier diagnostic |
| Profil default | primaire qwen3:4b | Inférence et outil non testés |
| Profil cronos | primaire gpt-6.1-sol ; fallback 1 openrouter/nvidia/nemotron-3.5-lightning ; fallback 2 custom/qwen3:1.7b | Contrôle statique OK, contrôle live à effectuer |
| Profil cronoslocal | primaire qwen3:4b-hermes64k ; aucune entrée fallback | Pas de relais secondaire |
| Ollama | 7 modèles installés (Qwen 1.7/4B et dérivés Chronos) ; ollama ps vide | Aucun modèle chargé pendant le test, pas une erreur en soi |
| VoiceStudio MCP | http://127.0.0.1:3900/mcp/ actif | Test d'appel d'outil à compléter |
| OpenAdapt MCP | désactivé ; uvx absent du PATH ; handshake timeout après 30 s | Installer uv avec winget, vérifier Python 3.12 puis retester |

## Commandes de validation non destructives

```powershell
hermes -p cronos fallback check --live
Invoke-RestMethod http://127.0.0.1:11434/api/tags | Select-Object -ExpandProperty models | Select-Object name
hermes -p cronoslocal fallback list
hermes -p default fallback list
hermes -p cronos doctor
hermes cron list
```

## Correctifs différés en attendant les tests

1. Conserver les configs existantes, ne pas appeler `hermes fallback clear`.
2. Si Ollama 4B produit de vrais tool_calls, privilégier `qwen3:4b-hermes64k` comme dernier secours de `cronos` plutôt que 1.7B pour les tâches agentiques longues. Vérifier ressources et contextes utilisés.
3. Si la chaîne n'a pas de modèle gratuit en ligne opérationnel, ajouter un Gemini validé avec `hermes -p cronos fallback add` (après vérification des quotas).
4. Tester `cronoslocal` avec un autre modèle local en relais ; ne pas le dupliquer avec son primaire.
5. Contrôler que cron et délégation ne sont pas épinglés à des fournisseurs non repliables (les jobs pinned n'héritent pas du fallback).
6. Si OpenAdapt est nécessaire, installer `uv` via `winget install --id astral-sh.uv -e`, démarrer une nouvelle console et vérifier `uvx --python 3.12 openadapt-agent --help`. Reconfigurer l'entrée MCP uniquement après test.

## Critère de reprise

Appel réel sur modèle primaire puis secours, test d'appel d'outil réel, session Hermes reprise dans le même profil, exécution de tâche vérifiée, mise à jour du journal. Aucune de ces validations n'est encore attestée.
