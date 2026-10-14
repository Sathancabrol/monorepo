# Génère audit/data/importance.json — classement v1→v5 des 79 éléments (analyse 2026-10-07).
# Usage : python3 scripts/audit_importance.py (depuis la racine du dépôt).
# -*- coding: utf-8 -*-
import json
E = []
def add(i, el, src, dom, etat, v, action):
    E.append(dict(id=i, element=el, source=src, domaine=dom, etat=etat, v=v, action=action))

# D1 Command Center
add("D1-01","Interface finale 12 domaines (html/css/js + registre)","branche feat/final-interface-skeleton-2026-10-07","D1","branche","v1","fusionner en premier")
add("D1-02","Coquille FastAPI (explorateur, previews, garde-fous)","app/main.py (monorepo main)","D1","existe","v1","conserver, renforcer")
add("D1-03","Registre des outils/donnees (9 domaines, regle referencer→adapter→normaliser→extraire)","docs/TOOL-DATA-CATALOG.md (feat/tool-data-catalog-2026-10)","D1","branche","v1","fusionner")
add("D1-04","Dashboard global, recherche globale, timeline","domaine 1 du registre","D1","specifie","v2","construire apres 3 domaines")
add("D1-05","Snapshot GitHub rafraichi + date en UI","data/github_inventory.json","D1","existe (perime)","v1","regenerer")
# D2 World/Territory
add("D2-01","Globe Cesium, ~29 calques, docks, vues territoire, epingles, bati 3D","projects/watchtower","D2","existe","v2","autorite monde")
add("D2-02","Barre unique de fonctions, carte 2D IGN, minicarte, volant, panneau FIL, archives/crues, charge mentale","branche arena/01a072e1-watchtower (+43)","D2","branche","v2","PR puis fusion")
add("D2-03","INTEL territorial Frontignan/Thau, import CSV, projets, lacunes, veille officielle, imprevus TP","branche arena/dec9cd88-watchtower (PR #3)","D2","branche","v2","fusionner")
add("D2-04","Dossier territoire Frontignan : rapport 826 l., 249 sources datees, vision 2040, deck 18 slides","projects/frontignan","D2","existe","v2","conserver comme modele")
add("D2-05","Atlas interactif Frontignan / Cognitarium City","branche arena/01a08203-monorepo","D2","branche","v3","evaluer")
add("D2-06","Couche solar system","projects/watchtower","D2","existe","v5","hors chaine de valeur")
add("D2-07","Fork watchtower-mods (doublon 62/62)","projects/COGNITORIUM/watchtower-mods","D2","doublon","v0","archiver")
# D3 Intel/OSINT
add("D3-01","intelTwin, OSINT case, evidence/source registry, veille, empreinte economique","projects/watchtower","D3","fragment","v3","apres le Core")
add("D3-02","Dossier de recherche : claims, contradictions, suffisance","projects/reaserch-engine","D3","existe","v2","corriger tests puis integrer")
add("D3-03","Correlation multi-signaux + baseline temporelle + gaps visibles","absent (modele World Monitor)","D3","absent","v3","construire")
add("D3-04","OSINT workbench (modules + specs)","branche watchtower/osint-workbench-v0.1 (COGNITORIUM)","D3","branche","v3","evaluer vs watchtower")
add("D3-05","Flux GDELT, scanner, news","absent (ref. OSIRIS)","D3","absent","v3","ajouter")
add("D3-06","Garde-fou : aucune fonctionnalite visant une personne physique","projects/watchtower/AGENTS.md","D3","existe","v1","eriger en regle plateau")
# D4 Projets/BTP
add("D4-01","Module BTP complet : corpus 154 sources, DCE→DOE, prix, DT/DICT/AIPR, dashboard","branche arena/01a08449-monorepo (projects/btp-conduite-travaux)","D4","branche","v3","apres territoire")
add("D4-02","Corpus racine 220 documents / 225 Mo (12 familles)","racine monorepo","D4","existe","v3","externaliser stockage (v0)")
add("D4-03","Couche chantier watchtower : 81 fiches imprevus, suivi, engins","projects/watchtower","D4","fragment","v3","aligner sur module BTP")
add("D4-04","Phasage 4D / BIM / jumeau numerique chantier","registre domaine 4 (placeholder)","D4","absent","v4","plus tard")
add("D4-05","Dossier de chantier duplique (branche BTP vs racine)","projects/btp-conduite-travaux/documents_sources","D4","doublon","v0","dedupliquer")
# D5 Human/Cognition
add("D5-01","HCSM : ontologie, constructs, provenance/incertitude/contexte/temporal state, validateur V1/V5 (23 cas, 29 tests)","projects/HCSM","D5","existe","v1","promouvoir en contrat du Core")
add("D5-02","Profils (6), graphe competences 5 niveaux, ROME 1911 fiches, decay, epistemique, CV alignment","projects/proto-cognitorium","D5","existe","v2","resync puis demembrer par domaine")
add("D5-03","Atlas psychologie + PsyRef + labo (experiences, evaluations, metacognition)","projects/proto-cognitorium (composants)","D5","existe","v2","atlas v2, labo v4")
add("D5-04","Language-decoder : moteur Python 12 modules + schema decoded-human + UI","branches arena/01a05471 et 01a05429 (Language-decoder)","D5","branche","v2","PR vers main")
add("D5-05","3 bases de connaissances psy concurrentes","proto + ETAT + HCSM","D5","doublon","v1","fermer ADR-009")
add("D5-06","Biais cognitifs, metacognition, histoire de vie","proto (cognitiveBiasesData.ts, distant)","D5","fragment","v3","enrichir le profil")
# D6 Knowledge/Research
add("D6-01","reaserch-engine : pipeline complet 21 modules, 9 schemas, JsonRunStore","projects/reaserch-engine","D6","existe","v2","corriger 2 tests rouges avant integration")
add("D6-02","ETAT-DE-LART : base 42 champs, app FastAPI+SQLite, PRISMA, scripts DOI, 4 viz D3","projects/ETAT-DE-LART-PSYCHOLOGIE","D6","existe","v2","conserver comme contenu")
add("D6-03","Agent de recherche litteraire, cosmos, 221 sorties","branche arena/01a04f7b-ETAT-DE-LART (+38)","D6","branche","v2","revue puis fusion")
add("D6-04","Cognitorium v8 (graphe 3D, 40 fiches)","branche arena/01a03aac-ETAT-DE-LART","D6","branche","v3","evaluer")
add("D6-05","Methode Talbot v4.2 : registre de claims, 12 corrections","docs/synthese-talbot-2026","D6","existe","v1","generaliser en registre de claims")
add("D6-06","Frontignan : 249 sources datees + balises de statut","projects/frontignan","D6","existe","v2","deja conforme")
add("D6-07","Redaction d'articles / paper writing","registre domaine 6","D6","absent","v4","apres synthese stabilisee")
# D7 Learning
add("D7-01","CLE : learning-engine.js, PoC turboreacteur, PoC money, architecture","projects/COGNITORIUM/learning","D7","fragment","v3","apres Skill Graph persistant")
add("D7-02","Scenario / challenge / operations cognitives / boucle adaptative / transfert","registre domaine 7","D7","fragment","v3","apres socle profil")
add("D7-03","Pattern de revelation progressive","projects/animation-chronos (ProgressiveDiscoveryBar)","D7","existe","v4","composant d'onboarding")
# D8 Simulation/Lab
add("D8-01","Experiment Studio + catalogue evaluations + boucle metacognitive","proto (ExperimentStudio, evaluationsCatalog, MetacogLoopView)","D8","existe","v4","quand donnees reelles")
add("D8-02","Graphes temporels et reseau interactifs","proto (TemporalNetworkGraph, NetworkGraph)","D8","existe","v3","viz reutilisable plus tot")
add("D8-03","Experience temporelle Chronos (9 composants)","projects/animation-chronos","D8","existe","v4","integrer comme composant, pas app")
add("D8-04","Sandbox de simulation","registre domaine 8 (placeholder)","D8","absent","v5","plus tard")
# D9 Design/CAD/Fabrication
add("D9-01","Decisions CAD : Replicad + OpenCascade.js ; JSCAD CSG ; OrcaSlicer local","constitution/03-architecture.md + audits external 004","D9","specifie","v4","rien a integrer (slicer v5)")
add("D9-02","three.js present dans proto (rendu, pas de CAD)","proto package.json","D9","fragment","v4","base du 3D objet")
add("D9-03","Espace objet 3D, CAO parametrique, CSG, import/export, impression","registre domaine 9 (missing)","D9","absent","v4","chantier neuf - apres v1-v3")
add("D9-04","Book of Shapes + audit CAD","docs/audits/external/002 et 004","D9","existe","v4","recherche deja faite")
# D10 Nexus/Agents
add("D10-01","nexus_os : 22 agents JSON, routeur multi-provider, skills, MCP, memoire, SSE, sandbox, evals (59 tests)","branche arena/01a08385-monorepo","D10","branche","v3","integrer apres le Core")
add("D10-02","13 fiches d'agents (orchestrateur, research, data, CAD, GIS, learning, verification...)","projects/COGNITORIUM/docs/agents","D10","specifie","v3","cahier des charges")
add("D10-03","Agent de recherche reaserch-engine (1 agent reel)","projects/reaserch-engine","D10","existe","v2","premier agent utile")
add("D10-04","Orchestrateur maison + MCP (ADR-008)","constitution/03-architecture.md","D10","specifie","v3","reconcilier avec nexus_os")
add("D10-05","Creator d'agents, evals, sandbox","nexus_os","D10","branche","v4","meta-outillage")
# D11 Data/Memory/Provenance
add("D11-01","Base unique PostgreSQL + pgvector + Apache AGE + PostGIS (ADR-007)","architecture/target.md + data-model.md","D11","specifie","v1","construire - fondation de tout")
add("D11-02","Schema bi-temporel (T valide + T' ingestion, invalidation, episodes)","absent du data-model (lecon Graphiti/Zep)","D11","absent","v1","acter avant premiere migration")
add("D11-03","HCSM : provenance, incertitude, observation/evidence/inference","projects/HCSM","D11","existe","v1","contrat semantique")
add("D11-04","JsonRunStore : 1 episode JSON atomique par run","reaserch-engine (engine/persistence.py)","D11","existe","v2","premier producteur d'episodes")
add("D11-05","Inventaires SHA-256, audit trail, import/export, frontiere vie privee, coffre a cles","registre domaine 11","D11","specifie","v2","hygiene de confiance")
add("D11-06","5 mecanismes de persistance heterogenes (localStorage x2, JSON, SQLite, 39 cles)","les 9 projets","D11","dette","v0","resorber par le Core")
add("D11-07","Memoire d'audit (state.json, MEMORY.md, JOURNAL.jsonl, graphe)","audit/","D11","existe","v1","outil de pilotage")
# D12 System/Settings
add("D12-01","Politique secrets : zero cle par defaut, .env 600, jamais commite, pas de 0.0.0.0","watchtower AGENTS.md + .env.example x4","D12","existe (partiel)","v1","generaliser")
add("D12-02","Licences : decider pour 6 projets ; attribuer le fork watchtower (MIT, Bilawal Sidhu)","audit C1","D12","manquant","v1","decider")
add("D12-03","Modes gratuit/payant + pre-validation des cles (keySetupCore.mjs)","projects/watchtower","D12","existe","v2","reutiliser tel quel")
add("D12-04","Provider manager multi-LLM, plugins, feature flags, diagnostics, backup","nexus_os + registre domaine 12","D12","branche/skeleton","v2","reutiliser")
add("D12-05","CI minimale (lint/build/tests) sur les 9 depots","audit C8 (1 CI sur 9)","D12","manquant","v1","garde-fou de restructuration")
# Transverse
add("T-01","PR #3 watchtower (CI verte)","branche arena/dec9cd88-watchtower","T","branche","v2","fusionner")
add("T-02","Branche watchtower +43 (UI reutilisable)","branche arena/01a072e1-watchtower","T","branche","v2","PR puis fusion")
add("T-03","ETAT +38 (agent, cosmos, 221 sorties)","branche arena/01a04f7b-ETAT-DE-LART","T","branche","v2","revue puis fusion")
add("T-04","Language-decoder (moteur + UI + tests)","branches arena/01a05471 et 01a05429","T","branche","v2","PR vers main")
add("T-05","proto resync (25 fichiers manquants dont auth/onboarding)","projects/proto-cognitorium","T","dette","v1","git pull + resync")
add("T-06","2 tests rouges reaserch-engine","tests/test_agents.py, tests/test_research_strategy.py","T","dette","v1","corriger")
add("T-07","19 branches mortes","9 depots","T","dette","v0","supprimer")
add("T-08","watchtower-mods (doublon 62/62)","projects/COGNITORIUM/watchtower-mods","T","doublon","v0","archiver")
add("T-09","Dossier de chantier en double (racine vs branche BTP)","monorepo","T","doublon","v0","dedupliquer")
add("T-10","289 Mo de binaires en Git (225 + 64 Mo)","racine + proto/raw","T","dette","v0","externaliser + SHA-256")
add("T-11","Donnees RH sensibles publiques (grilles salariales, corriges AIPR)","racine","T","risque","v0","retirer / restreindre")
add("T-12","Snapshot GitHub perime","data/github_inventory.json","T","dette","v1","regenerer + dater")
add("T-13","reaserch-engine mal orthographie","depot GitHub","T","dette","v1","renommer")
add("T-14","ADR-009 (3 bases de connaissances) non tranchee","COGNITORIUM","T","decision","v1","fermer l'ADR")
add("T-15","Doc animation-chronos inexistante","projects/animation-chronos","T","dette","v2","README d'intention ou archive")
for e in E:
    e["v_ordre"] = int(e["v"][1:])
E.sort(key=lambda e: (e["v_ordre"], e["domaine"], e["id"]))
out = {"audit":"audit-2026-10","genere":"2026-10-07","grille":"v1 socle | v2 coeur d'usage | v3 puissance | v4 conception | v5 horizon | v0 archive",
       "total":len(E),"elements":E}
json.dump(out, open("audit/data/importance.json","w"), ensure_ascii=False, indent=1)
from collections import Counter
c = Counter(e["v"] for e in E)
print("TOTAL:", len(E))
for k in ["v1","v2","v3","v4","v5","v0"]:
    print(f"  {k}: {c[k]}")
dc = Counter(e["domaine"] for e in E)
print("par domaine:", dict(sorted(dc.items())))
