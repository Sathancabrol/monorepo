import json

def get_company_data():
    return {
        "company": {
            "name": "COLAS AGENCE DE SÈTE & BASSIN DE THAU",
            "siege": "Zone Industrielle des Eaux Blanches, CS 10098, 34200 Sète (Hérault)",
            "capital": "1 500 000 € (Colas Midi Méditerranée SA)",
            "siren": "329 338 883 01359",
            "ca_annuel_prev": 18500000,
            "carnet_commandes_12m": 22400000,
            "tresorerie_actuelle": 1450000,
            "bfr": 420000,
            "dso_days": 42,
            "dpo_days": 48,
            "situations_en_attente": 845000,
            "retenues_garantie_5pct": 312000,
            "index_tp01_base": 128.4,
            "index_tp01_actuel": 136.2,
            "formule_revision": "P = P0 * (0.15 + 0.85 * (TP01 / TP01_0))",
            "depenses_mois": {
                "salaires_charges": 340000,
                "fournisseurs_materiaux": 420000,
                "carburant_energie": 68000,
                "centrales_enrobes": 195000
            },
            "marge_nette_moyenne": 14.8,
            "taux_frequence_accidents": 0,
            "taux_gravite": 0
        },
        "map_locations": [
            { "id": "ch_01", "name": "Port de Sète - Quai Richelieu (Hydromer & Colstrong)", "category": "chantier", "lat": 43.3980, "lng": 3.7020, "color": "#38bdf8", "icon": "🏗️", "ownership": "Colas Agence Sète (En cours)", "budget_ini": 1850000, "budget_used": 1258000, "progress": 68, "chef": "Rémi Bonnefoi (Chef Établissement: R. Caraï)", "desc": "Aménagement quai drague Hydromer, enrobés percolés brevetés Colstrong aux coquilles d'huîtres de Thau." },
            { "id": "ch_02", "name": "Voie Verte Bassin de Thau (Piste Cyclable Colstab Ostrea)", "category": "chantier", "lat": 43.4350, "lng": 3.6550, "color": "#38bdf8", "icon": "🏗️", "ownership": "Colas Agence Sète (En cours)", "budget_ini": 920000, "budget_used": 772800, "progress": 84, "chef": "Jérôme Vidal (Conductrice: S. Martinez)", "desc": "Création piste cyclable 4.2 km, revêtement drainant Colstab Ostrea à valorisation conchylicole." },
            { "id": "ch_03", "name": "Sète Centre - Réseaux & Voiries Rues Caraussane & de Gaulle", "category": "chantier", "lat": 43.4080, "lng": 3.6930, "color": "#38bdf8", "icon": "🏗️", "ownership": "Colas Agence Sète (En cours)", "budget_ini": 1420000, "budget_used": 596400, "progress": 42, "chef": "Bruno Dupuis (Conducteur: R. Bonnefoi)", "desc": "Séparation pluviale vers réservoir Simone Veil 1 500 m³, fonte DN600, BBSG 0/10 et béton désactivé." },
            { "id": "ch_04", "name": "Marché Entretien Routier RD600 / RD612 & Liaisons Thau", "category": "chantier", "lat": 43.4380, "lng": 3.7250, "color": "#38bdf8", "icon": "🏗️", "ownership": "Colas Agence Sète (Accord-cadre)", "budget_ini": 3200000, "budget_used": 960000, "progress": 30, "chef": "Marc Bellegarde (Conducteur: R. Caraï)", "desc": "Rabotage de nuit fin 5cm, BBTM 0/10 haute performance centrale Eaux Blanches, 30% recyclé." },
            { "id": "dep_01", "name": "Colas Établissement de Sète & Dépôt Matériel", "category": "depot", "lat": 43.4240, "lng": 3.7080, "color": "#f59e0b", "icon": "🏢", "stock_val": "1 450 000 €", "contact": "04 67 46 22 00", "desc": "Siège agence, ateliers poids lourds, parc finisseurs et stockage granulats/liants (1052 Av. des Eaux Blanches)." },
            { "id": "centrale_01", "name": "Centrale d'Enrobage Languedoc Enrobés / Colas", "category": "fournisseur", "lat": 43.5250, "lng": 3.8450, "color": "#ec4899", "icon": "🏭", "product": "Enrobés à chaud BBSG, BBTM, Colstrong & Colstab", "distance": "12 km", "desc": "Poste d'enrobage discontinu 240 t/h avec recyclage d'agrégats d'enrobés et liants modifiés." },
            { "id": "carriere_01", "name": "Carrières de l'Hérault / GSM Poussan & Mèze", "category": "fournisseur", "lat": 43.4900, "lng": 3.6800, "color": "#ec4899", "icon": "🏭", "product": "GNT 0/31.5 classe A, Enrochements, Sables 0/4", "distance": "9 km", "desc": "Extraction calcaire massif et plateforme de recyclage matériaux de déconstruction." },
            { "id": "fourn_02", "name": "Bétons Occitanie / CEMEX Bassin de Thau", "category": "fournisseur", "lat": 43.4200, "lng": 3.6600, "color": "#ec4899", "icon": "🏭", "product": "Bétons Prêts à l'Emploi C25/30, C30/37, Désactivés", "distance": "6 km", "desc": "Centrale certifiée NF Béton alimentant les chantiers de bordures et ouvrages béton." },
            { "id": "moa_01", "name": "Région Occitanie / Port Sud de France Sète (MOA)", "category": "moa_moe", "lat": 43.3960, "lng": 3.7050, "color": "#8b5cf6", "icon": "🏛️", "contact": "Direction Portuaire & Maritime", "desc": "Maître d'Ouvrage de la reconstruction et aménagement des quais portuaires." },
            { "id": "moa_02", "name": "Sète Agglopôle Méditerranée (MOA)", "category": "moa_moe", "lat": 43.4120, "lng": 3.6960, "color": "#8b5cf6", "icon": "🏛️", "contact": "Direction du Cycle de l'Eau & Aménagements", "desc": "Maître d'Ouvrage des réseaux d'assainissement et de la Voie Verte." },
            { "id": "moa_03", "name": "Conseil Départemental de l'Hérault (CD34 MOA)", "category": "moa_moe", "lat": 43.6100, "lng": 3.8700, "color": "#8b5cf6", "icon": "🏛️", "contact": "Direction des Routes & Agence Routière", "desc": "Maître d'Ouvrage du réseau routier départemental RD600/RD612." }
        ],
        "hierarchy": {
            "direction": [
                {
                    "id": "emp_01",
                    "name": "Romain CARAÏ",
                    "role": "Chef d'Établissement Colas Agence de Sète",
                    "salary_bracket": "Direction Établissement TP",
                    "cert": "AIPR Concepteur • Ingénieur TP",
                    "secu": "100%",
                    "rate": "95 €/h",
                    "color": "#38bdf8"
                }
            ],
            "conduite": [
                {
                    "id": "emp_02",
                    "name": "Rémi BONNEFOI",
                    "role": "Conducteur de Travaux Principal Grands Chantiers & Port",
                    "salary_bracket": "Cadre Position A",
                    "cert": "AIPR Encadrant • Spécialité Maritime & Enrobés",
                    "secu": "99.5%",
                    "rate": "62 €/h",
                    "color": "#0284c7",
                    "assigned": ["Port de Sète - Quai Richelieu", "Sète Centre - Caraussane"]
                },
                {
                    "id": "emp_03",
                    "name": "Sophie MARTINEZ",
                    "role": "Conductrice de Travaux VRD & Éco-aménagements",
                    "salary_bracket": "Cadre Position B",
                    "cert": "AIPR Encadrant • Ingénieure Environnement",
                    "secu": "100%",
                    "rate": "58 €/h",
                    "color": "#0284c7",
                    "assigned": ["Voie Verte Bassin de Thau", "Entretien Routier RD600"]
                }
            ],
            "chefs": [
                {
                    "id": "emp_04",
                    "name": "Bruno DUPUIS",
                    "role": "Chef de Chantier Réseaux Urbains & Séparatif",
                    "salary_bracket": "ETAM Niveau G",
                    "site": "Sète Centre - Rues Caraussane & de Gaulle",
                    "caces": "AIPR Encadrant • CATEC Espace Confiné",
                    "secu": "100%",
                    "color": "#10b981"
                },
                {
                    "id": "emp_05",
                    "name": "Jérôme VIDAL",
                    "role": "Chef de Chantier Voies Vertes & Revêtements Innovants",
                    "salary_bracket": "ETAM Niveau F",
                    "site": "Voie Verte Bassin de Thau",
                    "caces": "CACES R482 Cat B1/C1 • AIPR Encadrant",
                    "secu": "100%",
                    "color": "#10b981"
                },
                {
                    "id": "emp_06",
                    "name": "Marc BELLEGARDE",
                    "role": "Chef de Chantier Application Enrobés & Rabotage",
                    "salary_bracket": "ETAM Niveau G",
                    "site": "Port de Sète Quai Richelieu & RD600",
                    "caces": "CACES R482 Cat D (Finisseur) & E • AIPR",
                    "secu": "98.5%",
                    "color": "#10b981"
                }
            ]
        }
    }
