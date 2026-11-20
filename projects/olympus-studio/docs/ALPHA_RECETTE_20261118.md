# Recette alpha OLYMPUS Studio — 18 novembre 2026

**Statut : preview démontrable, pas recette Windows validée.** Référence CI [44196255249](https://github.com/Sathancabrol/monorepo/actions/runs/44196255249), HEAD `e212128c` : jobs `smoke` et `alpha-package` réussis sur Ubuntu 24.04. Artefact `olympus-studio-preview` publié (ID 14378652592). Les contrôles E2E Chromium/IndexedDB/Portable, manifest, export EDIT A/V et smoke HTTP du ZIP extrait sont verts **pour cette exécution**; la dérive A/V était intermittente lors de runs précédents. Une réussite isolée n'établit pas sa fiabilité.

## Installer sans payer ni exposer ses données

1. Ouvrir [Actions OLYMPUS](https://github.com/Sathancabrol/monorepo/actions/workflows/olympus-studio-ci.yml), choisir le **dernier run vert de la branche** `feat/olympus-studio-20261112`, puis l'artefact `olympus-studio-preview` du job `alpha-package`. Ne pas confondre ZIP de téléchargement GitHub et ZIP intérieur `olympus-studio-preview.zip` : extraire les deux niveaux si nécessaire.
2. Installer soi-même Node.js 20+ (22 conseillé) si absent. Décompresser le ZIP intérieur dans un répertoire utilisateur. Lancer `LANCER_OLYMPUS.bat` depuis le dossier extrait; garder la console ouverte. L'interface est sur `http://127.0.0.1:8787`. Aucun compte, API cloud ou modèle n'est requis pour la démo locale. Ne pas publier le port sur Internet.
3. Si rien ne s'ouvre, vérifier `node --version`, puis dans le dossier extrait `node server.mjs` et ouvrir manuellement l'URL. Port 8787 déjà occupé, antivirus, navigateur et politique d'accès local sont des pistes à vérifier; ne pas désactiver les protections sans diagnostic.

## Recette utilisateur — conserver les preuves

| Contrôle | Procédure | Résultat à noter |
|---|---|---|
| Navigation | Parcourir LIVE, EDIT, GENERATE, XR, AUDIO, MEETING, CAPTURE, CINEMA, AUTOMATE, GRAPHICS, LIBRARY, CONTROL | 12 espaces accessibles; ne pas confondre interface et moteur |
| Médias | Importer une petite vidéo de test et une image dans LIBRARY; fermer et rouvrir le navigateur sur **la même origine** | Médias toujours lisibles dans IndexedDB |
| EDIT | Ajouter deux segments de la même vidéo; régler IN/OUT, diviser, changer l'ordre, undo/redo | Timeline et références non destructrices |
| Sauvegarde | Exporter le projet Portable; garder une copie; réimporter dans un profil navigateur propre | Médias et timeline restaurés; vérifier aussi la piste audio |
| A/V | Importer WAV de test, définir départ/IN/volume, exporter WebM; écouter dans un lecteur externe | Piste réellement audible, durée et synchronisation |
| Vérification technique | Si FFmpeg est installé, lancer `ffprobe -v error -show_streams -show_format fichier.webm` | Présence vidéo et audio Opus, durées et horodatages cohérents |
| OBS | Si OBS 28+ est déjà installé, tester WebSocket v5 avec autorisation explicite | Authentification, scènes, REC; noter les erreurs, ne pas utiliser une scène privée |
| Compatibilité | Répéter sur Windows 10 / GTX 1060 et GTX 1650, noter navigateur, CPU, RAM, VRAM et FPS | **Non validé par la CI Linux** |

Ne pas utiliser des médias personnels sensibles pour cette recette. Enregistrer version Node, navigateur, modèle GPU, commit, captures des erreurs, taille/durée des fichiers et résultat oui/non pour chaque contrôle.

## Limites et secours

- EDIT utilise une seule piste audio indépendante; l'audio natif des clips vidéo n'est pas conservé. MediaRecorder peut perdre des trames malgré une CI verte : **ne pas utiliser le WebM comme master de production sans vérification**.
- Le réparateur FFmpeg documenté dans les guides EDIT peut réassembler des flux, mais son secours à image figée ne recrée pas les images perdues. Conserver les médias originaux et le JSON Portable; préférer un montage externe libre si l'export échoue. La licence exacte du binaire FFmpeg redistribué doit être vérifiée; aucun binaire FFmpeg n'est inclus ici.
- OBS réel, ComfyUI réel, ASR local, bus XR, Watchtower 3D, Chronos, installateur autonome et mesures GTX restent **non validés ou partiels**. Voir [matrice d'intégration](INTEGRATION_MATRIX_ALPHA.md).
- IndexedDB est lié à l'origine navigateur; effacer le profil peut supprimer les médias. Sauvegarder Portable régulièrement (limite de taille indiquée par l'interface). Le paquet nécessite Node et n'est **pas** un .exe autonome.

## Critère de décision

**Alpha technique Linux :** les deux jobs du run 44196255249 sont verts et le ZIP a passé son test HTTP après extraction. **Alpha Windows validée : NON**, tant que la recette manuelle ci-dessus n'a pas été exécutée et que la fiabilité A/V n'est pas démontrée. Garder PR #16 en brouillon; aucune fusion automatique.
