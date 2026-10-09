# -*- coding: utf-8 -*-
import json
import os
import sys

print("Patching section_js_part1.py, section_js_part2.py, section_js_part3.py and section_modals.py with authentic Colas Agence de Sète data...")

# ==============================================================================
# 1. UPDATE section_js_part1.py
# ==============================================================================
with open('scripts/section_js_part1.py', 'r', encoding='utf-8') as f:
    js1 = f.read()

# Replace global userAccountState
old_user_state = """    window.userAccountState = {
        userName: 'Jean DUPONT',
        userRole: 'direction',
        companyKey: 'occitanie_tp',
        companyName: 'Occitanie TP & VRD',
        treasury: 485200,
        headcount: 24,
        projectsCount: 4,
        fleetCount: 6,
        qseScore: 98.5
    };"""

new_user_state = """    window.userAccountState = {
        userName: 'Romain CARAÏ',
        userRole: 'direction',
        companyKey: 'colas_sete',
        companyName: 'Colas Agence Sète & Bassin de Thau',
        treasury: 1450000,
        headcount: 68,
        projectsCount: 4,
        fleetCount: 14,
        qseScore: 98.5
    };"""

js1 = js1.replace(old_user_state, new_user_state)

# Replace ticker update in updateAllHudAndTickerMetrics
old_ticker_txt = "ticker.textContent = '📢 ' + s.companyName + ' • Direction : ' + s.userName + ' • Caisse Active : ' + new Intl.NumberFormat('fr-FR').format(s.treasury) + ' € • Effectif : ' + s.headcount + ' salariés • Chantiers : ' + s.projectsCount + ' actifs (Barbazan, Aurouer, Sète).';"
new_ticker_txt = "ticker.textContent = '📢 ' + s.companyName + ' • Direction : ' + s.userName + ' • Caisse Active : ' + new Intl.NumberFormat('fr-FR').format(s.treasury) + ' € • Effectif : ' + s.headcount + ' salariés • Chantiers : ' + s.projectsCount + ' actifs (Quai Richelieu, Voie Verte Thau, Caraussane, RD600).';"
js1 = js1.replace(old_ticker_txt, new_ticker_txt)

# Replace ticker modes
old_modes_block = """        if (mode === 'general') {
            track.textContent = '📢 GÉNÉRAL : ' + s.companyName + ' • Marché Giratoire Barbazan notifié • Réception terrassement Aurouer validée • DICT AEP Sète conforme.';
        } else if (mode === 'finance') {
            track.textContent = '💰 FINANCE : Caisse active ' + formattedCaisse + ' € • Situation Chorus Pro n°4 encaissée (+42 500 €) • Déblocage retenue de garantie 5% • Marge moyenne 14.8%.';
        } else if (mode === 'security') {
            track.textContent = '🚨 SÉCURITÉ & QSE : Alerte météo vent 50 km/h bassin de Thau • Conformité blindage tranchées 100% • Score AIPR 100% • 0 accident sur 365j.';
        } else if (mode === 'logistics') {
            track.textContent = '🚛 LOGISTIQUE : ' + s.fleetCount + ' engins opérationnels (VGP 100%) • 8 rotations camions 8x4 enrobés BBSG 0/10 • Stock GNT 0/31.5 : 420 Tonnes.';
        }"""

new_modes_block = """        if (mode === 'general') {
            track.textContent = '📢 GÉNÉRAL : ' + s.companyName + ' • Chantier Quai Richelieu (Hydromer) : Enrobés percolés Colstrong en cours • Voie Verte Bouzigues-Sète : Revêtement Colstab Ostrea® validé • Séparation Pluvial Caraussane / Simone Veil active • QSE 98.5%.';
        } else if (mode === 'finance') {
            track.textContent = '💰 FINANCE : Caisse active Colas Sète ' + formattedCaisse + ' € • Acompte Port de Sète n°2 encaissé (340 000 € HT) • Facturation Sète Agglopôle Caraussane validée • Dépenses bitume & centrale Eaux Blanches équilibrées.';
        } else if (mode === 'security') {
            track.textContent = '🚨 SÉCURITÉ & QSE : 0 accident en cours (Score 98.5%) • DICT Enedis/GRDF validée Sète Centre • AIPR 100% à jour • Consigne Vent fort / Tramontane appliquée sur le Port de Sète.';
        } else if (mode === 'logistics') {
            track.textContent = '🚛 LOGISTIQUE : ' + s.fleetCount + ' engins opérationnels (VGP 100%) • 18t BBSG 0/10 expédiées depuis la Centrale Languedoc Enrobés • Rotations 8x4 régulées sur RD600.';
        }"""

js1 = js1.replace(old_modes_block, new_modes_block)

# Replace occitanie_tp block in companyProfilesData with Colas Agence de Sète
start_occ = js1.find("'occitanie_tp': {")
if start_occ != -1:
    end_occ = js1.find("'compte_neuf': {", start_occ)
    if end_occ != -1:
        colas_block = """'occitanie_tp': {
            id: 'colas_sete',
            name: 'Colas Agence Sète & Bassin de Thau',
            type: 'Établissement Secondaire Major TP (Colas France)',
            siret: '329 338 883 01359',
            capital: '1 500 000 € (Colas Midi Méditerranée SA)',
            siege: 'Zone Industrielle des Eaux Blanches, CS 10098, 34200 Sète',
            caisse: 1450000,
            bfr: 420000,
            ca_annuel: 18500000,
            ca_prev: 22400000,
            margin: 14.8,
            effectif_count: 68,
            fleet_count: 14,
            projects_count: 4,
            safety_status: '98.5% Conforme',
            safety_sub: '0 Incident • CSPS & DICT Validés',
            treasury_sub: 'BFR Couvert : 42 jours d\'exploitation',
            projects_sub: 'Quai Richelieu, Voie Verte Thau, Caraussane, RD600',
            effectif_sub: '68 Salariés • AIPR & CACES à jour • Colas Sète',
            desc: 'Établissement Colas Agence de Sète (1052 Av. des Eaux Blanches). Travaux maritimes et portuaires, voiries urbaines, pistes cyclables éco-innovantes Colstab Ostrea® et enrobés spéciaux Colstrong®.',
            
            projects: [
                {
                    id: "p-01",
                    code: "COLAS-SET-2026-01",
                    name: "Port de Sète - Quai Richelieu (Amarrage Drague Hydromer & Colstrong)",
                    type: "internal",
                    ownership: "🏢 Colas Agence Sète (En cours)",
                    badge_type: "Marché Public Actif",
                    loc: "Port de Sète - Quai Richelieu (34200)",
                    location: "Port de Sète - Quai Richelieu (34200)",
                    client: "Région Occitanie / Port Sud de France (Groupement Buesa-Soletanche / Colas)",
                    moe: "BRL Ingénierie / Direction Portuaire",
                    budget: 1850000,
                    spent: 1258000,
                    budget_used: 1258000,
                    progress: 68,
                    status: "En cours",
                    manager: "Romain Caraï",
                    site_chief: "Rémi Bonnefoi",
                    chef: "Rémi Bonnefoi (Chef Établissement: R. Caraï)",
                    workers_count: 12,
                    delai_consomme_pct: 70,
                    start_date: "16/09/2025",
                    end_date: "15/06/2026",
                    end: "15/06/2026",
                    desc: "Aménagement des voiries lourdes de bord à quai pour l'amarrage de la nouvelle drague électrique Hydromer de la Région Occitanie. Application d'enrobés percolés à très haute résistance Colstrong® (procédé breveté Colas avec 1/3 de coquilles d'huîtres recyclées de Thau), bordures T3 d'accostage, raccordement réseaux maritimes et séparateur hydrocarbures.",
                    assigned_machinery: [{ name: "Finisseur Vögele Super 1800-3i" }, { name: "Compacteur Tandem Bomag BW151" }, { name: "Pelle Chenilles 24t Liebherr R924" }],
                    assigned_tools: [{ name: "Centrale mobile percolation Colstrong" }, { name: "Laser de nivellement Piper" }],
                    docs: [{ name: "CCTP_Port_Sete_Richelieu", type: "pdf" }, { name: "Fiche_Technique_Colstrong", type: "pdf" }],
                    lots_breakdown: [
                        { name: "Lot 1 : Terrassement & Purges Quai (3 800 m³)", budget: 380000, progress: 100, ds: 283500, pv: 380000 },
                        { name: "Lot 2 : Assainissement & Séparateur Hydrocarbures", budget: 420000, progress: 85, ds: 313400, pv: 420000 },
                        { name: "Lot 3 : Sous-couche GNT 0/31.5 & Bordures T3", budget: 250000, progress: 75, ds: 186500, pv: 250000 },
                        { name: "Lot 4 : Enrobés Percolés Colstrong aux Coquilles de Thau", budget: 800000, progress: 40, ds: 597000, pv: 800000 }
                    ],
                    steps: [
                        { name: "Piquetage & DICT Maritime validée", progress: 100 },
                        { name: "Terrassement et purge sous nappe", progress: 100 },
                        { name: "Pose collecteur fonte DN300 & séparateur", progress: 85 },
                        { name: "Sous-couche GNT et bordures d'accostage T3", progress: 75 },
                        { name: "Coulage matrice ciment & enrobé percolé Colstrong", progress: 40 }
                    ]
                },
                {
                    id: "p-02",
                    code: "COLAS-SET-2026-02",
                    name: "Voie Verte Bassin de Thau - Piste Cyclable Bouzigues-Sète (Colstab Ostrea)",
                    type: "internal",
                    ownership: "🏢 Colas Agence Sète (En cours)",
                    badge_type: "Marché Public Actif",
                    loc: "Rive Nord Bassin de Thau / Sète - Bouzigues (34)",
                    location: "Rive Nord Bassin de Thau / Sète - Bouzigues (34)",
                    client: "Sète Agglopôle Méditerranée / Ville de Sète",
                    moe: "Direction Aménagement Durable du Territoire Thau",
                    budget: 920000,
                    spent: 772800,
                    budget_used: 772800,
                    progress: 84,
                    status: "Finition",
                    manager: "Sophie Martinez",
                    site_chief: "Jérôme Vidal",
                    chef: "Jérôme Vidal (Conductrice: S. Martinez)",
                    workers_count: 8,
                    delai_consomme_pct: 85,
                    start_date: "03/11/2025",
                    end_date: "30/04/2026",
                    end: "30/04/2026",
                    desc: "Création de 4.2 km de piste cyclable littorale éco-responsable. Mise en œuvre du revêtement innovant Colstab Ostrea® (technologie Colas à base de liant organo-minéral et valorisation conchylicole des coquilles d'huîtres de Thau), stabilisation des berges, passages faune et signalisation touristique.",
                    assigned_machinery: [{ name: "Niveleuse Cat 120M" }, { name: "Compacteur Mixte Bomag BW138" }],
                    assigned_tools: [{ name: "Répandeuse émulsion Colas" }, { name: "Laser rotatif Leica" }],
                    docs: [{ name: "CCTP_VoieVerte_Thau", type: "pdf" }, { name: "Agrément_Colstab_Ostrea", type: "pdf" }],
                    lots_breakdown: [
                        { name: "Lot 1 : Décapage, terrassement & stabilisation talus", budget: 280000, progress: 100, ds: 208000, pv: 280000 },
                        { name: "Lot 2 : Drainage transversal & buses PEHD", budget: 140000, progress: 100, ds: 104000, pv: 140000 },
                        { name: "Lot 3 : Revêtement drainant Colstab Ostrea (14 500 m²)", budget: 420000, progress: 75, ds: 313000, pv: 420000 },
                        { name: "Lot 4 : Signalétique & glissières bois-métal", budget: 80000, progress: 50, ds: 59000, pv: 80000 }
                    ],
                    steps: [
                        { name: "Piquetage environnemental & balisage", progress: 100 },
                        { name: "Terrassement fond de forme & reprofilage talus", progress: 100 },
                        { name: "Couche de forme GNT 0/20 non traitée", progress: 100 },
                        { name: "Application revêtement Colstab Ostrea", progress: 75 },
                        { name: "Pose glissières bois-métal et signalisation", progress: 50 }
                    ]
                },
                {
                    id: "p-03",
                    code: "COLAS-SET-2026-03",
                    name: "Sète Centre - Réseaux & Voiries Rues Caraussane & de Gaulle",
                    type: "internal",
                    ownership: "🏢 Colas Agence Sète (En cours)",
                    badge_type: "Marché Public Actif",
                    loc: "Centre-Ville / Mont Saint-Clair, Sète (34200)",
                    location: "Centre-Ville / Mont Saint-Clair, Sète (34200)",
                    client: "Sète Agglopôle Méditerranée (Cycle de l'Eau) & Ville de Sète",
                    moe: "Bureau d'Études SEIRI / Direction Eau Thau",
                    budget: 1420000,
                    spent: 596400,
                    budget_used: 596400,
                    progress: 42,
                    status: "En cours",
                    manager: "Rémi Bonnefoi",
                    site_chief: "Bruno Dupuis",
                    chef: "Bruno Dupuis (Conducteur: R. Bonnefoi)",
                    workers_count: 9,
                    delai_consomme_pct: 45,
                    start_date: "21/09/2025",
                    end_date: "30/05/2027",
                    end: "30/05/2027",
                    desc: "Mise en séparatif des réseaux pluviaux et eaux usées du bassin versant Mont Saint-Clair (13 ha), raccordement au réservoir Simone Veil réhabilité (1 500 m³), renouvellement conduites fonte DN300/DN600, tranchées blindées urbaines, puis réfection totale voirie en BBSG 0/10 et trottoirs en béton désactivé.",
                    assigned_machinery: [{ name: "Pelle Urbaine Mecalac 12MTX" }, { name: "Minipelle Yanmar SV26" }, { name: "Camion 6x4 bi-benne MAN" }],
                    assigned_tools: [{ name: "Caissons de blindage SBH" }, { name: "Laser Piper 200" }],
                    docs: [{ name: "DICT_Enedis_Sète_Centre", type: "pdf" }, { name: "Plan_Deviation_Circulation", type: "pdf" }],
                    lots_breakdown: [
                        { name: "Lot 1 : Tranchées blindées & Conduite Pluviale DN600", budget: 520000, progress: 60, ds: 388000, pv: 520000 },
                        { name: "Lot 2 : Renouvellement Réseau EU & Branchements AEP", budget: 380000, progress: 45, ds: 283500, pv: 380000 },
                        { name: "Lot 3 : Raccordement Bassin Tampon Simone Veil", budget: 220000, progress: 30, ds: 164000, pv: 220000 },
                        { name: "Lot 4 : Réfection Chaussée BBSG 0/10 & Trottoirs", budget: 300000, progress: 10, ds: 223800, pv: 300000 }
                    ],
                    steps: [
                        { name: "Mise en place déviations & DICT", progress: 100 },
                        { name: "Fouilles blindées Rue de la Caraussane", progress: 60 },
                        { name: "Pose fonte DN600 vers réservoir Simone Veil", progress: 50 },
                        { name: "Branchements particuliers & déconnexion toitures", progress: 40 },
                        { name: "Rabotage et réfection chaussée BBSG 0/10", progress: 10 }
                    ]
                },
                {
                    id: "p-04",
                    code: "COLAS-SET-2026-04",
                    name: "Marché d'Entretien Routier RD600 / RD612 & Liaisons Bassin de Thau",
                    type: "internal",
                    ownership: "🏢 Colas Agence Sète (Accord-cadre)",
                    badge_type: "Marché Public Actif",
                    loc: "Axe Sète - Frontignan - Balaruc - Saint-Thibéry (34)",
                    location: "Axe Sète - Frontignan - Balaruc - Saint-Thibéry (34)",
                    client: "Conseil Départemental de l'Hérault (CD34)",
                    moe: "Direction des Routes et Mobilités 34",
                    budget: 3200000,
                    spent: 960000,
                    budget_used: 960000,
                    progress: 30,
                    status: "En cours",
                    manager: "Romain Caraï",
                    site_chief: "Marc Bellegarde",
                    chef: "Marc Bellegarde (Conducteur: R. Caraï)",
                    workers_count: 14,
                    delai_consomme_pct: 32,
                    start_date: "01/01/2026",
                    end_date: "31/12/2028",
                    end: "31/12/2028",
                    desc: "Accord-cadre triennal à bons de commande pour le rabotage fin 5cm sous circulation de nuit, purges locales, et application d'enrobés très minces BBTM 0/10 et BBSG 0/10 formulés à la centrale Colas Sète - ZI Eaux Blanches avec 30% d'agrégats recyclés.",
                    assigned_machinery: [{ name: "Raboteuse Wirtgen W210i" }, { name: "Finisseur Vögele Super 1800-3i" }, { name: "Compacteur Hamm HD+ 90i" }],
                    assigned_tools: [{ name: "Balisage temporaire autoroutier" }, { name: "Thermomètre infrarouge thermique" }],
                    docs: [{ name: "BPU_Departement_34_Colas", type: "pdf" }, { name: "Formulation_Enrobes_Centrale", type: "pdf" }],
                    lots_breakdown: [
                        { name: "Bon de Commande 1 : Rabotage & BBTM RD600", budget: 950000, progress: 100, ds: 708000, pv: 950000 },
                        { name: "Bon de Commande 2 : Section RD612 Frontignan Plage", budget: 720000, progress: 25, ds: 537000, pv: 720000 },
                        { name: "Bon de Commande 3 : Giratoire ZI Eaux Blanches / Desserte Port", budget: 530000, progress: 0, ds: 395000, pv: 530000 },
                        { name: "Bon de Commande 4 : Purges & Réfection A9 / Bretelle Saint-Thibéry", budget: 1000000, progress: 0, ds: 746000, pv: 1000000 }
                    ],
                    steps: [
                        { name: "Plan de signalisation de nuit validé", progress: 100 },
                        { name: "Rabotage de nuit RD600 22 000 m²", progress: 100 },
                        { name: "Application BBTM 0/10 sous circulation", progress: 65 },
                        { name: "Purges ponctuelles et reconstitution GB4", progress: 25 },
                        { name: "Marquage thermoplastique rétro-réfléchissant", progress: 20 }
                    ]
                }
            ],

            fleet: [
                { id: "ENG-01", name: "Finisseur sur chenilles Vögele Super 1800-3i", cat: "Application Enrobés", type: "Finisseur lourd", brand: "Vögele", loc: "Port de Sète Quai Richelieu", status: "Sur Chantier", val: 320000, price: 320000, hourly_cost: 165, vgp: "01/10/2026", immat: "VOG-1800-3I", fuel: 85, hours: 1420, weight: "19.5t", power: "129 kW", capacity: "Table AB 500 TV (2.55m - 5.00m)", project: "Port de Sète - Quai Richelieu", icon: "🚜" },
                { id: "ENG-02", name: "Raboteuse à froid Wirtgen W210i", cat: "Rabotage Routier", type: "Fraiseuse 2m", brand: "Wirtgen", loc: "Axe RD600 / Frontignan", status: "Sur Chantier", val: 450000, price: 450000, hourly_cost: 210, vgp: "15/11/2026", immat: "WIR-210-I", fuel: 75, hours: 2180, weight: "28.5t", power: "537 kW", capacity: "Tambour 2.00m • Prof. 0-330mm", project: "Marché Entretien RD600", icon: "🚜" },
                { id: "ENG-03", name: "Compacteur Tandem Bomag BW151 AD-5", cat: "Compactage", type: "Cylindre vibrant", brand: "Bomag", loc: "Port de Sète Quai Richelieu", status: "Sur Chantier", val: 85000, price: 85000, hourly_cost: 65, vgp: "05/12/2026", immat: "BOM-151-AD", fuel: 90, hours: 1850, weight: "8.2t", power: "55 kW", capacity: "Largeur billes 1.50m (Asphalt Manager)", project: "Port de Sète - Quai Richelieu", icon: "🚜" },
                { id: "ENG-04", name: "Pelle Chenilles 24t Liebherr R924 G8", cat: "Terrassement Lourd", type: "Pelle Hydraulique", brand: "Liebherr", loc: "Port de Sète Quai Richelieu", status: "Sur Chantier", val: 240000, price: 240000, hourly_cost: 110, vgp: "20/09/2026", immat: "LIE-924-G8", fuel: 80, hours: 2650, weight: "24.5t", power: "129 kW", capacity: "Godet terrassement 1.45 m³ + Ligne BRH", project: "Port de Sète - Quai Richelieu", icon: "🚜" },
                { id: "ENG-05", name: "Pelle Urbaine Mecalac 12MTX", cat: "VRD & Réseaux", type: "Pelle sur pneus polyvalente", brand: "Mecalac", loc: "Sète Centre - Rue Caraussane", status: "Sur Chantier", val: 145000, price: 145000, hourly_cost: 85, vgp: "10/10/2026", immat: "MEC-12-MTX", fuel: 88, hours: 1920, weight: "9.7t", power: "85 kW", capacity: "Bras 3 pièces articulé + Attache rapide", project: "Sète Centre - Caraussane", icon: "🚜" },
                { id: "ENG-06", name: "Niveleuse compacte Caterpillar 120M", cat: "Nivellement", type: "Niveleuse 6x6", brand: "Caterpillar", loc: "Voie Verte Bouzigues-Sète", status: "Sur Chantier", val: 195000, price: 195000, hourly_cost: 95, vgp: "18/11/2026", immat: "CAT-120-M", fuel: 70, hours: 3100, weight: "14.2t", power: "103 kW", capacity: "Lame 3.65m guidée laser 3D", project: "Voie Verte Bassin de Thau", icon: "🚜" },
                { id: "ENG-07", name: "Minipelle Yanmar SV26-1", cat: "Petits Travaux", type: "Minipelle compacte", brand: "Yanmar", loc: "Sète Centre - Simone Veil", status: "Sur Chantier", val: 42000, price: 42000, hourly_cost: 45, vgp: "01/01/2027", immat: "YAN-SV26", fuel: 92, hours: 850, weight: "2.7t", power: "17.6 kW", capacity: "Godets 300, 600 et curage orientable", project: "Sète Centre - Caraussane", icon: "🚜" },
                { id: "ENG-08", name: "Chargeuse sur pneus Volvo L120H", cat: "Manutention Dépôt", type: "Chargeuse", brand: "Volvo", loc: "Centrale Colas Eaux Blanches", status: "Au Dépôt", val: 210000, price: 210000, hourly_cost: 98, vgp: "12/10/2026", immat: "VOL-L120H", fuel: 95, hours: 3400, weight: "20.7t", power: "203 kW", capacity: "Godet grand volume 3.5 m³", project: "Colas Établissement Sète", icon: "🚜" },
                { id: "ENG-09", name: "Camion Bi-Benne 8x4 Scania G450", cat: "Transport", type: "Poids Lourd 32t", brand: "Scania", loc: "Axe Sète - Frontignan", status: "En Rotation", val: 160000, price: 160000, hourly_cost: 75, vgp: "05/11/2026", immat: "SCA-8X4-G450", fuel: 82, hours: 4200, weight: "32t PTAC", power: "331 kW", capacity: "Benne calorifugée 18 m³ (Enrobés & GNT)", project: "Port de Sète - Quai Richelieu", icon: "🚛" },
                { id: "ENG-10", name: "Semi-remorque enrobés calorifugée MAN TGX", cat: "Transport", type: "Tracteur + Semi Benne", brand: "MAN", loc: "Centrale Maguelone - Sète", status: "En Rotation", val: 185000, price: 185000, hourly_cost: 88, vgp: "18/12/2026", immat: "MAN-TGX-SEMI", fuel: 78, hours: 2900, weight: "44t PTRA", power: "368 kW", capacity: "Benne ronde calorifugée 26 tonnes", project: "Marché Entretien RD600", icon: "🚛" }
            ],

            depot_inventory: [
                { id: "DEP-01", name: "Centrale d'enrobage Languedoc Enrobés / Colas (240 t/h)", cat: "Industriel", zone: "centrale", loc: "Site Maguelone / Sète", status: "Opérationnel", val: 2400000, vgp: "Contrôle DREAL OK", icon: "🏭" },
                { id: "DEP-02", name: "Stock GNT 0/31.5 calcaire concassé classe A (1 850 t)", cat: "Granulats", zone: "parc", loc: "Dépôt ZI Eaux Blanches", status: "Disponible", val: 33300, vgp: "NF Granulats", icon: "🧱" },
                { id: "DEP-03", name: "Stock liant spécial bitume modifié polymères Colstrong® (45 t)", cat: "Liants & Bitume", zone: "cuves", loc: "Cuve n°2 Centrale", status: "Disponible", val: 42750, vgp: "NF P 98-150", icon: "🛢️" },
                { id: "DEP-04", name: "Stock coquilles d'huîtres de Thau calibrées et lavées (120 t)", cat: "Éco-Matériaux", zone: "parc", loc: "Alvéole bio-recyclage", status: "Disponible", val: 14400, vgp: "Agrément Thau Agglo", icon: "🦪" },
                { id: "DEP-05", name: "Lot de 8 Caissons de blindage caisson léger SBH", cat: "Sécurité Tranchée", zone: "atelier", loc: "Magasin Sécurité", status: "Disponible", val: 38000, vgp: "VGP R.4534", icon: "🛡️" },
                { id: "DEP-06", name: "Tuyaux Fonte Ductile DN300 & DN600 avec joints express (280 ml)", cat: "Canalisations", zone: "rack", loc: "Zone Réseaux Humides", status: "Disponible", val: 48500, vgp: "NF EN 545", icon: "🚰" }
            ],

            cashflow_transactions: [
                { date: "02/04/2026", type: "Situation Marché", label: "Acompte n°2 - Port de Sète Quai Richelieu (Hydromer)", amount: 340000, status: "Encaissé (Chorus Pro)" },
                { date: "28/03/2026", type: "Situation Marché", label: "Situation n°5 - Voie Verte Bassin de Thau (Colstab)", amount: 165000, status: "Encaissé (Chorus Pro)" },
                { date: "20/03/2026", type: "Paiement Fournisseur", label: "Approvisionnement Bitumes & Liants Spéciaux Colas", amount: -85400, status: "Réglé" },
                { date: "15/03/2026", type: "Salaires", label: "Paie du personnel et charges sociales (68 salariés)", amount: -215000, status: "Débité" }
            ],

            documents: [
                { id: "DOC-COLAS-01", title: "CCTP Quai Richelieu - Aménagement Amarrage Drague Hydromer", cat: "DCE Actif", chantier: "Port de Sète - Quai Richelieu", date: "15/01/2026", format: "PDF", size: "8.4 Mo" },
                { id: "DOC-COLAS-02", title: "Fiche Technique & Avis Technique Procédé Colstrong® Percolé", cat: "Procédés Brevetés", chantier: "Port de Sète - Quai Richelieu", date: "10/02/2026", format: "PDF", size: "3.2 Mo" },
                { id: "DOC-COLAS-03", title: "CCTP Voie Verte Bassin de Thau - Revêtement Colstab Ostrea®", cat: "DCE Actif", chantier: "Voie Verte Bassin de Thau", date: "22/10/2025", format: "PDF", size: "5.7 Mo" },
                { id: "DOC-COLAS-04", title: "DICT Validée & Plan Réseaux Enedis / GRDF Sète Centre", cat: "DICT & Sécurité", chantier: "Sète Centre - Caraussane", date: "18/09/2025", format: "PDF", size: "4.1 Mo" }
            ],

            map_locations: [
                { id: "ch_01", name: "Port de Sète - Quai Richelieu (Hydromer & Colstrong)", category: "chantier", lat: 43.3980, lng: 3.7020, color: "#38bdf8", icon: "🏗️", ownership: "Colas Agence Sète (En cours)", budget_ini: 1850000, budget_used: 1258000, progress: 68, chef: "Rémi Bonnefoi", desc: "Aménagement voiries quai drague Hydromer, enrobés percolés Colstrong aux coquilles d'huîtres de Thau." },
                { id: "ch_02", name: "Voie Verte Bassin de Thau (Bouzigues-Sète Colstab)", category: "chantier", lat: 43.4350, lng: 3.6550, color: "#38bdf8", icon: "🏗️", ownership: "Colas Agence Sète (En cours)", budget_ini: 920000, budget_used: 772800, progress: 84, chef: "Jérôme Vidal", desc: "Création piste cyclable 4.2 km, revêtement drainant Colstab Ostrea® à valorisation conchylicole." },
                { id: "ch_03", name: "Sète Centre - Rues Caraussane & de Gaulle", category: "chantier", lat: 43.4080, lng: 3.6930, color: "#38bdf8", icon: "🏗️", ownership: "Colas Agence Sète (En cours)", budget_ini: 1420000, budget_used: 596400, progress: 42, chef: "Bruno Dupuis", desc: "Séparation pluviale vers réservoir Simone Veil 1 500 m³, fonte DN600, BBSG 0/10 et béton désactivé." },
                { id: "ch_04", name: "Marché Entretien Routier RD600 / RD612", category: "chantier", lat: 43.4380, lng: 3.7250, color: "#38bdf8", icon: "🏗️", ownership: "Colas Agence Sète (Accord-cadre)", budget_ini: 3200000, budget_used: 960000, progress: 30, chef: "Marc Bellegarde", desc: "Rabotage fin 5cm sous circulation de nuit, BBTM 0/10 haute performance centrale Eaux Blanches." },
                { id: "dep_01", name: "Colas Établissement Sète (ZI Eaux Blanches)", category: "depot", lat: 43.4240, lng: 3.7080, color: "#f59e0b", icon: "🏢", stock_val: "1 450 000 €", desc: "Siège agence Colas Sète, parc engins lourds, atelier d'entretien et centrale d'enrobage." },
                { id: "centrale_01", name: "Centrale Languedoc Enrobés / Colas Maguelone", category: "fournisseur", lat: 43.5250, lng: 3.8450, color: "#ec4899", icon: "🏭", product: "BBSG, BBTM, Colstrong & Colstab", desc: "Poste d'enrobage continu 240 t/h alimentant les chantiers de l'Hérault et du littoral." },
                { id: "carriere_01", name: "Carrières GSM Poussan & Villeveyrac", category: "fournisseur", lat: 43.4900, lng: 3.6800, color: "#ec4899", icon: "🏭", product: "GNT 0/31.5 & Enrochements", desc: "Carrière calcaire certifiée NF Granulats pour couches de forme et voiries portuaires." }
            ],

            hr_employees: [
                { id: "EMP-01", name: "Romain CARAÏ", role: "Chef d'Établissement Colas Agence de Sète", cat: "Direction", site: "Siège Agence Sète (Eaux Blanches)", phone: "04 67 46 22 00", email: "romain.carai@colas.com", caces: "AIPR Concepteur • Ingénieur TP", exp: "22 ans", icon: "👑" },
                { id: "EMP-02", name: "Rémi BONNEFOI", role: "Conducteur de Travaux Principal Port & Grands Travaux", cat: "Conduite Travaux", site: "Port de Sète Quai Richelieu", phone: "06 12 34 56 78", email: "remi.bonnefoi@colas.com", caces: "AIPR Encadrant • Spécialité Maritime", exp: "15 ans", icon: "👷‍♂️" },
                { id: "EMP-03", name: "Sophie MARTINEZ", role: "Conductrice de Travaux VRD & Éco-aménagements", cat: "Conduite Travaux", site: "Voie Verte Bassin de Thau", phone: "06 23 45 67 89", email: "sophie.martinez@colas.com", caces: "AIPR Encadrant • Ingénieure Environnement", exp: "11 ans", icon: "👷‍♀️" },
                { id: "EMP-04", name: "Bruno DUPUIS", role: "Chef de Chantier Réseaux Urbains & Séparatif", cat: "Chefs de Chantier", site: "Sète Centre - Caraussane", phone: "06 34 56 78 90", email: "bruno.dupuis@colas.com", caces: "AIPR Encadrant • CATEC Espace Confiné", exp: "18 ans", icon: "🦺" },
                { id: "EMP-05", name: "Jérôme VIDAL", role: "Chef de Chantier Voie Verte & Éco-revêtements", cat: "Chefs de Chantier", site: "Voie Verte Bouzigues-Sète", phone: "06 45 67 89 01", email: "jerome.vidal@colas.com", caces: "CACES R482 Cat B1/C1 • AIPR", exp: "14 ans", icon: "🦺" },
                { id: "EMP-06", name: "Marc BELLEGARDE", role: "Chef de Chantier Application Enrobés & Rabotage", cat: "Chefs de Chantier", site: "Marché Entretien RD600", phone: "06 56 78 90 12", email: "marc.bellegarde@colas.com", caces: "CACES R482 Cat D (Finisseur) & E • AIPR", exp: "19 ans", icon: "🦺" }
            ],

            hr_hierarchy: {
                direction: [{ name: "Romain CARAÏ", role: "Chef d'Établissement Colas Sète", color: "#38bdf8" }],
                conduite: [
                    { name: "Rémi BONNEFOI", role: "Conducteur Principal Port & Caraussane", color: "#0284c7" },
                    { name: "Sophie MARTINEZ", role: "Conductrice VRD Voie Verte & RD600", color: "#0284c7" }
                ],
                chefs: [
                    { name: "Bruno DUPUIS", role: "Chef de Chantier Rues Caraussane & de Gaulle", color: "#10b981" },
                    { name: "Jérôme VIDAL", role: "Chef de Chantier Voie Verte Bouzigues-Sète", color: "#10b981" },
                    { name: "Marc BELLEGARDE", role: "Chef de Chantier Application Enrobés RD600", color: "#10b981" }
                ]
            },

            ai_agents: [
                { id: "agent-port", name: "Agent IA Génie Maritime & Enrobés", avatar: "🚢", role: "Expertise Colstrong", status: "Actif", text: "Port de Sète Quai Richelieu : Formulation du coulis de percolation Colstrong validée avec 33% de coquilles conchylicoles de Thau broyées. Résistance en compression > 85 MPa." },
                { id: "agent-eco", name: "Agent IA Éco-Innovation & Voie Verte", avatar: "🌿", role: "Expertise Colstab Ostrea", status: "Actif", text: "Voie Verte Bouzigues-Sète : Perméabilité mesurée à 4.2x10^-4 m/s. Conforme aux exigences loi sur l'eau et protection de la lagune de Thau." }
            ]
        },
        """
        js1 = js1[:start_occ] + colas_block + js1[end_occ:]

with open('scripts/section_js_part1.py', 'w', encoding='utf-8') as f:
    f.write(js1)
print("Updated section_js_part1.py successfully!")

# ==============================================================================
# 2. UPDATE section_js_part2.py
# ==============================================================================
with open('scripts/section_js_part2.py', 'r', encoding='utf-8') as f:
    js2 = f.read()

# Update Watchtower camera locations and POIs
js2 = js2.replace("ales_giratoire", "sete_richelieu")
js2 = js2.replace("Alès - Giratoire RD906", "Port de Sète - Quai Richelieu (Hydromer)")
js2 = js2.replace("Pézenas (Centre Ancien)", "Sète Centre - Rues Caraussane")
js2 = js2.replace("Alès (Giratoire RD906)", "Port de Sète - Quai Richelieu")

with open('scripts/section_js_part2.py', 'w', encoding='utf-8') as f:
    f.write(js2)
print("Updated section_js_part2.py successfully!")

# ==============================================================================
# 3. UPDATE section_js_part3.py
# ==============================================================================
with open('scripts/section_js_part3.py', 'r', encoding='utf-8') as f:
    js3 = f.read()

js3 = js3.replace(
    "'finance': '💰 FINANCE : Caisse active 485 200 € (+14 200 € ce mois) • Acompte Barbazan n°3 encaissé (94 500 € HT) • Retenue de garantie 5% libérée sur Aurouer • Dépenses carburant & centrales à jour.'",
    "'finance': '💰 FINANCE : Caisse active Colas Sète 1 450 000 € (+14 200 € ce mois) • Acompte Port de Sète n°2 encaissé (340 000 € HT) • Facturation Sète Agglopôle Caraussane validée • Dépenses bitume & centrale Eaux Blanches équilibrées.'"
)
js3 = js3.replace(
    "`📢 ${s.companyName} • Marché Giratoire Barbazan notifié • Réception terrassement Aurouer validée • DICT AEP Sète conforme.`",
    "`📢 ${s.companyName} • Chantier Quai Richelieu (Hydromer) : Enrobés percolés Colstrong en cours • Voie Verte Bouzigues-Sète : Revêtement Colstab Ostrea® validé • Séparation Pluvial Caraussane / Simone Veil active • QSE 98.5%.`"
)
js3 = js3.replace(
    "`📢 ${s.companyName} • Direction : ${s.userName} • Caisse Active : ${new Intl.NumberFormat('fr-FR').format(s.treasury)} € • Effectif : ${s.headcount} salariés • Chantiers : ${s.projectsCount} actifs (Barbazan, Aurouer, Sète).`",
    "`📢 ${s.companyName} • Direction : ${s.userName} • Caisse Active : ${new Intl.NumberFormat('fr-FR').format(s.treasury)} € • Effectif : ${s.headcount} salariés • Chantiers : ${s.projectsCount} actifs (Quai Richelieu, Voie Verte Thau, Caraussane, RD600).`"
)

with open('scripts/section_js_part3.py', 'w', encoding='utf-8') as f:
    f.write(js3)
print("Updated section_js_part3.py successfully!")

# ==============================================================================
# 4. UPDATE section_modals.py
# ==============================================================================
with open('scripts/section_modals.py', 'r', encoding='utf-8') as f:
    modals = f.read()

modals = modals.replace(
    'Vue Chantier Barbazan - PK 0+120',
    'Vue Chantier Port de Sète - Quai Richelieu (Drague Hydromer)'
)

with open('scripts/section_modals.py', 'w', encoding='utf-8') as f:
    f.write(modals)
print("Updated section_modals.py successfully!")

print("All Javascript and Modal files patched successfully.")
