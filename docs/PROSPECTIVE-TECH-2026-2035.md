# 🔭 PROSPECTIVE 2026 → 2035 — L'accélération, année par année

> Document de prospective · 8 octobre 2026 · branche `arena/93b54a79-monorepo`
> **Sources** : GitHub (Octoverse, API trending), presse spécialisée (MIT Tech Review-class, IEA, Epoch AI), science (WMO/ONU climat), réseaux sociaux & Reddit (r/singularity, r/fusion), roadmaps industriels. Inspiration : *Les Revues du Monde — « Ces chercheurs ont prédit la fin de l'Histoire (et elle s'accélère) »* [vidéo](https://www.youtube.com/watch?v=GNxyOhgWZUA).
> **Méthode** : ni prophétie ni déni. On extrapole les tendances mesurées (Epoch AI), on écoute les signaux faibles (Reddit, GitHub), on cale sur les échéances institutionnelles (WMO, AI Act, roadmaps IBM/Google/Tesla), et on affecte une **confiance** à chaque bloc : 🟢 tendanciel / 🟡 probable / 🔴 spéculatif.

---

## 0. ⏱️ Le cadre : pourquoi « ça accélère »

- **L'horloge compressée** : sur 24 h d'histoire de la Terre, l'humanité apparaît à 23:58:43, l'écriture à 23:59:30, la révolution industrielle à 23:59:58, internet dans les dernières millisecondes (vidéo Les Revues du Monde).
- **Accélération sociale** (Hartmut Rosa) : les changements techniques, sociaux et biographiques s'enchaînent plus vite que le temps nécessaire pour les absorber — la TV a mis 35 ans à équiper les foyers, le smartphone 13 ans.
- **Retours exponentiels** (Kurzweil) : chaque innovation crée les conditions de la suivante. Version 2026 mesurable : les repos publics important un SDK LLM ont fait **+178 % en un an** ; ~**80 % des nouveaux développeurs GitHub utilisent Copilot dès la première semaine** ; **>1 million de pull requests rédigées par l'agent Copilot** entre mai et septembre 2025 ([Octoverse 2025](https://visualstudiomagazine.com/articles/2025/10/31/typescript-tops-github-octoverse-as-ai-era-reshapes-language-choices.aspx)).
- **La bonne méthode pour anticiper** (chapitre final de la vidéo) : fourchettes probabilistes + signaux précoces + révision continue — pas de date unique. C'est ce que fait ce document.

### Les deux profils comparés
| | **Profil A — Ingénieur·e à Paris, accès aux outils de pointe** | **Profil B — « Random » avec ~2 000 $/an de budget tech** |
|---|---|---|
| Accès | Agents frontier (API/cloud), GPU à la demande, outils agents (Claude Code, Copilot agents, Arena), monorepo perso | Abonnements grand public, smartphone milieu/haut de gamme, occasion |
| Levier | Orchestration, automatisation, données propriétaires | Consommation d'IA « incluse » (OS, apps) |
| Risque | Dépendance aux API, surcharge cognitive | Retard d'équipement, captivité plateformes |

---

## 1. 📍 Point de départ — octobre 2026 (état de l'art)

| Domaine | État des lieux | Source |
|---|---|---|
| IA / AGI | Labos : Altman « AGI fin 2026 », Amodei 2026-27, Hassabis 2030±1 · Prévisionnistes : **Metaculus avril 2033** (AGI « faible » : juin 2028) · AI 2027 : codeur surhumain ~mars 2027 · Karpathy 2035 · Panel LEAP : 2050 | [felloai](https://felloai.com/when-will-agi-happen/), [aimultiple](https://aimultiple.com/artificial-general-intelligence-singularity-timing), [veracalloway](https://www.veracalloway.com/blog/ai-culture/agi-timeline/) |
| Compute | Demande ×2,1/an (Epoch) ; runs d'entraînement → **10 GW en 2030** ; data centers → **945 TWh en 2030** (IEA) | [Epoch AI in 2030](https://epoch.ai/files/AI_2030.pdf), [whenwill.ai](https://whenwill.ai/) |
| Climat | WMO : **70 %** de chances que la moyenne 2025-2029 dépasse +1,5 °C ; 86 % qu'au moins une année >1,5 °C ; 80 % qu'une année batte 2024 | [WMO 2025-2029](https://wmo.int/sites/default/files/2025-05/WMO_GADCU_2025-2029_Final.pdf) |
| Robotique | Coûts humanoïdes **−40 % entre 2023 et 2024** (Goldman) ; Unitree G1 à 13 500 $ ; Optimus cible 20-30 k$ ; pilotes usine Occident : 90-100 k$/unité | [kashafnoor](https://www.kashafnoor.com/2026/04/humanoid-robots-2026-tesla-optimus.html) |
| Santé | GLP-1 : +38 %/an de prescriptions, marché → **~100 Md$ en 2030** ; mais OMS : **<10 % des personnes éligibles** traitées d'ici 2030 | [McKinsey](https://www.mckinsey.com/featured-insights/themes/glp1s-are-changing-obesity-care-what-comes-next), [cypris](https://www.cypris.ai/insights/patent-and-innovation-trends-in-glp-1-and-weight-loss-drugs-2020-2025-what-the-ip-and-the-science-signal-next) |
| Quantique | IBM Starling (~200 qubits logiques) **2029** ; Quantinuum Apollo 2029 ; Google « fin de décennie » ; casser RSA exigerait des milliers de qubits logiques → pas avant 2035+ | [roadmaps 2026-2030](https://andesqubit.com/en/blog/quantum-hardware-roadmaps-2026-2030/), [IBM](https://postquantum.com/quantum-computing-companies/ibm/) |
| Régulation | AI Act : GPAI depuis 08/2025 ; transparence/deepfakes **02/08/2026** ; haut risque annexe III **reporté au 02/12/2027** (Digital Omnibus, voté 16/06/2026) | [studeria](https://www.studeria.fr/articles-de-blog/ai-act-definition-niveaux-risque-calendrier), [dastra](https://www.dastra.eu/fr/blog/calendrier-ai-act-toutes-les-echeances-a-connaitre-pour-rester-conforme-au-regl/60277) |
| Confiance/info | C2PA + SynthID intégrés nativement dans Chrome/Search (Google I/O 2026) ; California CAITA : labels 2027, signature matérielle à la capture 2028 | [thefulcrum](https://thefulcrum.us/media-technology/ai-disinformation-2026-midterm-elections-threats-election-integrity), [techspective](https://techspective.net/2026/05/28/the-war-on-deepfakes/) |
| Hardware perso | Lunettes IA : Meta $249→799 (+ Neural Band), Samsung 2026, Apple pas avant 2027 ; toujours compagnon du smartphone | [dev.to](https://dev.to/the_daily_flare/smart-glasses-how-the-technology-is-advancing-in-2026-29pm), [docam](https://docam.io/articles/smartphones-vs-smartphones-2026) |

---

## 2. 📅 Horizon 1 — les 5 prochaines années (2027 → 2030/31)

### 2027 — « l'année des agents au travail » 🟡
- **Tech** : les agents deviennent des « collègues distants » : IDC prévoit une charge token/API ×1000 et ~40 % des apps d'entreprise avec automatisation agentique ([whenwill.ai](https://whenwill.ai/)). SWE-bench saturé, l'enjeu bascule sur les tâches de plusieurs heures (RE-Bench) ([Epoch](https://epoch.ai/files/AI_2030.pdf)). Scénario AI 2027 : codeur surhumain dès mars 2027 — **contesté** mais directionnellement plausible (🔴 sur la date, 🟢 sur la tendance). Ventes publiques Optimus visées fin 2027 à 20-30 k$ ([optimusk](https://optimusk.blog/blog/tesla-optimus-price/)).
- **Environnement** : dans la fenêtre WMO 2025-2029 ; probabilité forte d'une année >1,5 °C ; canicules françaises récurrentes, l'énergie des data centers entre dans le débat public ([WMO](https://wmo.int/sites/default/files/2025-05/WMO_GADCU_2025-2029_Final.pdf)).
- **Société** : premières sanctions AI Act (transparence, deepfakes) ; étiquetage IA obligatoire en Californie (CAITA) ; les midterms US font de l'IA un sujet central ([r/singularity](https://www.reddit.com/r/singularity/comments/1pvkki4/your_predictions_for_the_year_of_2026/)).
- **Individu/Groupe** : premiers remplacements visibles sur l'entry-level white collar (🟡) ; « il faut apprendre à manager des agents » devient une compétence de base (consensus Reddit [1](https://www.reddit.com/r/singularity/comments/1ntlc7t/are_we_almost_done_exponential_ai_progress/) [2](https://www.reddit.com/r/singularity/comments/1q0hsc9/singularity_predictions_2026/)).
- **Profil A** : orchestre 3-10 agents (code, veille, admin), possède son monorepo git-first, ses données perso alimentent ses agents. **Profil B** : assistants IA inclus dans l'OS et les abonnements (~20-40 $/mois), lunettes IA d'entrée de gamme (~$250-450) ; les 2 000 $ couvrent téléphone + lunettes + abonnements.

### 2028 — « l'année de la preuve et de l'énergie » 🟡
- **Tech** : Helion doit livrer 50 MW de fusion à Microsoft (PPA signé 2023) — pari industriel, risque de glissement ([contrary](https://research.contrary.com/company/helion)) ; Tesla vise 100 k+ Optimus ([optimusk](https://optimusk.blog/blog/tesla-optimus-price/)) ; les modèles ouverts rattrapent les fermés de ~2 ans (tendance observée depuis Llama) 🟡.
- **Environnement** : la moyenne quinquennale 2024-2028 flirte avec +1,5 °C (WMO : 70 % sur 2025-2029) ; plans canicule/eau renforcés en Europe du Sud.
- **Société** : conformité « haut risque » AI Act (entrée 02/12/2027) opérationnelle ; début des débats UBI/revenu de transition (prédiction récurrente r/singularity : « UBI nécessaire d'ici 2030 » ([thread](https://www.reddit.com/r/singularity/comments/1q0hsc9/singularity_predictions_2026/))) 🔴.
- **Individu/Groupe** : la **provenance** devient un réflexe : en Californie, les appareils de capture signent le contenu « authentique » à la prise de vue (CAITA 2028) ([thefulcrum](https://thefulcrum.us/media-technology/ai-disinformation-2026-midterm-elections-threats-election-integrity)) ; « vu » ≠ « vrai » sans Content Credentials.
- **Profil A** : agents perso 24/7 (mail, budget, planning) + modèle local open-source pour les données sensibles ; commence à arbitrer coût GPU vs API. **Profil B** : traduction instantanée et assistant vocal banalisés ; la fracture se déplace vers la **maîtrise** (qui configure vs qui subit les réglages par défaut).

### 2029 — « l'année des qubits logiques » 🟢 (roadmaps convergents)
- **Tech** : IBM **Starling ~200 qubits logiques / 100 M de portes** ; Quantinuum Apollo ; Microsoft cible 2029 ([roadmaps](https://andesqubit.com/en/blog/quantum-hardware-roadmaps-2026-2030/)). Les modèles demandent **10-100× moins de compute** à capacité égale (International AI Safety Report via [whenwill.ai](https://whenwill.ai/)) → l'IA de pointe se diffuse vers le hardware local.
- **Environnement** : les data centers approchent les 945 TWh/an (IEA) ; premiers SMR couplés à des data centers ; arbitrage électrification vs sobriété en France 🟡.
- **Société** : médiane Metaculus « AGI faible » (juin 2028) atteinte ou dépassée : la dispute porte sur le mot AGI pendant que les tâches s'automatisent (« on débattera d'AGI jusqu'en 2035 pendant que les jobs disparaissent » — r/singularity) ; mouvement « slow tech » en réaction à l'accélération (Rosa) 🟡.
- **Profil A** : flotte d'agents spécialisée (dev, admin, santé, finance) ; tests quantiques en cloud ; arbitre « posséder son compute » (station locale) vs louer. **Profil B** : avec 2 000 $, achète l'équivalent de ~8-10 k$ de tech 2026 (déflation matérielle : IA locale sur téléphone, lunettes avec assistant complet, occasion premium).

### 2030 — « l'année-charnière » 🟡
- **Tech** : synthèse Epoch : modèles entraînés avec **1000× le compute de 2025**, runs à **~200 Md$** (~1 % du PIB US), l'IA « au moins aussi importante qu'internet » ; productivité +10-20 % minimum sur les tâches non expérimentales ([Epoch AI in 2030](https://epoch.ai/files/AI_2030.pdf)). DeepMind/Hassabis : AGI « vers 2030, à un an près » ([felloai](https://felloai.com/when-will-agi-happen/)).
- **Robotique** : humanoïdes **<17 000 $** l'unité (Bank of America) ([kashafnoor](https://www.kashafnoor.com/2026/04/humanoid-robots-2026-tesla-optimus.html)) → déploiement industriel massif, premières flottes logistiques ; pas encore dans les foyers.
- **Santé** : GLP-1 ≈ 100 Md$/an, effet macro +0,4 % PIB US estimé ([ITIF](https://itif.org/publications/2025/08/18/a-shot-at-a-healthier-future-the-transformative-potential-of-glp-1s/)) ; mais l'OMS prévoit <10 % des éligibles couverts → l'accès reste un marqueur d'inégalité ([cypris](https://www.cypris.ai/insights/patent-and-innovation-trends-in-glp-1-and-weight-loss-drugs-2020-2025-what-the-ip-and-the-science-signal-next)).
- **Environnement** : la moyenne 2026-2030 a très probablement franchi +1,5 °C en tendance ; l'adaptation (îlots de fraîcheur, réseaux, assurance) pèse sur les budgets publics 🟢.
- **Société** : restructuration du tertiaire ; la question « qui paie la formation et la transition » domine les élections ; l'UE applique l'AI Act aux autorités publiques (échéance 02/08/2030) ([dastra](https://www.dastra.eu/fr/blog/calendrier-ai-act-toutes-les-echeances-a-connaitre-pour-rester-conforme-au-regl/60277)).
- **Profil A** : « chief of staff » IA personnel : agenda, budget, mails, santé, code — supervisé mais autonome ; les données git-first prennent de la valeur (mémoire longue). **Profil B** : l'IA est un service public/inclus (guichets, santé, éducation), mais la **capitalisation** diverge : ceux qui possèdent agents/données/compute accumulent, les autres louent.

---

## 3. 📅 Horizon 2 — les 5 suivantes (2031 → 2035) · confiance globalement 🔴/🟡

### 2031 — robots en série, fusion en sursis
- Humanoïdes classe Optimus à 15-20 k$ en production de masse (objectif Tesla « 1 M/an ») ([optimusk](https://optimusk.blog/blog/tesla-optimus-vs-human-cost/)) ; premiers usages B2C aisés (assistance personnes âgées — Japon/Europe) 🔴.
- Si Helion/CFS ont tenu leurs calendriers : **premières livraisons commerciales de fusion** (CFS/ARC : PPA Google 200 MW, « début des années 2030 » ([nucnet](https://www.nucnet.org/news/microsoft-backed-fusion-company-begins-work-on-washington-nuclear-fusion-plant-7-4-2025))) ; sinon, SMR nucléaires + solaire/batteries comme plancher 🟡.

### 2032 — IA de la science & souverainetés
- L'IA « fait de la science » : implémentation de logiciels scientifiques complexes en langage naturel, assistance à la formalisation de preuves (Epoch : déjà en trajectoire 2027-2030) → accélérations en matériaux (batteries), biologie, pharma 🟡.
- Chaque grande puissance opère ses modèles souverains ; l'Europe : Mistral & co en champions d'infrastructure, ou dépendance assumée — choix politique français/européen majeur 🟡.

### 2033 — le seuil symbolique
- Médiane Metaculus « AGI » (avril 2033) : que le mot soit prononcé ou non, la plupart des tâches intellectuelles décomposables en contexte fini sont automatisables ; Karpathy : « AGI = employé/intéressant fiable » vers 2035 ([aimultiple](https://aimultiple.com/artificial-general-intelligence-singularity-timing)).
- Statut juridique des agents (responsabilité, « personnalité électronique » ou non) tranché dans l'UE 🟡.

### 2034 — transition post-quantique sous tension
- Les premières machines à erreur corrigée (2029-2031) montent en échelle ; la migration cryptographique post-quantique (débutée dès 2024 avec les standards NIST) doit être achevée pour les systèmes critiques 🟡.
- Débats fiscaux : taxation du compute et/ou « dividende robot » pour financer la transition du travail 🔴.

### 2035 — deux futurs plausibles
- **Scénario rapide** (AI 2027 et labos avaient raison) : intelligence surhumaine de niche généralisée, R&D automatisée, croissance tirée par l'automatisation ; tensions sociales fortes, gouvernance en retard 🔴.
- **Scénario lent** (LeCun/panel LEAP : 2050) : IA = infrastructure mature type électricité, gains de productivité diffus, le travail se recompose plus qu'il ne disparaît 🟡.
- **Constante des deux** : provenance cryptographique généralisée (C2PA), robots physiques courants dans l'industrie et la logistique, climat à ~+1,6/1,8 °C avec adaptation obligatoire, santé métabolique transformée par GLP-1 et successeurs.

---

## 4. 🆚 La divergence des deux profils sur 10 ans

| Dimension | Profil A (ingénieur Paris, outils de pointe) | Profil B (2 000 $/an) | Verdict |
|---|---|---|---|
| **IA au travail** | Multiplie sa production ×5-10 en orchestrant des agents dès 2026-2027 ; chaque année d'avance se capitalise | Gagne +10-30 % via assistants inclus ; rattrape 2-3 ans plus tard | **Écart maximal en 2027-2029**, se resserre après par diffusion |
| **Coût d'accès** | API/compute = budget, mais ROI élevé | La déflation matérielle rend « inclus » ce qui était premium : 2 000 $ de 2031 ≈ 10 000 $ de 2026 | Le prix ne protège plus ; **la compétence d'orchestration oui** |
| **Santé** | Accès précoce GLP-1/diagnostics IA, quantified-self | Accès via santé publique, avec file d'attente | Inégalité d'accès persistante (OMS : <10 % des éligibles en 2030) |
| **Énergie/climat** | Peut investir (solaire, véhicule efficient, résilience domicile) | Subit les prix de l'énergie et les canicules | L'adaptation climatique est **régressive** |
| **Confiance/info** | Vérifie par provenance (C2PA), sources primaires, agents de veille | Dépend des labels plateforme | Les deux exposés ; l'éducation aux médias devient vitale |
| **Capital** | Possède ses données/agents (git-first) → actif qui s'apprécie | Loue ses assistants → dépendance plateforme | **Le vrai clivage de la décennie : propriétaire vs locataire de son IA** |

> **Le point le plus important** : la déflation technologique rendra l'*accès* quasi universel ; ce qui divergera, c'est la **propriété** (données, agents, compute, énergie) et la **maîtrise** (savoir diriger des agents). C'est exactement là que se joue l'écart entre A et B.

---

## 5. 🎲 Cartes sauvages (ce qui peut tout décaler)

| Événement | Effet | Probabilité |
|---|---|---|
| Fusion commerciale dès 2028-2032 | Énergie quasi illimitée → accélération maximale du compute | 🔴 faible-moyenne |
| Crise de type « AI winter » financier (promesses > revenus) | Ralentissement 2-3 ans, consolidation | 🟡 non négligeable |
| Conflit/embargo semi-conducteurs (Taïwan) | Coup de frein brutal sur le compute mondial | 🟡 |
| Effondrement de confiance (deepfake majeur non détecté) | Régulation d'urgence, frein social | 🟡 |
| Percée « continual learning » (prédiction r/singularity) | Compression des timelines AGI de 3-5 ans | 🔴 |
| Mouvement social « slow tech » / néo-luddite | Ralentissement volontaire, régulation travail | 🟡 |
| Réponse climatique d'urgence (guerre-économie verte) | Accélération énergétique, contraintes individuelles | 🟡 |

---

## 6. 🧭 Ce que ça change concrètement pour toi (ingénieur à Paris, avec ce monorepo)

1. **Tu es déjà positionné Profil A** : monorepo git-first, agents (Arena), mail-organizer, life-hub — c'est *exactement* le pattern « propriétaire de ses données + orchestration d'agents » qui capitalise sur 10 ans. → **continuer le Life Hub (décision en attente)**.
2. **Compétence-clé 2027-2030** : diriger des flottes d'agents (specs, validation, contexte). Ton doc `FEATURES-INVENTORY.md` + LifeOS (ISA/Algorithm) sont des brouillons de cette compétence.
3. **Souveraineté des données** : git-first + local-first te protègent des deux risques majeurs (lock-in plateforme, vie privée vs agents cloud). Garde un chemin 100 % local (modèles ouverts).
4. **Énergie/climat à Paris** : l'adaptation (canicules, prix) sera le poste de dépense croissant — le volet budget du Life Hub devrait tracker énergie/alimentation dès maintenant.
5. **Santé** : la fenêtre GLP-1/diagnostic IA 2027-2030 = meilleur ratio coût/bénéfice santé de la décennie pour un profil A informé.
6. **Post-quantique** : rien à faire avant 2030 côté perso, mais tes choix de stockage long terme (git, chiffrement) doivent rester migrables.
7. **Règle anti-vertige** (la vidéo a raison) : ne pas chercher LA date ; surveiller 4 signaux chaque trimestre — METR/longueur des tâches agents, FrontierMath, coût des humanoïdes, température annuelle WMO.

---

## 7. 📚 Sources principales
- **Accélération/cadre** : Les Revues du Monde ([vidéo](https://www.youtube.com/watch?v=GNxyOhgWZUA)) — Rosa, Kurzweil, méthode prévisionnelle
- **IA/timelines** : [felloai.com](https://felloai.com/when-will-agi-happen/) · [aimultiple.com](https://aimultiple.com/artificial-general-intelligence-singularity-timing) (10 000 prédictions) · [whenwill.ai](https://whenwill.ai/) · [veracalloway.com](https://www.veracalloway.com/blog/ai-culture/agi-timeline/) · [Epoch — AI in 2030 (PDF)](https://epoch.ai/files/AI_2030.pdf)
- **GitHub/développeurs** : [Octoverse 2025 — Visual Studio Magazine](https://visualstudiomagazine.com/articles/2025/10/31/typescript-tops-github-octoverse-as-ai-era-reshapes-language-choices.aspx) · [webpronews](https://www.webpronews.com/github-octoverse-2025-630m-repos-ai-fuels-developer-surge/) · [ODSC — top agentic repos](https://opendatascience.com/the-top-ten-github-agentic-ai-repositories-in-2025/)
- **Climat (Nature/WMO/ONU)** : [WMO Global Annual to Decadal Update 2025-2029 (PDF)](https://wmo.int/sites/default/files/2025-05/WMO_GADCU_2025-2029_Final.pdf) · [climatechangenews](https://www.climatechangenews.com/2025/05/28/scientists-predict-global-warming-of-more-than-1-5c-for-2025-2029-period/) · [UN Climate Reports (COP30)](https://www.un.org/en/climatechange/reports)
- **Robotique** : [kashafnoor.com](https://www.kashafnoor.com/2026/04/humanoid-robots-2026-tesla-optimus.html) · [optimusk.blog prix](https://optimusk.blog/blog/tesla-optimus-price/) · [optimusk.blog vs travail humain](https://optimusk.blog/blog/tesla-optimus-vs-human-cost/)
- **Énergie** : [Contrary Research — Helion](https://research.contrary.com/company/helion) · [NucNet — fusion Washington + CFS/Google](https://www.nucnet.org/news/microsoft-backed-fusion-company-begins-work-on-washington-nuclear-fusion-plant-7-4-2025) · [r/fusion coûts](https://www.reddit.com/r/fusion/comments/1b73kde/fusion_projected_cost_per_kwh_vs_solar_and_storage/)
- **Santé/GLP-1** : [McKinsey](https://www.mckinsey.com/featured-insights/themes/glp1s-are-changing-obesity-care-what-comes-next) · [ITIF](https://itif.org/publications/2025/08/18/a-shot-at-a-healthier-future-the-transformative-potential-of-glp-1s/) · [cypris brevets](https://www.cypris.ai/insights/patent-and-innovation-trends-in-glp-1-and-weight-loss-drugs-2020-2025-what-the-ip-and-the-science-signal-next)
- **Quantique** : [andesqubit — roadmaps 2026-2030](https://andesqubit.com/en/blog/quantum-hardware-roadmaps-2026-2030/) · [postquantum.com — IBM Starling](https://postquantum.com/quantum-computing-companies/ibm/) · [Quantum Insider](https://thequantuminsider.com/2025/05/16/quantum-computing-roadmaps-a-look-at-the-maps-and-predictions-of-major-quantum-players/)
- **Régulation** : [studeria.fr AI Act](https://www.studeria.fr/articles-de-blog/ai-act-definition-niveaux-risque-calendrier) · [reglementation-ia.fr](https://reglementation-ia.fr/ia-act-guide-complet) · [dastra.eu calendrier](https://www.dastra.eu/fr/blog/calendrier-ai-act-toutes-les-echeances-a-connaitre-pour-rester-conforme-au-regl/60277)
- **Confiance/deepfakes** : [thefulcrum.us](https://thefulcrum.us/media-technology/ai-disinformation-2026-midterm-elections-threats-election-integrity) · [metayeda.com](https://www.metayeda.com/p/ai-deepfakes-elections) · [techspective — Google I/O 2026 C2PA](https://techspective.net/2026/05/28/the-war-on-deepfakes/)
- **Réseaux/Reddit** : [r/singularity — prédictions 2026](https://www.reddit.com/r/singularity/comments/1q0hsc9/singularity_predictions_2026/) · [r/singularity — 2026-2027 décisives](https://www.reddit.com/r/singularity/comments/1ntlc7t/are_we_almost_done_exponential_ai_progress/) · [r/singularity — vos prédictions 2026](https://www.reddit.com/r/singularity/comments/1pvkki4/your_predictions_for_the_year_of_2026/)
- **Hardware grand public** : [dev.to smart glasses 2026](https://dev.to/the_daily_flare/smart-glasses-how-the-technology-is-advancing-in-2026-29pm) · [docam.io](https://docam.io/articles/smart-glasses-vs-smartphones-2026) · [solidaitech](https://www.solidaitech.com/2026/09/meta-glasses-ray-ban-gen-3-display-muse.html)
