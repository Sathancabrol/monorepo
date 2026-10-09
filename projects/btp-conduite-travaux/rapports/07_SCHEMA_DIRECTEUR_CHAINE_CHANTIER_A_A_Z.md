# RAPPORT DIRECTEUR 07 : SCHÉMAS ET FORMULES DE LA CHAÎNE COMPLÈTE D'UN CHANTIER DE A À Z

> **Domaine :** Ingénierie Travaux Publics, Conduite de Travaux & Modélisation Complète des Processus  
> **Objectif :** Cartographie exhaustive, formelle et mathématique de chaque étape d'une opération BTP (du sourcing à la clôture DGD/DOE), avec interfaçage bidirectionnel IA / Humain.  
> **Date de référence :** Septembre 2026  

---

## 1. Vue d'Ensemble Synoptique du Macro-Processus (A à Z)

Le cycle de vie complet d'un projet de Travaux Publics s'articule en **7 grandes phases séquentielles et interconnectées**, chacune régie par des contraintes juridiques, techniques, économiques et environnementales strictes :

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                       MACRO-FLUX OPÉRATIONNEL D'UNE OPÉRATION BTP / GÉNIE CIVIL                                       │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                                    │
                                                                    ▼
  ┌─────────────────────────────────┐       ┌─────────────────────────────────┐       ┌─────────────────────────────────┐
  │  PHASE 0 : CONSULTATION & DCE   │ ────> │   PHASE 1 : ÉTUDE DE PRIX       │ ────> │   PHASE 2 : PRÉPARATION & DICT  │
  │ • Avis de Marché (AAMP/BOAMP)   │       │ • Déboursé Sec (DS = MO+MAT...) │       │ • Guichet Unique (DT-DICT)      │
  │ • Analyse RC, CCTP, CCAP, DQE   │       │ • Coeff. K (Frais Généraux+BA)  │       │ • Cerfa 14023 (Voirie) & 14024  │
  │ • Candidature DC1, DC2, DC4     │       │ • Indexation TP01/TP08          │       │ • PGC SPS, PPSPS, PAE/SOGED     │
  │ • Mémoire Technique (SOPAQ...)  │       │ • Bilan Carbone (€/tCO2eq)      │       │ • Plan Installation Chantier    │
  └─────────────────────────────────┘       └─────────────────────────────────┘       └─────────────────────────────────┘
                                                                                                │
                                                                                                ▼
  ┌─────────────────────────────────┐       ┌─────────────────────────────────┐       ┌─────────────────────────────────┐
  │  PHASE 5 : RÉCEPTION & DOE/DGD  │ <──── │   PHASE 4 : PILOTAGE & ALÉAS    │ <──── │   PHASE 3 : EXÉCUTION & CAPTEURS│
  │ • Visite contradictoire OPR     │       │ • Réunions & Comptes-Rendus CR  │       │ • OS de Démarrage               │
  │ • PV de Réception (+/- réserves)│       │ • Fiches de Non-Conformité      │       │ • Signalisation temporaire IISR │
  │ • Standard DOE SI 022 + DIUO    │       │ • Travaux Supplémentaires (TS)  │       │ • Relevé GNSS & Nivellement 3D  │
  │ • ITV Caméra & Épreuves d'eau   │       │ • Situations Mensuelles (DP)    │       │ • Télémétrie Thermique (>130°C) │
  │ • Décompte DGD sur Chorus Pro   │       │ • Mémoire Réclamation Art. 55   │       │ • Compactage Dynaplaque (EV2)   │
  └─────────────────────────────────┘       └─────────────────────────────────┘       └─────────────────────────────────┘
```

---

## 2. Phase 0 : Consultation, Analyse du DCE & Candidature

### 2.1. Organigramme Décisionnel de Réponse à Appel d'Offres
```
   [ Réception Avis de Marché / DCE ]
                  │
                  ▼
   [ Analyse des Critères de Choix ] ─── Critères Typiques : 60% Prix / 40% Valeur Technique (Mémoire)
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
[ Analyse Risques CCAP ]  [ Analyse Exigences CCTP ]
- Pénalités (Plafond 10%) - Matériaux exigés (NF/CE)
- Clauses Env. Art. 20.4  - Tolérances de nivellement
- Délais et Intempéries   - Classes de réseaux (A/B/C)
        │                   │
        └─────────┬─────────┘
                  ▼
   [ Décision GO / NO-GO ] ───> [ Génération Dossier Candidature : DC1 + DC2 + DC4 + Mémoire Technique ]
```

### 2.2. Formules et Règles de Candidature
- **Plafonnement des pénalités (Art. 19.2.2 CCAG 2021) :**
  $$P_{\text{max}} = 0,10 \times \text{Montant Total HT du Marché}$$
- **Avance forfaitaire obligatoire pour PME (Art. 10.1 CCAG 2021) :**
  $$A = 0,20 \times \text{Montant Total TTC du Marché}$$

---

## 3. Phase 1 : Étude de Prix, Sous-Détails (SDP) & Déboursés Secs

### 3.1. Structure Formelle du Prix de Vente Hors Taxes
Le prix unitaire hors taxes de chaque bordereau est calculé par la cascade mathématique :

$$\text{PV}_{\text{HT}} = \text{DS} \times K$$

```
                                    ┌─────────────────────────────────────────┐
                                    │       DÉBOURSÉ SEC UNITAIRE (DS)        │
                                    └────────────────────┬────────────────────┘
                                                         │
               ┌───────────────────────┬─────────────────┴─────────────────┬───────────────────────┐
               ▼                       ▼                                   ▼                       ▼
     ┌───────────────────┐   ┌───────────────────┐               ┌───────────────────┐   ┌───────────────────┐
     │  MAIN D'ŒUVRE MO  │   │  FOURNITURES MAT  │               │   MATÉRIEL MATL   │   │  SOUS-TRAITANCE   │
     ├───────────────────┤   ├───────────────────┤               ├───────────────────┤   ├───────────────────┤
     │ Heures Productives│   │ Prix Achat Franco │               │ Amortissement     │   │ Prestation externe│
     │     × THMO        │   │ + Pertes (3 à 8%) │               │ + Entretien + GNR │   │ déboursée brute   │
     └───────────────────┘   └───────────────────┘               └───────────────────┘   └───────────────────┘
```

### 3.2. Formule du Taux Horaire Moyen Ouvrier (THMO)
$$\text{THMO} = \frac{\sum_{i=1}^{n} \left[ S_i \times (1 + C_{\text{pat}}) + \text{CNETP} + \text{OPPBTP} + \text{IPD}_i \right]}{H_{\text{prod}}}$$

Où :
- $S_i$ : Salaire brut de base de l'ouvrier $i$.
- $C_{\text{pat}}$ : Taux de charges sociales patronales ($45\%$ à $52\%$).
- $\text{CNETP}$ : Caisse Nationale des Congés Payés et Intempéries ($\approx 19,7\%$).
- $\text{IPD}_i$ : Indemnités de Petits Déplacements journalières (Panier repas $10,50$ € + Trajet + Transport).
- $H_{\text{prod}}$ : Heures réellement productives annuelles (environ $1540$ à $1600$ heures).

### 3.3. Formule du Coefficient de Vente $K$
$$K = \frac{1 + \text{FG}_{\text{chantier}}}{1 - (\text{FG}_{\text{siege}} + \text{BA} + \text{FF})}$$

Exemple appliqué dans le corpus Barbazan :
- $\text{FG}_{\text{chantier}} = 0,05$ ($5\%$)
- $\text{FG}_{\text{siege}} = 0,13$ ($13\%$)
- $\text{BA}$ (Bénéfices & Aléas) = $0,06$ ($6\%$)
- $\text{FF}$ (Frais Financiers) = $0,01$ ($1\%$)
$$K = \frac{1 + 0,05}{1 - (0,13 + 0,06 + 0,01)} = \frac{1,05}{0,80} = 1,3125 \quad (\text{Fixé à } 1,250 \text{ dans les barèmes simplifiés de cours})$$

### 3.4. Formule de Révision et d'Actualisation des Prix TP
$$P = P_0 \times \left[ 0,15 + 0,85 \times \frac{\text{TP08}}{\text{TP08}_0} \right]$$
Où $\text{TP08}$ est l'index officiel INSEE des travaux routiers et enrobés, et $\text{TP08}_0$ l'index au mois zéro du marché.

---

## 4. Phase 2 : Préparation de Chantier, DT-DICT & Sécurité

### 4.1. Chaîne Réglementaire Anti-Endommagement
```
   [ MAÎTRE D'OUVRAGE ]                         [ EXPLOITANTS DE RÉSEAUX ]                     [ ENTREPRISE ADJUDICATAIRE ]
            │                                                │                                               │
            ├────── Émet la DT (Guichet Unique) ───────────>│                                               │
            │                                                │                                               │
            │<───── Récépissés DT + Plans Réseaux ──────────┤                                               │
            │                                                                                                │
            ├────── Transmission DCE + Récépissés DT ───────────────────────────────────────────────────────>│
                                                                                                             │
                                                             │<───── Émet la DICT (Cerfa 14434) ─────────────┤
                                                             │                                               │
                                                             ├────── Récépissés DICT + Classes A/B/C ───────>│
                                                                                                             │
                                                                                                             ▼
                                                                                               [ ANALYSE DES CLASSES ]
                                                                                               - Classe A (<=40cm) : Mécanique
                                                                                               - Classe B (<=1.5m) : Manuel
                                                                                               - Classe C (>1.5m)  : Aspiratrice
```

### 4.2. Autorisations Administratives Indispensables
1. **Cerfa 14023*01 :** Permission de voirie (droit d'occuper le domaine public routier).
2. **Cerfa 14024*01 :** Arrêté de police de la circulation (déviation, alternat, limitations 70/50 km/h).

---

## 5. Phase 3 & 4 : Exécution, Télémétrie Temps Réel & Contrôles

### 5.1. Schéma de Pose et Contrôle Géotechnique des Chaussées
```
   [ SOL SUPPORT PST ] ───> Essai de plaque EV2 >= 50 MPa  (Si < 50 MPa : Purge ou Traitement Chaux 1.5%)
            │
            ▼
   [ COUCHE FORME GNT 0/20 ] ───> Nivellement 3D GNSS (+/- 10 mm) + Contrôle Dynaplaque (Ratio EV2/EV1 < 2.0)
            │
            ▼
   [ COUCHE FONDATION GB3 (12cm) ] ───> Contrôle Température Livraison (> 130°C) + Prélèvement Teneur Liant (4.5%)
            │
            ▼
   [ ROULEMENT BBSG 0/14 (6cm) ] ───> Application finisseur + Compactage tandem + Contrôle carottage (Compacité >= 93%)
```

### 5.2. Formules Géotechniques et Hydrauliques
- **Module sous plaque Westergaard ($EV_2$) :**
  $$EV_2 = \frac{1,5 \times p \times R}{\Delta z}$$
  Où $p = 0,5\text{ MPa}$, $R = 300\text{ mm}$, et $\Delta z$ est l'enfoncement sous le second cycle de chargement.
- **Règle d'Acceptation de Plateforme (Classe AR2) :**
  $$EV_2 \ge 50\text{ MPa} \quad \text{ET} \quad \frac{EV_2}{EV_1} \le 2,0$$
- **Formule de Manning-Strickler pour Cunettes et Caniveaux :**
  $$Q = K_s \times S \times R_h^{2/3} \times I^{1/2}$$
  Où $K_s = 70\text{ m}^{1/3}/\text{s}$ (béton lisse), $S$ est la section mouillée, $R_h$ le rayon hydraulique et $I$ la pente longitudinale.

---

## 6. Phase 5 : Pilotage In-Situ, Gestion des Aléas & Litiges

### 6.1. Arbre de Résolution d'un Litige (Ex. Non-Conformité Enrobé Barbazan)
```
   [ Découverte Non-Conformité Laboratoire (Teneur Liant 5.3% vs 4.5%) ]
                                  │
                                  ▼
   [ Notification Formelle Immédiate au MOE + Centrale d'Enrobés ]
                                  │
                                  ▼
   [ Évaluation Financière des Options Techniques ]
         │
         ├────────────────────────────────────────┬────────────────────────────────────────┐
         ▼                                        ▼                                        ▼
   [ OPTION A : Démolition Totale ]         [ OPTION B : Réfection Couche Sup ]      [ OPTION C : Réfaction & Garantie ]
   - Coût : 202 783,93 € HT                - Coût : 95 000,00 € HT                 - Réfaction : -25% sur prix GB3
   - Risque : Arrêt 4 semaines              - Risque : Liaison d'interface          - Garantie : 15 ans avec suivi
```

### 6.2. Procédure Contractuelle de Réclamation (Art. 55 CCAG 2021)
1. **Émission d'une lettre de réserves** sous **15 jours** après survenance du fait générateur (ex. retard concessionnaire Enedis).
2. **Notification du Mémoire de Réclamation** sous **30 jours** après notification de la décision contestée ou du DGD :
   $$\text{Indemnité Réclamée} = \text{Frais Fixes Chantier Immo} + \text{Surcoûts Matériel} + \text{Pertes de Rendement}$$

---

## 7. Phase 6 : Clôture, Réception, Standard DOE & DGD

### 7.1. Structure Obligatoire du DOE (Standard Aéroports de Lyon SI 022)
- **Volume 1 :** Procès-verbaux de réception, arrêtés, actes de sous-traitance.
- **Volume 2 :** Plans d'exécution conformes (« As-Built ») et récolement géoréférencé classe A (X, Y, Z).
- **Volume 3 :** Fiches techniques matériaux, certificats NF/CE, avis techniques.
- **Volume 4 :** Rapports d'autocontrôle, essais de plaque, rapports d'inspection vidéo ITV des canalisations (NF EN 13508-2).
- **Volume 5 :** Notices de maintenance et Dossier d'Intervention Ultérieure sur l'Ouvrage (DIUO).

### 7.2. Clôture Financière et Libération des Garanties
- **Décompte Général et Définitif (DGD) :** Établi par le MOE, notifié par le MOA et signé sur **Chorus Pro**.
- **Libération de la retenue de garantie (5%) :** Automatique à l'expiration du délai de garantie de parfait achèvement (1 an) si toutes les réserves sont levées.
