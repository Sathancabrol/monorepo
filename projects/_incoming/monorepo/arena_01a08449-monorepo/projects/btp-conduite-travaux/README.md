# Module d'Expertise BTP : Conduite de Travaux, État de l'Art 2026 & Retours In-Situ

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
