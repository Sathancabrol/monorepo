import json

def get_dqe_dataset():
    return [
        # PROJECT 1: GIRATOIRE RD906 ALÈS
        {
            "id": "dqe_01", "project_id": "projet_ales", "project_name": "Giratoire RD906 Alès",
            "lot": "Lot 1 : Terrassement & Déblais", "code": "1.1", "designation": "Décapage terre végétale ép. 20cm",
            "unite": "m²", "qte": 2400, "mo_u": 1.80, "mat_u": 0.00, "eq_u": 2.40, "st_u": 0.00,
            "statut": "Terminé", "k": 1.30
        },
        {
            "id": "dqe_02", "project_id": "projet_ales", "project_name": "Giratoire RD906 Alès",
            "lot": "Lot 1 : Terrassement & Déblais", "code": "1.2", "designation": "Déblais grande masse en pleine masse",
            "unite": "m³", "qte": 3800, "mo_u": 3.20, "mat_u": 0.00, "eq_u": 4.80, "st_u": 0.00,
            "statut": "Terminé", "k": 1.30
        },
        {
            "id": "dqe_03", "project_id": "projet_ales", "project_name": "Giratoire RD906 Alès",
            "lot": "Lot 1 : Terrassement & Déblais", "code": "1.3", "designation": "Traitement sol à la chaux vive 2%",
            "unite": "m³", "qte": 1200, "mo_u": 2.50, "mat_u": 8.20, "eq_u": 3.50, "st_u": 0.00,
            "statut": "Terminé", "k": 1.30
        },
        {
            "id": "dqe_04", "project_id": "projet_ales", "project_name": "Giratoire RD906 Alès",
            "lot": "Lot 1 : Terrassement & Déblais", "code": "1.4", "designation": "Évacuation terres en décharge ISDI",
            "unite": "m³", "qte": 2600, "mo_u": 1.20, "mat_u": 0.00, "eq_u": 6.50, "st_u": 4.50,
            "statut": "Terminé", "k": 1.30
        },
        {
            "id": "dqe_05", "project_id": "projet_ales", "project_name": "Giratoire RD906 Alès",
            "lot": "Lot 2 : Assainissement & EP", "code": "2.1", "designation": "Tranchée pour collecteur pluvial prof. 1.8m",
            "unite": "ml", "qte": 650, "mo_u": 14.50, "mat_u": 0.00, "eq_u": 18.20, "st_u": 0.00,
            "statut": "Terminé", "k": 1.30
        },
        {
            "id": "dqe_06", "project_id": "projet_ales", "project_name": "Giratoire RD906 Alès",
            "lot": "Lot 2 : Assainissement & EP", "code": "2.2", "designation": "Pose tuyau béton armé Ø400 135A",
            "unite": "ml", "qte": 650, "mo_u": 12.00, "mat_u": 38.50, "eq_u": 8.50, "st_u": 0.00,
            "statut": "Terminé", "k": 1.30
        },
        {
            "id": "dqe_07", "project_id": "projet_ales", "project_name": "Giratoire RD906 Alès",
            "lot": "Lot 2 : Assainissement & EP", "code": "2.3", "designation": "Regards de visite préfabriqués 1000x1000",
            "unite": "u", "qte": 14, "mo_u": 180.00, "mat_u": 340.00, "eq_u": 95.00, "st_u": 0.00,
            "statut": "Terminé", "k": 1.30
        },
        {
            "id": "dqe_08", "project_id": "projet_ales", "project_name": "Giratoire RD906 Alès",
            "lot": "Lot 2 : Assainissement & EP", "code": "2.4", "designation": "Avaloirs avec grilles concaves C250",
            "unite": "u", "qte": 22, "mo_u": 65.00, "mat_u": 160.00, "eq_u": 35.00, "st_u": 0.00,
            "statut": "Terminé", "k": 1.30
        },
        {
            "id": "dqe_09", "project_id": "projet_ales", "project_name": "Giratoire RD906 Alès",
            "lot": "Lot 3 : Voirie & Structure", "code": "3.1", "designation": "Fondation en GNT 0/31.5 ép. 25cm",
            "unite": "m²", "qte": 4200, "mo_u": 1.40, "mat_u": 9.80, "eq_u": 2.60, "st_u": 0.00,
            "statut": "Terminé", "k": 1.30
        },
        {
            "id": "dqe_10", "project_id": "projet_ales", "project_name": "Giratoire RD906 Alès",
            "lot": "Lot 3 : Voirie & Structure", "code": "3.2", "designation": "Grave Bitume GB 0/14 ép. 10cm",
            "unite": "m²", "qte": 4000, "mo_u": 2.10, "mat_u": 19.50, "eq_u": 3.80, "st_u": 0.00,
            "statut": "En cours", "k": 1.30
        },
        {
            "id": "dqe_11", "project_id": "projet_ales", "project_name": "Giratoire RD906 Alès",
            "lot": "Lot 3 : Voirie & Structure", "code": "3.3", "designation": "Enrobé roulement BBSG 0/10 ép. 6cm",
            "unite": "m²", "qte": 4000, "mo_u": 2.20, "mat_u": 14.80, "eq_u": 4.20, "st_u": 0.00,
            "statut": "À venir", "k": 1.30
        },
        {
            "id": "dqe_12", "project_id": "projet_ales", "project_name": "Giratoire RD906 Alès",
            "lot": "Lot 3 : Voirie & Structure", "code": "3.4", "designation": "Bordures béton type T2 sur semelle",
            "unite": "ml", "qte": 850, "mo_u": 11.50, "mat_u": 16.20, "eq_u": 2.80, "st_u": 0.00,
            "statut": "En cours", "k": 1.30
        },
        {
            "id": "dqe_13", "project_id": "projet_ales", "project_name": "Giratoire RD906 Alès",
            "lot": "Lot 3 : Voirie & Structure", "code": "3.5", "designation": "Caniveaux préfabriqués CC1",
            "unite": "ml", "qte": 850, "mo_u": 12.00, "mat_u": 18.50, "eq_u": 3.00, "st_u": 0.00,
            "statut": "En cours", "k": 1.30
        },
        {
            "id": "dqe_14", "project_id": "projet_ales", "project_name": "Giratoire RD906 Alès",
            "lot": "Lot 3 : Voirie & Structure", "code": "3.6", "designation": "Ilot central pavé / béton désactivé",
            "unite": "m²", "qte": 320, "mo_u": 28.00, "mat_u": 32.00, "eq_u": 6.00, "st_u": 0.00,
            "statut": "À venir", "k": 1.30
        },
        {
            "id": "dqe_15", "project_id": "projet_ales", "project_name": "Giratoire RD906 Alès",
            "lot": "Lot 4 : Réseaux Secs", "code": "4.1", "designation": "Fourreaux TPC Ø110 sous trottoir",
            "unite": "ml", "qte": 1100, "mo_u": 4.20, "mat_u": 3.90, "eq_u": 2.80, "st_u": 0.00,
            "statut": "Terminé", "k": 1.30
        },
        {
            "id": "dqe_16", "project_id": "projet_ales", "project_name": "Giratoire RD906 Alès",
            "lot": "Lot 4 : Réseaux Secs", "code": "4.2", "designation": "Massifs béton et candélabres LED 8m",
            "unite": "u", "qte": 12, "mo_u": 120.00, "mat_u": 650.00, "eq_u": 80.00, "st_u": 150.00,
            "statut": "À venir", "k": 1.30
        },

        # PROJECT 2: ZAC LITTORAL SÈTE
        {
            "id": "dqe_17", "project_id": "projet_sete", "project_name": "ZAC Littoral Sète",
            "lot": "Lot 1 : Terrassement & Déblais", "code": "1.1", "designation": "Terrassement en tranchée sous nappe rabattue",
            "unite": "m³", "qte": 4500, "mo_u": 6.50, "mat_u": 0.00, "eq_u": 12.80, "st_u": 4.20,
            "statut": "En cours", "k": 1.32
        },
        {
            "id": "dqe_18", "project_id": "projet_sete", "project_name": "ZAC Littoral Sète",
            "lot": "Lot 2 : Assainissement & EP", "code": "2.1", "designation": "Pose collecteur fonte DN400 avec blindage SBH",
            "unite": "ml", "qte": 1200, "mo_u": 24.00, "mat_u": 115.00, "eq_u": 22.00, "st_u": 0.00,
            "statut": "En cours", "k": 1.32
        },
        {
            "id": "dqe_19", "project_id": "projet_sete", "project_name": "ZAC Littoral Sète",
            "lot": "Lot 2 : Assainissement & EP", "code": "2.2", "designation": "Poste de refoulement préfabriqué 2 pompes",
            "unite": "u", "qte": 2, "mo_u": 1200.00, "mat_u": 18500.00, "eq_u": 950.00, "st_u": 2400.00,
            "statut": "À venir", "k": 1.32
        },
        {
            "id": "dqe_20", "project_id": "projet_sete", "project_name": "ZAC Littoral Sète",
            "lot": "Lot 3 : Voirie & Structure", "code": "3.1", "designation": "Plateforme portante PF3 GNT 0/31.5",
            "unite": "m²", "qte": 6500, "mo_u": 1.50, "mat_u": 11.20, "eq_u": 2.80, "st_u": 0.00,
            "statut": "À venir", "k": 1.32
        },

        # PROJECT 3: CENTRE ANCIEN PÉZENAS
        {
            "id": "dqe_21", "project_id": "projet_pezenas", "project_name": "Centre Ancien Pézenas",
            "lot": "Lot 1 : Terrassement & Déblais", "code": "1.1", "designation": "Terrassement manuel & mini-pelle en ruelle étroite",
            "unite": "m³", "qte": 850, "mo_u": 35.00, "mat_u": 0.00, "eq_u": 18.00, "st_u": 0.00,
            "statut": "Terminé", "k": 1.35
        },
        {
            "id": "dqe_22", "project_id": "projet_pezenas", "project_name": "Centre Ancien Pézenas",
            "lot": "Lot 2 : Assainissement & EP", "code": "2.1", "designation": "Remplacement réseau unitaire par PVC CR8 Ø250",
            "unite": "ml", "qte": 480, "mo_u": 22.00, "mat_u": 28.50, "eq_u": 12.00, "st_u": 0.00,
            "statut": "Terminé", "k": 1.35
        },
        {
            "id": "dqe_23", "project_id": "projet_pezenas", "project_name": "Centre Ancien Pézenas",
            "lot": "Lot 3 : Voirie & Structure", "code": "3.1", "designation": "Pavage en pierre calcaire locale avec joint mortier",
            "unite": "m²", "qte": 1400, "mo_u": 42.00, "mat_u": 48.00, "eq_u": 5.00, "st_u": 0.00,
            "statut": "En cours", "k": 1.35
        },

        # PROJECT 4: VOIE VERTE MONTPELLIER
        {
            "id": "dqe_24", "project_id": "projet_montpellier", "project_name": "Voie Verte Montpellier",
            "lot": "Lot 1 : Terrassement & Déblais", "code": "1.1", "designation": "Décapage linéaire & reprofilage de piste",
            "unite": "m²", "qte": 5200, "mo_u": 1.20, "mat_u": 0.00, "eq_u": 1.80, "st_u": 0.00,
            "statut": "Terminé", "k": 1.28
        },
        {
            "id": "dqe_25", "project_id": "projet_montpellier", "project_name": "Voie Verte Montpellier",
            "lot": "Lot 3 : Voirie & Structure", "code": "3.1", "designation": "Enrobé tiède bas carbone couleur ocre ép. 5cm",
            "unite": "m²", "qte": 4800, "mo_u": 1.90, "mat_u": 16.50, "eq_u": 3.40, "st_u": 0.00,
            "statut": "En cours", "k": 1.28
        }
    ]

print("DQE dataset generator loaded. Total items:", len(get_dqe_dataset()))
