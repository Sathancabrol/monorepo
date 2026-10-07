# RAPPORT THÉMATIQUE 02 : ÉTUDE DE PRIX, MÉTHODES ET SOUS-DÉTAILS (SDP)

> **Domaine :** Chiffrage, Déboursé Sec, Taux Horaires, Amortissement du Matériel et Coefficients de Frais Généraux  
> **Données analysées :** 28 Fiches de Sous-Détails de Prix (SDP), Bibliothèque Fournitures, Barèmes Engins et Main d'Œuvre  
> **Date de référence :** 2026  

---

## 1. Structure Mathématique du Prix de Vente dans le Corpus

L'ensemble des fiches d'étude de prix du corpus applique la formule canonique du génie civil :

$$\text{PV}_{\text{HT}} = \text{DS} \times K$$

avec :
- $\text{DS}$ (Déboursé Sec Unitaire) = $\text{MO} + \text{MAT} + \text{MATL} + \text{ST}$
  - $\text{MO}$ : Main d'œuvre directe d'exécution (Heures ouvriers $\times$ Taux horaire chargé THMO)
  - $\text{MAT}$ : Matériaux et fournitures livrés sur chantier (prix d'achat franco chantier)
  - $\text{MATL}$ : Matériel affecté à la tâche (Amortissement + Entretien/Réparations + Consommables GNR/Carburant)
  - $\text{ST}$ : Prestations sous-traitées éventuelles
- $K$ (Coefficient de Vente) appliqué dans le corpus : **$K = 1,250$** (soit 25% de majoration sur déboursé sec pour couvrir les Frais Généraux de siège $\approx 13\%$, les Frais de Chantier non affectés $\approx 5\%$ et les Bénéfices & Aléas $\approx 7\%$).

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
  - Manœuvre / Ouvrier TP : 155 € / jour (soit $\approx 22,14$ €/h sur base 7h).
  - Ouvrier Hautement Qualifié (OHQ) / Maçon : 180 à 270 € / jour (soit 25,71 à 38,57 €/h).
  - Chef de chantier : 275 € / jour (soit $\approx 39,29$ €/h).
- **Dans l'état de l'art 2026 (Grilles FNTP Occitanie actualisées) :**
  - Le **Taux Horaire Moyen Ouvrier (THMO)** réel comprend le salaire brut horaire, les charges sociales patronales (45-52%), les cotisations CNETP (congés payés + intempéries $\approx 19,7\%$), l'OPPBTP, la médecine du travail, ainsi que les Indemnités de Petits Déplacements (IPD : panier repas $10,50$ €, prime de trajet, prime de transport).
  - **THMO réel 2026 :** $38,00$ à $48,00$ €/h pour un ouvrier qualifié (Niveau III), et $58,00$ à $75,00$ €/h pour un chef de chantier (ETAM Niveau F/G). Les prix du corpus constituent des valeurs pédagogiques sous-estimant l'inflation salariale récente.

### 3.2. Parc Matériel et Engins (Fichier `Equipement 30-05.xlsx`)
- Pelle à chenilles 20,3 t (Volvo EC 200-D, 2021) : Coût journalier calculé = $336,57$ €/j $\rightarrow$ Coût majoré retenu = $350,00$ €/j.
- Pelle sur pneus 17,9 t (Volvo ECR48 C, 2009) : Coût journalier calculé = $310,47$ €/j $\rightarrow$ Coût majoré retenu = $320,00$ €/j.
- Petits matériels : Tronçonneuse à disque Stihl TS420 ($30$ €/j), plaque vibrante Mikasa 75 kg ($25$ €/j), fourgon double cabine Iveco Daily ($120$ €/j).

---

## 4. Confrontation In-Situ : Rendements Réels vs Rendements Théoriques

1. **Facteurs d'abattement urbain :** Les rendements théoriques de pose de bordures ($15$ ml/j en P2) supposent une tranchée ouverte continue sans obstacle. En milieu sous circulation (giratoire de Barbazan), les reprises d'alignement, les regards d'eaux pluviales et les accès riverains réduisent le rendement effectif à **$9-11$ ml/j** (-30%).
2. **Surconsommation de matériaux :** En application d'enrobés (BBSG 0/14), le tonnage théorique calculé sur une densité de $2,50$ t/m³ et une épaisseur constante de 6 cm est systématiquement dépassé de **$+5\%$ à $+10\%$** en raison des irrégularités du support raboté (déflachage) et du compactage. L'étude de prix terrain doit intégrer une perte de foisonnement et de matière.
3. **Formules de révision TP :** En période d'instabilité des cours pétroliers, l'application de la formule d'indexation $P = P_0 \times [0,15 + 0,85 \times (TP08 / TP08_0)]$ est la seule garantie pour préserver la marge nette de l'entreprise.
