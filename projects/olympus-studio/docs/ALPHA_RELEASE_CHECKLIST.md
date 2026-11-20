# OLYMPUS Studio — protocole de recette ALPHA (cible 18/11/2026)

**Statut : non validée sur Windows.** Ce document est une procédure de vérification, pas une attestation de réussite. Utiliser le dernier artefact `olympus-studio-preview` d'une CI dédiée **verte sur le SHA choisi** : https://github.com/Sathancabrol/monorepo/actions/workflows/olympus-studio-ci.yml . Ne pas confondre ZIP de prévisualisation et installateur autonome.

## Préparer sans écraser les données

1. Sur Windows 10, conserver une copie des projets JSON et des médias originaux hors du navigateur. Ne pas effacer IndexedDB ou le profil Chromium. Prévoir Node.js >=20 (22 recommandé), navigateur Chromium/Chrome récent, 2 Go d'espace libre. Aucun téléchargement de moteur ou modèle en arrière-plan.
2. Extraire le ZIP dans un **nouveau** dossier, lancer `LANCER_OLYMPUS.bat` ou, depuis `projects/olympus-studio`, `npm start`; ouvrir `http://127.0.0.1:8787`. Si le port est occupé, arrêter l'autre serveur après identification; ne pas écraser ses fichiers.
3. En terminal dans le dossier de l'application : `npm test`. Consigner version Node, navigateur, Windows, SHA Git, résultat exact. Tester séparément tour GTX 1060 6 Go et portable GTX 1650 4 Go si disponibles; aucune performance GPU n'est présumée.

## Recette de démonstration minimale — résultat attendu / preuve à conserver

| ID | Manipulation | Acceptation | Preuve |
|---|---|---|---|
| R01 | Naviguer dans les 12 espaces depuis la même interface | 12 panneaux accessibles, sans erreur console | Capture + journal console |
| R02 | Importer PNG, WebM court et WAV; créer deux clips depuis une vidéo et régler IN/OUT | Aperçu et deux références à une seule source, sans perte du fichier | Projet et captures EDIT |
| R03 | Modifier titre, ordre, volume; annuler puis rétablir | Retour exact des paramètres et de la timeline | Avant/après JSON |
| R04 | Exporter **Portable**, fermer l'onglet, rouvrir et importer le JSON | Clips et piste audio restaurés, médias lisibles, octets sources préservés; vérifier taille totale <=45 Mo | JSON + taille + journal |
| R05 | Exporter WebM EDIT avec WAV 440 Hz de test | Fichier lisible avec vidéo VP8/VP9 et audio Opus audible; mesurer départ/fin avec ffprobe, écart cible <0,6 s | Fichier WebM, rapport ffprobe, écoute humaine |
| R06 | Répéter R04 et R05 au moins trois fois, y compris après undo/redo | Aucun export absent, pas de dérive aléatoire; tout échec est bloquant | 3 journaux horodatés |
| R07 | Importer une image depuis un job ComfyUI local, si ComfyUI installé et autorisé | Résultat présent dans LIBRARY et conservé après rechargement | Capture + version/API du moteur |
| R08 | OBS WebSocket v5 si OBS installé et autorisé | Connexion, scène, REC, déconnexion contrôlées sans fuite de données privées | Version OBS + journal sans secret |

**Si R05 ou R06 échoue :** ne pas annoncer export A/V fiable. Pour l'alpha, présenter EDIT, sauvegarde Portable et un export vidéo expérimental explicitement marqué; proposer rendu externe FFmpeg comme procédure alternative **uniquement après test réel**, sans affirmer qu'il est intégré. Conserver le fichier source et la sortie défaillante pour diagnostic.

## Limites à annoncer dans la démo

- ComfyUI simulé en CI ne prouve pas une génération réelle; OBS simulé ne prouve pas la capture réelle.
- ASR local, XR/avatar, Watchtower 3D, Chronos et installateur .exe : vérifier individuellement les adaptateurs et licences; une carte de navigation ne signifie pas un moteur intégré.
- Les tests Ubuntu/Chromium CI ne valident pas les périphériques, pilotes, VRAM ni codecs Windows.
- Aucun modèle tiers redistribué sans vérification de sa licence; les moteurs sont des processus locaux externes et optionnels.

## Décision de livraison

Une alpha **démontrable** nécessite R01–R04 sur Windows, un chemin d'export R05 fiable **ou une limitation/alternative démontrée**, une CI verte sur le SHA livré et des instructions de lancement reproductibles. R07–R08 et les autres moteurs restent des capacités optionnelles ou explicitement non finies. Garder PR #16 en brouillon jusqu'à décision humaine; ne pas fusionner dans main.
