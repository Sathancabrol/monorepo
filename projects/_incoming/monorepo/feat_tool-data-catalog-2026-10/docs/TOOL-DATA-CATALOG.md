# Catalogue unifié des données et outils

> Index transversal du monorepo. Le catalogue décrit **ce qui existe**, **où se trouve la brique de référence**, **ce qu'elle apporte** et **où elle peut être réutilisée**. Il ne remplace pas les projets sources.

## Sources internes

| Domaine | Référence | Ce que l'on récupère |
|---|---|---|
| Cartographie / 3D / temps réel | `projects/COGNITORIUM/watchtower-mods` + dépôt `watchtower` | couches, globe Cesium, bâtiments 3D, cadastre, météo, trafic, avions, navires, CCTV, chantier, HUD, géolocalisation |
| Registre d'outils | Watchtower `audit/reference/REGISTRE-OUTILS.json` | outils locaux/cloud, licences, coûts, alternatives, intégration |
| Chantier TP/BTP | racine du monorepo + `projects/proto-cognitorium/raw` | DCE, CCTP, CCAP, BPU, DQE, plans, métrés, planning, PAQ, sécurité, DICT/DT, essais, rapports, fiches de tâches |
| Recherche / preuves | `projects/reaserch-engine` | retrieval, sources, evidence graph, claims, contradictions, dossiers, qualité, suffisance |
| Modèle cognitif | `projects/HCSM` | ontologie, provenance, incertitude, contexte, temporalité, observations, estimations |
| Cognitorium | `projects/COGNITORIUM` + `projects/proto-cognitorium` | graphes, compétences, ROME, psychologie, outils, learning engine, agents |
| Territoire | `projects/frontignan` | population, mobilité, acteurs, projets, scénarios 2026-2040 |
| Animation / découverte | `projects/animation-chronos` | séquences, progression, observation, visualisation temporelle |
| Langage | `projects/Language-decoder` | brique de décodage / langage à évaluer |

## Capacités cibles

### 1. Carte territoire
- fonds OSM / IGN / satellite / relief
- bâtiments et 3D
- cadastre
- hydrographie / environnement / risques
- transports / routes / équipements
- météo et données temporelles
- avions / navires / satellites
- couches chantier
- annotations et import GeoJSON
- fiche lieu / contexte / historique

### 2. Chantier intelligent
- DCE → CCTP / CCAP / BPU / DQE
- extraction des tâches, quantités, contraintes et acteurs
- planning / phasage
- ressources / matériel
- sécurité / signalisation
- DICT / réseaux
- qualité / essais / non-conformités
- journal chantier
- imprévus / risques / événements
- géolocalisation des engins
- rapprochement carte ↔ document ↔ tâche

### 3. Recherche et OSINT
- recherche multi-source
- crawl / extraction
- OCR / documents
- sources et provenance
- evidence graph
- claims / contradictions
- hypothèses séparées des faits
- chronologie
- graphe d'entités
- validation humaine

### 4. Cognition / connaissance
- HCSM comme modèle de provenance et d'incertitude
- graphes de connaissances
- compétences / tâches / métiers
- ROME et référentiels externes
- profils / trajectoires
- learning engine
- simulation / transfert

### 5. Agents
- orchestrateur
- agent GIS
- agent Data
- agent Research
- agent Project
- agent 3D/CAD
- agent Learning
- agent Verification
- agent Manufacturing
- agent IA
- agents spécialisés chantier

## Règle d'intégration

Une fonctionnalité ne doit être copiée dans plusieurs projets que si elle devient un composant réellement partagé.

Priorité :

1. **référencer** la source existante ;
2. **adapter** via une interface commune ;
3. **normaliser** les données ;
4. seulement ensuite **extraire** en module partagé.

### Schéma

```
SOURCE / REPO
      ↓
ADAPTER
      ↓
CANONICAL DATA
      ↓
CAPABILITY
      ↓
UI / AGENT / MAP / GRAPH
```

## Modèle canonique minimal

Toute donnée intégrable devrait pouvoir porter :

- `id`
- `type`
- `label`
- `source`
- `source_url`
- `retrieved_at`
- `observed_at`
- `geometry` si spatiale
- `valid_from / valid_to` si temporelle
- `provenance`
- `confidence`
- `license`
- `status`
- `relations[]`

Cela permet de relier une information de chantier, une entité géographique et une preuve documentaire sans perdre son origine.

## Important

Le registre Watchtower reste la source détaillée des logiciels externes. Le monorepo conserve ici l'**index de convergence** et les données internes. Les informations sensibles du corpus chantier ne doivent pas être poussées vers un service externe sans décision explicite.
