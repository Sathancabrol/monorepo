# Ajouter LAPLACE à Olympus

Ce guide crée un **bot Discord officiel** nommé LAPLACE. N'utilise pas un self-bot ou un compte utilisateur automatisé. Le code de ce module n'accède qu'aux commandes d'application ; il n'écoute pas les messages ordinaires.

## 1. Créer le bot

1. Ouvre le [Discord Developer Portal](https://discord.com/developers/applications) et crée une application appelée `LAPLACE`.
2. Dans **Bot**, ajoute l'utilisateur bot si Discord le demande, puis copie son token une seule fois vers le fichier local `projects/laplace/.env`. Ne le poste pas dans Discord, GitHub ou cette conversation.
3. Laisse désactivés les intents privilégiés **Message Content** et **Server Members**. Le bot utilise `discord.Intents.none()` avec l'intent `guilds` uniquement.
4. Dans **OAuth2 → URL Generator**, coche les scopes `bot` et `applications.commands`.
5. Accorde le minimum utile dans Olympus : `View Channels`, `Send Messages`, `Attach Files` (pour l'export JSON) et `Use Application Commands`. Il n'a pas besoin de `Read Message History`, de l'intent Message Content, du rôle Administrateur ni d'un accès au shell/PC.
6. Ouvre le lien généré, sélectionne Olympus et ajoute LAPLACE au serveur. Limite ensuite son rôle au salon de test si tu veux un déploiement progressif.

Sources Discord : [OAuth2](https://discord.com/developers/docs/topics/oauth2), [application commands](https://discord.com/developers/docs/interactions/application-commands), [Gateway intents](https://discord.com/developers/docs/events/gateway#gateway-intents).

## 2. Copier les IDs Discord

Dans Discord, active **Paramètres utilisateur → Avancé → Mode développeur**. Clic droit sur le serveur Olympus, sur ton profil et éventuellement sur le salon de test, puis **Copier l'identifiant**.

Crée `.env` depuis `.env.example` et renseigne localement :

```dotenv
DISCORD_BOT_TOKEN=...             # secret du bot, local uniquement
ALLOWED_GUILD_IDS=...              # ID numérique d'Olympus, obligatoire
ALLOWED_CHANNEL_IDS=...            # ID(s) de salon test, conseillé
OWNER_USER_IDS=...                 # ton ID Discord, obligatoire
```

`ALLOWED_GUILD_IDS` est obligatoire : les commandes sont synchronisées uniquement dans les serveurs listés. Si `ALLOWED_CHANNEL_IDS` est vide, elles peuvent être utilisées dans tous les salons du serveur autorisé. Ne donne jamais le rôle Administrateur au bot.

## 3. Démarrer le modèle local (Ollama)

Installe Ollama sur la machine qui fera tourner le bot, choisis un modèle compatible avec le matériel, puis vérifie son nom avec `ollama list`. Configure ce nom dans `LLM_MODEL`. Si aucun modèle n'est installé, choisis d'abord un modèle adapté à la mémoire et au GPU disponibles ; ce dépôt ne suppose pas ton matériel.

Par défaut, LAPLACE utilise le point d'accès local compatible OpenAI d'Ollama : `http://127.0.0.1:11434/v1`. La valeur `LLM_API_KEY=ollama` est un marqueur local, pas une vraie clé.

Une API externe peut aussi être configurée avec `LLM_PROVIDER=openai_compatible`, son URL et une clé conservée dans `.env`. L'utilisation d'une API externe transmet les requêtes et le contexte envoyé par LAPLACE à ce fournisseur et peut être facturée ; vérifie sa politique de conservation.

## 4. Installer et lancer

Depuis la racine du dépôt :

```bash
cd projects/laplace
python -m venv .venv
# Windows PowerShell : .venv\Scripts\Activate.ps1
# macOS / Linux : source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
```

Copie `.env.example` vers `.env`, complète les champs requis, puis lance :

```bash
python -m laplace
```

Le processus se connecte à Discord par une connexion sortante ; aucun port public n'est à ouvrir. Si le PC s'éteint ou si le processus s'arrête, le bot ne répond plus. Au démarrage, les commandes sont publiées pour les seuls serveurs autorisés. Une fois le bot connecté, utilise `/statut`, puis `/aide` dans Olympus.

## Commandes disponibles

| Commande | Effet | Accès et confidentialité |
|---|---|---|
| `/parler question` | Conversation avec LAPLACE, avec contexte récent et souvenirs pertinents | Réponse privée par défaut ; archive selon la durée configurée |
| `/analyser_image image question` | Analyse une image sélectionnée par la personne | Résultat éphémère; JPEG/PNG/WebP, 8 Mio max; aucun archivage; `VISION_MODEL` requis |
| `/retenir contenu portee` | Ajoute un souvenir privé ou partagé, avec confiance et URL source facultative | Les souvenirs partagés sont réservés aux propriétaires configurés |
| `/souvenirs recherche` | Liste ou recherche les souvenirs de l'utilisateur et ceux partagés dans ce serveur | Réponse privée |
| `/corriger identifiant nouveau_contenu` | Corrige un souvenir et conserve l'historique de révision | Le propriétaire du souvenir, ou un propriétaire LAPLACE pour les souvenirs partagés |
| `/oublier identifiant` | Supprime un souvenir et ses révisions | Même contrôle d'accès que `/corriger` |
| `/historique recherche` | Recherche dans l'archive brute personnelle | Réponse privée ; ne consulte jamais l'historique d'un autre utilisateur |
| `/exporter_mes_donnees` | Télécharge un JSON de ses souvenirs, révisions et archive | Réponse et fichier privés |
| `/effacer_mes_donnees confirmer` | Efface ses souvenirs privés et ses conversations archivées | Demande `confirmer: true`; les souvenirs partagés sont préservés |
| `/statut` | Affiche fournisseur, modèle et réglages non secrets | Réponse privée |
| `/aide` | Affiche l'aide intégrée | Réponse privée |

Pour les commandes de mémoire, choisis explicitement la portée privée ou partagée. Une mémoire personnelle est filtrée par ID Discord, pas par nom affiché. Une URL source facultative doit être en HTTPS.

## Paramètres utiles

- `PRIVATE_RESPONSES=true` (défaut) : réponses privées, même si la commande est lancée dans un salon public. Mettre `false` seulement dans un salon destiné aux réponses publiques.
- `ARCHIVE_RETENTION_DAYS=30` : durée de conservation des demandes/réponses brutes ; les entrées expirées sont purgées au démarrage, toutes les heures et avant une consultation. `0` désactive les nouvelles archives et purge l'archive existante au démarrage et toutes les heures ; les souvenirs explicites restent distincts.
- `MAX_HISTORY_TURNS=6` : nombre maximal d'échanges récents du même utilisateur transmis au modèle.
- `MEMORY_TOP_K=5` : souvenirs textuels pertinents transmis au modèle. La recherche actuelle est plein texte SQLite FTS5, avec repli `LIKE` ; la recherche sémantique par embeddings reste à ajouter.
- `VISION_MODEL=` vide par défaut : ajoute le nom d’un modèle local installé avec vision pour activer `/analyser_image`. Par défaut le fournisseur vision est Ollama (`VISION_PROVIDER=ollama`).
- Une vision externe exige `VISION_PROVIDER=openai_compatible`, `VISION_BASE_URL`, `VISION_API_KEY` et `ALLOW_EXTERNAL_VISION=true`. Cette autorisation est séparée du fournisseur de texte; une image envoyée partira au fournisseur indiqué.

Pour les données et les limites de la version, voir [Confidentialité](PRIVACY.md), [Architecture](ARCHITECTURE.md) et [Feuille de route](ROADMAP.md).
