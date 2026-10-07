import json

def get_dqe_dataset():
    items = [
        # PROJECT 1: PORT DE SÈTE - QUAI RICHELIEU (HYDROMER & COLSTRONG) (7 ITEMS)
        {
            "id": "dqe_01", "project_id": "projet_sete_richelieu", "project_name": "Port de Sète - Quai Richelieu (Hydromer)",
            "lot": "Lot 1 : Terrassement & Purges Quai", "code": "1.1", "code_prix": "PRIX 1.1", "designation": "Purge et déblais de quai en site maritime sous nappe",
            "unite": "m³", "quantite": 3800, "mo_u": 6.80, "mat_u": 0.00, "eq_u": 8.50, "st_u": 0.00, "k": 1.34
        },
        {
            "id": "dqe_02", "project_id": "projet_sete_richelieu", "project_name": "Port de Sète - Quai Richelieu (Hydromer)",
            "lot": "Lot 1 : Terrassement & Purges Quai", "code": "1.2", "code_prix": "PRIX 1.2", "designation": "Enrochements de protection maritime 1-3 tonnes",
            "unite": "t", "quantite": 1200, "mo_u": 4.50, "mat_u": 28.00, "eq_u": 6.20, "st_u": 0.00, "k": 1.34
        },
        {
            "id": "dqe_03", "project_id": "projet_sete_richelieu", "project_name": "Port de Sète - Quai Richelieu (Hydromer)",
            "lot": "Lot 2 : Assainissement & Réseaux Portuaires", "code": "2.1", "code_prix": "PRIX 2.1", "designation": "Collecteur fonte ductile maritime DN300 avec joint express",
            "unite": "ml", "quantite": 450, "mo_u": 22.00, "mat_u": 98.00, "eq_u": 14.50, "st_u": 0.00, "k": 1.34
        },
        {
            "id": "dqe_04", "project_id": "projet_sete_richelieu", "project_name": "Port de Sète - Quai Richelieu (Hydromer)",
            "lot": "Lot 2 : Assainissement & Réseaux Portuaires", "code": "2.2", "code_prix": "PRIX 2.2", "designation": "Séparateur hydrocarbures coalescence 40 l/s avec débourbeur",
            "unite": "u", "quantite": 1, "mo_u": 3200.00, "mat_u": 24500.00, "eq_u": 2800.00, "st_u": 0.00, "k": 1.34
        },
        {
            "id": "dqe_05", "project_id": "projet_sete_richelieu", "project_name": "Port de Sète - Quai Richelieu (Hydromer)",
            "lot": "Lot 3 : Sous-couche & Bordures Quai", "code": "3.1", "code_prix": "PRIX 3.1", "designation": "Couche de fondation GNT 0/31.5 classe A ép. 30cm",
            "unite": "m²", "quantite": 4600, "mo_u": 1.90, "mat_u": 9.40, "eq_u": 2.40, "st_u": 0.00, "k": 1.34
        },
        {
            "id": "dqe_06", "project_id": "projet_sete_richelieu", "project_name": "Port de Sète - Quai Richelieu (Hydromer)",
            "lot": "Lot 3 : Sous-couche & Bordures Quai", "code": "3.2", "code_prix": "PRIX 3.2", "designation": "Bordures béton haute résistance T3 d'accostage sur semelle C30/37",
            "unite": "ml", "quantite": 680, "mo_u": 16.50, "mat_u": 21.00, "eq_u": 4.20, "st_u": 0.00, "k": 1.34
        },
        {
            "id": "dqe_07", "project_id": "projet_sete_richelieu", "project_name": "Port de Sète - Quai Richelieu (Hydromer)",
            "lot": "Lot 4 : Enrobés Percolés Colstrong (Brevet Colas)", "code": "4.1", "code_prix": "PRIX 4.1", "designation": "Enrobé percolé spécial Colstrong® à haute résistance au poinçonnement (coquilles d'huîtres de Thau recyclées)",
            "unite": "m²", "quantite": 4600, "mo_u": 5.80, "mat_u": 32.50, "eq_u": 6.80, "st_u": 0.00, "k": 1.34
        },

        # PROJECT 2: VOIE VERTE BASSIN DE THAU - PISTE CYCLABLE BOUZIGUES-SÈTE (7 ITEMS)
        {
            "id": "dqe_08", "project_id": "projet_voie_verte_thau", "project_name": "Voie Verte Thau (Bouzigues-Sète)",
            "lot": "Lot 1 : Décapage & Stabilisation Talus", "code": "1.1", "code_prix": "PRIX 1.1", "designation": "Décapage terre végétale et mise en cordon écologique",
            "unite": "m²", "quantite": 14500, "mo_u": 1.10, "mat_u": 0.00, "eq_u": 1.30, "st_u": 0.00, "k": 1.34
        },
        {
            "id": "dqe_09", "project_id": "projet_voie_verte_thau", "project_name": "Voie Verte Thau (Bouzigues-Sète)",
            "lot": "Lot 1 : Décapage & Stabilisation Talus", "code": "1.2", "code_prix": "PRIX 1.2", "designation": "Reprofilage talus étang et enrochements de pied 100-300kg",
            "unite": "m³", "quantite": 850, "mo_u": 4.20, "mat_u": 22.00, "eq_u": 5.50, "st_u": 0.00, "k": 1.34
        },
        {
            "id": "dqe_10", "project_id": "projet_voie_verte_thau", "project_name": "Voie Verte Thau (Bouzigues-Sète)",
            "lot": "Lot 2 : Drainage & Ouvrages Hydrauliques", "code": "2.1", "code_prix": "PRIX 2.1", "designation": "Drainage transversal et buses PEHD annelé Ø300 sous piste",
            "unite": "ml", "quantite": 280, "mo_u": 12.00, "mat_u": 24.50, "eq_u": 6.80, "st_u": 0.00, "k": 1.34
        },
        {
            "id": "dqe_11", "project_id": "projet_voie_verte_thau", "project_name": "Voie Verte Thau (Bouzigues-Sète)",
            "lot": "Lot 3 : Chaussée & Éco-Revêtement Colstab Ostrea", "code": "3.1", "code_prix": "PRIX 3.1", "designation": "Couche de forme en GNT 0/20 non traitée ép. 18cm",
            "unite": "m²", "quantite": 14500, "mo_u": 1.40, "mat_u": 6.80, "eq_u": 1.60, "st_u": 0.00, "k": 1.34
        },
        {
            "id": "dqe_12", "project_id": "projet_voie_verte_thau", "project_name": "Voie Verte Thau (Bouzigues-Sète)",
            "lot": "Lot 3 : Chaussée & Éco-Revêtement Colstab Ostrea", "code": "3.2", "code_prix": "PRIX 3.2", "designation": "Revêtement perméable écologique Colstab Ostrea® (brevet Colas aux coquilles d'huîtres de Thau broyées)",
            "unite": "m²", "quantite": 14500, "mo_u": 3.80, "mat_u": 16.50, "eq_u": 3.40, "st_u": 0.00, "k": 1.34
        },
        {
            "id": "dqe_13", "project_id": "projet_voie_verte_thau", "project_name": "Voie Verte Thau (Bouzigues-Sète)",
            "lot": "Lot 4 : Signalétique & Équipements", "code": "4.1", "code_prix": "PRIX 4.1", "designation": "Glissière bois-métal de protection étang classe N2",
            "unite": "ml", "quantite": 650, "mo_u": 8.50, "mat_u": 42.00, "eq_u": 2.50, "st_u": 0.00, "k": 1.34
        },
        {
            "id": "dqe_14", "project_id": "projet_voie_verte_thau", "project_name": "Voie Verte Thau (Bouzigues-Sète)",
            "lot": "Lot 4 : Signalétique & Équipements", "code": "4.2", "code_prix": "PRIX 4.2", "designation": "Bornes d'information touristique et passages petite faune",
            "unite": "u", "quantite": 18, "mo_u": 65.00, "mat_u": 240.00, "eq_u": 18.00, "st_u": 0.00, "k": 1.34
        },

        # PROJECT 3: SÈTE CENTRE - ASSAINISSEMENT & VOIRIES CARAUSSANE (7 ITEMS)
        {
            "id": "dqe_15", "project_id": "projet_sete_caraussane", "project_name": "Sète Centre - Rues Caraussane & de Gaulle",
            "lot": "Lot 1 : Tranchées Blindées Urbaines", "code": "1.1", "code_prix": "PRIX 1.1", "designation": "Fouille en tranchée étroite blindée caisson léger (Rues Caraussane & Simone Veil)",
            "unite": "m³", "quantite": 1650, "mo_u": 14.50, "mat_u": 4.50, "eq_u": 18.00, "st_u": 0.00, "k": 1.34
        },
        {
            "id": "dqe_16", "project_id": "projet_sete_caraussane", "project_name": "Sète Centre - Rues Caraussane & de Gaulle",
            "lot": "Lot 2 : Séparation Pluviale & Eaux Usées", "code": "2.1", "code_prix": "PRIX 2.1", "designation": "Pose collecteur pluvial fonte ductile DN600 raccordé au réservoir Simone Veil (1 500 m³)",
            "unite": "ml", "quantite": 520, "mo_u": 32.00, "mat_u": 145.00, "eq_u": 22.00, "st_u": 0.00, "k": 1.34
        },
        {
            "id": "dqe_17", "project_id": "projet_sete_caraussane", "project_name": "Sète Centre - Rues Caraussane & de Gaulle",
            "lot": "Lot 2 : Séparation Pluviale & Eaux Usées", "code": "2.2", "code_prix": "PRIX 2.2", "designation": "Renouvellement réseau eaux usées grès vitrifié DN300 et boîte de branchement étanche",
            "unite": "ml", "quantite": 480, "mo_u": 26.00, "mat_u": 78.00, "eq_u": 15.00, "st_u": 0.00, "k": 1.34
        },
        {
            "id": "dqe_18", "project_id": "projet_sete_caraussane", "project_name": "Sète Centre - Rues Caraussane & de Gaulle",
            "lot": "Lot 2 : Séparation Pluviale & Eaux Usées", "code": "2.3", "code_prix": "PRIX 2.3", "designation": "Déconnexion des eaux de toiture et regards siphoïdes de décantation",
            "unite": "u", "quantite": 34, "mo_u": 180.00, "mat_u": 165.00, "eq_u": 35.00, "st_u": 0.00, "k": 1.34
        },
        {
            "id": "dqe_19", "project_id": "projet_sete_caraussane", "project_name": "Sète Centre - Rues Caraussane & de Gaulle",
            "lot": "Lot 3 : Voirie & Trottoirs Urbains", "code": "3.1", "code_prix": "PRIX 3.1", "designation": "Rabotage chaussée existante ép. 6cm et évacuation vers centrale Colas Sète pour recyclage",
            "unite": "m²", "quantite": 3600, "mo_u": 1.20, "mat_u": 0.00, "eq_u": 3.80, "st_u": 0.00, "k": 1.34
        },
        {
            "id": "dqe_20", "project_id": "projet_sete_caraussane", "project_name": "Sète Centre - Rues Caraussane & de Gaulle",
            "lot": "Lot 3 : Voirie & Trottoirs Urbains", "code": "3.2", "code_prix": "PRIX 3.2", "designation": "Couche de roulement en béton bitumineux semi-grenu BBSG 0/10 classe 3",
            "unite": "t", "quantite": 490, "mo_u": 18.00, "mat_u": 68.00, "eq_u": 16.00, "st_u": 0.00, "k": 1.34
        },
        {
            "id": "dqe_21", "project_id": "projet_sete_caraussane", "project_name": "Sète Centre - Rues Caraussane & de Gaulle",
            "lot": "Lot 3 : Voirie & Trottoirs Urbains", "code": "3.3", "code_prix": "PRIX 3.3", "designation": "Trottoirs en béton désactivé teinté ocre Thau et bordures granit T2",
            "unite": "m²", "quantite": 1200, "mo_u": 28.00, "mat_u": 32.00, "eq_u": 4.50, "st_u": 0.00, "k": 1.34
        },

        # PROJECT 4: MARCHÉ ENTRETIEN ROUTIER RD600 / RD612 (7 ITEMS)
        {
            "id": "dqe_22", "project_id": "projet_rd600_entretien", "project_name": "Entretien Routier RD600 / RD612",
            "lot": "Lot 1 : Rabotage & Purges Structurelles", "code": "1.1", "code_prix": "PRIX 1.1", "designation": "Rabotage de nuit fin pleine largeur ép. 5cm sous circulation alternée (RD600)",
            "unite": "m²", "quantite": 22000, "mo_u": 0.95, "mat_u": 0.00, "eq_u": 2.85, "st_u": 0.00, "k": 1.34
        },
        {
            "id": "dqe_23", "project_id": "projet_rd600_entretien", "project_name": "Entretien Routier RD600 / RD612",
            "lot": "Lot 1 : Rabotage & Purges Structurelles", "code": "1.2", "code_prix": "PRIX 1.2", "designation": "Purges localisées profondes 15cm et reconstitution en grave bitume GB4 0/14",
            "unite": "t", "quantite": 450, "mo_u": 14.00, "mat_u": 52.00, "eq_u": 18.00, "st_u": 0.00, "k": 1.34
        },
        {
            "id": "dqe_24", "project_id": "projet_rd600_entretien", "project_name": "Entretien Routier RD600 / RD612",
            "lot": "Lot 2 : Couches de Roulement Haute Performance", "code": "2.1", "code_prix": "PRIX 2.1", "designation": "Couche d'accrochage à l'émulsion de bitume modifié polymères",
            "unite": "m²", "quantite": 22000, "mo_u": 0.25, "mat_u": 0.85, "eq_u": 0.35, "st_u": 0.00, "k": 1.34
        },
        {
            "id": "dqe_25", "project_id": "projet_rd600_entretien", "project_name": "Entretien Routier RD600 / RD612",
            "lot": "Lot 2 : Couches de Roulement Haute Performance", "code": "2.2", "code_prix": "PRIX 2.2", "designation": "Béton Bitumineux Très Mince BBTM 0/10 classe 2 formulé avec 30% d'agrégats recyclés (Centrale Colas Sète Eaux Blanches)",
            "unite": "t", "quantite": 2850, "mo_u": 12.50, "mat_u": 74.00, "eq_u": 14.50, "st_u": 0.00, "k": 1.34
        },
        {
            "id": "dqe_26", "project_id": "projet_rd600_entretien", "project_name": "Entretien Routier RD600 / RD612",
            "lot": "Lot 3 : Épaulements & Assainissement Routier", "code": "3.1", "code_prix": "PRIX 3.1", "designation": "Reprofilage et arasement des accotements en GNT 0/20 calcaire",
            "unite": "ml", "quantite": 4800, "mo_u": 1.80, "mat_u": 4.20, "eq_u": 2.10, "st_u": 0.00, "k": 1.34
        },
        {
            "id": "dqe_27", "project_id": "projet_rd600_entretien", "project_name": "Entretien Routier RD600 / RD612",
            "lot": "Lot 4 : Signalisation & Sécurité Chantier de Nuit", "code": "4.1", "code_prix": "PRIX 4.1", "designation": "Marquage thermoplastique rétro-réfléchissant VNTP classe T3 Q4",
            "unite": "ml", "quantite": 5600, "mo_u": 1.10, "mat_u": 2.40, "eq_u": 0.80, "st_u": 0.00, "k": 1.34
        },
        {
            "id": "dqe_28", "project_id": "projet_rd600_entretien", "project_name": "Entretien Routier RD600 / RD612",
            "lot": "Lot 4 : Signalisation & Sécurité Chantier de Nuit", "code": "4.2", "code_prix": "PRIX 4.2", "designation": "Balisage d'urgence et flèches lumineuses KR11 pour chantier mobile de nuit",
            "unite": "u", "quantite": 12, "mo_u": 85.00, "mat_u": 350.00, "eq_u": 45.00, "st_u": 0.00, "k": 1.34
        }
    ]

    # Calculate unified fields
    for it in items:
        ds_u = it["mo_u"] + it["mat_u"] + it["eq_u"] + it["st_u"]
        k = it.get("k", 1.34)
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
    print(f"Total DQE items generated: {len(dataset)}")
