# Matrice de licences vérifiée — 8 octobre 2026

> **97 dépôts** contrôlés un par un via l'API GitHub le 08/10/2026 (licence déclarée + lecture du fichier de licence
> pour les 26 cas que GitHub ne classait pas). **C'est la « License Matrix » qui conditionne la monétisation future.**

## La règle, en une phrase

**On ne met dans le cœur (le code qui sera distribué et vendable) que du 🟢 permissif.** Tout ⚠️ copyleft fort ou
tout ⛔ devient soit un **outil externe lancé par l'application** (aucun lien de code), soit un **plugin optionnel
téléchargé séparément et désactivable**, soit il est **abandonné**.

| Niveau | Ce que ça permet | Exemples relevés |
|---|---|---|
| 🟢 Permissif | Lier, modifier, vendre | MIT, Apache-2.0, BSD, domaine public, MPL-2.0 |
| 🟡 Copyleft faible | Lier dynamiquement sans ouvrir son code | LGPL-2.1/3.0, wxWindows |
| ⚠️ Copyleft fort | Outil externe seulement (le lien contamine) | GPL-2.0/3.0, AGPL-3.0 (contamination **réseau**) |
| ⛔ Inutilisable | Interdiction commerciale ou verrouillage | SSPL, non-commercial, TOS propriétaire |

## Les pièges trouvés (à ne pas reproduire)

| Dépôt | Licence réelle | Conséquence |
|---|---|---|
| `mapbox/mapbox-gl-js` | **propriétaire (TOS Mapbox)** | Le tableau ci-dessus citait « Mapbox » : à remplacer par **MapLibre** (BSD-3, fork communautaire) |
| `FalkorDB/FalkorDB` | **SSPL-1.0** | Exclu du produit. Le moteur de graphe retenu est **LadybugDB (MIT)** |
| `graphdeco-inria/gaussian-splatting` | **non-commercial (INRIA)** | L'implémentation de référence est interdite en produit : utiliser **gsplat (Apache-2.0)**, **Brush (Apache-2.0)** ou **GaussianSplats3D (MIT)** |
| `WorldPixelMap/android-gods-eye-view` | **non-commercial** | Superbe démo, mais interdite en produit |
| `tldraw/tldraw` | **licence maison + filigrane** | À écarter (utiliser **Excalidraw** MIT pour le tableau blanc) |
| `OpenDroneMap/ODM`, `WebODM` | **AGPL-3.0** | Traitement photogrammétrique : à lancer comme **outil externe séparé** (et le préciser), jamais embarqué |
| `osmandapp/OsmAnd`, `x64dbg`, `CloudCompare`, `OpenSCAD`, `OpenTTD` | GPL | Outils externes / inspiration, jamais liés |
| `osmandapp/OsmAnd` vs `organicmaps` | GPL-3.0 vs **Apache-2.0** | Pour les cartes hors ligne, **Organic Maps** est juridiquement plus simple |
| `zed-industries/zed` | Apache-2.0 (crates) / **GPL-3.0** (éditeur) | Ne réutiliser que les crates |

## Le tableau complet

| Dépôt | ★ | Licence | Dernière publication | Risque |
|---|---|---|---|---|
| `tldraw/tldraw` | 50 814 | Licence maison tldraw (filigrane) | 2026-10-07 | ⛔ Restriction + filigrane. À ÉCARTER. |
| `graphdeco-inria/gaussian-splatting` | 24 137 | NON-COMMERCIAL | 2025-10-17 | ⛔ Usage commercial interdit. À ÉCARTER du produit (ok démo/recherche). |
| `mapbox/mapbox-gl-js` | 12 437 | PROPRIETAIRE (Mapbox TOS) | 2026-10-08 | ⛔ Verrouillage fournisseur + facturation. À ÉCARTER. |
| `FalkorDB/FalkorDB` | 7 967 | SSPL-1.0 | 2026-10-08 | ⛔ Interdit d'offrir le logiciel en service sans ouvrir toute la pile. À ÉCARTER. |
| `WorldPixelMap/android-gods-eye-view` | 38 | NON-COMMERCIAL | 2026-09-10 | ⛔ Usage commercial interdit. À ÉCARTER du produit (ok démo/recherche). |
| `EbookFoundation/free-programming-books` | 398 700 | CC-BY-4.0 | 2026-10-05 | 🟡 Attribution obligatoire (données). |
| `zed-industries/zed` | 91 449 | Apache-2.0 (crates) / GPL-3.0 (éditeur) | 2026-10-08 | 🟡 à qualifier |
| `FreeCAD/FreeCAD` | 34 025 | LGPL-2.1 | 2026-10-08 | 🟡 Copyleft faible : liaison dynamique autorisée  ne pas modifier ni statiquement lier. |
| `frida/frida` | 22 146 | wxWindows-Library-Licence-3.1 | 2026-10-08 | 🟡 Type LGPL : ok en outil externe. |
| `angr/angr` | 9 131 | BSD-2-Clause | 2026-10-08 | 🟡 à qualifier |
| `Project-OSRM/osrm-backend` | 8 126 | BSD-2-Clause | 2026-10-07 | 🟡 à qualifier |
| `valhalla/valhalla` | 6 292 | MIT (à confirmer : voir COPYING) | 2026-10-08 | 🟡 à qualifier |
| `rizinorg/rizin` | 3 942 | LGPL-3.0 | 2026-10-08 | 🟡 Copyleft faible : liaison dynamique autorisée. |
| `IfcOpenShell/IfcOpenShell` | 2 841 | LGPL-3.0 | 2026-10-08 | 🟡 Copyleft faible : liaison dynamique autorisée. |
| `libgeos/geos` | 1 513 | LGPL-2.1 | 2026-10-05 | 🟡 Copyleft faible : liaison dynamique autorisée  ne pas modifier ni statiquement lier. |
| `CrossRef/rest-api-doc` | 801 | MIT (doc propriétaire) | 2024-09-25 | 🟡 à qualifier |
| `LadybugDB/bugscope-tauri` | 18 | NONE | 2026-09-24 | 🟡 à qualifier |
| `openclaw/openclaw` | 391 640 | MIT | 2026-10-08 | 🟢 Permissive maximale. |
| `ollama/ollama` | 182 569 | MIT | 2026-10-08 | 🟢 Permissive maximale. |
| `excalidraw/excalidraw` | 133 685 | MIT | 2026-10-08 | 🟢 Permissive maximale. |
| `ggml-org/llama.cpp` | 130 687 | MIT | 2026-10-08 | 🟢 Permissive maximale. |
| `godotengine/godot` | 118 272 | MIT | 2026-10-07 | 🟢 Permissive maximale. |
| `mrdoob/three.js` | 116 356 | MIT | 2026-10-08 | 🟢 Permissive maximale. |
| `tauri-apps/tauri` | 111 674 | Apache-2.0 | 2026-10-08 | 🟢 Permissive + clause brevets. Idéale. |
| `PaddlePaddle/PaddleOCR` | 90 775 | Apache-2.0 | 2026-09-16 | 🟢 Permissive + clause brevets. Idéale. |
| `OpenHands/OpenHands` | 90 275 | MIT | 2026-10-08 | 🟢 Permissive maximale. |
| `syncthing/syncthing` | 89 219 | MPL-2.0 | 2026-10-08 | 🟢 Fichier par fichier : modifications des fichiers MPL à republier seulement. |
| `NationalSecurityAgency/ghidra` | 81 650 | Apache-2.0 | 2026-10-08 | 🟢 Permissive + clause brevets. Idéale. |
| `opendatalab/MinerU` | 81 295 | Apache-2.0 | 2026-10-06 | 🟢 Permissive + clause brevets. Idéale. |
| `tesseract-ocr/tesseract` | 76 861 | Apache-2.0 | 2026-10-08 | 🟢 Permissive + clause brevets. Idéale. |
| `docling-project/docling` | 68 537 | MIT | 2026-10-08 | 🟢 Permissive maximale. |
| `aaif-goose/goose` | 55 067 | Apache-2.0 | 2026-10-08 | 🟢 Permissive + clause brevets. Idéale. |
| `skylot/jadx` | 50 780 | Apache-2.0 | 2026-10-07 | 🟢 Permissive + clause brevets. Idéale. |
| `bilawalsidhu/gods-eye-view` | 49 027 | MIT | 2026-10-07 | 🟢 Permissive maximale. |
| `duckdb/duckdb` | 41 982 | MIT | 2026-10-08 | 🟢 Permissive maximale. |
| `datalab-to/marker` | 40 265 | Apache-2.0 | 2026-10-02 | 🟢 Permissive + clause brevets. Idéale. |
| `pola-rs/polars` | 40 008 | MIT | 2026-10-08 | 🟢 Permissive maximale. |
| `Crosstalk-Solutions/project-nomad` | 39 287 | Apache-2.0 | 2026-10-07 | 🟢 Permissive + clause brevets. Idéale. |
| `ocrmypdf/OCRmyPDF` | 34 960 | MPL-2.0 | 2026-10-07 | 🟢 Fichier par fichier : modifications des fichiers MPL à republier seulement. |
| `getzep/graphiti` | 31 553 | Apache-2.0 | 2026-10-07 | 🟢 Permissive + clause brevets. Idéale. |
| `a2aproject/A2A` | 26 073 | Apache-2.0 | 2026-10-08 | 🟢 Permissive + clause brevets. Idéale. |
| `yjs/yjs` | 22 910 | MIT | 2026-10-07 | 🟢 Permissive maximale. |
| `bytecodealliance/wasmtime` | 18 698 | Apache-2.0 | 2026-10-07 | 🟢 Permissive + clause brevets. Idéale. |
| `gfx-rs/wgpu` | 18 234 | Apache-2.0 | 2026-10-08 | 🟢 Permissive + clause brevets. Idéale. |
| `apache/arrow` | 17 188 | Apache-2.0 | 2026-10-08 | 🟢 Permissive + clause brevets. Idéale. |
| `CesiumGS/cesium` | 15 811 | Apache-2.0 | 2026-10-08 | 🟢 Permissive + clause brevets. Idéale. |
| `organicmaps/organicmaps` | 15 613 | Apache-2.0 | 2026-10-08 | 🟢 Permissive + clause brevets. Idéale. |
| `Unstructured-IO/unstructured` | 15 548 | Apache-2.0 | 2026-10-08 | 🟢 Permissive + clause brevets. Idéale. |
| `visgl/deck.gl` | 14 636 | MIT | 2026-10-07 | 🟢 Permissive maximale. |
| `colmap/colmap` | 12 874 | BSD-3-Clause | 2026-10-08 | 🟢 Permissive. |
| `nerfstudio-project/nerfstudio` | 12 053 | Apache-2.0 | 2025-07-29 | 🟢 Permissive + clause brevets. Idéale. |
| `maplibre/maplibre-gl-js` | 11 825 | BSD-3-Clause | 2026-10-08 | 🟢 Permissive. |
| `sqlite/sqlite` | 10 620 | Domaine public | 2026-10-08 | 🟢 Aucune contrainte. |
| `modelcontextprotocol/modelcontextprotocol` | 9 406 | Apache-2.0 | 2026-10-08 | 🟢 Permissive + clause brevets. Idéale. |
| `asg017/sqlite-vec` | 8 170 | Apache-2.0 | 2026-05-18 | 🟢 Permissive + clause brevets. Idéale. |
| `opengeos/GeoLibre` | 7 871 | MIT | 2026-10-08 | 🟢 Permissive maximale. |
| `automerge/automerge` | 6 650 | MIT | 2026-10-08 | 🟢 Permissive maximale. |
| `mindee/doctr` | 6 381 | Apache-2.0 | 2026-10-07 | 🟢 Permissive + clause brevets. Idéale. |
| `OSGeo/gdal` | 6 087 | MIT | 2026-10-08 | 🟢 Permissive maximale. |
| `extism/extism` | 5 789 | BSD-3-Clause | 2026-09-02 | 🟢 Permissive. |
| `potree/potree` | 5 632 | BSD (2 ou 3 clauses) | 2026-01-08 | 🟢 Permissive. |
| `agentclientprotocol/agent-client-protocol` | 4 391 | Apache-2.0 | 2026-10-08 | 🟢 Permissive + clause brevets. Idéale. |
| `apache/tika` | 4 091 | Apache-2.0 | 2026-10-07 | 🟢 Permissive + clause brevets. Idéale. |
| `maplibre/martin` | 3 983 | Apache-2.0 | 2026-10-08 | 🟢 Permissive + clause brevets. Idéale. |
| `mesa/mesa` | 3 877 | Apache-2.0 | 2026-10-06 | 🟢 Permissive + clause brevets. Idéale. |
| `protomaps/PMTiles` | 3 074 | BSD-3-Clause | 2026-09-16 | 🟢 Permissive. |
| `mkkellogg/GaussianSplats3D` | 2 904 | MIT | 2025-10-19 | 🟢 Permissive maximale. |
| `GuillaumeGomez/sysinfo` | 2 748 | MIT | 2026-10-04 | 🟢 Permissive maximale. |
| `moj-analytical-services/splink` | 2 462 | MIT | 2026-10-06 | 🟢 Permissive maximale. |
| `OSGeo/PROJ` | 2 030 | MIT | 2026-10-08 | 🟢 Permissive maximale. |
| `LadybugDB/ladybug` | 1 825 | MIT | 2026-10-08 | 🟢 Permissive maximale. |
| `danielbrendel/hortusfox-web` | 1 680 | MIT | 2026-10-05 | 🟢 Permissive maximale. |
| `PDAL/PDAL` | 1 422 | BSD-3-Clause | 2026-10-07 | 🟢 Permissive. |
| `learningequality/kolibri` | 1 136 | MIT | 2026-10-07 | 🟢 Permissive maximale. |
| `ThatOpen/engine_web-ifc` | 1 057 | MPL-2.0 | 2026-10-08 | 🟢 Fichier par fichier : modifications des fichiers MPL à republier seulement. |
| `JuliaDynamics/Agents.jl` | 919 | MIT | 2026-09-15 | 🟢 Permissive maximale. |
| `duckdb/duckdb-spatial` | 714 | MIT | 2026-10-01 | 🟢 Permissive maximale. |
| `ThatOpen/engine_components` | 710 | MIT | 2026-10-06 | 🟢 Permissive maximale. |
| `adewaskar/jarvis` | 412 | MIT | 2026-08-05 | 🟢 Permissive maximale. |
| `getodk/central` | 228 | Apache-2.0 | 2026-10-07 | 🟢 Permissive + clause brevets. Idéale. |
| `ourresearch/openalex-guts` | 157 | MIT | 2026-03-06 | 🟢 Permissive maximale. |
| `x64dbg/x64dbg` | 49 739 | GPL-3.0 | 2026-10-01 | ⚠️ Copyleft fort : idem GPL-2.0 + incompatibilité avec certains composants. |
| `rizinorg/cutter` | 19 942 | GPL-3.0 | 2026-09-11 | ⚠️ Copyleft fort : idem GPL-2.0 + incompatibilité avec certains composants. |
| `neo4j/neo4j` | 17 284 | GPL-3.0 | 2026-09-22 | ⚠️ Copyleft fort : idem GPL-2.0 + incompatibilité avec certains composants. |
| `OpenRCT2/OpenRCT2` | 16 397 | GPL-3.0 | 2026-10-07 | ⚠️ Copyleft fort : idem GPL-2.0 + incompatibilité avec certains composants. |
| `qgis/QGIS` | 14 483 | GPL-2.0 | 2026-10-08 | ⚠️ Copyleft fort : utilisable comme outil externe lancé par l'app (sidecar)  pas lié au cœur propriétaire/monétisé. |
| `openscad/openscad` | 10 392 | GPL-2.0 | 2026-10-08 | ⚠️ Copyleft fort : utilisable comme outil externe lancé par l'app (sidecar)  pas lié au cœur propriétaire/monétisé. |
| `OpenTTD/OpenTTD` | 8 345 | GPL-2.0 | 2026-10-08 | ⚠️ Copyleft fort : utilisable comme outil externe lancé par l'app (sidecar)  pas lié au cœur propriétaire/monétisé. |
| `OpenMW/openmw` | 6 609 | GPL-3.0 | 2026-10-07 | ⚠️ Copyleft fort : idem GPL-2.0 + incompatibilité avec certains composants. |
| `OpenDroneMap/ODM` | 6 509 | AGPL-3.0 | 2026-09-16 | ⚠️ Contamination réseau : si le code tourne dans un service exposé  tout le service doit être ouvert. Utilisable en outil interne séparé  PAS embarqué dans le cœur. |
| `osmandapp/OsmAnd` | 6 062 | GPL-3.0 | 2026-10-08 | ⚠️ Copyleft fort : idem GPL-2.0 + incompatibilité avec certains composants. |
| `CloudCompare/CloudCompare` | 4 788 | GPL-2.0 | 2026-10-08 | ⚠️ Copyleft fort : utilisable comme outil externe lancé par l'app (sidecar)  pas lié au cœur propriétaire/monétisé. |
| `osm-search/Nominatim` | 4 512 | GPL-3.0 | 2026-09-30 | ⚠️ Copyleft fort : idem GPL-2.0 + incompatibilité avec certains composants. |
| `WebODM/WebODM` | 4 205 | AGPL-3.0 | 2026-10-06 | ⚠️ Contamination réseau : si le code tourne dans un service exposé  tout le service doit être ouvert. Utilisable en outil interne séparé  PAS embarqué dans le cœur. |
| `LinuxCNC/linuxcnc` | 2 484 | GPL-2.0 | 2026-10-07 | ⚠️ Copyleft fort : utilisable comme outil externe lancé par l'app (sidecar)  pas lié au cœur propriétaire/monétisé. |
| `freeciv/freeciv` | 1 602 | GPL-2.0 | 2026-10-08 | ⚠️ Copyleft fort : utilisable comme outil externe lancé par l'app (sidecar)  pas lié au cœur propriétaire/monétisé. |
| `kiwix/kiwix-tools` | 961 | GPL-3.0 | 2026-10-01 | ⚠️ Copyleft fort : idem GPL-2.0 + incompatibilité avec certains composants. |
| `xeokit/xeokit-sdk` | 944 | AGPL-3.0 | 2026-10-05 | ⚠️ Contamination réseau : si le code tourne dans un service exposé  tout le service doit être ouvert. Utilisable en outil interne séparé  PAS embarqué dans le cœur. |
| `Kc1t/alethe-agents` | 832 | AGPL-3.0 | 2026-10-07 | ⚠️ Contamination réseau : si le code tourne dans un service exposé  tout le service doit être ouvert. Utilisable en outil interne séparé  PAS embarqué dans le cœur. |
| `openzim/zim-tools` | 221 | GPL-3.0 | 2026-10-04 | ⚠️ Copyleft fort : idem GPL-2.0 + incompatibilité avec certains composants. |
| `kobotoolbox/kpi` | 185 | AGPL-3.0 | 2026-10-08 | ⚠️ Contamination réseau : si le code tourne dans un service exposé  tout le service doit être ouvert. Utilisable en outil interne séparé  PAS embarqué dans le cœur. |

## Ce qu'ArenaAI doit ajouter à cette matrice

1. **Les données, pas seulement le code** : licences des jeux de données (IGN, OSM/ODbL, ROME, ESCO, O*NET, OpenAlex, INSEE),
   avec la clause d'attribution exacte à afficher dans l'application.
2. **Les modèles IA** : poids et licences (Apache-2.0, Gemma, Llama Community, CC-BY-NC), y compris les restrictions de redistribution.
3. **Les polices et les icônes** (Inter, JetBrains Mono, Material Symbols…).
4. **La voie de sortie** : pour chaque dépendance ⚠️, quel remplaçant permissif existe, et quel effort pour y passer.

