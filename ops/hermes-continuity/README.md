# Hermes / Chronos — autonomie et relais entre modèles

Ce dossier est un **point de reprise versionné** pour les agents Hermes. Il ne contient **aucun secret** et ne remplace pas la configuration locale Windows.

## Mission
Obtenir une exécution continue sans ChatGPT obligatoire : OpenRouter gratuit tant que disponible, Google Gemini si sa clé et son quota fonctionnent, puis modèle local Ollama. Les profils Hermes `default`, `cronos` et `cronoslocal` doivent rester isolés.

## Vérifications minimales
1. `hermes --version`, `hermes profile list`, `hermes gateway status`, `hermes -p cronos doctor`
2. `ollama list` et `ollama ps` ; distinguer le contexte effectivement chargé du contexte annoncé par Hermes.
3. `hermes -p cronos fallback check` puis `hermes -p cronos fallback check --live` (si la version installée supporte la commande).
4. Nouvelle session Hermes dans le bon répertoire de projet ; faire exécuter une lecture réelle de fichier, puis une tâche de code élémentaire avec test.
5. Contrôler la session et le profil réellement routés sur Discord/Telegram ; répéter les tests avec les crons et sous-agents (leur politique de fallback peut être distincte).

## Exemple de configuration (à ajuster aux modèles réellement installés)
```yaml
fallback_providers:
  - provider: gemini
    model: gemini-3.8-flash
  - provider: custom
    model: qwen3:4b-hermes64k
    base_url: http://127.0.0.1:11434/v1
    api_mode: chat_completions
```
Le modèle local est uniquement un fallback si Ollama répond et émet de vrais `tool_calls`. Une réponse texte n'est pas une preuve de compatibilité agentique. Sauvegarder `config.yaml` avant toute édition ; ne jamais publier `.env` ni `auth.json`.

## Limites opérationnelles
- La bascule Hermes préserve l'historique **à l'intérieur d'une même session Hermes**, mais n'importe pas les anciennes conversations ChatGPT.
- Les profils ont une mémoire séparée. Les instructions de projet doivent être relues dans `AGENTS.md` et `STATE.md`.
- Un gateway actif n'établit pas qu'un modèle, outil, cron ou nœud Android fonctionne.
- Les petits modèles locaux peuvent être utiles en secours mais ne doivent pas piloter seuls des modifications critiques sans tests.

## Sources
- https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers
- https://hermes-agent.nousresearch.com/docs/user-guide/profiles
- https://hermes-agent.nousresearch.com/docs/user-guide/windows-native
- https://hermes-agent.nousresearch.com/docs/user-guide/which-file-does-what
