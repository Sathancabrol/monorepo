import json

def get_dqe_dataset():
    items = [
        # PROJECT 1: GIRATOIRE RD906 ALÈS (7 ITEMS)
        {
            "id": "dqe_01", "project_id": "projet_ales", "project_name": "Giratoire RD906 Alès",
            "lot": "Lot 1 : Terrassement", "code": "1.1", "code_prix": "PRIX 1.1", "designation": "Décapage terre végétale ép. 20cm",
            "unite": "m²", "quantite": 2400, "mo_u": 1.80, "mat_u": 0.00, "eq_u": 2.40, "st_u": 0.00, "k": 1.35
        },
        {
            "id": "dqe_02", "project_id": "projet_ales", "project_name": "Giratoire RD906 Alès",
            "lot": "Lot 1 : Terrassement", "code": "1.2", "code_prix": "PRIX 1.2", "designation": "Déblais grande masse en pleine masse",
            "unite": "m³", "quantite": 3800, "mo_u": 3.20, "mat_u": 0.00, "eq_u": 4.80, "st_u": 0.00, "k": 1.35
        },
        {
            "id": "dqe_03", "project_id": "projet_ales", "project_name": "Giratoire RD906 Alès",
            "lot": "Lot 1 : Terrassement", "code": "1.3", "code_prix": "PRIX 1.3", "designation": "Traitement sol à la chaux vive 2%",
            "unite": "m³", "quantite": 1200, "mo_u": 2.50, "mat_u": 8.20, "eq_u": 3.50, "st_u": 0.00, "k": 1.35
        },
        {
            "id": "dqe_04", "project_id": "projet_ales", "project_name": "Giratoire RD906 Alès",
            "lot": "Lot 2 : Assainissement", "code": "2.1", "code_prix": "PRIX 2.1", "designation": "Tranchée pour collecteur pluvial prof. 1.8m",
            "unite": "ml", "quantite": 650, "mo_u": 14.50, "mat_u": 0.00, "eq_u": 18.20, "st_u": 0.00, "k": 1.35
        },
        {
            "id": "dqe_05", "project_id": "projet_ales", "project_name": "Giratoire RD906 Alès",
            "lot": "Lot 2 : Assainissement", "code": "2.2", "code_prix": "PRIX 2.2", "designation": "Pose tuyau béton armé Ø400 135A",
            "unite": "ml", "quantite": 650, "mo_u": 12.00, "mat_u": 38.50, "eq_u": 8.50, "st_u": 0.00, "k": 1.35
        },
        {
            "id": "dqe_06", "project_id": "projet_ales", "project_name": "Giratoire RD906 Alès",
            "lot": "Lot 3 : Voirie", "code": "3.1", "code_prix": "PRIX 3.1", "designation": "Couche de fondation GNT 0/31.5 ép. 25cm",
            "unite": "m²", "quantite": 4200, "mo_u": 1.80, "mat_u": 8.50, "eq_u": 2.20, "st_u": 0.00, "k": 1.35
        },
        {
            "id": "dqe_07", "project_id": "projet_ales", "project_name": "Giratoire RD906 Alès",
            "lot": "Lot 3 : Voirie", "code": "3.2", "code_prix": "PRIX 3.2", "designation": "Bordures béton T2 sur semelle C25/30",
            "unite": "ml", "quantite": 850, "mo_u": 14.00, "mat_u": 12.50, "eq_u": 3.50, "st_u": 0.00, "k": 1.35
        },

        # PROJECT 2: ZAC LITTORAL SÈTE (7 ITEMS)
        {
            "id": "dqe_08", "project_id": "projet_sete", "project_name": "ZAC Littoral Sète",
            "lot": "Lot 1 : Terrassement", "code": "1.1", "code_prix": "PRIX 1.1", "designation": "Terrassement tranchée profonde sous nappe 3.2m",
            "unite": "m³", "quantite": 5200, "mo_u": 6.50, "mat_u": 2.00, "eq_u": 9.50, "st_u": 0.00, "k": 1.35
        },
        {
            "id": "dqe_09", "project_id": "projet_sete", "project_name": "ZAC Littoral Sète",
            "lot": "Lot 1 : Terrassement", "code": "1.2", "code_prix": "PRIX 1.2", "designation": "Blindage caisson lourd continu R4534",
            "unite": "m²", "quantite": 1800, "mo_u": 8.00, "mat_u": 15.00, "eq_u": 5.00, "st_u": 0.00, "k": 1.35
        },
        {
            "id": "dqe_10", "project_id": "projet_sete", "project_name": "ZAC Littoral Sète",
            "lot": "Lot 2 : Assainissement", "code": "2.1", "code_prix": "PRIX 2.1", "designation": "Pose collecteur fonte ductile DN400",
            "unite": "ml", "quantite": 850, "mo_u": 24.00, "mat_u": 115.00, "eq_u": 18.00, "st_u": 0.00, "k": 1.35
        },
        {
            "id": "dqe_11", "project_id": "projet_sete", "project_name": "ZAC Littoral Sète",
            "lot": "Lot 2 : Assainissement", "code": "2.2", "code_prix": "PRIX 2.2", "designation": "Poste de refoulement EU béton armé 22 kW",
            "unite": "u", "quantite": 1, "mo_u": 8500.00, "mat_u": 42000.00, "eq_u": 4500.00, "st_u": 0.00, "k": 1.35
        },
        {
            "id": "dqe_12", "project_id": "projet_sete", "project_name": "ZAC Littoral Sète",
            "lot": "Lot 4 : Réseaux Secs", "code": "4.1", "code_prix": "PRIX 4.1", "designation": "Fourreaux TPC Ø110 Fibre & Télécom",
            "unite": "ml", "quantite": 1400, "mo_u": 4.50, "mat_u": 3.80, "eq_u": 1.50, "st_u": 0.00, "k": 1.35
        },
        {
            "id": "dqe_13", "project_id": "projet_sete", "project_name": "ZAC Littoral Sète",
            "lot": "Lot 4 : Réseaux Secs", "code": "4.2", "code_prix": "PRIX 4.2", "designation": "Câblage HTA 20kV Enedis sous gaine",
            "unite": "ml", "quantite": 600, "mo_u": 8.50, "mat_u": 28.00, "eq_u": 2.50, "st_u": 0.00, "k": 1.35
        },
        {
            "id": "dqe_14", "project_id": "projet_sete", "project_name": "ZAC Littoral Sète",
            "lot": "Lot 3 : Voirie", "code": "3.1", "code_prix": "PRIX 3.1", "designation": "Structure chaussée lourde GB 0/14 (12cm)",
            "unite": "m²", "quantite": 3200, "mo_u": 2.80, "mat_u": 14.50, "eq_u": 3.20, "st_u": 0.00, "k": 1.35
        },

        # PROJECT 3: CENTRE ANCIEN PÉZENAS (7 ITEMS)
        {
            "id": "dqe_15", "project_id": "projet_pezenas", "project_name": "Centre Ancien Pézenas",
            "lot": "Lot 1 : Terrassement", "code": "1.1", "code_prix": "PRIX 1.1", "designation": "Dépose manuelle soignée des pavés anciens",
            "unite": "m²", "quantite": 850, "mo_u": 18.00, "mat_u": 0.00, "eq_u": 2.00, "st_u": 0.00, "k": 1.35
        },
        {
            "id": "dqe_16", "project_id": "projet_pezenas", "project_name": "Centre Ancien Pézenas",
            "lot": "Lot 1 : Terrassement", "code": "1.2", "code_prix": "PRIX 1.2", "designation": "Micro-terrassement par aspiration en ruelle",
            "unite": "m³", "quantite": 320, "mo_u": 22.00, "mat_u": 0.00, "eq_u": 35.00, "st_u": 0.00, "k": 1.35
        },
        {
            "id": "dqe_17", "project_id": "projet_pezenas", "project_name": "Centre Ancien Pézenas",
            "lot": "Lot 2 : Assainissement", "code": "2.1", "code_prix": "PRIX 2.1", "designation": "Renouvellement conduite AEP fonte DN150",
            "unite": "ml", "quantite": 320, "mo_u": 28.00, "mat_u": 48.00, "eq_u": 12.00, "st_u": 0.00, "k": 1.35
        },
        {
            "id": "dqe_18", "project_id": "projet_pezenas", "project_name": "Centre Ancien Pézenas",
            "lot": "Lot 2 : Assainissement", "code": "2.2", "code_prix": "PRIX 2.2", "designation": "Branchements particuliers plomb/fonte",
            "unite": "u", "quantite": 22, "mo_u": 240.00, "mat_u": 180.00, "eq_u": 60.00, "st_u": 0.00, "k": 1.35
        },
        {
            "id": "dqe_19", "project_id": "projet_pezenas", "project_name": "Centre Ancien Pézenas",
            "lot": "Lot 4 : Réseaux Secs", "code": "4.1", "code_prix": "PRIX 4.1", "designation": "Fourreaux éclairage et télécom sous pavage",
            "unite": "ml", "quantite": 450, "mo_u": 8.00, "mat_u": 6.50, "eq_u": 2.00, "st_u": 0.00, "k": 1.35
        },
        {
            "id": "dqe_20", "project_id": "projet_pezenas", "project_name": "Centre Ancien Pézenas",
            "lot": "Lot 3 : Voirie", "code": "3.1", "code_prix": "PRIX 3.1", "designation": "Repose pavés granit avec mortier résine",
            "unite": "m²", "quantite": 850, "mo_u": 42.00, "mat_u": 18.00, "eq_u": 4.00, "st_u": 0.00, "k": 1.35
        },
        {
            "id": "dqe_21", "project_id": "projet_pezenas", "project_name": "Centre Ancien Pézenas",
            "lot": "Lot 4 : Réseaux Secs", "code": "4.2", "code_prix": "PRIX 4.2", "designation": "Lanternes murales LED style ancien",
            "unite": "u", "quantite": 14, "mo_u": 180.00, "mat_u": 650.00, "eq_u": 40.00, "st_u": 0.00, "k": 1.35
        },

        # PROJECT 4: VOIE VERTE MONTPELLIER (7 ITEMS)
        {
            "id": "dqe_22", "project_id": "projet_montpellier", "project_name": "Voie Verte Montpellier",
            "lot": "Lot 1 : Terrassement", "code": "1.1", "code_prix": "PRIX 1.1", "designation": "Débroussaillage et décapage plateforme 3m",
            "unite": "m²", "quantite": 6500, "mo_u": 1.20, "mat_u": 0.00, "eq_u": 1.50, "st_u": 0.00, "k": 1.35
        },
        {
            "id": "dqe_23", "project_id": "projet_montpellier", "project_name": "Voie Verte Montpellier",
            "lot": "Lot 1 : Terrassement", "code": "1.2", "code_prix": "PRIX 1.2", "designation": "Terrassement bassin d'infiltration 1200 m³",
            "unite": "m³", "quantite": 1200, "mo_u": 2.80, "mat_u": 0.00, "eq_u": 4.20, "st_u": 0.00, "k": 1.35
        },
        {
            "id": "dqe_24", "project_id": "projet_montpellier", "project_name": "Voie Verte Montpellier",
            "lot": "Lot 2 : Assainissement", "code": "2.1", "code_prix": "PRIX 2.1", "designation": "Création noues enherbées et buses béton",
            "unite": "ml", "quantite": 450, "mo_u": 8.50, "mat_u": 14.00, "eq_u": 5.50, "st_u": 0.00, "k": 1.35
        },
        {
            "id": "dqe_25", "project_id": "projet_montpellier", "project_name": "Voie Verte Montpellier",
            "lot": "Lot 3 : Voirie", "code": "3.1", "code_prix": "PRIX 3.1", "designation": "Couche de fondation GNT 0/31.5 ép. 20cm",
            "unite": "m²", "quantite": 5400, "mo_u": 1.50, "mat_u": 6.80, "eq_u": 1.80, "st_u": 0.00, "k": 1.35
        },
        {
            "id": "dqe_26", "project_id": "projet_montpellier", "project_name": "Voie Verte Montpellier",
            "lot": "Lot 3 : Voirie", "code": "3.2", "code_prix": "PRIX 3.2", "designation": "Enrobé tiède ocre drainant ép. 5cm",
            "unite": "m²", "quantite": 5400, "mo_u": 3.20, "mat_u": 11.50, "eq_u": 2.80, "st_u": 0.00, "k": 1.35
        },
        {
            "id": "dqe_27", "project_id": "projet_montpellier", "project_name": "Voie Verte Montpellier",
            "lot": "Lot 3 : Voirie", "code": "3.3", "code_prix": "PRIX 3.3", "designation": "Bordures bois chêne brut et mobilier",
            "unite": "ml", "quantite": 1200, "mo_u": 9.50, "mat_u": 14.50, "eq_u": 1.50, "st_u": 0.00, "k": 1.35
        },
        {
            "id": "dqe_28", "project_id": "projet_montpellier", "project_name": "Voie Verte Montpellier",
            "lot": "Lot 4 : Réseaux Secs", "code": "4.1", "code_prix": "PRIX 4.1", "designation": "Bornes solaires balisage nocturne",
            "unite": "u", "quantite": 30, "mo_u": 45.00, "mat_u": 160.00, "eq_u": 15.00, "st_u": 0.00, "k": 1.35
        }
    ]

    # Calculate unified fields
    for it in items:
        ds_u = it["mo_u"] + it["mat_u"] + it["eq_u"] + it["st_u"]
        k = it.get("k", 1.35)
        pv_u = ds_u * k
        qte = it["quantite"]
        it["ds_unitaire"] = round(ds_u, 2)
        it["prix_unitaire_vente_ht"] = round(pv_u, 2)
        it["ds_total"] = round(ds_u * qte, 2)
        it["montant_total_ht"] = round(pv_u * qte, 2)
        it["ds_mo"] = it["mo_u"]
        it["ds_mat"] = it["mat_u"]
        it["ds_eq"] = it["eq_u"]
        it["ds_st"] = it["st_u"]

    return items

if __name__ == "__main__":
    dataset = get_dqe_dataset()
    print(f"Total DQE items: {len(dataset)}")
