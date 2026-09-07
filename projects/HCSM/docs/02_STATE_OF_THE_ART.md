# 02 — État de l'art

**Statut du document :** cartographie critique, pas revue systématique exhaustive  
**Couche :** SCIENTIFIC KNOWLEDGE  
**Version :** 0.1.0 · 2026-08-25

Ce document situe HCSM dans les cadres existants. Il ne prétend pas à l'exhaustivité PRISMA. Une revue systématique dédiée reste un livrable du protocole (`docs/13_RESEARCH_PROTOCOL.md`). Les affirmations de consensus sont `ESTABLISHED` ou `SUPPORTED` ; les lectures HCSM sont `PROPOSED`.

Bibliographie développée : `papers/references/bibliography.md`.  
Corpus psychologie 2020–2026 : dépôt [ETAT-DE-LART-PSYCHOLOGIE](https://github.com/Sathancabrol/ETAT-DE-LART-PSYCHOLOGIE).

---

## 1. Question de cette cartographie

> Quels cadres existent déjà pour (a) représenter les construits cognitifs, (b) les mesurer à plusieurs niveaux, (c) les contextualiser, (d) les suivre dans le temps, et (e) en inférer un état individuel ?

Cinq familles répondent chacune à une partie de la question. Aucune ne répond à l'ensemble comme objet computationnel unique. C'est le point de départ de HCSM, pas une originalité automatique.

## 2. Ontologies et cadres de connaissance

### 2.1. Cognitive Atlas — `ESTABLISHED`

Poldrack et al. (2011) posent une distinction fondatrice, héritée de Cronbach & Meehl (1955) : **concepts mentaux** (construits latents) vs **tâches mentales** (opérations de mesure). Les relations (`is-a`, `part-of`, `measured-by`) formalisent une théorie psychologique comme un graphe.

Ce que l'Atlas fait :

- vocabulaire contrôlé des processus (attention, working memory, cognitive control, …) ;
- liaison construit ↔ tâche / contraste ;
- base pour l'annotation de jeux de données d'imagerie et la méta-analyse (Poldrack & Yarkoni, 2016 ; encoding models, 2022).

Ce que l'Atlas ne fait pas, et que HCSM ne doit pas lui voler :

- représenter l'état d'une *personne* ;
- porter de l'incertitude d'estimation individuelle ;
- gérer un contexte situationnel ou une trajectoire.

Lecture HCSM (`PROPOSED`) : le Cognitive Atlas est le candidat naturel du **knowledge graph** pour les construits et les tâches. HCSM s'aligne, il ne le réécrit pas.

CogPO (Turner & Laird, 2012) complète l'Atlas côté description opérationnelle des paradigmes (stimuli, réponses, consignes). Lien à prévoir dans l'ontologie.

### 2.2. RDoC — `ESTABLISHED`

Le Research Domain Criteria (NIMH ; Insel et al., 2010 ; Cuthbert & Insel, 2013) organise la recherche en psychopathologie selon une matrice :

- **lignes** : construits fonctionnels groupés en domaines (Negative Valence, Positive Valence, Cognitive Systems, Social Processes, Arousal/Regulatory, Sensorimotor) ;
- **colonnes** : unités d'analyse (gènes, molécules, cellules, circuits, physiologie, comportement, auto-évaluations, paradigmes) ;
- **dimensions additionnelles** : développement et environnement (Casey, Oliveri & Insel, 2014).

RDoC refuse le diagnostic DSM comme variable indépendante. Un construit (working memory, loss, threat) se mesure à plusieurs niveaux, dimensionnellement.

Ce que RDoC fait déjà et que HCSM ne doit plus présenter comme nouveau :

- intégration multi-niveaux d'un même construit ;
- prise en compte du développement et de l'environnement ;
- abandon d'une pile « biologique → psychologique → neurologique ».

Ce que RDoC n'est pas :

- un moteur d'inférence individuelle à T0 ;
- un modèle d'évidence avec provenance ;
- une spécification computationnelle d'état latent personnel.

Lecture HCSM (`PROPOSED`) : les unités d'analyse RDoC deviennent des **voies d'évidence**, pas des étages ontologiques.

### 2.3. ICF — `ESTABLISHED`

L'International Classification of Functioning, Disability and Health (WHO, 2001) pose que le fonctionnement n'est pas la conséquence linéaire d'une pathologie. Il résulte de l'interaction entre :

- fonctions et structures corporelles (y compris fonctions mentales) ;
- activités et participation ;
- facteurs environnementaux et personnels.

Deux notions critiques pour HCSM : **capacité** (ce qu'une personne peut faire dans un environnement standard) vs **performance** (ce qu'elle fait dans son environnement habituel). On n'infère pas la participation à partir d'une atteinte, ni l'atteinte à partir d'un diagnostic (Reed et al., 2005, application aux troubles cognitifs).

Lecture HCSM (`PROPOSED`) : l'ICF fournit le **fonctionnement contextualisé** en sortie du modèle, pas le construit cognitif en entrée.

### 2.4. HPO — `ESTABLISHED`

La Human Phenotype Ontology (Köhler et al., 2024) organise les phénotypes observables de la maladie humaine, avec inférence sémantique et similarité. La couverture comportementale s'étend (mood, neurodéveloppement ; ateliers NIMH 2023). HPO relie des observables atomiques selon leur sens, non selon leur co-occurrence à la DSM.

Lecture HCSM (`PROPOSED`) : HPO est une cible d'alignement pour les *phénotypes observés*, distincts des construits latents. Un retard de langage HPO n'est pas une estimation HCSM de « langage ».

### 2.5. Autres ressources à aligner

| Ressource | Rôle | Statut pour HCSM |
|---|---|---|
| Gene Ontology | Ontologie biologique de référence, modèle historique | alignement distant |
| NeuroLex / NIFSTD | Vocabulaires neurosciences | alignement knowledge graph |
| SNOMED CT, ICD | Terminologies cliniques | pont, pas cœur |
| Cognitive Atlas + CogPO | Concepts et paradigmes | alignement prioritaire |
| ICF Core Sets (TDAH, TSA, AVC, TCC, …) | Sous-ensembles fonctionnels | alignement functioning |

## 3. Mesure, construits latents, réseaux

### 3.1. Psychométrie des construits — `ESTABLISHED`

Cronbach & Meehl (1955) : un construit n'est pas l'opération qui le mesure. La validité de construit se joue dans un réseau nomologique. Messick, Kane, puis les modèles de validité argumentée ont durci cette exigence.

Conséquence directe pour HCSM : une tâche n-back n'est pas la mémoire de travail (Huang et al., 2025, validité de construit faible du n-back, cité dans le corpus ETAT-DE-LART). Un score CPT n'est pas l'attention.

Lee & Engle (2026) : le contrôle attentionnel explique une part majeure de la variance multitâche et réduit le lien WMC–gF une fois contrôlé. Cela illustre précisément le besoin de ne pas réifier un instrument.

### 3.2. Modèles à variables latentes — `ESTABLISHED`

Théorie de réponse à l'item, modèles factoriels, modèles SEM, modèles à classes latentes, modèles à état-espace : tous estiment un état non observé à partir d'indicateurs bruités, avec erreur de mesure.

HCSM n'invente pas l'état latent. Il impose que l'état latent soit **typé ontologiquement**, **contextualisé**, **temporellement borné** et **accompagné de provenance**.

### 3.3. Network psychometrics — `SUPPORTED`

Borsboom et collègues modélisent les symptômes comme un réseau d'interactions plutôt que comme effets d'un facteur commun. Utile pour HCSM : le graphe d'inférence peut représenter des influences (sommeil → fatigue → attention) sans postuler un facteur g cognitif unique.

Ce n'est pas une ontologie. C'est une famille de modèles d'inférence, à tenir à côté des modèles factoriels, pas à leur place.

### 3.4. Psychiatrie computationnelle — `SUPPORTED`

Montague, Dolan, Friston & Dayan (2012) : inférer des processus latents (apprentissage par renforcement, précision, gain) à partir du comportement, pour phénotyper computationnellement. Huys, Maia & Frank (2016) distinguent approches *data-driven* et *theory-driven*.

Lecture HCSM : un paramètre de modèle computationnel (taux d'apprentissage, bruit de décision) est une **mesure dérivée**, pas un construit ontologique. Il entre dans l'evidence graph avec le modèle qui l'a produit.

## 4. Temps, contexte, données in situ

### 4.1. EMA / ESM — `ESTABLISHED`

Shiffman, Stone & Hufford (2008) : échantillonnage répété des expériences dans l'environnement naturel, pour réduire le biais de rappel et étudier les micro-processus. Faisabilité établie y compris en psychose (revues 2023–2025).

### 4.2. Digital phenotyping — `SUPPORTED`

Onnela & Rauch (2016), Torous et al. : quantification moment-à-moment du comportement à partir des appareils personnels (GPS, actigraphie, logs de communication, capteurs). Complète l'EMA active par du passif.

Limites désormais bien documentées (`SUPPORTED`) : validité de construit fragile, dérive des capteurs, biais de couverture socio-économique, opacité des pipelines, risque de réidentification, faible reproductibilité des features.

HCSM n'ajoute pas un capteur. Il impose que chaque feature digitale soit une **évidence**, avec provenance et explications alternatives (sédentarité ≠ anhédonie ; écran allumé ≠ vigilance).

### 4.3. Fusion multimodale — `SUPPORTED`

La fusion de questionnaires, tâches, physiologie et traces numériques est un champ actif (santé mentale, cognition, vieillissement). Les performances prédictives existent ; l'interprétabilité et la validité de construit restent le point faible.

Un modèle qui prédit un PHQ-9 à partir du GPS n'estime pas un état cognitif HCSM. Il prédit un score. HCSM refuse cette substitution.

## 5. Connaissance, FAIR, provenance

Wilkinson et al. (2016) : principes FAIR.  
PROV-O (W3C) : entités, activités, agents, dérivation.

Sans provenance, une estimation HCSM n'est pas distinguable d'un score marketing. La provenance n'est pas un métadonnée décorative : elle est constitutive de l'objet `ConstructEstimate` (`PROPOSED`, sur une base `ESTABLISHED` en science ouverte).

## 6. Cognition 4E et validité écologique

Le corpus Cognitorium / ETAT-DE-LART documente embodiment, embeddedness, enaction, extension, affordance, charge cognitive, agence. Solidité empirique inégale (charge cognitive et affordance plus établies que l'énactivisme radical).

Pour HCSM, le point opératoire n'est pas philosophique : **un état sans contexte n'est pas un état de personne**. C'est déjà dans l'ICF. Les 4E renforcent l'argument, ils ne le fondent pas seuls.

Limite (`OPEN QUESTION`) : comment encoder une affordance ou un couplage agent–environnement sans psychologiser l'interface.

## 7. Ce que personne ne fournit encore comme objet unique

Synthèse prudente (`SUPPORTED` comme constat de couverture, `PROPOSED` comme lecture) :

| Besoin | Qui s'en approche | Qui ne le clôt pas |
|---|---|---|
| Vocabulaire des construits et tâches | Cognitive Atlas, CogPO | pas d'état personnel |
| Multi-niveaux d'analyse | RDoC | pas d'inférence individuelle T0 |
| Fonctionnement contextualisé | ICF | pas d'état latent cognitif |
| Phénotype observable formalisé | HPO | pas de construit latent ni de dynamique |
| État latent avec erreur | psychométrie, computational psychiatry | rarement ontologie + contexte + provenance |
| Observations in situ | EMA, digital phenotyping | rarement lié à une ontologie de construits |
| Trajectoire | modèles longitudinaux, state-space | rarement multi-graphes Knowledge/Evidence/Inference |

Le trou n'est pas « il manque une carte de la cognition ».  
Le trou est : **il manque une couche d'inférence personnelle, temporelle, evidentiale, qui relie des cadres déjà là sans les fusionner abusivement.**

C'est l'objet de `docs/03_RESEARCH_GAP.md`.
