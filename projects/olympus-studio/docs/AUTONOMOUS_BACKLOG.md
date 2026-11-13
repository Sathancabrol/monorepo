# OLYMPUS Studio — plan d'exécution autonome

**Créé le 13/11/2026.** Registre prioritaire utilisé par la tâche ChatGPT « OLYMPUS Studio — développement » (ID `6af632ef3df88191a7ef46e372054ac4`) une fois par heure, heure Europe/Paris. Chaque session dispose d'un temps fini : il ne s'agit **pas** d'un ordinateur qui travaille en continu.

Dépôt `Sathancabrol/monorepo` · branche `feat/olympus-studio-20261112` · uniquement `projects/olympus-studio/` et workflow CI dédié · PR #16 en brouillon · aucun merge dans main.

## Algorithme à appliquer à chaque session

1. **Synchroniser avant toute écriture** : relire ce fichier, `HANDOFF.md`, `STATUS.md`, `SESSION_PLAN.md`, PR #16, issues #11–#17, dernier commit et exécution GitHub Actions.
2. **Choisir automatiquement** la première tâche ouverte `READY` non couverte par un commit/test existant. Si impossible sans Windows/secret ou dépendance, indiquer `BLOCKED` et sauter vers le prochain `READY`; ne pas attendre « continue ».
3. **Livrer une tranche verticale** (fonction utilisateur visible + code + test au minimum). Dès qu'une tranche est terminée et validée, **enchaîner la suivante au cours du même run si ses ressources le permettent**; sinon enregistrer la prochaine action exacte pour l'exécution horaire suivante. Rester sur la branche isolée et utiliser SHA de fichier avant toute modification.
4. **Tester réellement** : syntaxe → tests Node → GitHub Actions au dernier commit → navigateur si possible → statut exact et preuve. Si CI rouge, réparer **avant** la prochaine fonctionnalité.
5. **Reporter** dans ce fichier, `STATUS.md` et `HANDOFF.md` les commits, résultats, limites, taille relative S/M/L/XL et nouvelle première tâche. Mettre à jour l'issue liée. Une CI verte n'est ni un test Windows ni une garantie d'export A/V.
6. Quand tous les critères de fin sont vérifiés, proposer une phase de recette finale; **ne jamais conclure « terminé » si les tests matériels et licences manquent.**

## Backlog priorisé — sélectionner par ordre, en sautant les blocages

| ID | Statut | Travail et critère observable | Ticket |
|---|---|---|---|
| A01 | READY | **Audio EDIT** : une piste audio locale choisie, départ/IN/volume, persistance, export WebM avec piste son et audio réellement audible à vérifier; zéro fuite vers LIVE | #17 |
| A02 | READY | **E2E navigateur** : vrai HTTP, IndexedDB, deux segments du même média sauvegardés/rechargés/export portable; tests CI Chromium et reprise après fermeture | #11, #17 |
| A03 | READY | **Tests A/V** : générer une fixture vidéo+son, mesurer décalage entre A/V et confirmer codec opus dans WebM exporté, enregistrer preuve; sans Windows si possible | #17 |
| A04 | READY | **Undo/redo EDIT** : annulation de coupes, ordre, titre et audio sans toucher aux fichiers sources; tests propriétés | #17 |
| A05 | READY | **FreeCut/OpenReelio** : benchmark du format d'échange, API, dépendances, licences et ressources; décision ADR étayée, pas de fork prématuré | #12 |
| A06 | READY | **Réunion ASR local** : sélectionner explicitement micro/onglet/fichier, transcription FR+EN offline (sherpa-onnx ou Whisper), SRT révisable et provenance | #14 |
| A07 | READY | **XR event bus** : flux local horodaté X-Ray, effets et gestes, activation par claquement de doigts, tests sans webcam avec fixtures | #14 |
| A08 | READY | **ComfyUI OUTPUT** : récupérer et importer un résultat de job terminé sans chemin arbitraire ni SSRF, cache local et gestion des erreurs | #14 |
| A09 | READY | **Chronos** : journal des ordres, permissions par action, confirmation des actions externes; agents non connectés par défaut | #14 |
| A10 | READY | **Watchtower** : contrat scène/GeoJSON/positions + passage de caméra sans dupliquer Cesium; démo sans données personnelles | #15 |
| A11 | READY | **3D/XR avatars** : rendu d'un VRM libre, suivi pose/visage avec démo synthétique, profil matériel dégradé | #15 |
| A12 | READY | **Packaging** : installateur Windows réversible, détecter Node/OBS/ComfyUI, modes offline et diagnostic de dépendances | #11 |
| W01 | BLOCKED_WINDOWS | Test OBS WebSocket v5 réel sur tour, scénarios mauvais mdp, déconnexion, 30 min de capture et scène privée/public | #13 |
| W02 | BLOCKED_WINDOWS | Validation GPU GTX 1060 6 Go / GTX 1650 4 Go, audio et vidéo synchronisés, temps réel, latence, captures sans dérive | #13, #17 |
| W03 | BLOCKED_WINDOWS | Import d'une scène Watchtower depuis installation utilisateur, contrôles 3D réels et profils faibles ressources | #15 |

**Règle** : `READY` signifie « peut être étudié/codé sans la tour », pas « déjà implémenté ». Une tâche ne devient `DONE` qu'après vérifications d'acceptation; les étapes partielles sont notées dans `STATUS.md`.

## Prérequis & contraintes permanentes

- Gratuit, local, hors-ligne autant que possible; aucune API payante, licence incompatible ou téléchargement de modèle/logiciel en silence.
- Aucun mot de passe/tokens en chat, GitHub ou journaux; connexions locales sur autorisation; permissions caméra et microphone explicites.
- Aucun autre projet modifié; conserver la PR #16 en brouillon et le code dans le dossier isolé.
- Livrer au moins une capacité réelle par itération; si tâche bloquée, passer à la suivante et documenter pourquoi.
- Ne pas présumer que la tâche dispose d'accès à la tour Windows, aux fichiers non montés, ou d'un droit de fusion.

## Critères de fin (non atteints)

Une seule interface Windows capable de créer et reprendre un projet avec médias, capter caméra/audio, piloter OBS réellement, transcrire une réunion localement, insérer un avatar XR, générer/importer une vidéo via modèle local, produire une composition 3D/Watchtower, monter et exporter vidéo+audio synchronisés, gérer les permissions/agents Chronos et installer hors ligne après setup. Les tests E2E/Windows (sur au moins un PC cible), licences des dépendances, récupération d'erreur et guide débutant doivent être prouvés.

## Reprise prévue

**Prochaine session planifiée dès le 13/11/2026 à 04:00 Europe/Paris, puis toutes les heures** : lire et vérifier A01 (audio EDIT). Si CI rouge, corriger; sinon chercher preuve d'export sonore A/V et reprendre A02 (IndexedDB) si A01 est bloquée. Chaque run doit préparer le prochain automatiquement. Ne pas répéter un correctif déjà livré.

## Cadence et estimation de charge

- Une session automatique démarre **au plus une fois par heure** et n'est pas une heure garantie de calcul ou de codage. Les travaux en cours sont repris depuis les checkpoints.
- **Taille relative des tâches** et règle de progression : [WORK_ESTIMATES.md](WORK_ESTIMATES.md). Ne pas confondre poids du chantier, temps de passage et date de livraison.
- Les tâches matérielles Windows restent dans les blocages; passer à une autre tâche READY sans attendre l'utilisateur.
