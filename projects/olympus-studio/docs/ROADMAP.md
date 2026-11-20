# Feuille de route / actions sauvegardées

## Principes invariants
- Interface unique, simple/expert, douze espaces : LIVE, EDIT, GENERATE, XR, AUDIO, MEETING, CAPTURE, CINEMA, AUTOMATE, GRAPHICS, LIBRARY, CONTROL.
- Local/hors-ligne, zéro abonnement ou API payante imposée ; aucune activation d'outils tiers sans décision explicite.
- Isolation dans ce dossier. Travail sur branche, revue puis merge explicite.
- Test mesurable, non destructif, conservation des fichiers source et journal d'audit.

## S0 — 12 novembre (réalisation immédiate)
- [x] Identifier monorepo et créer branche isolée.
- [x] Comparer les bases de montage intégrables et documenter les licences.
- [x] Conserver l'historique v0.3 dans le cahier des charges.
- [ ] Tester réellement shell GitHub sur Windows.
- [ ] Importer le prototype v0.3 complet, réconcilier ses fonctions avec ce dossier.

## S1 — socle unique / première tranche
- [ ] Sauvegarde de projet durable incluant les médias (pas de simples blob URLs).
- [ ] Connecter OBS websocket v5 : identifiant, scènes, sources, évènements; jamais enregistrer le mot de passe en clair.
- [ ] Sortie OBS source navigateur, séparer audio public / privé.
- [ ] Mesurer FPS, latences et charge GPU/CPU, GTX 1060 puis 1650.
- [ ] Sélectionner éditeur NLE : essai FreeCut (MIT) et OpenReelio (MIT), puis preuve d'un montage exporté.

## S2 — perception & meeting
- [ ] Connecteur événements XR depuis X-Ray Mirror (poses, gestes, objets, coordonnées normalisées).
- [ ] ASR local sherpa-onnx / WhisperLiveKit : micro ET audio système routables, diarisation avec incertitudes.
- [ ] Sous-titres, traduction, transcription corrigible, actions/décisions avec provenance.
- [ ] Synchronisation multimodale temps (audio, vidéo, détections, schémas).

## S3 — génération et environnement spatial
- [ ] Workflows ComfyUI API JSON, tâches asynchrones, modèles installés détectés.
- [ ] Rendu génératif vidéo différé avec profil GPU léger et garde-fous VRAM.
- [ ] Sortie Cesium Watchtower vers couche vidéo/texture, GeoJSON avec reprojection.
- [ ] Capture Android, photogrammétrie sans LiDAR (test COLMAP), profondeur estimée vs métrique.

## S4 — qualité, agents, redistribution
- [ ] Chronos orchestration avec permissions par action, journal et annulation.
- [ ] Scan et compatibilité licences tiers pour redistribution.
- [ ] Installation Windows idempotente, reprise après crash, profils matériels et ressources.
- [ ] Tests end-to-end et vidéo de preuve de chaque capacité.

## Prochaines sessions de recherche — ordonnées
1. Lire sources et bench de FreeCut, Velorn, OpenReelio, OBS+libobs : exports, licences, API, performances, packaging.
2. PoC OBS bidirectionnel (scène + start/stop REC + sous-titres) et tests erreurs auth.
3. POC import/export de projet entre shell et éditeur choisi.
4. POC X-Ray event bus et preuves de latence 720p.
5. ASR offline multi-source (micro/browser/sortie système), tests confidentialité.
6. Prévisualisation Cesium et scène 3D sans dépendre de Google Maps.
7. Plan migration v0.3 → dossier GitHub et CI.

## Routines de reprise
Chaque session : relire STATUS, choisir le premier test faisable, réaliser 1 changement isolé, ajouter preuve/limite, puis réordonner les trois prochaines tâches. Pas de promesse de travail continu : nécessite exécution explicite ou tâche planifiée active.

## 13 novembre — état S04

- [x] Contrôle des bornes IN/OUT sur durée source connue.
- [x] Contrôle du champ « Durée » par la même validation, avec test de régression.
- [ ] Test de sauvegarde/reprise de clips avec IndexedDB sur une vraie origine.
- [ ] Export EDIT A/V synchronisé et vérifié.
- [ ] Tests matériels Windows GTX 1060 / GTX 1650.

## Itération A02 — 13 novembre, 04h

- [x] Écrire un test Playwright Chromium HTTP/IndexedDB avec reload réel, deux segments partageant une seule source et roundtrip Portable.
- [x] Brancher le scénario sur la CI dédiée.
- [ ] Obtenir une CI verte au dernier commit et conserver sa preuve.
- [ ] Étendre à l'interface complète (sauvegarder/recharger le projet), puis valider sous Windows.

## A02 — 13 novembre, 05h

- [x] Corriger la syntaxe YAML du nouveau step Chromium (littéraux `\\n` remplacés par vrais sauts de ligne).
- [x] Ajouter un second reload HTTP et vérifier les octets du média Portable réimporté en IndexedDB.
- [ ] Vérifier CI verte sur dernier commit, corriger les échecs.
- [ ] Tester le parcours UI complet et l'export A/V sonore, puis Windows.
