# Données, mémoire et confidentialité

## Ce que le bot lit

La version actuelle n'a **aucun gestionnaire de messages ordinaires** et n'active pas l'intent Discord Message Content. Elle traite les valeurs des commandes slash autorisées dans les serveurs configurés. Elle ne lit pas l'historique des salons, les DMs ou les pièces jointes ordinaires. La seule pièce jointe traitée est l'image explicitement sélectionnée dans `/analyser_image`; cette commande est désactivée si aucun `VISION_MODEL` n'est configuré.

Audio, vidéo, génération média et capture caméra ne sont **pas encore implémentés**. La cible fonctionnelle et ses règles de consentement sont décrites dans [FEATURES.md](FEATURES.md). Les pistes de modèles vision/webcam et IRMf sont recensées dans [la veille de recherche](RECHERCHE-MODELES-VISION-IRMf.md); elles ne sont ni intégrées ni une autorisation d’inférer un état mental.

## Ce qui est enregistré

- **Archive brute** : question et réponse des seules commandes `/parler`, avec IDs Discord, date, serveur et salon. Elle conserve le contenu original sans le remplacer par un résumé. Durée configurable via `ARCHIVE_RETENTION_DAYS` (30 jours par défaut) ; la purge se fait au démarrage, toutes les heures et avant lecture. La valeur `0` désactive les nouvelles archives et purge les existantes au démarrage et toutes les heures.
- **Souvenirs durables** : uniquement ceux ajoutés explicitement avec `/retenir`. Chaque entrée conserve son périmètre, sa source (URL éventuelle + IDs de l'interaction Discord), sa date et un niveau de confiance fourni par l'utilisateur.
- **Révisions** : `/corriger` conserve l'ancienne et la nouvelle version jusqu'à ce que le souvenir soit supprimé.
- **Données non conservées par cette version** : pièces jointes ordinaires, audio, vidéo, transcription et messages ordinaires. L’image d’une commande `/analyser_image` est traitée en mémoire pour cette seule requête; LAPLACE ne la copie pas dans sa base, ses journaux, son historique ou ses souvenirs et ne crée pas de fichier temporaire. Le téléversement initial reste une pièce jointe Discord : LAPLACE ne la supprime pas. Si un fournisseur vision externe est activé, les octets de l’image lui sont transmis tels que sélectionnés, y compris les métadonnées encore présentes dans le fichier.

Les résumés non destructifs, les embeddings et la recherche sémantique ne sont pas encore implémentés. Toute future synthèse devra garder les IDs des messages sources et ne jamais écraser l'archive brute.

## Séparation des personnes

- L'archive et les souvenirs privés sont filtrés par ID Discord utilisateur.
- Les souvenirs partagés ne sont visibles que dans le serveur Discord où ils ont été créés (isolation par ID de serveur). Leur création/correction/suppression est réservée aux IDs de propriétaires configurés dans `OWNER_USER_IDS`, et ils ne peuvent être modifiés que depuis ce même serveur.
- Le bot ne lit pas spontanément les messages d'un groupe. Une future mémoire de groupe nécessitera une activation et un consentement explicites.

## Commandes de contrôle

- `/souvenirs` : consultation et recherche textuelle.
- `/corriger` et `/oublier` : correction versionnée ou suppression d'un souvenir.
- `/exporter_mes_donnees` : export JSON privé.
- `/effacer_mes_donnees confirmer:true` : suppression de l'archive et des souvenirs privés de l'utilisateur ; les souvenirs partagés restent en place.

La purge des archives est appliquée au démarrage et périodiquement toutes les heures (et avant la lecture des archives). Les journaux d'exécution n'incluent pas le texte des requêtes ; les messages d'erreur destinés à Discord restent génériques.

## Modèle et flux réseau

- **Ollama local** (défaut) : le processus du bot envoie le contexte au serveur Ollama indiqué, normalement sur la même machine. Le PC doit être accessible à Discord et à Ollama.
- **API externe** (optionnelle) : les questions, les échanges récents et les souvenirs récupérés sont transmis au fournisseur textuel configuré. Le modèle vision externe est distinct et bloqué par défaut; il exige `VISION_PROVIDER=openai_compatible`, une URL/clé `VISION_*` et `ALLOW_EXTERNAL_VISION=true`. Une image envoyée à ce fournisseur quitte le PC; le coût et la rétention relèvent du fournisseur.
- Le bot token et la clé API sont lus dans `.env`, ignoré par Git. Ne les publie jamais. Le fichier SQLite n'est pas chiffré par l'application ; utilise le chiffrement complet du disque et les permissions du compte système.

Évite d'envoyer des mots de passe, tokens, données de paiement ou informations sensibles dans Discord. Cette version ne prétend pas détecter ou expurger tous les secrets.
