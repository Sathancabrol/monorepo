# Inventaire Hermes / Chronos des moteurs IA — 2026-11-14

Ce tableau est construit à partir des diagnostics communiqués dans nos conversations. **Ne remplace pas un test en direct sur Windows**. Aucun secret enregistré.

## A. Tags Ollama installés — vérifiés par `ollama list` le 14 novembre 2026

| Modèle | Profil cible |
| --- | --- |
| `qwen3:4b` | `llm-qwen4b` |
| `qwen3:4b-hermes64k` | `llm-qwen4b64k` |
| `qwen3:1.7b` | `llm-qwen17b` |
| `qwen3:1.7b-hermes64k` | `llm-qwen17b64k` |
| `chronos-local-direct:latest` | `llm-direct` |
| `chronos-fast:latest` | `llm-fast` |
| `chronos-nothink:latest` | `llm-nothink` |

Sept tags installés, non nécessairement sept poids distincts. `ollama ps` vide au moment de la vérification.

## B. Modèles / artefacts hors Ollama — statut à revérifier

| Artefact | Moteur / site | Type | Profil ? | Preuve |
| --- | --- | --- | --- | --- |
| `google_gemma-4-E4B-it-Q4_K_M` | llama.cpp, tour | LLM | Oui si présent | ancien diagnostic 7/11 |
| `nomic-embed-text-v1.5.Q8_0` | tour | embedding | Non : service mémoire / index | ancien diagnostic 7/11 |
| `qwen05.gguf` | Samsung A17, Termux | LLM | Oui après test réseau | ancien test |
| `qwen35.gguf` | Samsung A17, Termux | LLM | Oui après test réseau | ancien test |
| `qwen08.gguf` | Redmi Note 13, Termux | LLM | Oui après test réseau | ancien test |
| Parakeet TDT 0.6B v3 int8 | VoiceStudio, Sherpa-ONNX, port 3900 | ASR / STT | Non : MCP `voicestudio` | VoiceStudio ancien diagnostic ; MCP activé 14/11 |

## C. Modèles en ligne et fournisseurs — ne pas confondre configuration et disponibilité

| Fournisseur / modèle | État connu | Profil candidat |
| --- | --- | --- |
| `gpt-6.1-sol` | Modèle primaire annoncé par profil `cronos` le 14/11 ; appel vivant non prouvé | `llm-gpt` |
| OpenRouter `nvidia/nemotron-3.5-lightning` | Fallback `cronos` ready **static**, requête réelle non testée | `llm-nemotron` |
| Google Gemini `gemini-3.8-flash` | Ancien essai positif ; quotas/auth à revalider | `llm-gemini` |
| Nous Portal | Authentifié précédemment, crédit/accès non établis | profil à décider après catalogue |
| OpenAI Codex | Authentifié précédemment ; ne pas supposer qu'un modèle distinct est utilisable | pas de profil additionnel sans preuve |
| OmniRoute | Chaîne de routage instable / erreurs précédentes | pas de profil tant que non réparé |
| GLM 5.3, Kimi K3, DeepSeek V4.1 FlashCloud, Gemma 4 31B Cloud, Qwen 34B | Noms rapportés anciennement ; pas confirmés installés ni accessibles | **non comptabilisés** |

## D. Autres outils, **pas des LLM**

- `voicestudio` : MCP actif `http://127.0.0.1:3900/mcp/` ; transcription Parakeet.
- `openadapt` : MCP désactivé ; `uvx` absent du PATH, timeout.
- Modules Vision Lab / X-Ray Mirror (détection visage/corps/mains/objets, etc.) : moteurs de perception ; pas de profil LLM par module.
- Services d'embeddings comme Nomic : à exposer pour RAG/recherche, pas comme interlocuteur.
- Discord, Telegram, PC portable : canaux ou nœuds, pas automatiquement un modèle distinct.

## E. Diagnostic de recensement en lecture seule

```powershell
hermes --version
hermes profile list
hermes mcp list
ollama list
ollama ps
Invoke-RestMethod 'http://127.0.0.1:11434/api/tags' |
    Select-Object -ExpandProperty models | Select-Object name
# Chercher les modèles GGUF dans les emplacements usuels.
# Attention, les parcours récursifs peuvent prendre du temps selon la taille de ces dossiers.
@("$env:USERPROFILE\Downloads", "$env:USERPROFILE\Documents") |
    Where-Object { Test-Path $_ } |
    ForEach-Object { Get-ChildItem $_ -Recurse -File -Filter '*.gguf' -ErrorAction SilentlyContinue } |
    Select-Object FullName, Length
```

Ne jamais copier les clés API, `.env`, ou `auth.json` dans un journal partagé. Les modèles des téléphones doivent être testés par l'accès réellement exposé au PC, sans supposer que leur adresse Termux `127.0.0.1` est atteignable depuis Windows.

## Principe d'architecture

- **Un profil par modèle réellement exploitable** pour l'inventaire et les tests de capacités.
- **Un orchestrateur `cronos`** pour l'attribution des tâches, la continuité et le suivi.
- **Des MCP/outils transversaux** pour VoiceStudio, vision, navigateur, GitHub, etc.
- **Un fallback par profil critique** : profil et bascule de fournisseur sont deux mécanismes distincts.
- Ne pas charger tous les poids simultanément sur la GTX 1060/16 Go ; faire un routage selon disponibilité.
