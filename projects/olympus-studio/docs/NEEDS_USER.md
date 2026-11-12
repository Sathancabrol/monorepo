# OLYMPUS Studio — ce qui exige vraiment l'utilisateur

**État au 12/11/2026.** Aucun logiciel à installer ni identifiant à transmettre dans le chat pour poursuivre l'écriture du code et les tests GitHub.

## Blocage de la planification ChatGPT

5 automations sur 5 sont actives (actualités/YouTube, emploi Thau, Cognitorium MVP, immobilier Thau, bilan économique Thau). Tentative de tâche quotidienne OLYMPUS rejetée le 12/11/2026 : `too_many_active_automations`. Pour des **sessions ChatGPT planifiées**, l'utilisateur doit **choisir une tâche existante à désactiver ou remplacer**. Ne pas désactiver une autre veille sans choix explicite. Même avec une tâche, chaque session est bornée; pas un processus informatique continu ni une garantie d'achèvement.

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
