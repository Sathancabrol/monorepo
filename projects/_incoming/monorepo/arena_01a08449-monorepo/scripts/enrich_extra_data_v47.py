import json

from scripts.generate_extra_data import get_company_data
data = get_company_data()

# 1. Enrich suppliers list with marketplace metrics (distance, price index, rating, phone, contact)
data["suppliers"] = [
    {
        "id": "sup_01",
        "name": "Carrières & Granulats du Languedoc",
        "specialty": "Grave GNT 0/31.5, Gravillons 4/10, Sables alluvionnaires",
        "location": "Frontignan / Villeveyrac (34)",
        "distance_km": 14,
        "price_index": "€€ (Très compétitif)",
        "price_level": 2,
        "quality_rating": 4.8,
        "delivery_delay": "Livraison 24h ou retrait direct",
        "phone": "04 67 18 22 10",
        "email": "commandes@carrieres-languedoc.fr",
        "active_orders": 3
    },
    {
        "id": "sup_02",
        "name": "Bétons Occitanie Méditerranée",
        "specialty": "Bétons Prêts à l'Emploi C25/30 XF1, Béton désactivé, Mortiers",
        "location": "Sète / ZI des Eaux Blanches",
        "distance_km": 6,
        "price_index": "€€€ (Standard NF)",
        "price_level": 3,
        "quality_rating": 4.9,
        "delivery_delay": "Toupie sous 2h (Centrale locale)",
        "phone": "04 67 46 80 00",
        "email": "contact@betons-occitanie.fr",
        "active_orders": 5
    },
    {
        "id": "sup_03",
        "name": "Saint-Gobain PAM Canalisation",
        "specialty": "Tuyaux Fonte Ductile DN100 à DN600, Tampons D400, Grilles C250",
        "location": "Dépôt Régional Montpellier / Vendargues",
        "distance_km": 28,
        "price_index": "€€€ (Haute résistance)",
        "price_level": 3,
        "quality_rating": 5.0,
        "delivery_delay": "Livraison sur chantier sous 48h",
        "phone": "04 67 87 90 00",
        "email": "commercial.sud@saint-gobain.com",
        "active_orders": 2
    },
    {
        "id": "sup_04",
        "name": "PUM Plastiques & Réseaux Sète",
        "specialty": "Tubes PVC CR8 Ø200/Ø300, PEHD Gaz SDR11, Gaines TPC, Géotextiles",
        "location": "Sète / Zone d'Activité",
        "distance_km": 4,
        "price_index": "€€ (Tarif Pro Négocié)",
        "price_level": 2,
        "quality_rating": 4.7,
        "delivery_delay": "Dispo comptoir immédiate ou navette matin",
        "phone": "04 67 43 12 34",
        "email": "agence.sete@mypum.fr",
        "active_orders": 4
    },
    {
        "id": "sup_05",
        "name": "Enrobés Bitumineux du Sud (Centrale Alès)",
        "specialty": "Enrobé à chaud BBSG 0/10 Classe 3, Enrobé Tiède Bas Carbone, EB8",
        "location": "Alès / Saint-Martin-de-Valgalgues (30)",
        "distance_km": 18,
        "price_index": "€€ (Direct usine)",
        "price_level": 2,
        "quality_rating": 4.8,
        "delivery_delay": "Semi calorifugée départ centrale 160°C",
        "phone": "04 66 56 44 20",
        "email": "enrobes.sud@eurovia.com",
        "active_orders": 1
    }
]

# 2. Enrich standard tools in tool catalog with stock badges and specs
data["tool_catalog"].extend([
    {
        "id": "cat_tool_01",
        "task": "outillage_main",
        "task_label": "🔨 Outillage Standard & Manutention",
        "name": "Massette TP 1.5kg & Marteau de Coffreur",
        "category": "Outillage Standard",
        "description": "Massette manche tri-matière incassable pour frappe de piquets et réglage de bordures. Tête en acier forgé trempé.",
        "prix_achat_neuf": "18.50 €",
        "tarif_location_jour": "Inclus boîte à outils",
        "conso_moyenne": "Manuelle",
        "rendement": "Usage continu",
        "caces": "Sensibilisation EPI",
        "impact_qualite": "Frappe précise sans éclat",
        "stock_status": "in_stock",
        "stock_qty": "18 unités en stock",
        "weight": "1.5 kg",
        "supplier": "Quincaillerie Pro TP Sète",
        "icon": "🔨"
    },
    {
        "id": "cat_tool_02",
        "task": "bordures",
        "task_label": "📐 Pose de Bordures & Caniveaux",
        "name": "Pince à Bordures Autobloquante Manuelle Probst",
        "category": "Outillage Standard",
        "description": "Pince de préhension mécanique à double serrage pour pose de bordures T2, A2, P1 jusqu'à 150 kg à deux compagnons.",
        "prix_achat_neuf": "280.00 €",
        "tarif_location_jour": "15 € / jour",
        "conso_moyenne": "Mécanique",
        "rendement": "40 ml / h",
        "caces": "Formation Gestes & Postures",
        "impact_qualite": "Zéro écornure des bordures",
        "stock_status": "in_stock",
        "stock_qty": "6 paires en stock",
        "weight": "8.5 kg",
        "supplier": "Probst BTP Distribution",
        "icon": "🗜️"
    },
    {
        "id": "cat_tool_03",
        "task": "sciage",
        "task_label": "⚡ Sciage & Découpe Béton / Enrobé",
        "name": "Découpeuse Thermique à Disque Stihl TS420 Ø350",
        "category": "Outillage Électroportatif",
        "description": "Tronçonneuse thermique pour découpe nette d'enrobé, tuyaux fonte et béton. Système d'arrosage eau anti-poussière.",
        "prix_achat_neuf": "1 250.00 €",
        "tarif_location_jour": "45 € / jour",
        "conso_moyenne": "1.2 L/h Mélange 2T",
        "rendement": "25 ml/h coupe 12cm",
        "caces": "Notice fabricant & Port EPI",
        "impact_qualite": "Bords de saignée parfaitement verticaux",
        "stock_status": "in_transit",
        "stock_qty": "En réappro (Livraison prévue 24h)",
        "weight": "9.6 kg",
        "supplier": "Stihl Pro Méditerranée",
        "icon": "🪚"
    },
    {
        "id": "cat_tool_04",
        "task": "sciage",
        "task_label": "⚡ Sciage & Découpe Béton / Enrobé",
        "name": "Scie à Sol Diamantée Thermique Husqvarna FS400",
        "category": "Outillage Lourd",
        "description": "Scie à sol poussée sur roues avec disque diamant Ø450mm pour tranchées longues et joints de dilatation réguliers.",
        "prix_achat_neuf": "3 400.00 €",
        "tarif_location_jour": "90 € / jour",
        "conso_moyenne": "2.5 L/h SP98",
        "rendement": "60 ml/h coupe 16cm",
        "caces": "Formation Sécurité Sciage",
        "impact_qualite": "Profondeur constante guidée",
        "stock_status": "in_stock",
        "stock_qty": "2 unités disponibles",
        "weight": "99 kg",
        "supplier": "Husqvarna Construction France",
        "icon": "⚙️"
    },
    {
        "id": "cat_tool_05",
        "task": "securite_epi",
        "task_label": "🦺 Équipements de Protection Individuelle (EPI)",
        "name": "Pack EPI Chantier TP Complet (Casque, Gilet Cl3, Gants, S3)",
        "category": "Sécurité & Protection",
        "description": "Kit complet réglementaire : Casque NF EN 397 avec jugulaire, Gilet haute visibilité Classe 3, Chaussures S3 anti-perforation, Gants anti-coupure D, Lunettes solaires et bouchons d'oreille.",
        "prix_achat_neuf": "145.00 €",
        "tarif_location_jour": "Dotation salarié obligatoire",
        "conso_moyenne": "Usage individuel",
        "rendement": "100% Protection",
        "caces": "Obligatoire sur tous chantiers",
        "impact_qualite": "0 accident corporel",
        "stock_status": "in_stock",
        "stock_qty": "24 packs neufs au magasin",
        "weight": "2.2 kg",
        "supplier": "Protect BTP Languedoc",
        "icon": "🦺"
    },
    {
        "id": "cat_tool_06",
        "task": "tranchee",
        "task_label": "💧 Laser & Guidage de Canalisations",
        "name": "Laser de Canalisation Piper 100 Rouge & Mire Automatique",
        "category": "Topographie & Guidage",
        "description": "Laser compact étanche IPX8 s'insérant directement dans le tuyau DN150 à DN600 pour contrôle permanent de la pente.",
        "prix_achat_neuf": "2 100.00 €",
        "tarif_location_jour": "50 € / jour",
        "conso_moyenne": "Batterie Li-Ion 40h",
        "rendement": "Précision ±0.005%",
        "caces": "Formation AIPR",
        "impact_qualite": "Pente au millimètre sans contre-pente",
        "stock_status": "in_stock",
        "stock_qty": "3 kits disponibles",
        "weight": "4.8 kg",
        "supplier": "Leica Geosystems France",
        "icon": "🔴"
    },
    {
        "id": "cat_tool_07",
        "task": "outillage_main",
        "task_label": "⛏️ Traçage & Implantation",
        "name": "Bombe de Peinture de Traçage Fluo TP 360° (Lot de 12)",
        "category": "Consommable Chantier",
        "description": "Aérosol de marquage au sol haute tenue pour piquetage DICT, réseaux sensibles et alignement bordures. Tenue 6 mois.",
        "prix_achat_neuf": "68.00 € / carton",
        "tarif_location_jour": "Consommable",
        "conso_moyenne": "1 bombe / 100 ml",
        "rendement": "Séchage 5 min",
        "caces": "Code couleur normalisé AFNOR",
        "impact_qualite": "Visibilité immédiate des réseaux",
        "stock_status": "out_of_stock",
        "stock_qty": "En rupture (Réappro sous 3j)",
        "weight": "5.5 kg",
        "supplier": "Soppec / Quincaillerie Pro",
        "icon": "🎨"
    }
])

# Write updated file
new_content = f"""import json

def get_company_data():
    return {json.dumps(data, indent=4, ensure_ascii=False)}
"""

with open("/home/user/monorepo/scripts/generate_extra_data.py", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Enriched generate_extra_data.py with suppliers and new standard tools successfully!")
