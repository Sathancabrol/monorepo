# Architecture de LAPLACE

## Rôle

`projects/laplace` est un module Python autonome qui fournit le bot Discord officiel **LAPLACE** et une frontière fournisseur réutilisable. Il fonctionne localement et ne dépend pas de l'interface FastAPI qui sert l'explorateur du monorepo.

```text
Discord application commands
          │ guild/channel allowlist
          ▼
LaplaceBot ──► LaplaceAgent ──► Fournisseur texte OpenAI-compatible
                    │                         ├─ Ollama local (défaut)
                    │                         └─ API compatible optionnelle
                    ├──► Fournisseur vision distinct (facultatif)
                    │     ├─ Ollama local (défaut)
                    │     └─ API compatible avec opt-in explicite
                    ▼
             SQLite local
             ├─ archives brutes par utilisateur
             ├─ souvenirs privés / partagés avec provenance
             ├─ historique des corrections
             └─ index plein texte FTS5
```

## Frontières de sécurité

- Slash commands seulement ; pas d'intent Message Content et pas d'écoute du texte ordinaire.
- Serveur autorisé obligatoire, salon facultatif ; commandes synchronisées au niveau des guilds explicitement autorisées.
- Les réponses sont éphémères par défaut. Les commandes de mémoire, d'historique, d'export et d'effacement sont toujours privées.
- L'historique est chargé avec l'ID de l'auteur uniquement ; aucune conversation d'un autre ID n'est incluse.
- Les souvenirs sont fournis comme contexte non fiable, jamais comme instructions d'outil.
- Aucun accès au shell, navigateur, fenêtres, souris, e-mail ou Carré d'As n'est implémenté. Seule l’image explicitement jointe à `/analyser_image` est lue pour cette requête, sans archivage.
- Les journaux n'enregistrent pas le texte utilisateur.

## Mémoire

1. **Archive** : append-only pendant la rétention choisie, par interaction Discord. On peut rechercher les originaux avec `/historique` et les exporter ; `/effacer_mes_donnees` est la suppression explicite.
2. **Souvenirs** : créés par `/retenir`, organisés en portée privée (par utilisateur) ou partagée (par ID de serveur), avec source, date et confiance. Les corrections sont versionnées et une mémoire partagée reste gérable uniquement depuis le serveur auquel elle appartient.
3. **Recherche** : FTS5 SQLite si disponible, sinon recherche `LIKE` locale. Elle n'est pas sémantique à ce stade.
4. **Aucun résumé destructif** : aucun compresseur ou résumé automatique n'est activé.

## Contrat du fournisseur

Le client `LLMClient` utilise le protocole Chat Completions compatible OpenAI. Le texte utilise Ollama local par défaut ; `/analyser_image` utilise un client vision séparé et facultatif, local par défaut. La requête image ponctuelle transmet seulement l'image et la question, pas l'historique ni les souvenirs. Un fournisseur vision externe est bloqué sans `ALLOW_EXTERNAL_VISION=true` et une configuration `VISION_*` distincte. Les capacités spécifiques à chaque API ne sont pas supposées. Une clé API n'est jamais exposée par `/statut`.

## Statut des intégrations

- **Discord texte** : implémenté, slash commands, allowlists, réponses privées.
- **Carré d'As** : objectif clarifié comme hub propriétaire d'agents, mais le code et le contrat d'API ne sont pas dans ce dépôt. Voir [Intégration Carré d'As](CARRE-DAS-INTEGRATION.md) et la [veille Agent Hub](../../../docs/AGENT-HUB-RESEARCH.md).
- **Profils d'expertise** : pas encore sélectionnables; future configuration versionnée avec sources, modèle, outils et tests.
- **Image jointe** : `/analyser_image` est disponible si `VISION_MODEL` est configuré; traitement éphémère et pas de mémoire/archivage.
- **Documents / audio / vidéo / caméra** : non implémentés; une photo/selfie devra d'abord être envoyée par l'utilisateur. Les flux vision, STT, TTS et vidéo doivent être séparés et bornés.
- **Contrôle du PC** : non implémenté; une future intégration devra être locale, réservée au propriétaire et demander confirmation pour chaque action sensible.

La conception vise un bot qui peut fonctionner dans Olympus sans rendre le monorepo ou l'application web dépendants de Discord ou d'Ollama. Voir [Fonctionnalités visées et critères d'acceptation](FEATURES.md).
