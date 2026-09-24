# -*- coding: utf-8 -*-
"""
Generate Section 18, 18.2, 21, and window.onload updates for section_js_part3.py
"""

# Let's define the 24 task sheets dataset
task_sheets_code = r'''
    const taskSheetsPresetsData = {
        'bordure_t2': {
            id: 'bordure_t2',
            title: 'Fiche 01 : Pose de Bordures Béton T2 avec Semelle Béton C25/30',
            unit: 'ml',
            cadence: '60 à 75 ml / jour (Équipe 2 ouvriers)',
            desc: 'Pose de bordures T2 droites au cordeau sur semelle béton C25/30 ép. 15cm, calage épaulement arrière et jointoiement mortier.',
            tu_mo: 0.50,
            k_coef: 1.350,
            lines: [
                { cat: "Main d'Œuvre", name: "Poseur de bordures qualifié (THMO)", unit: "h", qty: 0.25, pu: 38.00 },
                { cat: "Main d'Œuvre", name: "Manœuvre régleur VRD (THMO)", unit: "h", qty: 0.25, pu: 32.00 },
                { cat: "Matériaux", name: "Bordure béton T2 droite NF P98-305 (L=1.00m)", unit: "ml", qty: 1.02, pu: 8.80 },
                { cat: "Matériaux", name: "Béton de calage et semelle C25/30 XF1 BPE", unit: "m³", qty: 0.08, pu: 118.00 },
                { cat: "Matériaux", name: "Mortier de jointoiement & scellement rapide", unit: "sac", qty: 0.15, pu: 16.80 },
                { cat: "Matériel", name: "Pince à bordures mécanique & niveau optique", unit: "h", qty: 0.25, pu: 6.50 },
                { cat: "Matériel", name: "Mini-pelle 2.5t pour manutention palettes", unit: "h", qty: 0.10, pu: 45.00 }
            ]
        },
        'bordure_p2': {
            id: 'bordure_p2',
            title: 'Fiche 02 : Pose de Bordures Trottoir P2 avec Semelle Béton',
            unit: 'ml',
            cadence: '70 à 90 ml / jour',
            desc: 'Pose de bordures P2 de délimitation trottoir sur semelle béton dosé à 250 kg/m³ ép. 10cm et solin arrière.',
            tu_mo: 0.40,
            k_coef: 1.350,
            lines: [
                { cat: "Main d'Œuvre", name: "Poseur qualifié bordures", unit: "h", qty: 0.20, pu: 38.00 },
                { cat: "Main d'Œuvre", name: "Manœuvre aide poseur", unit: "h", qty: 0.20, pu: 32.00 },
                { cat: "Matériaux", name: "Bordure béton P2 (L=1.00m)", unit: "ml", qty: 1.02, pu: 7.20 },
                { cat: "Matériaux", name: "Béton de calage semelle C20/25", unit: "m³", qty: 0.05, pu: 112.00 },
                { cat: "Matériel", name: "Outillage de pose, cordeau & massette", unit: "h", qty: 0.20, pu: 4.50 }
            ]
        },
        'bordure_i1_i2': {
            id: 'bordure_i1_i2',
            title: 'Fiche 03 : Pose de Bordures d\'Îlot Giratoire Type I1 / I2 Franchissables',
            unit: 'ml',
            cadence: '50 à 65 ml / jour',
            desc: 'Pose soignée en courbe au rayon de giratoire des bordures d\'îlot I1/I2 franchissables avec calage béton résistant au trafic lourd.',
            tu_mo: 0.55,
            k_coef: 1.360,
            lines: [
                { cat: "Main d'Œuvre", name: "Poseur hautement qualifié (OHQ)", unit: "h", qty: 0.30, pu: 40.00 },
                { cat: "Main d'Œuvre", name: "Manœuvre VRD régleur", unit: "h", qty: 0.25, pu: 32.00 },
                { cat: "Matériaux", name: "Bordure d'îlot type I1/I2 béton armé", unit: "ml", qty: 1.03, pu: 14.50 },
                { cat: "Matériaux", name: "Béton de fondation C25/30 XF2", unit: "m³", qty: 0.09, pu: 120.00 },
                { cat: "Matériel", name: "Pince ventouse de manutention & laser", unit: "h", qty: 0.25, pu: 8.00 }
            ]
        },
        'caniveau_cc1_cc2': {
            id: 'caniveau_cc1_cc2',
            title: 'Fiche 04 : Pose Caniveau Profilé CC1 / CC2 avec Calage Béton',
            unit: 'ml',
            cadence: '45 à 60 ml / jour',
            desc: 'Pose de caniveaux doubles pentes CC1 pour fil d\'eau de voirie urbaine sur lit de béton C25/30 et raccordement aux avaloirs.',
            tu_mo: 0.60,
            k_coef: 1.350,
            lines: [
                { cat: "Main d'Œuvre", name: "Canalisateur / Poseur qualifié", unit: "h", qty: 0.30, pu: 38.00 },
                { cat: "Main d'Œuvre", name: "Manœuvre VRD", unit: "h", qty: 0.30, pu: 32.00 },
                { cat: "Matériaux", name: "Caniveau profilé CC1 (50x14cm)", unit: "ml", qty: 1.02, pu: 12.80 },
                { cat: "Matériaux", name: "Béton semelle C25/30", unit: "m³", qty: 0.07, pu: 118.00 },
                { cat: "Matériel", name: "Mini-dumper & niveau optique", unit: "h", qty: 0.20, pu: 18.00 }
            ]
        },
        'caniveau_grille': {
            id: 'caniveau_grille',
            title: 'Fiche 05 : Pose Caniveau à Grille Fonte D400 Type F900',
            unit: 'ml',
            cadence: '35 à 50 ml / jour',
            desc: 'Caniveau béton avec cornières métalliques et grille fonte ductile D400 pour traversées lourdes et entrées de giratoire.',
            tu_mo: 0.70,
            k_coef: 1.340,
            lines: [
                { cat: "Main d'Œuvre", name: "Poseur qualifié VRD", unit: "h", qty: 0.35, pu: 38.00 },
                { cat: "Main d'Œuvre", name: "Manœuvre en fouille", unit: "h", qty: 0.35, pu: 32.00 },
                { cat: "Matériaux", name: "Caniveau béton + grille fonte D400", unit: "ml", qty: 1.00, pu: 68.00 },
                { cat: "Matériaux", name: "Béton d'enrobage C25/30 (berceau)", unit: "m³", qty: 0.12, pu: 118.00 },
                { cat: "Matériel", name: "Mini-pelle avec élingues & godet", unit: "h", qty: 0.20, pu: 45.00 }
            ]
        },
        'trottoir_beton': {
            id: 'trottoir_beton',
            title: 'Fiche 06 : Trottoir & Îlot en Béton Coulé Désactivé Galets de Garonne',
            unit: 'm²',
            cadence: '80 à 120 m² / jour',
            desc: 'Coulage de dalle béton C30/37 ép. 12cm avec granulat alluvionnaire galets de Garonne, pulvérisation de désactivant et lavage HP sous pression.',
            tu_mo: 0.45,
            k_coef: 1.350,
            lines: [
                { cat: "Main d'Œuvre", name: "Chef d'équipe bétonneur", unit: "h", qty: 0.15, pu: 42.00 },
                { cat: "Main d'Œuvre", name: "Bétonneur régleur à la règle vibrante", unit: "h", qty: 0.30, pu: 36.00 },
                { cat: "Matériaux", name: "Béton désactivé C30/37 galets Garonne", unit: "m³", qty: 0.13, pu: 145.00 },
                { cat: "Matériaux", name: "Produit de cure & désactivant de surface", unit: "litre", qty: 0.25, pu: 8.50 },
                { cat: "Matériaux", name: "Treillis soudé PAFC anti-fissuration", unit: "m²", qty: 1.05, pu: 3.40 },
                { cat: "Matériel", name: "Règle vibrante, talocheuse & nettoyeur HP 200 bar", unit: "h", qty: 0.15, pu: 22.00 }
            ]
        },
        'decapage_terre_vege': {
            id: 'decapage_terre_vege',
            title: 'Fiche 07 : Décapage Terre Végétale ép. 20cm & Mise en Cordon',
            unit: 'm²',
            cadence: '1 500 à 2 200 m² / jour (Pelle 24t)',
            desc: 'Décapage soigné de la couche de terre arable sur 20cm d\'épaisseur à la pelle mécanique et régalage en cordon périphérique.',
            tu_mo: 0.005,
            k_coef: 1.350,
            lines: [
                { cat: "Main d'Œuvre", name: "Conducteur d'engins qualifié CACES B1", unit: "h", qty: 0.005, pu: 42.00 },
                { cat: "Matériel", name: "Pelle hydraulique 24t Liebherr R924", unit: "h", qty: 0.005, pu: 95.00 },
                { cat: "Matériel", name: "Carburant GNR & entretien machine", unit: "forfait", qty: 0.005, pu: 25.00 }
            ]
        },
        'terrassement_masse': {
            id: 'terrassement_masse',
            title: 'Fiche 08 : Terrassement Pleine Masse Déblais & Évacuation Camions 8x4',
            unit: 'm³',
            cadence: '350 à 480 m³ / jour',
            desc: 'Extraction des déblais rocheux/meubles en pleine masse, chargement sur camions 8x4 et transport vers centre agréé ISDI.',
            tu_mo: 0.035,
            k_coef: 1.340,
            lines: [
                { cat: "Main d'Œuvre", name: "Pelleur qualifié pelle 24t", unit: "h", qty: 0.02, pu: 42.00 },
                { cat: "Main d'Œuvre", name: "Chauffeur PL benne 8x4", unit: "h", qty: 0.06, pu: 36.00 },
                { cat: "Matériel", name: "Pelle hydraulique chenilles 24t", unit: "h", qty: 0.02, pu: 95.00 },
                { cat: "Matériel", name: "Camion benne 8x4 Scania (rotation 12km)", unit: "h", qty: 0.06, pu: 85.00 },
                { cat: "Sous-traitance", name: "Redevance mise en décharge ISDI (Trackdéchets)", unit: "tonne", qty: 1.80, pu: 4.80 }
            ]
        },
        'remblai_apport_gnt': {
            id: 'remblai_apport_gnt',
            title: 'Fiche 09 : Remblai d\'Emprunt GNT 0/31.5 & Compactage par Couches',
            unit: 'm³',
            cadence: '180 à 260 m³ / jour',
            desc: 'Fourniture, régalage et compactage méthodique par couches de 30cm de Grave Non Traitée 0/31.5 classe A pour objectif q4.',
            tu_mo: 0.08,
            k_coef: 1.340,
            lines: [
                { cat: "Main d'Œuvre", name: "Conducteur d'engins (Bouteur / Pelle)", unit: "h", qty: 0.04, pu: 42.00 },
                { cat: "Main d'Œuvre", name: "Conducteur compacteur vibrant", unit: "h", qty: 0.04, pu: 38.00 },
                { cat: "Matériaux", name: "GNT 0/31.5 calcaire concassé carrière", unit: "tonne", qty: 2.15, pu: 16.50 },
                { cat: "Matériel", name: "Compacteur monocylindre Bomag BW 213", unit: "h", qty: 0.04, pu: 75.00 }
            ]
        },
        'couche_fondation_gnt': {
            id: 'couche_fondation_gnt',
            title: 'Fiche 10 : Couche de Fondation Voirie en GNT 0/31.5 ép. 20cm',
            unit: 'm²',
            cadence: '600 à 900 m² / jour',
            desc: 'Régalage à la niveleuse laser 3D de grave de fondation ép. 20cm compactée pour obtention d\'un module de réaction EV2 >= 80 MPa.',
            tu_mo: 0.025,
            k_coef: 1.350,
            lines: [
                { cat: "Main d'Œuvre", name: "Conducteur niveleuse laser", unit: "h", qty: 0.012, pu: 45.00 },
                { cat: "Main d'Œuvre", name: "Conducteur compacteur tandem", unit: "h", qty: 0.012, pu: 38.00 },
                { cat: "Matériaux", name: "GNT 0/31.5A concassé (0.43 t/m²)", unit: "tonne", qty: 0.43, pu: 16.50 },
                { cat: "Matériel", name: "Niveleuse Caterpillar 120M & Compacteur", unit: "h", qty: 0.012, pu: 140.00 }
            ]
        },
        'couche_reprofilage_gb': {
            id: 'couche_reprofilage_gb',
            title: 'Fiche 11 : Couche de Reprofilage Grave Bitume GB3 (à la Tonne)',
            unit: 'tonne',
            cadence: '180 à 250 t / jour',
            desc: 'Application mécanisée au finisseur de Grave Bitume GB3 à 160°C pour rattrapage de profil en travers et renforcement d\'assise.',
            tu_mo: 0.07,
            k_coef: 1.320,
            lines: [
                { cat: "Main d'Œuvre", name: "Équipe d'application enrobés (4 ouvriers)", unit: "h", qty: 0.07, pu: 155.00 },
                { cat: "Matériaux", name: "Grave Bitume GB3 0/14 livré chaud", unit: "tonne", qty: 1.02, pu: 76.00 },
                { cat: "Matériaux", name: "Émulsion C65B4 couche d'accrochage", unit: "kg", qty: 3.00, pu: 1.55 },
                { cat: "Matériel", name: "Finisseur Vögele Super 1800 + Compacteur", unit: "h", qty: 0.07, pu: 180.00 }
            ]
        },
        'couche_roulement_bbsg': {
            id: 'couche_roulement_bbsg',
            title: 'Fiche 12 : Couche de Roulement Enrobés Chauds BBSG 0/10 ép. 5cm',
            unit: 'tonne',
            cadence: '160 à 220 t / jour',
            desc: 'Mise en œuvre soignée au finisseur de Béton Bitumineux Semi-Grenu BBSG 0/10 classe 3, compactage tandem sans vibration excessive sur joints.',
            tu_mo: 0.08,
            k_coef: 1.320,
            lines: [
                { cat: "Main d'Œuvre", name: "Équipe d'application enrobés", unit: "h", qty: 0.08, pu: 155.00 },
                { cat: "Matériaux", name: "BBSG 0/10 classe 3 (160°C)", unit: "tonne", qty: 1.02, pu: 84.00 },
                { cat: "Matériaux", name: "Émulsion bitume C65B4 (500g/m²)", unit: "kg", qty: 3.50, pu: 1.55 },
                { cat: "Matériel", name: "Finisseur + Compacteur vibrant Bomag", unit: "h", qty: 0.08, pu: 195.00 }
            ]
        },
        'arrachage_arbre': {
            id: 'arrachage_arbre',
            title: 'Fiche 13 : Arrachage, Abattage & Dessouchage d\'Arbres Ø > 60cm',
            unit: 'u',
            cadence: '4 à 6 unités / jour',
            desc: 'Abattage directionnel d\'arbres avec tronçonneuse thermique, extraction des souches à la pelle 24t et broyage/évacuation des rémanents.',
            tu_mo: 1.75,
            k_coef: 1.350,
            lines: [
                { cat: "Main d'Œuvre", name: "Bûcheron / Ouvrier hautement qualifié", unit: "h", qty: 1.00, pu: 40.00 },
                { cat: "Main d'Œuvre", name: "Conducteur de pelle 24t", unit: "h", qty: 0.75, pu: 42.00 },
                { cat: "Matériel", name: "Pelle 24t avec godet à dents & pince", unit: "h", qty: 0.75, pu: 95.00 },
                { cat: "Matériel", name: "Tronçonneuse Stihl & équipement bûcheron", unit: "h", qty: 1.00, pu: 15.00 }
            ]
        },
        'sciage_chaussee': {
            id: 'sciage_chaussee',
            title: 'Fiche 14 : Sciage de Chaussée Scie à Sol Diamantée prof 20cm',
            unit: 'ml',
            cadence: '180 à 280 ml / jour',
            desc: 'Sciage franc rectiligne de chaussée bitumineuse ou béton à la scie à sol automatique refroidie à l\'eau pour raccordement soigné.',
            tu_mo: 0.035,
            k_coef: 1.350,
            lines: [
                { cat: "Main d'Œuvre", name: "Scieur qualifié / Manœuvre VRD", unit: "h", qty: 0.035, pu: 34.00 },
                { cat: "Matériel", name: "Scie à sol thermique disque diamant Ø600", unit: "h", qty: 0.035, pu: 24.00 },
                { cat: "Matériaux", name: "Disque diamant (usure au ml scié)", unit: "ml", qty: 1.00, pu: 1.40 },
                { cat: "Matériaux", name: "Eau d'arrosage et lavage boues", unit: "forfait", qty: 1.00, pu: 0.20 }
            ]
        },
        'demo_decoupe_chaussee': {
            id: 'demo_decoupe_chaussee',
            title: 'Fiche 15 : Découpe & Démolition Chaussée Enrobés avec Évacuation',
            unit: 'm²',
            cadence: '150 à 220 m² / jour',
            desc: 'Décroutage mécanique de structure de chaussée au BRH / godet trapèze et chargement direct sur camion benne.',
            tu_mo: 0.05,
            k_coef: 1.340,
            lines: [
                { cat: "Main d'Œuvre", name: "Pelleur qualifié BRH", unit: "h", qty: 0.03, pu: 42.00 },
                { cat: "Main d'Œuvre", name: "Chauffeur camion 8x4", unit: "h", qty: 0.05, pu: 36.00 },
                { cat: "Matériel", name: "Pelle 24t équipée BRH + Godet rétro", unit: "h", qty: 0.03, pu: 115.00 },
                { cat: "Matériel", name: "Camion 8x4 transport gravats", unit: "h", qty: 0.05, pu: 85.00 }
            ]
        },
        'rabotage_enrobes': {
            id: 'rabotage_enrobes',
            title: 'Fiche 16 : Rabotage Chaussée Enrobés prof 5cm (au m²)',
            unit: 'm²',
            cadence: '1 200 à 2 000 m² / jour (Raboteuse 1.00m)',
            desc: 'Fraisage à froid de la couche d\'enrobé dégradée à la raboteuse sur 5cm, évacuation des fraisats par tapis convoyeur et balayage HP.',
            tu_mo: 0.008,
            k_coef: 1.320,
            lines: [
                { cat: "Main d'Œuvre", name: "Opérateur raboteuse + Chauffeur PL", unit: "h", qty: 0.012, pu: 85.00 },
                { cat: "Matériel", name: "Raboteuse à froid Wirtgen W100", unit: "h", qty: 0.008, pu: 190.00 },
                { cat: "Matériel", name: "Balayeuse aspiratrice de finition", unit: "h", qty: 0.004, pu: 85.00 }
            ]
        },
        'demolition_trottoir': {
            id: 'demolition_trottoir',
            title: 'Fiche 17 : Démolition Trottoirs & Îlots en Béton avec Évacuation',
            unit: 'm²',
            cadence: '120 à 180 m² / jour',
            desc: 'Démolition de dalle béton de trottoir au brise-roche hydraulique sur mini-pelle et chargement camion pour recyclage.',
            tu_mo: 0.06,
            k_coef: 1.350,
            lines: [
                { cat: "Main d'Œuvre", name: "Conducteur mini-pelle BRH", unit: "h", qty: 0.04, pu: 40.00 },
                { cat: "Main d'Œuvre", name: "Manœuvre tri des aciers & nettoyage", unit: "h", qty: 0.04, pu: 32.00 },
                { cat: "Matériel", name: "Mini-pelle 6t équipée BRH", unit: "h", qty: 0.04, pu: 65.00 },
                { cat: "Matériel", name: "Camion benne 6x4 évacuation", unit: "h", qty: 0.04, pu: 75.00 }
            ]
        },
        'reprise_terre_vege': {
            id: 'reprise_terre_vege',
            title: 'Fiche 18 : Reprise Terre Végétale & Régalage Espaces Verts ép. 15cm',
            unit: 'm²',
            cadence: '800 à 1 400 m² / jour',
            desc: 'Reprise des cordons de terre végétale stockés in-situ, régalage à la pelle avec godet de curage orientable et nivellement de finition.',
            tu_mo: 0.01,
            k_coef: 1.350,
            lines: [
                { cat: "Main d'Œuvre", name: "Pelleur qualifié finition", unit: "h", qty: 0.008, pu: 42.00 },
                { cat: "Main d'Œuvre", name: "Manœuvre jardinier ratissage", unit: "h", qty: 0.01, pu: 32.00 },
                { cat: "Matériel", name: "Pelle à pneus Mecalac avec godet curage", unit: "h", qty: 0.008, pu: 80.00 }
            ]
        },
        'tranchee_ba400': {
            id: 'tranchee_ba400',
            title: 'Fiche 19 : Collecteur EU/EP Béton Armé 135A Ø400 sous Blindage',
            unit: 'ml',
            cadence: '22 à 30 ml / jour (Prof 2.20m)',
            desc: 'Fouille en tranchée sous blindage caisson acier R4534, lit de pose sable 0/4, pose tuyau BA Ø400 au laser canalisateur Piper 200 et remblai GNT.',
            tu_mo: 0.90,
            k_coef: 1.340,
            lines: [
                { cat: "Main d'Œuvre", name: "Conducteur pelle 24t", unit: "h", qty: 0.25, pu: 42.00 },
                { cat: "Main d'Œuvre", name: "Canalisateur qualifié poseur", unit: "h", qty: 0.35, pu: 38.00 },
                { cat: "Main d'Œuvre", name: "Manœuvre canalisateur en fouille", unit: "h", qty: 0.35, pu: 32.00 },
                { cat: "Matériaux", name: "Tuyau Béton Armé 135A Ø400 (L=2.50m)", unit: "ml", qty: 1.00, pu: 54.00 },
                { cat: "Matériaux", name: "Sable 0/4 alluvionnaire lit de pose", unit: "tonne", qty: 0.35, pu: 21.00 },
                { cat: "Matériaux", name: "Grave GNT 0/31.5A remblai", unit: "tonne", qty: 1.80, pu: 16.50 },
                { cat: "Matériel", name: "Pelle 24t + Caisson blindage Krings + Laser Piper", unit: "h", qty: 0.30, pu: 125.00 }
            ]
        },
        'tuyau_pvc_d300': {
            id: 'tuyau_pvc_d300',
            title: 'Fiche 20 : Canalisation Assainissement PVC Compact Ø300 CR8',
            unit: 'ml',
            cadence: '30 à 45 ml / jour',
            desc: 'Pose en tranchée de canalisation PVC compacte CR8 Ø300 à emboîtement élastomère pour réseau pluvial gravitaire.',
            tu_mo: 0.65,
            k_coef: 1.340,
            lines: [
                { cat: "Main d'Œuvre", name: "Canalisateur qualifié", unit: "h", qty: 0.30, pu: 38.00 },
                { cat: "Main d'Œuvre", name: "Manœuvre aide poseur", unit: "h", qty: 0.35, pu: 32.00 },
                { cat: "Matériaux", name: "Tube PVC Assainissement CR8 Ø300 (L=3m)", unit: "ml", qty: 1.02, pu: 34.50 },
                { cat: "Matériaux", name: "Lit de pose gravillon 4/10 lavé", unit: "tonne", qty: 0.30, pu: 22.00 },
                { cat: "Matériel", name: "Laser de guidage + matériel d'épreuve", unit: "h", qty: 0.30, pu: 15.00 }
            ]
        },
        'regard_visite_ba': {
            id: 'regard_visite_ba',
            title: 'Fiche 21 : Regard de Visite Béton Ø1000 avec Tampon Fonte D400',
            unit: 'u',
            cadence: '2 à 3 unités / jour',
            desc: 'Fourniture et pose d\'élément de fond avec cunette hydraulique préformée, rehausses béton Ø1000, cône de réduction et tampon fonte D400 ventilé.',
            tu_mo: 4.50,
            k_coef: 1.340,
            lines: [
                { cat: "Main d'Œuvre", name: "Canalisateur qualifié + Pelleur", unit: "h", qty: 2.25, pu: 40.00 },
                { cat: "Main d'Œuvre", name: "Manœuvre VRD scellement", unit: "h", qty: 2.25, pu: 32.00 },
                { cat: "Matériaux", name: "Fond regard Ø1000 + rehausses + cône", unit: "u", qty: 1.00, pu: 380.00 },
                { cat: "Matériaux", name: "Tampon fonte ductile D400 articulé", unit: "u", qty: 1.00, pu: 195.00 },
                { cat: "Matériaux", name: "Mortier de scellement haute performance", unit: "sac", qty: 2.00, pu: 18.50 },
                { cat: "Matériel", name: "Pelle pour levage éléments lourds (CMU 2t)", unit: "h", qty: 1.50, pu: 95.00 }
            ]
        },
        'regard_40x40': {
            id: 'regard_40x40',
            title: 'Fiche 22 : Regard d\'Eaux Pluviales Béton 40x40 + Grille Fonte C250',
            unit: 'u',
            cadence: '6 à 8 unités / jour',
            desc: 'Regard à décantation en béton 40x40 avec opercules de raccordement et grille plate concave fonte ductile C250 scellée.',
            tu_mo: 1.20,
            k_coef: 1.350,
            lines: [
                { cat: "Main d'Œuvre", name: "Maçon VRD qualifié", unit: "h", qty: 0.60, pu: 38.00 },
                { cat: "Main d'Œuvre", name: "Manœuvre aide scellement", unit: "h", qty: 0.60, pu: 32.00 },
                { cat: "Matériaux", name: "Regard béton 40x40 avec fond", unit: "u", qty: 1.00, pu: 42.00 },
                { cat: "Matériaux", name: "Grille plate fonte C250 400x400", unit: "u", qty: 1.00, pu: 65.00 },
                { cat: "Matériaux", name: "Béton de calage et scellement", unit: "sac", qty: 1.50, pu: 16.80 }
            ]
        },
        'fourreaux_tpc110': {
            id: 'fourreaux_tpc110',
            title: 'Fiche 23 : Fourreaux TPC Janolène Ø110 Réseaux Secs & Aiguillage',
            unit: 'ml',
            cadence: '120 à 180 ml / jour (Nappe de 2)',
            desc: 'Pose en fouille de fourreaux TPC cintrables Ø110 avec tire-fil, calage sable 0/4, grillage avertisseur rouge/vert et aiguillage de test.',
            tu_mo: 0.15,
            k_coef: 1.350,
            lines: [
                { cat: "Main d'Œuvre", name: "Électricien / Poseur réseaux secs", unit: "h", qty: 0.08, pu: 38.00 },
                { cat: "Main d'Œuvre", name: "Manœuvre dérouleur touret", unit: "h", qty: 0.08, pu: 32.00 },
                { cat: "Matériaux", name: "Fourreau TPC Ø110 rouge/vert (touret 50m)", unit: "ml", qty: 1.05, pu: 3.40 },
                { cat: "Matériaux", name: "Sable d'enrobage 0/4", unit: "tonne", qty: 0.12, pu: 21.00 },
                { cat: "Matériaux", name: "Grillage avertisseur plastique normalisé", unit: "ml", qty: 1.05, pu: 0.55 },
                { cat: "Matériel", name: "Dérouleuse touret & compresseur aiguille", unit: "h", qty: 0.08, pu: 12.00 }
            ]
        },
        'chambre_tirage_l1t': {
            id: 'chambre_tirage_l1t',
            title: 'Fiche 24 : Chambre de Tirage Télécom L1T / Coffret S200',
            unit: 'u',
            cadence: '3 à 4 unités / jour',
            desc: 'Pose et scellement de chambre de tirage L1T modulaire préfabriquée avec cadre et tampon fonte 250kN articulé et masques d\'étanchéité.',
            tu_mo: 2.20,
            k_coef: 1.350,
            lines: [
                { cat: "Main d'Œuvre", name: "Poseur qualifié réseaux secs", unit: "h", qty: 1.10, pu: 38.00 },
                { cat: "Main d'Œuvre", name: "Manœuvre scellement béton", unit: "h", qty: 1.10, pu: 32.00 },
                { cat: "Matériaux", name: "Chambre L1T préfabriquée béton", unit: "u", qty: 1.00, pu: 165.00 },
                { cat: "Matériaux", name: "Cadre & tampon fonte B125/C250", unit: "u", qty: 1.00, pu: 120.00 },
                { cat: "Matériaux", name: "Béton de calage & gravillon drainage", unit: "forfait", qty: 1.00, pu: 35.00 }
            ]
        }
    };
'''

with open('scripts/section_js_part3.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace taskSheetsPresetsData
ts_start = text.find('const taskSheetsPresetsData = {')
ts_end = text.find('function loadTaskSheetPreset(')
if ts_start != -1 and ts_end != -1:
    text = text[:ts_start] + task_sheets_code.strip() + "\n\n    " + text[ts_end:]
    print("taskSheetsPresetsData replaced with all 24 presets successfully!")
else:
    print("Error locating taskSheetsPresetsData boundaries")

with open('scripts/section_js_part3.py', 'w', encoding='utf-8') as f:
    f.write(text)
