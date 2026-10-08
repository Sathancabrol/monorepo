#!/usr/bin/env python3
"""Génère le dossier d'audit pour ArenaAI.

Entrées  : docs/recherche/02-MATRICE-DOMAINES.csv   (85 domaines déjà cadrés)
           docs/arena-audit/data/_verif-licences.tsv (contrôle gh api du 08/10/2026)
           docs/arena-audit/data/_licences-resolues.tsv (26 cas non standard, résolus à la main)
Sorties  : docs/arena-audit/data/licences-2026-10-08.tsv + .json
           docs/arena-audit/data/domaines.json
           docs/arena-audit/01-TABLEAU-DOMAINES.md
Rejouer  : python3 scripts/gen-dossier-arena.py
"""
from __future__ import annotations

import csv
import json
import re
import unicodedata
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
AUDIT = RACINE / "docs" / "arena-audit"
DATA = AUDIT / "data"

# ---------------------------------------------------------------------------
# 1. Licences : corrections humaines des cas que GitHub ne classe pas
# ---------------------------------------------------------------------------
OVERRIDES = {
    "CloudCompare/CloudCompare": "GPL-2.0",
    "FalkorDB/FalkorDB": "SSPL-1.0",
    "OSGeo/gdal": "MIT",
    "openscad/openscad": "GPL-2.0",
    "OpenTTD/OpenTTD": "GPL-2.0",
    "PDAL/PDAL": "BSD-3-Clause",
    "WorldPixelMap/android-gods-eye-view": "NON-COMMERCIAL",
    "bilawalsidhu/gods-eye-view": "MIT",
    "colmap/colmap": "BSD-3-Clause",
    "frida/frida": "wxWindows-Library-Licence-3.1",
    "graphdeco-inria/gaussian-splatting": "NON-COMMERCIAL",
    "mapbox/mapbox-gl-js": "PROPRIETAIRE (Mapbox TOS)",
    "maplibre/maplibre-gl-js": "BSD-3-Clause",
    "modelcontextprotocol/modelcontextprotocol": "Apache-2.0",
    "opendatalab/MinerU": "Apache-2.0",
    "organicmaps/organicmaps": "Apache-2.0",
    "OSGeo/PROJ": "MIT",
    "osmandapp/OsmAnd": "GPL-3.0",
    "potree/potree": "BSD (2 ou 3 clauses)",
    "protomaps/PMTiles": "BSD-3-Clause",
    "sqlite/sqlite": "Domaine public",
    "tldraw/tldraw": "Licence maison tldraw (filigrane)",
    "valhalla/valhalla": "MIT (à confirmer : voir COPYING)",
    "x64dbg/x64dbg": "GPL-3.0",
    "yjs/yjs": "MIT",
    "zed-industries/zed": "Apache-2.0 (crates) / GPL-3.0 (éditeur)",
}

# Ce que le risque signifie concrètement pour un projet qui veut pouvoir se monétiser
RISQUE = {
    "AGPL-3.0": "⚠️ Contamination réseau : si le code tourne dans un service exposé, tout le service doit être ouvert. Utilisable en outil interne séparé, PAS embarqué dans le cœur.",
    "GPL-2.0": "⚠️ Copyleft fort : utilisable comme outil externe lancé par l'app (sidecar), pas lié au cœur propriétaire/monétisé.",
    "GPL-3.0": "⚠️ Copyleft fort : idem GPL-2.0 + incompatibilité avec certains composants.",
    "LGPL-2.1": "🟡 Copyleft faible : liaison dynamique autorisée, ne pas modifier ni statiquement lier.",
    "LGPL-3.0": "🟡 Copyleft faible : liaison dynamique autorisée.",
    "MPL-2.0": "🟢 Fichier par fichier : modifications des fichiers MPL à republier seulement.",
    "SSPL-1.0": "⛔ Interdit d'offrir le logiciel en service sans ouvrir toute la pile. À ÉCARTER.",
    "NON-COMMERCIAL": "⛔ Usage commercial interdit. À ÉCARTER du produit (ok démo/recherche).",
    "PROPRIETAIRE (Mapbox TOS)": "⛔ Verrouillage fournisseur + facturation. À ÉCARTER.",
    "Licence maison tldraw (filigrane)": "⛔ Restriction + filigrane. À ÉCARTER.",
    "wxWindows-Library-Licence-3.1": "🟡 Type LGPL : ok en outil externe.",
    "Apache-2.0": "🟢 Permissive + clause brevets. Idéale.",
    "MIT": "🟢 Permissive maximale.",
    "BSD-3-Clause": "🟢 Permissive.",
    "BSD (2 ou 3 clauses)": "🟢 Permissive.",
    "Domaine public": "🟢 Aucune contrainte.",
    "CC-BY-4.0": "🟡 Attribution obligatoire (données).",
    "CC0-1.0": "🟢 Aucune contrainte.",
}


def charger_licences() -> dict[str, dict]:
    """Fusionne le contrôle automatique et les corrections humaines."""
    f = DATA / "licences-2026-10-08.tsv"
    if f.exists():
        base = f
    else:
        base = DATA / "_verif-licences.tsv"
    out: dict[str, dict] = {}
    with base.open(encoding="utf-8") as fh:
        for ligne in fh:
            cols = ligne.rstrip("\n").split("\t")
            if len(cols) < 6:
                continue
            repo, stars, licence, maj, archive, langage = cols[:6]
            if not stars.isdigit():          # ligne d'en-tête
                continue
            licence = OVERRIDES.get(repo, licence)
            if licence == "NOASSERTION":
                licence = "À LIRE"
            out[repo] = {
                "repo": repo, "etoiles": int(stars), "licence": licence,
                "maj": maj, "archive": archive == "true", "langage": langage,
                "risque": RISQUE.get(licence, "🟡 à qualifier"),
            }
    return out


# ---------------------------------------------------------------------------
# 2. Candidats vérifiés (citables tels quels, contrôle du 08/10/2026)
# ---------------------------------------------------------------------------
CANDIDATS = {
    "assistant_voix": ["adewaskar/jarvis"],
    "gis": ["maplibre/maplibre-gl-js", "maplibre/martin", "protomaps/PMTiles", "opengeos/GeoLibre",
            "OSGeo/gdal", "duckdb/duckdb-spatial", "osm-search/Nominatim", "Project-OSRM/osrm-backend",
            "valhalla/valhalla", "OSGeo/PROJ", "libgeos/geos"],
    "globe": ["CesiumGS/cesium", "visgl/deck.gl", "mrdoob/three.js", "bilawalsidhu/gods-eye-view",
              "WorldPixelMap/android-gods-eye-view"],
    "carte_hors_ligne": ["organicmaps/organicmaps", "osmandapp/OsmAnd", "kiwix/kiwix-tools", "openzim/zim-tools",
                         "Crosstalk-Solutions/project-nomad"],
    "graphe": ["LadybugDB/ladybug", "getzep/graphiti", "neo4j/neo4j", "FalkorDB/FalkorDB"],
    "donnees": ["duckdb/duckdb", "sqlite/sqlite", "apache/arrow", "pola-rs/polars", "apache/sedona",
                "postgis/postgis", "asg017/sqlite-vec"],
    "recherche": ["asg017/sqlite-vec"],
    "canvas": ["excalidraw/excalidraw", "tldraw/tldraw"],
    "plugins": ["extism/extism", "bytecodealliance/wasmtime", "modelcontextprotocol/modelcontextprotocol"],
    "agents": ["aaif-goose/goose", "OpenHands/OpenHands", "openclaw/openclaw", "Kc1t/alethe-agents",
               "modelcontextprotocol/modelcontextprotocol", "a2aproject/A2A", "agentclientprotocol/agent-client-protocol"],
    "ia_locale": ["ggml-org/llama.cpp", "ollama/ollama"],
    "sync": ["yjs/yjs", "automerge/automerge", "syncthing/syncthing"],
    "docs": ["tesseract-ocr/tesseract", "ocrmypdf/OCRmyPDF", "PaddlePaddle/PaddleOCR", "mindee/doctr",
             "apache/tika", "opendatalab/MinerU", "docling-project/docling", "VikParuchuri/marker",
             "Unstructured-IO/unstructured"],
    "bim": ["IfcOpenShell/IfcOpenShell", "ThatOpen/engine_components", "ThatOpen/engine_web-ifc",
            "xeokit/xeokit-sdk"],
    "cao": ["FreeCAD/FreeCAD", "openscad/openscad", "LinuxCNC/linuxcnc"],
    "pointcloud": ["PDAL/PDAL", "CloudCompare/CloudCompare", "potree/potree", "colmap/colmap"],
    "drone": ["OpenDroneMap/ODM", "WebODM/WebODM"],
    "splat": ["nerfstudio-project/gsplat", "ArthurBrussee/brush", "mkkellogg/GaussianSplats3D",
              "graphdeco-inria/gaussian-splatting", "nerfstudio-project/nerfstudio"],
    "simulation": ["mesa/mesa", "JuliaDynamics/Agents.jl"],
    "jeu": ["OpenTTD/OpenTTD", "OpenRCT2/OpenRCT2", "OpenMW/openmw", "freeciv/freeciv", "godotengine/godot"],
    "re": ["NationalSecurityAgency/ghidra", "rizinorg/rizin", "rizinorg/cutter", "x64dbg/x64dbg",
           "frida/frida", "skylot/jadx", "angr/angr"],
    "terrain": ["getodk/central", "kobotoolbox/kpi", "danielbrendel/hortusfox-web",
                "learningequality/kolibri"],
    "qualite": ["moj-analytical-services/splink"],
    "materiel": ["GuillaumeGomez/sysinfo", "gfx-rs/wgpu"],
    "papers": ["ourresearch/openalex-guts", "CrossRef/rest-api-doc", "docling-project/docling", "opendatalab/MinerU"],
}

# mots-clés → clés de CANDIDATS (l'ordre compte : les premiers trouvés priment)
DECLENCHEURS = [
    (r"assistant|voix|vocal|jarvis", "assistant_voix"),
    (r"cartograph|gis|géograph|geograph|sig |tuile|tile|satellit", "gis"),
    (r"\b3d\b|globe|webgl|rendu 3d|vue 3d|gaussian|splat|photogramm|nuage de points", "globe"),
    (r"hors.ligne|offline|kiwix|zim|nomad", "carte_hors_ligne"),
    (r"graphe|graph|knowledge|connaissance", "graphe"),
    (r"persistance|base|sql|données|dataset|stockage|entrepôt", "donnees"),
    (r"ctrl\+k|\bfts\b|sqlite-vec|recherche (globale|hybride|sémantique|unifiée)|search", "recherche"),
    (r"tableau blanc|canvas|schéma interactif|diagramme|dessin", "canvas"),
    (r"plugin|wasm|extension|sandbox|bac à sable", "plugins"),
    (r"agent|mcp|a2a|orchestr|multi-agent|automatis", "agents"),
    (r"ia locale|llm|inférence|inference|modèle local", "ia_locale"),
    (r"sync|synchronis|crdt|collaborat", "sync"),
    (r"\bocr\b|tesseract|pdf|extraction de tableau|extraction de données|obsidian|corpus documentaire|papier", "docs"),
    (r"bim|ifc|openbim|maquette numérique", "bim"),
    (r"cad|cao|conception|usinage|cnc|fabrication", "cao"),
    (r"nuage de point|scan|photogram", "pointcloud"),
    (r"drone|aérien|aerien|orthophoto|lidar", "drone"),
    (r"splat|nerf|reconstruction 3d|gaussienne", "splat"),
    (r"simulation|agent-based|monte.carlo|discrete|systemes|systèmes", "simulation"),
    (r"\bjeu\b|stratég|strateg|scénario|scenario|4x|grand strategy|mécaniques de", "jeu"),
    (r"reverse|binaire|décompil|debug|frida", "re"),
    (r"terrain|enquête|enquete|collecte|sondage|kobo|odk", "terrain"),
    (r"déduplication|deduplication|entité|entity resolution|rapprochement", "qualite"),
    (r"hardware|cpu|gpu|vram|profils eco|budget de ressources|détection matériel", "materiel"),
    (r"recherche scientifique|publications?|papers?|openalex|crossref|bibliograph", "papers"),
]

# ---------------------------------------------------------------------------
# 3. Chaque domaine → modules du shell + fiche concept art
# ---------------------------------------------------------------------------
MODULES_DU_SHELL = [
    (r"architect|core|événement|evenement|persistance|graphe|recherche|mémoire|memoire|contexte|entit|projet|identit|sécurit|securit|plugin|mcp|hardware|installateur|offline|dataset|observab|test|documentation|rgpd|repo|migration|coût|cout|shell ui|performance|contrat de module|synchronisation|gouvernance",
     ["systeme", "command"]),
    (r"cartograph|gis|géograph|territoire|timeline|temporel|digital twin|risque|climat|mobilité|mobilite|données géo", "carte"),
    (r"chantier|btp|ifc|bim|cad|3d|drone|scan|métré|metre|coût|prix|fabrication|slicer|sécurité chantier", "btp"),
    (r"cogni|hcsm|compétence|competence|métier|metier|learning|pédagog|pedagog|langage|psycho", "cognition"),
    (r"agent|osint|monitoring|veille|automatis|intelligence", "agents"),
    (r"document|ocr|extraction", "documents"),
    (r"simulation|scénario|scenario|stratég|jeu", "command"),
    (r"graph|graphe|connaissance", "graphe"),
    (r"marketplace|communauté|communaute", "systeme"),
]

ART = [
    (r"architect|core|shell ui|design|contrat de module|migration|coûts ia|gouvernance", "art-19"),
    (r"cartograph|gis|géograph|territoire|données géo", "art-02"),
    (r"digital twin|jumeau", "art-10"),
    (r"timeline|temporel|4d", "art-04"),
    (r"osint|monitoring|veille|renseignement", "art-03"),
    (r"graphe|graph|connaissance|mémoire|memoire", "art-06"),
    (r"entit|fiche", "art-05"),
    (r"agent|mcp|orchestr|verification|intégrateur|integrateur|research agent|repo", "art-07"),
    (r"repo|archéologie|archeologie|git", "art-08"),
    (r"chantier|btp|ifc|bim|métré|metre|prix|drone|scan|nuage", "art-09"),
    (r"cogni|hcsm|compétence|competence|métier|metier|profil", "art-11"),
    (r"learning|pédagog|pedagog|apprentissage", "art-12"),
    (r"recherche scientifique|papers|état de l'art|etat de l'art", "art-14"),
    (r"simulation|scénario|scenario|stratég|jeu", "art-15"),
    (r"source|preuve|licence|provenance", "art-18"),
    (r"cartograph|jumeau|3d|globe|nuage", "art-17"),
]

# ---------------------------------------------------------------------------
# 4. Ce que le dépôt contient déjà, domaine par domaine (vérifié le 08/10/2026)
# ---------------------------------------------------------------------------
EXISTANT = [
    (r"architect|contrat de module",
     "docs/carre-das/00→03 ; shell/ (portail 14 modules/104 fonctions, non encore branché aux données)"),
    (r"core|persistance|graphe|recherche|événement|contexte|entit",
     "prototypes dispersés : proto-cognitorium (210 fichiers, 87 Mo, graphe NetworkGraph/TreeView), watchtower (999 fichiers, 52 Mo)"),
    (r"plugin|mcp|wasm",
     "nexus_os/plugins.py + mcp.py + mcp_demo.py (branche arena_01a08385) : 8 303 lignes Python, 22 agents, 30 compétences, 8 fichiers de tests"),
    (r"agent",
     "nexus_os : 22 agents, 30 skills, runtime/harness/evals/context/memory/providers/creator ; Kc1t/alethe-agents (★832) et openclaw/openclaw (★391 640) à comparer"),
    (r"cartograph|gis|territoire|climat|mobilité",
     "watchtower/index.html (55 Ko) + branche arena_01a072e1 (comparatif Cesium 21 357 ms vs MapLibre 3 ms) ; frontignan (28 fichiers, 14 Mo, deck 18 slides)"),
    (r"timeline|temporel",
     "animation-chronos (36 fichiers, 5,3 Mo)"),
    (r"btp|chantier|ifc|métré|prix|drone|scan|cad",
     "branche arena_01a08449 : 22 rapports, 11 documents_sources, engine/btp_multi_agent.py ; corpus raw : 61 fichiers (43 PDF, 5 xlsm) dont DCE/CCTP/CCAP/BPU, signalisation OPPBTP, AIPR"),
    (r"cogni|hcsm|compétence|métier|profil|psycho",
     "COGNITORIUM (131 fichiers, 24 Mo), proto-cognitorium (87 Mo), HCSM (87 fichiers), ETAT-DE-LART-PSYCHOLOGIE (37 fichiers) + 137 Ko de code récupéré du patch 01a0389d, docs/carre-das/07"),
    (r"langage",
     "Language-decoder (2 branches dans _incoming)"),
    (r"learning|pédagog",
     "docs/carre-das/07 (Learning Engine en V2) ; CLE défini dans les documents de cadrage"),
    (r"document|ocr|extraction",
     "corpus raw (43 PDF) ; docs/recherche/03 (Marker, MinerU, Docling déjà arbitrés)"),
    (r"recherche scientifique|papers",
     "reaserch-engine (61 fichiers, 301 Ko)"),
    (r"simulation|scénario|jeu|stratég",
     "docs/recherche/02 (D64→D68) ; aucune base de code"),
    (r"repos|git|migration|documentation",
     "9 projets + 13 branches ; _incoming 859 fichiers/31 Mo ; scripts/verif-completude-repos.py : 2 157 fichiers, 0 manquant"),
]

# ---------------------------------------------------------------------------
# 5. Les 85 domaines existants + 8 ajouts issus du tableau du 08/10/2026
# ---------------------------------------------------------------------------
AJOUTS = [
    ("D86", "World", "Synchronisation 2D ↔ 3D ↔ Temps (sélection unifiée)", "P0",
     "watchtower (2D/3D) + animation-chronos + proto-cognitorium (graphe temporel)",
     "Comment relient-ils carte, globe, timeline et fiche entité chez Palantir Gotham, Kepler.gl, QGIS (plugins de synchronisation) ? Un seul modèle d'état partagé ?",
     "deck.gl + MapLibre + Cesium, maplibre-gl-sync-move, Kepler.gl, LadybugDB",
     "Définir le contrat de synchronisation des vues (un identifiant sélectionné → toutes les vues réagissent)",
     "Sélectionner un objet sur la carte met à jour 3D, timeline et dossier en moins de 100 ms"),
    ("D87", "Knowledge", "Language Decoder (langage & cognition)", "P1",
     "Language-decoder, 2 branches dans _incoming",
     "Analyse linguistique locale : spaCy FR, Stanza, UDPipe, LanguageTool, modèles HF de parsing",
     "spaCy (MIT), Stanza (Apache-2.0), LanguageTool (LGPL-2.1), UDPipe (MPL-2.0)",
     "Brancher le décodeur comme compétence du profil cognitif (module langage)",
     "Un texte fourni produit une analyse réutilisable par le profil"),
    ("D88", "BTP", "Conformité & sécurité chantier (DT/DICT/AIPR, OPPBTP)", "P0",
     "corpus raw : signalisation OPPBTP, AIPR ×3, pv de marquage, guide croisement réseaux, DT/DICT",
     "Automatisation des DT/DICT (déclaration de travaux) : existe-t-il des API/SDK ouverts (reseaux-et-canalisations.ineris.fr, Réseaux et Canalisations) ?",
     "Réseaux et Canalisations (service public FR), INERIS, référentiels OPPBTP",
     "Construire le contrôle de conformité (DT/DICT, AIPR, signalisation) à partir du corpus",
     "Un chantier déclaré soulève les obligations manquantes avant travaux"),
    ("D89", "Fondations", "Registre d'outils (Tool Registry)", "P0",
     "nexus_os/tools + 30 skills",
     "Comment Goose, OpenHands, OpenClaw, Alethe déclarent-ils leurs outils ? Y a-t-il un format commun (MCP tools, JSON Schema) ?",
     "MCP (spécification), aaif-goose/goose, OpenHands/OpenHands, openclaw/openclaw",
     "Définir le format unique de déclaration d'un outil (schéma d'entrée/sortie, permissions)",
     "Ajouter un outil = un fichier de description, sans toucher au reste"),
    ("D90", "Agents", "Compétences d'agents (Skill Registry)", "P0",
     "nexus_os : 30 compétences Python",
     "Comment Alethe et OpenClaw empaquettent-ils des compétences réutilisables (dossiers, manifestes, résolution) ?",
     "Kc1t/alethe-agents, openclaw/openclaw, aaif-goose/goose",
     "Unifier skills et plugins sous un même manifeste (module.json)",
     "Une compétence écrite une fois est utilisable par tous les agents"),
    ("D91", "Fondations", "Mise à jour & retour arrière (Update Manager)", "P1",
     "décidé dans docs/carre-das/00 (MAJ signée + rollback)",
     "Mécanique de mise à jour Tauri (tauri-plugin-updater, signatures), stratégies de migration locale des données",
     "tauri-apps/plugins-workspace, mécanismes NSIS/MSIX, delta updates",
     "Implémenter : canal stable, signature, migration de schéma, retour arrière en un clic",
     "Une mise à jour échouée revient à l'état précédent sans perte"),
    ("D92", "Plateforme", "Collaboration & partage (multi-utilisateur)", "P2",
     "aucun",
     "Partage local-first : Automerge/Yjs + serveur minimal, partage de projet par dossier, pas de compte obligatoire",
     "yjs/yjs (MIT), automerge/automerge (MIT), syncthing/syncthing (MPL-2.0)",
     "Définir si le partage arrive en V2 (aujourd'hui : mono-utilisateur assumé)",
     "Deux postes peuvent partager un dossier projet sans serveur central"),
    ("D93", "Plateforme", "Benchmark & santé des briques (veille continue)", "P0",
     "aucun ; docs/recherche/03 contient des mesures ponctuelles (Cesium 21 357 ms vs MapLibre 3 ms)",
     "Comment mesurer et suivre la santé d'une dépendance (activité, bus factor, issues ouvertes, temps de réponse, RAM) ? Outils : OpenSSF Scorecard, deps.dev, endoflife.date",
     "ossf/scorecard, deps.dev API, libs.io, OpenHub",
     "Automatiser une fiche de santé par dépendance, rejouée à chaque montée de version",
     "Toute dépendance a une fiche santé datée et un plan de remplacement"),
]


def norm(t: str) -> str:
    t = unicodedata.normalize("NFKD", t.lower())
    return "".join(c for c in t if not unicodedata.combining(c))


CHAMPS = ("id", "groupe", "domaine", "priorite", "existant_interne",
          "ce_quil_faut_rechercher", "pistes_a_verifier", "decision_attendue", "critere_de_succes")


def charger_domaines() -> list[dict]:
    with (RACINE / "docs" / "recherche" / "02-MATRICE-DOMAINES.csv").open(encoding="utf-8") as fh:
        lignes = list(csv.DictReader(fh))
    domaine_par_id = {a[0]: dict(zip(CHAMPS, a)) for a in AJOUTS}
    for d in lignes:
        domaine_par_id[d["id"]] = d
    ordre = [d["id"] for d in lignes] + [a[0] for a in AJOUTS]
    return [domaine_par_id[i] for i in ordre]


def cle_domaine(d: dict) -> str:
    """id court et stable, utilisable par ArenaAI dans ses livrables."""
    return d["id"]


def enrichir(d: dict, licences: dict[str, dict]) -> dict:
    texte = norm(" ".join(d.get(k, "") or "" for k in
                          ("domaine", "ce_quil_faut_rechercher", "pistes_a_verifier", "existant_interne")))
    cand, vus = [], set()
    for motif, cle in DECLENCHEURS:
        if re.search(motif, texte):
            for r in CANDIDATS[cle]:
                if r not in vus and r in licences:
                    vus.add(r)
                    i = licences[r]
                    cand.append(f"{r} ★{i['etoiles']:,} [{i['licence']}]".replace(",", " "))
    mods: list[str] = []
    for motif, ms in MODULES_DU_SHELL:
        if re.search(motif, texte):
            mods.extend(m for m in ms if m not in mods)
    art = next((a for motif, a in ART if re.search(motif, texte)), "art-19")
    existant = next((e for motif, e in EXISTANT if re.search(motif, texte)), "")
    COURT = {
        "AGPL-3.0": "copyleft réseau", "GPL-2.0": "copyleft fort", "GPL-3.0": "copyleft fort",
        "LGPL-2.1": "copyleft faible", "LGPL-3.0": "copyleft faible", "MPL-2.0": "fichier par fichier",
        "SSPL-1.0": "⛔ à écarter", "NON-COMMERCIAL": "⛔ à écarter", "PROPRIETAIRE (Mapbox TOS)": "⛔ à écarter",
        "Licence maison tldraw (filigrane)": "⛔ à écarter", "wxWindows-Library-Licence-3.1": "type LGPL",
    }
    risques = [f"{r} [{licences[r]['licence']}] : {COURT.get(licences[r]['licence'], 'à qualifier')}"
               for r in vus if licences[r]["licence"] in COURT]
    return {
        **d,
        "cle": cle_domaine(d),
        "modules_shell": mods,
        "fiche_art": art,
        "candidats_verifies_2026_10_08": cand[:12],
        "existant_verifie": existant,
        "risques_licence": risques,
    }


def ecrire_tableau(domaines: list[dict]) -> None:
    par_groupe: dict[str, list[dict]] = {}
    for d in domaines:
        par_groupe.setdefault(d["groupe"], []).append(d)
    lignes = [
        "# Tableau maître des domaines — Carré d'As",
        "",
        "> **93 domaines** : les **85 déjà cadrés** (`docs/recherche/02-MATRICE-DOMAINES.csv`) augmentés de **8 manquants**",
        "> identifiés le 08/10/2026 (D86 → D93). Chaque domaine a : son état **vérifié**, ses **candidats testés le 08/10/2026**",
        "> (étoiles + licence contrôlées par l'API GitHub), **ce qu'ArenaAI doit auditer**, ce qu'il faut **construire**, la **décision attendue**",
        "> et la **fiche concept art** correspondante (`02-CONCEPT-ART-ET-PROMPTS.md`).",
        "",
        "> ⚠️ Colonne « Candidats » : ce sont des **pistes vérifiées**, pas des choix. Le travail d'ArenaAI est de",
        "> **trancher** (conserver / fusionner / remplacer / adapter / plugin / réécrire / abandonner) avec preuves à l'appui.",
        "",
        "---",
        "",
    ]
    for groupe, items in par_groupe.items():
        lignes += [f"## {groupe} — {len(items)} domaines", ""]
        for d in items:
            lignes.append(f"### {d['id']} · {d['domaine']} — *{d['priorite']}*")
            if d.get("existant_verifie"):
                lignes.append(f"- **Dans le dépôt** : {d['existant_verifie']}")
            for champ, titre in (("existant_interne", "Existant (cadrage initial)"),
                                 ("ce_quil_faut_rechercher", "À auditer par ArenaAI"),
                                 ("pistes_a_verifier", "Pistes d'origine à vérifier"),
                                 ("decision_attendue", "Décision attendue"),
                                 ("critere_de_succes", "Critère de succès")):
                if d.get(champ):
                    lignes.append(f"- **{titre}** : {d[champ]}")
            if d["candidats_verifies_2026_10_08"]:
                lignes.append("- **Candidats vérifiés (08/10/2026)** : " + " · ".join(d["candidats_verifies_2026_10_08"]))
            for r in d["risques_licence"]:
                lignes.append(f"- **⚠️ Licence** : {r}")
            if d["modules_shell"]:
                lignes.append(f"- **Modules du shell concernés** : {', '.join(d['modules_shell'])}")
            lignes.append(f"- **Concept art** : `{d['fiche_art']}`")
            lignes.append("")
    (AUDIT / "01-TABLEAU-DOMAINES.md").write_text("\n".join(lignes) + "\n", encoding="utf-8")


def ecrire_licences_md(licences: dict[str, dict]) -> None:
    ordre = {"⛔": 0, "⚠️": 1, "🟡": 2, "🟢": 3}
    def rang(i):
        return (ordre.get(i["risque"][0], 4), -i["etoiles"])
    lignes = [
        "# Matrice de licences vérifiée — 8 octobre 2026",
        "",
        "> **97 dépôts** contrôlés un par un via l'API GitHub le 08/10/2026 (licence déclarée + lecture du fichier de licence",
        "> pour les 26 cas que GitHub ne classait pas). **C'est la « License Matrix » qui conditionne la monétisation future.**",
        "",
        "## La règle, en une phrase",
        "",
        "**On ne met dans le cœur (le code qui sera distribué et vendable) que du 🟢 permissif.** Tout ⚠️ copyleft fort ou",
        "tout ⛔ devient soit un **outil externe lancé par l'application** (aucun lien de code), soit un **plugin optionnel",
        "téléchargé séparément et désactivable**, soit il est **abandonné**.",
        "",
        "| Niveau | Ce que ça permet | Exemples relevés |",
        "|---|---|---|",
        "| 🟢 Permissif | Lier, modifier, vendre | MIT, Apache-2.0, BSD, domaine public, MPL-2.0 |",
        "| 🟡 Copyleft faible | Lier dynamiquement sans ouvrir son code | LGPL-2.1/3.0, wxWindows |",
        "| ⚠️ Copyleft fort | Outil externe seulement (le lien contamine) | GPL-2.0/3.0, AGPL-3.0 (contamination **réseau**) |",
        "| ⛔ Inutilisable | Interdiction commerciale ou verrouillage | SSPL, non-commercial, TOS propriétaire |",
        "",
        "## Les pièges trouvés (à ne pas reproduire)",
        "",
        "| Dépôt | Licence réelle | Conséquence |",
        "|---|---|---|",
        "| `mapbox/mapbox-gl-js` | **propriétaire (TOS Mapbox)** | Le tableau ci-dessus citait « Mapbox » : à remplacer par **MapLibre** (BSD-3, fork communautaire) |",
        "| `FalkorDB/FalkorDB` | **SSPL-1.0** | Exclu du produit. Le moteur de graphe retenu est **LadybugDB (MIT)** |",
        "| `graphdeco-inria/gaussian-splatting` | **non-commercial (INRIA)** | L'implémentation de référence est interdite en produit : utiliser **gsplat (Apache-2.0)**, **Brush (Apache-2.0)** ou **GaussianSplats3D (MIT)** |",
        "| `WorldPixelMap/android-gods-eye-view` | **non-commercial** | Superbe démo, mais interdite en produit |",
        "| `tldraw/tldraw` | **licence maison + filigrane** | À écarter (utiliser **Excalidraw** MIT pour le tableau blanc) |",
        "| `OpenDroneMap/ODM`, `WebODM` | **AGPL-3.0** | Traitement photogrammétrique : à lancer comme **outil externe séparé** (et le préciser), jamais embarqué |",
        "| `osmandapp/OsmAnd`, `x64dbg`, `CloudCompare`, `OpenSCAD`, `OpenTTD` | GPL | Outils externes / inspiration, jamais liés |",
        "| `osmandapp/OsmAnd` vs `organicmaps` | GPL-3.0 vs **Apache-2.0** | Pour les cartes hors ligne, **Organic Maps** est juridiquement plus simple |",
        "| `zed-industries/zed` | Apache-2.0 (crates) / **GPL-3.0** (éditeur) | Ne réutiliser que les crates |",
        "",
        "## Le tableau complet",
        "",
        "| Dépôt | ★ | Licence | Dernière publication | Risque |",
        "|---|---|---|---|---|",
    ]
    for i in sorted(licences.values(), key=rang):
        lignes.append(f"| `{i['repo']}` | {i['etoiles']:,} | {i['licence']} | {i['maj']} | {i['risque']} |".replace(",", " "))
    lignes += [
        "",
        "## Ce qu'ArenaAI doit ajouter à cette matrice",
        "",
        "1. **Les données, pas seulement le code** : licences des jeux de données (IGN, OSM/ODbL, ROME, ESCO, O*NET, OpenAlex, INSEE),",
        "   avec la clause d'attribution exacte à afficher dans l'application.",
        "2. **Les modèles IA** : poids et licences (Apache-2.0, Gemma, Llama Community, CC-BY-NC), y compris les restrictions de redistribution.",
        "3. **Les polices et les icônes** (Inter, JetBrains Mono, Material Symbols…).",
        "4. **La voie de sortie** : pour chaque dépendance ⚠️, quel remplaçant permissif existe, et quel effort pour y passer.",
        "",
    ]
    (AUDIT / "03-LICENCES-VERIFIEES.md").write_text("\n".join(lignes) + "\n", encoding="utf-8")


def main() -> int:
    DATA.mkdir(parents=True, exist_ok=True)
    licences = charger_licences()

    # fichier de licences propre
    with (DATA / "licences-2026-10-08.tsv").open("w", encoding="utf-8") as fh:
        fh.write("repo\tetoiles\tlicence\tderniere_publication\tarchive\tlangage\trisque\n")
        for r in sorted(licences.values(), key=lambda x: x["repo"]):
            fh.write(f"{r['repo']}\t{r['etoiles']}\t{r['licence']}\t{r['maj']}\t{r['archive']}\t{r['langage']}\t{r['risque']}\n")
    (DATA / "licences-2026-10-08.json").write_text(
        json.dumps(sorted(licences.values(), key=lambda x: x["repo"]), ensure_ascii=False, indent=1), encoding="utf-8")

    domaines = [enrichir(d, licences) for d in charger_domaines()]
    (DATA / "domaines.json").write_text(json.dumps({
        "genere_le": "2026-10-08",
        "total": len(domaines),
        "source": "docs/recherche/02-MATRICE-DOMAINES.csv + 8 ajouts du 2026-10-08",
        "domaines": domaines,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    ecrire_tableau(domaines)
    ecrire_licences_md(licences)

    par_prio: dict[str, int] = {}
    for d in domaines:
        par_prio[d["priorite"]] = par_prio.get(d["priorite"], 0) + 1
    print(f"✓ {len(domaines)} domaines · {len(licences)} dépôts vérifiés")
    print("  priorités : " + " · ".join(f"{k} {v}" for k, v in sorted(par_prio.items())))
    print(f"  → {AUDIT/'01-TABLEAU-DOMAINES.md'}")
    print(f"  → {DATA/'domaines.json'}  ·  {DATA/'licences-2026-10-08.tsv'}")
    print(f"  → {AUDIT/'03-LICENCES-VERIFIEES.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
