import os
import json
from pathlib import Path

BASE = Path('/home/user/monorepo')
PROJECT_DIR = BASE / 'projects' / 'btp-conduite-travaux'
RAPPORTS_DIR = PROJECT_DIR / 'rapports'
DATA_DIR = PROJECT_DIR / 'data'
DOCS_SRC = PROJECT_DIR / 'documents_sources'

RAPPORTS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------
# 01. ANALYSE MARCHES DCE ET CADRE JURIDIQUE
# -------------------------------------------------------------
report_01 = """# RAPPORT THÉMATIQUE 01 : ANALYSE DES MARCHÉS PUBLICS, DCE ET CADRE JURIDIQUE

> **Domaine :** Passation, Analyse des DCE, Droit des Marchés Publics et Clauses Contractuelles  
> **Projets audités :** Giratoire de Barbazan (DVI 31), Voie Nouvelle PUP Saint-Nicolas-de-la-Grave, Lotissement La Croix Pruniaux à Aurouer (Moulins Habitat 03)  
> **Date de référence :** 2026  

---

## 1. Introduction et Périmètre d'Étude

Le présent rapport analyse les pièces administratives et contractuelles constitutives des Dossiers de Consultation des Entreprises (DCE) présents dans le corpus :
- **Projet Giratoire de Barbazan (Conseil Général 31 - Réf. 0593221) :** Marché public à bons de commande et prix unitaires pour l'aménagement d'un carrefour giratoire sur la RD33 / RD33D (PR 9+978).
- **Projet Urbain Partenarial (PUP) de Saint-Nicolas-de-la-Grave (Dossier A14210) :** Aménagement d'une voie nouvelle de desserte, procédure adaptée (MAPA) avec convention de PUP.
- **Lotissement « La Croix Pruniaux » à Aurouer (Moulins Habitat - 03) :** Marché alloti en 2 lots (Lot 1 Terrassement/Voirie/EP, Lot 2 Réseaux Divers EU/AEP/Secs) avec découpage en Tranche Ferme (T1 - 9 lots) et Tranche Conditionnelle (T2 - 4 lots).

---

## 2. Anatomie Comparative des Pièces Administratives

```
+-----------------------------------------------------------------------------------------------------------------------------------------+
|                                                  ANALYSE COMPARATIVE DES MARCHÉS DU CORPUS                                              |
+-----------------------------+------------------------------------+------------------------------------+---------------------------------+
| CARACTÉRISTIQUE             | GIRATOIRE DE BARBAZAN (31)         | PUP SAINT-NICOLAS-DE-LA-GRAVE (82) | LOTISSEMENT PRUNIAUX AUROUER(03)|
+-----------------------------+------------------------------------+------------------------------------+---------------------------------+
| Maîtrise d'Ouvrage (MOA)    | Conseil Général de Haute-Garonne   | Commune de St-Nicolas-de-la-Grave  | Moulins Habitat (Bailleur OPH)  |
| Maîtrise d'Œuvre (MOE)      | Service Études Sud + Reulet Ing.   | Bureau d'Études BL                 | Maîtrise d'œuvre interne / VRD  |
| Type de Marché              | Marché public de travaux unitaire  | Procédure Adaptée (MAPA - PUP)     | MAPA Alloti avec Tranches (T1/T2)|
| Découpage / Allotissement   | Lot unique VRD / Chaussée          | Lot unique Voie nouvelle           | Lot 1 (VRD/EP) & Lot 2 (EU/AEP) |
| Forme des Prix              | Prix Unitaires (BPU + DQE)         | Prix Unitaires (BPU + DQE)         | Prix Unitaires (BPU + DE T1/T2) |
| Révision des Prix           | Formule paramétrique TP01 / TP08   | Prix Ferme Actualisable            | Prix Ferme Actualisable         |
| Retenue de Garantie         | 5% ou Caution Personnelle Solidaire| 5% ou Garantie à Première Demande  | 5% ou Caution Bancaire          |
| Délais de Paiement          | 30 jours (Comptable Public)        | 30 jours (Trésorerie Municipale)   | 30 jours (Virement OPH)         |
| Pénalités de Retard         | 1/1000e par jour calendaire        | 100 € par jour ouvré de retard     | 1/2000e par jour de retard      |
+-----------------------------+------------------------------------+------------------------------------+---------------------------------+
```

---

## 3. Confrontation avec le CCAG-Travaux 2021 Actualisé

Les documents de formation reposent sur les versions historiques du Code des Marchés Publics et du CCAG-Travaux 2009/2014. La confrontation avec le **CCAG-Travaux 2021 actualisé (Arrêté du 30 mars 2021)** révèle des évolutions majeures que le conducteur de travaux moderne doit impérativement maîtriser :

### 3.1. L'Obligation des Clauses Environnementales (Article 20.4)
- **Dans le corpus historique :** L'aspect environnemental se limite au Plan Assurance Environnement (PAE) général et à des mentions génériques de propreté de chantier dans le CCTP.
- **Dans l'état de l'art CCAG 2021 :** L'article 20.4 impose au titulaire la remise d'un **Schéma d'Organisation et de Gestion des Déchets (SOGED)** et d'un **Schéma d'Organisation et de Suivi de la Qualité (SOPAQ)** sous peine de pénalités contractuelles automatiques. Le réemploi in-situ et le taux de valorisation matière doivent atteindre au minimum **70%** en masse conformément à la Loi AGEC et à la REP PMCB.

### 3.2. Le Plafonnement des Pénalités de Retard (Article 19.2.2)
- **Dans le corpus historique :** Les pénalités journalières s'appliquaient sans plafond explicite, risquant d'absorber l'intégralité de la marge de l'entreprise sur les chantiers subissant de forts retards (comme à Barbazan avec 3 semaines d'arrêt concessionnaires).
- **Dans l'état de l'art CCAG 2021 :** Les pénalités sont désormais **plafonnées à 10% du montant total hors taxes du marché**, protégeant la santé financière des PME du BTP.

### 3.3. Revalorisation des Avances Financières (Article 10.1)
- Pour les marchés publics de l'État et des collectivités supérieures, l'avance forfaitaire obligatoire pour les PME a été portée de 5% à **20% voire 30%**, injectant de la trésorerie indispensable pour couvrir les approvisionnements initiaux (bordures, tuyaux, géotextiles).

### 3.4. Gestion Dématérialisée et Chorus Pro (Article 11)
- Facturation et transmission des décomptes mensuels (DP) et du Décompte Général et Définitif (DGD) obligatoirement via le portail **Chorus Pro**, avec horodatage certifié réduisant les contestations sur la date de notification.

---

## 4. Retours d'Expérience In-Situ : Pièges et Contentieux

1. **Le retard d'Ordre de Service (OS) :** Sur le chantier de Barbazan, l'entreprise a démarré des travaux d'élargissement avant notification de l'OS de démarrage formel. En cas d'accident ou de contestation, l'entreprise engage sa responsabilité pleine et entière. **Règle in-situ :** Aucune intervention physique sans OS signé par le représentant du pouvoir adjudicateur.
2. **La gestion des tranches conditionnelles (Cas Aurouer) :** L'entreprise retenue sur le Lotissement Pruniaux doit surveiller l'OS d'affermissement de la Tranche Conditionnelle T2. Si la décision n'est pas notifiée dans le délai contractuel fixé au CCAP, l'entreprise a droit à une indemnité d'attente ou de dédit (Art. 72 CCP).
3. **Le Mémoire de Réclamation (Article 55 CCAG 2021) :** Tout litige relatif au décompte ou à des sujétions imprévues doit faire l'objet d'un mémoire en réclamation adressé dans les **30 jours** suivant la notification de la décision contestée, sous peine de forclusion irrémédiable.
"""

(RAPPORTS_DIR / '01_ANALYSE_MARCHES_DCE_ET_CADRE_JURIDIQUE.md').write_text(report_01, encoding='utf-8')
print("Wrote 01_ANALYSE_MARCHES_DCE_ET_CADRE_JURIDIQUE.md")

# -------------------------------------------------------------
# 02. ETUDE DE PRIX METHODES ET SOUS DETAILS
# -------------------------------------------------------------
report_02 = """# RAPPORT THÉMATIQUE 02 : ÉTUDE DE PRIX, MÉTHODES ET SOUS-DÉTAILS (SDP)

> **Domaine :** Chiffrage, Déboursé Sec, Taux Horaires, Amortissement du Matériel et Coefficients de Frais Généraux  
> **Données analysées :** 28 Fiches de Sous-Détails de Prix (SDP), Bibliothèque Fournitures, Barèmes Engins et Main d'Œuvre  
> **Date de référence :** 2026  

---

## 1. Structure Mathématique du Prix de Vente dans le Corpus

L'ensemble des fiches d'étude de prix du corpus applique la formule canonique du génie civil :

$$\\text{PV}_{\\text{HT}} = \\text{DS} \\times K$$

avec :
- $\\text{DS}$ (Déboursé Sec Unitaire) = $\\text{MO} + \\text{MAT} + \\text{MATL} + \\text{ST}$
  - $\\text{MO}$ : Main d'œuvre directe d'exécution (Heures ouvriers $\\times$ Taux horaire chargé THMO)
  - $\\text{MAT}$ : Matériaux et fournitures livrés sur chantier (prix d'achat franco chantier)
  - $\\text{MATL}$ : Matériel affecté à la tâche (Amortissement + Entretien/Réparations + Consommables GNR/Carburant)
  - $\\text{ST}$ : Prestations sous-traitées éventuelles
- $K$ (Coefficient de Vente) appliqué dans le corpus : **$K = 1,250$** (soit 25% de majoration sur déboursé sec pour couvrir les Frais Généraux de siège $\\approx 13\\%$, les Frais de Chantier non affectés $\\approx 5\\%$ et les Bénéfices & Aléas $\\approx 7\\%$).

---

## 2. Table Récapitulative des 20 Sous-Détails de Prix Clés du Corpus

```
+---------------------------------------------------------------------------------------------------------------------------------+
|                                          SYNTHÈSE DES SOUS-DÉTAILS DE PRIX DU CHANTIER DE BARBAZAN                              |
+-------+------------------------------------------+----+---------+--------+----------+------------+------------------------------+
| CODE  | DÉSIGNATION DE L'OUVRAGE                 | U  | DS (€)  | COEFF K| PV HT (€)| RENDEMENT  | COMPOSITION DE L'ÉQUIPE      |
+-------+------------------------------------------+----+---------+--------+----------+------------+------------------------------+
| 515_P2| Bordure P2 pour anneau giratoire         | ml |   34,17 |  1,250 |    42,71 |  15,0 ml/j | 1 Chef (275€/j) + 1 Ouv (155€)|
| 514_I1| Bordure d'îlot séparateur I1             | ml |   37,39 |  1,250 |    46,74 |  14,5 ml/j | 1 Chef (275€/j) + 1 Ouv (155€)|
| 515_I2| Bordure d'îlot séparateur I2             | ml |   57,38 |  1,250 |    71,73 |  12,7 ml/j | 1 Chef (275€/j) + 2 Ouv (310€)|
| 522CC1| Bordure Caniveau CC1                     | ml |  122,74 |  1,250 |   153,43 |   9,0 ml/j | 2 Ouv (310€/j) + 1 OHQ (180€)|
| 409c  | Couche fondation Grave Bitume Cl.3 (12cm)| t  |   86,71 |  1,250 |   108,39 |   23,9 t/j | 1 Chef (275€/j) + 1 Ouv (155€)|
| 409b  | Couche reprofilage Grave Bitume Cl.2     | t  |   67,56 |  1,250 |    84,45 |   23,5 t/j | 1 Chef (275€/j) + 1 Ouv (155€)|
| 423B1 | Couche de roulement BBSG 0/14 Cl.3 (6cm) | t  |   89,71 |  1,250 |   112,14 |   19,8 t/j | 1 Chef (275€/j) + 1 Ouv (155€)|
| 412S  | Couche de réglage GNT 0/20 concassée     | m³ |   77,11 |  1,250 |    96,39 |  10,2 m³/j | 1 Chef (275€/j) + 1 Ouv (155€)|
| 301   | Décapage terre végétale ép. 20cm         | m² |    2,81 |  1,250 |     3,51 | 235,0 m²/j | 1 Chef (275€/j) + 1 Ouv (155€)|
| 311   | Remblais d'apport compactés              | m³ |   57,28 |  1,250 |    71,60 |  17,5 m³/j | 1 Chef (275€/j) + 1 Ouv (155€)|
| 207B  | Démolition découpe chaussée scie hydr.   | m² |   16,65 |  1,250 |    20,81 | 361,6 m²/j | 1 Chef (275€/j) + 1 Ouv (155€)|
| 210   | Rabotage de chaussée 0-5 cm              | m² |   11,63 |  1,250 |    14,54 | 504,3 m²/j | 1 Chef (275€/j) + 1 Ouv (155€)|
| 537B  | Galets maçonnés en surlargeur giratoire  | m² |   51,47 |  1,250 |    64,34 |   4,3 m²/j | 2 Ouv (310€/j) + 1 OHQ (180€)|
| 537S  | Îlots en béton et galets de Garonne      | m² |   34,71 |  1,250 |    43,39 |   4,3 m²/j | 2 Ouv (310€/j) + 1 OHQ (180€)|
| 536B  | Remplissage d'îlots en béton C20/25      | m² |   29,93 |  1,250 |    37,41 |  72,9 m²/j | 2 Ouv (310€/j) + 1 OHQ (180€)|
| 662SE | Construction de cunette bétonnée coulée  | ml |  149,35 |  1,250 |   186,69 |   6,7 ml/j | 2 Ouv (310€/j) + 1 OHQ (180€)|
| 665D  | Regard 40x40 avec grille fonte           | u  | 1143,92 |  1,250 |  1429,90 |    1,0 u/j | 1 Ouv (155€/j) + 2 OHQ (360€)|
| 676S  | Tuyaux PVC Ø300 classe 41 (CR4)          | ml |  400,86 |  1,250 |   501,08 |   8,0 ml/j | 1 Ouv (155€/j) + 2 OHQ (360€)|
| 672B  | Fourreau TPC Janolène Ø110               | ml |   34,27 |  1,250 |    42,84 |  14,3 ml/j | 1 Ouv (155€/j) + 1 OHQ (180€)|
| 930S  | Dépose de glissières de sécurité GS2     | ml |   15,31 |  1,250 |    19,14 |  27,3 ml/j | 2 Ouvriers (310€/j)           |
+-------+------------------------------------------+----+---------+--------+----------+------------+------------------------------+
```

---

## 3. Analyse Critique des Barèmes Engins et Main d'Œuvre

### 3.1. Main d'Œuvre : Confrontation des Coûts Horaires
- **Dans le corpus de formation :**
  - Manœuvre / Ouvrier TP : 155 € / jour (soit $\\approx 22,14$ €/h sur base 7h).
  - Ouvrier Hautement Qualifié (OHQ) / Maçon : 180 à 270 € / jour (soit 25,71 à 38,57 €/h).
  - Chef de chantier : 275 € / jour (soit $\\approx 39,29$ €/h).
- **Dans l'état de l'art 2026 (Grilles FNTP Occitanie actualisées) :**
  - Le **Taux Horaire Moyen Ouvrier (THMO)** réel comprend le salaire brut horaire, les charges sociales patronales (45-52%), les cotisations CNETP (congés payés + intempéries $\\approx 19,7\\%$), l'OPPBTP, la médecine du travail, ainsi que les Indemnités de Petits Déplacements (IPD : panier repas $10,50$ €, prime de trajet, prime de transport).
  - **THMO réel 2026 :** $38,00$ à $48,00$ €/h pour un ouvrier qualifié (Niveau III), et $58,00$ à $75,00$ €/h pour un chef de chantier (ETAM Niveau F/G). Les prix du corpus constituent des valeurs pédagogiques sous-estimant l'inflation salariale récente.

### 3.2. Parc Matériel et Engins (Fichier `Equipement 30-05.xlsx`)
- Pelle à chenilles 20,3 t (Volvo EC 200-D, 2021) : Coût journalier calculé = $336,57$ €/j $\\rightarrow$ Coût majoré retenu = $350,00$ €/j.
- Pelle sur pneus 17,9 t (Volvo ECR48 C, 2009) : Coût journalier calculé = $310,47$ €/j $\\rightarrow$ Coût majoré retenu = $320,00$ €/j.
- Petits matériels : Tronçonneuse à disque Stihl TS420 ($30$ €/j), plaque vibrante Mikasa 75 kg ($25$ €/j), fourgon double cabine Iveco Daily ($120$ €/j).

---

## 4. Confrontation In-Situ : Rendements Réels vs Rendements Théoriques

1. **Facteurs d'abattement urbain :** Les rendements théoriques de pose de bordures ($15$ ml/j en P2) supposent une tranchée ouverte continue sans obstacle. En milieu sous circulation (giratoire de Barbazan), les reprises d'alignement, les regards d'eaux pluviales et les accès riverains réduisent le rendement effectif à **$9-11$ ml/j** (-30%).
2. **Surconsommation de matériaux :** En application d'enrobés (BBSG 0/14), le tonnage théorique calculé sur une densité de $2,50$ t/m³ et une épaisseur constante de 6 cm est systématiquement dépassé de **$+5\\%$ à $+10\\%$** en raison des irrégularités du support raboté (déflachage) et du compactage. L'étude de prix terrain doit intégrer une perte de foisonnement et de matière.
3. **Formules de révision TP :** En période d'instabilité des cours pétroliers, l'application de la formule d'indexation $P = P_0 \\times [0,15 + 0,85 \\times (TP08 / TP08_0)]$ est la seule garantie pour préserver la marge nette de l'entreprise.
"""

(RAPPORTS_DIR / '02_ETUDE_DE_PRIX_METHODES_ET_SOUS_DETAILS.md').write_text(report_02, encoding='utf-8')
print("Wrote 02_ETUDE_DE_PRIX_METHODES_ET_SOUS_DETAILS.md")

# -------------------------------------------------------------
# 03. TECHNIQUE VOIRIE RESEAUX ET TERRASSEMENT
# -------------------------------------------------------------
report_03 = """# RAPPORT THÉMATIQUE 03 : TECHNIQUE ROUTIÈRE, VRD, TERRASSEMENT ET ASSAINISSEMENT

> **Domaine :** Conception et Dimensionnement des Chaussées, Géotechnique, Pose de Réseaux et Nivellement 3D  
> **Normes de référence :** NF P 98-086, NF EN 13108, NF EN 1340, NF EN 1610, Fascicules 29 et 70 du CCTG  
> **Date de référence :** 2026  

---

## 1. Structures de Chaussées Étudiées dans le Corpus

Le dimensionnement des chaussées du giratoire de Barbazan et du PUP de Saint-Nicolas repose sur un catalogue de structures semi-lourdes à fort trafic :

```
+----------------------------------------------------------------------------------------------------+
|                                    COUPE TRANSVERSALE TYPE DE CHAUSSÉE                            |
+====================================================================================================+
| [ COUCHE DE ROULEMENT ]    : BBSG 0/14 Classe 3 (Béton Bitumineux Semi-Grenu)       -> Épaisseur : 6 cm   |
| -------------------------------------------------------------------------------------------------- |
| [ COUCHE D'ACCROCHAGE ]    : Émulsion de bitume cationique à 65%                    -> Dosage : 350 g/m²  |
| -------------------------------------------------------------------------------------------------- |
| [ COUCHE DE FONDATION ]    : GB3 (Grave Bitume Classe 3)                            -> Épaisseur : 12 cm  |
| -------------------------------------------------------------------------------------------------- |
| [ COUCHE DE BASE/RÉGLAGE]  : GNT 0/20 Classe A (Grave Non Traitée concassée)       -> Épaisseur : 10 cm  |
| -------------------------------------------------------------------------------------------------- |
| [ COUCHE DE FORME ]        : Matériaux d'apport sélectionnés + Géotextile anti-contam. -> Épaisseur : 30 cm  |
| -------------------------------------------------------------------------------------------------- |
| [ PLATEFORME SUPPORT PST ] : Sol support préparé (Objectif de portance AR2 : EV2 >= 50 MPa)        |
+----------------------------------------------------------------------------------------------------+
```

---

## 2. Éléments Préfabriqués et Bordures de Voirie

Le corpus détaille les profils normalisés selon la norme **NF EN 1340** :
- **Bordures P1 / P2 :** Bordures pour pistes cyclables et giratoires à profil incliné (franchissables pour véhicules de secours, infranchissables pour véhicules légers).
- **Bordures d'îlots I1 / I2 :** Profils verticaux assurant la canalisation des flux aux entrées d'anneau.
- **Bordures trottoirs T2 :** Séparation des cheminements piétons et PMR.
- **Caniveaux CC1 / CS2 :** Évacuation fil d'eau le long des bordures vers les avaloirs.
- **Prescription de pose :** Lit de béton C16/20 de 10 cm d'épaisseur avec épaulement / solin arrière à 45° montant jusqu'au tiers supérieur de la bordure.

---

## 3. Réseaux d'Assainissement et Gestion des Eaux Pluviales

### 3.1. Réseaux Enterrés (Fascicule 70 Titre I)
- Canalisations PVC rigide Ø300 mm classe de rigidité **CR4** (SN4) ou **CR8** (SN8) pour passage sous voirie lourde.
- Lit de pose en gravillon 4/10 ou 6/10 d'épaisseur 10 cm avec compactage soigné sous les flancs (zone de reins).
- Remblaiement méthodique par couches de 20 cm compactées jusqu'à l'arase de terrassement.

### 3.2. Bassins d'Orage et Écoulement Superficiel
- Sur Aurouer (La Croix Pruniaux) : Bassin de rétention à ciel ouvert avec surverse de sécurité et décanteur.
- Sur Barbazan : Cunettes bétonnées trapézoïdales coulées en place pour drainer les eaux de ruissellement vers les fossés naturels.

---

## 4. Confrontation avec l'État de l'Art 2026

```
+---------------------------------------------------------------------------------------------------------------------------------+
|                                                  CONFRONTATION TECHNIQUE & INNOVATIONS                                          |
+-----------------------------+------------------------------------+------------------------------------+-------------------------+
| DOMAINE TECHNIQUE           | RÉFÉRENTIEL CORPUS FORMATION       | ÉTAT DE L'ART 2026 (NORMES & R&D)  | GAINS & IMPACTS IN-SITU |
+-----------------------------+------------------------------------+------------------------------------+-------------------------+
| Fabrication des Enrobés     | Enrobés à chaud standards (160°C)  | Enrobés Tièdes (BBT à 120-130°C)   | -20% énergie, -30% CO2, |
|                             | Bitume pur 35/50 ou 50/70          | Liants biosourcés + 40-70% d'AE    | confort des ouvriers    |
+-----------------------------+------------------------------------+------------------------------------+-------------------------+
| Matériaux de Terrassement   | GNT vierge de carrière             | Graves recyclées de classe B       | Économie circulaire,    |
|                             | Évacuation des déblais en décharge | Traitement in-situ chaux/ciment    | réduction trafic camions|
+-----------------------------+------------------------------------+------------------------------------+-------------------------+
| Nivellement et Guidage      | Piquetage manuel, chaises bois     | Guidage 3D GNSS / Station totale   | Précision millimétrique,|
|                             | Niveau laser de chantier classique | Niveleuses asservies Trimble/Leica | gain de temps x3        |
+-----------------------------+------------------------------------+------------------------------------+-------------------------+
| Gestion des Eaux Pluviales  | Tuyaux PVC enterrés + bassins durs | Gestion intégrée à la source       | Recharge des nappes,    |
|                             | Rejet direct vers exutoire         | Noues paysagères, SAUL, drainant   | îlots de fraîcheur      |
+-----------------------------+------------------------------------+------------------------------------+-------------------------+
```

---

## 5. Retours d'Expérience Terrain et Aléas Géotechniques

1. **Perte de portance sous pluie battante :** Lors de la mise en œuvre de la GNT 0/20, si un orage survient avant le cylindrage final, l'eau s'infiltre dans les fines. Le contrôle par essai à la plaque Westergaard chute sous les 50 MPa exigés. **Solution terrain :** Purge des zones plastifiées ou scarification et malaxage à la chaux vive (1,5% à 2%).
2. **Refroidissement des enrobés en cours de transport :** Sur les chantiers ruraux éloignés de la centrale (trajet > 45 min), la température de fond de benne peut chuter sous 120°C. La mise en œuvre d'enrobé refroidi empêche le compactage correct par le tandem vibrant et engendre un risque d'arrachement superficiel sous trafic. L'usage de bennes calorifugées et le contrôle thermique au thermomètre infrarouge à l'arrivée sont obligatoires.
"""

(RAPPORTS_DIR / '03_TECHNIQUE_VOIRIE_RESEAUX_ET_TERRASSEMENT.md').write_text(report_03, encoding='utf-8')
print("Wrote 03_TECHNIQUE_VOIRIE_RESEAUX_ET_TERRASSEMENT.md")

# -------------------------------------------------------------
# 04. REGLEMENTATION ANTI ENDOMMAGEMENT DICT AIPR ET SECURITE
# -------------------------------------------------------------
report_04 = """# RAPPORT THÉMATIQUE 04 : RÉGLEMENTATION ANTI-ENDOMMAGEMENT (DT-DICT), AIPR ET SÉCURITÉ ROUTIÈRE

> **Domaine :** Prévention des Risques Liés aux Réseaux Enterrés, Habilitations AIPR, Sécurité SPS et Signalisation Temporaire  
> **Textes de référence :** Code de l'Environnement (L554-1 à L554-5, R554-1 à R554-39), Arrêté du 15 février 2012 modifié, Arrêté du 29 octobre 2018, IISR Livre 1 8e partie  
> **Date de référence :** 2026  

---

## 1. Le Dispositif Réglementaire Anti-Endommagement

Le corpus contient l'intégralité de la chaîne documentaire réglementaire obligatoire :
- **Déclaration de projet de Travaux (DT) :** Établie par le Maître d'Ouvrage (MOA) en phase conception via le Guichet Unique (*reseaux-et-canalisations.gouv.fr*). Exemple : Les 14 récépissés DT du projet PUP de Saint-Nicolas-de-la-Grave (Enedis, GRDF, Orange, SIVOM, etc.).
- **Déclaration d'Intention de Commencement de Travaux (DICT) :** Émise par l'entreprise adjudicataire au moins 9 jours ouvrés (téléservice) avant le coup de pioche (Cerfa 14434*03).
- **Récépissés et Cartographies :** Analyse des plans d'exploitants et détermination des classes de précision.

```
+----------------------------------------------------------------------------------------------------+
|                                 CLASSES DE PRÉCISION DES RÉSEAUX ENTERRÉS                          |
+=========+================================================+=========================================+
| CLASSE  | INCERTITUDE MAXIMALE POSITIONNEMENT HORIZONTAL | MODE OPÉRATOIRE D'EXCAVATION AUTORISÉ   |
+---------+------------------------------------------------+-----------------------------------------+
| CLASSE A| <= 40 cm (ouvrage rigide : béton, fonte)       | Engin mécanique autorisé avec précaution|
|         | <= 50 cm (ouvrage flexible : PEHD, câble)      | Godet lisse sans dents à proximité      |
+---------+------------------------------------------------+-----------------------------------------+
| CLASSE B| > 40/50 cm et <= 1,50 mètre                    | Sondages préliminaires manuels requis   |
|         |                                                | Terrassement doux / Aspiratrice déblais |
+---------+------------------------------------------------+-----------------------------------------+
| CLASSE C| > 1,50 mètre ou tracé imprécis                 | Fouille mécanique STRICTEMENT INTERDITE |
|         | (Cas fréquent sur réseaux anciens d'eau/gaz)   | Détection non destructive ou arrêt      |
+---------+------------------------------------------------+-----------------------------------------+
```

---

## 2. Analyse de la Base QCM AIPR du Corpus (Fichiers `AIPR CORRECTION.xlsx` & `QCM AIPR Encadrant.xls`)

Le corpus intègre plus de **300 questions-réponses officielles** ventilées selon les 3 profils d'habilitation :
1. **Profil Concepteur (C) :** Établissement des DT, intégration des investigations complémentaires (IC), clauses de sécurité dans les marchés.
2. **Profil Encadrant (E - Conducteur de Travaux / Chef de Chantier) :** Analyse des réponses DICT, préparation du piquetage, gestion des constats d'arrêt et de dommage.
3. **Profil Opérateur (O - Conducteur d'engins / Ouvrier) :** Respect du marquage-piquetage, gestes d'urgence en cas d'accrochage de câble ou fuite de gaz.

### Code Couleur Normalisé du Marquage-Piquetage (Arrêté du 15/02/2012)
- 🔴 **Rouge :** Électricité (BT, HTA, HTB) et Éclairage Public.
- 🟡 **Jaune :** Gaz combustible et Hydrocarbures.
- 🔵 **Bleu :** Eau potable.
- 🟢 **Vert :** Télécommunications, Fibre optique et Vidéoprotection.
- 🟤 **Marron :** Assainissement et Eaux Pluviales.
- ⚪ **Blanc :** Zone d'emprise des travaux et repères géomètres.

---

## 3. Signalisation Temporaire et Police de la Circulation

### 3.1. Autorisations Administratives Obligatoires
- **Cerfa 14023*01 :** Demande de permission ou d'autorisation de voirie (délivrée par le gestionnaire de voirie : Département pour RD, Maire pour voie communale).
- **Cerfa 14024*01 :** Demande d'arrêté de police de la circulation fixant les restrictions (vitesse, alternat, déviation).

### 3.2. Dispositifs Opérationnels Déployés (Manuel Chef de Chantier OPPBTP)
- **Alternat par feux tricolores de chantier (KR11j) :** Réglage du temps de vert et de rouge en fonction de la longueur de la zone neutralisée et du trafic moyen journalier annuel (TMJA).
- **Alternat manuel par piquets K10 :** Présence obligatoire de 2 agents équipés d'EPI haute visibilité classe 3 reliés par liaison radio.
- **Présignalisation réglementaire :** Panneau AK5 (Travaux) à 150m, suivi de AK17 (Feux tricolores), limitation dégressive BK14 (70 km/h puis 50 km/h), interdiction de dépasser BK31, fin d'interdiction BK31 en sortie de zone.

---

## 4. Confrontation In-Situ : Réalités du Terrain et Gestion d'Urgence

1. **La découverte d'un réseau non répertorié ou en classe C :** En cas d'anomalie sur le terrain (câble non cartographié à l'emplacement de la fouille de Barbazan), le chef de chantier doit immédiatement suspendre le terrassement mécanique et établir un **Constat d'arrêt ou de sursis de travaux** contresigné par le MOE. Ce constat suspend le délai d'exécution et justifie l'indemnisation des temps d'attente.
2. **L'accrochage accidentel d'une conduite de gaz :**
   - Règle d'or : Ne jamais tenter de boucher la fuite ni remblayer.
   - Évacuation immédiate de la zone sous le vent dans un rayon de 100 mètres.
   - Interdiction formelle de toute source d'ignition (moteurs d'engins coupés, pas de téléphone dans la zone d'exclusion).
   - Appel d'urgence aux Sapeurs-Pompiers (18/112) et au gestionnaire de réseau (Urgence Sécurité Gaz GRDF : 0 800 47 33 33).
   - Rédaction obligatoire d'un **Constat de Dommage** transmis sous 24 heures.
"""

(RAPPORTS_DIR / '04_REGLEMENTATION_ANTI_ENDOMMAGEMENT_DICT_AIPR_ET_SECURITE.md').write_text(report_04, encoding='utf-8')
print("Wrote 04_REGLEMENTATION_ANTI_ENDOMMAGEMENT_DICT_AIPR_ET_SECURITE.md")

# -------------------------------------------------------------
# 05. PILOTAGE IN SITU CR CHANTIER ALEAS ET GESTION LITIGES
# -------------------------------------------------------------
report_05 = """# RAPPORT THÉMATIQUE 05 : PILOTAGE D'EXÉCUTION IN-SITU, AUTOPSIE DES RÉUNIONS DE CHANTIER ET GESTION DES LITIGES

> **Domaine :** Conduite Opérationnelle, Comptes-Rendus Hebdomadaires, Non-Conformités et Réclamations Contractuelles  
> **Chantier d'étude :** Carrefour Giratoire RD33 / RD33D à Barbazan (Comptes-Rendus 1 à 9 & Fiche de Non-Conformité)  
> **Date de référence :** 2026  

---

## 1. Chronologie et Autopsie des Réunions de Chantier de Barbazan

L'analyse des comptes-rendus hebdomadaires réels (CR 1 à CR 9) et des fiches de suivi met en lumière la dynamique contractuelle et les frottements opérationnels réels vécus par l'équipe de conduite de travaux :

```
+---------------------------------------------------------------------------------------------------------------------------------+
|                                            CHRONOLOGIE ÉVÉNEMENTIELLE DU CHANTIER DE BARBAZAN                                    |
+======+==================+==============================================================+========================================+
| CR N°| DATE RÉUNION     | ÉVÉNEMENTS MARQUANTS & AVANCEMENT                            | DÉCISIONS, BLOCAGES & IMPACTS PLANNING |
+------+------------------+--------------------------------------------------------------+----------------------------------------+
| CR 1 | Démarrage        | Installation de chantier, mise en place signalisation        | Validation du plan de signalisation    |
|      |                  | Piquetage général de l'axe et repérage réseaux concessionn.  | Demande d'arrêtés préfectoraux confirmée|
+------+------------------+--------------------------------------------------------------+----------------------------------------+
| CR 2 | Semaine 2        | Début des terrassements et décapage terre végétale           | Découverte de câbles Télécom non classés|
|      |                  | Coactivité avec équipe Enedis pour déplacement de poteau     | Demande d'intervention urgente Orange  |
+------+------------------+--------------------------------------------------------------+----------------------------------------+
| CR 3 | Semaine 3        | Pose des bordures d'îlots I1 et caniveaux CC1 phase 1        | Blocage élargissement RD33D : poteau   |
|      |                  | Réalisation de la couche de réglage en GNT 0/20              | EDF non déplacé -> Décalage planning 5j|
+------+------------------+--------------------------------------------------------------+----------------------------------------+
| CR 4 | Semaine 4        | Épisode pluvieux intense : arase de terrassement détrempée   | Arrêt intempéries formalisé par OS     |
|      |                  | Essai de plaque Dynaplaque : EV2 insuffisant (38 MPa < 50)   | Prescription de traitement chaux (TS)  |
+------+------------------+--------------------------------------------------------------+----------------------------------------+
| CR 5 | Semaine 5        | Reprise des terrassements après séchage, fin pose bordures   | Enedis termine enfin son dévoiement    |
|      |                  | Validation de la couche de forme traitée par le laboratoire  | Phasage modifié pour rattraper retard  |
+------+------------------+--------------------------------------------------------------+----------------------------------------+
| CR 6 | Semaine 6        | Application de la Grave Bitume GB3 (12cm) en fondation       | Prélèvement d'échantillons enrobé par  |
|      |                  | Réalisation des îlots centraux en béton et galets Garonne    | le contrôle extérieur LRPC             |
+------+------------------+--------------------------------------------------------------+----------------------------------------+
| CR 7 | Semaine 7        | Pose des enrobés de roulement BBSG 0/14                      | Réception des résultats d'essais LRPC :|
|      |                  | Début des travaux de finition trottoirs et glissières        | ALERTE NON-CONFORMITÉ GRAVE SUR GB3    |
+------+------------------+--------------------------------------------------------------+----------------------------------------+
| CR 9 | Semaine 9        | Réunion de crise technique : gestion de la non-conformité    | Arrêt des réceptions définitives       |
|      |                  | Négociation tripartite Entreprise / Centrale / MOE           | Chiffrage de reprise à 202 783,93 € HT |
+------+------------------+--------------------------------------------------------------+----------------------------------------+
```

---

## 2. Autopsie de la Non-Conformité Majeure de Barbazan (Fichier `Recours Barbazan.pdf`)

### 2.1. Description du Désordre
- **Nature :** Surdosage massif en liant bitumineux sur la Grave Bitume Classe 3 (GB3) destinée aux couches de fondation et de base, fabriquée par la centrale d'enrobés de Villeneuve-de-Rivière (31800).
- **Mesure laboratoire :** Teneur en bitume mesurée à **$5,3\\%$** contre une formule nominale prescrite à **$4,5\\%$** (écart de $+0,8\\%$ hors tolérances de la norme NF EN 13108-1).
- **Risque mécanique à terme :** Fluage sous trafic lourd estival, ressuage de bitume en surface et orniérage structurel prématuré sur l'anneau giratoire.
- **Confirmation :** Non-conformité validée contradictoirement par le laboratoire de l'entreprise et le Laboratoire Régional des Ponts et Chaussées (LRPC / Cerema).

### 2.2. Chiffrage de l'Action Corrective Initiale

$$\\text{Coût Total de Reconstruction} = 202\\,783,93\\text{ € HT}$$

Ventilation détaillée :
- **Destruction et Dépose :**
  - Rabotage couche de roulement et base : $2\\,700,00$ €
  - Évacuation et mise en décharge agréée : $10\\,481,93$ €
- **Remise en Œuvre Conforme :**
  - Fourniture et application nouvelle GB3 + BBSG : $192\\,302,00$ €

### 2.3. Stratégie de Résolution et Droit des Marchés
Face à ce coût représentant plus de 75% de la valeur totale du marché, le conducteur de travaux a déployé la stratégie suivante :
1. **Appel en garantie du fournisseur :** Mise en demeure immédiate de la centrale d'enrobés en responsabilité produit défectueux.
2. **Proposition d'une solution de réfaction avec garantie étendue :** Si les calculs de fatigue démontrent une durée de vie acceptable sous réserve d'un trafic modéré, négociation d'une réfaction financière de 25% sur le prix unitaire de la GB3 assortie d'une garantie contractuelle de 15 ans avec suivi topographique annuel d'orniérage.

---

## 3. Confrontation avec le Lean Construction et le Last Planner System (LPS)

Dans les pratiques traditionnelles illustrées par le corpus, la planification est réactive (constat des retards à chaque réunion hebdomadaire). L'état de l'art 2026 promeut le **Last Planner System (LPS)** :
- **Planification inversée (*Pull Planning*) à 6 semaines :** Chaque tâche n'est engagée que si toutes ses contraintes préalables (libération des réseaux par Enedis, fourniture des bordures, météo favorable) sont levées à 100%.
- **Indicateur PPC (Pourcentage de Promesses Tenues) :** Suivi hebdomadaire de la fiabilité des engagements des chefs d'équipe et sous-traitants pour éradiquer la variabilité de chantier.
"""

(RAPPORTS_DIR / '05_PILOTAGE_IN_SITU_CR_CHANTIER_ALEAS_ET_GESTION_LITIGES.md').write_text(report_05, encoding='utf-8')
print("Wrote 05_PILOTAGE_IN_SITU_CR_CHANTIER_ALEAS_ET_GESTION_LITIGES.md")

# -------------------------------------------------------------
# 06. RECEPTION DOE ET TRANSITION NUMERIQUE BIM LEAN
# -------------------------------------------------------------
report_06 = """# RAPPORT THÉMATIQUE 06 : RÉCEPTION, CLÔTURE, DOE ET TRANSITION NUMÉRIQUE (BIM / SIG / TRACKDÉCHETS)

> **Domaine :** Dossier des Ouvrages Exécutés (DOE), Récolement Géoréférencé, OpenBIM Infrastructure (IFC 4.3), Traçabilité des Terres et Clôture Financière  
> **Documents analysés :** Standard Interne DOE Aéroports de Lyon (SI 022 - 37 pages), Fiche de Synthèse DOE (`Dossier des Ouvrages Exécutés.docx` / `doe.pdf`)  
> **Date de référence :** 2026  

---

## 1. Analyse du Standard DOE du Corpus (Standard SI 022 Aéroports de Lyon)

Le document de référence présent dans le corpus (Standard Interne SI 022 - 37 pages) constitue une référence méthodologique d'excellence industrielle pour la formalisation des DOE :

```
+----------------------------------------------------------------------------------------------------+
|                                    ARCHITECTURE TYPE D'UN DOE CONFORME                             |
+====================================================================================================+
| VOLUME 1 : PIÈCES GÉNÉRALES & ADMINISTRATIVES                                                     |
| - Fiche synthétique d'identification du marché, intervenants et dates de réception                 |
| - Procès-Verbal de Réception avec ou sans réserves et PV de levée des réserves                     |
| - Certificats de conformité, garanties constructeurs et polices d'assurance décennale              |
| -------------------------------------------------------------------------------------------------- |
| VOLUME 2 : PLANS D'EXÉCUTION CONFORMES (« AS-BUILT ») & RÉCOLEMENT GÉORÉFÉRENCÉ                   |
| - Plans de récolement géoréférencés en coordonnées nationales RGF93 / CC43 / NGF-IGN69            |
| - Nivellement X, Y, Z de la voirie, profils en travers réels, dévers et points bas                 |
| - Récolement de classe A des canalisations d'assainissement (cotes aux fils d'eau et tampons)      |
| -------------------------------------------------------------------------------------------------- |
| VOLUME 3 : FICHES TECHNIQUES DES MATÉRIAUX & AVIS TECHNIQUES                                      |
| - Marquage CE et fiches NF des bordures, bétons C20/25, tuyaux PVC CR4, émulsions et enrobés       |
| - Fiches de Données de Sécurité (FDS) et fiches d'impact environnemental (FDES / Base INIES)        |
| -------------------------------------------------------------------------------------------------- |
| VOLUME 4 : CONTRÔLES QUALITÉ, RAPPORTS D'ESSAIS & INSPECTIONS TÉLÉVISÉES (ITV)                     |
| - Rapports de compactage (essais de plaque Westergaard, Dynaplaque, pénétromètre dynamique)       |
| - Résultats d'essais de formulation et d'extraction de bitume des enrobés                          |
| - Rapports d'inspection vidéo ITV des réseaux d'assainissement (NF EN 13508-2) et épreuves d'eau  |
| -------------------------------------------------------------------------------------------------- |
| VOLUME 5 : NOTICES D'ENTRETIEN, DE MAINTENANCE & DIUO                                              |
| - Prescriptions de curage périodique des caniveaux, dessableurs et bassins d'orage                 |
| - Fiches d'intervention ultérieure transmises au coordonnateur SPS pour constitution du DIUO       |
+----------------------------------------------------------------------------------------------------+
```

---

## 2. Modalités Contractuelles de Remise du DOE

- **Délais :** Selon le CCAG Travaux et le standard interne, le DOE doit être remis par le titulaire au plus tard lors de la demande de réception, ou dans un délai maximal de **1 mois** suivant la notification de la décision de réception.
- **Sanctions financières en cas de retard :**
  - Blocage du paiement du solde du marché (Décompte Général et Définitif - DGD).
  - Impossibilité de libérer la caution bancaire se substituant à la **retenue de garantie de 5%**.
  - Application de pénalités journalières spécifiques prévues au CCAP pour retard de remise du DOE.

---

## 3. Confrontation avec l'État de l'Art 2026 : La Révolution BIM Infra et Trackdéchets

```
+---------------------------------------------------------------------------------------------------------------------------------+
|                                                  TRANSITION NUMÉRIQUE ET INNOVATIONS DOE                                        |
+-----------------------------+------------------------------------+------------------------------------+-------------------------+
| DOMAINE D'EXPERTIS          | PRATIQUE CORPUS HISTORIQUE         | ÉTAT DE L'ART 2026 (DIGITAL/LÉGAL) | AVANTAGES IN-SITU       |
+-----------------------------+------------------------------------+------------------------------------+-------------------------+
| Format du DOE               | Classeurs papier + Clé USB / CD-ROM| Jumeau Numérique (Digital Twin)    | Données interopérables, |
|                             | Fichiers PDF et plans DWG 2D isolés| Modèle OpenBIM IFC 4.3 (ISO 19650) | mise à jour continue    |
+-----------------------------+------------------------------------+------------------------------------+-------------------------+
| Récolement Topographique    | Relevé géomètre ponctuel           | Relevé par drone LiDAR / GNSS RTK  | Tranchée ouverte levée  |
|                             | Risque de fouilles refermées       | Intégration directe PCRS / SIG     | sans surcoût destructif |
+-----------------------------+------------------------------------+------------------------------------+-------------------------+
| Traçabilité des Déchets     | Bordereaux de suivi papier (BSDD)  | Plateforme nationale Trackdéchets  | Zéro risque pénal,      |
|                             | Registre de chantier manuel        | Registre National RNDTS dématérial.| conformité Loi AGEC     |
+-----------------------------+------------------------------------+------------------------------------+-------------------------+
| Clôture Financière          | Échanges postaux papier du DGD     | Validation dématérialisée Chorus   | Règlement solde en <30j,|
|                             | Délais de règlement > 3 à 6 mois   | Notification horodatée sécurisée   | libération caution auto |
+-----------------------------+------------------------------------+------------------------------------+-------------------------+
```

---

## 4. Retours d'Expérience In-Situ : Clés de Succès pour la Clôture de Chantier

1. **Anticiper le récolement en tranchée ouverte :** Dès que les tuyaux PVC ou fourreaux Janolène sont posés sur le lit de sable, le chef de chantier doit procéder au relevé GNSS centimétrique avant remblayage. Tout récolement différé impose des sondages destructifs coûteux.
2. **La constitution continue du DOE :** Attendre la fin des travaux pour réclamer les fiches techniques aux fournisseurs et sous-traitants est la première cause de retard de DOE. La bonne pratique in-situ consiste à classer les fiches d'agrément matériaux dès la phase de validation préalable en bureau d'études.
3. **La gestion de l'Année de Parfait Achèvement (GPA) :** Pendant les 12 mois suivant la réception, le conducteur de travaux doit traiter immédiatement toute notification de désordre pour éviter la mise en jeu de la garantie décennale ou l'exécution des réparations aux frais et risques de l'entreprise.
"""

(RAPPORTS_DIR / '06_RECEPTION_DOE_ET_TRANSITION_NUMERIQUE_BIM_LEAN.md').write_text(report_06, encoding='utf-8')
print("Wrote 06_RECEPTION_DOE_ET_TRANSITION_NUMERIQUE_BIM_LEAN.md")

# -------------------------------------------------------------
# 07. MATRICE DE TRACABILITE DU CORPUS BTP
# -------------------------------------------------------------
with open(DATA_DIR / 'corpus_btp_inventory.json', 'r', encoding='utf-8') as f:
    inv_data = json.load(f)

matrice_md = f"""# MATRICE DE TRAÇABILITÉ DU CORPUS BTP (154 DOCUMENTS)

> **Emplacement du corpus :** `projects/btp-conduite-travaux/documents_sources/`  
> **Nombre total de documents sources :** {len(inv_data)}  
> **Intégrité cryptographique :** Hachages SHA-256 calculés pour chaque fichier  
> **Génération :** Septembre 2026  

---

## 1. Inventaire Unitaire Exhaustif par Sous-Dossier

"""

by_sub = {}
for item in inv_data:
    sub = item['target_subfolder']
    if sub not in by_sub:
        by_sub[sub] = []
    by_sub[sub].append(item)

for sub in sorted(by_sub.keys()):
    files = by_sub[sub]
    matrice_md += f"\n### Sous-dossier : `{sub}` ({len(files)} fichiers)\n\n"
    matrice_md += "| Nom du Fichier | Type | Taille | Hachage SHA-256 (Intégrité) | Chemin Relatif |\n"
    matrice_md += "|---|:---:|:---:|---|---|\n"
    for f in sorted(files, key=lambda x: x['filename']):
        matrice_md += f"| `{f['filename']}` | `{f['extension']}` | {f['size_kb']} KB | `{f['sha256'][:16]}...` | `{f['relative_path']}` |\n"

(PROJECT_DIR / 'MATRICE_TRACABILITE_CORPUS_BTP.md').write_text(matrice_md, encoding='utf-8')
print("Wrote MATRICE_TRACABILITE_CORPUS_BTP.md")

# -------------------------------------------------------------
# 08. INDEX SOURCES ET REFERENCES REGLEMENTAIRES
# -------------------------------------------------------------
index_sources = """# INDEX DES SOURCES, NORMES ET RÉFÉRENCES RÉGLEMENTAIRES

> **Périmètre :** Corpus de Conduite de Travaux, Génie Civil, VRD et Marchés Publics  
> **Actualisation :** Référentiels 2026  

---

## 1. Cadre Législatif et Réglementaire National

- **Code de la Commande Publique (CCP) :**
  - Articles L. 2111-1 à L. 2197-4 : Définition des besoins, passation, allotissement, exécution financière et résiliation.
  - Articles R. 2194-1 à R. 2194-10 : Modifications du marché en cours d'exécution (Avenants et Travaux Supplémentaires).
- **Cahier des Clauses Administratives Générales applicables aux marchés de travaux (CCAG-Travaux 2021) :**
  - Arrêté du 30 mars 2021 portant approbation du CCAG-Travaux (modifié 2023/2024).
  - Article 10 : Avances financières et acomptes mensuels.
  - Article 19 : Pénalités de retard et plafonnement à 10% HT.
  - Article 20.4 : Clauses environnementales, SOGED, SOPAQ et valorisation des déchets.
  - Article 41 : Opérations préalables à la réception et réception des ouvrages.
  - Article 44 : Documents fournis après exécution (Dossier des Ouvrages Exécutés - DOE).
  - Article 55 : Règlement des différends et mémoires de réclamation.
- **Réglementation Anti-Endommagement des Réseaux (Décret DT-DICT) :**
  - Code de l'Environnement : Articles L. 554-1 à L. 554-5 et R. 554-1 à R. 554-39.
  - Arrêté du 15 février 2012 modifié pris en application du chapitre IV du titre V du livre V du Code de l'environnement.
  - Arrêté du 29 octobre 2018 relatif aux critères de compétences pour l'Autorisation d'Intervention à Proximité des Réseaux (AIPR).
- **Sécurité et Protection de la Santé (SPS) :**
  - Code du Travail : Articles L. 4531-1 à L. 4532-19 et R. 4532-1 à R. 4532-98 (Coordination SPS, PGC, PPSPS, DIUO).
- **Code de la Route et Voirie :**
  - Articles L. 411-1 à L. 411-7 et R. 411-1 à R. 411-28 (Pouvoirs de police de circulation et arrêtés temporaires).
  - Code Général des Collectivités Territoriales (CGCT) : Articles L. 2213-1 à L. 2213-6.1.
  - Instruction Interministérielle sur la Signalisation Routière (IISR) - Livre 1, 8ème partie : Signalisation temporaire des chantiers.
- **Législation Environnementale et Déchets :**
  - Loi n° 2020-105 du 10 février 2020 relative à la lutte contre le gaspillage et à l'économie circulaire (Loi AGEC).
  - Décret n° 2021-321 du 25 mars 2021 relatif à la traçabilité des déchets, terres excavées et sédiments (Plateforme nationale Trackdéchets & RNDTS).
  - Filière REP PMCB (Responsabilité Élargie du Producteur pour les Produits et Matériaux de Construction du Bâtiment).

---

## 2. Normes Techniques AFNOR et Eurocodes

- **Dimensionnement et Structures de Chaussées :**
  - **NF P 98-086 :** Dimensionnement structurel des chaussées routières - Application aux chaussées neuves et renforcements.
  - **NF EN 13108-1 à 7 :** Mélanges bitumineux - Spécifications des matériaux (BBSG, BBME, BBTM, Grave Bitume).
  - **NF P 98-150-1 :** Enrobés hydrocarbonés - Exécution des corps de chaussées, couches de liaison et de roulement.
  - **NF P 98-115 :** Assises de chaussées - Graves non traitées (GNT) - Définition, composition, classification.
  - **NF EN 1340 :** Bordures de trottoir en béton - Prescriptions et méthodes d'essais (Bordures P1, P2, I1, I2, T2, Caniveaux CC1, CS2).
- **Assainissement et Réseaux Enterrés :**
  - **NF EN 1610 :** Mise en œuvre et essais des branchements et canalisations d'assainissement.
  - **NF EN 13508-2 :** Évaluation des réseaux d'évacuation et d'assainissement à l'extérieur des bâtiments - Système de codage de l'inspection visuelle (ITV).
  - **NF EN 124-1 à 6 :** Dispositifs de couronnement et de fermeture pour les zones de circulation utilisées par les piétons et les véhicules (Classes C250, D400).
  - **NF EN 1401-1 :** Systèmes de canalisations en plastique pour les branchements et les collecteurs d'assainissement enterrés sans pression - Poly(chlorure de vinyle) non plastifié (PVC-U).
  - **NF P 98-331 :** Chaussées et dépendances - Tranchées : ouverture, remblayage, réfection.
- **Cahier des Clauses Techniques Générales (CCTG Travaux Publics) :**
  - **Fascicule 29 :** Exécution des terrassements.
  - **Fascicule 70 Titre I :** Réseaux d'assainissement (eaux usées et pluviales).
  - **Fascicule 70 Titre II :** Ouvrages de distribution d'eau potable.
  - **Fascicule 71 :** Fourniture et pose de conduites d'adduction et de distribution d'eau.

---

## 3. Guides Techniques Professionnels (CEREMA, SETRA, IDRRIM, OPPBTP)

- **Guides CEREMA / SETRA / LCPC :**
  - Guide des Terrassements Routiers (GTR 92 / 2000) - Réalisation des remblais et des couches de forme.
  - Manuel de Conception des Carrefours Giratoires Interurbains et Urbains (SETRA / CERTU).
  - Guide Technique : Conception et dimensionnement des structures de chaussées (SETRA/LCPC).
  - Guide d'application : Les Enrobés Tièdes (IDRRIM).
  - Guide Technique : Utilisation des agrégats d'enrobés dans les mélanges bitumineux (CEREMA).
- **Guides OPPBTP & Prévention :**
  - Manuel du Chef de Chantier : Signalisation temporaire des chantiers routiers (OPPBTP / FNTP).
  - Guide Pratique : Travaux à proximité des réseaux - Guide technique d'application de la réglementation anti-endommagement.
  - Guide de Prévention : Risque d'ensevelissement en tranchée et blindage des fouilles (OPPBTP).
"""

(PROJECT_DIR / 'INDEX_SOURCES_ET_REFERENCES_REGLEMENTAIRES.md').write_text(index_sources, encoding='utf-8')
print("Wrote INDEX_SOURCES_ET_REFERENCES_REGLEMENTAIRES.md")

# -------------------------------------------------------------
# 09. README DU PROJET BTP
# -------------------------------------------------------------
readme_btp = """# Module d'Expertise BTP : Conduite de Travaux, État de l'Art 2026 & Retours In-Situ

> **Dossier :** `projects/btp-conduite-travaux/`  
> **Périmètre :** Audit, Structuration, Traçabilité et Confrontation de 154 documents sources du BTP (Conducteur de Travaux & Chef de Chantier).  

---

## 🗂 Architecture du Projet

```
projects/btp-conduite-travaux/
├── README.md                                         <- Présentation du module et guide d'exploitation
├── index.html                                        <- Dashboard interactif (Visualisations, Tableaux, Simulateurs)
├── MATRICE_TRACABILITE_CORPUS_BTP.md                 <- Traçabilité unitaire complète des 154 documents
├── INDEX_SOURCES_ET_REFERENCES_REGLEMENTAIRES.md     <- Répertoire exhaustif des normes, lois et guides
├── data/
│   ├── corpus_btp_inventory.json                     <- Métadonnées complètes avec hachages SHA-256
│   ├── corpus_btp_inventory.csv                      <- Format tabulaire pour export SIG/BIM
│   ├── synthese_chantiers_et_prix.json               <- Chantiers audités et barèmes des sous-détails de prix
│   └── confrontation_theorie_etatdelart_insitu.json  <- Matrice de confrontation tripartite
├── rapports/
│   ├── 00_RAPPORT_SYNTHESE_ETAT_DE_L_ART_ET_IN_SITU.md  <- Rapport Maître Global
│   ├── 01_ANALYSE_MARCHES_DCE_ET_CADRE_JURIDIQUE.md
│   ├── 02_ETUDE_DE_PRIX_METHODES_ET_SOUS_DETAILS.md
│   ├── 03_TECHNIQUE_VOIRIE_RESEAUX_ET_TERRASSEMENT.md
│   ├── 04_REGLEMENTATION_ANTI_ENDOMMAGEMENT_DICT_AIPR_ET_SECURITE.md
│   ├── 05_PILOTAGE_IN_SITU_CR_CHANTIER_ALEAS_ET_GESTION_LITIGES.md
│   └── 06_RECEPTION_DOE_ET_TRANSITION_NUMERIQUE_BIM_LEAN.md
└── documents_sources/                                <- 154 Fichiers sources classés et sécurisés
    ├── 01_dce_marches_publics/
    │   ├── saint_nicolas_de_la_grave/
    │   ├── giratoire_barbazan/
    │   ├── lotissement_la_croix_pruniaux_aurouer/
    │   └── formulaires_marches/
    ├── 02_preparation_etude_prix_sdp/
    ├── 03_reglementation_dict_aipr_securite/
    ├── 04_suivi_execution_comptes_rendus/
    ├── 05_doe_reception_cloture/
    ├── 06_management_rh_formation/
    └── 07_plans_et_cartographie/
```

---

## 🚀 Consultation et Navigation

1. **Rapports Détaillés :** Tous les rapports d'analyse et de confrontation sont rédigés en Markdown structuré dans le dossier `rapports/`.
2. **Dashboard Interactif :** Ouvrez `index.html` dans votre navigateur ou via la prévisualisation du monorepo (`/preview/btp-conduite-travaux/index.html`) pour accéder :
   - Au comparateur dynamique Théorie vs État de l'Art 2026 vs In-Situ.
   - Au catalogue interactif des 28 Sous-Détails de Prix avec simulateur de marge et de déboursé sec.
   - À l'explorateur de documents avec recherche instantanée parmi les 154 fichiers.
   - Au lecteur intégré des 7 rapports de synthèse.
"""

(PROJECT_DIR / 'README.md').write_text(readme_btp, encoding='utf-8')
print("Wrote README.md")

print("All reports generated successfully!")
