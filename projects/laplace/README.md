# LAPLACE — agent Discord officiel

**Statut :** MVP autonome centré texte, avec analyse d’image locale facultative; à configurer par le propriétaire.

**Cible :** serveur Discord Olympus ; le bot n'est pas encore invité ni connecté à un modèle dans ce dépôt.

LAPLACE est le bot conversationnel de l'application. Ce module est volontairement indépendant du reste du monorepo : il peut utiliser Ollama sur le PC, un fournisseur compatible OpenAI par API, ou être adapté à l'application quand son code et son contrat d'intégration seront disponibles.

> Le dépôt ne contient pas Carré d'As. La connexion native à cette application est donc documentée comme bloquée, et non simulée. Voir [l'état de l'intégration](docs/CARRE-DAS-INTEGRATION.md).

## Fonctionnalités de cette version

| Fonction | État | Détails |
|---|---|---|
| Bot Discord officiel + commandes slash | ✅ | Guilds/salons autorisés ; pas de self-bot ; aucun Message Content Intent |
| Conversation texte | ✅ | Ollama local par défaut ; fournisseur OpenAI-compatible optionnel |
| Mémoire personnelle | ✅ | Séparée par ID Discord ; création explicite, correction versionnée, suppression |
| Mémoire partagée | ✅ | Opt-in, isolée par serveur ; écriture réservée aux propriétaires configurés |
| Archive brute | ✅ | Conversations `/parler`, rétention configurée, recherche, export, oubli |
| Provenance | ✅ | Date, utilisateur, interaction source, URL HTTPS facultative, confiance |
| Recherche | ✅ | SQLite FTS5 avec repli plein texte `LIKE` ; **pas encore sémantique** |
| Réponses privées | ✅ | Éphémères par défaut ; commandes de mémoire toujours privées |
| Profils d’expertise | ⏳ | Profil général d’abord; profils versionnés et publiés par le propriétaire ensuite |
| Analyse d’image jointe | ✅* | `/analyser_image`; modèle vision configuré localement; analyse privée sans archivage (`*` nécessite `VISION_MODEL`) |
| Audio/vidéo et génération multimédia | ⏳ | Pas encore implémentés; modèles locaux d’abord et API externe par capacité sur opt-in |
| Voix | ⏳ | STT/TTS et conversation en salon vocal à concevoir séparément |
| Caméra selfie | ⏳ | L’utilisateur pourra d’abord envoyer une photo; capture locale par compagnon seulement avec autorisation |
| Contrôle fenêtres/onglets/PC | ⏳ | Aucun outil local n'est activé |
| Intégration native Carré d'As | ⏸️ | Nécessite son dépôt, son API officielle ou son contrat d'agent |

## Prérequis

- Python 3.11 ou ultérieur.
- Une application bot créée dans le [Discord Developer Portal](https://discord.com/developers/applications).
- Un ID de serveur Olympus et un ID utilisateur propriétaire.
- Ollama et un modèle adapté au PC **ou** les paramètres d'un fournisseur API compatible.
- La machine qui exécute le bot doit rester allumée pour qu'il réponde.

## Installation rapide

Le guide détaillé pour inviter le bot, limiter ses permissions et configurer son modèle est dans [docs/DISCORD_SETUP.md](docs/DISCORD_SETUP.md).

```bash
cd projects/laplace
python -m venv .venv
# Windows PowerShell : .venv\Scripts\Activate.ps1
# macOS / Linux : source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
cp .env.example .env       # Windows : Copy-Item .env.example .env
```

Renseigne `.env` localement. Les valeurs `DISCORD_BOT_TOKEN`, `ALLOWED_GUILD_IDS`, `OWNER_USER_IDS` et `LLM_MODEL` sont requises. Pour Ollama, choisis `LLM_MODEL` parmi les modèles installés (`ollama list`). **Ne partage jamais `.env`, token ou clé API.**

```bash
python -m laplace
```

Dans le serveur configuré, teste `/statut`, puis `/aide` et `/parler`. Pour `/analyser_image`, configure aussi un modèle vision local dans `VISION_MODEL`. Le bot synchronise les commandes uniquement avec les guilds de `ALLOWED_GUILD_IDS`.

## Commandes Discord

- `/parler question` : conversation avec LAPLACE.
- `/analyser_image image question` : analyser une image envoyée (JPEG/PNG/WebP, 8 Mio max); privé et non mémorisé, nécessite `VISION_MODEL`.
- `/retenir contenu portee` : crée un souvenir privé ou partagé ; la portée doit être choisie explicitement. La confiance est facultative (0–1), et une URL HTTPS peut être jointe.
- `/souvenirs recherche` : consulter ses souvenirs privés et les souvenirs partagés du serveur courant.
- `/corriger identifiant nouveau_contenu` : corriger un souvenir tout en gardant l'historique des versions.
- `/oublier identifiant` : supprimer un souvenir autorisé.
- `/historique recherche` : recherche uniquement dans l'archive de l'utilisateur.
- `/exporter_mes_donnees` : export JSON éphémère.
- `/effacer_mes_donnees confirmer` : effacer les souvenirs privés, révisions et archives de l'utilisateur ; le booléen doit être `true`.
- `/statut` et `/aide` : état non sensible et documentation intégrée.

Les réponses `/parler` sont éphémères par défaut. Pour une conversation publique, régler `PRIVATE_RESPONSES=false` uniquement dans un salon prévu à cet effet.

## Configuration fournisseur

### Ollama local (défaut)

```dotenv
LLM_PROVIDER=ollama
LLM_BASE_URL=http://127.0.0.1:11434/v1
LLM_API_KEY=ollama
LLM_MODEL=nom-dun-modele-installe
```

### Analyse d’image locale (facultative)

Pour activer `/analyser_image`, installe dans Ollama un modèle qui accepte des images, puis renseigne son nom :

```dotenv
VISION_PROVIDER=ollama
VISION_BASE_URL=http://127.0.0.1:11434/v1
VISION_API_KEY=ollama
VISION_MODEL=nom-du-modele-vision-installe
ALLOW_EXTERNAL_VISION=false
```

Le nom dépend des modèles réellement présents (`ollama list`). Aucune analyse n’est faite si `VISION_MODEL` est vide. Pour envoyer des images à une API externe, renseigne séparément `VISION_PROVIDER=openai_compatible`, `VISION_BASE_URL` et `VISION_API_KEY`, puis active explicitement `ALLOW_EXTERNAL_VISION=true`; l’image quitte alors ton PC.

### API compatible OpenAI (facultatif)

```dotenv
LLM_PROVIDER=openai_compatible
LLM_BASE_URL=https://api.example.invalid/v1
LLM_API_KEY=secret-local-a-ne-pas-partager
LLM_MODEL=nom-du-modele
```

Ne mets pas d'identifiants dans l'URL. Une API externe peut facturer l'usage et reçoit le contexte transmis ; consulte [Confidentialité](docs/PRIVACY.md). L'abonnement ChatGPT et la facturation API sont distincts.

## Documentation et développement

- [Installation et invitation Discord](docs/DISCORD_SETUP.md)
- [Architecture et frontières d'accès](docs/ARCHITECTURE.md)
- [Confidentialité, export et suppression](docs/PRIVACY.md)
- [Carré d'As : état de l'intégration](docs/CARRE-DAS-INTEGRATION.md)
- [Fonctionnalités visées, état et critères d’acceptation](docs/FEATURES.md)
- [Feuille de route](docs/ROADMAP.md)
- [Sources techniques](docs/SOURCES.md)
- [Recherche modèles vision, caméra et IRMf — veille non intégrée](docs/RECHERCHE-MODELES-VISION-IRMf.md)

Lancer les tests :

```bash
python -m pytest
```

Lancer le lint :

```bash
ruff check .
```

Les choix fonctionnels sont précisés dans [Fonctionnalités visées](docs/FEATURES.md); le choix des modèles dépend encore de l'OS, de la RAM/VRAM et de `ollama list`. L’analyse d’image jointe est disponible seulement après configuration d’un modèle vision; voix, capture caméra locale, audio/vidéo et outils PC restent à développer.
