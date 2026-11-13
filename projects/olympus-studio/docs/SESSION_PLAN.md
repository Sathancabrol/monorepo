# OLYMPUS Studio — plan d'itérations vers une version complète

**Mis à jour : 2026-11-12.** Dossier unique `projects/olympus-studio/`, branche `feat/olympus-studio-20261112`, PR #16 (brouillon). Aucun merge `main` et aucune modification des projets voisins par défaut.

## Définition de « terminé »

Le projet n'est pas terminé tant qu'on ne peut pas, depuis **une seule interface**, créer un projet, enregistrer une scène et des pistes audio/vidéo synchronisées, brancher OBS, analyser ou enrichir une réunion (transcription/traduction), piloter un avatar XR, générer au moins une séquence via un modèle **gratuit/local**, monter les médias et exporter une vidéo finale; les données doivent survivre à un redémarrage, les traitements être isolés, les licences vérifiées, et les tests Windows 10 (GTX 1060 et/ou GTX 1650) documentés.

Les fonctionnalités très coûteuses (génération temps réel photoréaliste, reconstruction 3D dense) restent options matérielles dans le périmètre long terme, mais **la dégradation de mode** doit être testée.

## Cadence et automatisation

- Lancer une **itération de travail** à chaque session agent disponible : consulter STATUS, HANDOFF, PR #16 et tickets #11 à #15 ; sélectionner une tâche ; implémenter ; ajouter des tests ; vérifier GitHub Actions ; documenter la preuve ; mettre à jour les tickets ; conserver le travail sur la branche.
- Les **tests GitHub Actions** s'exécutent déjà automatiquement aux pushes sur `feat/olympus-studio-20261112` et sur PR. Une exécution CI n'est **pas** un agent qui écrit du nouveau code.
- **Tâche ChatGPT activée le 12/11/2026** : `OLYMPUS Studio — développement` (`6af632ef3df88191a7ef46e372054ac4`), reprise **horaire** à partir du 13/11/2026 à 04:00 Europe/Paris. Une exécution immédiate a été déclenchée à la demande de l'utilisateur le 12/11.
- Une tâche planifiée exécute des sessions **bornées**; pas de programmation ou génération garantie en continu. Accès GitHub et qualité CI à revérifier à chaque passage.

## Ordre de travail, critères et preuves

| Séquence | Livrable | Critères d'acceptation | Dépendances |
|---|---|---|---|
| S01 — consolidation | Coffre IndexedDB, export portable, migration du prototype v0.3 | Importer image/vidéo, fermer/recharger, rouvrir projet, retrouver les médias; export/import portable sous 45 Mo; tests Node et Chromium | Partiellement codé; test navigateur réel et quota à faire |
| S02 — LIVE fiable | OBS WebSocket, commandes scènes/sources/REC, monitoring, capture Windows | Connexion réelle OBS v5, scénario mauvais mot de passe, 30 min stable, absence de fuite des notes privées | OBS Windows et autorisation micro/écran |
| S03 — Audio/Meeting | Sélection des sources audio, sherpa-onnx/WhisperLiveKit, SRT, traduction, diarisation | Un fichier test FR et EN transcrit et exporté; corriger les sous-titres; distinguer incertitude et identités | Modèles ASR légers libres |
| S04 — Éditeur | Timeline de clips, coupes, trims, transitions, mixage, rendu de fichier, annulation | Import vidéo témoin, coupe, réordonne, sauvegarde/recharge, export A/V synchronisé | Benchmark FreeCut/OpenReelio et choix ADR |
| S05 — XR & avatar | Events X-Ray horodatés, tracker gestes, Three-VRM et rendu 3D | Webcam → avatar/overlay animé → OBS → export ; test « claquement de doigts » | Contrat événements X-Ray, matériel test |
| S06 — IA générative | File ComfyUI/WanGP, modèle gratuit, progression et import médias | 1 job réel, échec/reprise, artefact importé, travail LIVE prioritaire | ComfyUI et modèle compatible VRAM |
| S07 — Spatial | Vidéo Android → tracking / COLMAP, profondeur estimée, Watchtower/Cesium | Une scène test construite et enregistrée; séparer précision mesurée/estimée | Accès vidéos, pas besoin de LiDAR |
| S08 — Cinéma/graphics | Caméras, titres, diagrammes, animations et automatisations Chronos | Storyboard → scène animée → export; actions agents journalisées | Moteur de scènes stabilisé |
| S09 — Livraison | Installateur Windows, détection existant, sauvegardes, licences, tests de régression | Installation machine vierge, hors ligne hors setup, tests E2E et manuel, package versionné | Tests réels et audit sécurité/licences |

## Fonctionnement de chaque session

1. **Lire** `docs/HANDOFF.md`, `docs/STATUS.md`, `docs/SESSION_PLAN.md` et PR #16 ; inspecter les derniers échecs CI.
2. **Choisir une tranche verticale** testable de 1 à 3 fonctions complémentaires avec une nouveauté visible par version. Une fois cette tranche validée, enchaîner une autre tranche si le run dispose encore des ressources; sinon consigner le prochain incrément exact.
3. **Implémenter** sur la branche isolée, en préservant le mode local sans cloud/paywall ; ne jamais envoyer une clé/API privée au dépôt.
4. **Ajouter des tests** (syntaxiques, API, unitaires, E2E si navigateur disponible), confirmer le workflow GitHub Actions après le dernier commit.
5. **Tracer** fonctionnalité annoncée vs codée vs testée vs validée Windows ; documenter la provenance des modules tiers/licences.
6. **Transmettre** les bloqueurs matériels uniquement quand un essai ne peut pas avancer sans l'utilisateur ; ne pas demander une nouvelle installation par réflexe.
7. **Conserver l'état** dans les tickets #11-#15 et docs/HANDOFF ; si CI en échec, fixer avant d'annoncer réussite.

## Ressources déjà disponibles

- Repo : https://github.com/Sathancabrol/monorepo/tree/feat/olympus-studio-20261112/projects/olympus-studio
- PR : https://github.com/Sathancabrol/monorepo/pull/16
- CI : https://github.com/Sathancabrol/monorepo/actions/workflows/olympus-studio-ci.yml
- X-Ray et Watchtower : bibliothèques **externes** ; lire les contrats et preuves avant toute attribution d'une fonction « intégrée ».
- Archive v0.3 indépendante dans la conversation `OLYMPUS_STUDIO_reprise_2026-11-12.zip`, non fusionnée.

## Session immédiate — v0.2.3, 12 novembre au soir
- S04 : édition vidéo avec réglages IN/OUT et découpage au curseur sur la timeline globale (sans mutation des fichiers sources).
- Fonctions pures `trimVideoClip`, `splitVideoClip`, `splitStoryboardAt` testées, sérialisation JSON stable.
- Preuve : https://github.com/Sathancabrol/monorepo/actions/runs/43316401111 — **29/29 tests réussis** sur Node/Ubuntu.
- Critère S04 **partiel** : export vidéo sans audio, durée source non contraignante, validation Chromium/Windows requise.

## Suivi 2026-11-13 — session de consolidation S04

- Correctif du champ « Durée » (même règle source que IN/OUT), test de régression et message d'erreur. Pas de nouvelle capacité audio.
- Les critères S04 « sauvegarde/recharge et export A/V synchronisé » restent ouverts; v0.2.4 ne signifie pas une version complète.
- Prochaine tranche : fixture E2E IndexedDB puis audio EDIT. Conserver l'éditeur non destructif et le mode local.

## Planification autonome mise à jour — 13 novembre 2026

- L'automatisation ChatGPT `6af632ef3df88191a7ef46e372054ac4` a été vérifiée **active** et son instruction mise à jour pour exécuter la première tâche `READY` du [backlog autonome](AUTONOMOUS_BACKLOG.md) chaque heure sans attendre un nouveau « continue ».
- Prochaine exécution annoncée par l'automatisation après modification : **13 novembre 2026, 04:00 Europe/Paris**. Les sessions restent bornées, et les tests Windows/OBS/ComfyUI réels peuvent nécessiter une intervention ultérieure.
- A01 démarre par le module son unique d'EDIT et ses tests de modèle; la génération A/V n'est pas validée. Éviter de fermer A01 avant preuve de sortie sonore.

## Cadence renforcée — 13 novembre 2026

- L'utilisateur demande une reprise qui enchaîne sans nouvelle sollicitation. La tâche existante reste unique, activée **toutes les heures à partir de 04:00 Europe/Paris**. Aucun deuxième automate concurrent n'est créé.
- Une exécution reste bornée et peut durer moins que l'intervalle entre deux déclenchements : il n'y a **pas de processus réellement continu** sur un ordinateur permanent.
- À la fin d'une tranche, traiter la suivante si possible; à la fin de la session, sauvegarder le checkpoint et reprendre depuis celui-ci au déclenchement horaire suivant.
- Estimation par **taille relative**, et non par promesse de délai : [WORK_ESTIMATES.md](WORK_ESTIMATES.md). Si un exécuteur permanent Hermes/Chronos est établi ultérieurement avec autorisations, l'automatisation horaire peut servir de contrôle/supervision plutôt que de moteur de développement.

## Itération A02 — 13 novembre, 04h

- Nouveau scénario E2E Chromium **sur origine HTTP réelle**, avec IndexedDB persistant après `reload`, Blob octet-identique, `splitVideoClip` et export Portable unique. La CI a été modifiée pour exécuter ce scénario ; vérifier le statut avant de le considérer comme validé.
- Prochaine tranche : corriger tout échec du job Chromium, étendre le test à la sauvegarde UI complète, puis prouver la piste sonore de l'export EDIT. Aucun essai Windows effectué.

## Reprise A02 — 13 novembre, 05h

- Corriger le step GitHub Actions Chromium mal formaté (séquences `\\n` littérales), puis tester deux rechargements HTTP/IndexedDB avec import Portable intermédiaire. Commits `a83a31a9` et `eabbd614`.
- Vérification CI des commits en attente : ne pas fermer A02 avant résultat vert. Prochaine tranche S : logs CI et réparation; ensuite M : sauvegarde/reprise depuis l'interface complète, puis preuve WebM/Opus A/V.

## Checkpoint A02 — 13 novembre 2026, 06h — import média par l'interface

- Relecture des documents de pilotage, PR #16, tickets #11–#17, workflow CI et scénario IndexedDB avant écriture.
- **Nouveau test E2E réel-origine HTTP codé** : `tests/browser_indexeddb_e2e.py` pilote maintenant le champ `#fileMedia` dans Chromium Playwright, importe un PNG 1×1 via l'interface, vérifie son stockage IndexedDB, recharge le navigateur puis confirme le média et ses octets en base (taille). Le scénario API existant continue à tester split et aller-retour Portable.
- Commit de test : `a7819e49df64eb4ec80864d5d1cea694be4128a3` (branche isolée). **Pas de preuve CI verte pour ce commit** : la recherche des runs liés a retourné zéro résultat lors de la session; la CI précédente `43362826557` a été annulée, ce qui n'est pas une preuve d'échec de tests. Les annulations peuvent venir de `cancel-in-progress: true`.
- Ce test **ne valide pas** la sauvegarde d'un projet complet via les boutons de l'interface, ni l'export A/V, ni Windows. Il reste à vérifier la présence du média dans l'UI après rechargement et l'export/import Portable par l'UI.
- **Reprise exacte (taille S)** : récupérer le run CI le plus récent sur la branche, inspecter le job Chromium et corriger immédiatement si rouge. **Ensuite (taille M)** : E2E de projet complet `#btnPortable`/`#fileProject`, puis A01/A03 fixture WebM + son et vérification codec Opus/décalage. Aucun merge ni installation sur Windows.

## Checkpoint A02 — 13 novembre 2026, 07h — export/import Portable via l'interface

- **Incrément E2E livré** : `tests/browser_indexeddb_e2e.py` pilote `#btnPortable`, capture le fichier JSON réellement téléchargé, vérifie la scène et l'unique média intégré, efface volontairement l'enregistrement IndexedDB de la fixture, recharge la page puis importe le JSON par `#fileProject`. Il contrôle le calque réapparu et l'égalité octet à octet du PNG restauré. Aucun média utilisateur n'est utilisé.
- Commit de code : [`16ef2e1d`](https://github.com/Sathancabrol/monorepo/commit/16ef2e1da3c5099eb5844f80a6f672f85684be8e). CI associée [`43376152256`](https://github.com/Sathancabrol/monorepo/actions/runs/43376152256) **en cours à la consultation**, donc ne pas déclarer A02 validée.
- **Limites** : test Chromium Linux/HTTP automatisé, sans preuve Windows, ni sauvegarde du montage de clips par les boutons UI, ni export WebM audio audible. A01 et A02 restent ouverts.
- **Reprise exacte (S)** : lire les étapes/logs de la CI `43376152256`; si échec, corriger d'abord le test ou le produit. Si succès, poursuivre A01/A03 (M) : fixture WebM A/V avec inspection du codec Opus, présence sonore et dérive; ne pas confondre présence de piste et qualité audio.


## Session 08h — incrément de sûreté audio EDIT

- A01 (taille M) : `src/editor-export.js` sélectionne exclusivement VP8/Opus ou VP9/Opus quand une piste audio est demandée. Sans encodeur audio déclaré compatible, l'export est refusé plutôt que de produire silencieusement un WebM potentiellement muet.
- Tests de contrat écrits dans `tests/editor-export.test.mjs`, syntaxe intégrée au workflow CI dédié, module ajouté à l'allowlist du serveur local.
- **À reprendre (S)** : contrôler CI du dernier commit et réparer si nécessaire. **Puis (M)** : test E2E réel avec fichier WebM et ffprobe, puis E2E sauvegarde clips UI. Pas de preuve Windows.

## Checkpoint 13 novembre 2026, 09h — réparation CI A02

- Lecture des logs [run 43383108337](https://github.com/Sathancabrol/monorepo/actions/runs/43383108337) : `Static parse` et `API smoke tests` verts; l'E2E Chromium a expiré à la ligne 75 en attendant `olympus-ui-fixture.png`. Chromium a bien été téléchargé sous Ubuntu 24.04. Il ne s'agit plus de l'erreur de support Ubuntu 26.04.
- **Cause déduite du code, à confirmer par CI** : `src/app.js` importe `./video-duration.js`, mais la liste statique de `server.mjs` ne contenait pas `/src/video-duration.js`; le navigateur reçoit donc 403 et n'initialise pas l'interface. Correctif [ca9fc17e](https://github.com/Sathancabrol/monorepo/commit/ca9fc17eb4d2c492549c525d2e302534b76020a1).
- **Test de non-régression** : [d8df55a3](https://github.com/Sathancabrol/monorepo/commit/d8df55a3ff988548743540bf558315f5567083a9) vérifie HTTP 200 sur ce module, les 12 espaces réellement initialisés et l'absence d'erreurs JavaScript avant le parcours IndexedDB.
- **Validation** : correctif et test codés; pas encore de preuve d'exécution Chromium verte sur ces commits. A01/A02/A03 restent ouverts. Aucune intervention Windows ni merge main.
- **Reprise exacte, taille S** : consulter la CI du dernier commit, réparer tout nouveau traceback, confirmer le parcours IndexedDB/Portable. **Ensuite, taille M** : fixture A/V WebM Opus réelle avec analyse ffprobe et mesure de dérive; puis sauvegarde de clips via UI.

## Checkpoint 13 novembre 2026 — 10 h — A03 fixture A/V

- **Vérification CI précédente** : run [43390610164](https://github.com/Sathancabrol/monorepo/actions/runs/43390610164), job `smoke` **success**. Ce run suit le correctif de l'allowlist HTTP et les tests E2E, mais ne valide pas la fixture A/V ajoutée ensuite.
- **Code nouveau** : `tests/browser_av_fixture.py` produit un WebM synthétique à partir d'un Canvas animé et d'un oscillateur Web Audio, via MediaRecorder Chromium, sans caméra/micro/fichier personnel. `ffprobe` doit constater un flux VP8/VP9 et un flux audio Opus; le test échoue si un flux manque. Le workflow CI dédié exécute ce test après l'E2E IndexedDB. Commits `b6550d00` et `af3c84cc`.
- **Limite essentielle** : il s'agit d'une preuve de capacité de l'encodeur navigateur, pas encore d'un export EDIT de l'application, ni d'une mesure de dérive ou de volume audible. Le test n'a pas encore de résultat CI constaté sur ces commits; A01/A03 restent ouverts.
- **Reprise exacte (S)** : lire la CI du dernier commit `af3c84cc` ou suivant et réparer les erreurs de génération/ffprobe. **Ensuite (M)** : piloter le bouton `Exporter WebM (audio optionnel)` d'EDIT sur média synthétique et analyser la sortie via ffprobe, comparer durées/début audio/vidéo; poursuivre A02 UI clips.

## Checkpoint 13 novembre 2026, 11 h — A03 vérification temporelle et niveau sonore

- **CI du précédent incrément confirmée verte** : [run 43397793335](https://github.com/Sathancabrol/monorepo/actions/runs/43397793335), job `smoke` success, y compris Chromium E2E IndexedDB et fixture A/V Opus. Ceci valide une **fixture d'encodeur**, pas l'export EDIT.
- **Nouvelle tranche codée** : `tests/browser_av_fixture.py` vérifie désormais les paquets réels via `ffprobe -show_packets` : bornes temporelles des pistes audio et vidéo, durée >0,7 s, écarts de début et de fin <0,5 s. Décode l'audio avec FFmpeg `volumedetect` et exige un niveau moyen non silencieux. Le test imprime les écarts et le volume mesurés. Commit `2ef71e5e011f1cad159a3a3b8dc6b42152514177`.
- **Limites** : seuils de fumée larges, pas une mesure précise de dérive ni preuve d'écoute humaine; la fixture ne passe pas par le bouton d'export EDIT. **CI du nouveau commit à vérifier** avant de déclarer ces assertions réussies. A01/A03 restent ouverts.
- **Prochaine action exacte (S)** : inspecter le job CI du commit `2ef71e5e`; corriger toute erreur FFprobe, décodeur ou timing. **Ensuite (M)** : E2E export WebM du véritable éditeur EDIT avec WAV de synthèse et inspection ffprobe/volumedetect. Puis **(M)** : clips EDIT persistés via l'interface et restauration Portable. Aucun test Windows/OBS/ComfyUI réel.

## Checkpoint 13 novembre 2026 — correction FFmpeg A03

- Relecture backlog, HANDOFF, STATUS, SESSION_PLAN, ROADMAP, état A03 et CI. La recherche de runs pour `2ef71e5e` retourne [43406132636](https://github.com/Sathancabrol/monorepo/actions/runs/43406132636) **annulé** : ce n'est ni un succès ni un échec de test. Le run antérieur [43397793335](https://github.com/Sathancabrol/monorepo/actions/runs/43397793335) était vert pour la fixture A/V avant les nouveaux contrôles temporels/volume.
- **Bug certain identifié par inspection** : la regex Python raw-string `mean_volume:\\\\s*(-?[\\\\d.]+) dB` cherchait des antislashs littéraux, pas les espaces et chiffres de FFmpeg. Correction `b1ff456b` vers `mean_volume:\\s*(-?[\\d.]+) dB` et assertion de non-régression `b9eea37b` sur une ligne représentative de `volumedetect`. Vérification locale de la regex Python : PASS. Les contrôles FFprobe/FFmpeg complets n'ont pas été exécutés localement dans cette session.
- **CI du nouveau commit : à confirmer**; ne pas considérer A03 validée tant que la fixture réelle n'a pas produit ses mesures en CI. Pas de preuve d'export via le bouton EDIT ni de validation Windows.
- **Prochaine action exacte (S)** : consulter la CI du dernier commit `b9eea37b` et ses logs; réparer si rouge. **Ensuite (M)** : E2E réel du bouton export EDIT avec média WAV synthétique, inspection Opus, énergie sonore et bornes A/V. **Puis (M)** : reprise et sauvegarde des clips EDIT depuis UI/Portable. Aucun secret ni merge main.
