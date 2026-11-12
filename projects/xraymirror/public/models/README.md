# Modèles locaux

Ce dossier peut contenir les modèles téléchargés pour un fonctionnement hors ligne.
Le résolveur essaie `models/<id>.task` puis bascule sur l'URL distante épinglée.

Fichiers attendus (jamais committés dans Git) :

- `face_landmarker.task`
- `hand_landmarker.task`
- `gesture_recognizer.task`
- `pose_landmarker_lite.task`
- `efficientdet_lite0.task` (le fichier distant est un `.tflite`, à renommer)

Les tailles et URL sont dans `src/core/modelManager.ts`. Les empreintes SHA-256
sont marquées `PENDING` tant qu'elles n'ont pas été calculées sur une machine
connectée : aucune fausse garantie d'intégrité n'est affichée.
