import json
from pathlib import Path

def get_obsidian_dataset():
    nodes = [
        # 1. RAPPORTS (🟣 #a855f7)
        {
            "id": "doc_00",
            "label": "00 - Synthèse Globale & État de l'Art 2026",
            "group": "Rapports Maîtres",
            "val": 28,
            "color": "#a855f7",
            "tags": ["#rapport", "#synthese", "#etatdelart", "#corpus"],
            "summary": "Synthèse exécutive unifiant les 154 sources réelles du corpus, les 7 phases A-Z et le BIM IFC 4.3.",
            "content": """---
title: 00 - Synthèse Globale & État de l'Art 2026
tags: [#rapport, #synthese, #etatdelart, #corpus]
group: Rapports Maîtres
date: 2026-09-09
---

# 00 - Synthèse Globale & État de l'Art 2026

Ce rapport constitue la **pierre angulaire** de la plateforme BTP Autonomous Command. Il réunit l'analyse méthodique des 154 documents du corpus d'entreprise avec les standards technologiques et juridiques de 2026.

## Nœuds Liés dans le Vault
- [[07 - Schéma Directeur A à Z & Formules]] : La cartographie complète des 7 phases de chantier.
- [[08 - OpenBIM IFC 4.3 & Jumeau Numérique]] : L'intégration 3D/5D et détection des clashs.
- [[01 - Analyse Marchés DCE & CCAG 2021]] : Le cadre contractuel et juridique.
- [[02 - Étude de Prix & 28 SDP]] : Le moteur analytique de déboursé sec.
- [[04 - Sécurité DICT, AIPR & Anti-Endommagement]] : La conformité zéro accident.
- [[06 - Réception, DOE SI 022 & Clôture]] : Le protocole de fin de chantier standardisé.

## Chantiers Étudiés
- [[Giratoire Barbazan (152 795 € HT)]]
- [[Piste Éolienne Saint-Nicolas (46 800 € HT)]]
- [[Traverse Aurouer (187 400 € HT)]]
"""
        },
        {
            "id": "doc_01",
            "label": "01 - Analyse Marchés DCE & CCAG 2021",
            "group": "Rapports Maîtres",
            "val": 22,
            "color": "#a855f7",
            "tags": ["#rapport", "#dce", "#ccag2021", "#juridique"],
            "summary": "Analyse critique des pièces du DCE, du CCAG-Travaux 2021, de la pondération prix/technique et de la gestion des ordres de service.",
            "content": """---
title: 01 - Analyse Marchés DCE & CCAG 2021
tags: [#rapport, #dce, #ccag2021, #juridique]
group: Rapports Maîtres
date: 2026-09-09
---

# 01 - Analyse des Marchés Publics & Cadre Juridique DCE

Ce rapport décortique la structure contractuelle des marchés de VRD et de terrassement sous le régime du **CCAG Travaux 2021**.

## Points Clés & Règles
- Hiérarchie des pièces : CCAP > CCTP > BPU / DQE > Mémoire Technique.
- Gestion des Ordres de Service (OS) et délais de recours sous 30 jours (Art. 14).
- Application des pénalités journalières de retard plafonnées à 10% du montant du marché.

## Nœuds Liés
- [[CCAG Travaux 2021]]
- [[Phase 0 : Consultation & DCE]]
- [[Phase 1 : Étude de Prix & Déboursés]]
- [[AGENT_LEGAL (Marchés & DCE)]]
- [[Giratoire Barbazan (152 795 € HT)]]
"""
        },
        {
            "id": "doc_02",
            "label": "02 - Étude de Prix & 28 SDP",
            "group": "Rapports Maîtres",
            "val": 24,
            "color": "#a855f7",
            "tags": ["#rapport", "#chiffrage", "#sdp", "#budget"],
            "summary": "Décomposition analytique des 28 Sous-Détails de Prix réels du corpus, calcul du THMO et coefficient multiplicateur K.",
            "content": """---
title: 02 - Étude de Prix & 28 SDP
tags: [#rapport, #chiffrage, #sdp, #budget]
group: Rapports Maîtres
date: 2026-09-09
---

# 02 - Étude de Prix, Méthodes & Sous-Détails (SDP)

Analyse approfondie de la chaîne de rentabilité d'une entreprise de Travaux Publics :

$$\\mathbf{DS} = \\sum MO + \\sum MAT + \\sum MATER + \\sum ST \\quad \\Rightarrow \\quad \\mathbf{PV_{HT}} = DS \\times K$$

## Formules Directes
- [[Formule Déboursé Sec (DS)]]
- [[Coefficient Multiplicateur Vente (K)]]
- [[Taux THMO Ouvrier & Charges]]
- [[Formule Révision Paramétrique TP08]]

## Nœuds Liés
- [[Phase 1 : Étude de Prix & Déboursés]]
- [[AGENT_BUDGET (Prix & 28 SDP)]]
- [[SDP 12 : Bordure Béton T2 Préfabriquée]]
- [[SDP 18 : Enrobé Bitumineux BB 0/10]]
"""
        },
        {
            "id": "doc_03",
            "label": "03 - Technique VRD, Enrobés & Hydraulique",
            "group": "Rapports Maîtres",
            "val": 22,
            "color": "#a855f7",
            "tags": ["#rapport", "#technique", "#vrd", "#hydraulique"],
            "summary": "Guides de mise en œuvre : couches de chaussée BB/GB/GNT, dimensionnement hydraulique Manning-Strickler et compactage.",
            "content": """---
title: 03 - Technique VRD, Enrobés & Hydraulique
tags: [#rapport, #technique, #vrd, #hydraulique]
group: Rapports Maîtres
date: 2026-09-09
---

# 03 - Technique Voirie, Réseaux et Terrassement

Prescriptions d'exécution in-situ pour les travaux de voirie et canalisations :
- Dimensionnement des canalisations : [[Hydraulique Manning-Strickler]]
- Vérification de la portance sous couche d'assise : [[Portance Dynaplaque Westergaard EV2]]
- Température de compactage des enrobés : [[Thermométrie & Compactage BBSG]]

## Nœuds Liés
- [[Phase 3 : Exécution & Pilotage Terrain]]
- [[Fascicule 70 (Canalisations Assainissement)]]
- [[IfcRoad & IfcCourse (Chaussée BB/GNT)]]
- [[IfcPipeSegment (Réseau Assainissement EU)]]
"""
        },
        {
            "id": "doc_04",
            "label": "04 - Sécurité DICT, AIPR & Anti-Endommagement",
            "group": "Rapports Maîtres",
            "val": 22,
            "color": "#a855f7",
            "tags": ["#rapport", "#securite", "#dict", "#aipr"],
            "summary": "Cadre réglementaire anti-endommagement des réseaux, Cerfa 14023*01, marquage-piquetage et habilitations AIPR.",
            "content": """---
title: 04 - Sécurité DICT, AIPR & Anti-Endommagement
tags: [#rapport, #securite, #dict, #aipr]
group: Rapports Maîtres
date: 2026-09-09
---

# 04 - Réglementation Anti-Endommagement, DICT & Sécurité

Guide réglementaire absolu pour la prévention des accidents de chantier :
- Procédure obligatoire : [[Décret Anti-Endommagement (Cerfa 14023*01)]]
- Habilitation des personnels : [[Habilitation AIPR Encadrant / Concepteur]]
- Règles de croisement sous-terrain : [[Norme NF P 98-332 (Croisements Réseaux)]]
- Plan Général de Coordination : [[Plan Général de Coordination (PGC SPS)]]

## Nœuds Liés
- [[Phase 2 : Préparation 30j & DICT]]
- [[AGENT_DICT_SAFETY (Sécurité & AIPR)]]
"""
        },
        {
            "id": "doc_05",
            "label": "05 - Pilotage In-Situ, Litiges & Aléas",
            "group": "Rapports Maîtres",
            "val": 20,
            "color": "#a855f7",
            "tags": ["#rapport", "#chantier", "#litiges", "#journal"],
            "summary": "Management de chantier : tenue du journal de bord vocal, traitement des non-conformités, gestion des intempéries et réclamations.",
            "content": """---
title: 05 - Pilotage In-Situ, Litiges & Aléas
tags: [#rapport, #chantier, #litiges, #journal]
group: Rapports Maîtres
date: 2026-09-09
---

# 05 - Pilotage In-Situ, Journal de Chantier & Gestion des Aléas

Protocoles de gestion quotidienne pour le conducteur de travaux et chef de chantier :
- Suivi journalier des effectifs, matériels et intempéries météo certifiées.
- Émission immédiate des Fiches de Non-Conformité (FNC) et courriers de réserve sous 30 jours.
- Réclamations financières et délais supplémentaires selon le [[CCAG Travaux 2021]].

## Nœuds Liés
- [[Phase 3 : Exécution & Pilotage Terrain]]
- [[Phase 4 : Pointage & Révision TP08]]
- [[AGENT_TELEMETRY (Vision & Capteurs)]]
- [[AGENT_PLANNING_LEAN (Last Planner 4D)]]
"""
        },
        {
            "id": "doc_06",
            "label": "06 - Réception, DOE SI 022 & Clôture",
            "group": "Rapports Maîtres",
            "val": 22,
            "color": "#a855f7",
            "tags": ["#rapport", "#doe", "#reception", "#trackdechets"],
            "summary": "Standard DOE SI 022 Aéroports de Lyon (37 pages), Opérations Préalables à la Réception, DGD Chorus Pro et Trackdéchets.",
            "content": """---
title: 06 - Réception, DOE SI 022 & Clôture
tags: [#rapport, #doe, #reception, #trackdechets]
group: Rapports Maîtres
date: 2026-09-09
---

# 06 - Réception, Clôture, DOE et Transition Numérique

Cadre normatif pour la clôture réussie d'un marché public :
- Standard documentaire d'excellence : [[Standard DOE SI 022 Aéroports (37p)]]
- Traçabilité environnementale : [[Loi AGEC & Trackdéchets (BSDD)]]
- Télétransmission du solde : [[Portail Chorus Pro (DGD Solde)]]

## Nœuds Liés
- [[Phase 5 : Réception & Levée Réserves]]
- [[Phase 6 : DOE SI 022 & DGD Final]]
- [[AGENT_DOE_CLOSEOUT (Standard SI 022)]]
"""
        },
        {
            "id": "doc_07",
            "label": "07 - Schéma Directeur A à Z & Formules",
            "group": "Rapports Maîtres",
            "val": 26,
            "color": "#a855f7",
            "tags": ["#rapport", "#schema", "#formules", "#lifecycle"],
            "summary": "Cartographie complète des 7 phases de vie d'un chantier VRD avec formulaires mathématiques d'ingénierie et de chiffrage.",
            "content": """---
title: 07 - Schéma Directeur A à Z & Formules
tags: [#rapport, #schema, #formules, #lifecycle]
group: Rapports Maîtres
date: 2026-09-09
---

# 07 - Schéma Directeur de la Chaîne Chantier de A à Z

Ce document détaille l'intégralité du cycle de vie opérationnel d'un projet de Travaux Publics :

```
[Phase 0] -> [Phase 1] -> [Phase 2] -> [Phase 3] -> [Phase 4] -> [Phase 5] -> [Phase 6]
```

## Phases Détaillées
- [[Phase 0 : Consultation & DCE]]
- [[Phase 1 : Étude de Prix & Déboursés]]
- [[Phase 2 : Préparation 30j & DICT]]
- [[Phase 3 : Exécution & Pilotage Terrain]]
- [[Phase 4 : Pointage & Révision TP08]]
- [[Phase 5 : Réception & Levée Réserves]]
- [[Phase 6 : DOE SI 022 & DGD Final]]

## Formulaires Liés
- [[Formule Déboursé Sec (DS)]] | [[Coefficient Multiplicateur Vente (K)]] | [[Formule Révision Paramétrique TP08]]
- [[Hydraulique Manning-Strickler]] | [[Portance Dynaplaque Westergaard EV2]]
"""
        },
        {
            "id": "doc_08",
            "label": "08 - OpenBIM IFC 4.3 & Jumeau Numérique",
            "group": "Rapports Maîtres",
            "val": 24,
            "color": "#a855f7",
            "tags": ["#rapport", "#bim", "#ifc43", "#clash"],
            "summary": "Standards OpenBIM infrastructure (ISO 16739), formats IFC 4.3, LandXML 1.2, détection de clashs 3D et liaison 5D devis.",
            "content": """---
title: 08 - OpenBIM IFC 4.3 & Jumeau Numérique
tags: [#rapport, #bim, #ifc43, #clash]
group: Rapports Maîtres
date: 2026-09-09
---

# 08 - BIM Infrastructure, IFC 4.3 & Jumeau Numérique VRD

Guide d'ingénierie numérique 3D/4D/5D pour les Travaux Publics :
- Structure spatiale et objets linéaires : [[IfcProject (ZAC Barbazan VRD)]], [[IfcRoad & IfcCourse (Chaussée BB/GNT)]], [[IfcPipeSegment (Réseau Assainissement EU)]].
- Contrôle des proximités souterraines : [[Norme NF P 98-332 (Croisements Réseaux)]].
- Échange pour guidage d'engins GPS 3D : [[LandXML 1.2 (Guidage GPS Engins 3D)]].
- Gestion collaborative des réserves : [[BCF 2.1 (Coordination & Rapports Clashs)]].

## Agents Liés
- [[AGENT_BIM_3D (IFC 4.3 & Clashs)]]
"""
        },

        # 2. PHASES DU CYCLE DE VIE (🔵 #38bdf8)
        {
            "id": "phase_0",
            "label": "Phase 0 : Consultation & DCE",
            "group": "Phases A-Z",
            "val": 18,
            "color": "#38bdf8",
            "tags": ["#phase", "#dce", "#marche"],
            "summary": "Études préalables géotechniques G1/G2, constitution du DCE (CCTP, CCAP, BPU, DQE, PGC) et analyse des offres.",
            "content": """---
title: Phase 0 : Consultation & DCE
tags: [#phase, #dce, #marche]
group: Phases A-Z
date: 2026-09-09
---

# Phase 0 : Consultation, DCE & Choix des Entreprises

Étape d'initialisation sous la responsabilité de la Maîtrise d'Ouvrage (MOA) et Maîtrise d'Œuvre (MOE).

## Documents Clés
- Avis d'Appel Public à Concurrence (AAPC)
- Règlement de Consultation (RC)
- Cahier des Clauses Techniques Particulières (CCTP)
- [[CCAG Travaux 2021]]

## Nœuds Liés
- [[01 - Analyse Marchés DCE & CCAG 2021]]
- [[AGENT_LEGAL (Marchés & DCE)]]
- [[Phase 1 : Étude de Prix & Déboursés]]
"""
        },
        {
            "id": "phase_1",
            "label": "Phase 1 : Étude de Prix & Déboursés",
            "group": "Phases A-Z",
            "val": 20,
            "color": "#38bdf8",
            "tags": ["#phase", "#chiffrage", "#sdp", "#k"],
            "summary": "Étude technique et financière : décomposition Déboursé Sec (DS), THMO, coefficient K et offre de prix.",
            "content": """---
title: Phase 1 : Étude de Prix & Déboursés
tags: [#phase, #chiffrage, #sdp, #k]
group: Phases A-Z
date: 2026-09-09
---

# Phase 1 : Étude de Prix, Déboursés & Offre Technique

Chiffrage minutieux réalisé par le Bureau d'Études de Prix de l'entreprise :
$$\\mathbf{DS} = MO + MAT + MATER + ST \\quad ; \\quad \\mathbf{PV_{HT}} = DS \\times K$$

## Formules Appliquées
- [[Formule Déboursé Sec (DS)]]
- [[Coefficient Multiplicateur Vente (K)]]
- [[Taux THMO Ouvrier & Charges]]

## Nœuds Liés
- [[02 - Étude de Prix & 28 SDP]]
- [[AGENT_BUDGET (Prix & 28 SDP)]]
- [[Phase 2 : Préparation 30j & DICT]]
"""
        },
        {
            "id": "phase_2",
            "label": "Phase 2 : Préparation 30j & DICT",
            "group": "Phases A-Z",
            "val": 20,
            "color": "#38bdf8",
            "tags": ["#phase", "#preparation", "#dict", "#securite"],
            "summary": "Période réglementaire obligatoire de 30 jours : envoi DICT (Cerfa 14023*01), PPSPS, PAQ et arrêtés de voirie.",
            "content": """---
title: Phase 2 : Préparation 30j & DICT
tags: [#phase, #preparation, #dict, #securite]
group: Phases A-Z
date: 2026-09-09
---

# Phase 2 : Période de Préparation de Chantier (30 Jours)

Phase obligatoire selon le CCAG Travaux pour sécuriser l'intervention :
- Déclaration DICT dématérialisée obligatoire sous 15 jours : [[Décret Anti-Endommagement (Cerfa 14023*01)]].
- Marquage-piquetage contradictoire Classe A/B/C : [[Norme NF P 98-332 (Croisements Réseaux)]].
- Vérification des compétences : [[Habilitation AIPR Encadrant / Concepteur]].

## Nœuds Liés
- [[04 - Sécurité DICT, AIPR & Anti-Endommagement]]
- [[AGENT_DICT_SAFETY (Sécurité & AIPR)]]
- [[Phase 3 : Exécution & Pilotage Terrain]]
"""
        },
        {
            "id": "phase_3",
            "label": "Phase 3 : Exécution & Pilotage Terrain",
            "group": "Phases A-Z",
            "val": 22,
            "color": "#38bdf8",
            "tags": ["#phase", "#execution", "#terrassement", "#enrobes"],
            "summary": "Réalisation terrain : terrassement, pose canalisations, réglage GNT, compactage EV2 et répandage enrobés sous télémétrie.",
            "content": """---
title: Phase 3 : Exécution & Pilotage Terrain
tags: [#phase, #execution, #terrassement, #enrobes]
group: Phases A-Z
date: 2026-09-09
---

# Phase 3 : Exécution des Travaux & Pilotage Technique

Phase active de réalisation in-situ des ouvrages de génie civil et VRD :
- Contrôle de compactage plateforme : [[Portance Dynaplaque Westergaard EV2]] ($EV_2 \\ge 50\\text{ MPa}$).
- Pose de canalisations avec respect des pentes : [[Hydraulique Manning-Strickler]].
- Surveillance thermique de l'enrobé : [[Thermométrie & Compactage BBSG]] ($135^\\circ\\text{C} - 165^\\circ\\text{C}$).
- Traçabilité des évacuations de terres : [[Loi AGEC & Trackdéchets (BSDD)]].

## Nœuds Liés
- [[03 - Technique VRD, Enrobés & Hydraulique]]
- [[05 - Pilotage In-Situ, Litiges & Aléas]]
- [[AGENT_TELEMETRY (Vision & Capteurs)]]
- [[Phase 4 : Pointage & Révision TP08]]
"""
        },
        {
            "id": "phase_4",
            "label": "Phase 4 : Pointage & Révision TP08",
            "group": "Phases A-Z",
            "val": 18,
            "color": "#38bdf8",
            "tags": ["#phase", "#facturation", "#tp08", "#situations"],
            "summary": "Attachements contradictoires mensuels, situations de travaux avec application de l'indexation paramétrique TP08.",
            "content": """---
title: Phase 4 : Pointage & Révision TP08
tags: [#phase, #facturation, #tp08, #situations]
group: Phases A-Z
date: 2026-09-09
---

# Phase 4 : Suivi Budgétaire, Situations & Révision des Prix

Calcul des acomptes mensuels et maîtrise des dérives de coûts :
$$\\mathbf{P_n} = P_0 \\cdot \\left[ 0{,}15 + 0{,}85 \\cdot \\frac{\\text{TP08}_n}{\\text{TP08}_0} \\right]$$

## Nœuds Liés
- [[Formule Révision Paramétrique TP08]]
- [[AGENT_BUDGET (Prix & 28 SDP)]]
- [[Phase 5 : Réception & Levée Réserves]]
"""
        },
        {
            "id": "phase_5",
            "label": "Phase 5 : Réception & Levée Réserves",
            "group": "Phases A-Z",
            "val": 18,
            "color": "#38bdf8",
            "tags": ["#phase", "#reception", "#opr", "#garanties"],
            "summary": "Opérations Préalables à la Réception (OPR), procès-verbal, délai de reprise 30j et départ des garanties légales.",
            "content": """---
title: Phase 5 : Réception & Levée Réserves
tags: [#phase, #reception, #opr, #garanties]
group: Phases A-Z
date: 2026-09-09
---

# Phase 5 : Réception des Travaux & Levée des Réserves

Inspection contradictoire finale marquant le transfert de garde de l'ouvrage au Maître d'Ouvrage :
- Visite préalable OPR en présence de la MOE, MOA, CSPS et Entreprise.
- Démarrage de la Garantie de Parfait Achèvement (GPA - 1 an), Biennale (2 ans) et Décennale (10 ans).

## Nœuds Liés
- [[06 - Réception, DOE SI 022 & Clôture]]
- [[Phase 6 : DOE SI 022 & DGD Final]]
"""
        },
        {
            "id": "phase_6",
            "label": "Phase 6 : DOE SI 022 & DGD Final",
            "group": "Phases A-Z",
            "val": 20,
            "color": "#38bdf8",
            "tags": ["#phase", "#doe", "#dgd", "#chorus"],
            "summary": "Remise du DOE 5 volumes (Standard SI 022), récolement géoréférencé Classe A, validation DGD et paiement solde via Chorus Pro.",
            "content": """---
title: Phase 6 : DOE SI 022 & DGD Final
tags: [#phase, #doe, #dgd, #chorus]
group: Phases A-Z
date: 2026-09-09
---

# Phase 6 : Clôture Administrative, DOE & DGD Final

Clôture complète du marché public :
- Dépôt du Dossier des Ouvrages Exécutés : [[Standard DOE SI 022 Aéroports (37p)]].
- Facturation finale dématérialisée : [[Portail Chorus Pro (DGD Solde)]].
- Libération de la caution de retenue de garantie (5%).

## Nœuds Liés
- [[06 - Réception, DOE SI 022 & Clôture]]
- [[AGENT_DOE_CLOSEOUT (Standard SI 022)]]
"""
        },

        # 3. FORMULES MATHÉMATIQUES (🟢 #10b981)
        {
            "id": "form_ds",
            "label": "Formule Déboursé Sec (DS)",
            "group": "Formules Mathématiques",
            "val": 16,
            "color": "#10b981",
            "tags": ["#formule", "#debourse", "#couts"],
            "summary": "DS = Somme(THMO x H) + Somme(Qmat x Pmat) + Somme(Conso Matériel) + Sous-traitance.",
            "content": """---
title: Formule Déboursé Sec (DS)
tags: [#formule, #debourse, #couts]
group: Formules Mathématiques
date: 2026-09-09
---

# Formule Analytique du Déboursé Sec (DS)

$$\\mathbf{DS} = \\sum (\\text{THMO} \\times \\text{Heures}) + \\sum (Q_{mat} \\times P_{mat}) + \\sum \\text{Matériel} + \\sum \\text{Sous-Traitance}$$

Le DS représente le coût strict de revient direct du chantier, sans aucune marge ni frais de siège.

## Nœuds Liés
- [[Coefficient Multiplicateur Vente (K)]]
- [[Taux THMO Ouvrier & Charges]]
- [[02 - Étude de Prix & 28 SDP]]
"""
        },
        {
            "id": "form_k",
            "label": "Coefficient Multiplicateur Vente (K)",
            "group": "Formules Mathématiques",
            "val": 16,
            "color": "#10b981",
            "tags": ["#formule", "#coefficient", "#marge"],
            "summary": "K = (1 + FG + FC) / (1 - (B + A + I)) — Facteur transformant le Déboursé Sec en Prix de Vente HT.",
            "content": """---
title: Coefficient Multiplicateur Vente (K)
tags: [#formule, #coefficient, #marge]
group: Formules Mathématiques
date: 2026-09-09
---

# Coefficient Multiplicateur de Vente (K)

$$\\mathbf{K} = \\frac{1 + FG + FC}{1 - (B + A + I)} \\quad \\Rightarrow \\quad \\mathbf{PV_{HT}} = DS \\times K$$

- $FG$ = Frais Généraux Siège ($14\\%$)
- $FC$ = Frais de Chantier directs ($9\\%$)
- $B$ = Bénéfice Net cible ($5\\%$)
- $A$ = Provision pour Aléas ($3\\%$)
- $I$ = Frais Financiers ($1\\%$)

## Nœuds Liés
- [[Formule Déboursé Sec (DS)]]
- [[Phase 1 : Étude de Prix & Déboursés]]
"""
        },
        {
            "id": "form_tp08",
            "label": "Formule Révision Paramétrique TP08",
            "group": "Formules Mathématiques",
            "val": 15,
            "color": "#10b981",
            "tags": ["#formule", "#tp08", "#indexation", "#inflation"],
            "summary": "Pn = P0 x [0.15 + 0.85 x (TP08_n / TP08_0)] — Ajuste la facturation mensuelle selon l'inflation des intrants.",
            "content": """---
title: Formule Révision Paramétrique TP08
tags: [#formule, #tp08, #indexation, #inflation]
group: Formules Mathématiques
date: 2026-09-09
---

# Formule Paramétrique de Révision des Prix (Indice TP08)

$$\\mathbf{P_n} = P_0 \\cdot \\left[ 0{,}15 + 0{,}85 \\cdot \\frac{\\text{TP08}_n}{\\text{TP08}_0} \\right]$$

- Part fixe invariable : $15\\%$
- Part paramétrique indexée sur les Travaux Publics : $85\\%$

## Nœuds Liés
- [[Phase 4 : Pointage & Révision TP08]]
- [[CCAG Travaux 2021]]
"""
        },
        {
            "id": "form_manning",
            "label": "Hydraulique Manning-Strickler",
            "group": "Formules Mathématiques",
            "val": 16,
            "color": "#10b981",
            "tags": ["#formule", "#hydraulique", "#assainissement", "#pente"],
            "summary": "Q = Ks x S x Rh^(2/3) x I^(1/2) — Débit maximal admissible d'une canalisation gravitaire.",
            "content": """---
title: Hydraulique Manning-Strickler
tags: [#formule, #hydraulique, #assainissement, #pente]
group: Formules Mathématiques
date: 2026-09-09
---

# Formule Hydraulique de Manning-Strickler

$$\\mathbf{Q} = K_s \\cdot S \\cdot R_h^{2/3} \\cdot I^{1/2}$$

- $K_s$ = Coefficient de rugosité ($90$ pour PVC CR8, $70$ pour Béton)
- $S$ = Section mouillée ($m^2$)
- $R_h$ = Rayon hydraulique ($R_h = D/4$ à section pleine)
- $I$ = Pente longitudinale ($m/m$)
- Condition d'auto-curage : $0{,}60\\text{ m/s} \\le V \\le 3{,}00\\text{ m/s}$.

## Nœuds Liés
- [[IfcPipeSegment (Réseau Assainissement EU)]]
- [[Fascicule 70 (Canalisations Assainissement)]]
"""
        },
        {
            "id": "form_ev2",
            "label": "Portance Dynaplaque Westergaard EV2",
            "group": "Formules Mathématiques",
            "val": 15,
            "color": "#10b981",
            "tags": ["#formule", "#geotechnique", "#portance", "#dynaplaque"],
            "summary": "EV2 = (1.5 x p x r) / w2 — Module de réaction sous plaque de 600mm. Exigence PF2 >= 50 MPa.",
            "content": """---
title: Portance Dynaplaque Westergaard EV2
tags: [#formule, #geotechnique, #portance, #dynaplaque]
group: Formules Mathématiques
date: 2026-09-09
---

# Portance de Plateforme & Essai Dynaplaque (EV2)

$$\\mathbf{EV_2} = \\frac{1{,}5 \\cdot p \\cdot r}{w_2} \\quad ; \\quad \\text{Critère Compactage : } \\mathbf{\\frac{EV_2}{EV_1} \\le 2{,}0}$$

- Exigence minimale plateforme routière : $EV_2 \\ge 50\\text{ MPa}$
- Piste éolienne lourde : $EV_2 \\ge 80\\text{ MPa}$

## Nœuds Liés
- [[Phase 3 : Exécution & Pilotage Terrain]]
- [[AGENT_TELEMETRY (Vision & Capteurs)]]
"""
        },
        {
            "id": "form_thmo",
            "label": "Taux THMO Ouvrier & Charges",
            "group": "Formules Mathématiques",
            "val": 14,
            "color": "#10b981",
            "tags": ["#formule", "#thmo", "#salaires", "#charges"],
            "summary": "THMO = Salaire Brut x (1 + 45% Charges) x (1 + 12% Primes) x (1 + 8% Trajet) = 34.50 €/h.",
            "content": """---
title: Taux THMO Ouvrier & Charges
tags: [#formule, #thmo, #salaires, #charges]
group: Formules Mathématiques
date: 2026-09-09
---

# Taux Horaire Moyen Ouvrier (THMO)

$$\\mathbf{THMO} = \\text{Salaire Brut} \\times 1{,}45 \\times 1{,}12 \\times 1{,}08 = \\mathbf{34{,}50\\text{ €/h}}$$

Composante fondamentale pour le calcul de la main-d'œuvre directe sur les 28 SDP.

## Nœuds Liés
- [[Formule Déboursé Sec (DS)]]
- [[02 - Étude de Prix & 28 SDP]]
"""
        },
        {
            "id": "form_bordure",
            "label": "Métré & Déboursé Bordures T2",
            "group": "Formules Mathématiques",
            "val": 13,
            "color": "#10b981",
            "tags": ["#formule", "#sdp", "#bordure"],
            "summary": "DS Bordure T2 = 18.40 €/ml (Pose 0.25 h/ml + Béton calage C20/25 + Fourniture T2 NF).",
            "content": """---
title: Métré & Déboursé Bordures T2
tags: [#formule, #sdp, #bordure]
group: Formules Mathématiques
date: 2026-09-09
---

# Sous-Détail Analytique Bordure T2 Béton

- Main d'œuvre : $0{,}25\\text{ h/ml} \\times 34{,}50\\text{ €} = 8{,}63\\text{ €}$
- Béton de calage C20/25 ($0{,}04\\text{ m}^3/\\text{ml}$) : $4{,}60\\text{ €}$
- Fourniture bordure T2 NF EN 1340 : $5{,}17\\text{ €}$
- **Déboursé Sec Total = 18.40 €/ml | Prix Vente HT = 23.55 €/ml**

## Nœuds Liés
- [[SDP 12 : Bordure Béton T2 Préfabriquée]]
- [[IfcRoad & IfcCourse (Chaussée BB/GNT)]]
"""
        },
        {
            "id": "form_enrobe",
            "label": "Thermométrie & Compactage BBSG",
            "group": "Formules Mathématiques",
            "val": 14,
            "color": "#10b981",
            "tags": ["#formule", "#enrobe", "#temperature"],
            "summary": "Surveillance thermique continue LiDAR FLIR (135°C à 165°C) selon la norme NF EN 12697.",
            "content": """---
title: Thermométrie & Compactage BBSG
tags: [#formule, #enrobe, #temperature]
group: Formules Mathématiques
date: 2026-09-09
---

# Contrôle Thermique & Formulation Enrobés BB 0/10

$$\\text{Plage de Répandage Conforme : } \\mathbf{135^\\circ\\text{C} \\le T_{pose} \\le 165^\\circ\\text{C}}$$

Tout enrobé appliqué en dessous de $130^\\circ\\text{C}$ subit un compactage défaillant entraînant une perte d'imperméabilité et un risque d'orniérage précoce.

## Nœuds Liés
- [[SDP 18 : Enrobé Bitumineux BB 0/10]]
- [[AGENT_TELEMETRY (Vision & Capteurs)]]
"""
        },

        # 4. CADRE RÉGLEMENTAIRE & NORMES (🟠 #f59e0b)
        {
            "id": "norme_ccag",
            "label": "CCAG Travaux 2021",
            "group": "Réglementation & Normes",
            "val": 17,
            "color": "#f59e0b",
            "tags": ["#norme", "#ccag", "#juridique"],
            "summary": "Cahier des Clauses Administratives Générales applicables aux marchés publics de travaux.",
            "content": """---
title: CCAG Travaux 2021
tags: [#norme, #ccag, #juridique]
group: Réglementation & Normes
date: 2026-09-09
---

# CCAG Travaux 2021

Texte de référence régissant l'exécution financière et contractuelle des marchés :
- Clause d'insertion sociale et environnementale obligatoire.
- Délais stricts de réclamation (30 jours sous peine de forclusion).
- Procédure d'établissement du Décompte Général et Définitif (DGD).

## Nœuds Liés
- [[01 - Analyse Marchés DCE & CCAG 2021]]
- [[Phase 0 : Consultation & DCE]]
- [[Phase 6 : DOE SI 022 & DGD Final]]
"""
        },
        {
            "id": "norme_dict",
            "label": "Décret Anti-Endommagement (Cerfa 14023*01)",
            "group": "Réglementation & Normes",
            "val": 17,
            "color": "#f59e0b",
            "tags": ["#norme", "#dict", "#securite"],
            "summary": "Cadre légal imposant la Déclaration d'Intention de Commencement de Travaux auprès du Guichet Unique.",
            "content": """---
title: Décret Anti-Endommagement (Cerfa 14023*01)
tags: [#norme, #dict, #securite]
group: Réglementation & Normes
date: 2026-09-09
---

# Décret Anti-Endommagement & Cerfa 14023*01

Obligation de consulter les exploitants de réseaux avant tout coup de godet :
- Réponse dématérialisée obligatoire sous **9 jours ouvrés**.
- Cartographie des réseaux en Classe A ($XYZ \\le 5\\text{ cm}$ rigide, $10\\text{ cm}$ souple), Classe B ($40\\text{ cm}$) ou Classe C ($> 40\\text{ cm}$).

## Nœuds Liés
- [[04 - Sécurité DICT, AIPR & Anti-Endommagement]]
- [[Phase 2 : Préparation 30j & DICT]]
- [[Norme NF P 98-332 (Croisements Réseaux)]]
"""
        },
        {
            "id": "norme_aipr",
            "label": "Habilitation AIPR Encadrant / Concepteur",
            "group": "Réglementation & Normes",
            "val": 15,
            "color": "#f59e0b",
            "tags": ["#norme", "#aipr", "#securite"],
            "summary": "Autorisation d'Intervention à Proximité des Réseaux obligatoire pour conducteurs, chefs et opérateurs.",
            "content": """---
title: Habilitation AIPR Encadrant / Concepteur
tags: [#norme, #aipr, #securite]
group: Réglementation & Normes
date: 2026-09-09
---

# Habilitation AIPR (Autorisation d'Intervention à Proximité des Réseaux)

Obligation réglementaire issue du décret du 5 octobre 2011 :
- Au moins 1 encadrant sur le chantier doit être titulaire de l'AIPR Encadrant.
- Tous les conducteurs d'engins doivent détenir l'AIPR Opérateur.

## Nœuds Liés
- [[04 - Sécurité DICT, AIPR & Anti-Endommagement]]
- [[AGENT_DICT_SAFETY (Sécurité & AIPR)]]
"""
        },
        {
            "id": "norme_nfp98332",
            "label": "Norme NF P 98-332 (Croisements Réseaux)",
            "group": "Réglementation & Normes",
            "val": 16,
            "color": "#f59e0b",
            "tags": ["#norme", "#nfp98332", "#croisements", "#clash"],
            "summary": "Distances minimales entre réseaux souterrains : Delta Z >= 0.20m au croisement et Delta X >= 0.50m en parallèle.",
            "content": """---
title: Norme NF P 98-332 (Croisements Réseaux)
tags: [#norme, #nfp98332, #croisements, #clash]
group: Réglementation & Normes
date: 2026-09-09
---

# Norme NF P 98-332 : Règles d'Implantation Souterraine

$$\\text{Règle de Sécurité Anti-Clash : } \\mathbf{\\Delta z \\ge 0{,}20\\text{ m (20 cm)}} \\quad \\text{et} \\quad \\mathbf{\\Delta x \\ge 0{,}50\\text{ m (50 cm)}}$$

- Réseau Eau Potable (AEP) : Toujours situé **au-dessus** des réseaux d'assainissement gravitaire.
- Si croisement sous assainissement : Fourreau acier de protection étanche obligatoire.

## Nœuds Liés
- [[08 - OpenBIM IFC 4.3 & Jumeau Numérique]]
- [[AGENT_BIM_3D (IFC 4.3 & Clashs)]]
"""
        },
        {
            "id": "norme_fascicule70",
            "label": "Fascicule 70 (Canalisations Assainissement)",
            "group": "Réglementation & Normes",
            "val": 15,
            "color": "#f59e0b",
            "tags": ["#norme", "#fascicule70", "#assainissement"],
            "summary": "Cahier des charges type pour les ouvrages d'assainissement et réseaux d'eaux pluviales.",
            "content": """---
title: Fascicule 70 (Canalisations Assainissement)
tags: [#norme, #fascicule70, #assainissement]
group: Réglementation & Normes
date: 2026-09-09
---

# Fascicule 70 du CCTG : Ouvrages d'Assainissement

Prescriptions d'exécution :
- Épaisseur du lit de pose en sable ou gravillon : $10\\text{ cm}$ minimum sous la génératrice inférieure.
- Remblaiement latéral et supérieur en couches compactées de $20\\text{ cm}$.
- Essais d'étanchéité et inspection télévisée ITV (NF EN 13508-2) obligatoires avant réception.

## Nœuds Liés
- [[Hydraulique Manning-Strickler]]
- [[IfcPipeSegment (Réseau Assainissement EU)]]
"""
        },
        {
            "id": "norme_trackdechets",
            "label": "Loi AGEC & Trackdéchets (BSDD)",
            "group": "Réglementation & Normes",
            "val": 15,
            "color": "#f59e0b",
            "tags": ["#norme", "#trackdechets", "#agec", "#environnement"],
            "summary": "Traçabilité dématérialisée obligatoire de tous les déblais et déchets de chantier sur la plateforme d'État.",
            "content": """---
title: Loi AGEC & Trackdéchets (BSDD)
tags: [#norme, #trackdechets, #agec, #environnement]
group: Réglementation & Normes
date: 2026-09-09
---

# Loi AGEC & Plateforme Trackdéchets

Obligation légale de traçabilité des terres excavées et déchets de chantier :
- Bordereau de Suivi de Déchets Dématérialisé (BSDD).
- Inscription au Registre National des Terres Excavées et Sédiments (RNDTS).
- Code Déchet Inerte : `17 05 04` (Terres et cailloux non pollués).

## Nœuds Liés
- [[Phase 3 : Exécution & Pilotage Terrain]]
- [[AGENT_PROCUREMENT (Fournisseurs & BSDD)]]
"""
        },
        {
            "id": "norme_si022",
            "label": "Standard DOE SI 022 Aéroports (37p)",
            "group": "Réglementation & Normes",
            "val": 18,
            "color": "#f59e0b",
            "tags": ["#norme", "#si022", "#doe", "#qualite"],
            "summary": "Standard d'excellence industrielle en 5 volumes pour la constitution du Dossier des Ouvrages Exécutés.",
            "content": """---
title: Standard DOE SI 022 Aéroports (37p)
tags: [#norme, #si022, #doe", "#qualite]
group: Réglementation & Normes
date: 2026-09-09
---

# Standard Interne DOE SI 022 (Aéroports de Lyon - 37 Pages)

Architecture de référence du DOE en 5 Volumes :
- Volume 1 : Pièces administratives & PV de réception
- Volume 2 : Plans As-Built & Récolement RGF93 Classe A
- Volume 3 : Fiches techniques matériaux & FDES
- Volume 4 : Essais de compactage & Rapports ITV
- Volume 5 : Notices de maintenance & DIUO

## Nœuds Liés
- [[06 - Réception, DOE SI 022 & Clôture]]
- [[Phase 6 : DOE SI 022 & DGD Final]]
- [[AGENT_DOE_CLOSEOUT (Standard SI 022)]]
"""
        },
        {
            "id": "norme_chorus",
            "label": "Portail Chorus Pro (DGD Solde)",
            "group": "Réglementation & Normes",
            "val": 14,
            "color": "#f59e0b",
            "tags": ["#norme", "#chorus", "#dgd", "#facturation"],
            "summary": "Plateforme publique obligatoire de facturation électronique et notification du Décompte Général Définitif.",
            "content": """---
title: Portail Chorus Pro (DGD Solde)
tags: [#norme, #chorus, #dgd, #facturation]
group: Réglementation & Normes
date: 2026-09-09
---

# Portail Chorus Pro & DGD Dématérialisé

Obligation légale pour tous les marchés publics :
- Dépôt du Projet de Décompte Final (PDF) sous 30 jours après réception.
- Notification du DGD par la Maîtrise d'Œuvre sous 30 jours.
- Règlement du solde dans le délai global de paiement de 30 jours.

## Nœuds Liés
- [[Phase 6 : DOE SI 022 & DGD Final]]
"""
        },
        {
            "id": "norme_pgc",
            "label": "Plan Général de Coordination (PGC SPS)",
            "group": "Réglementation & Normes",
            "val": 13,
            "color": "#f59e0b",
            "tags": ["#norme", "#pgc", "#sps", "#securite"],
            "summary": "Document de sécurité rédigé par le coordonnateur SPS définissant la coactivité et les voies d'accès.",
            "content": """---
title: Plan Général de Coordination (PGC SPS)
tags: [#norme, #pgc, #sps, #securite]
group: Réglementation & Normes
date: 2026-09-09
---

# Plan Général de Coordination SPS (PGC)

Document contractuel de niveau 1, 2 ou 3 imposant les mesures de sécurité collective et l'organisation des secours sur le site.

## Nœuds Liés
- [[Phase 0 : Consultation & DCE]]
- [[Phase 2 : Préparation 30j & DICT]]
"""
        },

        # 5. CHANTIERS RÉELS (🔴 #f43f5e)
        {
            "id": "chantier_barbazan",
            "label": "Giratoire Barbazan (152 795 € HT)",
            "group": "Chantiers Réels",
            "val": 22,
            "color": "#f43f5e",
            "tags": ["#chantier", "#barbazan", "#giratoire", "#vrd"],
            "summary": "Requalification de carrefour giratoire : terrassement, GNT, bordures T2, BB 0/10 et assainissement.",
            "content": """---
title: Giratoire Barbazan (152 795 € HT)
tags: [#chantier, #barbazan, #giratoire, #vrd]
group: Chantiers Réels
date: 2026-09-09
---

# Chantier Réel : Aménagement du Giratoire de Barbazan

- **Montant HT :** 152 795.00 €
- **Durée :** 7 semaines
- **Prestations :** 1 450 T d'enrobé BB 0/10, 650 ml de bordures T2, réseau EU PVC Ø200 (120 ml).
- **Particularité :** Découverte in-situ d'un réseau gaz MPB PEHD non répertorié -> arrêt temporaire et dévoiement validé par FNC.

## Nœuds Liés
- [[00 - Synthèse Globale & État de l'Art 2026]]
- [[IfcProject (ZAC Barbazan VRD)]]
- [[SDP 12 : Bordure Béton T2 Préfabriquée]]
- [[SDP 18 : Enrobé Bitumineux BB 0/10]]
"""
        },
        {
            "id": "chantier_stnicolas",
            "label": "Piste Éolienne Saint-Nicolas (46 800 € HT)",
            "group": "Chantiers Réels",
            "val": 18,
            "color": "#f43f5e",
            "tags": ["#chantier", "#stnicolas", "#eoliens", "#piste"],
            "summary": "Piste lourde pour convoi éolien 120T : forte déclivité, renforcement géogrille et GNT 0/31.5.",
            "content": """---
title: Piste Éolienne Saint-Nicolas (46 800 € HT)
tags: [#chantier, #stnicolas, #eoliens, #piste]
group: Chantiers Réels
date: 2026-09-09
---

# Chantier Réel : Desserte Éolienne de Saint-Nicolas-des-Biefs

- **Montant HT :** 46 800.00 €
- **Prestations :** Terrassement rocheux, pose de géogrille haute résistance, couche de roulement GNT.
- **Contrôle Qualité :** Essai Dynaplaque $EV_2 = 62{,}1\\text{ MPa}$ validant le passage des convois exceptionnels.

## Nœuds Liés
- [[Portance Dynaplaque Westergaard EV2]]
- [[SDP 05 : Couche Fondation GNT 0/31.5]]
"""
        },
        {
            "id": "chantier_aurouer",
            "label": "Traverse Aurouer (187 400 € HT)",
            "group": "Chantiers Réels",
            "val": 18,
            "color": "#f43f5e",
            "tags": ["#chantier", "#aurouer", "#traverse", "#voirie"],
            "summary": "Aménagement de traverse d'agglomération sous circulation alternée KR11, rabotage et bordures.",
            "content": """---
title: Traverse Aurouer (187 400 € HT)
tags: [#chantier, #aurouer, #traverse, #voirie]
group: Chantiers Réels
date: 2026-09-09
---

# Chantier Réel : Traverse d'Agglomération d'Aurouer

- **Montant HT :** 187 400.00 €
- **Gestion Sécurité :** Balisage lourd par feux tricolores KR11 et arrêté de circulation départemental.

## Nœuds Liés
- [[Phase 2 : Préparation 30j & DICT]]
- [[04 - Sécurité DICT, AIPR & Anti-Endommagement]]
"""
        },

        # 6. ESSAIM D'AGENTS AUTONOMES (🟡 #ec4899)
        {
            "id": "agent_legal",
            "label": "AGENT_LEGAL (Marchés & DCE)",
            "group": "Essaim Agents IA",
            "val": 16,
            "color": "#ec4899",
            "tags": ["#agent", "#legal", "#marche"],
            "summary": "Audit automatique des pièces de marchés, conformité CCAG 2021 et rédaction des mémoires de réclamation.",
            "content": """---
title: AGENT_LEGAL (Marchés & DCE)
tags: [#agent, #legal, #marche]
group: Essaim Agents IA
date: 2026-09-09
---

# Agent Spécialisé : Marchés Publics & DCE (AGENT_LEGAL)

Rôle : Supervision juridique continue, détection des clauses abusives et rédaction des correspondances contractuelles.

## Nœuds Liés
- [[CCAG Travaux 2021]]
- [[01 - Analyse Marchés DCE & CCAG 2021]]
"""
        },
        {
            "id": "agent_budget",
            "label": "AGENT_BUDGET (Prix & 28 SDP)",
            "group": "Essaim Agents IA",
            "val": 18,
            "color": "#ec4899",
            "tags": ["#agent", "#budget", "#prix", "#sdp"],
            "summary": "Moteur analytique de chiffrage, actualisation des 28 SDP et application des indexations TP08.",
            "content": """---
title: AGENT_BUDGET (Prix & 28 SDP)
tags: [#agent, #budget, #prix, #sdp]
group: Essaim Agents IA
date: 2026-09-09
---

# Agent Spécialisé : Prix & Déboursés (AGENT_BUDGET)

Rôle : Calcul instantané des Déboursés Secs, marge brute et génération des situations de travaux.

## Nœuds Liés
- [[Formule Déboursé Sec (DS)]]
- [[Coefficient Multiplicateur Vente (K)]]
- [[02 - Étude de Prix & 28 SDP]]
"""
        },
        {
            "id": "agent_bim",
            "label": "AGENT_BIM_3D (IFC 4.3 & Clashs)",
            "group": "Essaim Agents IA",
            "val": 18,
            "color": "#ec4899",
            "tags": ["#agent", "#bim", "#ifc43", "#clash"],
            "summary": "Génération de maquettes OpenBIM IFC 4.3, LandXML et détection temps réel des clashs selon NF P 98-332.",
            "content": """---
title: AGENT_BIM_3D (IFC 4.3 & Clashs)
tags: [#agent, #bim, #ifc43, #clash]
group: Essaim Agents IA
date: 2026-09-09
---

# Agent Spécialisé : BIM & Maquette 3D (AGENT_BIM_3D)

Rôle : Modélisation des tranchées VRD, calcul hydraulique Manning-Strickler et détection des conflits géométriques.

## Nœuds Liés
- [[08 - OpenBIM IFC 4.3 & Jumeau Numérique]]
- [[Norme NF P 98-332 (Croisements Réseaux)]]
- [[IfcProject (ZAC Barbazan VRD)]]
"""
        },
        {
            "id": "agent_dict",
            "label": "AGENT_DICT_SAFETY (Sécurité & AIPR)",
            "group": "Essaim Agents IA",
            "val": 16,
            "color": "#ec4899",
            "tags": ["#agent", "#securite", "#dict", "#aipr"],
            "summary": "Vérification des 9 récépissés de DICT, marquage-piquetage et gestion des habilitations de personnel.",
            "content": """---
title: AGENT_DICT_SAFETY (Sécurité & AIPR)
tags: [#agent, #securite, #dict, #aipr]
group: Essaim Agents IA
date: 2026-09-09
---

# Agent Spécialisé : Sécurité & DICT (AGENT_DICT_SAFETY)

Rôle : Garantie zéro accident réseau et vérification des attestations AIPR in-situ.

## Nœuds Liés
- [[Décret Anti-Endommagement (Cerfa 14023*01)]]
- [[04 - Sécurité DICT, AIPR & Anti-Endommagement]]
"""
        },
        {
            "id": "agent_telemetry",
            "label": "AGENT_TELEMETRY (Vision & Capteurs)",
            "group": "Essaim Agents IA",
            "val": 16,
            "color": "#ec4899",
            "tags": ["#agent", "#telemetrie", "#thermique", "#dynaplaque"],
            "summary": "Ingestion des flux de caméras thermiques enrobé (FLIR) et essais de portance Dynaplaque EV2.",
            "content": """---
title: AGENT_TELEMETRY (Vision & Capteurs)
tags: [#agent, #telemetrie, #thermique, #dynaplaque]
group: Essaim Agents IA
date: 2026-09-09
---

# Agent Spécialisé : Vision & Capteurs (AGENT_TELEMETRY)

Rôle : Surveillance continue de la qualité physique des matériaux mis en œuvre sur la plateforme.

## Nœuds Liés
- [[Portance Dynaplaque Westergaard EV2]]
- [[Thermométrie & Compactage BBSG]]
"""
        },
        {
            "id": "agent_procurement",
            "label": "AGENT_PROCUREMENT (Fournisseurs & BSDD)",
            "group": "Essaim Agents IA",
            "val": 15,
            "color": "#ec4899",
            "tags": ["#agent", "#fournisseurs", "#logistique", "#trackdechets"],
            "summary": "Ordonnancement des livraisons de carrières, centrales d'enrobage et scellement des BSDD Trackdéchets.",
            "content": """---
title: AGENT_PROCUREMENT (Fournisseurs & BSDD)
tags: [#agent, #fournisseurs, #logistique, #trackdechets]
group: Essaim Agents IA
date: 2026-09-09
---

# Agent Spécialisé : Fournisseurs & Traçabilité (AGENT_PROCUREMENT)

Rôle : Logistique en flux tendu et traçabilité zéro infraction des déchets de terrassement.

## Nœuds Liés
- [[Loi AGEC & Trackdéchets (BSDD)]]
"""
        },
        {
            "id": "agent_planning",
            "label": "AGENT_PLANNING_LEAN (Last Planner 4D)",
            "group": "Essaim Agents IA",
            "val": 15,
            "color": "#ec4899",
            "tags": ["#agent", "#planning", "#lean", "#gantt"],
            "summary": "Méthode Last Planner System (LPS), calcul du Pourcentage de Tâches Complétées (PPC) et phasage 4D.",
            "content": """---
title: AGENT_PLANNING_LEAN (Last Planner 4D)
tags: [#agent, #planning, #lean, #gantt]
group: Essaim Agents IA
date: 2026-09-09
---

# Agent Spécialisé : Ordonnancement Lean (AGENT_PLANNING_LEAN)

Rôle : Pilotage hebdomadaire des contraintes et synchronisation des équipes d'application d'enrobé et pose bordures.

## Nœuds Liés
- [[Phase 3 : Exécution & Pilotage Terrain]]
"""
        },
        {
            "id": "agent_closeout",
            "label": "AGENT_DOE_CLOSEOUT (Standard SI 022)",
            "group": "Essaim Agents IA",
            "val": 16,
            "color": "#ec4899",
            "tags": ["#agent", "#doe", "#cloture", "#si022"],
            "summary": "Compilation continue des 5 volumes du DOE et télétransmission du DGD sur Chorus Pro.",
            "content": """---
title: AGENT_DOE_CLOSEOUT (Standard SI 022)
tags: [#agent, #doe, #cloture, #si022]
group: Essaim Agents IA
date: 2026-09-09
---

# Agent Spécialisé : DOE & Clôture (AGENT_DOE_CLOSEOUT)

Rôle : Automatisation de la constitution du Dossier des Ouvrages Exécutés et libération de la caution 5%.

## Nœuds Liés
- [[Standard DOE SI 022 Aéroports (37p)]]
- [[Phase 6 : DOE SI 022 & DGD Final]]
"""
        },

        # 7. BIM & OPENBIM IFC 4.3 (🩵 #06b6d4)
        {
            "id": "bim_ifcproject",
            "label": "IfcProject (ZAC Barbazan VRD)",
            "group": "OpenBIM & IFC 4.3",
            "val": 18,
            "color": "#06b6d4",
            "tags": ["#bim", "#ifcproject", "#openbim"],
            "summary": "Racine du conteneur IFC 4.3 géoréférencée en RGF93 / CC43 / NGF-IGN69.",
            "content": """---
title: IfcProject (ZAC Barbazan VRD)
tags: [#bim, #ifcproject, #openbim]
group: OpenBIM & IFC 4.3
date: 2026-09-09
---

# IfcProject : Modèle Racine BIM VRD

Entité de tête ISO 16739 contenant l'ensemble de la hiérarchie spatiale et technique du projet :
`IfcProject` -> `IfcSite` -> `IfcRoad` & `IfcDistributionSystem`.

## Nœuds Liés
- [[08 - OpenBIM IFC 4.3 & Jumeau Numérique]]
- [[IfcRoad & IfcCourse (Chaussée BB/GNT)]]
- [[IfcPipeSegment (Réseau Assainissement EU)]]
"""
        },
        {
            "id": "bim_ifcroad",
            "label": "IfcRoad & IfcCourse (Chaussée BB/GNT)",
            "group": "OpenBIM & IFC 4.3",
            "val": 16,
            "color": "#06b6d4",
            "tags": ["#bim", "#ifcroad", "#voirie"],
            "summary": "Modélisation des couches de voirie BB 0/10 (5cm), GB 0/14 (10cm), GNT 0/31.5 (25cm) et bordures T2.",
            "content": """---
title: IfcRoad & IfcCourse (Chaussée BB/GNT)
tags: [#bim, #ifcroad, #voirie]
group: OpenBIM & IFC 4.3
date: 2026-09-09
---

# IfcRoad & IfcCourse : Superstructure Routière

Modélisation solide 3D des couches d'enrobé et de fondation avec extraction automatique des cubatures.

## Nœuds Liés
- [[IfcProject (ZAC Barbazan VRD)]]
- [[SDP 18 : Enrobé Bitumineux BB 0/10]]
"""
        },
        {
            "id": "bim_ifcpipe_eu",
            "label": "IfcPipeSegment (Réseau Assainissement EU)",
            "group": "OpenBIM & IFC 4.3",
            "val": 17,
            "color": "#06b6d4",
            "tags": ["#bim", "#ifcpipe", "#assainissement", "#pente"],
            "summary": "Canalisation PVC CR8 DN200 (120ml) avec pente 1.20% et cotes fil d'eau amont/aval.",
            "content": """---
title: IfcPipeSegment (Réseau Assainissement EU)
tags: [#bim, #ifcpipe, #assainissement, #pente]
group: OpenBIM & IFC 4.3
date: 2026-09-09
---

# IfcPipeSegment : Réseau Gravitaire EU

Tronçon linéaire modélisé avec ses attributs hydrauliques :
- $DN = 200\\text{ mm}$
- Pente $I = 1{,}20\\%$
- $FE_{amont} = 142{,}50\\text{ m NGF}$ | $FE_{aval} = 141{,}06\\text{ m NGF}$

## Nœuds Liés
- [[Hydraulique Manning-Strickler]]
- [[IfcDistributionChamber (Regards Béton)]]
"""
        },
        {
            "id": "bim_ifcchamber",
            "label": "IfcDistributionChamber (Regards Béton)",
            "group": "OpenBIM & IFC 4.3",
            "val": 14,
            "color": "#06b6d4",
            "tags": ["#bim", "#regard", "#manhole"],
            "summary": "Regards de visite béton armé DN1000 avec cheminées et tampons fonte C250.",
            "content": """---
title: IfcDistributionChamber (Regards Béton)
tags: [#bim, #regard, #manhole]
group: OpenBIM & IFC 4.3
date: 2026-09-09
---

# IfcDistributionChamberElement : Regards de Visite

Regards R1 (Amont) et R2 (Aval) permettant le curage et l'inspection ITV des réseaux gravitaires.

## Nœuds Liés
- [[IfcPipeSegment (Réseau Assainissement EU)]]
"""
        },
        {
            "id": "bim_ifcpipe_aep",
            "label": "IfcPipeSegment (Conduite Eau Potable AEP)",
            "group": "OpenBIM & IFC 4.3",
            "val": 15,
            "color": "#06b6d4",
            "tags": ["#bim", "#aep", "#clash"],
            "summary": "Conduite Fonte DN100 traversante — élément de contrôle anti-clash NF P 98-332.",
            "content": """---
title: IfcPipeSegment (Conduite Eau Potable AEP)
tags: [#bim, #aep, #clash]
group: OpenBIM & IFC 4.3
date: 2026-09-09
---

# IfcPipeSegment : Réseau AEP & Détection de Conflits

Conduite sous pression croisant la voirie à $X = 45{,}0\\text{ m}$. L'écart avec le réseau EU est surveillé en temps réel.

## Nœuds Liés
- [[Norme NF P 98-332 (Croisements Réseaux)]]
- [[IfcPipeSegment (Réseau Assainissement EU)]]
"""
        },
        {
            "id": "bim_landxml",
            "label": "LandXML 1.2 (Guidage GPS Engins 3D)",
            "group": "OpenBIM & IFC 4.3",
            "val": 15,
            "color": "#06b6d4",
            "tags": ["#bim", "#landxml", "#gps", "#guidage"],
            "summary": "Modèle TIN de plateforme et axe 3D exporté pour les pelles et niveleuses Leica/Trimble 3D.",
            "content": """---
title: LandXML 1.2 (Guidage GPS Engins 3D)
tags: [#bim, #landxml, #gps, #guidage]
group: OpenBIM & IFC 4.3
date: 2026-09-09
---

# Format LandXML 1.2 & Guidage GNSS 3D

Permet le contrôle automatique de la cote de fond de forme à $\\pm 1{,}5\\text{ cm}$ sans piquetage intermédiaire.

## Nœuds Liés
- [[Phase 3 : Exécution & Pilotage Terrain]]
"""
        },
        {
            "id": "bim_bcf",
            "label": "BCF 2.1 (Coordination & Rapports Clashs)",
            "group": "OpenBIM & IFC 4.3",
            "val": 14,
            "color": "#06b6d4",
            "tags": ["#bim", "#bcf", "#clash", "#coordination"],
            "summary": "BIM Collaboration Format pour l'échange de tickets de conflits géométriques avec la MOE.",
            "content": """---
title: BCF 2.1 (Coordination & Rapports Clashs)
tags: [#bim, #bcf, #clash, #coordination]
group: OpenBIM & IFC 4.3
date: 2026-09-09
---

# Format BCF 2.1 (BIM Collaboration Format)

Standard d'échange des requêtes de modifications et alertes de clashs géométriques entre intervenants du chantier.

## Nœuds Liés
- [[Norme NF P 98-332 (Croisements Réseaux)]]
- [[AGENT_BIM_3D (IFC 4.3 & Clashs)]]
"""
        },

        # 8. SOUS-DÉTAILS DE PRIX (SDP) & MATÉRIAUX (⚪ #64748b)
        {
            "id": "sdp_terrassement",
            "label": "SDP 01 : Déblai & Terrassement Tranchée",
            "group": "Sous-Détails & Matériaux",
            "val": 13,
            "color": "#64748b",
            "tags": ["#sdp", "#terrassement", "#pelle"],
            "summary": "Pelle mécanique 21T (Rdt 35 m3/h) + Chef de file — DS = 8.50 €/m3, PV = 10.88 €/m3.",
            "content": """---
title: SDP 01 : Déblai & Terrassement Tranchée
tags: [#sdp, #terrassement, #pelle]
group: Sous-Détails & Matériaux
date: 2026-09-09
---

# SDP 01 : Terrassement de Tranchée en Terrain Ordinaire

- Main d'œuvre : $0{,}08\\text{ h/m}^3 \\times 34{,}50\\text{ €} = 2{,}76\\text{ €}$
- Pelle chenille 21T + carburant : $5{,}74\\text{ €/m}^3$
- **DS = 8.50 €/m³ | PV HT = 10.88 €/m³**

## Nœuds Liés
- [[02 - Étude de Prix & 28 SDP]]
- [[Formule Déboursé Sec (DS)]]
"""
        },
        {
            "id": "sdp_gnt",
            "label": "SDP 05 : Couche Fondation GNT 0/31.5",
            "group": "Sous-Détails & Matériaux",
            "val": 14,
            "color": "#64748b",
            "tags": ["#sdp", "#gnt", "#fondation"],
            "summary": "GNT 0/31.5 reconstituée compactée — DS = 22.40 €/T, PV = 28.67 €/T.",
            "content": """---
title: SDP 05 : Couche Fondation GNT 0/31.5
tags: [#sdp, #gnt, #fondation]
group: Sous-Détails & Matériaux
date: 2026-09-09
---

# SDP 05 : Grave Non Traitée GNT 0/31.5

- Fourniture carrière : $14{,}50\\text{ €/T}$
- Transport semi-remorque ($20\\text{ km}$) : $4{,}20\\text{ €/T}$
- Régalage niveleuse + compacteur V3 : $3{,}70\\text{ €/T}$
- **DS = 22.40 €/T | PV HT = 28.67 €/T**

## Nœuds Liés
- [[Portance Dynaplaque Westergaard EV2]]
- [[Fourniture GNT Carrières de la Montagne]]
"""
        },
        {
            "id": "sdp_bordure_t2",
            "label": "SDP 12 : Bordure Béton T2 Préfabriquée",
            "group": "Sous-Détails & Matériaux",
            "val": 15,
            "color": "#64748b",
            "tags": ["#sdp", "#bordure", "#t2"],
            "summary": "Bordure T2 NF EN 1340 sur lit de béton C20/25 — DS = 18.40 €/ml, PV = 23.55 €/ml.",
            "content": """---
title: SDP 12 : Bordure Béton T2 Préfabriquée
tags: [#sdp, #bordure, #t2]
group: Sous-Détails & Matériaux
date: 2026-09-09
---

# SDP 12 : Bordure T2 Béton Préfabriquée

- **DS = 18.40 €/ml | PV HT = 23.55 €/ml** (Marge $21{,}9\\%$)

## Nœuds Liés
- [[Métré & Déboursé Bordures T2]]
- [[Préfabriqués Bétons & Bordures FR]]
"""
        },
        {
            "id": "sdp_enrobe_bb",
            "label": "SDP 18 : Enrobé Bitumineux BB 0/10",
            "group": "Sous-Détails & Matériaux",
            "val": 16,
            "color": "#64748b",
            "tags": ["#sdp", "#enrobe", "#bb010"],
            "summary": "BBSG 0/10 classe 3 appliqué au finisseur — DS = 84.50 €/T, PV = 108.16 €/T.",
            "content": """---
title: SDP 18 : Enrobé Bitumineux BB 0/10
tags: [#sdp, #enrobe, #bb010]
group: Sous-Détails & Matériaux
date: 2026-09-09
---

# SDP 18 : Béton Bitumineux Semi-Grenu BB 0/10

- Fourniture centrale d'enrobage : $62{,}00\\text{ €/T}$
- Transport camion calorifugé : $8{,}50\\text{ €/T}$
- Atelier de répandage (Finisseur + Cylindres) : $14{,}00\\text{ €/T}$
- **DS = 84.50 €/T | PV HT = 108.16 €/T**

## Nœuds Liés
- [[Thermométrie & Compactage BBSG]]
- [[Fourniture BBSG Centrale Enrobés Sud]]
"""
        },
        {
            "id": "sdp_canalisation_eu",
            "label": "SDP 24 : Tuyau PVC CR8 Ø200",
            "group": "Sous-Détails & Matériaux",
            "val": 14,
            "color": "#64748b",
            "tags": ["#sdp", "#tuyau", "#pvc"],
            "summary": "Pose tuyau PVC assainissement joint élastomère — DS = 54.00 €/ml, PV = 69.12 €/ml.",
            "content": """---
title: SDP 24 : Tuyau PVC CR8 Ø200
tags: [#sdp, #tuyau, #pvc]
group: Sous-Détails & Matériaux
date: 2026-09-09
---

# SDP 24 : Pose de Tuyaux PVC CR8 Ø200

- Fourniture tuyau PVC CR8 : $18{,}50\\text{ €/ml}$
- Lit de pose et remblai d'enrobage : $16{,}20\\text{ €/ml}$
- Équipe poseur + aide : $19{,}30\\text{ €/ml}$
- **DS = 54.00 €/ml | PV HT = 69.12 €/ml**

## Nœuds Liés
- [[IfcPipeSegment (Réseau Assainissement EU)]]
- [[Hydraulique Manning-Strickler]]
"""
        },
        {
            "id": "mat_carriere",
            "label": "Fourniture GNT Carrières de la Montagne",
            "group": "Sous-Détails & Matériaux",
            "val": 12,
            "color": "#64748b",
            "tags": ["#fournisseur", "#carriere", "#gnt"],
            "summary": "Contrat d'approvisionnement GNT 0/31.5 Reconstituée Humidifiée (1 850 Tonnes).",
            "content": """---
title: Fourniture GNT Carrières de la Montagne
tags: [#fournisseur, #carriere, #gnt]
group: Sous-Détails & Matériaux
date: 2026-09-09
---

# Fournisseur Agréé : Carrières de la Montagne

Granulats certifiés NF P 18-545 catégorie B.

## Nœuds Liés
- [[SDP 05 : Couche Fondation GNT 0/31.5]]
"""
        },
        {
            "id": "mat_centrale_enrobe",
            "label": "Fourniture BBSG Centrale Enrobés Sud",
            "group": "Sous-Détails & Matériaux",
            "val": 12,
            "color": "#64748b",
            "tags": ["#fournisseur", "#enrobage", "#bitume"],
            "summary": "Formule BBSG 0/10 35/50 avec 20% d'agrégats d'enrobés recyclés (920 Tonnes).",
            "content": """---
title: Fourniture BBSG Centrale Enrobés Sud
tags: [#fournisseur, #enrobage, #bitume]
group: Sous-Détails & Matériaux
date: 2026-09-09
---

# Fournisseur Agréé : Centrale Enrobés Sud

Centrale d'enrobage discontinue certifiée CE Niveau 2+.

## Nœuds Liés
- [[SDP 18 : Enrobé Bitumineux BB 0/10]]
"""
        },
        {
            "id": "mat_prefa_beton",
            "label": "Préfabriqués Bétons & Bordures FR",
            "group": "Sous-Détails & Matériaux",
            "val": 12,
            "color": "#64748b",
            "tags": ["#fournisseur", "#prefa", "#bordures"],
            "summary": "Bordures béton T2 et caniveaux CS2 conformes NF EN 1340.",
            "content": """---
title: Préfabriqués Bétons & Bordures FR
tags: [#fournisseur, #prefa, #bordures]
group: Sous-Détails & Matériaux
date: 2026-09-09
---

# Fournisseur Agréé : Bétons & Préfabriqués FR

Éléments préfabriqués en béton auto-plaçant C30/37 résistant au gel sévère.

## Nœuds Liés
- [[SDP 12 : Bordure Béton T2 Préfabriquée]]
"""
        }
    ]

    # COMPREHENSIVE EDGES (140+ links)
    links = [
        # Rapports to Master Synthesis
        {"source": "doc_00", "target": "doc_01", "type": "synthese"},
        {"source": "doc_00", "target": "doc_02", "type": "synthese"},
        {"source": "doc_00", "target": "doc_03", "type": "synthese"},
        {"source": "doc_00", "target": "doc_04", "type": "synthese"},
        {"source": "doc_00", "target": "doc_05", "type": "synthese"},
        {"source": "doc_00", "target": "doc_06", "type": "synthese"},
        {"source": "doc_00", "target": "doc_07", "type": "synthese"},
        {"source": "doc_00", "target": "doc_08", "type": "synthese"},
        {"source": "doc_00", "target": "chantier_barbazan", "type": "etudie"},
        {"source": "doc_00", "target": "chantier_stnicolas", "type": "etudie"},
        {"source": "doc_00", "target": "chantier_aurouer", "type": "etudie"},

        # Rapport 01 Marchés
        {"source": "doc_01", "target": "phase_0", "type": "cadre"},
        {"source": "doc_01", "target": "norme_ccag", "type": "analyse"},
        {"source": "doc_01", "target": "agent_legal", "type": "execute_par"},
        {"source": "doc_01", "target": "norme_pgc", "type": "examine"},

        # Rapport 02 Prix
        {"source": "doc_02", "target": "phase_1", "type": "chiffre"},
        {"source": "doc_02", "target": "form_ds", "type": "formule"},
        {"source": "doc_02", "target": "form_k", "type": "formule"},
        {"source": "doc_02", "target": "form_thmo", "type": "formule"},
        {"source": "doc_02", "target": "form_tp08", "type": "formule"},
        {"source": "doc_02", "target": "agent_budget", "type": "execute_par"},
        {"source": "doc_02", "target": "sdp_terrassement", "type": "detail"},
        {"source": "doc_02", "target": "sdp_gnt", "type": "detail"},
        {"source": "doc_02", "target": "sdp_bordure_t2", "type": "detail"},
        {"source": "doc_02", "target": "sdp_enrobe_bb", "type": "detail"},
        {"source": "doc_02", "target": "sdp_canalisation_eu", "type": "detail"},

        # Rapport 03 VRD
        {"source": "doc_03", "target": "phase_3", "type": "prescrit"},
        {"source": "doc_03", "target": "form_manning", "type": "calcule"},
        {"source": "doc_03", "target": "form_ev2", "type": "controle"},
        {"source": "doc_03", "target": "form_enrobe", "type": "controle"},
        {"source": "doc_03", "target": "norme_fascicule70", "type": "reglemente"},
        {"source": "doc_03", "target": "bim_ifcroad", "type": "specifie"},

        # Rapport 04 DICT
        {"source": "doc_04", "target": "phase_2", "type": "prescrit"},
        {"source": "doc_04", "target": "norme_dict", "type": "applique"},
        {"source": "doc_04", "target": "norme_aipr", "type": "verifie"},
        {"source": "doc_04", "target": "norme_nfp98332", "type": "impose"},
        {"source": "doc_04", "target": "agent_dict", "type": "execute_par"},

        # Rapport 05 Pilotage
        {"source": "doc_05", "target": "phase_3", "type": "pilote"},
        {"source": "doc_05", "target": "phase_4", "type": "suivi"},
        {"source": "doc_05", "target": "agent_telemetry", "type": "alimente"},
        {"source": "doc_05", "target": "agent_planning", "type": "planifie"},
        {"source": "doc_05", "target": "chantier_barbazan", "type": "retour_experience"},

        # Rapport 06 DOE
        {"source": "doc_06", "target": "phase_5", "type": "valide"},
        {"source": "doc_06", "target": "phase_6", "type": "cloture"},
        {"source": "doc_06", "target": "norme_si022", "type": "standardise"},
        {"source": "doc_06", "target": "norme_trackdechets", "type": "tracabilite"},
        {"source": "doc_06", "target": "norme_chorus", "type": "transmet"},
        {"source": "doc_06", "target": "agent_closeout", "type": "execute_par"},

        # Rapport 07 Schéma
        {"source": "doc_07", "target": "phase_0", "type": "inclut"},
        {"source": "doc_07", "target": "phase_1", "type": "inclut"},
        {"source": "doc_07", "target": "phase_2", "type": "inclut"},
        {"source": "doc_07", "target": "phase_3", "type": "inclut"},
        {"source": "doc_07", "target": "phase_4", "type": "inclut"},
        {"source": "doc_07", "target": "phase_5", "type": "inclut"},
        {"source": "doc_07", "target": "phase_6", "type": "inclut"},

        # Rapport 08 BIM
        {"source": "doc_08", "target": "bim_ifcproject", "type": "structure"},
        {"source": "doc_08", "target": "bim_ifcroad", "type": "modele"},
        {"source": "doc_08", "target": "bim_ifcpipe_eu", "type": "modele"},
        {"source": "doc_08", "target": "bim_ifcpipe_aep", "type": "modele"},
        {"source": "doc_08", "target": "bim_landxml", "type": "exporte"},
        {"source": "doc_08", "target": "bim_bcf", "type": "coordonne"},
        {"source": "doc_08", "target": "agent_bim", "type": "execute_par"},

        # Lifecycle Sequence Chain (Phases 0 to 6)
        {"source": "phase_0", "target": "phase_1", "type": "succede"},
        {"source": "phase_1", "target": "phase_2", "type": "succede"},
        {"source": "phase_2", "target": "phase_3", "type": "succede"},
        {"source": "phase_3", "target": "phase_4", "type": "succede"},
        {"source": "phase_4", "target": "phase_5", "type": "succede"},
        {"source": "phase_5", "target": "phase_6", "type": "succede"},

        # Phases to Agents
        {"source": "phase_0", "target": "agent_legal", "type": "supervise_par"},
        {"source": "phase_1", "target": "agent_budget", "type": "supervise_par"},
        {"source": "phase_2", "target": "agent_dict", "type": "supervise_par"},
        {"source": "phase_3", "target": "agent_telemetry", "type": "supervise_par"},
        {"source": "phase_3", "target": "agent_planning", "type": "supervise_par"},
        {"source": "phase_4", "target": "agent_budget", "type": "supervise_par"},
        {"source": "phase_5", "target": "agent_closeout", "type": "supervise_par"},
        {"source": "phase_6", "target": "agent_closeout", "type": "supervise_par"},

        # Formulas to Components & Agents
        {"source": "form_ds", "target": "form_k", "type": "multiplie"},
        {"source": "form_ds", "target": "form_thmo", "type": "integre"},
        {"source": "form_ds", "target": "agent_budget", "type": "utilise_par"},
        {"source": "form_k", "target": "agent_budget", "type": "utilise_par"},
        {"source": "form_tp08", "target": "phase_4", "type": "applique_a"},
        {"source": "form_manning", "target": "bim_ifcpipe_eu", "type": "calibre"},
        {"source": "form_ev2", "target": "chantier_stnicolas", "type": "valide"},
        {"source": "form_ev2", "target": "sdp_gnt", "type": "eprouve"},
        {"source": "form_enrobe", "target": "chantier_barbazan", "type": "surveille"},
        {"source": "form_enrobe", "target": "sdp_enrobe_bb", "type": "controle"},
        {"source": "form_bordure", "target": "sdp_bordure_t2", "type": "quantifie"},

        # Regulatory connections
        {"source": "norme_dict", "target": "norme_aipr", "type": "exige"},
        {"source": "norme_dict", "target": "phase_2", "type": "impose_delai"},
        {"source": "norme_nfp98332", "target": "bim_ifcpipe_aep", "type": "surveille_clash"},
        {"source": "norme_nfp98332", "target": "bim_ifcpipe_eu", "type": "surveille_clash"},
        {"source": "norme_fascicule70", "target": "bim_ifcpipe_eu", "type": "norme_pose"},
        {"source": "norme_fascicule70", "target": "sdp_canalisation_eu", "type": "conforme_a"},
        {"source": "norme_trackdechets", "target": "agent_procurement", "type": "tracabilite"},
        {"source": "norme_si022", "target": "phase_6", "type": "standard_doe"},
        {"source": "norme_chorus", "target": "phase_6", "type": "solde_marche"},
        {"source": "norme_pgc", "target": "phase_2", "type": "integre_dans"},

        # Real Cases Links
        {"source": "chantier_barbazan", "target": "bim_ifcproject", "type": "jumeau_3d"},
        {"source": "chantier_barbazan", "target": "sdp_enrobe_bb", "type": "consomme"},
        {"source": "chantier_barbazan", "target": "sdp_bordure_t2", "type": "consomme"},
        {"source": "chantier_barbazan", "target": "sdp_canalisation_eu", "type": "consomme"},
        {"source": "chantier_stnicolas", "target": "sdp_gnt", "type": "consomme"},
        {"source": "chantier_stnicolas", "target": "sdp_terrassement", "type": "consomme"},
        {"source": "chantier_aurouer", "target": "norme_dict", "type": "securite"},
        {"source": "chantier_aurouer", "target": "sdp_enrobe_bb", "type": "consomme"},

        # BIM Hierarchy Links
        {"source": "bim_ifcproject", "target": "bim_ifcroad", "type": "contient"},
        {"source": "bim_ifcproject", "target": "bim_ifcpipe_eu", "type": "contient"},
        {"source": "bim_ifcroad", "target": "bim_landxml", "type": "exporte_axe"},
        {"source": "bim_ifcpipe_eu", "target": "bim_ifcchamber", "type": "connecte"},
        {"source": "bim_ifcpipe_eu", "target": "bim_ifcpipe_aep", "type": "croise"},
        {"source": "bim_ifcpipe_aep", "target": "bim_bcf", "type": "signale_conflit"},

        # Materials & SDP
        {"source": "mat_carriere", "target": "sdp_gnt", "type": "fournit"},
        {"source": "mat_centrale_enrobe", "target": "sdp_enrobe_bb", "type": "fournit"},
        {"source": "mat_prefa_beton", "target": "sdp_bordure_t2", "type": "fournit"},
        {"source": "agent_procurement", "target": "mat_carriere", "type": "commande_a"},
        {"source": "agent_procurement", "target": "mat_centrale_enrobe", "type": "commande_a"},
        {"source": "agent_procurement", "target": "mat_prefa_beton", "type": "commande_a"}
    ]

    return {"nodes": nodes, "links": links}

if __name__ == "__main__":
    data = get_obsidian_dataset()
    print(f"Generated {len(data['nodes'])} nodes and {len(data['links'])} links successfully!")
