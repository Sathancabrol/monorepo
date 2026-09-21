import json

def get_company_data():
    return {
        "company": {
            "name": "BTP HÉRAULT OCCITANIE TP & VRD",
            "siege": "Sète / Agde / Alès (Occitanie)",
            "capital": "500 000 €",
            "siren": "849 321 654",
            "ca_annuel_prev": 4250000,
            "carnet_commandes_12m": 5890000,
            "tresorerie_actuelle": 485200,
            "bfr": 142800,
            "dso_days": 52,
            "dpo_days": 45,
            "situations_en_attente": 318450,
            "retenues_garantie_5pct": 138200,
            "index_tp01_base": 128.4,
            "index_tp01_actuel": 136.2,
            "formule_revision": "P = P0 * (0.15 + 0.85 * (TP01 / TP01_0))",
            "depenses_mois": {
                "salaires_charges": 112000,
                "fournisseurs_materiaux": 68400,
                "carburant_energie": 18200,
                "location_materiel": 16000
            },
            "marge_nette_moyenne": 14.2,
            "taux_frequence_accidents": 0,
            "taux_gravite": 0
        },
        "map_locations": [
            { "id": "ch_01", "name": "Giratoire RD906 Alès", "category": "chantier", "lat": 44.1284, "lng": 4.0833, "color": "#38bdf8", "icon": "🏗️", "ownership": "Interne Entreprise (En cours)", "budget_ini": 850000, "budget_used": 612000, "progress": 80, "chef": "Alain Martin", "desc": "Giratoire RD906, réseaux pluviaux Ø400 et couche BBSG." },
            { "id": "ch_02", "name": "ZAC Littoral Sète", "category": "chantier", "lat": 43.4075, "lng": 3.6928, "color": "#38bdf8", "icon": "🏗️", "ownership": "Interne Entreprise (En cours)", "budget_ini": 1450000, "budget_used": 435000, "progress": 38, "chef": "Marc Gomez", "desc": "Viabilisation lourde, collecteur Fonte DN400 sous nappe." },
            { "id": "ch_03", "name": "Centre Ancien Pézenas", "category": "chantier", "lat": 43.4600, "lng": 3.4230, "color": "#38bdf8", "icon": "🏗️", "ownership": "Interne Entreprise (En cours)", "budget_ini": 480000, "budget_used": 210000, "progress": 52, "chef": "Karim Benali", "desc": "Renouvellement AEP Ø150 et pavage granit patrimoine." },
            { "id": "ch_04", "name": "Voie Verte Montpellier", "category": "chantier", "lat": 43.6108, "lng": 3.8767, "color": "#38bdf8", "icon": "🏗️", "ownership": "Interne Entreprise (En cours)", "budget_ini": 620000, "budget_used": 124000, "progress": 25, "chef": "David Lemoine", "desc": "Aménagement voie cyclable 3.00m et bassin rétention." },
            { "id": "ref_01", "name": "Giratoire Barbazan (DCE Public)", "category": "marche_public_ref", "lat": 44.1120, "lng": 4.0950, "color": "#a855f7", "icon": "🏛️", "ownership": "Marché Public Réel DCE Référence", "budget_ini": 920000, "budget_used": 918500, "progress": 100, "chef": "Référence Étalon DCE", "desc": "Marché public départemental achevé - Utilisé pour étalonnage des cadences." },
            { "id": "ref_02", "name": "Lotissement Aurouer (DCE Public)", "category": "marche_public_ref", "lat": 46.6800, "lng": 3.3000, "color": "#a855f7", "icon": "🏛️", "ownership": "Marché Public Réel DCE Référence", "budget_ini": 1150000, "budget_used": 1145000, "progress": 100, "chef": "Référence Étalon DCE", "desc": "Lotissement 42 parcelles - Référence viabilisation et métrés." },
            { "id": "ref_03", "name": "Aménagement Saint-Nicolas (DCE)", "category": "marche_public_ref", "lat": 44.0600, "lng": 1.0200, "color": "#a855f7", "icon": "🏛️", "ownership": "Marché Public Réel DCE Référence", "budget_ini": 530000, "budget_used": 528000, "progress": 100, "chef": "Référence Étalon DCE", "desc": "Voirie urbaine et pluvial - Référence ratio prix et déboursés." },
            { "id": "dep_01", "name": "Dépôt Central Sète Littoral", "category": "depot", "lat": 43.4150, "lng": 3.7100, "color": "#f59e0b", "icon": "🏢", "stock_val": "420 000 €", "contact": "04 67 11 22 33", "desc": "Stock principal bordures, fontes, caissons blindage et atelier engins." },
            { "id": "dep_02", "name": "Dépôt Logistique Alès Grand Centre", "category": "depot", "lat": 44.1350, "lng": 4.0750, "color": "#f59e0b", "icon": "🏢", "stock_val": "280 000 €", "contact": "04 66 88 99 00", "desc": "Stockage graves GNT, tuyaux bétons et base vie Gard." },
            { "id": "eq_01", "name": "Équipe 1 - Terrassement & Plateforme", "category": "equipe", "lat": 44.1284, "lng": 4.0833, "color": "#10b981", "icon": "👷‍♂️", "leader": "Alain Martin (6 compagnons)", "radio": "Canal 4 TP", "desc": "Pelle Liebherr 24t + Chargeuse Volvo + 2 Camions 8x4." },
            { "id": "eq_02", "name": "Équipe 2 - Réseaux Profonds & Blindage", "category": "equipe", "lat": 43.4075, "lng": 3.6928, "color": "#10b981", "icon": "👷‍♂️", "leader": "Marc Gomez (5 compagnons)", "radio": "Canal 2 TP", "desc": "Pelle 24t + Mecalac 12MTX + Poseurs canalisations fontes." },
            { "id": "eq_03", "name": "Équipe 3 - Pavage & VRD Patrimoine", "category": "equipe", "lat": 43.4600, "lng": 3.4230, "color": "#10b981", "icon": "👷‍♂️", "leader": "Karim Benali (4 compagnons)", "radio": "Canal 3 TP", "desc": "Mini-pelle Kubota 5.5t + Poseurs pavés granit et résine." },
            { "id": "eq_04", "name": "Équipe 4 - Topographie & Drone 3D", "category": "equipe", "lat": 43.6108, "lng": 3.8767, "color": "#10b981", "icon": "🛰️", "leader": "David Lemoine (2 techniciens)", "radio": "Canal 1 TP", "desc": "Station totale Leica + Canne GPS RTK + Drone DJI RTK." },
            { "id": "fourn_01", "name": "Carrières du Languedoc", "category": "fournisseur", "lat": 43.5500, "lng": 3.5200, "color": "#ec4899", "icon": "🏭", "product": "Grave GNT 0/31.5 & Concassés", "distance": "14 km", "desc": "Fournisseur agréé matériaux granulaires et graves routières." },
            { "id": "fourn_02", "name": "Bétons Occitanie (Centrales BPE)", "category": "fournisseur", "lat": 43.4200, "lng": 3.6600, "color": "#ec4899", "icon": "🏭", "product": "Bétons C25/30 & Désactivés", "distance": "8 km", "desc": "Centrale certifiée NF Béton prêt à l'emploi et bordures NF." },
            { "id": "fourn_03", "name": "PAM Saint-Gobain Canalisation", "category": "fournisseur", "lat": 43.6500, "lng": 3.9000, "color": "#ec4899", "icon": "🏭", "product": "Tuyaux Fonte & Fontes Voirie", "distance": "22 km", "desc": "Fabricant fonte ductile DN100 à DN600 et tampons D400." },
            { "id": "fourn_04", "name": "Négoce TP Littoral", "category": "fournisseur", "lat": 43.4300, "lng": 3.7000, "color": "#ec4899", "icon": "🏭", "product": "Bordures T2, Caniveaux CC1, TPC", "distance": "6 km", "desc": "Distribution négoce outillage, EPI et signalisation OPBTP." },
            { "id": "moa_01", "name": "Conseil Départemental du Gard (MOA)", "category": "moa_moe", "lat": 43.8367, "lng": 4.3600, "color": "#8b5cf6", "icon": "🏛️", "contact": "Direction des Routes & Mobilités", "desc": "Maître d'Ouvrage du Giratoire RD906 Alès." },
            { "id": "moa_02", "name": "Sète Agglopôle Méditerranée (MOA)", "category": "moa_moe", "lat": 43.4000, "lng": 3.6900, "color": "#8b5cf6", "icon": "🏛️", "contact": "Direction Aménagement & Eau", "desc": "Maître d'Ouvrage de la ZAC Littoral Sète." },
            { "id": "moe_01", "name": "BET VRD Occitanie Ingénierie (MOE)", "category": "moa_moe", "lat": 43.6000, "lng": 3.8700, "color": "#6366f1", "icon": "📐", "contact": "Ingénieur Maître d'Œuvre", "desc": "Maîtrise d'Œuvre et contrôle d'exécution chantiers VRD." },
            { "id": "csps_01", "name": "APAVE / Bureau Veritas (CSPS & CT)", "category": "moa_moe", "lat": 43.6200, "lng": 3.8500, "color": "#f97316", "icon": "🦺", "contact": "Coordonnateur SPS Niv. 1", "desc": "Coordination Sécurité et Protection de la Santé & Contrôle Technique." }
        ],
        "hierarchy": {
            "direction": [
                {
                    "id": "emp_01",
                    "name": "Laurent VIALA",
                    "role": "Directeur Général / Gérant TP",
                    "salary_bracket": "Direction Générale",
                    "cert": "AIPR Concepteur • Ingénieur ESTP",
                    "secu": "100%",
                    "rate": "85 €/h",
                    "color": "#38bdf8"
                }
            ],
            "conduite": [
                {
                    "id": "emp_02",
                    "name": "Sylvain CABROL",
                    "role": "Conducteur de Travaux Principal VRD",
                    "salary_bracket": "Cadre Position A",
                    "cert": "AIPR Encadrant • Master Génie Civil",
                    "secu": "99%",
                    "rate": "55 €/h",
                    "color": "#0284c7",
                    "assigned": ["Giratoire RD906 Alès", "ZAC Littoral Sète"]
                },
                {
                    "id": "emp_03",
                    "name": "Sophie LACOMBE",
                    "role": "Conductrice de Travaux Aménagements & Prix",
                    "salary_bracket": "Cadre Position B",
                    "cert": "AIPR Encadrant • Ingénieure BTP",
                    "secu": "100%",
                    "rate": "52 €/h",
                    "color": "#0284c7",
                    "assigned": ["Centre Ancien Pézenas", "Voie Verte Montpellier"]
                }
            ],
            "chefs": [
                {
                    "id": "emp_04",
                    "name": "Alain MARTIN",
                    "role": "Chef de Chantier TP / VRD",
                    "salary_bracket": "ETAM Niveau G",
                    "site": "Giratoire RD906 Alès",
                    "caces": "CACES R482 B1/C1 • AIPR Encadrant",
                    "secu": "100%",
                    "color": "#10b981"
                },
                {
                    "id": "emp_05",
                    "name": "Mamadou TRAORÉ",
                    "role": "Chef de Chantier Terrassement & Réseaux",
                    "salary_bracket": "ETAM Niveau F",
                    "site": "Giratoire RD906 Alès",
                    "caces": "CACES R482 Cat B1 • AIPR Encadrant",
                    "secu": "100%",
                    "color": "#10b981"
                },
                {
                    "id": "emp_06",
                    "name": "Marc GOMEZ",
                    "role": "Chef de Chantier Réseaux Profonds",
                    "salary_bracket": "ETAM Niveau G",
                    "site": "ZAC Littoral Sète",
                    "caces": "AIPR Encadrant • CATEC Espace Confiné",
                    "secu": "98%",
                    "color": "#10b981"
                },
                {
                    "id": "emp_07",
                    "name": "Karim BENALI",
                    "role": "Chef de Chantier Réseaux Secs & Télécom",
                    "salary_bracket": "ETAM Niveau F",
                    "site": "ZAC Littoral Sète",
                    "caces": "AIPR Encadrant • H0B0 Élec",
                    "secu": "100%",
                    "color": "#10b981"
                },
                {
                    "id": "emp_08",
                    "name": "Patrick DURAND",
                    "role": "Chef d'Équipe Enrobés & Chaussée",
                    "salary_bracket": "ETAM Niveau E",
                    "site": "Centre Ancien Pézenas",
                    "caces": "CACES R482 Cat D/E",
                    "secu": "100%",
                    "color": "#f59e0b"
                },
                {
                    "id": "emp_09",
                    "name": "David LEMOINE",
                    "role": "Chef de Cellule Topographie & Drone",
                    "salary_bracket": "ETAM Niveau F",
                    "site": "Voie Verte Montpellier",
                    "caces": "Télépilote Drone Pro DGAC • GPS RTK",
                    "secu": "100%",
                    "color": "#f59e0b"
                }
            ],
            "partenaires_moa_moe": [
                {
                    "id": "part_01",
                    "name": "Conseil Départemental du Gard",
                    "category": "MOA (Maître d'Ouvrage)",
                    "rep": "M. Bernard DUPUIS (Directeur des Routes)",
                    "role": "Commanditaire public & Validation Situations",
                    "color": "#a855f7"
                },
                {
                    "id": "part_02",
                    "name": "Sète Agglopôle Méditerranée",
                    "category": "MOA (Maître d'Ouvrage)",
                    "rep": "Mme Claire MÉRIDIER (Chef de Projet ZAC)",
                    "role": "Commanditaire public & Décisions Travaux",
                    "color": "#a855f7"
                },
                {
                    "id": "part_03",
                    "name": "Cabinet VRD Ingénierie Occitanie",
                    "category": "MOE (Maître d'Œuvre)",
                    "rep": "Ing. Marc VALENTIN",
                    "role": "Visa des plans, validation récolements & OPR",
                    "color": "#6366f1"
                },
                {
                    "id": "part_04",
                    "name": "APAVE Sécurité & Prévention",
                    "category": "CSPS (Coordination Sécurité)",
                    "rep": "M. Luc CHABERT (CSPS Niveau 1)",
                    "role": "Audit PPSPS, DICT, conformité blindage et balisage",
                    "color": "#f97316"
                }
            ]
        },
        "ai_agents": [
            {
                "id": "ai_nexus",
                "tier": "direction",
                "name": "BTP-Nexus (Direction & Trésorerie)",
                "role": "Agent IA Gouvernance & Trésorerie",
                "status": "Actif • 1.2% CPU • Latence 4ms",
                "recommendation": "Situation de travaux ZAC n°2 validée à 125k€. Prévoir émission sous Chorus Pro sous 48h.",
                "desc": "Surveillance prédictive BFR, arbitrage situations de travaux Chorus Pro, respect CCAG 2021 et alertes trésorerie.",
                "color": "#34d399"
            },
            {
                "id": "ai_optichantier",
                "tier": "conduite",
                "name": "OptiChantier-AI (Méthodes & Planif)",
                "role": "Agent IA Méthodes & Logistique",
                "status": "Actif • 3.5% CPU • 4D Synchro OK",
                "recommendation": "Optimiser la rotation des 2 camions 8x4 sur Alès pour réduire l'attente pelle de 18 minutes.",
                "desc": "Optimisation des cadences de rotation d'engins, synchronisation 4D des phases et gestion des flux de trafic résiduel.",
                "color": "#38bdf8"
            },
            {
                "id": "ai_kestimator",
                "tier": "conduite",
                "name": "K-Estimator (Étude de Prix)",
                "role": "Agent IA Étude de Prix & SDP",
                "status": "Actif • Marge Réelle K=1.354",
                "recommendation": "Gain d'achat de 4.2% sur les bordures T2 négocié auprès de Bétons Occitanie. Marge brute +1.1%.",
                "desc": "Contrôle en continu du ratio Déboursé Sec vs Prix de Vente, analyse des écarts et recalcul dynamique du coefficient K.",
                "color": "#38bdf8"
            },
            {
                "id": "ai_safetysentinel",
                "tier": "terrain",
                "name": "SafetySentinel (AIPR & Sécurité)",
                "role": "Agent IA Prévention des Risques",
                "status": "Actif • 0 Alerte Critique en cours",
                "recommendation": "Vérifier le piquetage jaune gaz MPB à l'avancement du PK 0+240 avant reprise terrassement demain matin.",
                "desc": "Vérification continue des distances d'approche DICT, des hauteurs de blindage de tranchée et de la conformité des EPI.",
                "color": "#facc15"
            },
            {
                "id": "ai_topobot",
                "tier": "terrain",
                "name": "TopoBot (Contrôle Altimétrique)",
                "role": "Agent IA Nivellement & Guidage 3D",
                "status": "Actif • Précision RTK ±4mm",
                "recommendation": "Nivellement radier pluvial BA Ø400 à -1.82m conforme au CCTP. Pente 1.52% validée.",
                "desc": "Contrôle altimétrique temps réel des pentes de canalisation (tolérance ±5mm) et guidage automatique des engins par GPS RTK.",
                "color": "#34d399"
            }
        ],
        "cashflow_transactions": [
            { "id": "tx_01", "date": "2026-09-02", "type": "Encaissement Client", "label": "Situation n°4 Giratoire RD906 Alès", "project": "Giratoire RD906 Alès", "tier": "Client MOA", "amount": 142000, "category": "Entrée CA", "status": "Encaissé", "details": "Validation MOE + Chorus Pro" },
            { "id": "tx_02", "date": "2026-09-05", "type": "Décaissement Salaires", "label": "Salaires & Charges Équipes Terrain (18 ouvriers + 4 cadres)", "project": "Siège & Chantiers", "tier": "Salariés / URSSAF", "amount": -112000, "category": "Main d'Œuvre", "status": "Payé", "details": "Virement SEPA direct" },
            { "id": "tx_03", "date": "2026-09-08", "type": "Décaissement Fournisseur", "label": "Achat 1800t GNT 0/31.5 Classe A", "project": "Giratoire RD906 Alès", "tier": "Carrières du Languedoc", "amount": -29700, "category": "Matériaux", "status": "Payé", "details": "Facture F-8842 à 30 jours" },
            { "id": "tx_04", "date": "2026-09-12", "type": "Encaissement Client", "label": "Acompte Démarrage Voie Verte Montpellier", "project": "Voie Verte Montpellier", "tier": "Client MOA", "amount": 62000, "category": "Entrée CA", "status": "Encaissé", "details": "Avance forfaitaire CCAG 10%" },
            { "id": "tx_05", "date": "2026-09-15", "type": "Décaissement Fournisseur", "label": "Fourniture Tuyaux Fonte DN400 Integral", "project": "ZAC Littoral Sète", "tier": "Saint-Gobain PAM", "amount": -40250, "category": "Matériaux", "status": "Payé", "details": "Bordereau de livraison 340m" },
            { "id": "tx_06", "date": "2026-09-18", "type": "Décaissement Carburant", "label": "Gazole Non Routier (GNR) Engins TP & Camions", "project": "Flotte Totale", "tier": "TotalEnergies Pro", "amount": -18200, "category": "Énergie / Carburant", "status": "Payé", "details": "Livraison cuve Sète & Alès" },
            { "id": "tx_07", "date": "2026-09-20", "type": "Encaissement Client", "label": "Situation n°2 ZAC Littoral Sète", "project": "ZAC Littoral Sète", "tier": "Client MOA", "amount": 125000, "category": "Entrée CA", "status": "Encaissé", "details": "Tranchée profonde et blindage" }
        ],
        "benchmark_data": [
            { "code": "TERR_01", "designation": "Décapage terre végétale e=20cm (m²)", "unit": "m²", "cost_internal": 1.45, "pv_internal": 1.96, "ref_dce_barbazan": 2.10, "ref_dce_aurouer": 1.90, "fntp_regional_avg": 2.05, "variance_pct": -4.4, "status": "Très Compétitif" },
            { "code": "TERR_02", "designation": "Déblais grande masse en pleine masse (m³)", "unit": "m³", "cost_internal": 5.80, "pv_internal": 7.83, "ref_dce_barbazan": 8.20, "ref_dce_aurouer": 7.95, "fntp_regional_avg": 8.10, "variance_pct": -3.3, "status": "Optimisé Pelle 24t" },
            { "code": "BORD_01", "designation": "Bordures béton T2 sur semelle (ml)", "unit": "ml", "cost_internal": 18.20, "pv_internal": 24.57, "ref_dce_barbazan": 25.50, "ref_dce_aurouer": 24.00, "fntp_regional_avg": 25.00, "variance_pct": -1.7, "status": "Conforme Marché" },
            { "code": "CAN_01", "designation": "Caniveaux béton CC1 avec calage (ml)", "unit": "ml", "cost_internal": 28.50, "pv_internal": 38.48, "ref_dce_barbazan": 39.50, "ref_dce_aurouer": 37.80, "fntp_regional_avg": 39.00, "variance_pct": -1.3, "status": "Conforme Marché" },
            { "code": "ASSAIN_01", "designation": "Collecteur Pluvial Béton Armé Ø400 (ml)", "unit": "ml", "cost_internal": 72.00, "pv_internal": 97.20, "ref_dce_barbazan": 102.00, "ref_dce_aurouer": 98.50, "fntp_regional_avg": 100.00, "variance_pct": -2.8, "status": "Très Rentable" },
            { "code": "ASSAIN_02", "designation": "Collecteur Fonte Ductile DN400 Integral (ml)", "unit": "ml", "cost_internal": 145.00, "pv_internal": 195.75, "ref_dce_barbazan": 205.00, "ref_dce_aurouer": 198.00, "fntp_regional_avg": 202.00, "variance_pct": -3.1, "status": "Rentabilité Maîtrisée" },
            { "code": "VOIR_01", "designation": "GNT 0/31.5 compactée e=25cm (m²)", "unit": "m²", "cost_internal": 8.10, "pv_internal": 10.94, "ref_dce_barbazan": 11.20, "ref_dce_aurouer": 10.80, "fntp_regional_avg": 11.10, "variance_pct": -1.4, "status": "Marge Optimisée" },
            { "code": "VOIR_02", "designation": "Enrobé BBSG 0/10 e=6cm appliqué chaud (m²)", "unit": "m²", "cost_internal": 14.80, "pv_internal": 19.98, "ref_dce_barbazan": 20.80, "ref_dce_aurouer": 19.50, "fntp_regional_avg": 20.20, "variance_pct": -1.1, "status": "Standard Régional" }
        ],
        "inventory_assets": [
            { "id": "ast_01", "name": "Pelle Hydraulique Liebherr R924 G8 (24t)", "category": "Engin de Production", "year": 2023, "purchase_val": 285000, "book_val": 218000, "hourly_cost": 52.50, "hours": 1420, "next_maint": "14/11/2026 (VGP)", "location": "Giratoire RD906 Alès" },
            { "id": "ast_02", "name": "Pelleteuse Urbaine Mecalac 12MTX", "category": "Engin Polyvalent", "year": 2024, "purchase_val": 195000, "book_val": 165000, "hourly_cost": 38.00, "hours": 890, "next_maint": "08/10/2026 (VGP)", "location": "ZAC Littoral Sète" },
            { "id": "ast_03", "name": "Compacteur Tandem Bomag BW 154 AP-5", "category": "Compacteur Lourd", "year": 2023, "purchase_val": 145000, "book_val": 110000, "hourly_cost": 29.50, "hours": 620, "next_maint": "22/12/2026", "location": "Giratoire RD906 Alès" },
            { "id": "ast_04", "name": "Camion Porteur 8x4 Scania G450 XT (32t)", "category": "Transport Lourd", "year": 2022, "purchase_val": 210000, "book_val": 145000, "hourly_cost": 44.00, "hours": 2150, "next_maint": "15/01/2027", "location": "Alès & Sète" },
            { "id": "ast_05", "name": "Camion Hydrocureur Renault K480 (10m³)", "category": "Assainissement", "year": 2023, "purchase_val": 380000, "book_val": 305000, "hourly_cost": 65.00, "hours": 1100, "next_maint": "05/02/2027", "location": "Pézenas Centre" },
            { "id": "ast_06", "name": "Lot 6 Caissons Blindage Acier Krings R4534", "category": "Sécurité Tranchée", "year": 2024, "purchase_val": 64000, "book_val": 56000, "hourly_cost": 8.00, "hours": 450, "next_maint": "Contrôle trimestriel", "location": "ZAC Littoral Sète" },
            { "id": "ast_07", "name": "Station Topo Totale & Canne GPS RTK Leica", "category": "Topographie Guidage", "year": 2024, "purchase_val": 32000, "book_val": 28000, "hourly_cost": 5.50, "hours": 780, "next_maint": "Étalonnage annuel", "location": "Voie Verte Montpellier" }
        ],
        "benchmark_teams": [
            { "team_name": "Équipe 1 : Terrassement Grande Masse & Purges", "composition": "1 Chef de chantier + 2 Conducteurs engins B1/C1 + 1 Chauffeur PL 8x4 + 1 Manœuvre VRD", "hourly_cost_team": 185.00, "daily_yield_our": "420 m³/jour", "fntp_ref_yield": "380 m³/jour", "diff_yield": "+10.5%", "safety_score": "100% AIPR", "main_equipment": "Liebherr R924 (24t) + Scania 8x4" },
            { "team_name": "Équipe 2 : Pose Canalisations Pluviales & EU", "composition": "1 Chef d'équipe + 1 Canalisateur qualifié + 1 Chauffeur mini-pelle + 1 Aide poseur", "hourly_cost_team": 145.00, "daily_yield_our": "28 ml/jour (BA Ø400)", "fntp_ref_yield": "24 ml/jour", "diff_yield": "+16.7%", "safety_score": "100% AIPR", "main_equipment": "Mecalac 12MTX + Laser Piper + Caisson R4534" },
            { "team_name": "Équipe 3 : Pose Bordures, Caniveaux & Trottoirs", "composition": "1 Chef d'équipe + 2 Poseurs qualifiés + 1 Manœuvre régleur", "hourly_cost_team": 135.00, "daily_yield_our": "68 ml/jour (Bordures T2)", "fntp_ref_yield": "58 ml/jour", "diff_yield": "+17.2%", "safety_score": "100% CACES", "main_equipment": "Pince hydraulique + Scie thermique Stihl" },
            { "team_name": "Équipe 4 : Application Chaussées & Enrobés", "composition": "1 Chef d'application + 1 Régleur finisseur + 2 Cylindreurs + 2 Tireurs au râteau", "hourly_cost_team": 220.00, "daily_yield_our": "185 t/jour (BBSG)", "fntp_ref_yield": "160 t/jour", "diff_yield": "+15.6%", "safety_score": "100% CACES R482", "main_equipment": "Finisseur Vögele + Bomag BW154 + Bi-benne" }
        ],
        "projects": [
            {
                "id": "projet_ales",
                "name": "Aménagement Giratoire RD906 & Voie Verte",
                "client": "Conseil Départemental du Gard / Ville d'Alès",
                "ownership": "🏢 Notre Entreprise (En cours)",
                "location": "Alès / Barbazan (30)",
                "conducteur": "Sylvain CABROL",
                "chef_chantier": "Alain MARTIN",
                "budget_total": 850000,
                "depense_reelle": 612000,
                "avancement_physique_pct": 80,
                "delai_consomme_pct": 78,
                "statut": "En cours - Phase Enrobés",
                "date_debut": "2026-05-15",
                "date_fin_prevue": "2026-10-30",
                "risques_aipr": "Conduite Gaz MPB 4 bars à 1.20m (DICT validée)",
                "kpis": { "cpi": 1.11, "spi": 1.02 },
                "timeline_steps": [
                    { "step": 1, "name": "DICT & Piquetage Réseaux 7 Couleurs", "date": "15/05/2026", "progress": 100, "status": "Terminé", "lot": "Lot 01" },
                    { "step": 2, "name": "Terrassement en déblai & Purge sol", "date": "10/06/2026", "progress": 100, "status": "Terminé", "lot": "Lot 01" },
                    { "step": 3, "name": "Pose Collecteur Pluvial BA Ø400", "date": "15/07/2026", "progress": 100, "status": "Terminé", "lot": "Lot 02" },
                    { "step": 4, "name": "Fourreaux TPC Réseaux Secs & Massifs", "date": "15/08/2026", "progress": 100, "status": "Terminé", "lot": "Lot 04" },
                    { "step": 5, "name": "Pose Bordures T2 & Caniveaux CC1", "date": "10/09/2026", "progress": 85, "status": "En cours", "lot": "Lot 03" },
                    { "step": 6, "name": "Couche de Roulement BBSG 0/10 (350t)", "date": "15/10/2026", "progress": 10, "status": "À venir", "lot": "Lot 03" },
                    { "step": 7, "name": "Réception des Travaux & OPR / DGD", "date": "30/10/2026", "progress": 0, "status": "À venir", "lot": "Clôture" }
                ],
                "assigned_machinery": [
                    { "name": "Pelle Liebherr R924 G8 (24t)", "type": "Terrassement / Pose", "status": "Actif" },
                    { "name": "Chargeuse Volvo L110H", "type": "Manutention GNT", "status": "Actif" },
                    { "name": "Camion Scania 8x4 Bi-Benne", "type": "Évacuation Déblais", "status": "En rotation" }
                ],
                "assigned_tools": [
                    { "name": "Laser Canalisateur Piper 200", "type": "Topographie" },
                    { "name": "Scie Diamant Stihl TS800", "type": "Découpe Chaussée" },
                    { "name": "Pilonneuse Wacker Neuson BS60", "type": "Compactage Tranchée" }
                ],
                "assigned_materials": [
                    { "name": "Grave GNT 0/31.5 Classe A", "qty": "4 200 tonnes", "supplier": "Carrières du Languedoc" },
                    { "name": "Bordures Béton T2 NF", "qty": "850 ml", "supplier": "Bétons Occitanie" },
                    { "name": "Tuyau Béton Ø400 135A", "qty": "650 ml", "supplier": "BOM" },
                    { "name": "Enrobé Chaud BBSG 0/10", "qty": "350 tonnes", "supplier": "Enrobés du Sud" }
                ],
                "lots_breakdown": [
                    {
                        "lot": "01",
                        "name": "Terrassement & Déblais",
                        "budget": 212500,
                        "progress": 100,
                        "status": "Terminé",
                        "tech_steps": [
                            "Décapage terre végétale épaisseur 20cm au scraper et stockage séparé pour réemploi paysager.",
                            "Déblais grande masse en pleine masse à la pelle 24t avec nivellement guidé laser (pente 2%).",
                            "Traitement de la plateforme de sol à la chaux vive 2% pour assurer une portance EV2 >= 50 MPa.",
                            "Évacuation des déblais excédentaires inertes en décharge agréée ISDI avec bordereau BSD."
                        ],
                        "admin_steps": [
                            "Obtention des récépissés DICT conformes auprès de GRDF, Enedis et Orange.",
                            "Arrêté municipal de circulation et de restriction de vitesse (30 km/h) validé.",
                            "Dépôt et validation du Plan Particulier de Sécurité et Protection de la Santé (PPSPS).",
                            "Édition du Procès-Verbal de réception de plateforme terrassement par le géotechnicien."
                        ]
                    },
                    {
                        "lot": "02",
                        "name": "Assainissement & Eaux Pluviales",
                        "budget": 297500,
                        "progress": 100,
                        "status": "Terminé",
                        "tech_steps": [
                            "Ouverture de tranchée 1.80m avec blindage continu et lit de pose sable 4/10 compacté (10cm).",
                            "Pose au laser des tuyaux béton armé Ø400 135A avec contrôle continu des pentes (1.5%).",
                            "Mise en place de 14 regards de visite préfabriqués 1000x1000 avec cunettes hydrauliques soignées.",
                            "Remblaiement par couches de 30cm en GNT 0/31.5 avec contrôle au pénétromètre dynamique PANDA (Q4)."
                        ],
                        "admin_steps": [
                            "Validation des fiches d'agrément des fournitures par la Maîtrise d'Œuvre.",
                            "Rapport d'épreuve d'étanchéité à l'air / eau selon Fascicule 70-1 Titre I.",
                            "Rapport d'inspection télévisée (ITV) caméra haute définition avant remblai final.",
                            "Plans de récolement DAO levés en classe A par géomètre-expert."
                        ]
                    },
                    {
                        "lot": "03",
                        "name": "Voirie, Bordures & Structure de Chaussée",
                        "budget": 170000,
                        "progress": 75,
                        "status": "En cours",
                        "tech_steps": [
                            "Réglage de la couche de fondation GNT 0/31.5 épaisseur 25cm au compacteur vibrant V5.",
                            "Pose sur semelle béton C25/30 de 850 ml de bordures T2 et 850 ml de caniveaux CC1.",
                            "Coulage de l'îlot central en béton désactivé décoratif avec gravillons de Garonne 6/10.",
                            "Application de la couche de roulement enrobé à chaud BBSG 0/10 à 160°C au finisseur grande largeur."
                        ],
                        "admin_steps": [
                            "Validation de la formule de compactage et rapport Terrameter (EV2 > 120 MPa).",
                            "Essais d'extraction et de compacité de l'enrobé par laboratoire accrédité COFRAC.",
                            "Contrôle de l'uni longitudinal et transversal de la couche de roulement.",
                            "Dossier des Ouvrages Exécutés (DOE) provisoire remis à la MOE."
                        ]
                    },
                    {
                        "lot": "04",
                        "name": "Réseaux Secs & Éclairage Public",
                        "budget": 170000,
                        "progress": 65,
                        "status": "En cours",
                        "tech_steps": [
                            "Pose sous trottoir de fourreaux TPC Ø110 rouge (élec), vert (télécom) et jaune (gaz).",
                            "Mise en place d'un grillage avertisseur normé 20cm au-dessus des génératrices supérieures.",
                            "Coulage des massifs béton armé 1.00m x 1.00m pour 12 candélabres LED 8m.",
                            "Tirage des câbles et raccordement au coffret de commande télégestion."
                        ],
                        "admin_steps": [
                            "Contrôle d'isolement et de continuité électrique par organisme tiers agréé (APAVE).",
                            "Déclaration d'achèvement de raccordement auprès du gestionnaire Enedis.",
                            "Fiche technique de conformité photométrique des luminaires LED.",
                            "Attestation de conformité Consuel pour les installations d'éclairage public."
                        ]
                    }
                ]
            },
            {
                "id": "projet_sete",
                "name": "Viabilisation & Réseaux Profonds ZAC Littoral",
                "client": "Sète Agglopôle Méditerranée",
                "ownership": "🏢 Notre Entreprise (En cours)",
                "location": "Sète / Entrée Est (34)",
                "conducteur": "Sylvain CABROL",
                "chef_chantier": "Marc GOMEZ",
                "budget_total": 1450000,
                "depense_reelle": 435000,
                "avancement_physique_pct": 38,
                "delai_consomme_pct": 35,
                "statut": "En cours - Tranchée Profonde",
                "date_debut": "2026-07-01",
                "date_fin_prevue": "2027-02-28",
                "risques_aipr": "Nappe phréatique sub-affleurante à -1.40m, rabattement actif",
                "kpis": { "cpi": 1.05, "spi": 1.00 },
                "timeline_steps": [
                    { "step": 1, "name": "DICT & Pompage / Rabattement de nappe", "date": "01/07/2026", "progress": 100, "status": "Terminé", "lot": "Lot 01" },
                    { "step": 2, "name": "Terrassement sous blindage lourd caisson", "date": "20/07/2026", "progress": 100, "status": "Terminé", "lot": "Lot 01" },
                    { "step": 3, "name": "Pose Collecteur Fonte DN400 (prof. 3.20m)", "date": "15/08/2026", "progress": 70, "status": "En cours", "lot": "Lot 02" },
                    { "step": 4, "name": "Station de refoulement EU & Électromécanique", "date": "01/10/2026", "progress": 20, "status": "En cours", "lot": "Lot 02" },
                    { "step": 5, "name": "Réseaux Divers (AEP, BT/HTA, Fibre)", "date": "15/11/2026", "progress": 0, "status": "À venir", "lot": "Lot 04" },
                    { "step": 6, "name": "Structure Voirie Lourde & Enrobés", "date": "15/01/2027", "progress": 0, "status": "À venir", "lot": "Lot 03" },
                    { "step": 7, "name": "Épreuves Fascicule 70 & Réception", "date": "28/02/2027", "progress": 0, "status": "À venir", "lot": "Clôture" }
                ],
                "assigned_machinery": [
                    { "name": "Pelle Liebherr R924 G8 (24t)", "type": "Tranchée Profonde", "status": "Actif" },
                    { "name": "Pelleteuse Mecalac 12MTX", "type": "Manutention Urbaine", "status": "Actif" },
                    { "name": "Hydrocureur Renault K480", "type": "Curage Réseaux", "status": "Actif" }
                ],
                "assigned_tools": [
                    { "name": "Laser Canalisateur Piper 200", "type": "Topographie" },
                    { "name": "Détecteur de Réseaux RD8100", "type": "Détection DICT" }
                ],
                "assigned_materials": [
                    { "name": "Tuyau Fonte DN400 Integral", "qty": "850 ml", "supplier": "Saint-Gobain PAM" },
                    { "name": "Grave GNT 0/31.5 Concassée", "qty": "3 100 tonnes", "supplier": "Carrières du Languedoc" }
                ],
                "lots_breakdown": [
                    {
                        "lot": "01",
                        "name": "Terrassement Profond & Rabattement",
                        "budget": 362500,
                        "progress": 85,
                        "status": "En cours",
                        "tech_steps": [
                            "Installation de pointes filtrantes tous les 1.50m pour rabattement de nappe phréatique.",
                            "Terrassement par passe de 1.00m avec descente guidée des caissons de blindage acier (R4534).",
                            "Évacuation en site propre des limons maritimes saturés d'eau."
                        ],
                        "admin_steps": [
                            "Autorisation de rejet des eaux de pompage (Loi sur l'Eau).",
                            "Surveillance piézométrique continue du niveau de nappe.",
                            "Contrôle journalier de l'étaiement des caissons de blindage."
                        ]
                    },
                    {
                        "lot": "02",
                        "name": "Assainissement Fonte & Poste de Relevage",
                        "budget": 652500,
                        "progress": 45,
                        "status": "En cours",
                        "tech_steps": [
                            "Pose au tire-fort hydraulique des tuyaux fonte ductile DN400 avec joints verrouillés Vi.",
                            "Coulage du radier béton armé hydrofuge pour la bâche de pompage (diamètre 3.00m).",
                            "Installation des pompes submersibles dilacératrices 22 kW."
                        ],
                        "admin_steps": [
                            "Contrôle de conformité de l'ancrage anti-sous-pression par bureau de contrôle.",
                            "Essais d'étanchéité sous pression 6 bars Fascicule 71.",
                            "Réception électromécanique par le délégataire d'assainissement."
                        ]
                    }
                ]
            },
            {
                "id": "projet_pezenas",
                "name": "Rénovation Réseaux & Voirie Centre Ancien",
                "client": "Ville de Pézenas (34)",
                "ownership": "🏢 Notre Entreprise (En cours)",
                "location": "Pézenas / Centre Historique (34)",
                "conducteur": "Sophie LACOMBE",
                "chef_chantier": "Karim BENALI",
                "budget_total": 480000,
                "depense_reelle": 210000,
                "avancement_physique_pct": 52,
                "delai_consomme_pct": 50,
                "statut": "En cours - Pose Pavage & Réseaux",
                "date_debut": "2026-06-01",
                "date_fin_prevue": "2026-11-15",
                "risques_aipr": "Ruelles étroites (largeur 2.40m), voûtes et réseaux anciens non répertoriés",
                "kpis": { "cpi": 1.08, "spi": 1.01 },
                "timeline_steps": [
                    { "step": 1, "name": "Reconnaissance géoradar & Sondages doux", "date": "01/06/2026", "progress": 100, "status": "Terminé", "lot": "Lot 01" },
                    { "step": 2, "name": "Dépose pavés anciens & Tri patrimonial", "date": "15/06/2026", "progress": 100, "status": "Terminé", "lot": "Lot 01" },
                    { "step": 3, "name": "Renouvellement Conduite AEP Fonte Ø150", "date": "10/07/2026", "progress": 100, "status": "Terminé", "lot": "Lot 02" },
                    { "step": 4, "name": "Enfouissement Réseaux Élec & Fibre", "date": "15/08/2026", "progress": 60, "status": "En cours", "lot": "Lot 04" },
                    { "step": 5, "name": "Repose Pavés Granit & Joints Résine", "date": "15/09/2026", "progress": 30, "status": "En cours", "lot": "Lot 03" },
                    { "step": 6, "name": "Éclairage Public Style Ancien & Lanternes", "date": "15/10/2026", "progress": 0, "status": "À venir", "lot": "Lot 04" },
                    { "step": 7, "name": "Réception & Libération des Rues", "date": "15/11/2026", "progress": 0, "status": "À venir", "lot": "Clôture" }
                ],
                "assigned_machinery": [
                    { "name": "Mini-Pelle Kubota KX057-4 (5.5t)", "type": "Micro-Terrassement", "status": "Actif" },
                    { "name": "Hydrocureur Renault K480", "type": "Curage / Aspiration", "status": "Actif" }
                ],
                "assigned_tools": [
                    { "name": "Scie Diamant Stihl TS800", "type": "Découpe Granit" },
                    { "name": "Pilonneuse Wacker Neuson BS60", "type": "Compactage Tranchée" }
                ],
                "assigned_materials": [
                    { "name": "Tuyau Fonte DN150 AEP", "qty": "320 ml", "supplier": "Saint-Gobain PAM" },
                    { "name": "Pavés Granit Occitanie", "qty": "850 m²", "supplier": "Carrières Régionales" }
                ],
                "lots_breakdown": [
                    {
                        "lot": "01",
                        "name": "Terrassement & Dépose Patrimoniale",
                        "budget": 120000,
                        "progress": 100,
                        "status": "Terminé",
                        "tech_steps": [
                            "Dépose manuelle soignée des pavés anciens et palettisation pour réemploi.",
                            "Terrassement par aspiration / micro-pelle pour préserver les caves voûtées."
                        ],
                        "admin_steps": [
                            "Autorisation de l'Architecte des Bâtiments de France (ABF).",
                            "Arrêté de fermeture de rue avec gestion des accès piétons riverains."
                        ]
                    }
                ]
            },
            {
                "id": "projet_montpellier",
                "name": "Création Voie Verte & Réseaux Pluviaux",
                "client": "Montpellier Méditerranée Métropole",
                "ownership": "🏢 Notre Entreprise (En cours)",
                "location": "Montpellier / Grabels (34)",
                "conducteur": "Sophie LACOMBE",
                "chef_chantier": "David LEMOINE",
                "budget_total": 620000,
                "depense_reelle": 124000,
                "avancement_physique_pct": 25,
                "delai_consomme_pct": 20,
                "statut": "En cours - Nivellement & Bassin",
                "date_debut": "2026-08-01",
                "date_fin_prevue": "2026-12-20",
                "risques_aipr": "Zone naturelle sensible, franchissement cours d'eau temporaire",
                "kpis": { "cpi": 1.15, "spi": 1.05 },
                "timeline_steps": [
                    { "step": 1, "name": "Débroussaillage & Piquetage Topo Drone", "date": "01/08/2026", "progress": 100, "status": "Terminé", "lot": "Lot 01" },
                    { "step": 2, "name": "Création Bassin de Rétention Infiltrant", "date": "20/08/2026", "progress": 80, "status": "En cours", "lot": "Lot 02" },
                    { "step": 3, "name": "Terrassement Plateforme Voie 3.00m", "date": "10/09/2026", "progress": 40, "status": "En cours", "lot": "Lot 01" },
                    { "step": 4, "name": "Pose Noues Enherbées & Buses Béton", "date": "01/10/2026", "progress": 0, "status": "À venir", "lot": "Lot 02" },
                    { "step": 5, "name": "Couche de Fondation & Enrobé Tiède Ocre", "date": "01/11/2026", "progress": 0, "status": "À venir", "lot": "Lot 03" },
                    { "step": 6, "name": "Signalétique Cyclable & Mobilier Bois", "date": "01/12/2026", "progress": 0, "status": "À venir", "lot": "Lot 03" },
                    { "step": 7, "name": "Réception & DGD", "date": "20/12/2026", "progress": 0, "status": "À venir", "lot": "Clôture" }
                ],
                "assigned_machinery": [
                    { "name": "Pelleteuse Mecalac 12MTX", "type": "Nivellement Guidé", "status": "Actif" },
                    { "name": "Compacteur Bomag BW 154 AP", "type": "Compactage Écologique", "status": "Actif" }
                ],
                "assigned_tools": [
                    { "name": "Canne GPS RTK Leica", "type": "Contrôle Altimétrique" },
                    { "name": "Drone Aérien DJI RTK", "type": "Photogrammétrie" }
                ],
                "assigned_materials": [
                    { "name": "Grave GNT 0/31.5 Concassée", "qty": "1 800 tonnes", "supplier": "Carrières du Languedoc" },
                    { "name": "Enrobé Tiède Ocre Drainant", "qty": "450 tonnes", "supplier": "Enrobés du Sud" }
                ],
                "lots_breakdown": [
                    {
                        "lot": "01",
                        "name": "Terrassement Voie Verte & Bassin",
                        "budget": 248000,
                        "progress": 60,
                        "status": "En cours",
                        "tech_steps": [
                            "Décapage terre végétale et création d'un merlon paysager antibruit.",
                            "Terrassement du bassin de rétention 1200 m³ avec talus à 1:2.",
                            "Réglage guidé 3D au drone de la plateforme cyclo-piétonne 3.00m."
                        ],
                        "admin_steps": [
                            "Autorisation environnementale Loi sur l'Eau.",
                            "Plan d'implantation topographique certifié classe A."
                        ]
                    }
                ]
            }
        ],
        "fleet": [
            {
                "id": "veh_01",
                "name": "Pelle sur Chenilles Liebherr R924 G8 (24t)",
                "type": "Pelle Hydraulique",
                "brand": "Liebherr",
                "immat": "TP-340-LH",
                "hours": 1420,
                "project": "Giratoire RD906 Alès",
                "vgp": "14/11/2026",
                "price": 285000,
                "weight": "24 200 kg",
                "dimensions": "9.90m x 2.98m x 3.15m",
                "power": "129 kW (175 ch)",
                "capacity": "1.45 m³ (Godet terrassement)",
                "consumption": "16.8 L/h",
                "geoloc": { "lat": 44.1284, "lng": 4.0833, "site": "Alès RD906" },
                "photo_url": "https://images.unsplash.com/photo-1578632767115-351597cf2477?w=800",
                "status": "Opérationnel (En fonction)"
            },
            {
                "id": "veh_02",
                "name": "Pelleteuse sur Pneus Mecalac 12MTX",
                "type": "Pelle sur Pneus Polyvalente",
                "brand": "Mecalac",
                "immat": "TP-120-MC",
                "hours": 890,
                "project": "ZAC Littoral Sète",
                "vgp": "08/10/2026",
                "price": 195000,
                "weight": "9 700 kg",
                "dimensions": "5.60m x 2.38m x 3.10m",
                "power": "85 kW (115 ch)",
                "capacity": "0.75 m³ (Godet 4 en 1)",
                "consumption": "10.5 L/h",
                "geoloc": { "lat": 43.4075, "lng": 3.6928, "site": "Sète ZAC" },
                "photo_url": "https://images.unsplash.com/photo-1581094288338-2314dddb7ece?w=800",
                "status": "Opérationnel (En fonction)"
            },
            {
                "id": "veh_03",
                "name": "Compacteur Tandem Vibrant Bomag BW 154 AP-5",
                "type": "Compacteur Lourd V5",
                "brand": "Bomag",
                "immat": "TP-154-BM",
                "hours": 620,
                "project": "Giratoire RD906 Alès",
                "vgp": "22/12/2026",
                "price": 145000,
                "weight": "8 800 kg",
                "dimensions": "4.61m x 1.68m x 2.95m",
                "power": "55 kW (75 ch)",
                "capacity": "Largeur bille 1.50m double vibration",
                "consumption": "9.2 L/h",
                "geoloc": { "lat": 44.1290, "lng": 4.0840, "site": "Alès RD906" },
                "photo_url": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=800",
                "status": "Opérationnel (En fonction)"
            },
            {
                "id": "veh_04",
                "name": "Camion Bi-Benne 8x4 Scania G450 XT (32t)",
                "type": "Camion Porteur 8x4",
                "brand": "Scania",
                "immat": "FN-842-TP",
                "hours": 2150,
                "project": "Giratoire RD906 Alès",
                "vgp": "15/01/2027",
                "price": 210000,
                "weight": "32 000 kg (PTAC)",
                "dimensions": "8.80m x 2.55m x 3.40m",
                "power": "331 kW (450 ch)",
                "capacity": "Benne Hardox 18 m³ (20 tonnes)",
                "consumption": "34.5 L/100km",
                "geoloc": { "lat": 44.1280, "lng": 4.0820, "site": "Rotation Alès" },
                "photo_url": "https://images.unsplash.com/photo-1601584115197-04ecc0da31d7?w=800",
                "status": "Opérationnel (En fonction)"
            },
            {
                "id": "veh_05",
                "name": "Camion Hydrocureur / Aspiratrice Renault K480",
                "type": "Camion Spécialisé Assainissement",
                "brand": "Renault Trucks",
                "immat": "GQ-318-VR",
                "hours": 1100,
                "project": "Centre Ancien Pézenas",
                "vgp": "05/02/2027",
                "price": 380000,
                "weight": "26 000 kg",
                "dimensions": "9.20m x 2.50m x 3.65m",
                "power": "353 kW (480 ch)",
                "capacity": "Cuve 10 000 L (Boues 7000L + Eau 3000L)",
                "consumption": "28.0 L/h (Travail pompe)",
                "geoloc": { "lat": 43.4600, "lng": 3.4230, "site": "Pézenas Centre" },
                "photo_url": "https://images.unsplash.com/photo-1541888946425-d0fbb180c5f5?w=800",
                "status": "Opérationnel (En fonction)"
            },
            {
                "id": "veh_06",
                "name": "Mini-Pelle Urbaine Kubota KX057-4 (5.5t)",
                "type": "Mini-Pelle Compacte",
                "brand": "Kubota",
                "immat": "TP-057-KB",
                "hours": 940,
                "project": "Centre Ancien Pézenas",
                "vgp": "18/10/2026",
                "price": 68000,
                "weight": "5 545 kg",
                "dimensions": "5.52m x 1.96m x 2.55m",
                "power": "35 kW (47.6 ch)",
                "capacity": "0.18 m³ (Godet terrassement)",
                "consumption": "6.2 L/h",
                "geoloc": { "lat": 43.4605, "lng": 3.4235, "site": "Pézenas Centre" },
                "photo_url": "https://images.unsplash.com/photo-1581094288338-2314dddb7ece?w=800",
                "status": "Opérationnel (En fonction)"
            }
        ],
        "catalog": [
            # 1. EPI & SIGNALÉTIQUE
            { "id": "mat_01", "name": "Pack EPI Réglementaire BTP Classe 3", "category": "EPI & Signalétique", "supplier": "Négoce Protection Directe", "price_ht": 145.00, "unit": "pack", "stock": 50, "norm": "NF EN ISO 20471", "description": "Casque avec jugulaire, gilet haute visibilité classe 3, gants anti-coupure D et chaussures S3." },
            { "id": "mat_02", "name": "Kit Signalisation Temporaire de Chantier AK5 + B14 + Cônes K5a", "category": "EPI & Signalétique", "supplier": "Signalétique Occitanie", "price_ht": 850.00, "unit": "kit", "stock": 15, "norm": "Instruction Interministérielle Livre I - 8e partie", "description": "2 panneaux AK5 1000mm, 2 panneaux B14 (30 km/h), 30 cônes K5a rétro-réfléchissants classe 2." },
            { "id": "mat_03", "name": "Balises d'Alignement K8 Monodirectionnelles Rétro-Réfléchissantes", "category": "EPI & Signalétique", "supplier": "Signalétique Occitanie", "price_ht": 42.00, "unit": "u", "stock": 80, "norm": "NF P98-453", "description": "Balises plastiques avec socle lesté 15kg pour balisage d'approche de nuit." },
            { "id": "mat_04", "name": "Séparateurs de Voies Plastiques K16 Lestables (Rouge & Blanc)", "category": "EPI & Signalétique", "supplier": "Signalétique Occitanie", "price_ht": 38.00, "unit": "ml", "stock": 250, "norm": "NF P98-450", "description": "Séparateur monobloc emboîtable à lester d'eau ou de sable pour déviation." },

            # 2. PETIT OUTILLAGE & LASERS
            { "id": "tool_01", "name": "Laser Canalisateur Rouge Automatique Piper 200", "category": "Petit Outillage & Lasers", "supplier": "Leica Geosystems France", "price_ht": 3450.00, "unit": "u", "stock": 4, "norm": "IP68 Submersible / Précision ±1.5mm à 30m", "description": "Laser de pose de canalisations avec télécommande infrarouge et alignement automatique." },
            { "id": "tool_02", "name": "Niveau Laser Rotatif Double Pente Rugby CLA-CLX 700", "category": "Petit Outillage & Lasers", "supplier": "Leica Geosystems France", "price_ht": 2890.00, "unit": "u", "stock": 6, "norm": "IP68 / Portée 1350m", "description": "Laser rotatif pour guidage d'engins, terrassement et nivellement de plateforme." },
            { "id": "tool_03", "name": "Découpeuse à Disque Diamant Thermique Stihl TS 800 (Ø400 mm)", "category": "Petit Outillage & Lasers", "supplier": "Stihl France Distribution", "price_ht": 1420.00, "unit": "u", "stock": 8, "norm": "CE / Profondeur coupe 145mm", "description": "Scie à béton et enrobé avec raccord d'arrosage anti-poussière intégré." },
            { "id": "tool_04", "name": "Pilonneuse Vibrante 4 Temps Wacker Neuson BS 60-4As", "category": "Petit Outillage & Lasers", "supplier": "Wacker Neuson Occitanie", "price_ht": 2650.00, "unit": "u", "stock": 10, "norm": "ISO 9001 / Force frappe 18 kN", "description": "Pilonneuse pour compactage efficace en tranchée étroite et pied de bordure." },
            { "id": "tool_05", "name": "Plaque Vibrante Réversible Wacker Neuson DPU 4045Ye (Diesel)", "category": "Petit Outillage & Lasers", "supplier": "Wacker Neuson Occitanie", "price_ht": 5800.00, "unit": "u", "stock": 5, "norm": "Force frappe 40 kN", "description": "Plaque pour compactage des couches de fondation GNT et enrobés." },

            # 3. BÉTONS & BORDURES
            { "id": "mat_05", "name": "Bordures Béton Trottoir Droites T2 NF (L=1.00m)", "category": "Bétons, Bordures & Tuyaux", "supplier": "Bétons Occitanie Méditerranée", "price_ht": 8.80, "unit": "ml", "stock": 1400, "norm": "NF P98-305 / Classe U+D", "description": "Bordure de voirie standard 12x15x20 cm pour trottoirs et séparations de chaussée." },
            { "id": "mat_06", "name": "Bordures Basses Infranchissables A2 NF (L=1.00m)", "category": "Bétons, Bordures & Tuyaux", "supplier": "Bétons Occitanie Méditerranée", "price_ht": 9.20, "unit": "ml", "stock": 900, "norm": "NF P98-305", "description": "Bordure d'accotement et d'îlot pour canalisation de trafic urbain." },
            { "id": "mat_07", "name": "Bordures Giratoire Franchissables I2 / P2 (L=1.00m)", "category": "Bétons, Bordures & Tuyaux", "supplier": "Bétons Occitanie Méditerranée", "price_ht": 12.50, "unit": "ml", "stock": 650, "norm": "NF EN 1340", "description": "Bordure inclinée pour anneaux de giratoires franchissables par poids lourds." },
            { "id": "mat_08", "name": "Caniveaux Préfabriqués CC1 à Fente Hydraulique (L=1.00m)", "category": "Bétons, Bordures & Tuyaux", "supplier": "Bétons Occitanie Méditerranée", "price_ht": 18.50, "unit": "ml", "stock": 500, "norm": "NF EN 1433", "description": "Caniveau préfabriqué avec profil d'évacuation des eaux pluviales de chaussée." },
            { "id": "mat_09", "name": "Béton Prêt à l'Emploi C25/30 XF1 / S3 pour Semelle Bordures", "category": "Bétons, Bordures & Tuyaux", "supplier": "Bétons Occitanie Méditerranée", "price_ht": 128.00, "unit": "m³", "stock": 200, "norm": "NF EN 206+A2/CN", "description": "Béton dosé à 250-300 kg de ciment avec calage rigide des bordures." },
            { "id": "mat_10", "name": "Béton Désactivé Formulé Gravillons Garonne 6/10", "category": "Bétons, Bordures & Tuyaux", "supplier": "Bétons Occitanie Méditerranée", "price_ht": 155.00, "unit": "m³", "stock": 100, "norm": "NF EN 206 Décoratif", "description": "Béton d'ornement pour îlots centraux et trottoirs piétons." },

            # 4. CANALISATIONS & FONTES
            { "id": "mat_11", "name": "Tampon Fonte Ductile D400 PAM Rexel Ø600 Trafic Lourd", "category": "Bétons, Bordures & Tuyaux", "supplier": "Saint-Gobain PAM Canalisation", "price_ht": 145.00, "unit": "u", "stock": 65, "norm": "NF EN 124-2 / 400 kN", "description": "Tampon de regard de visite articulé avec joint polyéthylène antibruit." },
            { "id": "mat_12", "name": "Grille Avaloir Concave Fonte C250 (500x500 mm)", "category": "Bétons, Bordures & Tuyaux", "supplier": "Saint-Gobain PAM Canalisation", "price_ht": 98.00, "unit": "u", "stock": 70, "norm": "NF EN 124-2 / 250 kN", "description": "Grille de caniveau concave pour absorption optimale du fil d'eau." },
            { "id": "mat_13", "name": "Tuyau Fonte Ductile DN400 Integral (L=6.00m)", "category": "Bétons, Bordures & Tuyaux", "supplier": "Saint-Gobain PAM Canalisation", "price_ht": 115.00, "unit": "ml", "stock": 350, "norm": "Fascicule 70-1 / Revêtement Zinc-Alu", "description": "Tuyau fonte haute résistance mécanique avec joint automatique élastomère." },
            { "id": "mat_14", "name": "Tuyau PVC Assainissement CR8 Ø200 (L=3.00m)", "category": "Bétons, Bordures & Tuyaux", "supplier": "PUM Plastiques Sète", "price_ht": 18.50, "unit": "ml", "stock": 600, "norm": "NF EN 1401 / Rigidité CR8", "description": "Canalisation PVC compact à joint pour réseau eaux usées et pluviales." },
            { "id": "mat_15", "name": "Tube PEHD Gaz 100mm SDR11 Bande Jaune (4 bars)", "category": "Bétons, Bordures & Tuyaux", "supplier": "PUM Plastiques Sète", "price_ht": 22.00, "unit": "ml", "stock": 400, "norm": "NF EN 1555 / Gaz MPB", "description": "Tube polyéthylène haute densité pour distribution de gaz combustible." },
            { "id": "mat_16", "name": "Grave Non Traitée GNT 0/31.5 Classe A Concassée", "category": "Bétons, Bordures & Tuyaux", "supplier": "Carrières du Languedoc", "price_ht": 16.50, "unit": "tonne", "stock": 3500, "norm": "NF EN 13285 / Guide GTR", "description": "Grave concassée pure pour couche de fondation et remblaiement de tranchée." },
            { "id": "mat_17", "name": "Enrobé Bitumineux Chaud BBSG 0/10 Classe 3 (160°C)", "category": "Bétons, Bordures & Tuyaux", "supplier": "Enrobés du Sud", "price_ht": 82.00, "unit": "tonne", "stock": 800, "norm": "NF P98-150 / Roulement", "description": "Béton Bitumineux Semi-Grenu pour couche de roulement de chaussée." }
        ]
    }

if __name__ == "__main__":
    data = get_company_data()
    print(f"Company data loaded successfully. Projects: {len(data['projects'])}, Map points: {len(data['map_locations'])}, Benchmark: {len(data['benchmark_data'])}")
