# OLYMPUS Fleet — fonctionnement 24 h/24 et coopération multi-appareils

Plan technique du 13 novembre 2026. **État : conception documentée, non installée sur les machines.** Branche isolée, sans toucher au serveur déjà fonctionnel.

## Architecture

- Tour Windows : OLYMPUS Studio (localhost:8787), passerelle web privée Tailscale (localhost:8788 en HTTPS/443), Hermes principal et orchestration locale.
- Portable Windows : Hermes secondaire, outils de compilation, tests et agents spécialisés. Ses tâches s'exécutent physiquement sur le portable.
- Samsung et Redmi : clients OLYMPUS et sources de caméra/capteurs autorisées. Le code existant permet le partage de caméras ; pas encore de worker autonome durable.
- ChatGPT : collaborateur GitHub pour analyse/revue/code et interventions sur créneaux planifiés, sans accès direct continu aux PC.
- GitHub : source de vérité pour code, PR, CI et rapports ; jamais pour secrets.

## Réutilisation : Hermes Peer (pas un second agent framework)

Documentation officielle :
- https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode
- https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server
- https://hermes-agent.nousresearch.com/docs/reference/cli-commands
- https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban

Hermes Kanban est MONO-HÔTE, sa base SQLite ne doit pas être partagée entre PC. Le sous-système Hermes Peer est MULTI-HÔTES et permet les commandes peer dm, peer run (asynchrone avec clé d'idempotence), peer status et peer stop vers un Hermes distant disposant d'un API Server protégé par clé. Des Cron/Kanban peuvent fonctionner indépendamment sur chaque PC.

## Priorité A : infrastructure toujours joignable

Sur LES DEUX PC :
1. Maintenir l'alimentation et le réseau, désactiver la veille sur secteur, assurer ventilation et refroidissement du portable.
2. Sur Tailscale Windows, activer Preferences > Run unattended (persistance VPN après déconnexion utilisateur).
3. Dans une nouvelle fenêtre PowerShell, lancer les diagnostics non destructifs :
   hermes --version
   hermes gateway status
   hermes cron status
   hermes peer --help
   tailscale status
   tailscale serve status
4. Si non installé, hermes gateway install crée une tâche Windows AU LOGIN, et hermes gateway start lance le gateway. Cela n'est PAS suffisant pour une reprise après reboot sans login. Prévoir une étape spécifique pour un vrai service Windows protégé sous le bon compte, avec sauvegarde et test de redémarrage.
5. Ne pas utiliser auto-login Windows, ne pas effacer la configuration Hermes actuelle. Le mode unattended de Tailscale concerne Tailscale, pas Hermes ni OLYMPUS.

## Priorité B : rendre les deux Hermes mutuellement accessibles

Seulement si hermes peer --help montre la fonctionnalité sur les deux PC.

Configuration locale de CHAQUE Hermes (installation Windows native) : fichier %LOCALAPPDATA%\hermes\.env, conserver les autres paramètres.

    API_SERVER_ENABLED=true
    API_SERVER_HOST=127.0.0.1
    API_SERVER_PORT=8642
    API_SERVER_KEY=<CLE_ALEATOIRE_UNIQUE_DE_32_OCTETS_OU_PLUS>

Créer une clé robuste différente par machine, en local ; ne jamais la copier dans un chat, GitHub, rapport de diagnostic ou URL. Redémarrer Hermes avec hermes gateway restart. Vérifier que le serveur écoute uniquement sur 127.0.0.1:8642. Sans jeton, une réponse non autorisée (401) est attendue.

Ne pas modifier le Serve HTTPS/443 déjà utilisé par Studio. Sur CHAQUE PC, après consultation de tailscale serve status, ajouter le second port :

    tailscale serve --https=8443 --bg 8642
    tailscale serve status

Vérifier la coexistence du port 443 (Studio sur la tour) et 8443 (API Hermes). Ne jamais utiliser tailscale funnel, serve reset, ni ouvrir un port sur la box.

Sur la TOUR :

    hermes peer add portable --url https://<URL_TAILSCALE_PORTABLE>:8443

La clé côté tour doit être celle du serveur Hermes du PORTABLE : enregistrer localement HERMES_PEER_PORTABLE_KEY dans le .env de la tour, sans la placer sur la ligne de commande.

Sur le PORTABLE :

    hermes peer add tour --url https://<URL_TAILSCALE_TOUR>:8443

Enregistrer localement HERMES_PEER_TOUR_KEY avec la clé du serveur Hermes de la TOUR. Ne pas envoyer de clés dans le navigateur Studio. En cas de doute sur le format de votre version, examiner hermes peer add --help.

Test à faire sur tour :

    hermes peer list
    hermes peer dm portable "Confirme le nom de ta machine et que tu es Hermes sur le portable."

Puis réciproquement sur le portable :

    hermes peer list
    hermes peer dm tour "Confirme le nom de ta machine et que tu es Hermes sur la tour."

Test de longue tâche sur la tour, sans écriture :

    hermes peer run portable --idempotency-key olympus-smoke-001 "Inspecte en lecture seule les scripts de tests OLYMPUS disponibles et retourne leur liste."

Récupérer le run_id et suivre avec hermes peer status portable <RUN_ID>. Ne PAS relancer le même travail sans vérifier d'abord son statut.

Attention : API Server Hermes donne accès aux outils complets de l'agent, terminal compris. Tailscale est la protection réseau ; une clé API et la réduction des privilèges des agents restent indispensables. Pas de route de commande shell arbitraire dans Studio.

## Priorité C : 24/7 au sens fort

Configurer un vrai démarrage AU BOOT après avoir validé les peers : service Windows sécurisé ou équivalent démarré sous le compte Hermes dédié, droits minimaux, secrets conservés et redémarrage en cas de crash. Faire un test sans session ouverte. Démarrer aussi les serveurs Node OLYMPUS sur la tour en service. Ne pas considérer un simple .bat et une tâche ONLOGON comme du 24/7.

Gestion de vie :
- Tâches légères et diagnostics : sans modèle IA si possible.
- Inférence locale Ollama/llama.cpp : prioritaire, testée sur chaque machine avant attribution.
- Services cloud gratuits : facultatifs, soumis à quota et erreur 429 ; jamais de bascule implicite vers paiement.
- Files persistantes, checkpoints, clé d'idempotence, limites de relance, journal d'erreur, approbation explicite pour actions sensibles.
- LIVE caméra prioritaire sur tâches GPU intensives ; Android peut suspendre Chrome/Termux en arrière-plan, donc les téléphones ne sont pas les nœuds critiques H24.
- Logiciel gratuit ne signifie pas courant électrique gratuit ni disponibilité 100 % en cas de panne de courant/Internet.

## Priorité D : couche OLYMPUS Fleet à coder ensuite

Ne pas dupliquer Hermes Peer ni Kanban. OLYMPUS supervise :
- Statut de chaque nœud (online, degraded, offline), dernière activité, versions, modèles disponibles, CPU/GPU/RAM, caméras, jobs, logs et anomalies.
- Interrogation par la TOUR de ses peers Hermes, clés stockées serveur UNIQUEMENT, jamais dans JavaScript ou IndexedDB du téléphone.
- Routines d'ordonnancement et de surveillance, reprise par identifiant, déduplication, limite de concurrence ; stockage durable SQLite côté coordinateur.
- Exécution strictement délimitée par commandes autorisées (diagnostic, tests de projet, statut, lecture de journaux) avant tout contrôle étendu.
- Git en worktrees/branches isolés et PR après tests. Une seule source de vérité par tâche, aucun commit simultané depuis deux agents sur le même worktree.
- ChatGPT passe par GitHub et par les tâches planifiées existantes. Pas de prétention à une présence synchrone 24/7 sur les PC, ni à une API gratuite illimitée liée à ChatGPT Plus.

## Critères d'acceptation

A. La tour, Samsung et Redmi partagent les caméras dans Studio : confirmé par test utilisateur.
B. Tailscale unattended actif sur tour et portable ; 443 Studio ET 8443 API Hermes coexistent : à prouver.
C. Hermes peer dm a fonctionné dans LES DEUX SENS avec identité de machine correcte : à prouver.
D. Une tâche peer run se termine sur le portable et le résultat revient sur la tour : à prouver.
E. Une coupure réseau et un redémarrage n'entraînent ni tâche perdue ni double exécution : à développer et tester.
F. OLYMPUS montre les nœuds, leurs capacités et les états réels dans une seule interface : à développer.
G. Le système complet redémarre après extinction/reboot sans ouverture de session : à développer et tester.

**Prochaine action recommandée :** obtenir les résultats non secrets des six commandes diagnostiques sur les deux PC, puis activer les deux API Hermes avec clés individuelles et HTTPS/8443 privé. Ne pas exposer la clé ni casser le port 443 d'OLYMPUS.