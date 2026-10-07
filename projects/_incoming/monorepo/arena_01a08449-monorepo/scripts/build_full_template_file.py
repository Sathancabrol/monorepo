import json
import sys
from pathlib import Path

ROOT = Path('/home/user/monorepo')
TARGET = ROOT / 'projects' / 'btp-conduite-travaux'
sys.path.insert(0, str(ROOT))

from scripts.generate_obsidian_data import get_obsidian_dataset
from scripts.generate_extra_data import get_company_data
from scripts.generate_complete_dqe_data import get_dqe_dataset
from scripts.generate_technical_illustrations import get_vehicle_svg, get_tool_material_svg

# Load JSON Datasets
with open(TARGET / 'data' / 'corpus_btp_inventory.json', 'r', encoding='utf-8') as f:
    inventory = json.load(f)

with open(TARGET / 'data' / 'synthese_chantiers_et_prix.json', 'r', encoding='utf-8') as f:
    synthese = json.load(f)

with open(TARGET / 'data' / 'confrontation_theorie_etatdelart_insitu.json', 'r', encoding='utf-8') as f:
    confrontation = json.load(f)

with open(TARGET / 'data' / 'btp_audit_ledger.json', 'r', encoding='utf-8') as f:
    ledger_data = json.load(f)

reports = {}
for rfile in sorted((TARGET / 'rapports').glob('*.md')):
    reports[rfile.name] = rfile.read_text(encoding='utf-8')

obsidian_graph_data = get_obsidian_dataset()
extra_data = get_company_data()
extra_data['dqe_items'] = get_dqe_dataset()

# Materials Catalog
extra_data['materials_catalog'] = [
    {
        "id": "mat_01", "category": "bordures", "name": "Bordures Béton Type T2 (100x20x28 cm)",
        "fournisseur": "Bétons Occitanie Méditerranée", "unit": "ml", "prix_unitaire": 14.50,
        "conditionnement": "Palette de 12 ml (960 kg)", "norme": "NF EN 1340 / Classe A",
        "stock": "450 ml", "stock_status": "in_stock", "poids": "80 kg / ml", "dimensions": "100 x 20 x 28 cm", "icon": "📐"
    },
    {
        "id": "mat_02", "category": "bordures", "name": "Bordures Béton Type A2 (100x20x20 cm)",
        "fournisseur": "Bétons Occitanie Méditerranée", "unit": "ml", "prix_unitaire": 12.80,
        "conditionnement": "Palette de 15 ml (850 kg)", "norme": "NF EN 1340",
        "stock": "320 ml", "stock_status": "in_stock", "poids": "58 kg / ml", "dimensions": "100 x 20 x 20 cm", "icon": "📐"
    },
    {
        "id": "mat_03", "category": "voirie_fonte", "name": "Tampon Fonte Ductile D400 PAM REXEL Ø600",
        "fournisseur": "Saint-Gobain PAM Canalisation", "unit": "u", "prix_unitaire": 145.00,
        "conditionnement": "Palette de 10 unités", "norme": "NF EN 124 / 400 kN Trafic Lourd",
        "stock": "28 u", "stock_status": "in_stock", "poids": "54 kg / pièce", "dimensions": "Cadre 850x850 mm / Tampon Ø600 mm", "icon": "🔘"
    },
    {
        "id": "mat_04", "category": "voirie_fonte", "name": "Grille Avaloir Fonte Concave C250 (500x500 mm)",
        "fournisseur": "Saint-Gobain PAM Canalisation", "unit": "u", "prix_unitaire": 98.00,
        "conditionnement": "Palette de 12 unités", "norme": "NF EN 124 / 250 kN Eaux Pluviales",
        "stock": "0 u (Rupture)", "stock_status": "out_of_stock", "poids": "38 kg / pièce", "dimensions": "500 x 500 mm", "icon": "🔲"
    },
    {
        "id": "mat_05", "category": "tuyaux", "name": "Tuyau Fonte Ductile DN400 Integral (L=6.00m)",
        "fournisseur": "Saint-Gobain PAM Canalisation", "unit": "ml", "prix_unitaire": 115.00,
        "conditionnement": "Fardeau 3 tuyaux (18 ml)", "norme": "Fascicule 70-1 / Revêtement Zinc-Alu",
        "stock": "180 ml", "stock_status": "in_stock", "poids": "102 kg / ml", "dimensions": "Longueur 6,00 m / Øint 400 mm", "icon": "💧"
    },
    {
        "id": "mat_06", "category": "tuyaux", "name": "Tuyau PVC Assainissement CR8 Ø200 (L=3.00m)",
        "fournisseur": "PUM Plastiques Sète", "unit": "ml", "prix_unitaire": 18.50,
        "conditionnement": "Palette de 60 ml", "norme": "NF EN 1401 / CR8 Résistance accrue",
        "stock": "420 ml", "stock_status": "in_stock", "poids": "4.8 kg / ml", "dimensions": "Longueur 3,00 m / Ø 200 mm", "icon": "💧"
    },
    {
        "id": "mat_07", "category": "tuyaux", "name": "Tube PEHD Gaz 100mm Bande Jaune SDR11",
        "fournisseur": "PUM Plastiques Sète", "unit": "ml", "prix_unitaire": 22.00,
        "conditionnement": "Couronne de 50 ml ou barre 12m", "norme": "NF EN 1555 / 4 bars MPB",
        "stock": "En cours de livraison (100 ml)", "stock_status": "in_transit", "poids": "3.1 kg / ml", "dimensions": "Øext 110 mm / SDR 11", "icon": "⚡"
    },
    {
        "id": "mat_08", "category": "granulats", "name": "Grave Non Traitée GNT 0/31.5 Classe A",
        "fournisseur": "Carrières du Languedoc", "unit": "tonne", "prix_unitaire": 16.50,
        "conditionnement": "Vrac Semi-remorque 30t", "norme": "NF EN 13285 / GTR 2000",
        "stock": "1 250 t", "stock_status": "in_stock", "poids": "Masse volumique foisonnée 1.75 t/m³", "dimensions": "Granulométrie 0/31.5 mm", "icon": "🪨"
    },
    {
        "id": "mat_09", "category": "granulats", "name": "Gravillon Concassé Lavé 4/10 (Lit de Pose)",
        "fournisseur": "Carrières du Languedoc", "unit": "tonne", "prix_unitaire": 21.00,
        "conditionnement": "Vrac Porteur 8x4 18t", "norme": "Fascicule 70-1 Titre I",
        "stock": "450 t", "stock_status": "in_stock", "poids": "Masse volumique 1.55 t/m³", "dimensions": "Calibre 4/10 mm", "icon": "🪨"
    },
    {
        "id": "mat_10", "category": "beton", "name": "Béton Prêt à l'Emploi C25/30 XF1 / S3",
        "fournisseur": "Bétons Occitanie Méditerranée", "unit": "m³", "prix_unitaire": 128.00,
        "conditionnement": "Toupie malaxeuse 8 m³", "norme": "NF EN 206 / Bordures & Calages",
        "stock": "Sur commande (Livrable sous 2h)", "stock_status": "in_stock", "poids": "2 350 kg / m³", "dimensions": "Affaissement cône d'Abrams 160 mm (S3)", "icon": "🧱"
    },
    {
        "id": "mat_11", "category": "enrobes", "name": "Enrobé Bitumineux BBSG 0/10 Classe 3 (160°C)",
        "fournisseur": "Enrobés du Sud (Centrale Alès)", "unit": "tonne", "prix_unitaire": 82.00,
        "conditionnement": "Camion calorifugé 30t", "norme": "NF P98-150 / Roulement",
        "stock": "Fabrication continue en centrale", "stock_status": "in_stock", "poids": "Densité compactée 2.35 t/m³", "dimensions": "Épaisseur d'application 5 à 7 cm", "icon": "🛣️"
    },
    {
        "id": "mat_12", "category": "geotextiles", "name": "Géotextile Non-Tissé Anti-Contaminant 200g/m²",
        "fournisseur": "PUM Plastiques Sète", "unit": "m²", "prix_unitaire": 1.45,
        "conditionnement": "Rouleau 2.00m x 100m (200 m²)", "norme": "Classe 4 / ASQUAL",
        "stock": "800 m²", "stock_status": "in_stock", "poids": "200 g / m²", "dimensions": "Largeur 2,00 m x Longueur 100 m", "icon": "📜"
    }
]

# Standard Tools Catalog
extra_data['tool_catalog'] = [
    {
        "id": "tool_01", "category": "terrassement", "task": "terrassement",
        "name": "Pelle sur Chenilles 24T (Liebherr R924 / CAT 320 GC)",
        "description": "Pelle hydraulique de production équipée godet rétro 1200L, attache rapide hydraulique et guidage GPS 3D Trimble.",
        "prix_achat_neuf": "245 000.00 €", "tarif_location_jour": "650.00 € / jour", "conso_moyenne": "22.5 L/h GNR",
        "rendement": "65 m³/h en tranchée", "stock_status": "in_stock", "stock": "2 en parc", "poids": "24 500 kg", "dimensions": "9.50 x 2.98 x 3.10 m", "norme": "CE / Stage V Faibles Émissions", "icon": "🚜"
    },
    {
        "id": "tool_02", "category": "compactage", "task": "compactage",
        "name": "Compacteur Tandem Vibrant Bomag BW 120 AD-5",
        "description": "Cylindre vibrant double bille acier 120cm pour couches de fondation GNT et enrobés de roulement avec arrosage sous pression.",
        "prix_achat_neuf": "48 000.00 €", "tarif_location_jour": "180.00 € / jour", "conso_moyenne": "6.8 L/h GNR",
        "rendement": "450 m²/h (Objectif q4)", "stock_status": "in_stock", "stock": "2 en parc", "poids": "2 700 kg", "dimensions": "2.50 x 1.28 x 1.80 m", "norme": "CE / Norme NF P 98-736", "icon": "🔨"
    },
    {
        "id": "tool_03", "category": "transport", "task": "transport",
        "name": "Camion Porteur 8x4 Scania G450 Bi-Benne HARDOX",
        "description": "Porteur lourd 32 tonnes PTAC, bibenne en acier HARDOX 450 résistant à l'abrasion et bâche électrique automatique.",
        "prix_achat_neuf": "165 000.00 €", "tarif_location_jour": "420.00 € / jour", "conso_moyenne": "38.0 L/100km",
        "rendement": "18 tonnes / rotation", "stock_status": "in_stock", "stock": "3 en parc", "poids": "14 200 kg à vide / 32 000 kg PTAC", "dimensions": "8.90 x 2.55 x 3.40 m", "norme": "Euro 6d / Caméra 360°", "icon": "🚛"
    },
    {
        "id": "tool_04", "category": "topographie", "task": "topographie",
        "name": "Laser de Canalisation Automatique Piper 100",
        "description": "Laser d'alignement étanche IPX8 en fonte d'aluminium avec faisceau vert ultra-lumineux pour pose précise des collecteurs EU/EP.",
        "prix_achat_neuf": "4 200.00 €", "tarif_location_jour": "45.00 € / jour", "conso_moyenne": "Batterie Li-Ion 40h",
        "rendement": "Précision ± 1.5 mm à 30 m", "stock_status": "in_stock", "stock": "3 unités", "poids": "5.4 kg", "dimensions": "Ø 100 mm x 320 mm", "norme": "Laser Classe 3R / IP68 submersible", "icon": "🎯"
    },
    {
        "id": "tool_05", "category": "sciage", "task": "sciage",
        "name": "Découpeuse Thermique Disque Diamant Stihl TS 420",
        "description": "Découpeuse portative à essence 2-temps avec disque diamant Ø 350 mm et raccord arrosage pour sciage d'enrobé et bordures.",
        "prix_achat_neuf": "1 350.00 €", "tarif_location_jour": "35.00 € / jour", "conso_moyenne": "1.2 L/h Mélange 2%",
        "rendement": "Profondeur de coupe 125 mm", "stock_status": "in_stock", "stock": "4 unités", "poids": "9.6 kg", "dimensions": "720 x 280 x 390 mm", "norme": "CE / Filtre cyclonique HD2", "icon": "⚙️"
    },
    {
        "id": "tool_06", "category": "sciage", "task": "sciage",
        "name": "Scie à Sol Diamant Autotractée Golz FS 170",
        "description": "Scie à sol thermique 13 CV pour tranchées nettes dans les enrobés et bétons avant terrassement.",
        "prix_achat_neuf": "3 800.00 €", "tarif_location_jour": "75.00 € / jour", "conso_moyenne": "2.8 L/h SP98",
        "rendement": "Profondeur de coupe 190 mm", "stock_status": "in_stock", "stock": "1 unité", "poids": "115 kg", "dimensions": "1100 x 550 x 950 mm", "norme": "CE / Réservoir d'eau 25L intégré", "icon": "⚙️"
    },
    {
        "id": "tool_07", "category": "manutention", "task": "pose_bordures",
        "name": "Pince à Bordures Manuelle Réglable Probst VZ",
        "description": "Pince à ciseaux avec patins en caoutchouc vulcanisé pour préhension et pose ergonomique de bordures T2, A2 et caniveaux.",
        "prix_achat_neuf": "290.00 €", "tarif_location_jour": "12.00 € / jour", "conso_moyenne": "Manuelle 2 opérateurs",
        "rendement": "Capacité 100 kg / Ouverture 500-1045 mm", "stock_status": "in_stock", "stock": "6 unités", "poids": "12 kg", "dimensions": "1100 x 300 x 150 mm", "norme": "Conformité CE / Prévention TMS", "icon": "🔧"
    },
    {
        "id": "tool_08", "category": "outillage_main", "task": "pose_bordures",
        "name": "Massette TP Manche Composite Tri-Matière 1.5kg",
        "description": "Massette de maçon TP anti-vibrations avec tête forgée en acier traité et poignée ergonomique anti-glisse.",
        "prix_achat_neuf": "32.00 €", "tarif_location_jour": "Inclus lot équipier", "conso_moyenne": "Manuel",
        "rendement": "Frappe amortie", "stock_status": "in_stock", "stock": "12 unités", "poids": "1.5 kg", "dimensions": "Longueur manche 280 mm", "norme": "NF ISO 15601", "icon": "🔨"
    },
    {
        "id": "tool_09", "category": "securite_epi", "task": "securite",
        "name": "Pack EPI Réglementaire BTP Complet (Casque, Gilet, S3, Gants)",
        "description": "Kit individuel comprenant casque avec jugulaire NF EN 397, gilet haute visibilité classe 3 EN ISO 20471, chaussures S3 SRC anti-perforation et gants niveau D.",
        "prix_achat_neuf": "185.00 €", "tarif_location_jour": "Dotation obligatoire entreprise", "conso_moyenne": "Renouvellement annuel",
        "rendement": "Protection 100% des compagnons", "stock_status": "in_stock", "stock": "25 packs en réserve", "poids": "3.8 kg le kit complet", "dimensions": "Tailles du S au XXL / Pointures 38-47", "norme": "NF EN 397 / EN ISO 20471 / EN ISO 20345", "icon": "🦺"
    },
    {
        "id": "tool_10", "category": "terrassement", "task": "terrassement",
        "name": "Robot de Démolition Électrique Husqvarna DXR 300",
        "description": "Robot compact télécommandé sur chenilles caoutchouc équipé brise-roche hydraulique pour travaux en milieu confiné ou dangereux.",
        "prix_achat_neuf": "140 000.00 €", "tarif_location_jour": "550.00 € / jour", "conso_moyenne": "22 kW Électrique 400V",
        "rendement": "Portée 5.2 m / Frappe 410 J", "stock_status": "in_stock", "stock": "1 unité", "poids": "1 960 kg", "dimensions": "2.05 x 0.78 x 1.37 m", "norme": "CE / Télécommande radio portée 100m", "icon": "🤖"
    },
    {
        "id": "tool_11", "category": "drone", "task": "topographie",
        "name": "Drone de Relevé Topographique DJI Matrice 350 RTK + LiDAR Zenmuse L2",
        "description": "Système aérien de photogrammétrie et LiDAR géoréférencé centimétrique RGF93 pour MNT et calcul de cubatures de déblais/remblais.",
        "prix_achat_neuf": "32 000.00 €", "tarif_location_jour": "400.00 € / jour", "conso_moyenne": "Autonomie 55 min / 2 accus TB65",
        "rendement": "250 hectares / vol à 100m", "stock_status": "in_stock", "stock": "1 unité", "poids": "6.47 kg avec charge utile", "dimensions": "810 x 670 x 430 mm déplié", "norme": "Catégorie Ouverte / Scénario S1-S2-S3 DGAC", "icon": "🛸"
    },
    {
        "id": "tool_12", "category": "ergonomie", "task": "pose_bordures",
        "name": "Exosquelette de Portage Lombaire HAPO Ergonomie",
        "description": "Exosquelette passif à ressorts composites réduisant de 30% la pression sur les vertèbres lombaires lors de la manutention des bordures.",
        "prix_achat_neuf": "1 850.00 €", "tarif_location_jour": "25.00 € / jour", "conso_moyenne": "Zéro énergie externe (Passif)",
        "rendement": "Réduction de 70% des arrêts TMS", "stock_status": "in_stock", "stock": "4 unités", "poids": "1.2 kg", "dimensions": "Ajustable morphologie opérateur", "norme": "Dispositif ergonomique certifié INRS", "icon": "🦾"
    }
]

# Agenda Tasks dataset for Week S38 (15-21 Septembre 2026)
extra_data['agenda_tasks'] = [
    {
        "id": "ag_01", "day": "lundi", "date_str": "Lundi 21 Sept 2026", "time_slot": "07h30 - 12h00",
        "project": "Giratoire RD906 Alès", "project_id": "projet_ales", "color": "#06b6d4",
        "task": "Pose Bordures T2 & Caniveaux CC1 sur ilot central", "progress": 85,
        "team": "A. Martin (Chef) + 3 compagnons", "machines": "Pelle Cat 320 GC + Pince hydraulique Probst",
        "aipr_alert": "DICT Gaz MPB à 1.50m (vigilance godet)", "status": "En cours"
    },
    {
        "id": "ag_02", "day": "lundi", "date_str": "Lundi 21 Sept 2026", "time_slot": "13h00 - 17h00",
        "project": "ZAC Littoral Sète", "project_id": "projet_sete", "color": "#10b981",
        "task": "Tranchée blindée SBH & Rabattement de nappe", "progress": 45,
        "team": "M. Gomez (Chef) + K. Benali + 3 ouvriers", "machines": "Pelle Liebherr 24T + Pompe d'épuisement 120m³/h",
        "aipr_alert": "Nappe à -1.20m, pompage continu actif", "status": "En cours"
    },
    {
        "id": "ag_03", "day": "mardi", "date_str": "Mardi 22 Sept 2026", "time_slot": "07h30 - 12h00",
        "project": "Giratoire RD906 Alès", "project_id": "projet_ales", "color": "#06b6d4",
        "task": "Réglage fin GNT 0/31.5 & Essais à la plaque Dynaplaque (EV2 > 80 MPa)", "progress": 90,
        "team": "A. Martin + Géomètre Topographe", "machines": "Compacteur Bomag BW 120 + Camion 8x4 Scania (Lest 14t)",
        "aipr_alert": "Contrôle de compactage validé par laboratoire", "status": "Planifié"
    },
    {
        "id": "ag_04", "day": "mardi", "date_str": "Mardi 22 Sept 2026", "time_slot": "13h00 - 17h00",
        "project": "Centre Ancien Pézenas", "project_id": "projet_pezenas", "color": "#a855f7",
        "task": "Pavage en pierre calcaire locale & Raccordement EU boîte de branchement", "progress": 95,
        "team": "S. Lacombe (Chef) + 2 compagnons paveurs", "machines": "Mini-pelle Kubota 2.5T + Dumper 1.5T",
        "aipr_alert": "Ruelle piétonne protégée par barrières Nadar", "status": "Planifié"
    },
    {
        "id": "ag_05", "day": "mercredi", "date_str": "Mercredi 23 Sept 2026", "time_slot": "07h30 - 17h00",
        "project": "Giratoire RD906 Alès", "project_id": "projet_ales", "color": "#06b6d4",
        "task": "Application Couche de Roulement BBSG 0/10 (160°C - 350 tonnes)", "progress": 10,
        "team": "S. Cabrol (Conducteur) + Équipe Enrobés (6 ouvriers)", "machines": "Finisseur Vögele Super 1800 + Cylindre BW120 + 4x Camions 8x4",
        "aipr_alert": "Arrêté de circulation temporaire avec alternat feux KR11j", "status": "Planifié"
    },
    {
        "id": "ag_06", "day": "jeudi", "date_str": "Jeudi 24 Sept 2026", "time_slot": "07h30 - 12h00",
        "project": "Voie Verte Montpellier", "project_id": "projet_montpellier", "color": "#f59e0b",
        "task": "Mise en œuvre enrobé tiède bas carbone couleur ocre (L=800 ml)", "progress": 60,
        "team": "M. Gomez + 3 compagnons", "machines": "Mini-finisseur + Cylindre tandem",
        "aipr_alert": "Espace naturel sensible Natura 2000", "status": "Planifié"
    },
    {
        "id": "ag_07", "day": "jeudi", "date_str": "Jeudi 24 Sept 2026", "time_slot": "13h00 - 17h00",
        "project": "ZAC Littoral Sète", "project_id": "projet_sete", "color": "#10b981",
        "task": "Pose Collecteur Fonte Ductile DN400 Integral (60 ml posés)", "progress": 30,
        "team": "K. Benali (Canalisateur) + 3 ouvriers", "machines": "Pelle Liebherr 24T + Laser Piper 100",
        "aipr_alert": "Pente laser contrôlée à 1.25% fil d'eau", "status": "Planifié"
    },
    {
        "id": "ag_08", "day": "vendredi", "date_str": "Vendredi 25 Sept 2026", "time_slot": "07h30 - 12h00",
        "project": "Portfolio Multi-Chantiers", "project_id": "projet_ales", "color": "#38bdf8",
        "task": "Réunion de chantier hebdomadaire MOE / CSPS & Visite de sécurité AIPR", "progress": 100,
        "team": "S. Cabrol + A. Martin + Coordonnateur SPS", "machines": "Véhicule d'encadrement Renault Kangoo ZE",
        "aipr_alert": "Validation des fiches d'accueil et registres de sécurité", "status": "Planifié"
    },
    {
        "id": "ag_09", "day": "vendredi", "date_str": "Vendredi 25 Sept 2026", "time_slot": "13h00 - 16h30",
        "project": "Tous Chantiers", "project_id": "projet_sete", "color": "#64748b",
        "task": "Repli sécurisé de fin de semaine, vérification balisage OPBTP & consignation engins", "progress": 100,
        "team": "Ensemble des équipes de chantier", "machines": "Flotte complète en position de sécurité",
        "aipr_alert": "Clôture et cadenas sur accès chantiers", "status": "Planifié"
    }
]

# Add SVGs to fleet and catalog items
for v in extra_data.get('fleet', []):
    v['svg_illustration'] = get_vehicle_svg(v.get('type', '') + ' ' + v.get('name', ''))

for m in extra_data.get('materials_catalog', []):
    m['svg_illustration'] = get_tool_material_svg(m.get('id', ''), m.get('name', ''))

for t in extra_data.get('tool_catalog', []):
    t['svg_illustration'] = get_tool_material_svg(t.get('id', ''), t.get('name', ''))

print("All datasets and SVGs prepared.")
