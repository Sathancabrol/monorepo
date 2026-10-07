# Écosystème libre et local — modèles IA, bases hors ligne, cartes et fiches

**Statut :** `ANALYSE` · **Date :** 7 octobre 2026 · Toutes les étoiles/licences GitHub vérifiées le 7 octobre 2026 via l'API GitHub.
**Contrainte de départ :** tout doit pouvoir tourner **gratuitement, en local, hors ligne** — machine cible **GTX 1060 6 Go** + RAM standard.

---

## 1. Modèles IA locaux utilisables en octobre 2026

### 1.1 Ce qui tient réellement dans 6 Go de VRAM

| Modèle | Taille sur disque | Mémoire nécessaire | Vitesse | Licence | Pour quoi il est le meilleur |
|---|---|---|---|---|---|
| **Qwen 3.5 9B** | 6,6 Go | ~6,0 Go | 19 tok/s | Apache-2.0 | Le meilleur compromis général : 256 000 tokens de contexte, 100+ langues, bon en résumé de longs documents |
| **Granite 4.2 8B** (IBM) | 5,3 Go | ~8,3 Go (déborde un peu → RAM) | 19 tok/s | **Apache-2.0** | ⭐ **Extraction d'information, sorties structurées, travail sur documents** — « n'invente rien » : le profil idéal pour lire un DQE, un CCTP, un rapport |
| **Gemma 4 12B** (Google) | 7,6 Go | 8,4 Go (→ RAM) | 13 tok/s | Apache-2.0 | La meilleure qualité globale, lit aussi les images (plans, photos de chantier) |
| **Gemma 4 E4B** | ~9,6 Go (collection) | 5 Go min (Q4) | rapide | Apache-2.0 | Conçu pour les machines légères, multimodal natif (texte, image, audio) |
| **LFM2.5 8B** (Liquid AI) | 5,2 Go | 5,5 Go | **82 tok/s** | à vérifier | Ultra rapide : brouillons, reformulation, classification |
| **Phi-4 Reasoning Plus** | ~8 Go | ~8 Go | moyen | **MIT** | Raisonnement et calcul : utile pour les métrés et les écarts de prix |
| **DeepSeek R1 8B** | 5,2 Go | 7,9 Go | 20 tok/s | MIT | Raisonnement visible (on voit son raisonnement) |
| **Mistral 7B** | 4,1 Go | 6-7 Go | rapide | **Apache-2.0** | Le plus léger ; dépannage |
| gpt-oss 20B | ~16 Go | 16 Go | lent | Apache-2.0 | Hors budget VRAM, mais possible en RAM si la machine a 32 Go |

> **Règle pratique :** sur 6 Go de VRAM, on charge **un seul modèle à la fois** de 7–9B en quantification Q4. Les trois à installer en priorité : **Qwen 3.5 9B** (généraliste), **Granite 4.2 8B** (extraction de documents — le cœur de notre usage), **Gemma 4 12B** (qualité/vision, quitte à déborder en RAM).

### 1.2 Les autres briques, toutes libres

| Besoin | Outil libre | Note |
|---|---|---|
| Faire tourner les modèles | **Ollama**, LM Studio (gratuit), llama.cpp | Ollama = le standard local, installable, hors ligne après téléchargement |
| Transcription audio (réunions de chantier, dictées) | **Whisper large-v3-turbo** / **faster-whisper** (CTranslate2, ~4× plus rapide) | Excellent en français, tourne en local |
| Synthèse vocale (lire un rapport à voix haute) | **Piper** | Voix françaises, tourne même sur Raspberry Pi |
| Lecture de documents (PDF → texte structuré) | **Marker**, **MinerU**, **Docling**, **markitdown** | Déjà retenus dans `docs/recherche/03` |
| OCR (plans scannés, photos) | **Tesseract**, **PaddleOCR**, **Surya** | À compléter par un modèle vision pour les plans |
| Base vectorielle locale (mémoire sémantique) | **Qdrant**, **Chroma**, **pgvector**, **LanceDB** | Qdrant est celui embarqué par NOMAD (voir §2) |
| Génération d'images (illustrations de fiches) | ComfyUI / Stable Diffusion | Licence du modèle à vérifier selon le checkpoint |

**Ce qu'il faut créer (il n'existe pas tout fait) :**
- un **routeur de modèles** local : « cette tâche → ce modèle » (un petit modèle pour classer, un gros pour rédiger) pour ne pas charger 12 Go quand 5 Go suffisent ;
- un **cache de résultats** : ne jamais refaire deux fois le même calcul coûteux (indexation, extraction, OCR) — c'est ce qui rend l'expérience fluide sur une machine modeste ;
- un **mode dégradé explicite** : quand aucun modèle n'est chargé, l'application doit rester utilisable (recherche plein texte, tableaux) et le dire (⚠ « IA non chargée »).

---

## 2. L'écosystème « prepper » : la connaissance hors ligne

C'est un vrai écosystème, mature, et il fait **exactement** ce que tu veux : de la donnée utile, hors ligne, gratuitement.

| Projet | Licence | ★ | Ce que c'est | Pour nous |
|---|---|---|---|---|
| **Kiwix** (`kiwix/kiwix-tools`) | GPL-3.0 | 961 | Moteur qui sert les fichiers **ZIM** (Wikipédia, WikiMed, iFixit, Stack Exchange, Wikivoyage, Gutenberg) — hors ligne, avec recherche plein texte | ⭐ **La brique de base** : une bibliothèque de référence locale, sans internet |
| **Project NOMAD** (`Crosstalk-Solutions/project-nomad`) | **Apache-2.0** | **39 218** | « Ordinateur de survie » complet : Kiwix + Kolibri (cours) + **ProtoMaps** (cartes hors ligne) + **Ollama** + **Qdrant** + CyberChef + FlatNotes ; installation en une commande ; min 2 cœurs / 4 Go RAM / 5 Go de disque | ⭐⭐ **Le modèle d'architecture à copier** : c'est la version « somme toute modeste » de ce que Carré d'As veut être, mais sans métier. À disséquer, pas à réinventer |
| **pimaps** (`BobbyLLM/pimaps`) | **AGPL-3.0** | 4 | Cartes hors ligne : **MapLibre + PMTiles** (rendu) + **SQLite/FTS5** (recherche) + **BRouter** (itinéraires) + couche Wikipédia via **Kiwix** | ⭐ **La pile de carte locale exacte** dont on a besoin. Le projet est petit (4 ★) mais l'assemblage est juste et documenté |
| **Kolibri** (`learningequality/kolibri`) | MIT | 1 134 | Plateforme d'apprentissage hors ligne (cours, progression) | Formation interne, tutoriels dans l'app |
| **Organic Maps** | (voir dépôt) | 15 611 | Application cartographique hors ligne Android/iOS | À recommander sur **téléphone** pour le terrain, en complément de la carte de l'app |
| **OsmAnd** | (voir dépôt) | 6 061 | Idem, plus orienté pro/capteurs | Terrain, hors ligne |
| **ODK / KoboToolbox** | libre, auto-hébergeable | — | **Collecte de données terrain hors ligne** : formulaires, GPS, photos, signatures, audio — puis synchronisation | ⭐⭐ **Directement applicable au chantier** : relevés, essais, non-conformités, métrés contradictoires, **sans réseau** |
| Fichiers **ZIM** (contenu) | selon source | — | Wikipédia (4,3 Go « best of » → 100 Go complet), WikiMed (1 Go), iFixit (4 Go), Stack Exchange (92 Go), Wikivoyage, Gutenberg | Choix du contenu = choix éditorial, pas technique |

**Ce qu'il faut créer (le vrai manque) :**
1. **Un « Kiwix du BTP »** : Kiwix existe, **le contenu métier n'existe pas**. Il n'y a **aucune** bibliothèque libre hors ligne de DTU, guides OPPBTP, sous-détails de prix, fiches matériaux. C'est là qu'est la valeur — et c'est parfaitement monétisable (voir §4).
2. **Un format de « fiche ID »** (voir §3) avec éditeur local.
3. **Un pont entre le corpus local et les référentiels** (ROME, IGN, DVF, Géorisques) — personne ne l'a fait.

---

## 3. Cartes et « fiches ID » : ce qui existe, ce qui manque

### 3.1 Cartes — la pile recommandée (100 % libre, 100 % local)

```
Données : OpenStreetMap (extraits régionaux) + IGN (cadastre, BD TOPO) + DVF (prix)
Format   : PMTiles (un seul fichier par région, servable en local)
Rendu    : MapLibre GL JS (2D, léger — 3 ms mesurés dans watchtower)
           Cesium seulement à la demande (21 357 ms mesurés → pas par défaut)
Recherche : SQLite + FTS5 (locale, instantanée)
Itinéraires : BRouter (hors ligne)
Wiki/culture : Kiwix + ZIM (Wikipédia, Wikivoyage)
Risques  : Géorisques, aléas inondation — à importer une fois puis hors ligne
```

Cette pile est **validée par deux projets indépendants** (pimaps et NOMAD) : on ne l'invente pas, on la reprend.

### 3.2 Fiches ID — état des lieux honnête

| Piste | Ce qui existe | Verdict |
|---|---|---|
| Champignons / plantes (identification terrain) | **Shroomify** (guide hors ligne, 400+ espèces, Android/iOS), Pl@ntNet (freemium), **HortusFox** (gestion de plantes auto-hébergée, libre) | Rien de **libre + auto-hébergé + base ouverte** : les meilleurs sont des applis mobiles fermées |
| Espèces, objets, lieux, personnes | **Wikipédia / Wikidata via ZIM (Kiwix)**, avec images et liens | ⭐ La meilleure base existante, déjà hors ligne et déjà libre |
| Matériaux, réseaux, engins, normes (BTP) | Éparpillé (PDF de fournisseurs, guides, catalogues) | **À construire** : c'est notre « fiche ID » métier |
| Matériel de secours / autonomie | Contenu ZIM (WikiMed, iFixit, Wikivoyage) + listes communautaires | Réutilisable tel quel par import |

> **Décision proposée :** créer un **module « Fiches »** dans Carré d'As, générique :
> `fiche = { id, type, titre, propriétés[], photos[], sources[], liens[], statut ✅📅🔮⚠️ }`
> avec trois sources possibles : (a) **saisie/photo terrain**, (b) **import ZIM/Wikipédia** (texte + image + licence), (c) **import métier** (catalogue, norme, prix).
> Un seul format pour les espèces, les matériaux, les réseaux, les engins, les contacts — et le même atelier d'édition. C'est ce qui manque à tout le monde, et c'est faisable.

---

## 4. Conséquence juridique à ne pas oublier (lien avec la monétisation)

| Licence de l'outil repris | Ce qu'on peut faire | Précaution |
|---|---|---|
| **Apache-2.0** (NOMAD, Qwen, Granite, Gemma, map/PMTiles) | Intégrer dans un produit, même vendu, même fermé | Citer la licence et les auteurs |
| **MIT** (Kolibri, Phi-4, Marker) | Idem, très souple | Citer |
| **GPL-3.0** (Kiwix) | Utiliser **comme programme séparé** appelé par l'application (processus distinct, ligne de commande) → pas de contamination | **Ne jamais coller du code GPL dans un module fermé** ; garder l'appel « à distance » (HTTP/ligne de commande) |
| **AGPL-3.0** (pimaps) | Réutiliser en respectant l'obligation de publier les modifications si on offre le service en réseau | Si on **copie du code** de pimaps dans Carré d'As, le module concerné doit être AGPL/GPL-compatible → à décider en connaissance de cause ; sinon, réimplémenter l'idée |
| **NOASSERTION** (Organic Maps, OsmAnd, GDAL…) | Vérifier fichier par fichier | Le plus souvent ce sont des licences libres avec clauses de marque |

**Règle simple à retenir :** *les outils, on les appelle ; on ne les aspire pas.* Ainsi le cœur peut rester Apache-2.0, la monétisation reste possible, et on profite de tout l'écosystème libre.

---

## 5. Ce qu'on doit créer nous-mêmes (la liste courte)

| # | Brique manquante | Pourquoi personne ne l'a faite | Effort |
|---|---|---|---|
| 1 | **Module « Fiches »** génériques (espèces, matériaux, réseaux, engins) | Chacun est resté sur son métier | Moyen |
| 2 | **Bibliothèque métier hors ligne** (DTU, guides, prix) servie localement | Contenu sous droits → à agréger proprement | Moyen |
| 3 | **Pont corpus ↔ référentiels** (ROME, IGN, DVF, Géorisques) | Personne n'a ce besoin en même temps que toi | Moyen |
| 4 | **Rangement automatique** des documents (famille, doublons, dates) | Les briques existent (Docling/Marker), l'assemblage non | Faible |
| 5 | **Synchronisation simple sans cloud** (dossier local + Google `drive.appdata`) | Les solutions libres visent le serveur, pas le poste de travail | Moyen |
| 6 | **Mode terrain hors ligne** (relevés + photos + GPS, comme ODK mais intégré au chantier) | ODK fait la collecte, pas le chantier | Moyen |

Chacune de ces six briques est **faisable avec l'existant** : aucune ne demande de recherche fondamentale. C'est la matière de la V1 et de la V1.5.

---

## 6. Sources vérifiées

- GitHub API (7 oct. 2026) : `kiwix/kiwix-tools` GPL-3.0 ★961 · `openzim/zim-tools` GPL-3.0 ★221 · `learningequality/kolibri` MIT ★1 134 · `Crosstalk-Solutions/project-nomad` Apache-2.0 ★39 218 · `BobbyLLM/pimaps` AGPL-3.0 ★4 · `organicmaps/organicmaps` ★15 611 · `osmandapp/OsmAnd` ★6 061.
- Project NOMAD : présentation (readthemanual.co.uk, topaiproduct.com 21/03/2026) — Kiwix + Kolibri + ProtoMaps + Ollama + Qdrant, min 2 cœurs/4 Go/5 Go, installation en une commande, Apache-2.0.
- Kiwix/ZIM : tailles des collections (localaimaster.com 23/04/2026) — Wikipédia 100 Go complet / 4,3 Go « best of » / 50 Go sans images, WikiMed 1 Go, iFixit 4 Go, Stack Exchange 92 Go, Gutenberg 16 Go.
- Modèles locaux : briefia.fr (30/09/2026), double-slash.dev (10/05/2026), quelllm.fr (29/09/2026), digitiz.fr (26/09/2026, mesures 13–82 tok/s).
- Collecte terrain : synergaid.com.au (26/08/2026), casrai.org (23/07/2026), dt4si.com — ODK/Kobo hors ligne, auto-hébergeables.
- Identification terrain : foragers-friend.com (Shroomify), androidpolice.com (27/06/2026), alternativeto.net (HortusFox).
- Association et fiscalité : service-public.gouv.fr `F31838`, legalstart.fr (2026 : franchise ≈ 81 051 €), assoconnect.com.
