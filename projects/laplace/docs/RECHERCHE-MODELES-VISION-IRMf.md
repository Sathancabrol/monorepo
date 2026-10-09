# Recherche — modèles de vision, webcam et IRMf pour LAPLACE

**État :** veille technique, aucun modèle intégré ni poids téléchargé.
**Recherche effectuée le :** 9 octobre 2026.
**Portée :** modèles pré-entraînés pertinents pour l’analyse d’images/selfies, la caméra locale, les expressions, l’identité, les scènes, le regard, des indicateurs physiologiques et la charge cognitive; comparaison avec les principes produit de LAPLACE.

> Cette note sert à orienter un choix futur. Elle n’autorise pas l’activation d’une caméra, l’ajout d’une dépendance, le téléchargement de poids ni l’inférence d’un état mental. Toute nouvelle capacité reste soumise à une décision explicite du propriétaire.

## Synthèse

- Il existe des modèles locaux assez légers pour **détecter un visage, repérer des points du visage, détecter des objets et classer des scènes**. Ces tâches sont les plus compatibles avec une analyse ponctuelle et consentie.
- Des modèles pré-entraînés classent aussi des **mouvements ou configurations du visage** et estiment le **regard**. Ils ne mesurent pas directement ce que la personne ressent, comprend ou regarde avec attention.
- Il n’a pas été établi qu’il existe un modèle webcam universel, prêt à intégrer et suffisamment validé pour déduire de façon fiable l’humeur ou la charge cognitive d’une personne. Les résultats les plus intéressants nécessitent une tâche définie, des annotations et souvent une calibration personnelle.
- Les modèles d’IRMf, dont BrainLM, reçoivent des signaux issus d’un scanner et d’un prétraitement neuro-imagerie. Ils ne peuvent pas analyser une photo ou une vidéo webcam sans un nouveau modèle appris sur des données appariées IRMf–vidéo.
- **Choix de recherche recommandé :** si LAPLACE reçoit de nouvelles fonctions visuelles, commencer par des observations locales et explicites (repères faciaux non identifiants, objets, éventuellement scène). Ne pas activer la reconnaissance d’identité ou les affirmations automatiques d’émotion/charge cognitive.

## État du dépôt et contexte LAPLACE

- `projects/laplace/` permet actuellement de faire analyser une **image jointe explicitement** avec `/analyser_image`, si un modèle vision est configuré. La réponse est éphémère; la commande ne place pas l’image dans l’archive ou la mémoire.
- LAPLACE **n’active pas de caméra** et aucun modèle de webcam/facial, checkpoint ou poids d’IRMf n’est inclus dans le dépôt.
- `projects/watchtower/` possède des mesures heuristiques de lumière et de mouvement à basse résolution. Il ne s’agit pas de reconnaissance d’identité, d’émotions, de scènes ou de charge cognitive. Les règles du projet excluent notamment la recherche de personnes nommées et la reconnaissance faciale.
- Des références bibliographiques ou de catalogue à OpenFace, PyGaze, SPM, FSL, AFNI, fMRIPrep et Nilearn ne signifient pas que ces outils ou des poids de modèle sont intégrés dans LAPLACE.
- La machine Ollama du propriétaire, les modèles vision installés, le système d’exploitation, la RAM et la VRAM ne sont pas connus. Les performances et la compatibilité doivent donc être mesurées sur le PC cible avant toute décision.

## Modèles webcam et vision

### 1. Visage, repères et mouvements descriptifs — adéquation élevée

**MediaPipe Face Landmarker** peut analyser des images ou une séquence vidéo et renvoyer des repères faciaux 3D, des coefficients de mouvements (`blendshapes`) et des matrices de transformation. Cela fournit une géométrie utile pour cadrage, position et mouvements observables; ce n’est pas une identification biométrique ni une lecture du ressenti. Le modèle peut être utilisé dans un pipeline local si ses ressources sont installées localement.

**YuNet**, du modèle zoo OpenCV, est un détecteur de visages très léger : le fichier ONNX publié est d’environ 227 Ko et les fichiers de ce modèle sont sous licence MIT. Il localise des visages, sans répondre à la question « qui est cette personne ? ».

**Intérêt pour LAPLACE :** repérer qu’un visage est dans l’image, vérifier le cadrage, produire des observations visuelles simples. Si une nouvelle capacité est retenue, MediaPipe ou YuNet sont de meilleures premières pistes que des modèles d’émotion ou d’identité.

Sources : [MediaPipe Face Landmarker](https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker), [YuNet dans OpenCV Zoo](https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet).

### 2. Objets et scènes — adéquation bonne, selon la question

**EfficientDet-Lite0** est le modèle de détection d’objets recommandé par MediaPipe dans sa documentation. Il traite des images 320 × 320 et des classes COCO (80 types d’objets); une version INT8 est disponible. Le benchmark publié par Google donne environ 29 ms sur CPU pour cette version, chiffre indicatif qui ne garantit pas les performances sur le PC du propriétaire. **SSD MobileNetV2** est une option plus rapide/légère au prix d’une précision généralement plus faible. Ces détecteurs disent quels objets apparaissent, pas ce que la scène signifie pour la personne.

**Places365** est un véritable classifieur de scènes, avec 365 catégories et plusieurs architectures dont ResNet18. La variante Places365 ResNet18 est également empaquetée par IBM MAX. Les poids pré-entraînés Places365 sont indiqués sous **CC BY** : il faut prévoir attribution et vérifier les conditions applicables au modèle effectivement choisi. ResNet18 est une option plus lourde qu’un petit détecteur d’objets.

**Intérêt pour LAPLACE :** si le besoin est « quels objets visibles ? », essayer d’abord le détecteur léger. Si le besoin est « quel type d’environnement semble apparaître ? », évaluer Places365 séparément et ne montrer que des catégories approximatives, avec confiance et incertitude.

Sources : [Guide MediaPipe Object Detector](https://ai.google.dev/edge/mediapipe/solutions/vision/object_detector), [guide Python et fichier de modèle local](https://ai.google.dev/edge/mediapipe/solutions/vision/object_detector/python), [Places365](https://github.com/CSAILVision/places365), [IBM MAX Scene Classifier](https://github.com/IBM/MAX-Scene-Classifier).

### 3. Expressions et émotions — expérimental, à ne pas présenter comme lecture de l’état intérieur

**EmotiEffLib** (ancien HSEmotion) fournit des modèles de reconnaissance d’expressions faciales, avec des interfaces Python/C++ et des backends PyTorch/ONNX. Son README rapporte pour `mobilenet_7.h5` une taille de 14 Mo, une inférence de 16 ± 5 ms sur un Samsung Fold 3/Qualcomm 888 et une exactitude de 64,71 % sur AffectNet à 7 classes. Ce sont des mesures de benchmark sur les jeux de données et conditions rapportés par le projet, pas un taux de réussite dans une conversation réelle.

Point de vigilance : le README indique que les modèles ont été pré-entraînés pour l’identification faciale sur VGGFace2 avant leur entraînement aux tâches d’expression. Cela ne signifie pas que ce modèle renvoie une identité, mais mérite d’être pris en compte. La licence Apache-2.0 du code ne doit pas être assimilée sans vérification à une licence identique pour chaque poids ou jeu de données.

La revue de Barrett et ses collègues conclut que les mouvements faciaux ne sont pas des marqueurs universels, suffisamment fiables et spécifiques, des états émotionnels. Une description comme « configuration faciale » ou « mouvement apparent » est plus défendable qu’une certitude telle que « tu es triste » ou « tu es en colère ».

**Intérêt pour LAPLACE :** ne pas activer par défaut. Si le propriétaire demande une expérimentation ultérieure, la présenter comme une classification incertaine de l’apparence, sans la mémoriser comme un fait sur la personne et sans en déduire humeur, intention ou santé.

Sources : [EmotiEffLib](https://github.com/sb-ai-lab/EmotiEffLib), [Barrett et al., *Emotional Expressions Reconsidered*](https://pmc.ncbi.nlm.nih.gov/articles/PMC6640856/).

### 4. Identité faciale — techniquement disponible, inadéquat par défaut

Il faut distinguer **détection de visage** (localiser un visage) et **reconnaissance d’identité** (comparer ou associer un visage à une personne). YuNet n’identifie pas. **SFace** offre un modèle de reconnaissance faciale dans OpenCV Zoo dont les fichiers sont annoncés sous Apache 2.0. **InsightFace** fournit des modèles plus larges : `buffalo_s` fait environ 159 Mo; le dépôt distingue la licence MIT du code et les restrictions **recherche non commerciale uniquement** des poids pré-entraînés.

Une licence ouverte ne rend pas l’identification nécessaire ou souhaitable. L’identification implique enrôlement de visages, comparaison biométrique et possibilité de faux rapprochements. Elle ne répond pas au besoin initial de selfie/personnalisation de LAPLACE et est exclue par défaut.

Sources : [SFace dans OpenCV Zoo](https://github.com/opencv/opencv_zoo/tree/main/models/face_recognition_sface), [licence et zoo de modèles InsightFace](https://github.com/deepinsight/insightface/blob/master/python-package/README.md).

### 5. Regard — mesure instrumentale approximative, pas mesure d’attention

**GazeFollower** est un système Python de suivi du regard par webcam avec calibration et enregistrement. Le dépôt contient un modèle indiqué comme entraîné sur 7 millions d’images; l’accès au modèle de base 32 millions d’images demande un contact et est décrit pour la recherche académique. Le dépôt porte une licence **CC BY-NC-SA 4.0**. L’article de 2025 évalue le système sur 31 personnes et annonce un suivi jusqu’à 60 Hz; cet échantillon et les conditions de l’étude ne constituent pas une garantie de précision sur une webcam quelconque. Le suivi peut être perturbé par les mouvements de tête ou les changements importants d’éclairage, et nécessite calibration.

Autre piste : **OpenVINO `gaze-estimation-adas-0002`**, dont la fiche indique 1,882 million de paramètres et 0,139 GFLOPs. Mais la démo complète s’appuie aussi sur des modèles de détection de visage, de pose de tête et de repères faciaux. Il s’agit d’une chaîne de modèles orientée ADAS, pas forcément de l’intégration la plus simple pour LAPLACE; licence et données d’entraînement doivent être vérifiées pour tout usage envisagé.

**Intérêt pour LAPLACE :** éventuellement estimer vers quelle zone de l’écran le propriétaire regarde, après calibration volontaire sur le compagnon local. Ne jamais convertir automatiquement cette sortie en « attentif », « distrait », « comprend » ou « consent »; ne pas conserver de trajectoire oculaire par défaut.

Sources : [GazeFollower — dépôt et licence](https://github.com/GanchengZhu/GazeFollower), [article GazeFollower](https://dl.acm.org/doi/10.1145/3729410), [modèles Intel Open Model Zoo](https://github.com/openvinotoolkit/open_model_zoo/blob/master/models/intel/index.md), [démo OpenVINO du pipeline](https://github.com/openvinotoolkit/open_model_zoo/blob/master/demos/gaze_estimation_demo/cpp/README.md).

### 6. Charge cognitive — aucun modèle webcam universel prêt à intégrer identifié

La piste la plus récente repérée est un préprint arXiv de mars 2026, *Facial Movement Dynamics Reveal Workload During Complex Multitasking*. Il étudie 72 personnes dans une simulation multitâche définie et utilise OpenPose pour extraire des points du visage/de la tête, puis des caractéristiques cinématiques et des modèles Random Forest. Le préprint rapporte environ 43 % en validation croisée entre participants, pour un hasard à 33 %. Les modèles personnalisés commencent autour de 50 % après une calibration de deux minutes par condition et atteignent des valeurs supérieures avec plus de calibration (jusqu’à 73 % rapportés). Ces chiffres sont propres à la tâche, au protocole et aux partitions de l’étude; le travail ne constitue pas un classifieur universel pré-entraîné à déployer sur n’importe quelle webcam.

**COLET** est un jeu de données de suivi oculaire de 47 personnes qui ont effectué des tâches de recherche visuelle; les évaluations de charge reposent notamment sur des questionnaires remplis après les activités. Le dépôt **SaccadeFormer** utilise ce type de données, mais décrit une classe de forte charge extrêmement rare (une seule séquence originale issue d’un participant) et l’absence d’exemples de cette classe dans les partitions de validation/test sous séparation stricte des personnes. Son README contient aussi un emplacement de métrique non vérifiée. Il ne faut pas le traiter comme un modèle de production validé. Un autre prototype, **Cognitive-State-Estimation**, indique lui-même que ses modèles ne se généralisent pas entre participants.

**Conclusion LAPLACE :** privilégier le ressenti déclaré volontairement par le propriétaire ou un retour explicitement associé à une tâche. Si une étude personnalisée est souhaitée plus tard, elle devrait définir les tâches, les étiquettes de référence, la calibration et les règles de rétention avant de construire un classifieur local. Pas d’estimation par défaut d’un état mental à partir d’un selfie.

Sources : [préprint complet de 2026](https://arxiv.org/html/2603.17767), [résumé arXiv](https://arxiv.org/abs/2603.17767), [COLET — article sur le jeu de données](https://www.sciencedirect.com/science/article/pii/S0169260722003716), [SaccadeFormer](https://github.com/RamaChandraMurthyMamidipalli/Cognitive-Load-Estimation-using-Event-Level-Eye-Movement), [Cognitive-State-Estimation](https://github.com/j-holub/Cognitive-State-Estimation).

### 7. Pouls vidéo (rPPG) — capacité différente, très facultative

Le **rPPG-Toolbox** regroupe des algorithmes classiques et des réseaux pré-entraînés (notamment TS-CAN, PhysNet et EfficientPhys) qui tentent d’estimer un signal de pouls/une fréquence cardiaque à partir d’une vidéo du visage. Les résultats dépendent du mouvement, de la lumière et des données d’évaluation; les performances ne se transfèrent pas nécessairement de la même façon entre jeux de données. Le projet annonce une licence **Responsible AI**; vérifier les conditions de chaque poids avant toute distribution.

Une estimation du pouls n’est pas une mesure de stress, d’émotion ou de charge cognitive. Elle impliquerait le traitement de données physiologiques et devrait exiger un consentement séparé, rester locale, être ponctuelle et ne pas être conservée par défaut.

Sources : [rPPG-Toolbox](https://github.com/ubicomplab/rPPG-Toolbox), [article et évaluations du toolbox](https://ubicomplab.cs.washington.edu/pdfs/rppg-toolbox.pdf).

## Modèles entraînés sur l’IRMf

**IRM et IRMf ne désignent pas la même entrée de modèle.** L’IRM structurelle est une image anatomique du cerveau; l’IRMf suit un signal fonctionnel BOLD au cours du temps, qui nécessite acquisition et prétraitement. Les modèles ci-dessous ne reçoivent pas une image de webcam.

| Modèle | Entrée et apprentissage | Ce que cela signifie pour LAPLACE |
|---|---|---|
| **BrainLM** | Modèle de fondation sur des séries temporelles d’IRMf UK Biobank/HCP, annoncées à environ 6 700 heures. Utilise un atlas de 424 régions; poids de 111 M et 650 M de paramètres. Les poids sont disponibles sur Hugging Face; l’accès aux données UK Biobank est soumis à des conditions d’accès. La fiche du modèle indique explicitement une formation/évaluation sur IRMf; les poids y sont marqués CC BY-NC-ND 4.0. | Modèle de recherche IRMf, avec prétraitement et entrée par régions cérébrales. Ni modèle selfie, ni outil local léger de webcam, ni diagnostic autonome. La variante 650 M est particulièrement éloignée de l’objectif d’un petit module caméra. |
| **fm-MAE** | Modèle de fondation MedARC d’environ 89 M de paramètres, pré-entraîné sur des données HCP-YA représentées en « flat maps »; poids annoncés en deux configurations. | Reste un modèle IRMf qui attend ses représentations d’entrée spécifiques. Licence des poids à vérifier avant usage ou redistribution. |
| **CortexMAE** | Famille MedARC annoncée comme pré-entraînée sur environ 2 100 heures HCP; checkpoints avec plusieurs représentations (flat map, parcelles, volume). | Piste de recherche IRMf récente, toujours non applicable à une image webcam. Vérifier la licence et les exigences d’inférence du checkpoint retenu. |
| **fMRI-LM** | Travail récent d’alignement de l’IRMf et du langage. | Un alignement entre deux modalités ne supprime pas le besoin d’une entrée IRMf; aucune brique webcam LAPLACE n’en découle. La disponibilité d’un checkpoint prêt à intégrer n’a pas été confirmée dans cette recherche. |
| **MindEye2** | Recherche de reconstruction d’images à partir d’activité IRMf, avec adaptation par sujet. | Va de l’activité cérébrale vers des représentations/images; ne transforme pas la webcam en scanner et n’analyse pas directement une photo selfie. |

Un modèle IRMf pré-entraîné ne peut pas être « branché » à une webcam. Un pont caméra–IRMf demanderait des vidéos synchronisées avec les acquisitions IRMf, des annotations/une cible précises, un modèle entraîné pour cette correspondance et une validation indépendante. Même alors, un résultat appris dans un protocole de recherche ne démontrerait pas une capacité générale à lire l’état mental d’une personne.

Sources : [BrainLM GitHub](https://github.com/vandijklab/BrainLM), [fiche Hugging Face BrainLM](https://huggingface.co/vandijklab/brainlm), [MedARC fm-MAE](https://github.com/MedARC-AI/fmri-fm), [MedARC CortexMAE](https://github.com/MedARC-AI/CortexMAE), [article fMRI-LM (CVPR 2026)](https://openaccess.thecvf.com/content/CVPR2026/papers/Wei_fMRI-LM_Towards_a_Universal_Foundation_Model_for_Language-Aligned_fMRI_Understanding_CVPR_2026_paper.pdf), [MindEye2](https://medarc-ai.github.io/mindeye2/).

## Comparaison aux objectifs et garde-fous produit

Les décisions de LAPLACE sont local-first, consentement explicite, photo envoyée d’abord, capture ponctuelle future par compagnon avec confirmation visible, et API externe désactivée par défaut indépendamment pour chaque capacité. La mémoire personnelle/partagée reste séparée; une analyse ponctuelle d’image ne doit pas créer un souvenir ou un enregistrement automatique.

### Ordre recommandé si le propriétaire demande ensuite un prototype

1. **Conserver le parcours actuel** : image choisie par l’utilisateur, analyse par le modèle vision local configuré, réponse éphémère.
2. **Ajouter éventuellement des mesures visuelles descriptives** : cadrage/repères avec MediaPipe ou détection de visage YuNet; objets avec EfficientDet-Lite0/SSD MobileNetV2. Garder les modèles et l’inférence sur l’appareil si cette capacité est sélectionnée.
3. **Tester la scène si elle répond à un besoin concret** : Places365, sans prétendre identifier une situation privée à partir d’une catégorie approximative.
4. **Réserver regard, expression et rPPG à des options distinctes** avec explication des limites, consentement séparé, bouton d’arrêt et aucune conservation par défaut. Vérifier les licences des poids avant toute distribution.
5. **Ne pas inclure la reconnaissance d’identité ou l’inférence automatique de charge mentale/émotions dans le MVP.** Pour la charge cognitive, demander plutôt une indication volontaire et contextuelle; une expérience de calibration personnelle serait une fonctionnalité de recherche séparée.

### Contraintes d’implémentation si une option est autorisée

- Capture par action explicite, témoin visuel clairement actif et confirmation au moment de la capture; jamais de caméra silencieuse/en arrière-plan.
- Modèles/version/licences identifiés; poids téléchargés séparément, non ajoutés au dépôt Git sans nécessité.
- API externe désactivée tant que le propriétaire n’a pas opté pour cette capacité précise; avertissement avant l’envoi d’une image ou d’un signal physiologique hors du PC.
- Sorties formulées comme des observations ou probabilités, avec incertitude; ne pas enregistrer automatiquement des interprétations dans la mémoire personnelle ou partagée.
- Tester le fonctionnement, la latence, la qualité et les échecs sur le PC réel, différentes lumières, distances, lunettes et positions; aucun benchmark publié ne remplace cette validation.

## Références de recherche supplémentaires

- Visage : [MediaPipe Face Landmarker](https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker), [OpenCV Zoo YuNet](https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet), [EmotiEffLib](https://github.com/sb-ai-lab/EmotiEffLib), [revue sur l’inférence d’émotion depuis les mouvements faciaux](https://pmc.ncbi.nlm.nih.gov/articles/PMC6640856/).
- Objets/scènes : [MediaPipe Object Detector](https://ai.google.dev/edge/mediapipe/solutions/vision/object_detector), [Places365](https://github.com/CSAILVision/places365), [IBM MAX Scene Classifier](https://github.com/IBM/MAX-Scene-Classifier).
- Identité/regard : [InsightFace — licence des modèles](https://github.com/deepinsight/insightface/blob/master/python-package/README.md), [SFace](https://github.com/opencv/opencv_zoo/tree/main/models/face_recognition_sface), [GazeFollower](https://github.com/GanchengZhu/GazeFollower), [OpenVINO Open Model Zoo](https://github.com/openvinotoolkit/open_model_zoo).
- Charge cognitive : [préprint webcam 2026](https://arxiv.org/abs/2603.17767), [COLET](https://www.sciencedirect.com/science/article/pii/S0169260722003716), [SaccadeFormer](https://github.com/RamaChandraMurthyMamidipalli/Cognitive-Load-Estimation-using-Event-Level-Eye-Movement), [Cognitive-State-Estimation](https://github.com/j-holub/Cognitive-State-Estimation).
- Physiologie : [rPPG-Toolbox](https://github.com/ubicomplab/rPPG-Toolbox) et son [article d’évaluation](https://ubicomplab.cs.washington.edu/pdfs/rppg-toolbox.pdf).
- IRMf : [BrainLM](https://github.com/vandijklab/BrainLM), [fm-MAE](https://github.com/MedARC-AI/fmri-fm), [CortexMAE](https://github.com/MedARC-AI/CortexMAE), [fMRI-LM](https://openaccess.thecvf.com/content/CVPR2026/papers/Wei_fMRI-LM_Towards_a_Universal_Foundation_Model_for_Language-Aligned_fMRI_Understanding_CVPR_2026_paper.pdf), [MindEye2](https://medarc-ai.github.io/mindeye2/).
