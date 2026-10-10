# Creative Toolchain Registry — cahier des charges v0.1

**Statut :** proposition d'architecture, non exécutée en production  
**Branche :** `feat/creative-toolchain-registry`  
**Périmètre :** monorepo Windows-first, intégration progressive de Blender, Unreal Engine, outils créatifs open source et serveurs MCP.

## 1. Objectif

Créer un registre central qui découvre, documente et vérifie les outils créatifs sans installer automatiquement du code tiers. Nexus pourra ensuite s'appuyer sur ce registre pour proposer des installations reproductibles, des mises à jour contrôlées et des diagnostics.

Le registre ne doit pas fusionner les environnements Python/Node des projets existants et ne doit pas remplacer leurs lockfiles.

## 2. Principes obligatoires

- **Audit avant installation** : aucune commande distante ou script tiers ne s'exécute pendant la découverte.
- **Opt-in** : une installation nécessite une action explicite de l'utilisateur.
- **Provenance** : URL canonique, licence déclarée, version/release observée, date de vérification et état de confiance.
- **Compatibilité explicite** : OS, versions de Blender/Unreal, runtime, GPU/RAM si connus.
- **Séparation des environnements** : environnement par outil/serveur quand pertinent; aucune modification du Python global.
- **Reproductibilité** : version ou commit épinglé, empreinte des artefacts quand disponible, journal d'installation.
- **Désinstallation et retour arrière** : prévus dès la conception; ne pas promettre de rollback si l'outil ne le permet pas.
- **Sécurité MCP** : bind local par défaut, liste d'outils autorisés, confirmation pour opérations destructrices, secrets uniquement côté serveur.
- **Aucune dépendance obligatoire au cloud** : le catalogue et les diagnostics de base doivent fonctionner localement.
- **Pas de promesse de parité Adobe** : maturité, licence, limites et état alpha/bêta doivent être affichés séparément.

## 3. Architecture cible

1. **Catalogue statique versionné** : fichiers JSON validés dans le dépôt.
2. **Validateur** : vérifie les champs obligatoires, les identifiants uniques, les URLs et les statuts autorisés.
3. **Scanner local en lecture seule** : détecte les exécutables et versions présents sans modifier le poste.
4. **Planificateur d'installation** : produit un plan explicatif et une liste de changements avant toute exécution.
5. **Exécuteur contrôlé (phase ultérieure)** : lance uniquement les commandes approuvées, avec journal, code de sortie et possibilité d'annulation lorsque techniquement possible.
6. **API/UI FastAPI existante** : exposera ultérieurement le catalogue et l'état local; ne pas exposer de secrets ou de chemins privés dans une UI publique.
7. **Connecteurs** : Blender MCP, Unreal MCP, import/export et gestion d'assets sont des intégrations distinctes; Nexus les orchestre sans supposer qu'ils partagent le même protocole.

## 4. Schéma minimal d'une entrée

- `id`: identifiant stable, en minuscules avec tirets.
- `name`, `category`, `purpose`.
- `source_url`, `license`, `license_status` (confirmed / declared / unknown).
- `maturity` (stable / beta / alpha / experimental / unknown).
- `platforms`, `integrations`, `requirements`.
- `install_methods`: instructions informatives seulement dans cette phase; ne pas les exécuter.
- `security_notes`, `verification_status`, `last_verified`.
- `evidence`: sources vérifiables, et remarques sur les affirmations du mainteneur.

## 5. Candidats initiaux à évaluer

Les projets ci-dessous sont des **candidats non validés**, pas des dépendances approuvées :

- Blender : extensions officielles, serveur MCP officiel, projets communautaires Blender MCP.
- Unreal Engine : plugin/serveur MCP natif ou communautaire, compatibilité à vérifier avec la version installée.
- Pont Blender–Unreal : uniquement après validation des formats, licences et workflow.
- ArtCraft : applications PhotoCraft/VectorCraft/FilmCraft/etc.; vérifier séparément chaque application, licence, releases, maturité et besoins matériels.
- Sloom Studio et autres suites créatives : à garder dans le registre de recherche jusqu'à inspection du code et des builds.
- Genjutsu-OSS : pipeline de transformation vidéo orienté ComfyUI; source déclarée Apache-2.0, mais état actuel limité à une fondation et un pipeline simulé. Voir [la fiche d’intégration Nexus](genjutsu-video-integration.md); ne pas le traiter comme un moteur de production tant que les backends réels et les licences des poids ne sont pas vérifiés.
- Motion Mirror : candidat de transfert de mouvement; contraintes annoncées (~9 GB VRAM / 32 GB RAM pour le backend léger) supérieures au PC cible, licences des poids/LoRA à vérifier.
- Viggle-Animate : modèle de remplacement de personnage publié en septembre 2026; poids sous licence MiniMax H3 Community, exigences GPU élevées et limites reconnues sur lip-sync/plans coupés.
- Maestro : studio vidéo/audio avec orchestration « Director »; licence WanGP Non-Commercial Evaluation, donc pas une base logicielle commerciale sans revue de licence.
- Voir [la veille vidéo IA du 10 octobre 2026](../research/video-ai-landscape-2026-10-10.md) pour la comparaison, les sources et les contraintes matérielles.

Les nombres d'outils, affirmations de compatibilité et annonces de prix sont des déclarations de projet tant qu'ils n'ont pas été reproduits par un test.

## 6. Phases d'implémentation

### Phase A — registre et validation
- JSON versionné.
- Validateur Python sans dépendance tierce.
- Rapport lisible : entrées valides, champs manquants, candidats expérimentaux.
- Tests automatisés sur entrées valides et invalides.

### Phase B — inventaire local en lecture seule
- Détecter Blender, Unreal, Python, Node et versions sans lancer d'installation.
- Ne pas lire ni afficher les secrets.
- Signaler les résultats inconnus plutôt que deviner.

### Phase C — plan d'installation
- Générer un plan avec les changements attendus, téléchargements, licences et espace disque estimé si connu.
- Exiger confirmation avant exécution.
- Refuser les commandes arbitraires fournies par des métadonnées distantes.

### Phase D — exécution et UI
- Exécuteur à liste d'autorisation, journal structuré et gestion d'erreurs.
- API FastAPI et UI du monorepo.
- Installation/désinstallation sur bac à sable avant toute intégration utilisateur.

## 7. Critères d'acceptation

- La validation ne fait aucun accès réseau et n'exécute aucun outil tiers.
- Un catalogue mal formé retourne une erreur non nulle avec un message exploitable.
- Les IDs dupliqués sont détectés.
- Les statuts inconnus ne sont pas silencieusement convertis en « stable ».
- Aucun outil n'est installé par défaut.
- Le rapport distingue clairement « déclaré par le mainteneur », « vérifié sur source » et « testé localement ».
- Tests reproductibles depuis Windows et CI Python standard.

## 8. Hors périmètre de cette première version

- Télécharger ou installer automatiquement des logiciels.
- Exécuter un MCP ou un script Python tiers.
- Modifier des projets Blender/Unreal existants.
- Installer des modèles IA lourds ou des assets commerciaux.
- Garantir une équivalence fonctionnelle à Adobe.
- Déployer l'application sur Internet.

## 9. Décisions techniques provisoires

- Python standard library pour le validateur initial.
- JSON versionné pour le catalogue.
- FastAPI existant comme intégration future, après vérification de la structure et des tests.
- Aucun nouveau service en arrière-plan tant qu'un besoin mesuré ne le justifie pas.
