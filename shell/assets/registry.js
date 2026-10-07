/* Généré par shell/tools/gen-registry.py — ne pas éditer à la main.
   Source : docs/carre-das/07-INVENTAIRE-FONCTIONNALITES.md */
window.CARRE_REGISTRY = {
  "meta": {
    "name": "Carré d'As",
    "subtitle": "Le portail vers les fonctionnalités de Cognitorium",
    "version": "0.2.0",
    "date": "2026-10-07",
    "principle": "Aucune fonctionnalité n'est perdue : chaque module déclare ses fonctions et leur source dans le dépôt.",
    "source": "docs/carre-das/07-INVENTAIRE-FONCTIONNALITES.md",
    "statuses": {
      "dispo": "disponible",
      "a-porter": "à porter",
      "a-construire": "à construire"
    }
  },
  "doors": [
    {
      "id": "accueil",
      "label": "Accueil",
      "icon": "⌂",
      "hint": "Reprendre, chercher, voir l'état"
    },
    {
      "id": "projets",
      "label": "Projets",
      "icon": "🏗",
      "hint": "Chantiers, prix, planning, qualité"
    },
    {
      "id": "documents",
      "label": "Documents",
      "icon": "📄",
      "hint": "Retrouver, extraire, classer"
    },
    {
      "id": "carte",
      "label": "Carte",
      "icon": "🗺",
      "hint": "Territoire, parcelles, réseaux"
    },
    {
      "id": "agents",
      "label": "Agents",
      "icon": "🤖",
      "hint": "Ils travaillent, tu valides"
    },
    {
      "id": "explorer",
      "label": "Explorer",
      "icon": "🌳",
      "hint": "Profil, graphe, métiers, référentiels"
    },
    {
      "id": "assistant",
      "label": "Assistant",
      "icon": "🛡",
      "hint": "Parler, demander, être guidé"
    },
    {
      "id": "systeme",
      "label": "Système",
      "icon": "⚙",
      "hint": "Modules, comptes, réglages"
    }
  ],
  "modules": [
    {
      "id": "command",
      "label": "Command Center",
      "icon": "⌂",
      "door": "accueil",
      "tagline": "Le portail : quatre portes, la recherche, la reprise.",
      "desc": "Point d'entrée unique. Recherche globale, reprise de l'activité, alertes, état du système.",
      "color": "cyan",
      "features": [
        {
          "n": "Quatre portes",
          "d": "Projets · Carte · Documents · Agents, chacune avec son compteur",
          "s": "a-construire",
          "src": "docs/carre-das/04",
          "p": "V1"
        },
        {
          "n": "Palette de commandes (Ctrl+K)",
          "d": "Tout est atteignable au clavier ; navigation, modules, actions",
          "s": "a-construire",
          "src": "docs/carre-das/02",
          "p": "V1"
        },
        {
          "n": "Reprendre où j'en étais",
          "d": "Activité récente, éléments en cours, à traiter aujourd'hui",
          "s": "dispo",
          "src": "app/templates · projects/proto-cognitorium DashboardView",
          "p": "V1"
        },
        {
          "n": "Barre d'état permanente",
          "d": "Mode local/hors ligne, volume de données, version, latence",
          "s": "dispo",
          "src": "projects/COGNITORIUM (images Vision 2050) · watchtower",
          "p": "V1"
        },
        {
          "n": "Alertes et notifications",
          "d": "Retards, écarts de prix, pièces non classées, risques",
          "s": "a-porter",
          "src": "projects/_incoming/monorepo/arena_01a08449",
          "p": "V1"
        },
        {
          "n": "Registre d'interface (12 catégories)",
          "d": "Toutes les surfaces déclarées et couvertes, avec source",
          "s": "a-porter",
          "src": "projects/_incoming/monorepo/feat_final-interface-skeleton-2026-10-07/data/interface_registry.json",
          "p": "V1"
        },
        {
          "n": "Mode présentation plein écran",
          "d": "Montrer le projet à une association, une mairie, un financeur",
          "s": "dispo",
          "src": "projects/frontignan (deck 18 slides, export PDF)",
          "p": "V1"
        }
      ]
    },
    {
      "id": "projets",
      "label": "Projets & chantiers",
      "icon": "🏗",
      "door": "projets",
      "tagline": "Le conteneur de tout le travail réel.",
      "desc": "Un projet regroupe documents, prix, planning, carte, qualité et journal. C'est l'espace de travail de l'Atelier.",
      "color": "cyan",
      "features": [
        {
          "n": "Fiche projet",
          "d": "Identité, phase, acteurs, localisation, historique",
          "s": "a-porter",
          "src": "projects/_incoming/monorepo/arena_01a08449",
          "p": "V1"
        },
        {
          "n": "Onglets de contexte",
          "d": "Documents · Prix · Métrés · Planning · Qualité · Carte · 3D · Réseaux · Sécurité",
          "s": "a-construire",
          "src": "docs/carre-das/maquettes/v2-l-atelier.html",
          "p": "V1"
        },
        {
          "n": "Panneau détails + provenance",
          "d": "Chaque valeur affiche sa source, sa page, sa date de validation",
          "s": "dispo",
          "src": "projects/proto-cognitorium (utils/epistemics)",
          "p": "V1"
        },
        {
          "n": "Journal d'activité",
          "d": "Qui a fait quoi, quand : agents et humain",
          "s": "dispo",
          "src": "projects/COGNITORIUM watchtower-mods + proto (ValidationCenterModal)",
          "p": "V1"
        },
        {
          "n": "Multi-projets",
          "d": "Plusieurs chantiers en parallèle, comparaison",
          "s": "dispo",
          "src": "projects/proto-cognitorium/src/components/MultiProjectsView.tsx",
          "p": "V1"
        },
        {
          "n": "Pièces jointes et versions",
          "d": "Chaque document garde son historique",
          "s": "a-construire",
          "src": "docs/carre-das/01 (owns/reads)",
          "p": "V1.5"
        }
      ]
    },
    {
      "id": "documents",
      "label": "Documents",
      "icon": "📄",
      "door": "documents",
      "tagline": "Retrouver, comprendre, extraire.",
      "desc": "154 pièces indexées, recherche plein texte + sémantique, extraction structurée, CV ciblé, classification automatique.",
      "color": "cyan",
      "features": [
        {
          "n": "Corpus BTP indexé",
          "d": "154 documents en 7 familles, inventaire SHA-256, matrice de traçabilité",
          "s": "dispo",
          "src": "projects/_incoming/monorepo/arena_01a08449/projects/btp-conduite-travaux",
          "p": "V1"
        },
        {
          "n": "Recherche plein texte + sémantique",
          "d": "FTS + vecteurs, fusion des deux classements",
          "s": "a-construire",
          "src": "docs/recherche/03 (stack)",
          "p": "V1"
        },
        {
          "n": "Extraction structurée",
          "d": "PDF/Office → texte, tableaux, métadonnées, pages citées",
          "s": "a-construire",
          "src": "docs/recherche/03-ENRICHISSEMENTS-ET-ARBITRAGES.md",
          "p": "V1"
        },
        {
          "n": "Rangement automatique",
          "d": "Famille, doublons, dates, pièces non classées",
          "s": "a-construire",
          "src": "docs/carre-das/06 §5.4",
          "p": "V1"
        },
        {
          "n": "CV ciblé par offre",
          "d": "Adapter le CV à une annonce, alignement compétences ↔ besoin",
          "s": "dispo",
          "src": "projects/proto-cognitorium/src/components/TargetedCvView.tsx + cv/",
          "p": "V1.5"
        },
        {
          "n": "Import CV → profil",
          "d": "Le CV est une source, pas le produit final",
          "s": "dispo",
          "src": "projects/proto-cognitorium (OnboardingModal, ExperienceDistillerModal)",
          "p": "V1"
        },
        {
          "n": "Pièces justificatives",
          "d": "Devis, factures, PV, photos terrain",
          "s": "dispo",
          "src": "projects/proto-cognitorium/raw + _incoming (arena_01a08449)",
          "p": "V1"
        }
      ]
    },
    {
      "id": "carte",
      "label": "Carte & territoire",
      "icon": "🗺",
      "door": "carte",
      "tagline": "Le réel, à sa place.",
      "desc": "Parcelles, réseaux, aléas, prix. 2D par défaut (3 ms), 3D à la demande. Atlas territorial et données ouvertes.",
      "color": "cyan",
      "features": [
        {
          "n": "Carte 2D (MapLibre)",
          "d": "Rendu vectoriel local, PMTiles, très rapide",
          "s": "a-porter",
          "src": "projects/watchtower + _incoming/watchtower/arena_01a072e1",
          "p": "V1"
        },
        {
          "n": "Bascule 2D/3D",
          "d": "Cesium à la demande (mesuré 21 357 ms vs 3 ms en 2D → jamais par défaut)",
          "s": "a-porter",
          "src": "projects/_incoming/watchtower/arena_01a072e1",
          "p": "V1.5"
        },
        {
          "n": "Atlas territorial",
          "d": "Nœuds, communes, images, données locales",
          "s": "a-porter",
          "src": "projects/_incoming/monorepo/arena_01a08203-monorepo/projects/frontignan/atlas",
          "p": "V1.5"
        },
        {
          "n": "Barre de 24 fonctions",
          "d": "Couches, mesures, recherche de lieu, itinéraires",
          "s": "a-porter",
          "src": "projects/_incoming/watchtower/arena_01a072e1",
          "p": "V1.5"
        },
        {
          "n": "Grille de vérité ✅📅🔮⚠️",
          "d": "Chaque information territoriale est marquée établie / à venir / hypothèse / alerte",
          "s": "dispo",
          "src": "projects/watchtower/INTEL-TERRITOIRE.md",
          "p": "V1"
        },
        {
          "n": "Données ouvertes branchées",
          "d": "IGN (cadastre, BD TOPO), BAN, DVF, Géorisques",
          "s": "a-construire",
          "src": "docs/recherche/03 (connecteurs)",
          "p": "V1.5"
        },
        {
          "n": "Itinéraires hors ligne",
          "d": "BRouter, sans réseau",
          "s": "a-construire",
          "src": "docs/carre-das/06 §3.1",
          "p": "V1.5"
        },
        {
          "n": "Fond de carte « prepper »",
          "d": "Extraits OSM + Wikipédia hors ligne (Kiwix) consultables au clic",
          "s": "a-construire",
          "src": "docs/carre-das/06 §2",
          "p": "V2"
        }
      ]
    },
    {
      "id": "btp",
      "label": "BTP — conduite de travaux",
      "icon": "🧱",
      "door": "projets",
      "tagline": "Le métier : prix, métrés, suivi, sécurité.",
      "desc": "Le module le plus fourni : DCE/marchés, étude de prix, métrés, planning, qualité, sécurité, réseaux. 7 piliers, 154 documents source.",
      "color": "amber",
      "features": [
        {
          "n": "DCE & marchés publics",
          "d": "CCTP, DQE, BPU, délibérations, DT/DICT",
          "s": "dispo",
          "src": "projects/_incoming/monorepo/arena_01a08449-monorepo/projects/btp-conduite-travaux/documents_sources/01_dce_marches_publics",
          "p": "V1"
        },
        {
          "n": "Étude de prix & sous-détails",
          "d": "28 sous-détails, simulateur, comparaison aux références",
          "s": "a-porter",
          "src": "projects/_incoming/monorepo/arena_01a08449-monorepo/projects/btp-conduite-travaux/rapports",
          "p": "V1"
        },
        {
          "n": "Métrés & quantités",
          "d": "Contrôle de cohérence, écarts, révision",
          "s": "dispo",
          "src": "proto-cognitorium/projects/proto-cognitorium/raw/métré.xlsx",
          "p": "V1"
        },
        {
          "n": "Suivi de chantier",
          "d": "Avancement, PV de réunion, réserves, DOE",
          "s": "dispo",
          "src": "projects/proto-cognitorium/raw/pv de marquage - piquetage.pdf",
          "p": "V1"
        },
        {
          "n": "Sécurité & AIPR",
          "d": "Signalisation temporaire, plan de prévention, QCM/formations AIPR",
          "s": "dispo",
          "src": "projects/proto-cognitorium/raw/Signalisation OPPBTP.pdf",
          "p": "V1"
        },
        {
          "n": "Réseaux secs",
          "d": "Croisement de réseaux, DT/DICT, grilles de protection télécom",
          "s": "dispo",
          "src": "projects/proto-cognitorium/raw/guide pour le croisement des reseaux.pdf",
          "p": "V1"
        },
        {
          "n": "Géotechnique & voirie",
          "d": "Coupe type, compactage, ICE, assainissement",
          "s": "dispo",
          "src": "projects/proto-cognitorium/raw/coupe type.pdf",
          "p": "V1.5"
        },
        {
          "n": "Non-conformités & essais",
          "d": "Registre NC, essais, levées de réserves",
          "s": "a-construire",
          "src": "docs/carre-das/03 (entités)",
          "p": "V1.5"
        },
        {
          "n": "Moteur multi-agents BTP",
          "d": "Analyse croisée documents / prix / in situ",
          "s": "a-porter",
          "src": "projects/_incoming/monorepo/arena_01a08449-monorepo/projects/btp-conduite-travaux/engine/btp_multi_agent.py",
          "p": "V1.5"
        },
        {
          "n": "Bâti 3D (voir & mesurer)",
          "d": "IFC + nuage de points : palier 1 du module 3D",
          "s": "a-construire",
          "src": "docs/carre-das/03 (3 paliers)",
          "p": "V2"
        },
        {
          "n": "Gestion RH & formation",
          "d": "Habiliations, journaux pédagogiques, encadrement",
          "s": "dispo",
          "src": "projects/proto-cognitorium/raw/fntp_journalkitpedago2015_v8.pdf",
          "p": "V2"
        }
      ]
    },
    {
      "id": "cognition",
      "label": "Cognition & profil",
      "icon": "🧠",
      "door": "explorer",
      "tagline": "Comprendre ce que l'on sait faire — et le prouver.",
      "desc": "Tableau de bord cognitif, décroissance des compétences, biais, métacognition, modèle scientifique HCSM.",
      "color": "violet",
      "features": [
        {
          "n": "Tableau de bord cognitif",
          "d": "Indicateurs, jauges, résumé du profil",
          "s": "dispo",
          "src": "projects/proto-cognitorium/src/components/DashboardView.tsx",
          "p": "V1.5"
        },
        {
          "n": "Disponibilité estimée (decay)",
          "d": "Décroissance puis réactivation d'une compétence ; jamais présenté comme une mesure absolue",
          "s": "dispo",
          "src": "proto-cognitorium/utils/decay.ts + DecayTimeline",
          "p": "V1.5"
        },
        {
          "n": "Biais cognitifs (6 fiches)",
          "d": "Ancrage, disponibilité, confirmation, Dunning-Kruger, halo, excès de confiance",
          "s": "dispo",
          "src": "projects/proto-cognitorium/src/components/CognitiveBiasesView.tsx",
          "p": "V2"
        },
        {
          "n": "Métacognition & écart perçu/réel",
          "d": "Comparer le ressenti à l'application réelle",
          "s": "dispo",
          "src": "projects/proto-cognitorium/src/components/MetacogLoopView.tsx",
          "p": "V1.5"
        },
        {
          "n": "Modèle scientifique HCSM",
          "d": "État cognitif multidimensionnel, validateur, ontologie",
          "s": "dispo",
          "src": "projects/HCSM (87 fichiers, 32 de validation)",
          "p": "V1.5"
        },
        {
          "n": "Protocoles & sessions",
          "d": "N-back jouable, expériences, mesures dans l'app",
          "s": "dispo",
          "src": "projects/proto-cognitorium/src/components/ExperimentStudio.tsx",
          "p": "V2"
        },
        {
          "n": "Évaluations",
          "d": "Catalogue d'évaluations, passations, résultats",
          "s": "dispo",
          "src": "projects/proto-cognitorium/src/components/MesEvaluationsView.tsx",
          "p": "V2"
        },
        {
          "n": "Atlas de psychologie",
          "d": "Références psychologiques reliées aux compétences",
          "s": "dispo",
          "src": "projects/proto-cognitorium/src/components/PsychologyAtlasView.tsx",
          "p": "V2"
        }
      ]
    },
    {
      "id": "graphe",
      "label": "Graphe & arbre",
      "icon": "🌳",
      "door": "explorer",
      "tagline": "Six façons de voir le même modèle.",
      "desc": "Le graphe n'est pas l'unique porte d'entrée : chaque représentation montre les mêmes données autrement, avec un équivalent textuel.",
      "color": "violet",
      "features": [
        {
          "n": "Vue libre (constellation)",
          "d": "Exploration globale, zoom sémantique",
          "s": "dispo",
          "src": "projects/proto-cognitorium/src/components/NetworkGraph.tsx",
          "p": "V1.5"
        },
        {
          "n": "Arbre de compétences",
          "d": "Racines = expériences, tronc = savoirs, branches = compétences",
          "s": "dispo",
          "src": "projects/proto-cognitorium/src/components/TreeView.tsx",
          "p": "V1.5"
        },
        {
          "n": "Graphe temporel",
          "d": "Évolution dans le temps, périodes d'activité",
          "s": "dispo",
          "src": "projects/proto-cognitorium/src/components/TemporalNetworkGraph.tsx",
          "p": "V1.5"
        },
        {
          "n": "Vue métiers",
          "d": "Le profil face à un métier cible",
          "s": "dispo",
          "src": "projects/proto-cognitorium/src/components/MetiersGraph.tsx",
          "p": "V1.5"
        },
        {
          "n": "Tableau",
          "d": "Comparer, filtrer, trier, exporter",
          "s": "dispo",
          "src": "projects/proto-cognitorium/src/components/TableView.tsx",
          "p": "V1"
        },
        {
          "n": "Vue liste accessible",
          "d": "Le même contenu sans graphique (lecteurs d'écran, RGAA)",
          "s": "dispo",
          "src": "projects/proto-cognitorium/projects/proto-cognitorium/projects/proto-cognitorium/raw/noeud neurono.html",
          "p": "V1"
        },
        {
          "n": "Zoom sémantique à 5 niveaux",
          "d": "réseaux → domaines → sous-domaines → capacités → micro-compétences",
          "s": "dispo",
          "src": "projects/proto-cognitorium/projects/proto-cognitorium/raw/noeud neurono.html",
          "p": "V1.5"
        },
        {
          "n": "Statut épistémique",
          "d": "Établi · Modèle · Spéculatif sur chaque nœud",
          "s": "dispo",
          "src": "projects/proto-cognitorium/raw/noeud neurono.html",
          "p": "V1"
        },
        {
          "n": "Inspecteur de nœud",
          "d": "Provenance, preuves, confiance, historique",
          "s": "dispo",
          "src": "projects/proto-cognitorium/src/components/NodeInspectorModal.tsx",
          "p": "V1"
        }
      ]
    },
    {
      "id": "metiers",
      "label": "Métiers & passerelles",
      "icon": "🎯",
      "door": "explorer",
      "tagline": "Ce qui est accessible, et par où passer.",
      "desc": "Matching explicable : compétences démontrées, transférables, écarts, étapes. Référentiels ROME et formations.",
      "color": "violet",
      "features": [
        {
          "n": "Matching explicable",
          "d": "Chaque métier recommandé dit pourquoi, ce qui manque, et les étapes",
          "s": "dispo",
          "src": "projects/proto-cognitorium/src/components/HorizonsBridge.tsx",
          "p": "V1.5"
        },
        {
          "n": "Référentiel ROME",
          "d": "Données ROME intégrées et normalisées",
          "s": "dispo",
          "src": "proto-cognitorium/src/data/romeData.ts (5,5 Mo)",
          "p": "V1.5"
        },
        {
          "n": "Formations & acquisitions",
          "d": "Relier une compétence manquante à une formation",
          "s": "dispo",
          "src": "projects/proto-cognitorium/src/components/ResourcesView.tsx",
          "p": "V2"
        },
        {
          "n": "Passerelles professionnelles",
          "d": "expérience / projet / formation / étape suivante",
          "s": "dispo",
          "src": "projects/proto-cognitorium/src/components/HorizonsBridge.tsx",
          "p": "V2"
        },
        {
          "n": "Scores par catégories",
          "d": "très forte · forte · modérée · à explorer (jamais un score nu)",
          "s": "dispo",
          "src": "docs/carre-das/00 (UX-09)",
          "p": "V1"
        },
        {
          "n": "Trajectoire avec incertitude",
          "d": "Représenter le futur comme un faisceau, pas une ligne",
          "s": "dispo",
          "src": "projects/proto-cognitorium/projects/proto-cognitorium/raw/noeud neurono.html",
          "p": "V1.5"
        }
      ]
    },
    {
      "id": "agents",
      "label": "Agents & automatisation",
      "icon": "🤖",
      "door": "agents",
      "tagline": "Des assistants qui travaillent, sous contrôle.",
      "desc": "22 agents, 22 outils sandboxés, MCP, moteur de recherche autonome, veille OSINT : la brique IA du produit.",
      "color": "green",
      "features": [
        {
          "n": "NEXUS·OS — 22 agents",
          "d": "Analyste, architecte, archiviste, rédacteur… avec rôles déclarés",
          "s": "a-porter",
          "src": "_incoming/monorepo/arena_01a08385-monorepo/projects/_incoming/monorepo/arena_01a08385-monorepo/nexus_os/agents",
          "p": "V1.5"
        },
        {
          "n": "8 fournisseurs / 20 modèles",
          "d": "Routeur local d'abord, cloud ensuite, mode dégradé sans clé",
          "s": "a-porter",
          "src": "projects/_incoming/monorepo/arena_01a08385-monorepo/nexus_os",
          "p": "V1.5"
        },
        {
          "n": "22 outils sandboxés",
          "d": "Chaque outil tourne isolé avec des permissions déclarées",
          "s": "a-porter",
          "src": "projects/_incoming/monorepo/arena_01a08385-monorepo/nexus_os/tools",
          "p": "V1.5"
        },
        {
          "n": "MCP (Model Context Protocol)",
          "d": "Brancher des outils externes proprement",
          "s": "a-porter",
          "src": "projects/_incoming/monorepo/arena_01a08385-monorepo/nexus_os/mcp",
          "p": "V1.5"
        },
        {
          "n": "147 tests automatisés",
          "d": "Les agents sont testés avant d'être branchés",
          "s": "a-porter",
          "src": "projects/_incoming/monorepo/arena_01a08385-monorepo/nexus_os/tests",
          "p": "V1.5"
        },
        {
          "n": "Recherche autonome & sourcée",
          "d": "question → plan → preuves → contradictions → synthèse → vérification",
          "s": "dispo",
          "src": "projects/reaserch-engine (engine, schemas, tests)",
          "p": "V1.5"
        },
        {
          "n": "Veille OSINT",
          "d": "Registre de sources, dossier, preuves horodatées",
          "s": "a-porter",
          "src": "_incoming/COGNITORIUM/watchtower_osint-workbench-v0.1",
          "p": "V2"
        },
        {
          "n": "Agent scientifique",
          "d": "Planificateur, collecte, rapport structuré",
          "s": "a-porter",
          "src": "projects/_incoming/ETAT-DE-LART-PSYCHOLOGIE/arena_01a04f7b-etat-de-lart-psychologie/agent",
          "p": "V1.5"
        },
        {
          "n": "Journal & garde-fous",
          "d": "Rien ne s'exécute sans trace ; permissions « rien par défaut »",
          "s": "dispo",
          "src": "docs/carre-das/01 (contrat de module) + projects/_incoming/monorepo/arena_01a08385-monorepo/nexus_os/security",
          "p": "V1"
        }
      ]
    },
    {
      "id": "referentiels",
      "label": "Référentiels & fiches",
      "icon": "📚",
      "door": "explorer",
      "tagline": "La connaissance, hors ligne, vérifiable.",
      "desc": "Fiches génériques (espèces, matériaux, réseaux, engins), base scientifique de l'état de l'art, références psy, Wikipédia/ZIM hors ligne.",
      "color": "violet",
      "features": [
        {
          "n": "Module Fiches (générique)",
          "d": "Un format unique : id, type, propriétés, photos, sources, statut",
          "s": "a-construire",
          "src": "docs/carre-das/06 §3.2",
          "p": "V1.5"
        },
        {
          "n": "État de l'art psychologie",
          "d": "Cartographie critique PRISMA 2020, 12 domaines, équations reproductibles",
          "s": "dispo",
          "src": "projects/ETAT-DE-LART-PSYCHOLOGIE (docs, 42 champs)",
          "p": "V2"
        },
        {
          "n": "Base à 42 champs",
          "d": "14 entrées validées, trust factor 73,2, guide de remplissage IA",
          "s": "dispo",
          "src": "ETAT-DE-LART-PSYCHOLOGIE/data + output/",
          "p": "V1.5"
        },
        {
          "n": "Fiches de biais illustrées",
          "d": "6 biais + 10 schémas + 4 expériences fondatrices (contenu récupéré du patch)",
          "s": "a-porter",
          "src": "projects/_incoming/ETAT-DE-LART-PSYCHOLOGIE/arena_01a04f7b-etat-de-lart-psychologie/app/bias_cards.py",
          "p": "V2"
        },
        {
          "n": "Bibliothèque hors ligne (Kiwix/ZIM)",
          "d": "Wikipédia, WikiMed, iFixit consultables sans internet",
          "s": "a-construire",
          "src": "docs/carre-das/06 §2",
          "p": "V2"
        },
        {
          "n": "Ateliers & laboratoire",
          "d": "App concepts + lab + stats (Flask) à porter",
          "s": "a-porter",
          "src": "projects/_incoming/ETAT-DE-LART-PSYCHOLOGIE/arena_01a04f7b-etat-de-lart-psychologie/app",
          "p": "V2"
        },
        {
          "n": "Sources & traçabilité",
          "d": "Chaque fiche cite ses sources ; jamais de donnée sans origine",
          "s": "dispo",
          "src": "projects/ETAT-DE-LART-PSYCHOLOGIE/data",
          "p": "V1"
        }
      ]
    },
    {
      "id": "apprentissage",
      "label": "Apprentissage",
      "icon": "🎓",
      "door": "explorer",
      "tagline": "Comprendre en résolvant.",
      "desc": "Learning Engine : parcours par résolution de problèmes avec retour explicatif et graphe conceptuel qui se construit.",
      "color": "violet",
      "features": [
        {
          "n": "Parcours « Comprendre l'argent »",
          "d": "troc → monnaie → prix → épargne → crédit → intérêt → inflation → investissement",
          "s": "dispo",
          "src": "projects/COGNITORIUM (Learning Engine PoC v0.1)",
          "p": "V2"
        },
        {
          "n": "Graphe conceptuel dynamique",
          "d": "Le graphe se construit au fur et à mesure des réussites",
          "s": "dispo",
          "src": "projects/COGNITORIUM/learning",
          "p": "V2"
        },
        {
          "n": "Retour explicatif",
          "d": "On explique pourquoi c'est faux, pas seulement que c'est faux",
          "s": "dispo",
          "src": "projects/COGNITORIUM (learning)",
          "p": "V2"
        },
        {
          "n": "Kolibri (cours hors ligne)",
          "d": "Plateforme d'apprentissage hors ligne, auto-hébergeable",
          "s": "a-construire",
          "src": "docs/carre-das/06 §2 (learningequality/kolibri, MIT)",
          "p": "V2"
        }
      ]
    },
    {
      "id": "langage",
      "label": "Langage & notes",
      "icon": "🗣",
      "door": "agents",
      "tagline": "Décoder, reformuler, garder.",
      "desc": "Décodeur de langage multimodal, multi-IA, ontologie, mémoire, notes structurées.",
      "color": "violet",
      "features": [
        {
          "n": "Décodeur de langage",
          "d": "decoder, dynamics, evidence, functioning, inference + CLI",
          "s": "a-porter",
          "src": "_incoming/Language-decoder/arena_01a05471-language-decoder/language_decoder/",
          "p": "V2"
        },
        {
          "n": "Mémoire & sessions multi-IA",
          "d": "Conversations, mémoire, monde 2040, session simulée",
          "s": "a-porter",
          "src": "_incoming/Language-decoder/arena_01a05429-language-decoder/data/",
          "p": "V2"
        },
        {
          "n": "Ontologie",
          "d": "Structure de concepts réutilisable",
          "s": "a-porter",
          "src": "projects/_incoming/Language-decoder/arena_01a05429-language-decoder/data/ontology.json",
          "p": "V2"
        },
        {
          "n": "Dashboard de suivi",
          "d": "Visualisation des échanges et de l'évolution",
          "s": "a-porter",
          "src": "projects/_incoming/Language-decoder/arena_01a05429-language-decoder/css/dashboard.css",
          "p": "V2"
        },
        {
          "n": "Transcription locale (Whisper)",
          "d": "Réunions de chantier, dictées, en français",
          "s": "a-construire",
          "src": "docs/carre-das/06 §1.2",
          "p": "V1.5"
        }
      ]
    },
    {
      "id": "assistant",
      "label": "Assistant JARVIS",
      "icon": "🛡",
      "door": "assistant",
      "tagline": "Un guide, pas un gadget.",
      "desc": "Assistant vocal et visuel : il navigue, cherche, explique, et ne fait rien sans trace. Mode sans clé garanti.",
      "color": "amber",
      "features": [
        {
          "n": "Orbe réactive",
          "d": "États : repos · écoute · réflexion · parole (visualisation audio réelle)",
          "s": "dispo",
          "src": "shell/assets/assistant.js (ce squelette)",
          "p": "V1"
        },
        {
          "n": "Voix (entrée)",
          "d": "Web Speech API, mot de réveil, mode push-to-talk si refus du micro",
          "s": "dispo",
          "src": "shell/assets/assistant.js · réf. adewaskar/jarvis (MIT)",
          "p": "V1"
        },
        {
          "n": "Voix (sortie)",
          "d": "Synthèse vocale locale, choix de la voix, français d'abord",
          "s": "dispo",
          "src": "shell/assets/assistant.js (speechSynthesis)",
          "p": "V1"
        },
        {
          "n": "Guidage par la voix",
          "d": "« ouvre le BTP », « montre les documents », « cherche métrés »",
          "s": "dispo",
          "src": "shell/assets/assistant.js (routeur de commandes sur le registre)",
          "p": "V1"
        },
        {
          "n": "Sons d'interface",
          "d": "Pings, whoosh, confirmations — synthétisés hors ligne (CC0)",
          "s": "dispo",
          "src": "shell/assets/sounds.js · pack optionnel uisfx « scifi » (MIT code, CC0 audio)",
          "p": "V1"
        },
        {
          "n": "IA locale (Ollama) optionnelle",
          "d": "Si un modèle local tourne, l'assistant l'utilise ; sinon il le dit",
          "s": "dispo",
          "src": "shell/assets/assistant.js + docs/carre-das/06 §1",
          "p": "V1.5"
        },
        {
          "n": "Contrôle total",
          "d": "Micro coupable, voix coupable, sons coupables, tout est tracé",
          "s": "dispo",
          "src": "docs/carre-das/01 (permissions) + shell",
          "p": "V1"
        }
      ]
    },
    {
      "id": "systeme",
      "label": "Système & modules",
      "icon": "⚙",
      "door": "systeme",
      "tagline": "Installer, brancher, sauvegarder, rester libre.",
      "desc": "Comptes, synchronisation, installation des modules à chaud, mises à jour signées, accessibilité, sauvegardes.",
      "color": "grey",
      "features": [
        {
          "n": "Comptes & profils",
          "d": "Portail d'authentification, inscription, gestion de profils",
          "s": "dispo",
          "src": "proto-cognitorium/src/components/auth/ (10 composants)",
          "p": "V1"
        },
        {
          "n": "Synchronisation multi-comptes",
          "d": "Local = vérité ; Google drive.appdata / OneDrive / WebDAV ; conflits jamais écrasés",
          "s": "a-construire",
          "src": "docs/carre-das/03 (sync)",
          "p": "V1.5"
        },
        {
          "n": "Modules à chaud",
          "d": "Activer/désactiver un module sans redémarrer, défaillance isolée",
          "s": "dispo",
          "src": "docs/carre-das/01 (contrat) + _incoming feat_tool-data-catalog (JSON Schema)",
          "p": "V1"
        },
        {
          "n": "Contrats de données",
          "d": "module.schema.json + canonical-record.schema.json",
          "s": "a-porter",
          "src": "_incoming/monorepo/feat_tool-data-catalog-2026-10/core/contracts/",
          "p": "V1"
        },
        {
          "n": "Mises à jour signées + retour arrière",
          "d": "Installeur, version, rollback",
          "s": "a-construire",
          "src": "docs/carre-das/00 (définition du fini)",
          "p": "V1"
        },
        {
          "n": "Licence & monétisation",
          "d": "Cœur Apache-2.0 + CLA + marque + open core : la porte de la monétisation reste ouverte (double licence possible)",
          "s": "dispo",
          "src": "docs/carre-das/05-REPONSES-AUX-QUESTIONS.md §1",
          "p": "V1"
        },
        {
          "n": "Gouvernance",
          "d": "Constitution, journal de décisions, registre d'outils et licences",
          "s": "dispo",
          "src": "projects/COGNITORIUM/docs/constitution + watchtower/audit",
          "p": "V1"
        },
        {
          "n": "Audit qualité",
          "d": "52 constats mesurés, analyse V1→V5, plan d'action",
          "s": "a-porter",
          "src": "_incoming/monorepo/arena_171a1f38-monorepo/audit/",
          "p": "V1"
        },
        {
          "n": "Accessibilité (RGAA/WCAG)",
          "d": "Vue liste équivalente, clavier complet, contraste, mouvement réduit",
          "s": "dispo",
          "src": "projects/proto-cognitorium/projects/proto-cognitorium/raw/noeud neurono.html",
          "p": "V1"
        },
        {
          "n": "Réglages : sons, voix, thème",
          "d": "Tout ce qui parle ou sonne est désactivable en un clic",
          "s": "dispo",
          "src": "shell/data/modules.json → module systeme",
          "p": "V1"
        }
      ]
    }
  ]
};
