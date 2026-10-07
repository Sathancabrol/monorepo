# -*- coding: utf-8 -*-
"""
Socle de données de l'Atlas interactif Frontignan.

Toutes les valeurs sont sourcées (voir champ `source` de chaque bloc).
- INSEE, Comparateur de territoires, millésime paru le 27/08/2026
  (RP2023 / Filosofi 2023 / Flores 2024 / état civil 2025), géographie au 01/01/2026.
- geo.api.gouv.fr (surfaces communales, centroïdes) — extraction du 08/09/2026.
- Rapport d'analyse territoriale Frontignan (sept. 2026) et Vision 2026-2040
  pour les données budgétaires, projets, acteurs et prospective.

Convention de fiabilité :
  "A" = source officielle primaire ; "B" = source secondaire recoupée ;
  "C" = estimation / lecture d'analyste (explicitée).
"""

SOURCE_INSEE = {
    "t": "INSEE — Comparateur de territoires (RP2023, Filosofi 2023, Flores 2024)",
    "u": "https://www.insee.fr/fr/statistiques/1405599?geo=COM-34108",
    "d": "27/08/2026",
}
SOURCE_GEO = {
    "t": "API Géo (découpage administratif) — surfaces et centroïdes",
    "u": "https://geo.api.gouv.fr/epcis/200066355/communes",
    "d": "08/09/2026",
}

# --------------------------------------------------------------------------
# 1. Les 14 communes de Sète Agglopôle Méditerranée
# --------------------------------------------------------------------------
# pop        : population municipale 2023
# surf_ha    : superficie (hectares, IGN)
# dens       : densité hab/km² 2023
# tvam       : variation annuelle moyenne 2017-2023 (%)
# sn / sm    : dont solde naturel / solde migratoire apparent (%/an)
# men        : nombre de ménages 2023
# nais/deces : naissances / décès domiciliés 2025
# logts      : nombre total de logements 2023
# rp/rs/vac  : part résidences principales / secondaires / vacantes (%)
# prop       : part de ménages propriétaires (%)
# nvm        : niveau de vie médian 2023 (€/UC)
# pauv       : taux de pauvreté 2023 (%) — None si secret statistique
# emp        : emplois au lieu de travail 2023
# psal       : part de l'emploi salarié (%)
# tact/tcho  : taux d'activité / taux de chômage des 15-64 ans (%)
# etab       : établissements employeurs fin 2024
# s_agri … s_apesas : répartition sectorielle des établissements (%)
COMMUNES = [
    dict(code="34108", nom="Frontignan", pop=24136, surf_ha=4001.24, dens=760.9, tvam=1.0, sn=-0.1, sm=1.1,
         men=11183, nais=174, deces=272, logts=14566, rp=76.5, rs=20.6, vac=2.9, prop=61.6,
         nvm=24580, pauv=17.0, emp=6556, psal=81.1, tact=75.3, tcho=14.0, etab=671,
         s_agri=4.0, s_indus=9.1, s_constr=11.2, s_comm=64.7, s_apesas=11.0,
         lat=43.4486, lon=3.7493, role="Siège de l'agglo · 2ᵉ ville"),
    dict(code="34301", nom="Sète", pop=45337, surf_ha=4058.10, dens=1872.7, tvam=0.8, sn=-0.5, sm=1.3,
         men=24859, nais=288, deces=673, logts=33815, rp=73.1, rs=21.4, vac=5.5, prop=47.5,
         nvm=22740, pauv=26.0, emp=18025, psal=81.3, tact=67.9, tcho=17.1, etab=1864,
         s_agri=2.2, s_indus=6.1, s_constr=5.6, s_comm=74.9, s_apesas=11.2,
         lat=43.3844, lon=3.6441, role="Ville-centre · port"),
    dict(code="34157", nom="Mèze", pop=12669, surf_ha=4772.88, dens=366.3, tvam=1.5, sn=-0.5, sm=2.0,
         men=6157, nais=84, deces=158, logts=7531, rp=81.3, rs=13.8, vac=5.0, prop=58.1,
         nvm=24180, pauv=20.0, emp=3196, psal=72.6, tact=72.1, tcho=15.1, etab=418,
         s_agri=13.6, s_indus=6.2, s_constr=9.1, s_comm=62.7, s_apesas=8.4,
         lat=43.4323, lon=3.5843, role="Pôle nord-Thau · conchyliculture"),
    dict(code="34150", nom="Marseillan", pop=8414, surf_ha=5273.21, dens=162.7, tvam=1.3, sn=-0.7, sm=2.1,
         men=4360, nais=59, deces=124, logts=10881, rp=39.9, rs=59.7, vac=0.4, prop=59.7,
         nvm=23800, pauv=19.0, emp=2190, psal=65.1, tact=71.7, tcho=16.8, etab=476,
         s_agri=5.9, s_indus=5.7, s_constr=7.6, s_comm=78.2, s_apesas=2.7,
         lat=43.3543, lon=3.5560, role="Station balnéaire · Noilly Prat"),
    dict(code="34023", nom="Balaruc-les-Bains", pop=7139, surf_ha=867.47, dens=824.4, tvam=0.9, sn=-0.3, sm=1.3,
         men=3444, nais=41, deces=51, logts=7729, rp=44.5, rs=54.3, vac=1.2, prop=65.0,
         nvm=26450, pauv=13.0, emp=2267, psal=78.1, tact=74.2, tcho=13.7, etab=287,
         s_agri=2.4, s_indus=5.9, s_constr=8.4, s_comm=71.4, s_apesas=11.8,
         lat=43.4476, lon=3.6922, role="1ʳᵉ station thermale de France"),
    dict(code="34213", nom="Poussan", pop=6797, surf_ha=2991.74, dens=226.0, tvam=2.2, sn=0.2, sm=2.0,
         men=2926, nais=59, deces=62, logts=3173, rp=92.3, rs=2.7, vac=5.0, prop=70.3,
         nvm=25860, pauv=13.0, emp=1389, psal=74.2, tact=78.0, tcho=9.1, etab=178,
         s_agri=2.2, s_indus=10.1, s_constr=12.9, s_comm=62.4, s_apesas=12.4,
         lat=43.4976, lon=3.6623, role="Croissance la plus forte du bassin"),
    dict(code="34113", nom="Gigean", pop=6639, surf_ha=1630.09, dens=400.9, tvam=0.5, sn=0.3, sm=0.3,
         men=2709, nais=66, deces=59, logts=2997, rp=90.5, rs=1.7, vac=7.8, prop=70.5,
         nvm=25740, pauv=16.0, emp=1843, psal=80.1, tact=77.3, tcho=10.5, etab=235,
         s_agri=1.3, s_indus=8.1, s_constr=21.7, s_comm=59.1, s_apesas=9.8,
         lat=43.4953, lon=3.7242, role="Porte nord · échangeur A9"),
    dict(code="34341", nom="Villeveyrac", pop=3972, surf_ha=3726.49, dens=107.0, tvam=0.8, sn=-0.0, sm=0.8,
         men=1614, nais=31, deces=46, logts=1813, rp=88.7, rs=4.1, vac=7.2, prop=72.8,
         nvm=25390, pauv=12.0, emp=851, psal=71.5, tact=81.7, tcho=10.1, etab=112,
         s_agri=9.8, s_indus=10.7, s_constr=19.6, s_comm=50.0, s_apesas=9.8,
         lat=43.4956, lon=3.5931, role="Arrière-pays viticole"),
    dict(code="34333", nom="Vic-la-Gardiole", pop=3428, surf_ha=3071.74, dens=185.4, tvam=0.8, sn=-0.0, sm=0.9,
         men=1681, nais=25, deces=42, logts=2506, rp=67.2, rs=27.5, vac=5.3, prop=66.3,
         nvm=25970, pauv=13.0, emp=694, psal=68.5, tact=80.6, tcho=12.0, etab=147,
         s_agri=7.5, s_indus=7.5, s_constr=21.1, s_comm=55.8, s_apesas=8.2,
         lat=43.4838, lon=3.8046, role="Voisine directe · AOP muscat partagée"),
    dict(code="34159", nom="Mireval", pop=3301, surf_ha=1122.66, dens=298.7, tvam=0.1, sn=-0.6, sm=0.7,
         men=1457, nais=19, deces=41, logts=1593, rp=91.4, rs=3.8, vac=4.8, prop=72.9,
         nvm=27260, pauv=10.0, emp=693, psal=79.4, tact=78.5, tcho=8.0, etab=73,
         s_agri=0.0, s_indus=6.8, s_constr=17.8, s_comm=65.8, s_apesas=9.6,
         lat=43.5158, lon=3.8022, role="Muscat de Mireval · TAD vers Frontignan"),
    dict(code="34165", nom="Montbazin", pop=2877, surf_ha=2148.52, dens=136.2, tvam=-0.4, sn=0.3, sm=-0.8,
         men=1212, nais=29, deces=20, logts=1328, rp=91.9, rs=2.6, vac=5.5, prop=76.7,
         nvm=26870, pauv=11.0, emp=359, psal=57.3, tact=77.8, tcho=9.2, etab=56,
         s_agri=3.6, s_indus=10.7, s_constr=26.8, s_comm=48.2, s_apesas=10.7,
         lat=43.5325, lon=3.6694, role="Village résidentiel en repli"),
    dict(code="34024", nom="Balaruc-le-Vieux", pop=2737, surf_ha=692.37, dens=462.3, tvam=0.7, sn=-0.6, sm=1.3,
         men=1205, nais=10, deces=41, logts=1377, rp=87.7, rs=11.2, vac=1.1, prop=72.7,
         nvm=27840, pauv=7.0, emp=1220, psal=86.5, tact=78.1, tcho=10.2, etab=149,
         s_agri=2.0, s_indus=3.4, s_constr=4.0, s_comm=84.6, s_apesas=6.0,
         lat=43.4650, lon=3.6971, role="Zone commerciale intercommunale"),
    dict(code="34143", nom="Loupian", pop=2169, surf_ha=2325.60, dens=135.6, tvam=0.1, sn=0.2, sm=-0.1,
         men=975, nais=16, deces=19, logts=1291, rp=75.5, rs=14.4, vac=10.1, prop=72.5,
         nvm=25580, pauv=13.0, emp=575, psal=58.4, tact=78.8, tcho=13.0, etab=85,
         s_agri=36.5, s_indus=2.4, s_constr=25.9, s_comm=28.2, s_apesas=7.1,
         lat=43.4509, lon=3.6279, role="Villa gallo-romaine · viticulture"),
    dict(code="34039", nom="Bouzigues", pop=1601, surf_ha=649.85, dens=524.9, tvam=-0.6, sn=-0.1, sm=-0.4,
         men=770, nais=17, deces=8, logts=1060, rp=72.9, rs=22.5, vac=4.5, prop=73.7,
         nvm=29610, pauv=None, emp=412, psal=65.3, tact=75.2, tcho=5.1, etab=97,
         s_agri=26.8, s_indus=6.2, s_constr=8.2, s_comm=51.5, s_apesas=7.2,
         lat=43.4450, lon=3.6563, role="Capitale de l'huître de Thau"),
]

# --------------------------------------------------------------------------
# 2. Les échelles emboîtées (entonnoir) — mêmes indicateurs, autres périmètres
# --------------------------------------------------------------------------
ECHELLES = [
    dict(id="france", nom="France métropolitaine", niveau="Nation", pop=66165815, dens=121.6, tvam=0.4,
         sn=0.1, sm=0.3, men=30473653, logts=36907413, rp=82.4, rs=9.8, vac=7.8, prop=57.6,
         nvm=25920, pauv=15.9, emp=27504543, tact=75.7, tcho=11.0, etab=2344770),
    dict(id="occitanie", nom="Occitanie", niveau="Région", pop=6124653, dens=84.2, tvam=0.8,
         sn=-0.1, sm=0.9, men=2932388, logts=3798163, rp=77.1, rs=15.0, vac=7.9, prop=58.8,
         nvm=24650, pauv=18.6, emp=2428864, tact=74.5, tcho=12.5, etab=222652),
    dict(id="herault", nom="Hérault", niveau="Département", pop=1230289, dens=201.7, tvam=1.2,
         sn=0.1, sm=1.1, men=596084, logts=782278, rp=76.0, rs=17.2, vac=6.7, prop=53.0,
         nvm=24280, pauv=21.0, emp=482010, tact=72.9, tcho=14.5, etab=47229),
    dict(id="montpellier", nom="Montpellier Méditerranée Métropole", niveau="Métropole voisine",
         pop=522542, dens=1238.8, tvam=1.7, sn=0.5, sm=1.2, men=262102, logts=291054,
         rp=89.9, rs=3.9, vac=6.3, prop=41.8, nvm=24750, pauv=22.4, emp=257597,
         tact=71.9, tcho=14.8, etab=20461),
    dict(id="sam", nom="Sète Agglopôle Méditerranée", niveau="Intercommunalité", pop=131216, dens=422.9,
         tvam=0.9, sn=-0.3, sm=1.2, men=64553, logts=91660, rp=70.2, rs=25.7, vac=4.2, prop=58.1,
         nvm=24500, pauv=18.7, emp=40268, tact=73.2, tcho=13.9, etab=4848),
    dict(id="frontignan", nom="Frontignan la Peyrade", niveau="Commune", pop=24136, dens=760.9,
         tvam=1.0, sn=-0.1, sm=1.1, men=11183, logts=14566, rp=76.5, rs=20.6, vac=2.9, prop=61.6,
         nvm=24580, pauv=17.0, emp=6556, tact=75.3, tcho=14.0, etab=671),
]

# --------------------------------------------------------------------------
# 3. Séries temporelles
# --------------------------------------------------------------------------
POP_FRONTIGNAN = {
    "label": "Population municipale de Frontignan (recensements)",
    "annees": [1968, 1975, 1982, 1990, 1999, 2007, 2012, 2017, 2023],
    "valeurs": [11141, 12238, 14951, 16245, 19145, 23068, 22728, 22762, 24136],
    "densites": [351.2, 385.8, 471.3, 512.1, 603.6, 727.2, 716.5, 717.6, 760.9],
    "source": SOURCE_INSEE,
}

AGES_FRONTIGNAN = {
    "label": "Structure par âge (part en %)",
    "classes": ["< 15 ans", "15-24", "25-39", "40-54", "55-64", "65-79", "80 +"],
    "an2012": [16.4, 11.5, 16.5, 21.9, 13.5, 14.1, 6.2],
    "an2017": [16.5, 10.1, 15.5, 21.6, 13.6, 15.8, 6.9],
    "an2023": [14.8, 10.3, 14.6, 19.9, 15.1, 17.4, 7.9],
    "effectifs2023": [3562, 2488, 3532, 4801, 3644, 4209, 1900],
    "source": SOURCE_INSEE,
}

BUDGET_VILLE = {
    "label": "Budget principal de la Ville (M€)",
    "annees": [2022, 2024, 2025, 2026],
    "fonctionnement": [40.5, 45.0, 39.55, 43.9],
    "investissement": [18.5, 24.0, 17.18, 20.9],
    "note": "BP 2022 et BP 2025 votés hors reprise des résultats ; 2024 partiellement estimé ; "
            "2026 = BP + BS + reports. Taux d'imposition inchangés depuis 9 ans.",
    "source": {"t": "Ville de Frontignan (FLP Mag, conseils municipaux) / Midi Libre",
               "u": "https://www.frontignan.fr/flp-mag-36-le-dossier-un-financement-au-cordeau/", "d": "2026"},
}

FINANCES_STRATE = {
    "label": "Frontignan vs moyenne de strate (communes 20-50 000 hab.), comptes 2024",
    "indicateurs": [
        dict(k="Dette par habitant (€)", v=995, ref=986, sens="bas"),
        dict(k="Annuité de la dette (€/hab.)", v=126, ref=163, sens="bas"),
        dict(k="Capacité de désendettement (années)", v=7.5, ref=5.5, sens="bas"),
        dict(k="Impôts locaux (€/hab.)", v=1011, ref=793, sens="bas"),
        dict(k="Charges de personnel (€/hab.)", v=946, ref=849, sens="bas"),
        dict(k="Investissement (€/hab.)", v=270, ref=438, sens="haut"),
        dict(k="Rigidité structurelle (%)", v=66, ref=56, sens="bas"),
    ],
    "source": {"t": "Décomptes publics — comptes 2024",
               "u": "https://www.decomptes-publics.fr/villes/34108-34110-frontignan", "d": "2025"},
}

MOBILITES = {
    "label": "Modes de déplacement domicile-travail des actifs de Frontignan (RP2023, %)",
    "modes": ["Voiture", "Transports en commun", "Marche", "Vélo", "Deux-roues motorisé", "Pas de déplacement"],
    "parts": [80.0, 7.1, 4.4, 2.6, 2.0, 3.9],
    "hors_commune": 67.0,
    "actifs_occupes": 9565,
    "source": SOURCE_INSEE,
}

CLIMAT = {
    "label": "Projections Météo-France TRACC pour l'Hérault / l'Occitanie",
    "lignes": [
        dict(k="Température moyenne", now="référence 1976-2005", h2050="+2,2 °C (+2,5 °C en été)", h2100="+3,5 °C"),
        dict(k="Jours > 35 °C", now="1,3 / an", h2050="7,7 / an", h2100="17,8 / an"),
        dict(k="Nuits tropicales", now="5 / an", h2050="24 / an", h2100="—"),
        dict(k="Jours de sols secs", now="93 / an", h2050="126 / an", h2100="—"),
        dict(k="Niveau de la mer (Méditerranée)", now="0", h2050="+24 cm", h2100="+62 à +81 cm"),
        dict(k="Risque de feu de forêt", now="indice 1", h2050="× 2,5", h2100="—"),
    ],
    "source": {"t": "Météo-France — Quel climat futur en Occitanie ? (TRACC)",
               "u": "https://meteofrance.com/changement-climatique/quel-climat-futur-en-occitanie", "d": "13/05/2026"},
}

SUBMERSION = {
    "label": "Dommages estimés par submersion sur le bassin de Thau (fiche risques du SCoT)",
    "scenarios": [
        dict(k="Aléa décennal (Q10)", bassin=343.5, part_frontignan=33.0),
        dict(k="Aléa centennal (Q100)", bassin=970.9, part_frontignan=26.0),
    ],
    "note": "Montants en M€ de dommages sur l'ensemble du bassin ; Frontignan est la commune la plus exposée. "
            "PPRI : aléa de référence = tempête marine centennale, PHE 2,00 m. A9 impraticable dès Q10.",
    "source": {"t": "SMBT — fiche risques du SCoT du bassin de Thau (arrêt du 15/10/2024)",
               "u": "https://www.smbt.fr/storage/2020/04/3.1.9-ANNEXE-EIE-Fiche-Risques-SCOT-BASIN-DE-THAU-ARRET-15-10-24.pdf",
               "d": "15/10/2024"},
}

MUNICIPALES_2026 = {
    "label": "Municipales du 15 mars 2026 — 1ᵉʳ tour (19 089 inscrits, abstention 38,1 %)",
    "listes": [
        dict(k="Union de la gauche — Michel Arrouy (PS)", voix=5922, pct=51.16, sieges=27),
        dict(k="RN — Cédric Delapierre", voix=4152, pct=35.87, sieges=6),
        dict(k="DVD — Thibaut Cléret-Villagordo", voix=1501, pct=12.97, sieges=2),
    ],
    "source": {"t": "Midi Libre / résultats officiels", "u": "https://www.midilibre.fr/2026/03/15/resultats-des-municipales-2026-a-frontignan-le-maire-sortant-michel-arrouy-fait-le-grand-chelem-et-conserve-son-poste-13274171.php", "d": "15/03/2026"},
}

# --------------------------------------------------------------------------
# 4. Projets — portefeuille chiffré et daté
# --------------------------------------------------------------------------
PROJETS = [
    dict(id="friche-mobil", nom="Friche ExxonMobil (11 ha)", cout=None, debut=2026, fin=2035,
         statut="engagé", moa="Ville de Frontignan", impact=5, maturite=2,
         note="Restitution des 11 ha dépollués à la Ville le 27 mai 2026. Études d'usages fin 2026."),
    dict(id="pem-gare", nom="Gare nouvelle & PEM", cout=25.0, debut=2026, fin=2029,
         statut="annoncé", moa="Région Occitanie / SNCF Réseau / agglo / Ville", impact=5, maturite=3,
         note="25 M€ : Région 40 % plafonnés à 10 M€, agglo 20 %, État, Ville. Livraison visée 2028-2029."),
    dict(id="oru-coeur-ville", nom="ORU Cœur de Ville", cout=15.0, debut=2023, fin=2033,
         statut="engagé", moa="Ville", impact=4, maturite=4,
         note="Opération de renouvellement urbain, ≈ 15 M€ sur 10 ans ; label Action cœur de Ville (mars 2025)."),
    dict(id="port-plaisance", nom="Restructuration du port de plaisance", cout=4.5, debut=2026, fin=2029,
         statut="engagé", moa="Régie Frontignan Plaisance / Ville", impact=3, maturite=4,
         note="603 → 750 anneaux (plafond SCoT : 880). Chantier lancé hiver 2025-2026."),
    dict(id="centre-aquatique", nom="Centre aquatique intercommunal (Hierles)", cout=None, debut=2026, fin=2030,
         statut="annoncé", moa="Sète Agglopôle Méditerranée", impact=4, maturite=3,
         note="Études 2025 (100 k€), marchés lancés au budget agglo 2026 ; coût public non publié."),
    dict(id="mas-de-chave", nom="Secteur Mas de Chave (≈ 400 logements)", cout=None, debut=2025, fin=2032,
         statut="incertain", moa="Ville + aménageur", impact=3, maturite=2,
         note="Programme ramené de 336-450 à ≈ 400 logements ; concertation reprise le 15 juillet 2026."),
    dict(id="tcsp-rd2", nom="TCSP / voie bus prioritaire RD2", cout=42.0, debut=2024, fin=2030,
         statut="engagé", moa="Sète Agglopôle Méditerranée", impact=4, maturite=3,
         note="12 M€ phase 1 (en service janv. 2026) + ≈ 30 M€ de sections Frontignan/Balaruc annoncées."),
    dict(id="le-quai", nom="Pôle culturel Le Quai (chais Botta)", cout=2.6, debut=2022, fin=2025,
         statut="livré", moa="Ville / DSP Véo Cinémas", impact=3, maturite=5,
         note="Cinéma 3 salles ouvert en décembre 2025 (2,6 M€ pour l'espace cinéma), glissement de ~18 mois."),
    dict(id="quai-voltaire", nom="Quai Voltaire & passerelle", cout=1.5, debut=2024, fin=2025,
         statut="livré", moa="Ville / Humbert & David", impact=2, maturite=5,
         note="Promenade apaisée, piste cyclable, 1 300 m² d'espaces verts (volet 2025 : 1,5 M€)."),
    dict(id="zae-barnier", nom="Requalification de la ZAE du Barnier", cout=2.7, debut=2025, fin=2027,
         statut="engagé", moa="SPL Bassin de Thau", impact=3, maturite=4,
         note="2,7 M€, livraison annoncée juin 2027 — support d'emplois locaux."),
    dict(id="terres-blanches", nom="Groupe scolaire Terres-Blanches (cours oasis)", cout=3.1, debut=2025, fin=2027,
         statut="engagé", moa="Ville", impact=2, maturite=4,
         note="765 k€ désimperméabilisation + rénovation, 2,3 M€ rénovation thermique."),
    dict(id="maison-mathieu", nom="Salle de spectacle Maison Mathieu (≈ 150 places)", cout=0.22, debut=2025, fin=2027,
         statut="engagé", moa="Ville", impact=2, maturite=3,
         note="220 k€ inscrits au BP 2025 ; ex-Cinémistral fermé en avril 2025."),
    dict(id="lido", nom="Protection et mise en valeur du lido (7 km)", cout=13.5, debut=2012, fin=2030,
         statut="tendance", moa="État / Région / agglo", impact=4, maturite=2,
         note="≈ 13,5 M€ HT (estimation AVP 2012, à actualiser) ; désormais cadré par le PPA trait de côte."),
]

# --------------------------------------------------------------------------
# 5. Acteurs — cartographie pouvoir / intérêt
# --------------------------------------------------------------------------
# influence : capacité à décider ou bloquer (1-5)  [estimation d'analyste, fiabilité C]
# interet   : intensité de l'enjeu pour l'acteur (1-5)
# ressource : nature du levier détenu
# posture   : attitude probable vis-à-vis d'une mission de design de services
ACTEURS = [
    dict(id="a-arrouy", nom="Michel Arrouy", role="Maire (PS), réélu au 1ᵉʳ tour en 2026",
         famille="Institutionnel", influence=5, interet=5, ressource="Décision politique, agenda, budget",
         posture="Commanditaire — arbitre final", echelle="Commune"),
    dict(id="a-linares", nom="Loïc Linares", role="Président de Sète Agglopôle, élu frontignanais",
         famille="Institutionnel", influence=5, interet=4, ressource="Budget agglo 242 M€, compétences mobilités/eau/déchets",
         posture="Allié structurel — clé de l'échelle intercommunale", echelle="Agglo"),
    dict(id="a-adjoints", nom="Adjoints & conseillers délégués", role="Cadre de vie, culture, urbanisme, participation, risques, finances",
         famille="Institutionnel", influence=4, interet=5, ressource="Portefeuilles thématiques, relais terrain",
         posture="Co-constructeurs quotidiens de la mission", echelle="Commune"),
    dict(id="a-services", nom="Services municipaux (≈ 700 agents)", role="DGS, urbanisme, technique, culture, communication",
         famille="Institutionnel", influence=4, interet=4, ressource="Maîtrise d'ouvrage, données, continuité",
         posture="Alliés indispensables — attention à la charge", echelle="Commune"),
    dict(id="a-opposition", nom="Opposition (RN 6 élus, DVD 2)", role="35,9 % des voix au 1ᵉʳ tour 2026",
         famille="Institutionnel", influence=2, interet=4, ressource="Tribune, représentation d'un électorat massif",
         posture="À ne pas ignorer : la concertation doit être inattaquable", echelle="Commune"),
    dict(id="a-etat", nom="État / Préfecture de l'Hérault", role="ACV, PPRI, PPRT, ZAN, Fonds vert, DSIL",
         famille="Institutionnel", influence=5, interet=3, ressource="Réglementation et subventions",
         posture="Cadre contraignant + guichet — dossiers à documenter", echelle="National"),
    dict(id="a-region", nom="Région Occitanie", role="Gare/PEM (≤ 10 M€), TER, Plan Littoral 21, friches",
         famille="Institutionnel", influence=5, interet=4, ressource="Financement du PEM et de la desserte",
         posture="Décideur du calendrier ferroviaire — à sécuriser", echelle="Région"),
    dict(id="a-departement", nom="Département de l'Hérault", role="RD2, chemin de halage, collèges, social",
         famille="Institutionnel", influence=3, interet=3, ressource="Voirie départementale, action sociale",
         posture="Partenaire d'aménagement de proximité", echelle="Département"),
    dict(id="a-smbt", nom="SMBT — Syndicat mixte du bassin de Thau", role="SCoT, SAGE, gestion de la lagune",
         famille="Institutionnel", influence=4, interet=4, ressource="Règles d'urbanisme opposables",
         posture="Cadre juridique du littoral — à mobiliser en amont", echelle="Bassin"),
    dict(id="a-anct", nom="ANCT", role="Action cœur de Ville, ingénierie territoriale",
         famille="Institutionnel", influence=3, interet=2, ressource="Ingénierie, cofinancement d'études",
         posture="Levier d'expertise sous-utilisé", echelle="National"),
    dict(id="a-sncf", nom="SNCF Réseau / SNCF Gares & Connexions", role="Maîtrise d'ouvrage ferroviaire du PEM",
         famille="Institutionnel", influence=4, interet=3, ressource="Emprise et calendrier ferroviaires",
         posture="Contrainte technique majeure du projet gare", echelle="National"),
    dict(id="a-bdt", nom="Banque des Territoires / EPF Occitanie", role="PPA recomposition spatiale, portage foncier",
         famille="Institutionnel", influence=3, interet=3, ressource="Ingénierie financière, foncier",
         posture="Partenaires du temps long littoral", echelle="National"),
    dict(id="a-cave", nom="Cave coopérative Frontignan Muscat", role="≈ 80 % de l'AOP, 1904, ≈ 9 M€ de CA",
         famille="Économique", influence=3, interet=4, ressource="Patrimoine, marque, foncier viticole",
         posture="Pivot de la stratégie œnotouristique", echelle="Commune"),
    dict(id="a-vignerons", nom="8 vignerons indépendants", role="≈ 800 ha d'AOP avec Vic-la-Gardiole",
         famille="Économique", influence=2, interet=4, ressource="Paysage, récit, accueil",
         posture="Alliés d'un parcours muscat", echelle="Commune"),
    dict(id="a-hexis", nom="Hexis & industriels de La Peyrade", role="≈ 194 salariés (Hexis), 55 entreprises en ZA",
         famille="Économique", influence=3, interet=3, ressource="Emploi productif, taxe économique",
         posture="À associer à la programmation de la friche", echelle="Commune"),
    dict(id="a-seveso", nom="GDH & SCORI (Seveso seuil haut)", role="Dépôt d'hydrocarbures, traitement de déchets",
         famille="Économique", influence=3, interet=2, ressource="PPRT — servitudes d'urbanisme",
         posture="Contrainte foncière et enjeu d'image", echelle="Commune"),
    dict(id="a-conchyliculteurs", nom="Conchyliculteurs & pêcheurs de Thau", role="≈ 4 000 emplois de filière sur le bassin",
         famille="Économique", influence=3, interet=5, ressource="Identité, économie bleue, alerte sanitaire",
         posture="Baromètre de la santé du territoire", echelle="Bassin"),
    dict(id="a-commercants", nom="Commerçants du centre-ville", role="≈ 180 commerces, vacance ≈ 4 %",
         famille="Économique", influence=2, interet=5, ressource="Vitalité perçue du cœur de ville",
         posture="Fatigue des chantiers — quick wins nécessaires", echelle="Commune"),
    dict(id="a-tourisme", nom="Office de tourisme intercommunal « Archipel de Thau »", role="Présidé par K. Gouvernayre (Frontignan)",
         famille="Économique", influence=3, interet=4, ressource="Promotion, données de fréquentation",
         posture="Canal de la désaisonnalisation", echelle="Agglo"),
    dict(id="a-promoteurs", nom="Promoteurs & aménageurs", role="Mas de Chave, Pielles, opérations privées",
         famille="Économique", influence=3, interet=4, ressource="Capacité à produire du logement",
         posture="À encadrer par la qualité et la mixité", echelle="Commune"),
    dict(id="a-comites", nom="6 comités habitants & budget participatif", role="50 000 €/an, Maison des projets (2021)",
         famille="Société civile", influence=2, interet=4, ressource="Légitimité d'usage, veille de terrain",
         posture="Infrastructure participative existante à outiller", echelle="Commune"),
    dict(id="a-assos", nom="Associations (FIRN, joutes, patrimoine, environnement)", role="FIRN depuis 1998, 29ᵉ édition en 2026",
         famille="Société civile", influence=2, interet=4, ressource="Capital culturel et bénévole",
         posture="Producteurs de récit local", echelle="Commune"),
    dict(id="a-qpv", nom="Habitants des QPV (Deux Pins, centre)", role="Contrat de ville Quartiers 2030 (2024-2030)",
         famille="Société civile", influence=1, interet=5, ressource="Expérience vécue des services publics",
         posture="Public prioritaire — inclusion à construire", echelle="Commune"),
    dict(id="a-seniors", nom="Seniors (25,3 % de 65 ans et +)", role="28,1 % des 65-79 ans vivent seuls",
         famille="Société civile", influence=2, interet=5, ressource="Temps, mémoire, usage quotidien",
         posture="Cible n°1 du confort urbain (chaleur, marche, santé)", echelle="Commune"),
    dict(id="a-jeunes", nom="Jeunes 15-24 ans (10,3 %)", role="Chômage des 15-24 ans : 28,9 %",
         famille="Société civile", influence=1, interet=4, ressource="Usages numériques, avenir du territoire",
         posture="Grand absent des dispositifs classiques", echelle="Commune"),
    dict(id="a-navetteurs", nom="Navetteurs (67 % des actifs)", role="80 % en voiture, double bassin Sète/Montpellier",
         famille="Société civile", influence=1, interet=5, ressource="Masse critique du PEM",
         posture="Utilisateurs finaux du projet gare", echelle="Bassin"),
    dict(id="a-riverains", nom="Riverains de La Peyrade & des chantiers", role="Mobilisés sur Mas de Chave (2025-2026)",
         famille="Société civile", influence=2, interet=5, ressource="Capacité de blocage / contentieux",
         posture="Co-conception obligatoire, sinon recours", echelle="Commune"),
    dict(id="a-presse", nom="Presse locale (Midi Libre, Hérault Tribune, Plurielle)", role="Fabrique de l'opinion territoriale",
         famille="Société civile", influence=3, interet=3, ressource="Mise à l'agenda, récit public",
         posture="Relais des preuves visibles", echelle="Bassin"),
]

# --------------------------------------------------------------------------
# 6. Prospective : scénarios 2040 et conditions de succès 2030
# --------------------------------------------------------------------------
SCENARIOS = [
    dict(id="s1", nom="S1 — Thau tranquille", pop2040="24-25 000", emplois="stables", proba=30,
         moteur="Stagnation du bassin (+0,05 %/an), friche sous-aménagée, PEM sous-utilisé",
         risque="Banlieue résidentielle vieillissante (65+ > 30 %), déclin des services, abstention"),
    dict(id="s2", nom="S2 — Couronne métropolitaine", pop2040="> 27 000", emplois="précaires/saisonniers", proba=30,
         moteur="Débordement du Montpelliérain (60 % des gains départementaux), spéculation littorale",
         risque="Résidences secondaires 25-30 %, gentrification du centre, conflits d'usages"),
    dict(id="s3", nom="S3 — Pôle de la transition ★", pop2040="≈ 26 000", emplois="+500 à +1 000", proba=40,
         moteur="Friche + PEM + identité (muscat, FIRN, Thau) = renaissance économique et culturelle",
         risque="Fatigue participative si les promesses 2026-2030 ne tiennent pas"),
]

CONDITIONS_2030 = [
    dict(k="PEM livré ET desservi", cible="2028-2029 + cadence TER", etat="en cours", poids=5),
    dict(k="Programmation de la friche validée et financée", cible="2027-2028", etat="à risque", poids=5),
    dict(k="Emploi local en progression", cible="+300 à +600 postes", etat="à prouver", poids=4),
    dict(k="Qualité de l'eau de Thau en amélioration", cible="fin des suspensions sanitaires", etat="critique", poids=5),
    dict(k="Trajectoire démographique sans gentrification", cible="loyers, vacance, mixité", etat="à surveiller", poids=4),
]

JALONS = [
    dict(an=2026, k="Restitution des 11 ha dépollués (27 mai) · budget agglo 242 M€ · SCoT attendu", type="engagé"),
    dict(an=2027, k="Programmation de la friche · PLU révisé · cartes PPA 30/100 ans · ZAE Barnier livrée", type="annoncé"),
    dict(an=2028, k="Livraison visée du PEM · premières autorisations Mas de Chave", type="annoncé"),
    dict(an=2029, k="Fin des travaux du port (750 anneaux) · démarrage des travaux LGV phase 1", type="annoncé"),
    dict(an=2030, k="Centre aquatique en service · premiers usages sur la friche · règles PPA figées", type="tendance"),
    dict(an=2032, k="Municipales : mandature d'exécution jugée sur pièces", type="tendance"),
    dict(an=2034, k="LGV phase 1 en service : bascule TGV → TER du quotidien", type="tendance"),
    dict(an=2040, k="LGV phase 2 · recomposition de Frontignan-Plage engagée · projet de territoire agglo", type="tendance"),
]
