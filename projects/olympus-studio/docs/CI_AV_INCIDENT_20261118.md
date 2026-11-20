# CI A/V incident — 18 novembre 2026, 22 h Paris

## Reproduction GitHub Actions

- Branche : `feat/olympus-studio-20261112`, HEAD `1bbf005ae4854c33d9d2b8d20c4141c67244a64a`.
- Run : https://github.com/Sathancabrol/monorepo/actions/runs/44387201044 — **failure**.
- `alpha-package` : success. `smoke` : failure à `python tests/browser_edit_export_e2e.py`, ligne 278, scénario **delayed WebAudio preparation**.
- `inspect_export(delayed_path)` : `video_end=1.358 s`, `audio_end=2.674 s`, écart `-1.316 s`; 22 paquets vidéo et 44 audio; plus grands écarts PTS vidéo 0.134, 0.133, 0.130 s. Assertion conservée : `abs(ve-aue)<0.6`.
- Le test synthétique Chromium WebM VP8/Opus distinct a réussi; le test de mux FFmpeg (incluant offset +250 ms) a réussi; les tests du manifeste IndexedDB et erreurs MediaRecorder ont réussi.
- Artefact diagnostic CI : https://github.com/Sathancabrol/monorepo/actions/runs/44387201044/artifacts/14466787206 (rétention 7 jours).

## Décision technique

Ne **pas** assouplir le seuil A/V, ni déclarer l'alpha validée. Les horodatages indiquent un déficit de production/encodage vidéo pendant la préparation WebAudio différée; la cause précise (Canvas, scheduling navigateur, MediaRecorder) n'est pas encore isolée. Conserver la voie FFmpeg locale séparée comme secours documenté, mais elle ne recrée pas les images manquantes.

## Reprise exacte

1. Instrumenter `browser_edit_export_e2e.py` et `src/app.js` pour corréler temps réel, compteur des dessins Canvas, appels `requestFrame`, paquets vidéo et audio **dans le scénario différé**, sans changer les seuils.
2. Vérifier l'ordonnancement de démarrage `MediaRecorder` / `AudioContext` / capture Canvas, puis corriger le producteur plutôt que masquer la dérive.
3. Exécuter le scénario E2E complet dans `smoke`, confirmer `alpha-package`, consigner le SHA exact. Si le défaut est structurel, basculer vers export vidéo et WAV timeline FFmpeg documenté.
4. Après CI verte, raccorder le manifeste de rendu audio au parcours EDIT; auditer adaptateurs/licences des 12 espaces.

Statut : **BLOCKED_CI (régression A/V intermittente)**. Aucune validation Windows/GTX/OBS/écoute; PR #16 draft; aucun merge main.
