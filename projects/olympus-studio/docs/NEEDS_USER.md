# OLYMPUS Studio — ce qui exige vraiment l'utilisateur

**État au 12/11/2026.** Aucun logiciel à installer ni identifiant à transmettre dans le chat pour poursuivre l'écriture du code et les tests GitHub.

## Planification ChatGPT — active depuis le 12 novembre 2026

**Tâche activée :** « OLYMPUS Studio — développement », identifiant `6af632ef3df88191a7ef46e372054ac4`, chaque jour à 02:00, heure Europe/Paris. L'utilisateur a libéré un emplacement le 12 novembre et demandé une exécution immédiate. `run_now` a réussi et a déclenché une session inline dans la conversation le 12 novembre au soir.

Une session est **bornée** : elle ne maintient pas un processus en continu, ne garantit pas l'achèvement, et ne peut pas valider la GTX/Windows sans accès matériel réel.


## Tests matériels Windows, quand disponibles

- Node.js >=20 (22 conseillé) et Chrome/Edge récent : pour exécuter l'interface locale.
- OBS Studio 28+ avec WebSocket v5 activé (port 4455, mot de passe local **non partagé**).
- Microphone/webcam autorisés dans le navigateur pour tests A/V, aucune capture silencieuse.
- ComfyUI installé **uniquement si** les tests de génération réelle doivent démarrer; pas besoin d'acheter de modèle, pas d'API payante.
- GPU GTX 1060/1650 : les tests de VRAM/fps exigent une véritable session sur la tour/portable, indisponible actuellement depuis ChatGPT.
- X-Ray Mirror : chemin et version installés sur la tour seront requis seulement pour brancher des événements réels, pas pour finaliser les contrats logiciels.

## Accès distant

Un lien GitHub ne fournit **pas** d'accès à la tour. Pour des essais avec les applications déjà installées, lancer OLYMPUS localement et transmettre un journal de test, ou utiliser un mode de travail avec accès ordinateur autorisé. Ne pas transmettre de mots de passe OBS, tokens GitHub, secrets Discord ni IP publiques.

## Instructions futures

Tester la version ZIP depuis l'exécution GitHub Actions récente et signaler uniquement les erreurs, comme les flux média muets et les sources qui ne se relient pas. Cette étape n'est pas un prérequis à l'avancement des fonctionnalités simulables sur GitHub.

## Infra et coûts

- GitHub connecté ; aucun nouveau plugin requis pour écriture de code, issues et tests CI.
- Les services cloud de génération peuvent entraîner frais/confidentialité : non obligatoires et non activés.
- Si un agent d'exécution durable externe (Hermes/Chronos/GitHub runner) doit coder sans intervention, le provisionner sur une machine contrôlée, dans une branche isolée, avec budget/permissions définis et garde-fous CI ; ce service **n'est pas actuellement configuré ni démarré** par la présente discussion.
