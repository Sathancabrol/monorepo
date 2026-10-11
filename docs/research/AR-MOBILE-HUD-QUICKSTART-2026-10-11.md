# Dossier — AR mobile immédiate et HUD modulaire
Date : 2026-10-11
Statut : pistes archivées ; prototype à tester sur téléphone.
Priorité : P0 — obtenir gratuitement une expérience HUD/AR mobile utilisable rapidement, puis connecter les modules du monorepo.

## Objectif
Utiliser la caméra et les capteurs du smartphone pour afficher une interface configurable : couches activables, données contextuelles, notes et raccourcis. Connecter progressivement Watchtower, Atlas Frontignan, BTP, Cognitorium et Nexus. Ce dossier complète les listes de recherche existantes ; il ne remplace aucun projet et n'importe pas de code tiers.

## Démarrage le plus rapide
1. **Essai HUD mobile** : ouvrir https://github.com/xTech5x/AR-HUD et suivre le lien de démo/déploiement indiqué dans le README si disponible. Le projet se présente comme un HUD/PWA installable : carte/bâtiments OSM via OpenFreeMap, GPS/vitesse/cap, batterie/réseau, météo/qualité de l'air et scan caméra avec modèle de détection d'objets. Certaines fonctions sont estimées ou démonstratives (pas des mesures garanties). Internet requis pour certaines couches.
2. **Démo AR géolocalisée sans installation** : ouvrir https://gps.csutil.com/ dans Chrome sur Android et choisir « Wayfinding HUD Demo » ou « OpenStreetMap Demo ». C'est un essai rapide de superpositions/waypoints, pas encore l'app personnalisée intégrée aux modules.
3. Si l'expérience convient, utiliser « ⋮ > Installer l'application » ou « Ajouter à l'écran d'accueil » dans Chrome lorsque proposé. L'installation PWA dépend du déploiement HTTPS, du manifeste, du service worker et du navigateur. La caméra/capteurs doivent être autorisés explicitement.
4. Pour placer des objets 3D dans une pièce plutôt que des informations GPS, tester https://github.com/sergidomenechguzy/app-ar-viewer ou AR.js : WebXR et l'AR immersive ne fonctionnent pas uniformément sur tous les téléphones.
5. **Ne pas prétendre que l'app est déjà connectée à nos modules** : les connecteurs sont une étape de développement à part.

## Inventaire des ressources
| Ressource | Usage potentiel | Décision / vigilance |
|---|---|---|
| https://github.com/xTech5x/AR-HUD | HUD mobile/PWA, capteurs, carte, météo, scan caméra | Premier candidat à tester ; distinguer réel, estimé, démo et indisponible ; vérifier lien déployé, licence et dépendances |
| https://gps.csutil.com/ | WebAR géolocalisée, wayfinding HUD, ancres QR, points OSM | Démo rapide sans installation ; mesurer la précision réelle et vérifier licence/compatibilité |
| https://github.com/AR-js-org/AR.js | AR web par marqueur/image et localisation | Bibliothèque candidate ; vérifier version, API et cas d'usage |
| https://github.com/sergidomenechguzy/app-ar-viewer | PWA AR-Viewer, objets GLTF/GLB, WebXR et fallback 3D | Alternative pour objets 3D ; compatibilité annoncée limitée |
| https://github.com/Nic-Gould/HUD | HUD sur flux vidéo FPV et modules de vision | Référence historique seulement ; audit vie privée/sécurité impératif |
| https://github.com/fayazara/robot-heads | Têtes animées avec états d'agent | Piste pour afficher écouter/réfléchir/rechercher/travailler/erreur ; vérifier licence |
| https://github.com/GNeironiAR/scouterHUD | Écosystème HUD matériel + app téléphone, QR, MQTT et données d'appareils | Piste complémentaire prometteuse ; ce n'est pas une app AR caméra équivalente, vérifier dépendances, matériel, sécurité et licence |
| https://repodir.com/repo/0x4m4-hexstrike-ai | Piste d'outillage agentique/sécurité | Identifier le dépôt canonique et auditer capacités, licence et risques avant usage |
| https://github.com/agent-infra/sandbox | Sandbox Docker navigateur/shell/fichiers/VS Code/Jupyter/MCP | À envisager pour agents isolés seulement ; authentification, localhost, réseau limité, versions épinglées ; ne pas exposer publiquement |
| https://github.com/cporter202/stock-market-signal-automation | Exemples de webhooks/alertes orientés événements | Réutiliser éventuellement les motifs génériques, pas comme moteur prédictif complet |
| https://github.com/cporter202/google-maps-scraping-apis | Catalogue d'acteurs Apify pour cartes/avis/contacts | Secondaire ; coût, conditions d'utilisation, protection des données et provenance à vérifier ; privilégier OSM et données officielles ouvertes |
| https://github.com/awesome-selfhosted/awesome-selfhosted | Catalogue de logiciels auto-hébergeables | Source de découverte, pas une dépendance à fusionner |
| https://github.com/tektrip-biggles/BB-WebAR-experiments | Expériences AR web | Référence technique ; vérifier maintenance/licence avant usage |
| https://github.com/liyasthomas/lvr | Framework WebAR/VR ancien basé sur AR.js/A-Frame | Référence historique, pas choix par défaut |
| https://github.com/damiansire/web-ar-hand-tracking | Suivi des mains et figures 3D en navigateur | Démonstrateur spécialisé, non HUD territorial |
| https://github.com/8thwall/8thwall | Outils AR/3D open source | Vérifier chaque licence, notamment les composants binaires |
| https://arsynth.cc/ | Création/partage de scènes AR web | Alternative de publication de scènes, pas nécessairement base du HUD |
| Recherche Brave Images « AR-HUD » | Inspirations visuelles : Ghost Recon Future Soldier / Anduril | Référence de design uniquement, pas preuve de capacités |

## Architecture cible
- **Shell PWA mobile** : caméra, permissions explicites, navigation, réglages, mode dégradé/hors ligne.
- **Couches indépendantes** : carte/lieux ; orientation/GPS ; météo ; notes ; chantier ; territoire ; cognition ; agent/chat. Chaque couche peut être activée ou masquée.
- **Manifeste de module** : `id`, nom, version, données fournies, actions, permissions, endpoint, disponibilité, provenance et confiance.
- **Connecteurs** : Watchtower (sources/alertes/couches géographiques), Atlas Frontignan (commune/Thau/risques/scénarios), BTP (chantiers/phases/observations), Cognitorium (profil/connaissances/mémoire), Nexus (agents/outils/tâches/journal).
- **Mémoire type humaine** : détails dans un stockage indexé ; résumé abstrait cohérent dans le contexte actif ; decay de pertinence ; récupération à la demande par source/identifiant ; rien ne disparaît silencieusement.
- **Provenance visible** : chaque élément doit indiquer s'il s'agit d'une mesure du téléphone, d'une donnée externe sourcée, d'une estimation, d'une simulation ou d'une note utilisateur.

## Limites et sécurité
- Un téléphone seul ne voit pas à travers les murs, ne localise pas les réseaux enterrés sans données/instrumentation et ne fournit pas d'imagerie thermique sans capteur dédié.
- GPS et boussole sont variables ; pas de promesse de précision centimétrique.
- Permissions minimales ; caméra/localisation désactivables ; traitement local privilégié.
- Pas d'identification faciale, d'analyse de sentiment ou de profilage des personnes par défaut.
- Pour la sandbox agentique : isoler le code non fiable, authentifier les API, limiter réseau/ressources et journaliser les actions.
- Vérifier licences, dépendances, maintenance, coûts, politiques de données et conditions d'utilisation avant tout fork/import.

## Checklist
### P0 — aujourd'hui
- [ ] Ouvrir la démo AR-HUD ou le Wayfinding HUD sur le téléphone.
- [ ] Tester caméra, GPS, orientation, carte et lisibilité ; noter modèle du téléphone, navigateur et erreurs.
- [ ] Vérifier si l'installation PWA est proposée ; ne pas confondre raccourci web et vraie expérience AR immersive.
- [ ] Distinguer fonctions réelles, estimées, simulées et indisponibles.
### P1 — prototype connecté
- [ ] Ajouter des couches activables et une première source JSON locale.
- [ ] Définir le manifeste commun de modules ; relier une vue de démonstration aux projets existants.
- [ ] Vérifier les licences et dépendances des candidats avant import.
### P2 — intégration maîtrisée
- [ ] Tester AR.js / AR-Viewer sur l'appareil cible.
- [ ] Évaluer ancrage GPS/QR et précision mesurée.
- [ ] Évaluer Robot Heads pour les états d'agents et AIO Sandbox uniquement dans un environnement isolé.
- [ ] Comparer données géographiques ouvertes aux scrapers payants ou soumis à conditions.

## Critères d'acceptation du premier prototype
- Gratuit à l'usage pour le test.
- Caméra et permissions clairement contrôlées.
- Au moins une couche HUD/AR utile.
- Couches activables/désactivables.
- Contenu simulé explicitement étiqueté.
- Installable depuis le navigateur si la PWA et l'appareil le permettent.
- Extensible par registre/adaptateur, sans réécrire le moteur pour chaque module.


## Appareil cible confirmé et pont PC ↔ téléphone
- Téléphone déclaré : Xiaomi Redmi Note 13 5G, modèle 2312DRAABG, Android 15, stockage 256 Go, mémoire annoncée 8+4 Go.
- La FAQ Xiaomi confirme gyroscope, accéléromètre, boussole électronique et capteur de champ magnétique. Cela rend possible un prototype qui lit orientation et champ magnétique via une app native compatible ; la disponibilité exacte dans le navigateur doit être testée. Le modèle n'a pas de baromètre selon la FAQ.
- PC cible : Windows, environnement de développement local déjà utilisé pour le monorepo. Le pont doit d'abord fonctionner sur le réseau local, sans service cloud obligatoire.

### Trois outils distincts (ne pas les confondre)
1. **PWA/HUD** : affiche l'interface AR sur le téléphone ; c'est la priorité produit.
2. **scrcpy** : affiche et contrôle le téléphone depuis Windows par USB ou TCP/IP, sans installer une app dédiée sur Android. Gratuit/open source. Source officielle : https://github.com/Genymobile/scrcpy. Cela aide à tester/présenter la vue mobile sur le PC, mais ne connecte pas à lui seul les modules IA.
3. **LocalSend** : transfère des fichiers entre Windows et Android via réseau local, sans compte ni Internet ; utile pour échanger captures, JSON de configuration et exports. Ce n'est pas un canal de commandes temps réel. https://localsend.org/fr/download

### Pont logiciel à développer pour les modules
- Servir la PWA depuis le PC sur le Wi-Fi local ; le téléphone et le PC doivent être sur le même réseau.
- Le PC expose une API locale avec authentification par jeton court, CORS limité à l'origine de la PWA, schéma JSON validé et journal des actions.
- Les données vont PC → téléphone en lecture seule au début (couches/notes/points). Ajouter les commandes téléphone → PC plus tard, avec liste d'actions autorisées et confirmation explicite pour les actions sensibles.
- Ne pas exposer le serveur de développement ou les endpoints d'agents sur Internet ; éviter d'écouter sur toutes les interfaces sans pare-feu et authentification.
- Pour un premier test sans code : utiliser scrcpy pour refléter le téléphone et LocalSend pour déplacer des fichiers ; ce sont des outils de pont/diagnostic, pas l'intégration finale.

### Checklist appareil
- [ ] Confirmer dans Paramètres > À propos du téléphone le modèle/Android exacts.
- [ ] Ouvrir une démo WebAR dans Chrome et autoriser caméra/localisation seulement si nécessaires.
- [ ] Tester si orientation et boussole sont accessibles et stables dans le navigateur.
- [ ] Comparer une démo HUD GPS avec une démo de placement 3D : ce sont deux catégories d'AR différentes.
- [ ] Connecter le PC via USB pour scrcpy d'abord ; activer le débogage USB uniquement si nécessaire et depuis une source officielle.
- [ ] Tester ensuite le partage Wi-Fi local ; ne pas ouvrir ADB sur un réseau public.


### Pont PC ↔ Redmi : recommandation pratique
- **KDE Connect** (gratuit, open source) : meilleur premier essai pour un pont quotidien téléphone-PC — presse-papiers, notifications, fichiers/liens, télécommande/touchpad, sur Wi-Fi avec chiffrement TLS. Installe-le sur Windows et Android, puis associe les deux appareils sur le même réseau. Sources officielles : https://kdeconnect.kde.org/download.html et https://github.com/KDE/kdeconnect-android.
- **scrcpy** : meilleur pour voir et piloter l'écran du Redmi depuis Windows pendant les tests ; connexion USB recommandée au départ, sans app Android dédiée. Source canonique : https://github.com/Genymobile/scrcpy.
- **LocalSend** : meilleur pour transférer simplement des fichiers sans compte ni Internet : https://localsend.org/fr/download.
- **Pont Cognitorium/Nexus à terme** : la PWA s'ouvre sur le téléphone et consomme une API hébergée sur le PC, sur le réseau local. KDE Connect/scrcpy ne remplacent pas cette API métier ; ils sont des utilitaires de liaison et de test.
- **Précaution** : ne pas activer des commandes distantes générales sur le PC sans nécessité. Avec KDE Connect, n'autoriser que les fonctions nécessaires ; avec scrcpy, n'activer le débogage USB que depuis le PC de confiance et déconnecter le mode TCP/IP après usage.
