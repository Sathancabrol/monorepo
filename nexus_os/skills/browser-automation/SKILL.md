---
name: browser-automation
description: Piloter un navigateur pas à pas — une action annoncée, un état observé.
triggers: [navigateur, browser, scrape, formulaire, clic, screenshot, e2e, page web]
tags: [web, automation]
tools: [http_get, write_file]
license: MIT
---
# Automatisation navigateur

1. Une seule action par étape, annoncée avant : « je clique X parce que Y ».
2. Après chaque action, décris l'état observé (URL, titre, éléments clés) avant de décider.
3. Sélecteurs stables : `data-testid`, `name`, `role` — jamais une classe CSS générée.
4. Attends un signal réel (élément présent, navigation finie), jamais un `sleep` fixe.
5. Idempotence : un rejeu ne doit ni dupliquer ni détruire.
6. Aucun envoi destructif (paiement, suppression, publication) sans confirmation explicite.
7. Sans moteur navigateur : `http_get` et signale la limite, ne simule pas un rendu.
