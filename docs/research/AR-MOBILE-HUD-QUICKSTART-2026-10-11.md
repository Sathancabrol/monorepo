# Dossier — AR mobile immédiate et HUD modulaire
Date de capture : 2026-10-11
Statut : recherche archivée, prototype à valider sur téléphone
Priorité : P0 — obtenir une expérience AR gratuite et installable rapidement, puis connecter les modules internes.

## Objectif utilisateur
Disposer sur smartphone d'une vue caméra/AR configurable : choisir les couches affichées, ajouter du contenu contextuel, puis connecter progressivement Cognitorium, Watchtower, Atlas Frontignan, Nexus et le module BTP. Préserver les projets sources et ne pas remplacer les listes de recherche existantes : ce dossier est un ajout au catalogue.

## Décision provisoire
1. **Tester d'abord xTech5x/AR-HUD** comme prototype HUD mobile installable (PWA). Le dépôt décrit un fond sombre type jeu, carte/bâtiments OpenStreetMap via OpenFreeMap, GPS/vitesse/cap, batterie, réseau, météo/qualité de l'air, et scan caméra avec modèle de détection d'objets. Certaines vues (tâches, communications, pouls, bruit) sont décrites comme démonstratives/estimées, pas comme mesures garanties. Carte et modèle de scan nécessitent internet ; le shell de l'app peut fonctionner hors ligne.
2. Sur le téléphone, ouvrir le dépôt et suivre ses instructions de déploiement/démo. Si une URL Pages est fournie dans le dépôt, l'ouvrir avec Chrome sur Android, autoriser uniquement les capteurs nécessaires, puis utiliser « Ajouter à l'écran d'accueil » / « Installer l'application » si proposé. **Ne pas supposer que l'URL Pages existe ou que WebXR fonctionne sur tout téléphone avant de vérifier le README et l'appareil.**
3. Si le but prioritaire est de placer des objets 3D dans la pièce plutôt qu'un HUD orienté GPS, évaluer ensuite AR-Viewer PWA et les démos AR.js/location-based AR. Le support WebXR immersif est variable ; Chrome sur Android est le candidat de test principal.
4. Garder une branche d'intégration distincte et ne fusionner aucun code tiers avant audit des licences, dépendances, permissions et données collectées.

## Inventaire des pistes reçues
| Projet / ressource | Rôle possible | Décision / vigilance |
|---|---|---|
| https://github.com/xTech5x/AR-HUD | HUD/PWA smartphone, capteurs, carte, météo, scan caméra | **Premier prototype à tester** ; distinguer réel, estimé et démo ; vérifier URL de déploiement, licence et dépendances |
| https://github.com/Nic-Gould/HUD | HUD sur flux vidéo FPV, modules de vision | Référence historique/architecture seulement ; audit sécurité, dépendances et vie privée avant toute réutilisation |
| https://github.com/AR-js-org/AR.js | AR web basée sur marqueur/image et localisation | Bibliothèque candidate ; valider le cas d'usage et la compatibilité mobile |
| https://github.com/sergidomenechguzy/app-ar-viewer | PWA AR-Viewer, WebXR, objets GLTF/GLB locaux, mode 3D de secours | Alternative si placement d'objets 3D dans l'espace réel est central ; compatibilité annoncée limitée |
| https://gps.csutil.com/ | Démonstrations WebAR ancrées GPS, wayfinding HUD, ancres QR, OSM | Piste de test location-based ; vérifier précision, fonctionnement hors ligne, licence et contraintes appareils |
| https://github.com/fayazara/robot-heads | Têtes de robot 2D/3D stylisées avec états d'agent | Réutilisation visuelle potentielle pour états « écoute / réflexion / recherche / travail / erreur » ; vérifier licence avant intégration |
| https://repodir.com/repo/0x4m4-hexstrike-ai | Piste d'outillage agentique / sécurité à auditer | Ne pas intégrer sans identifier dépôt canonique, fonctionnalités exactes, licence et risques |
| https://github.com/agent-infra/sandbox | Sandbox Docker regroupant navigateur, shell, fichiers, VS Code, Jupyter, MCP | Candidat pour exécuter des outils isolés ; durcissement obligatoire, clé API, liaison localhost, versions épinglées ; ne pas exposer publiquement |
| https://github.com/cporter202/stock-market-signal-automation | Exemple d'automatisation par événements/webhooks | Réutiliser éventuellement les motifs génériques d'événements/alertes, pas comme moteur de prédiction complet |
| https://github.com/cporter202/google-maps-scraping-apis | Catalogue d'acteurs de scraping Google Maps/Apify | Piste secondaire ; coûts, conditions d'utilisation, protection des données et provenance à vérifier. Prioriser OSM/données publiques officielles quand adaptées |
| https://github.com/awesome-selfhosted/awesome-selfhosted | Catalogue de logiciels auto-hébergeables | Source de découverte, pas une dépendance logicielle à fusionner |
| https://github.com/tektrip-biggles/BB-WebAR-experiments | Expériences AR web/AR.js | Référence technique ; vérifier l'état actuel du code avant usage |
| https://github.com/liyasthomas/lvr | Framework WebAR/VR ancien basé sur AR.js/A-Frame | Référence historique, ne pas choisir avant vérification de maintenance |
| https://github.com/damiansire/web-ar-hand-tracking | Détection des mains et figures 3D en navigateur | Démonstrateur spécialisé, pas un HUD territorial général |
| https://github.com/8thwall/8thwall | Outils AR/3D open source | Vérifier précisément les licences des composants, notamment tout composant distribué sous licence binaire |
| https://arsynth.cc/ | Création/partage de scènes AR web | Alternative pour publier des scènes, pas forcément la base du HUD personnel |

Images de référence évoquées : recherche Brave Images pour « AR-HUD » et HUD type Ghost Recon Future Soldier / Anduril. Les images sont des inspirations de design, pas des preuves de capacités techniques.

## Architecture cible à relier au monorepo
- **Shell mobile/PWA** : caméra, état des permissions, navigation, paramètres de couches, mode hors ligne, erreurs visibles.
- **Couche capteurs** : GPS, orientation/boussole, vitesse si disponible, batterie/réseau selon permissions et navigateur. Stocker la source, l'horodatage, la précision et l'état de disponibilité.
- **Moteur de vues** : HUD opérationnel ; carte et points d'intérêt ; vue chantier ; vue territoire ; vue cognition ; panneau agent/chat.
- **Registre de modules** : chaque module fournit un manifeste avec identifiant, nom, icône, données fournies, actions disponibles, permissions, endpoint local/distant, niveau de confiance et état.
- **Connecteurs prévus** :
  - Watchtower : observations, sources OSINT, alertes et couches géographiques.
  - Atlas Frontignan : données communales/Thau, risques et scénarios territoriaux.
  - BTP : chantiers, phases, incidents, plans et observations terrain.
  - Cognitorium : profil, connaissances, mémoire et explications contextualisées.
  - Nexus : agents, outils autorisés, tâches et journal d'exécution.
- **Mémoire** : conserver les faits détaillés en stockage indexé ; présenter des résumés abstraits avec liens vers preuves/source ; decay de pertinence, mais récupération à la demande ; aucune donnée ne disparaît silencieusement.
- **Provenance** : chaque élément AR doit être étiqueté comme mesure du téléphone, donnée externe sourcée, estimation, simulation ou contenu utilisateur.

## Limites et sécurité
- Un téléphone seul ne voit pas à travers les murs, ne localise pas des réseaux enterrés sans données/instrumentation, et ne fournit pas d'imagerie thermique sans capteur dédié.
- GPS/boussole smartphone : précision variable ; une étiquette AR ne doit pas être présentée comme un placement centimétrique.
- Permissions minimales ; caméra et localisation désactivables ; préférer traitement local ; pas d'identification faciale, d'analyse de sentiment ou de profilage de personnes par défaut.
- Pour sandbox agentique : aucune exécution non fiable sur la machine principale ; isolation, authentification, réseau limité, journaux et limites de ressources.
- Licences, dépendances, maintenabilité, coût d'exploitation et politiques de données doivent être contrôlés avant tout fork/import.

## Liste de tâches priorisée
### P0 — aujourd'hui
- [ ] Ouvrir xTech5x/AR-HUD sur le téléphone et vérifier si la démo est déployée.
- [ ] Tester caméra, GPS, orientation, affichage de carte et ajout à l'écran d'accueil ; noter modèle du téléphone, navigateur et erreurs.
- [ ] Séparer dans l'inventaire les fonctionnalités réelles, estimées, simulées et indisponibles.
- [ ] Préparer un manifeste de couche minimal (id, label, source, permissions, données, actions, état, confiance).

### P1 — prototype connecté
- [ ] Créer un mode « couches » activables individuellement.
- [ ] Ajouter une première source JSON locale et un connecteur de démonstration, sans exposer de secrets dans le navigateur.
- [ ] Mapper les modules existants du monorepo vers les vues : Watchtower/Atlas/BTP/Cognitorium/Nexus.
- [ ] Vérifier licences, versions, dépendances et état de maintenance des projets candidats.

### P2 — intégration maîtrisée
- [ ] Tester AR-Viewer/WebXR et AR.js sur l'appareil cible.
- [ ] Évaluer l'ancrage spatial GPS/QR et la précision réelle.
- [ ] Évaluer Robot Heads pour les états des agents.
- [ ] Évaluer AIO Sandbox seulement dans un environnement isolé et durci.
- [ ] Comparer les données géographiques ouvertes aux scrapers payants/à conditions restrictives.

## Critères d'acceptation du premier prototype
- [ ] Gratuit pour l'utilisateur au moment du test.
- [ ] Ouvre la caméra et demande les permissions explicitement.
- [ ] Au moins une vue utile s'affiche en superposition ou en HUD.
- [ ] Les couches peuvent être activées/désactivées.
- [ ] Les données simulées sont clairement étiquetées.
- [ ] Le prototype est installable via le navigateur si le PWA est pris en charge.
- [ ] Les modules internes peuvent être ajoutés via un registre/adaptateur sans réécrire le moteur d'affichage.

## Liens d'inspiration
- HUD type Ghost Recon Future Soldier : référence de hiérarchie visuelle uniquement.
- Anduril / interfaces de situation : référence de visualisation opérationnelle, pas de promesse de capacités équivalentes.
- Recherche d'images Brave « AR-HUD » : benchmark visuel à compléter par des captures sourcées et datées.
