# Réponses à tes 7 points — licence, ordre réel des travaux, corpus, écosystème libre

**Statut :** `ANALYSE` — rien n'est implémenté, rien n'est figé. Ces réponses remplacent/complètent `00-CADRAGE-CARRE-D-AS.md`.
**Date :** 7 octobre 2026.

---

## 1. Licence : garder la porte de la monétisation ouverte

### 1.1 D'abord un point qu'il faut comprendre (rassurant)

> **Quelle que soit la licence choisie, tu peux toujours vendre ton logiciel.** La licence ne limite pas *ton* droit de vendre : elle limite les droits des autres. Un logiciel sous GNU GPL peut être vendu (Red Hat, Nextcloud, Blender le font). La licence n'est **pas** le verrou de la monétisation.
> Ce qui peut te fermer des portes, ce sont **trois autres choses** :
> 1. **accepter des contributions extérieures sans contrat** (CLA) → tu perds le droit de changer de licence plus tard ;
> 2. **un cœur en licence permissive** (MIT/Apache) → un concurrent peut vendre ton travail, y compris en cloud, sans rien te devoir ;
> 3. **aucune marque déposée** → n'importe qui peut nommer son logiciel « Carré d'As » ou « Cognitorium ».

### 1.2 Contrainte particulière d'une association (loi 1901)

| Point | Ce que dit le droit | Conséquence pour toi |
|---|---|---|
| Activité commerciale | Une association peut exercer une activité économique : elle reste non lucrative si la gestion est **désintéressée** (les bénéfices ne sont pas partagés) | Tu peux **facturer** (licences, formation, hébergement) |
| Franchise d'impôts commerciaux | Si les recettes lucratives accessoires restent **« marginales »** : franchise jusqu'à **≈ 81 051 € / an (2026)** ; au-delà, imposition dès le 1er euro. Règle des 4 critères (produit, public, prix, publicité) pour rester exonéré | Une activité de services modeste n'entraîne pas de bascule fiscale ; une activité « main part of resources » devient imposable |
| Interdiction de fond | Ne jamais distribuer les bénéfices aux membres | Les recettes servent l'objet associatif (c'est ce que tu veux) |
| Risque de requalification | Si l'activité lucrative devient **l'objet principal** et concurrence le privé, requalification possible | Si un jour la part commerciale devient dominante → créer une **structure distincte** (SAS / SCIC / coopérative) et rester avec l'association pour le militantisme et les subventions |

Sources : service-public.gouv.fr `F31838`, legalstart.fr (mise à jour 2026), assoconnect.com.

> **En clair :** association = tu peux vendre, facturer, héberger, former. Ce qu'on doit protéger maintenant, c'est **le choix de le faire plus tard**, sans avoir à tout réécrire ni à demander la permission à des contributeurs.

### 1.3 Les 3 combinaisons possibles (avec la monétisation comme critère n°1)

| | **A. Tout Apache-2.0 + « open core »** | **B. Cœur AGPL-3.0 + double licence commerciale** | **C. Cœur Apache-2.0 + modules pro propriétaires** |
|---|---|---|---|
| Le cœur | Apache-2.0 (permissive) | AGPL-3.0 (copyleft fort) | Apache-2.0 |
| Moyens de gagner de l'argent | Services (intégration, formation, données), hébergement, modules payants, marketplace | **Double licence** : vendre une exception commerciale à qui ne veut pas de l'AGPL ; plus hébergement et services | Modules avancés fermés (3D, multi-sites, conformité) + services |
| Risque « un concurrent vend mon travail » | **Élevé** (il peut, sans payer) | **Faible** (l'AGPL lui interdit le SaaS fermé) | Moyen (le cœur oui, les modules non) |
| Compatible association / non lucratif ? | Oui, très | Oui, mais certains se méfient de l'AGPL | Oui |
| Effort juridique | Faible | **Plus élevé** : il faut un CLA signé par chaque contributeur, sinon tu ne peux pas faire de double licence | Moyen |
| Amitié avec les collectivités et les associations | Excellente | Correcte | Correcte si le cœur reste libre |
| Précédents | Code de la plupart des logiciels d'infrastructure | Grafana, MongoDB, Nextcloud (modèle AGPL + édition commerciale) | GitLab, Open Core classique |

### 1.4 Ma recommandation, ré-écrite sous l'angle monétisation

> **Cœur Apache-2.0 + CLA obligatoire (ou DCO + Copyright Assignment) + marque déposée + « open core » assumé.**

Pourquoi c'est le meilleur compromis pour **ton** objectif :
1. **Tu peux tout monétiser dès demain** : prestations, formation, hébergement, cartes/fiches de données, packs métier — c'est le plus gros du revenu d'un logiciel métier, pas la licence.
2. **Si un jour tu veux vendre des licences**, le CLA te redonne la main : tu es propriétaire de tout le code, donc tu peux **re-licencier une variante propriétaire** sans rien réécrire (exactement ce que fait Blender/MongoDB).
3. **L'Apache-2.0 rassure** les associations, les collectivités et les entreprises qui voudraient contribuer ou intégrer : sauf l'AGPL, qui bloque beaucoup de DSI.
4. **Ce qui protège vraiment, c'est ce que tu ajoutes** : les modules BTP, les référentiels enrichis, l'expérience d'interface. Le cœur seul n'est pas ce qui se vend.

**Deux clauses à ne pas oublier dès le premier contributeur extérieur :**
- **CLA** (ou au minimum DCO) avant de fusionner la moindre pull request ;
- **marque** : déposer « Carré d'As » (et vérifier « Cognitorium » — il est déjà utilisé par d'autres projets, dont un logiciel brésilien de cartographie cognitive).

**Trois offres possibles à terme (à ne pas construire maintenant) :**
1. **Gratuit** : l'application complète, locale, hors ligne, pour tout le monde.
2. **Soutien** : cotisation/adhesion qui finance le développement et donne accès aux référentiels enrichis mis à jour.
3. **Pro** : prestation d'installation/paramétrage, hébergement multi-sites, formation, module 3D avancé, conformité.

---

## 2. La séquence P0 → P6, expliquée sans jargon

Ton retour : **« pas compris »**. La faute est à moi : j'ai utilisé une nomenclature de chef de projet. Voici la même chose en langage courant :

> **L'image à garder : construire une maison.**
> On ne pose pas les fenêtres avant les murs, et on ne fait pas les peintures avant d'avoir un toit. Les 7 étapes sont les 7 étages du chantier. Chacune **se voit** : à la fin de chaque étape, il y a quelque chose de nouveau sur l'écran.

| Étape | Ce que je fais | **Ce que tu vois, toi** | Durée indicative | Pourquoi c'est dans cet ordre |
|---|---|---|---|---|
| **P0 — Rassembler** | Je réunis les branches, je ne jette rien, je note ce qui existe déjà | Rien à l'écran : un dossier propre et une liste « voilà tout ce qu'on a » | 2–3 jours | On ne construit pas sur du sable ; tu as 8 projets et 8 branches |
| **P1 — Le socle** | J'installe la base : la coquille de l'application + les données (documents, projets, chantiers) + la recherche | **Une seule application qui s'ouvre et retrouve un document** en tapant 3 lettres | 1–2 semaines | Sans ça, chaque module réinvente tout |
| **P2 — Le tour de l'interface** | Je pose les 4 portes, le rail, la barre du haut, le Ctrl+K, l' état (✅📅🔮⚠️), les 4 écrans de la V1 | **Tu navigues** : Projets, Carte, Documents, Agents, Système | 2–3 semaines | C'est ce que tu montres à quelqu'un ; sans interface, rien n'existe |
| **P3 — Le premier métier (BTP)** | J'installe le module BTP : lire un DQE, comparer des prix, suivre un chantier, ranger 154 documents | **Tu vois un vrai chantier dans l'application**, avec ses prix et ses écarts | 3–5 semaines | C'est le métier qui a le plus de matière dans ton dépôt : c'est ce qui prouve le concept |
| **P4 — L'installable** | Je fabrique l'installeur Windows : double-clic, ça marche, sans Node ni Python ni Docker ; sauvegarde, mise à jour, retour arrière | **Un fichier `.exe`** que tu donnes à quelqu'un : il clique, ça marche | 2–4 semaines | Un logiciel qu'on n'installe pas n'est pas un logiciel ; c'est aussi ça qui rend l'association crédible |
| **P5 — La carte et la 3D** | J'ajoute la carte du territoire et la 3D « voir et mesurer » ; je branche le compte Google pour synchroniser | **Le chantier sur la carte**, la maquette 3D, et les données qui suivent d'un ordinateur à l'autre | 3–6 semaines | Ces briques coûtent cher (GPU) et ne servent que si le reste tient |
| **P6 — Le navigateur** | Je transforme l'application pour qu'elle tourne aussi dans un navigateur, sans installation | **La même application dans Chrome**, accessible à distance | 4–8 semaines | Windows d'abord : c'est ta demande et c'est là qu'est ta machine |

**Trois phrases pour retenir :**
- **P0 → P2 : on construit le contenant.** Rien d'intelligent, mais tout doit être solide.
- **P3 : on met le métier dedans.** C'est là que le projet devient crédible.
- **P4 → P6 : on le rend livrable.** Installation, carte/3D, puis navigateur.

**Ce qui change par rapport à la version précédente :** l'ordre n'est plus « le mien », c'est **le tien** — voir la section 3. (Dans ton historique, tu as fait : voir → comprendre → modéliser → outiller → unifier. La séquence P0→P6 reprend cette logique : d'abord le socle qui permet de voir, ensuite le métier, ensuite le livrable.)

---

## 3. L'ordre chronologique **réel** de tes travaux (retrouvé, pas inventé)

Établi à partir de **deux sources datées** : (a) les dépôts de ton compte GitHub (`Sathancabrol`, dates de création) et (b) les prompts/documents de ton Drive (dates de dernière modification), plus le dépôt `monorepo` lui-même.

### 3.1 La frise

| Date | Ce que tu as fait | Source |
|---|---|---|
| **28 juil. 2026** | Prompt « **Cognitarium City : Frontignan 2026** » — l'idée « ville/territoire » | Drive |
| **31 juil. 2026** | Prompt « **Interface Cognitorium : Graphe Cognitif** » — première intention d'interface | Drive |
| **1er août 2026** | Prompt « **Cognitarium : Personal Cognitive Profile Design** » — le profil cognitif | Drive |
| **2 août 2026** | Dépôt **COGNITORIUM** créé — « outils de visualisation cognitif » | GitHub |
| **7 août 2026** | Prompt « **Conception du parcours d'onboarding** » | Drive |
| **16 août 2026** | « **Frise chronologique de l'Histoire** » + série d'images | Drive |
| **24 août 2026** | **Le grand jour** : `proto-cognitorium` + `ETAT-DE-LART-PSYCHOLOGIE` créés **et** rédaction du **Cahier des charges de référence v1.0** (le document directeur) | GitHub + dépôt |
| **25 août 2026** | Dépôt **HCSM — Human Cognitive State Model** + planche des **12 vues** cognitives | GitHub + dépôt |
| **26 août 2026** | Dépôt **reaserch-engine** (moteur de recherche) | GitHub |
| **27 août 2026** | Prompt « **Évolution de l'ingénierie IA** » — dernière recherche IA avant le code | Drive |
| **30 août 2026** | Dépôt **Language-decoder** — décodeur de langage multimodal | GitHub |
| **1er sept. 2026** | Dépôt **watchtower** — le poste de travail : barre de 24 fonctions, carte, bascule 2D/3D | GitHub |
| **2 sept. 2026** | Dépôt **animation-chronos** | GitHub |
| **7–9 sept. 2026** | Dépôt **monorepo** : unification des 8 projets ; puis 8 lots d'uploads | GitHub |
| **7 oct. 2026** | **Carré d'As** : recadrage produit, contrat de module, UI, module BTP (ce dossier) | dépôt |

### 3.2 Ce que cette frise dit de toi (et pas de moi)

**Ton ordre naturel est :**
1. **Voir** (juillet–août : images, interfaces, graphe, arbre, carte, ville) ;
2. **Comprendre / documenter** (24 août : cahier des charges + état de l'art) ;
3. **Modéliser** (25 août : HCSM, modèle d'état cognitif) ;
4. **Chercher** (26–27 août : reaserch-engine, veille IA) ;
5. **Outiller** (1er sept. : watchtower — carte, barres, 2D/3D) ;
6. **Unifier** (7 sept. : monorepo).

**Conséquence directe pour la V1 :** l'ordre ci-dessus est aussi le bon ordre de construction, et il **remplace** ma séquence précédente en la précisant :

| Ton étape naturelle | Devient dans la V1 |
|---|---|
| **Voir** | P0–P2 : socle + coquille + **une vue qui montre les données tout de suite** (liste, tableau, carte 2D — pas la 3D) |
| **Comprendre** | Le cahier des charges v1.0 devient **la spécification de référence** (il est déjà écrit : on l'applique au lieu d'en écrire un autre) |
| **Modéliser** | Le « Core » : entités et relations (Experience → Tâche → Compétence → Cognition → Matching, exactement comme ta planche `html ghierarchi.png`) |
| **Chercher** | Le moteur : indexation, recherche plein texte + sémantique, extraction de documents (Marker/MinerU, déjà local) |
| **Outiller** | P3 : le module BTP (DQE, prix, chantier) |
| **Unifier** | P4–P6 : livrable, carte/3D, navigateur |

### 3.3 Donc : quel chantier pilote la V1 ?

**Réponse, tirée de ta propre chronologie :** le premier chantier est **celui qui te fait VOIR tes données** — c'est-à-dire **le socle + la vue « Documents/Projets » sur ton corpus BTP réel (les 154 pièces)**. Tu as commencé par voir, tu as continué en documentant, puis en modélisant. Redémarrer par du code d'IA ou de la 3D serait une rupture avec ton ordre naturel ; redémarrer par « je vois mes 154 documents dans une seule application, et je retrouve n'importe lequel en tapant 3 lettres » est exactement la suite de ta ligne.

**Le module BTP (P3) reste ton choix** et c'est cohérent : c'est là qu'est la matière (documents, prix, chantiers, carte).

---

## 4. Le corpus de 100 documents : pourquoi je proposais de le sortir, et pourquoi je retire cette proposition

### 4.1 Les chiffres réels (mesurés aujourd'hui)

| Mesure | Valeur |
|---|---|
| Poids du dossier de travail complet | **720 Mo** |
| Dont fichiers **suivis par Git** (410 Mo) | PDF, XLSX, DWG, PPT… dont `slide carte représentation.pptx` 21,8 Mo, `Manuel_exploitation.pdf` 9 Mo, `métré.xlsx` 8,4 Mo |
| Dont **historique Git** (`.git`) | **306 Mo** |
| Plus gros fichiers | `memoire justificatif Giratoire.doc` 10,8 Mo · `lotissement la croix pruniau … fps.pdf` 9,6 Mo |

### 4.2 Sur quoi je m'appuyais (et pourquoi c'était insuffisant)

Mon argument était technique, pas éditorial :
1. **Git ne compresse pas les binaires** : chaque nouvelle version d'un PDF de 10 Mo ajoute 10 Mo à l'historique, pour toujours, chez chaque personne qui clone ;
2. **un clone devient pénible** : 410 Mo aujourd'hui, et ça ne fera qu'augmenter ;
3. **Git est fait pour du texte** : il ne peut pas montrer ce qui a changé entre deux plans.

**Pourquoi cet argument ne suffit pas — tu as raison :**
- Ce corpus n'est **pas un déchet** : c'est **la matière première qui donne sa crédibilité au module BTP** (les 154 documents, les sous-détails de prix, les métrés, les rapports). L'enlever, c'est livrer une démonstration vide ;
- Déplacer ces fichiers vers un stockage externe crée **deux sources de vérité** et des liens cassés — exactement ce que tu veux éviter ;
- **Un dépôt de 410 Mo n'est pas un problème** : au-delà de 1 Go, oui ; en dessous, c'est un confort de confort.

### 4.3 Nouvelle règle proposée (à la place de l'ancienne)

> **Les documents restent dans Git. On encadre seulement l'avenir.**

1. **Rien ne sort du dépôt.** Le corpus reste là où il est, avec son inventaire.
2. **Une politique écrite** (`docs/carre-das/07-POLITIQUE-DONNEES.md` à créer) :
   - les documents **de référence** (guides, prix, normes, plans types) : **dans Git**, ils sont la valeur du produit ;
   - les **données d'utilisateur** (un chantier client, une facture nominative, un dossier RH) : **jamais dans Git** — elles vivent dans l'application ;
   - **plafond** : au-delà de **~25 Mo par fichier** ou si un fichier change souvent, on décide explicitement (Git LFS, ou dossier de données local non suivi).
3. **Une vérification de propreté** au lieu d'une exclusion : passer les pièces qui contiennent des **données personnelles de tiers** (factures, noms, coordonnées, paie) au crible, et les anonymiser si besoin — c'est le vrai risque, pas la taille.
4. **Un test simple** : si le dépôt dépasse **1 Go**, on rouvre le sujet. Pas avant.

**Je retire donc la recommandation « sortir le corpus du dépôt ».** Elle est remplacée par : *« on garde tout, on écrit la règle, on surveille le poids ».*

---

## 5. Derniers modèles et outils libres — et ce qu'il faudra créer

*(voir le fichier dédié `06-ECOSYSTEME-LOCAL-GRATUIT.md`)*

---

## 6. Enrichir les cartes et les fiches — l'écosystème local gratuit

*(voir le fichier dédié `06-ECOSYSTEME-LOCAL-GRATUIT.md`)*

---

## 7. Récapitulatif des décisions que ça change

| # | Décision | Statut |
|---|---|---|
| 1 | Licence : **Apache-2.0 + CLA + marque + open core** | **proposé** (à valider) |
| 2 | Séquencer en 7 étapes « maison » avec un résultat visible à chaque étage | proposé |
| 3 | Ordre de construction **calqué sur ta chronologie réelle** (voir → comprendre → modéliser → chercher → outiller → unifier) | proposé |
| 4 | **Corpus conservé dans Git** + politique écrite + seuil de 1 Go | proposé (correction assumée) |
| 5 | Écosystème local : Kiwix / ZIM / NOMAD / cartes hors ligne (voir fichier 06) | proposé |
| 6 | Interface : V1 Le Carré + V2 L'Atelier + V3 L'Arbre | **en attente de ton choix** (voir fichier 04) |
