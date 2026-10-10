# Veille vidéo IA — 10 octobre 2026

**Périmètre :** dépôts publics consultés et annonces de recherche récentes; aucun logiciel installé, aucun modèle téléchargé, aucun benchmark local effectué.
**Objectif :** choisir les briques vidéo pertinentes pour Nexus en tenant compte de la configuration locale connue (Windows, GTX 1060 6 GB VRAM, RAM 16 GB).

## Synthèse décisionnelle

- **Genjutsu-OSS** reste une bonne référence d’architecture et une fondation de test, mais son pipeline réel de génération n’est pas implémenté : le test CPU copie l’entrée.
- **Viggle-Animate** est la nouvelle piste la plus proche du remplacement de personnage observé dans la vidéo. La publication du 4 septembre 2026 décrit un modèle de remplacement à partir d’une seule frame repeinte. Les performances annoncées (124 frames en 26 secondes) sont rapportées sur un GPU B200; ce n’est pas une promesse de performance sur une carte grand public.
- **Motion Mirror** propose un pipeline local plus complet : détourage, pose corporelle 133 points, génération Wan2.1-VACE et passage de l’audio. Cependant, le README annonce environ 9 GB de VRAM et 32 GB de RAM au minimum pour son backend le plus léger. Il ne correspond donc pas à la machine locale actuelle sans évolution matérielle ou calcul distant.
- **Maestro** offre une interface de studio et une orchestration « Director » pour planifier des plans, générer des images/clips et assembler des séquences. Son dépôt déclare une licence WanGP Non-Commercial Evaluation License 1.1 : à ne pas adopter comme fondation d’un produit commercial sans revue et autorisation appropriée.
- **Blender MCP officiel** est désormais une piste concrète pour l’atelier 3D, mais sa documentation exige Blender 5.1+ et avertit que le serveur exécute du code généré par le LLM sans garde-fous. Il doit être isolé et restreint, jamais branché directement sur les fichiers sensibles.

## État des dépôts

### Genjutsu-OSS
Source : https://github.com/Tschuki/genjutsu-oss

- Le dépôt public est petit et expérimental; le commit consulté le plus récent date du 2 octobre 2026.
- Code source déclaré Apache-2.0.
- Contrats de données et interfaces de providers déjà présents; nœuds ComfyUI de base disponibles.
- Le pipeline CPU de démonstration est simulé et copie la vidéo d’origine.
- Les backends réels de génération, segmentation, pose, profondeur, stabilisation temporelle et export de production sont encore listés comme non implémentés.
- Conclusion : réutiliser les contrats et le découpage par étapes comme référence d’architecture; ne pas considérer le dépôt comme un éditeur vidéo utilisable en production.

### Motion Mirror
Source : https://github.com/halli75/motion-mirror

- Projet local-first avec CLI, API Python, UI web et nœuds ComfyUI.
- Pipeline décrit : image du personnage + vidéo de mouvement → segmentation → pose 133 points → génération Wan2.1-VACE → audio.
- Le README annonce environ 9 GB VRAM, 32 GB RAM et 20 GB de cache modèle pour le backend 1.3B; backend 14B plus exigeant.
- Le code du dépôt est annoncé MIT, mais les poids/LoRA ont leurs propres licences. L’artefact rapide 1.3B est annoncé CC-BY-NC-SA-4.0 (non commercial).
- Conclusion : excellente référence de workflow et candidat à tester sur un poste plus puissant ou un worker distant contrôlé; pas une cible d’installation immédiate sur 6 GB VRAM / 16 GB RAM.

### Viggle-Animate
Sources :
- https://viggle.ai/research/viggle-animate-character-replacement-from-a-repainted-frame
- https://huggingface.co/Viggle/Viggle-Animate

- Publication datée du 4 septembre 2026.
- Remplacement d’un personnage à partir de la vidéo source et d’une seule frame de cette vidéo, repeinte dans un éditeur d’image.
- La recherche affirme que l’inférence vidéo n’a pas besoin de pose, segmentation, suivi facial ou prompt textuel; les attributs de la frame de référence conditionnent le résultat.
- Le fournisseur annonce 124 frames en 26 secondes sur un GPU B200 et une comparaison 6,1 fois plus rapide que Wan2.2-Animate-14B dans les conditions décrites.
- Limites reconnues : synchronisation labiale faible, plans coupés, interactions complexes et multi-personnages.
- Le code d’inférence est annoncé Apache-2.0; les poids dérivés de MiniMax H3 relèvent de la MiniMax H3 Community License.
- Conclusion : piste prioritaire pour une intégration future de remplacement de personnage, mais seulement après vérification des poids, de la licence et de la faisabilité matérielle. Les chiffres du B200 ne sont pas extrapolables au GPU local.

### Maestro
Source : https://github.com/chitaodu-pixel/maestro

- Studio d’images, vidéo et audio; mode Director pour analyser une piste audio ou un scénario, planifier des plans, générer des images et clips, puis assembler le résultat.
- L’historique consulté montre la version 1.9.1 au 25 août 2026.
- Le fichier LICENSE du dépôt déclare WanGP Non-Commercial Evaluation License 1.1 et interdit notamment la distribution payante du logiciel ou sa fourniture comme service commercial.
- Conclusion : s’inspirer de l’UX d’orchestration, mais ne pas intégrer le logiciel comme dépendance produit sans clarifier la licence. Les licences des modèles et poids doivent aussi être auditées séparément.

### Blender MCP officiel
Source : https://www.blender.org/lab/mcp-server/

- Documentation officielle : Blender 5.1 ou plus récent, add-on, client LLM et serveur MCP.
- La page précise que le serveur exécute du code généré par le LLM sans garde-fous contre la suppression de données ou l’envoi vers un emplacement distant.
- Conclusion : intégration à travers l’orchestrateur Nexus, avec environnement isolé, bind local, liste d’outils autorisés, répertoire de travail dédié, confirmation des opérations destructrices et journalisation. Ne pas exposer les secrets ni les dossiers personnels au processus Blender.

## Audit des dépôts de l’utilisateur

Dépôts GitHub accessibles consultés :
- monorepo : branche main au commit 988b86d (7 octobre 2026); branche feat/creative-toolchain-registry basée sur ce commit et en avance de 7 commits, sans retard par rapport à main au moment de la comparaison.
- animation-chronos : dernière activité consultée le 2 septembre 2026; application React/Vite autonome, avec progression narrative, hotspots d’inspection, contrôles d’observation et audio. C’est un pattern UX réutilisable, pas un moteur vidéo.
- watchtower : dernière activité consultée le 7 septembre 2026; le sous-projet embarqué est un globe d’intelligence géospatiale Cesium, sans lien direct nécessaire avec la génération vidéo.
- COGNITORIUM : dernière activité consultée le 6 septembre 2026; documentation qui identifie déjà Animation Chronos comme pattern de découverte progressive.
- proto-cognitorium : dernière activité consultée le 10 septembre 2026.

Le manifeste monorepo est daté du 7 septembre 2026 : il doit être régénéré ou vérifié avant de le traiter comme inventaire exhaustif et à jour.

## Intégration recommandée dans Nexus

1. Garder un catalogue commun, mais séparer explicitement les catégories : « outil d’orchestration », « moteur vidéo réel », « prototype simulé », « service cloud ».
2. Définir un contrat de job média commun : source, durée, timecodes, références, opérations, contraintes à préserver, modèle/version, licence, budget, artefacts, statut et résultats de contrôle qualité.
3. Créer des adaptateurs distincts pour Genjutsu-OSS, Motion Mirror, Viggle-Animate, ComfyUI et Blender MCP. Ne pas lier le cœur de Nexus à un seul backend.
4. Construire d’abord un workflow local sans IA lourde : import, extraction de frames, analyse basique, aperçu, journal, copie/export et reprise sur erreur.
5. Ajouter une vraie génération seulement après une vérification matérielle et une validation de licence.
6. Prévoir le mode worker distant uniquement comme option explicite, avec estimation de coût, transfert de fichiers consenti et suppression des artefacts à la demande.

## Critères de validation

- Les tests de registre passent dans l’environnement du monorepo.
- Le scanner ne télécharge ni n’exécute aucun outil tiers.
- Chaque outil affiche clairement sa maturité, sa licence, son besoin matériel et son état de vérification.
- Les tests simulés sont explicitement étiquetés comme tels.
- Les fichiers sources restent immuables et les opérations sont journalisées.
- Les modèles/poids sont téléchargés seulement après approbation et audit de licence.
- Aucun backend n’est déclaré compatible avec la GTX 1060 6 GB sans test local reproductible.

## Sources consultées

- Genjutsu-OSS README, LICENSE, pyproject.toml, THIRD_PARTY_LICENSES.md et historique GitHub.
- Motion Mirror README et historique GitHub.
- Viggle-Animate recherche et carte modèle Hugging Face.
- Maestro README, LICENSE et historique GitHub.
- Blender Lab MCP Server et rapport d’activité Q1 2026.
- Dépôts accessibles de monorepo, animation-chronos, watchtower, COGNITORIUM et proto-cognitorium.
