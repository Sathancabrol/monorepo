# OLYMPUS Studio — régie OBS WebSocket v5 (v0.2)

## Statut et périmètre

Connecteur **implémenté dans l'interface**, sans dépendance npm, via `src/obs-client.js` et `src/obs-panel.js`. Tests automatisés : URL locale, défi SHA-256, protocole d'identification, GetSceneList, GetRecordStatus, SetCurrentProgramScene, StartRecord, StopRecord, refus sans mot de passe.

**OBS Windows réel, enregistrement audiovisuel et retour d'événements réels NON vérifiés.** Les tests utilisent un serveur WebSocket simulé.

## Mise en service sur le PC

1. Installer ou lancer **OBS Studio 28+**.
2. Dans OBS : `Outils → Paramètres du serveur WebSocket` ; activer, conserver le port local 4455 et choisir un mot de passe.
3. Lancer OLYMPUS : `cd projects/olympus-studio && npm start`, ouvrir `http://127.0.0.1:8787`.
4. À droite dans « OBS · RÉGIE DISTANTE », entrer `ws://127.0.0.1:4455` et le mot de passe. Cliquer **Connecter**.
5. Choisir une scène dans la liste. Les boutons « Démarrer REC » et « Arrêter REC » commandent le **vrai OBS**. Ils n'activent aucun streaming.
6. Pour diffuser le Canvas OLYMPUS dans OBS, cliquer séparément « Sortie OBS » dans la barre d'outils, puis créer dans OBS une **Source navigateur** : `http://127.0.0.1:8787/obs`, 1280×720. Cette route est vidéo MJPEG, sans audio.

## Enregistrer de l'audio directement dans le Canvas

- Bouton **+ Micro** : permission explicite du navigateur.
- Bouton **+ Écran** : autorisation Chrome/Edge de partager un onglet, fenêtre ou écran. L'audio partagé dépend des capacités offertes par le navigateur et le système.
- Bouton **WebM** : filme le Canvas. Si un flux audio autorisé est disponible, ajoute une piste audio; si les deux sources existent, les mélange via Web Audio.
- La piste audio n'est **pas transmise** dans le MJPEG OBS. Pour streaming fiable, capturer le micro et l'audio système dans OBS séparément.
- Les commandes ne démarrent aucune capture automatiquement.

## Sécurité

- Connexion OBS uniquement via `ws://127.0.0.1`, `ws://localhost` ou boucle locale IPv6. Aucun endpoint distant.
- L'authentification OBS v5 utilise deux étapes SHA-256 WebCrypto; le mot de passe n'est enregistré ni sur disque, ni dans localStorage, ni dans le projet. Effacé du champ dès connexion.
- Le serveur de Studio n'accepte que les fichiers publics explicitement autorisés. Les routes d'action refusent les origines web distantes, le serveur écoute seulement `127.0.0.1`.
- L'utilisateur contrôle lui-même chaque changement de scène et chaque départ/arrêt d'enregistrement.
- Pour réunions filmées : informer les participants et appliquer les règles de consentement/confidentialité.

## Limites et tests prochains

- Vraie connexion OBS v5 Windows, scénarios mot de passe incorrect/reconnexion et événements RecordStateChanged.
- Test navigateur Chrome/Edge avec écran + microphone, piste Opus, durée 30 minutes, stabilité RAM/CPU, pertes d'images et réimport de l'export.
- Pas de mapping automatique entre scènes Studio et OBS. OBS reste un processus distinct piloté depuis l'interface.
- Pas d'audio multipiste natif, pas de caméra virtuelle gérée par Studio, pas de RTMP propre.
- Aucun code tiers OBS n'est distribué dans ce dossier : connecteur réseau uniquement.
