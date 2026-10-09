# RAPPORT THÉMATIQUE 06 : RÉCEPTION, CLÔTURE, DOE ET TRANSITION NUMÉRIQUE (BIM / SIG / TRACKDÉCHETS)

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
