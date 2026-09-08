# -*- coding: utf-8 -*-
"""
Graphe de connaissance de l'Atlas Frontignan : nœuds, liens, arborescence
heuristique et scénario de présentation (slides).

Schéma d'un nœud
----------------
id     : identifiant unique (slug)
label  : nom affiché au cœur du nœud
type   : territoire | commune | acteur | projet | risque | politique | ressource | futur | data
tier   : 0 Frontignan (cœur) · 1 la ville · 2 l'agglo de Thau · 3 les environs · 4 la France
icon   : glyphe de repli quand il n'y a pas d'image
img    : image affichée au cœur du nœud (chemin relatif à atlas/index.html)
sub    : sous-titre court (une ligne)
txt    : texte de fond (2-5 phrases)
facts  : chiffres clés [(libellé, valeur)]
bul    : puces d'analyse
src    : sources [(titre, url, date)]
data   : clé d'un jeu de données statistique à afficher dans le panneau
parent : parent dans la carte heuristique
"""

F = "../figures/"
V = "../visuals/"
I = "img/"

NODES = [
    # ================= TIER 0 — le cœur =================
    dict(id="frontignan", label="Frontignan la Peyrade", type="territoire", tier=0, icon="🍇",
         img=V + "hero-frontignan-2030.jpg", parent=None,
         sub="24 136 hab. · siège de Sète Agglopôle · 34110",
         txt="Ville littorale de 24 136 habitants (2023) entre Sète (7 km) et Montpellier (21 km), au pied de la "
             "Gardiole et entre étangs, canal et lido. 2ᵉ commune et siège de Sète Agglopôle Méditerranée, elle "
             "entame en 2026 le plus grand cycle de transformation urbaine depuis les années 1970 : 11 ha de friche "
             "dépolluée restitués, une gare nouvelle actée, un label Action cœur de Ville et la présidence de l'agglo.",
         facts=[("Population 2023", "24 136 hab."), ("Densité", "760,9 hab./km²"), ("Superficie", "40,0 km²"),
                ("Niveau de vie médian", "24 580 €/UC"), ("Taux de pauvreté", "17,0 %"),
                ("Chômage 15-64 ans", "14,0 %"), ("Emplois sur place", "6 556")],
         bul=["Croissance portée à 100 % par le solde migratoire (+1,1 %/an) : une attractivité réversible.",
              "1 emploi local pour 1,5 actif résident → ville d'habitat à ré-équiper en emplois.",
              "Cumul rare : siège de l'agglo + présidence + vice-présidence tourisme."],
         src=[("INSEE — Comparateur de territoires", "https://www.insee.fr/fr/statistiques/1405599?geo=COM-34108", "27/08/2026")],
         data="communes"),

    # ================= TIER 1 — la ville =================
    dict(id="identite", label="Identité & mémoire", type="ressource", tier=1, icon="🏺",
         img=I + "node-muscat.jpg", parent="frontignan",
         sub="Muscat · sel · pétrole · polar · joutes",
         txt="Quatre couches de mémoire structurent l'image de la ville : le muscat (AOP 1936, 90 ans en 2026), "
             "le sel (salins fermés en 1968, devenus espace naturel de 149 ha), le pétrole (raffinerie Mobil "
             "fermée en 1986) et le roman noir (FIRN depuis 1998). Un capital symbolique riche mais éclaté, "
             "encore peu traduit en stratégie d'expérience.",
         facts=[("AOP Muscat", "1936 — 1ʳᵉ appellation muscat de France"), ("Salins", "149 ha, fermés en 1968"),
                ("Raffinerie", "1904-1986, 11 ha restitués en 2026"), ("FIRN", "29ᵉ édition en 2026")],
         bul=["Marqueurs forts mais non fédérés : pas de plateforme de marque territoriale.",
              "Trois pôles urbains à relier : centre médiéval, La Peyrade, Frontignan-Plage."],
         src=[("Ville de Frontignan — dossier Muscat 90 ans", "https://www.frontignan.fr/flp-mag-51-le-dossier-muscat-90-ans-dappellation-celebres/", "06/07/2026")]),

    dict(id="demographie", label="Démographie", type="data", tier=1, icon="👥",
         img=F + "fig2_population.png", parent="frontignan",
         sub="+6,0 % depuis 2017 · âge médian ≈ 45 ans",
         txt="La ville a retrouvé une croissance (+1,0 %/an entre 2017 et 2023) après dix ans de stagnation, mais "
             "elle vieillit : 25,3 % de 65 ans et plus, un solde naturel devenu négatif (−0,1 %/an) et 9,4 ‰ de "
             "natalité contre 10,5 ‰ de mortalité.",
         facts=[("1968 → 2023", "11 141 → 24 136 hab."), ("Variation 2017-2023", "+1,0 %/an"),
                ("65 ans et +", "25,3 %"), ("Moins de 15 ans", "14,8 %"), ("Ménages", "11 183"),
                ("Taille moyenne des ménages", "2,1")],
         bul=["Croissance longue : TCAM 1968-2023 = +1,42 %/an, mais rupture nette après 2007.",
              "Le vieillissement est plus rapide que la croissance : +5,0 points de 65 ans et + depuis 2012."],
         src=[("INSEE — RP2023", "https://www.insee.fr/fr/statistiques/2011101?geo=COM-34108", "27/08/2026")],
         data="pop_serie"),

    dict(id="ages", label="Pyramide des âges", type="data", tier=1, icon="📊",
         img=F + "fig3_ages_csp.png", parent="demographie",
         sub="Vieillissement net entre 2012 et 2023",
         txt="En onze ans, la structure par âge bascule : les moins de 15 ans perdent 1,6 point, les 65-79 ans en "
             "gagnent 3,3 et les 80 ans et plus 1,7. Les 55 ans et plus représentent désormais 40,4 % de la population.",
         facts=[("65-79 ans", "17,4 % (14,1 % en 2012)"), ("80 ans et +", "7,9 %"),
                ("Personnes seules 65-79 ans", "28,1 %"), ("Familles monoparentales", "16,8 %")],
         bul=["Deux bouts de pyramide à tenir simultanément : petite enfance et grand âge.",
              "L'espace public doit intégrer confort thermique, repos et accessibilité."],
         src=[("INSEE — RP2023", "https://www.insee.fr/fr/statistiques/2011101?geo=COM-34108", "27/08/2026")],
         data="ages"),

    dict(id="revenus", label="Revenus & pauvreté", type="data", tier=1, icon="💶",
         img=None, parent="frontignan",
         sub="24 580 €/UC · 17 % de pauvreté",
         txt="Le niveau de vie médian frontignanais (24 580 €) est proche de la moyenne du bassin (24 500 €) et de "
             "l'Hérault (24 280 €), mais reste 5,2 % sous la France métropolitaine (25 920 €). Le taux de pauvreté "
             "de 17 % est supérieur à la moyenne nationale (15,9 %) tout en étant nettement inférieur à Sète (26 %).",
         facts=[("Niveau de vie médian", "24 580 €/UC"), ("Écart à la France", "−1 340 € (−5,2 %)"),
                ("Taux de pauvreté", "17,0 %"), ("Rang dans l'agglo", "9ᵉ / 13 pour le niveau de vie")],
         bul=["Frontignan est la commune médiane du bassin : ni Sète (26 % de pauvreté), ni Balaruc-le-Vieux (7 %).",
              "L'écart intercommunal de niveau de vie atteint 6 870 € entre Bouzigues et Sète."],
         src=[("INSEE — Filosofi 2023", "https://www.insee.fr/fr/statistiques/1405599?geo=COM-34108", "27/08/2026")],
         data="communes"),

    dict(id="emploi", label="Emploi & navettes", type="data", tier=1, icon="🧰",
         img=F + "fig9_mobilites.png", parent="frontignan",
         sub="14,0 % de chômage · 67 % de navetteurs",
         txt="6 556 emplois au lieu de travail pour 9 565 actifs occupés : la ville n'offre qu'un emploi pour "
             "1,5 actif résident. 67 % des actifs travaillent hors de la commune, dont l'essentiel vers Sète et "
             "Montpellier, et 80 % s'y rendent en voiture.",
         facts=[("Emplois au lieu de travail", "6 556"), ("Taux de chômage 15-64", "14,0 %"),
                ("Chômage des 15-24 ans", "28,9 %"), ("Actifs travaillant hors commune", "67 %"),
                ("Part voiture", "80 %"), ("Part transports en commun", "7,1 %")],
         bul=["Le ratio emploi/actif (0,69) est la justification économique de la friche Mobil.",
              "Un gradient social fort : 26,2 % de chômage chez les sans-diplôme contre 6,9 % à bac+5."],
         src=[("INSEE — RP2023", "https://www.insee.fr/fr/statistiques/2011101?geo=COM-34108", "27/08/2026")],
         data="mobilites"),

    dict(id="economie", label="Tissu économique", type="ressource", tier=1, icon="🏭",
         img=None, parent="frontignan",
         sub="2 263 établissements · 6 311 postes salariés",
         txt="Économie résidentielle et publique (39,9 % des emplois en administration, enseignement, santé, action "
             "sociale) avec un socle industriel rare pour une ville littorale de cette taille (16,4 % des emplois), "
             "concentré sur la Z.A. de La Peyrade (15,4 ha, 55 entreprises).",
         facts=[("Établissements actifs", "2 263"), ("Postes salariés", "6 311"),
                ("Sphère présentielle", "67 %"), ("Établissements de 50 salariés et +", "18"),
                ("Créations", "≈ 470/an")],
         bul=["Hexis (≈ 194 salariés) est le premier employeur industriel privé.",
              "La ZAE du Barnier (2,7 M€, livraison juin 2027) est le vivier d'emplois de court terme."],
         src=[("INSEE — Flores 2024", "https://www.insee.fr/fr/statistiques/2011101?geo=COM-34108", "27/08/2026")],
         data="secteurs"),

    dict(id="budget", label="Budget & finances", type="data", tier=1, icon="🏛️",
         img=F + "fig4_budget.png", parent="frontignan",
         sub="≈ 65 M€ · dette 995 €/hab. · taux stables depuis 9 ans",
         txt="Des comptes sains mais contraints : une fiscalité déjà élevée (1 011 €/hab. contre 793 € pour la "
             "strate) qui interdit de financer l'investissement par l'impôt, une épargne nette en reconstruction "
             "(1,4 M€ en 2025) et un investissement par habitant contenu (270 € contre 438 €).",
         facts=[("Budget 2026 (BP+BS+reports)", "64,9 M€"), ("Dette/hab. 2024", "995 € (strate : 986 €)"),
                ("Capacité de désendettement", "7,5 ans (strate : 5,5)"), ("Investissement/hab.", "270 € (strate : 438)"),
                ("Épargne nette 2025", "≈ 1,4 M€")],
         bul=["Écart-type des ratios vs strate : la ville est atypique surtout par sa pression fiscale (+27,5 %).",
              "Conséquence design : projets à fort effet de levier, phasés, avec des preuves rapides et peu coûteuses."],
         src=[("Décomptes publics — comptes 2024", "https://www.decomptes-publics.fr/villes/34108-34110-frontignan", "2025")],
         data="finances"),

    dict(id="gouvernance", label="Gouvernance municipale", type="acteur", tier=1, icon="🗳️",
         img=I + "node-gouvernance.jpg", parent="frontignan",
         sub="Arrouy réélu à 51,16 % · RN à 35,87 %",
         txt="Michel Arrouy (PS) est réélu dès le 1ᵉʳ tour le 15 mars 2026 avec 51,16 % et 27 sièges sur 35, en "
             "remportant les 19 bureaux de vote. Mais le RN atteint 35,87 % et l'abstention 38,1 % : une société "
             "clivée que tout dispositif participatif doit prendre au sérieux.",
         facts=[("Maire", "Michel Arrouy (PS), 2ᵉ mandat"), ("Majorité", "27 sièges / 35"),
                ("Opposition", "RN 6 · DVD 2"), ("Abstention", "38,1 %"), ("Prochaine échéance", "municipales 2032")],
         bul=["Mandat frais 2026-2032 : fenêtre d'action réelle 2026-2029.",
              "10 adjoints dont plusieurs portefeuilles directement « design-pertinents » (cadre de vie, patrimoine, participation)."],
         src=[("Midi Libre — résultats 2026", "https://www.midilibre.fr/2026/03/15/resultats-des-municipales-2026-a-frontignan-le-maire-sortant-michel-arrouy-fait-le-grand-chelem-et-conserve-son-poste-13274171.php", "15/03/2026")],
         data="municipales"),

    dict(id="participation", label="Démocratie participative", type="acteur", tier=1, icon="🤝",
         img=None, parent="gouvernance",
         sub="6 comités habitants · 50 k€ de budget participatif",
         txt="La ville dispose déjà d'une infrastructure participative : Maison des projets et de la Citoyenneté "
             "(2021), six comités habitants (2022), budget participatif de 50 000 €/an, concertations "
             "réglementaires et « ateliers du territoire ». Elle est sous-outillée en méthodes de design.",
         facts=[("Maison des projets", "ouverte en septembre 2021"), ("Comités habitants", "6 (ex-11 conseils de quartier)"),
                ("Budget participatif", "50 000 €/an"), ("Contrat de ville", "Quartiers 2030 (2024-2030)")],
         bul=["Risque identifié : la parole se concentre sur les habitants déjà organisés.",
              "Deux dossiers exigent une concertation irréprochable : friche Mobil et Mas de Chave."],
         src=[("Ville de Frontignan — concertation citoyenne", "https://www.frontignan.fr/la-concertation-citoyenne-est-lancee/", "28/09/2021")]),

    # --- quartiers ---
    dict(id="q-centre", label="Frontignan-centre", type="territoire", tier=1, icon="🏘️",
         img=I + "node-coeur-ville.jpg", parent="frontignan",
         sub="Cœur médiéval · halles · chantier permanent depuis 2023",
         txt="Le centre historique concentre l'ORU (≈ 15 M€ sur 10 ans), les commerces (vacance ≈ 4 %), le marché "
             "et le stationnement gratuit. Il est en travaux depuis 2023 et le restera jusqu'en 2029+, ce qui use "
             "commerçants et riverains.",
         facts=[("Vacance commerciale", "≈ 4 % (moyenne strate ≈ 12 %)"), ("Commerces", "≈ 180"),
                ("ORU", "≈ 15 M€ / 10 ans"), ("Label", "Action cœur de Ville (mars 2025)")],
         bul=["Le « design des transitions » de chantier est le quick win le plus rentable.",
              "QPV centre (Calmette, Anatole-France) : attention à la paupérisation."]),

    dict(id="q-peyrade", label="La Peyrade", type="territoire", tier=1, icon="⚙️",
         img=None, parent="frontignan",
         sub="Quartier canal · zone d'activité · Seveso",
         txt="Quartier nord de la ville, adossé au canal du Rhône à Sète et à la zone d'activité (15,4 ha, "
             "55 entreprises). Il porte la mémoire industrielle, les deux sites Seveso seuil haut et la "
             "mobilisation habitante la plus vive (Mas de Chave).",
         facts=[("Z.A. de La Peyrade", "15,4 ha · 55 entreprises"), ("Hexis", "≈ 194 salariés"),
                ("Sites Seveso seuil haut", "2 (GDH, SCORI) + PPRT")],
         bul=["Interface la plus sensible entre habitat, industrie et projet urbain.",
              "La limite avec l'AOP muscat est le point dur du dossier Mas de Chave."]),

    dict(id="q-plage", label="Frontignan-Plage", type="territoire", tier=1, icon="🏖️",
         img=I + "node-littoral.jpg", parent="frontignan",
         sub="Station · lido 7 km · scénario de recomposition",
         txt="La station balnéaire concentre le port de plaisance, le lido de 7 km et l'essentiel des ≈ 3 000 "
             "résidences secondaires (20,6 % du parc). C'est aussi le secteur le plus exposé : le PPA de 2024 "
             "prévoit explicitement un « scénario de recomposition spatiale de Frontignan-Plage ».",
         facts=[("Lido", "7 km (canal de Sète → Aresquiers)"), ("Résidences secondaires", "20,6 % du parc communal"),
                ("Campings", "6 (508 emplacements)"), ("Hôtels", "3 (130 chambres)")],
         bul=["Offre hôtelière quasi inexistante : la station capte peu de valeur.",
              "La recomposition sera d'abord un problème d'acceptabilité, donc de design de la concertation."]),

    dict(id="q-hierles", label="Les Hierles", type="territoire", tier=1, icon="🏊",
         img=None, parent="frontignan",
         sub="Futur centre aquatique intercommunal · friche Lafarge",
         txt="Quartier retenu pour le centre aquatique intercommunal (marchés lancés au budget agglo 2026) et "
             "concerné par l'étude de renaturation de la friche Lafarge.",
         facts=[("Centre aquatique", "études 2025 (100 k€), marchés 2026"), ("Horizon", "2028-2030")]),

    dict(id="q-qpv", label="QPV Deux Pins & centre", type="territoire", tier=1, icon="🏢",
         img=None, parent="frontignan",
         sub="Contrat de ville Quartiers 2030 (2024-2030)",
         txt="Quartiers prioritaires élargis en 2024 (Deux Pins, puis Calmette et Anatole-France au centre). "
             "Crédits d'intervention annuels et appels à projets — un levier de financement pour des dispositifs "
             "de design social.",
         facts=[("Périmètre", "Deux Pins + centre (Calmette, Anatole-France)"), ("Cadre", "Quartiers 2030, 2024-2030")]),

    # --- projets ---
    dict(id="friche-mobil", label="Friche ExxonMobil", type="projet", tier=1, icon="🏗️",
         img=I + "node-friche-mobil.jpg", parent="frontignan",
         sub="11 ha dépollués restitués le 27 mai 2026",
         txt="Le projet du siècle frontignanais : 11 hectares en cœur de ville, dépollués de 2022 à 2026 selon le "
             "principe pollueur-payeur et restitués à la Ville le 27 mai 2026. Les études d'usages rendent leurs "
             "résultats fin 2026 ; l'arrêté de récolement n'autorise pour l'instant qu'un usage industriel.",
         facts=[("Surface", "11 ha"), ("Restitution", "27 mai 2026"), ("Dépollution", "2022-2026, pollueur-payeur"),
                ("Ambition", "emplois non délocalisables + quartier de gare"), ("Premiers usages", "≈ 2030")],
         bul=["Foncier public rarissime : un « martyr foncier » déjà consommé, donc une avance en régime ZAN.",
              "Point de fragilité : les usages tertiaires/culturels dépendent d'études complémentaires.",
              "Usages transitoires dès 2027 = la meilleure façon de tenir le récit pendant 8 ans de projet."],
         src=[("Rapport d'analyse territoriale §7.2", "rapport-frontignan-analyse-territoriale.md", "08/09/2026")]),

    dict(id="pem-gare", label="Gare nouvelle & PEM", type="projet", tier=1, icon="🚉",
         img=I + "node-gare-pem.jpg", parent="frontignan",
         sub="25 M€ · livraison visée 2028-2029",
         txt="Déplacement de la gare et création d'un pôle d'échanges multimodal sur la friche Mobil, chiffré à "
             "25 M€ (Région 40 % plafonnés à 10 M€, agglo 20 %, État, Ville). Livré avant la bascule LGV de 2034, "
             "le PEM est conçu pour un monde de « trains du quotidien ».",
         facts=[("Coût", "25 M€"), ("Financement", "Région ≤ 10 M€ · agglo 20 % · État · Ville"),
                ("Horizon", "2028-2029"), ("Ligne", "Montpellier-Sète, axe TER le plus fréquenté d'Occitanie")],
         bul=["Le vrai risque n'est pas le bâtiment, c'est la cadence TER après 2034 (SERM non contractualisé).",
              "Le PEM est le seul projet capable de faire bouger la part modale (80 % de voiture aujourd'hui)."],
         src=[("Vision 2026-2040 §1.3", "vision-frontignan-2026-2040.md", "08/09/2026")]),

    dict(id="oru", label="ORU Cœur de Ville", type="projet", tier=1, icon="🧱",
         img=F + "fig5_frise_projets.png", parent="q-centre",
         sub="≈ 15 M€ sur 10 ans · label ACV 2025",
         txt="Opération de renouvellement urbain matricielle : requalification des espaces publics, habitat, "
             "commerces. Le label Action cœur de Ville obtenu en mars 2025 apporte ingénierie ANCT et accès "
             "renforcé aux dispositifs (Fonds vert, DSIL).",
         facts=[("Enveloppe", "≈ 15 M€ / 10 ans"), ("Label ACV", "mars 2025, convention juin 2025"),
                ("Maîtrise d'œuvre espaces publics", "Humbert & David")],
         bul=["Phase 2 nationale de l'ACV élargie aux entrées de ville et quartiers de gare : sur mesure pour Frontignan."]),

    dict(id="port", label="Port de plaisance", type="projet", tier=1, icon="⛵",
         img=I + "node-port.jpg", parent="q-plage",
         sub="≈ 4,5 M€ · 603 → 750 anneaux (2026-2029)",
         txt="Restructuration lancée à l'hiver 2025-2026 : avant-port et promenade Rive Est d'abord, puis bassins, "
             "pontons et espace des petits métiers de la pêche. Le port est excédentaire (607 505 € d'excédent "
             "d'exploitation 2025) : une ressource, pas une charge.",
         facts=[("Budget", "≈ 4,5 M€"), ("Capacité", "603 → 750 anneaux (plafond SCoT 880)"),
                ("Excédent 2025", "607 505 €"), ("Calendrier", "2026-2029")]),

    dict(id="mas-de-chave", label="Mas de Chave", type="projet", tier=1, icon="🏡",
         img=None, parent="q-peyrade",
         sub="≈ 400 logements · calendrier fragilisé",
         txt="Seule zone AU « fermée » du PLU. Programme initial de 336 logements, revu à ≈ 400 puis « ramené à la "
             "baisse » après la reprise de concertation votée le 15 juillet 2026. L'enquête publique annoncée pour "
             "2026 est fragilisée.",
         facts=[("Programme", "≈ 400 logements + parc urbain > 2 ha"), ("Statut", "déclaration de projet / DPMEC"),
                ("Concertation", "reprise le 15 juillet 2026"), ("Maîtrise d'œuvre", "Urban Projects")],
         bul=["Dossier le plus conflictuel du mandat : les riverains de La Peyrade sont organisés.",
              "Interface directe avec l'AOP muscat : la limite ville/vignoble est un sujet de projet, pas de règlement."]),

    dict(id="le-quai", label="Pôle culturel Le Quai", type="projet", tier=1, icon="🎬",
         img=None, parent="q-centre",
         sub="Chais Botta · cinéma 3 salles ouvert en déc. 2025",
         txt="Reconversion des chais Botta en pôle culturel : cinéma de trois salles (2,6 M€ pour l'espace cinéma, "
             "exploité en DSP par un groupement incluant Véo Cinémas), librairie, école de cinéma. Livré avec "
             "≈ 18 mois de retard.",
         facts=[("Ouverture", "décembre 2025"), ("Espace cinéma", "2,6 M€ · 2 108 m²"),
                ("Salle Maison Mathieu", "≈ 150 places, 220 k€ au BP 2025")]),

    dict(id="zae-barnier", label="ZAE du Barnier", type="projet", tier=1, icon="🏬",
         img=None, parent="q-peyrade",
         sub="2,7 M€ · livraison juin 2027",
         txt="Requalification de zone d'activité portée par la SPL Bassin de Thau : le levier d'emplois locaux le "
             "plus rapide du portefeuille de projets.",
         facts=[("Budget", "2,7 M€"), ("Maître d'ouvrage", "SPL Bassin de Thau"), ("Livraison", "juin 2027")]),

    dict(id="lido", label="Lido & trait de côte", type="risque", tier=1, icon="🌊",
         img=None, parent="q-plage",
         sub="Érosion chronique · cartes 30/100 ans à produire",
         txt="Frontignan fait partie des 31 communes maritimes inscrites au décret « recul du trait de côte » "
             "(31 juillet 2023) : elle doit produire des cartes d'exposition à 30 et 100 ans, finançables jusqu'à "
             "80 % par le Fonds vert. Les protections du lido sont explicitement considérées comme temporaires.",
         facts=[("Linéaire", "7 km"), ("Programme de défense", "≈ 13,5 M€ HT (estimation AVP 2012)"),
                ("Cartes réglementaires", "30 et 100 ans, attendues 2026-2027"), ("Fonds vert", "jusqu'à 80 %")]),

    # --- risques ---
    dict(id="submersion", label="Submersion marine", type="risque", tier=1, icon="🌀",
         img=None, parent="frontignan",
         sub="Commune la plus exposée du bassin de Thau",
         txt="Frontignan concentre ≈ 33 % des dommages estimés du bassin à aléa décennal (Q10 : 343,5 M€) et ≈ 26 % "
             "à aléa centennal (Q100 : 970,9 M€). L'A9 devient impraticable dès Q10 et 19 % du linéaire "
             "d'infrastructures est impacté. Le PPRI retient une PHE centennale de 2,00 m.",
         facts=[("Part des dommages Q10", "≈ 33 %"), ("Part des dommages Q100", "≈ 26 %"),
                ("PHE de référence", "2,00 m"), ("Événements", "nov. 2014, oct. 2019")],
         bul=["Le risque est déjà chiffré : le sujet n'est plus la connaissance, mais l'appropriation collective."],
         src=[("SMBT — fiche risques du SCoT", "https://www.smbt.fr/storage/2020/04/3.1.9-ANNEXE-EIE-Fiche-Risques-SCOT-BASIN-DE-THAU-ARRET-15-10-24.pdf", "15/10/2024")],
         data="submersion"),

    dict(id="canicule", label="Chaleur & sécheresse", type="risque", tier=1, icon="🔥",
         img=None, parent="frontignan",
         sub="1,3 → 7,7 jours > 35 °C par an en 2050",
         txt="Les projections TRACC de Météo-France donnent +2,2 °C en 2050 pour l'Occitanie (+2,5 °C en été dans "
             "l'Hérault), une multiplication par ~6 des jours à plus de 35 °C, des nuits tropicales passant de 5 à "
             "24 par an et un risque de feu multiplié par 2,5. Vigilances orange répétées durant l'été 2026.",
         facts=[("2050", "+2,2 °C (Occitanie)"), ("Jours > 35 °C", "1,3 → 7,7 / an"),
                ("Nuits tropicales", "5 → 24 / an"), ("Feux", "× 2,5")],
         src=[("Météo-France — TRACC Occitanie", "https://meteofrance.com/changement-climatique/quel-climat-futur-en-occitanie", "13/05/2026")],
         data="climat"),

    dict(id="seveso", label="Risque industriel", type="risque", tier=1, icon="☣️",
         img=None, parent="q-peyrade",
         sub="2 sites Seveso seuil haut + PPRT",
         txt="GDH (dépôt d'hydrocarbures) et SCORI (traitement de déchets) imposent un plan de prévention des "
             "risques technologiques qui contraint l'urbanisme de La Peyrade — et pèse sur l'image de la ville.",
         facts=[("Sites Seveso seuil haut", "2"), ("Outil", "PPRT")]),

    # ================= TIER 2 — l'agglo de Thau =================
    dict(id="sam", label="Sète Agglopôle Méditerranée", type="territoire", tier=2, icon="🏛️",
         img=F + "figV5_schema_territorial.png", parent="frontignan",
         sub="14 communes · 131 216 hab. · 310 km²",
         txt="Née en 2017 de la fusion de Thau Agglo et de la CCNBT, la 2ᵉ agglomération de l'Hérault a son siège à "
             "Frontignan. Depuis mai 2025, elle est présidée par le Frontignanais Loïc Linares (réélu le "
             "31 mars 2026) : un rééquilibrage historique face à la ville-centre sétoise.",
         facts=[("Communes", "14"), ("Population 2023", "131 216 hab."), ("Superficie", "310 km²"),
                ("Budget 2026", "242 M€ dont 68 M€ d'investissement"), ("Dette fin 2025", "99,7 M€"),
                ("Épargne brute", "18,4 %"), ("Désendettement", "6,3 ans")],
         bul=["Le poids de Frontignan (18,4 % de la population) est doublé par le poids politique (siège + présidence).",
              "13,1 M€ d'investissements 2026 fléchés contre les risques dans la lagune de Thau.",
              "Budget « tagué climat » (méthodologie I4CE) pour la 2ᵉ année."],
         src=[("Sète Agglopôle — budget 2026", "https://www.agglopole.fr/le-budget-2026-de-l-agglopole-a-ete-vote/", "05/03/2026")],
         data="communes"),

    dict(id="thau", label="Lagune de Thau", type="ressource", tier=2, icon="🦪",
         img=I + "node-thau.jpg", parent="sam",
         sub="7 500 ha · ≈ 4 000 emplois conchylicoles",
         txt="La lagune est à la fois le capital naturel, économique et symbolique du bassin. Elle est aussi son "
             "point de fragilité : suspension sanitaire de 28 jours fin décembre 2025 (norovirus après fortes "
             "pluies), mortalités récurrentes, 120 M€ investis en dix ans dans l'assainissement.",
         facts=[("Surface", "7 500 ha"), ("Emplois de filière", "≈ 4 000 sur le bassin"),
                ("Assainissement", "120 M€ en 10 ans"), ("Plan 2026", "+2,1 M€ fonctionnement, +5,3 M€ investissement")],
         bul=["La qualité de l'eau de Thau est l'indicateur vital du territoire à l'horizon 2030-2040.",
              "Le nombre de jours de fermeture sanitaire par an est le meilleur signal faible à suivre."]),

    dict(id="sete", label="Sète", type="commune", tier=2, icon="🐟",
         img=I + "node-sete.jpg", parent="sam",
         sub="45 337 hab. · ville-centre · 26 % de pauvreté",
         txt="Ville-centre du bassin, port de commerce et de pêche, capitale culturelle (MIAM, di Rosa). Elle "
             "concentre 34,6 % de la population de l'agglo et 44,8 % de ses emplois, mais affiche le taux de "
             "pauvreté le plus élevé du bassin (26 %) et le niveau de vie le plus bas (22 740 €).",
         facts=[("Population", "45 337 hab."), ("Emplois", "18 025"), ("Pauvreté", "26 %"),
                ("Niveau de vie médian", "22 740 €"), ("Densité", "1 872,7 hab./km²")],
         bul=["Relation Frontignan-Sète : interdépendance forte (bus express, rail, bassin d'emploi) et rivalité historique atténuée.",
              "Hervé Marquès (Sète) est 1ᵉʳ vice-président de l'agglo : cogestion gauche-droite."],
         data="communes"),

    dict(id="communes-thau", label="Les 12 autres communes", type="commune", tier=2, icon="🗺️",
         img=None, parent="sam",
         sub="De Bouzigues (1 601 hab.) à Mèze (12 669 hab.)",
         txt="Le bassin est très hétérogène : densités de 107 à 1 873 hab./km², niveaux de vie de 22 740 à "
             "29 610 €, taux de résidences secondaires de 1,7 % (Gigean) à 59,7 % (Marseillan). Les villages du "
             "nord (Poussan, Gigean, Montbazin, Villeveyrac) sont des communes de report résidentiel ; les rives de "
             "l'étang (Bouzigues, Loupian, Mèze) vivent de la conchyliculture.",
         facts=[("Communes", "14 au total"), ("Étendue des densités", "107 → 1 873 hab./km²"),
                ("Étendue des niveaux de vie", "22 740 → 29 610 €"),
                ("Croissance la plus forte", "Poussan +2,2 %/an"), ("Seules communes en recul", "Bouzigues, Montbazin")],
         bul=["Deux communes perdent des habitants (Bouzigues −0,6 %/an, Montbazin −0,4 %/an).",
              "La moitié des communes ont un solde naturel négatif : le bassin ne se renouvelle plus par lui-même."],
         data="communes"),

    dict(id="scot", label="SCoT du bassin de Thau", type="politique", tier=2, icon="📐",
         img=None, parent="sam",
         sub="Révision : −54 % d'artificialisation · approbation fin 2026",
         txt="Porté par le SMBT, le SCoT révisé traduit localement le ZAN : accueil ramené à +12 000 / +16 400 "
             "habitants à l'horizon 2043-2045 (contre +40 500 à 2030 dans la version précédente), −54 % "
             "d'artificialisation, ≈ 1 000 logements/an, priorité au renouvellement urbain et aux friches.",
         facts=[("Horizon", "2043-2045"), ("Accueil démographique", "+12 000 à +16 400 hab."),
                ("Artificialisation", "−54 % vs SCoT précédent"), ("Production de logements", "≈ 1 000/an"),
                ("Friches à remobiliser", "≈ 30 ha sur le bassin")],
         src=[("SMBT — révision du SCoT", "https://www.smbt.fr/blog/2026/02/06/revision-du-scot-du-bassin-de-thau/", "06/02/2026")]),

    dict(id="ppa", label="PPA « recomposition spatiale »", type="politique", tier=2, icon="🧭",
         img=None, parent="sam",
         sub="Mai 2024 · 700 k€ d'études · 4 axes",
         txt="Projet partenarial d'aménagement signé en mai 2024 entre l'agglo, l'État (Fonds vert), la Banque des "
             "Territoires, l'EPF Occitanie, la Région et le Département. Quatre axes : cartes du recul du trait de "
             "côte à 30/100 ans, plan-guide du triangle Sète-Balaruc-Frontignan, scénario de recomposition de "
             "Frontignan-Plage, association des habitants.",
         facts=[("Signature", "mai 2024"), ("Budget d'études", "700 k€ HT"),
                ("Partenaires", "État, agglo, Banque des Territoires, EPF, Région, Département"),
                ("Statut", "l'un des premiers PPA « trait de côte » de France")],
         bul=["C'est LE cadre méthodologique et financier de tout projet littoral frontignanais.",
              "Doctrine assumée (avis MRAe 2025) : les protections sont temporaires, le retrait est jugé inéluctable."],
         src=[("Dossier de presse PPA", "https://www.agglopole.fr/storage/2024/06/Dossier-de-Presse-du-Projet-Partenarial-dAmenagement.pdf", "2024")]),

    dict(id="mobilites-agglo", label="Mobilités du bassin", type="projet", tier=2, icon="🚌",
         img=None, parent="sam",
         sub="TCSP RD2 · SAMobilité · ≈ 30 M€ de sections à venir",
         txt="Phase 1 du TCSP RD2 et nouveau réseau bus en service le 5 janvier 2026 (ligne express électrique "
             "Sète-Frontignan). Les sections sur Frontignan, Balaruc-les-Bains et Balaruc-le-Vieux, estimées à "
             "≈ 30 M€, sont attendues entre 2027 et 2030. PDU agglo 2020-2030 : ≈ 154 M€ programmés.",
         facts=[("TCSP phase 1", "en service le 05/01/2026"), ("Requalification RD2", "12 M€"),
                ("Sections à venir", "≈ 30 M€"), ("Bus électriques", "3 + 3 (1,65 M€ en 2026)"),
                ("Réseau", "SAMobilité — Keolis, DSP 2022-2030")]),

    dict(id="centre-aquatique", label="Centre aquatique intercommunal", type="projet", tier=2, icon="🏊‍♀️",
         img=None, parent="sam",
         sub="À Frontignan (Hierles) · marchés lancés en 2026",
         txt="Équipement intercommunal localisé à Frontignan : études en 2025 (100 k€), lancement des marchés au "
             "budget agglo 2026, horizon de mise en service 2028-2030. Coût public non encore publié.",
         facts=[("Localisation", "Frontignan, quartier des Hierles"), ("Études", "100 k€ en 2025"),
                ("Horizon", "2028-2030"), ("Coût", "non publié ❓")]),

    # ================= TIER 3 — les environs =================
    dict(id="herault", label="Hérault", type="territoire", tier=3, icon="🌍",
         img=None, parent="sam",
         sub="1 230 289 hab. · +1,2 %/an · 21 % de pauvreté",
         txt="Département le plus dynamique du littoral occitan (+1,2 %/an), mais aussi l'un des plus pauvres "
             "(21 %). Il atteindrait 1 430 000 habitants en 2050 (+245 000), dont 60 % des gains captés par le "
             "Montpelliérain.",
         facts=[("Population 2023", "1 230 289 hab."), ("Croissance", "+1,2 %/an"),
                ("Pauvreté", "21,0 %"), ("Projection 2050", "1 430 000 hab.")],
         data="echelles"),

    dict(id="montpellier", label="Montpellier Méditerranée Métropole", type="territoire", tier=3, icon="🚊",
         img=I + "node-montpellier.jpg", parent="herault",
         sub="522 542 hab. · +1,7 %/an · à 21 km",
         txt="La métropole voisine croît quatre fois plus vite que la France et capterait 60 % des gains "
             "démographiques du département d'ici 2050. Elle est à la fois le marché d'emploi des navetteurs "
             "frontignanais, la source de pression foncière et le débouché culturel du territoire.",
         facts=[("Population", "522 542 hab."), ("Croissance", "+1,7 %/an"), ("Emplois", "257 597"),
                ("Distance", "21 km · ligne TER la plus fréquentée d'Occitanie")],
         bul=["Le système à deux vitesses est le fait majeur : métropole en croissance, bassin de Thau à +0,05 %/an."],
         data="echelles"),

    dict(id="occitanie", label="Occitanie", type="territoire", tier=3, icon="🌞",
         img=None, parent="herault",
         sub="6 124 653 hab. · +640 000 hab. attendus d'ici 2050",
         txt="Région parmi les plus attractives de France (+0,8 %/an, quasi exclusivement migratoire). D'ici 2050 : "
             "+640 000 habitants, +570 000 ménages, un besoin estimé à 29 000 logements/an et une bascule des "
             "personnes seules en tête des types de ménages dès 2035.",
         facts=[("Population 2023", "6 124 653 hab."), ("Croissance", "+0,8 %/an (dont +0,9 migratoire)"),
                ("Horizon 2050", "+640 000 hab., +570 000 ménages"), ("Besoin de logements", "29 000/an")],
         src=[("INSEE Analyses Occitanie n°115", "https://www.insee.fr/fr/statistiques/8568012", "15/05/2025")],
         data="echelles"),

    dict(id="thau-2050", label="Bassin de Thau 2050", type="futur", tier=3, icon="⏳",
         img=F + "figV3_macro_2050.png", parent="occitanie",
         sub="+0,05 %/an : la plus faible croissance héraultaise",
         txt="Le territoire « Étang de Thau » atteindrait seulement ≈ 127 000 habitants en 2050 selon l'INSEE, soit "
             "une quasi-stagnation. Autrement dit : la croissance frontignanaise récente se fait en captant des "
             "flux, pas en créant de la démographie — une position réversible.",
         facts=[("Croissance projetée", "+0,05 %/an"), ("Population 2050", "≈ 127 000 hab."),
                ("Comparaison", "Hérault +0,8 %/an, Montpelliérain +60 % des gains")],
         src=[("INSEE Analyses — 170 000 ménages de plus dans l'Hérault", "https://www.insee.fr/fr/statistiques/8283176", "14/11/2024")]),

    dict(id="lgv", label="LGV Montpellier-Perpignan", type="projet", tier=3, icon="🚄",
         img=None, parent="occitanie",
         sub="Travaux 2029 · phase 1 en service 2034",
         txt="La ligne nouvelle rebat les cartes ferroviaires du littoral : à partir de 2034, Sète et Frontignan "
             "seront « orphelines de la plupart des TGV », la compensation devant venir des TER (SERM : amplitude "
             "5 h-23 h, jusqu'à un train toutes les 10 minutes aux heures de pointe). Phase 2 : DUP ≈ 2030, service "
             "≈ 2040.",
         facts=[("Appel d'offres phase 1", "≈ 1,5 Md€, fin 2026"), ("Travaux", "2029"),
                ("Mise en service phase 1", "2034"), ("Phase 2", "≈ 2040"),
                ("Compensations LGV pour l'agglo", "10-15 M€")],
         bul=["Ne pas caler le modèle économique local sur la LGV : miser sur le train du quotidien.",
              "Le PEM aura 5 ans d'avance sur la bascule — atout si l'offre TER suit, risque sinon."]),

    dict(id="climat-2050", label="Climat littoral 2050", type="risque", tier=3, icon="🌡️",
         img=None, parent="occitanie",
         sub="+24 cm de mer en 2050 · +2,2 °C",
         txt="Le littoral occitan est sous contrainte croissante mais à vitesse connue : c'est ce qui rend la "
             "planification possible. La mer monte de +24 cm en 2050 et de +62 à +81 cm en 2100, tandis que le PPRI "
             "retient déjà une PHE centennale de 2,00 m.",
         facts=[("Mer 2050", "+24 cm"), ("Mer 2100", "+62 à +81 cm"), ("Été héraultais 2050", "+2,5 °C")],
         data="climat"),

    # ================= TIER 4 — la France =================
    dict(id="france", label="France", type="territoire", tier=4, icon="🇫🇷",
         img=F + "fig1_entonnoir.png", parent="occitanie",
         sub="66,2 M hab. · le cadre des marges de manœuvre",
         txt="Le dernier palier ne sert pas de décor : il fixe les règles (ZAN, trait de côte, loi 3DS), les "
             "guichets (ACV, Fonds vert, DSIL, FCTVA) et la contrainte budgétaire des collectivités. C'est là que "
             "se décide ce qu'une ville de 24 000 habitants peut financer.",
         facts=[("Population métropolitaine", "66 165 815 hab."), ("Croissance", "+0,4 %/an"),
                ("Niveau de vie médian", "25 920 €"), ("Pauvreté", "15,9 %"), ("Chômage 15-64", "11,0 %")],
         data="echelles"),

    dict(id="zan", label="ZAN & loi Climat", type="politique", tier=4, icon="📉",
         img=None, parent="france",
         sub="−50 % d'artificialisation en 2031 · ZAN 2050",
         txt="La loi Climat et résilience du 22 août 2021 impose de réduire de moitié la consommation d'espaces "
             "naturels, agricoles et forestiers entre 2021 et 2031, puis d'atteindre le zéro artificialisation "
             "nette en 2050. Frontignan, qui a déjà « consommé » ses friches, part avec une avance stratégique.",
         facts=[("Loi", "22 août 2021"), ("Décrets", "28 novembre 2023"), ("Palier 2031", "−50 %"), ("Cible", "ZAN 2050")]),

    dict(id="trait-de-cote", label="Dispositif recul du trait de côte", type="politique", tier=4, icon="📏",
         img=None, parent="france",
         sub="Décret du 31 juillet 2023 · Frontignan inscrite",
         txt="Frontignan fait partie des communes maritimes tenues de cartographier leur exposition à 30 et 100 "
             "ans, aux côtés de Sète, Marseillan, Villeneuve-lès-Maguelone ou Mauguio. Ces cartes deviendront un "
             "front d'urbanisme — et un sujet politique majeur pour la station balnéaire.",
         facts=[("Décret-liste", "31 juillet 2023"), ("Horizons", "30 et 100 ans"),
                ("Financement", "Fonds vert jusqu'à 80 %")]),

    dict(id="acv", label="Action cœur de Ville", type="politique", tier=4, icon="🎯",
         img=None, parent="france",
         sub="Label obtenu en mars 2025 · prolongé fin 2025",
         txt="Programme national de revitalisation : ingénierie ANCT, accès facilité aux financements, phase 2 "
             "élargie aux entrées de ville et quartiers de gare. Frontignan est la 5ᵉ ville héraultaise labellisée ; "
             "plus de 200 M€ ont déjà été mobilisés par l'ACV dans le département.",
         facts=[("Label", "mars 2025, convention juin 2025"), ("Phase 2", "entrées de ville & quartiers de gare"),
                ("Effet levier dans l'Hérault", "> 200 M€")]),

    dict(id="finances-nat", label="Contraction des financements", type="politique", tier=4, icon="📉",
         img=None, parent="france",
         sub="Fonds vert 2,5 Md€ → 834 M€ · FCTVA −2 pts",
         txt="L'ère de la rareté maîtrisée : le Fonds vert passe de 2,5 Md€ (2024) à 1,15 Md€ (2025) puis 834 M€ "
             "(2026), le taux de FCTVA baisse de 16,4 % à 14,85 %, les taux d'intérêt montent (+27,6 % de charge "
             "d'intérêts pour l'agglo en 2025). Les financements existent mais se gagnent dossier par dossier.",
         facts=[("Fonds vert 2026", "834 M€ (−67 % en 2 ans)"), ("FCTVA", "16,4 % → 14,85 %"),
                ("Intérêts agglo 2025", "+27,6 %")]),

    # ================= FUTUR =================
    dict(id="focus-2030", label="Focus 2030", type="futur", tier=1, icon="🎯",
         img=F + "figV2_focus_2030.png", parent="frontignan",
         sub="5 conditions de succès mesurables",
         txt="2030 est la première date où le mandat 2026-2032 sera jugé sur pièces : PEM livré et desservi, "
             "programmation de la friche validée et financée, +300 à +600 emplois locaux, qualité de l'eau de Thau "
             "en amélioration, trajectoire démographique tenue sans gentrification du centre.",
         facts=[("Population 2030", "≈ 25 000 hab. (estimation)"), ("Emplois visés", "+300 à +600"),
                ("Jalons visibles", "PEM, centre aquatique, port, premiers usages de la friche")],
         data="conditions"),

    dict(id="scenarios-2040", label="Trois scénarios 2040", type="futur", tier=1, icon="🔮",
         img=F + "figV4_scenarios_2040.png", parent="frontignan",
         sub="Thau tranquille · Couronne métropolitaine · Pôle de la transition",
         txt="S1 « Thau tranquille » : stagnation, friche sous-aménagée, ville-dortoir vieillissante. "
             "S2 « Couronne métropolitaine » : débordement montpelliérain, spéculation, gentrification. "
             "S3 « Pôle de la transition » ★ : friche + PEM + identité produisent +500 à +1 000 emplois. "
             "Les probabilités affichées sont une lecture d'analyste, pas une prévision.",
         facts=[("S1", "24-25 000 hab., 65+ > 30 %"), ("S2", "> 27 000 hab., 25-30 % de résidences secondaires"),
                ("S3 ★", "≈ 26 000 hab., +500 à +1 000 emplois")],
         data="scenarios"),

    dict(id="trajectoire", label="Trajectoire 2026-2040", type="futur", tier=1, icon="🛤️",
         img=F + "figV1_trajectoire_2026_2040.png", parent="frontignan",
         sub="2030 la ville rééquipée · 2034 la bascule ferroviaire · 2040 le littoral recomposé",
         txt="Trois blocs : 2026-2030 « tout se joue maintenant » (friche, PEM, port, centre aquatique, SCoT/PLU), "
             "2030-2034 « le temps des preuves » (municipales 2032, LGV 2034), 2034-2040 « la maturité » "
             "(recomposition de la plage, désaisonnalisation, services au vieillissement).",
         data="jalons"),

    # ================= SYNTHÈSES =================
    dict(id="swot", label="SWOT", type="data", tier=1, icon="⚖️",
         img=F + "fig6_swot.png", parent="frontignan",
         sub="9 forces · 9 faiblesses · 9 opportunités · 8 menaces",
         txt="Forces : muscat, littoral, position bipolaire, poids intercommunal, finances maîtrisées, 11 ha "
             "dépollués, faible vacance commerciale, culture, équipe réélue. Faiblesses : chômage et pauvreté, "
             "vieillissement, dépendance automobile, risques majeurs, pression fiscale, offre hôtelière, image "
             "industrielle, fracture civique, offre de soins.",
         data="swot"),

    dict(id="acteurs", label="Cartographie des acteurs", type="acteur", tier=1, icon="🕸️",
         img=F + "fig8_parties_prenantes.png", parent="frontignan",
         sub="28 acteurs positionnés en influence × intérêt",
         txt="Trois familles : institutionnels (co-construction obligatoire), acteurs économiques (alliances "
             "gagnant-gagnant) et société civile (écoute et preuve). Le point singulier de Frontignan est la "
             "superposition ville/agglo : les mêmes personnes décident aux deux échelles.",
         bul=["Dynamiques à surveiller : couple ville/agglo, relation Sète-Frontignan, clivage centre / Peyrade / plage, fatigue démocratique.",
              "Les scores d'influence et d'intérêt sont une estimation d'analyste (fiabilité C), à valider en entretien."],
         data="acteurs"),

    dict(id="recos", label="Recommandations design", type="data", tier=1, icon="✅",
         img=F + "fig7_priorisation.png", parent="frontignan",
         sub="10 recommandations priorisées impact × faisabilité",
         txt="R1 plateforme d'identité et signalétique · R2 concertation outillée friche & Mas de Chave · R3 design "
             "du pôle gare · R4 « bien vivre les chantiers » · R5 stratégie muscat 90→100 ans · R6 design du risque · "
             "R7 revitalisation commerciale · R8 écoconception des espaces publics · R9 montée en gamme de la plage · "
             "R10 observatoire du territoire.",
         data="recos"),
]

# --------------------------------------------------------------------------
# Liens du graphe : (source, cible, type, poids, libellé)
# types : gouverne · finance · dessert · coopere · tension · depend · expose · produit · compose
# --------------------------------------------------------------------------
LINKS = [
    # cœur → thématiques
    ("frontignan", "identite", "compose", 3, "capital symbolique"),
    ("frontignan", "demographie", "compose", 3, ""),
    ("demographie", "ages", "compose", 2, ""),
    ("frontignan", "revenus", "compose", 3, ""),
    ("frontignan", "emploi", "compose", 3, ""),
    ("frontignan", "economie", "compose", 3, ""),
    ("frontignan", "budget", "compose", 3, ""),
    ("frontignan", "gouvernance", "compose", 3, ""),
    ("gouvernance", "participation", "compose", 2, ""),
    ("frontignan", "q-centre", "compose", 3, ""),
    ("frontignan", "q-peyrade", "compose", 3, ""),
    ("frontignan", "q-plage", "compose", 3, ""),
    ("frontignan", "q-hierles", "compose", 2, ""),
    ("frontignan", "q-qpv", "compose", 2, ""),
    ("frontignan", "swot", "compose", 2, ""),
    ("frontignan", "acteurs", "compose", 3, ""),
    ("frontignan", "recos", "compose", 2, ""),
    ("frontignan", "focus-2030", "compose", 3, ""),
    ("frontignan", "scenarios-2040", "compose", 3, ""),
    ("frontignan", "trajectoire", "compose", 2, ""),
    # projets
    ("q-peyrade", "friche-mobil", "compose", 3, "11 ha en cœur de ville"),
    ("friche-mobil", "pem-gare", "depend", 4, "le PEM s'implante sur la friche"),
    ("q-centre", "oru", "compose", 3, ""),
    ("q-plage", "port", "compose", 3, ""),
    ("q-plage", "lido", "expose", 3, ""),
    ("q-peyrade", "mas-de-chave", "compose", 3, ""),
    ("q-centre", "le-quai", "compose", 2, ""),
    ("q-peyrade", "zae-barnier", "compose", 2, ""),
    ("q-hierles", "centre-aquatique", "compose", 3, ""),
    ("oru", "acv", "finance", 3, "label et ingénierie ANCT"),
    ("friche-mobil", "zan", "depend", 2, "friche = foncier ZAN-compatible"),
    ("friche-mobil", "emploi", "produit", 3, "emplois non délocalisables visés"),
    ("pem-gare", "emploi", "produit", 2, "accès au bassin d'emploi"),
    ("pem-gare", "a-region", "finance", 4, "≤ 10 M€ (40 %)"),
    ("pem-gare", "a-sncf", "depend", 3, "emprise et calendrier ferroviaires"),
    ("pem-gare", "lgv", "depend", 3, "bascule TER 2034"),
    ("pem-gare", "mobilites-agglo", "coopere", 3, "intermodalité TCSP/TER"),
    ("centre-aquatique", "sam", "finance", 3, "maîtrise d'ouvrage agglo"),
    ("mas-de-chave", "a-riverains", "tension", 4, "concertation reprise en 2026"),
    ("mas-de-chave", "identite", "tension", 2, "limite ville / AOP muscat"),
    ("zae-barnier", "economie", "produit", 2, ""),
    ("le-quai", "identite", "produit", 2, ""),
    # risques
    ("frontignan", "submersion", "expose", 4, "1ʳᵉ commune exposée du bassin"),
    ("frontignan", "canicule", "expose", 3, ""),
    ("q-peyrade", "seveso", "expose", 3, ""),
    ("submersion", "ppa", "depend", 3, "cadre de recomposition"),
    ("lido", "trait-de-cote", "depend", 3, "cartes 30/100 ans"),
    ("canicule", "climat-2050", "depend", 3, ""),
    ("submersion", "q-plage", "expose", 3, ""),
    ("thau", "submersion", "depend", 2, ""),
    # agglo
    ("frontignan", "sam", "gouverne", 5, "siège + présidence + VP tourisme"),
    ("sam", "sete", "compose", 4, ""),
    ("sam", "communes-thau", "compose", 4, ""),
    ("sam", "thau", "compose", 3, ""),
    ("sam", "scot", "gouverne", 3, "via le SMBT"),
    ("sam", "ppa", "gouverne", 3, ""),
    ("sam", "mobilites-agglo", "gouverne", 4, ""),
    ("sam", "centre-aquatique", "gouverne", 3, ""),
    ("sete", "frontignan", "tension", 3, "interdépendance et rivalité"),
    ("sete", "emploi", "depend", 3, "bassin d'emploi partagé"),
    ("communes-thau", "thau", "depend", 3, "conchyliculture"),
    ("thau", "a-conchyliculteurs", "produit", 3, ""),
    ("scot", "zan", "depend", 3, "−54 % d'artificialisation"),
    ("scot", "mas-de-chave", "gouverne", 2, ""),
    ("scot", "port", "gouverne", 2, "plafond de 880 anneaux"),
    ("mobilites-agglo", "sete", "dessert", 3, "ligne express RD2"),
    ("mobilites-agglo", "frontignan", "dessert", 3, ""),
    # environs
    ("sam", "herault", "compose", 3, ""),
    ("herault", "montpellier", "compose", 3, ""),
    ("herault", "occitanie", "compose", 3, ""),
    ("montpellier", "frontignan", "depend", 4, "pression résidentielle & emploi"),
    ("montpellier", "emploi", "depend", 3, "navetteurs"),
    ("occitanie", "thau-2050", "produit", 2, ""),
    ("thau-2050", "sam", "depend", 3, "+0,05 %/an"),
    ("occitanie", "lgv", "gouverne", 3, ""),
    ("occitanie", "climat-2050", "expose", 3, ""),
    ("occitanie", "a-region", "gouverne", 3, ""),
    # france
    ("occitanie", "france", "compose", 3, ""),
    ("france", "zan", "gouverne", 3, ""),
    ("france", "trait-de-cote", "gouverne", 3, ""),
    ("france", "acv", "finance", 3, ""),
    ("france", "finances-nat", "gouverne", 3, ""),
    ("finances-nat", "budget", "depend", 3, "FCTVA, dotations"),
    ("trait-de-cote", "ppa", "finance", 3, "Fonds vert 80 %"),
    ("zan", "scot", "gouverne", 3, ""),
    ("acv", "q-centre", "finance", 3, ""),
    ("finances-nat", "sam", "depend", 2, ""),
    # futur
    ("focus-2030", "pem-gare", "depend", 3, "condition n°1"),
    ("focus-2030", "friche-mobil", "depend", 3, "condition n°2"),
    ("focus-2030", "emploi", "depend", 3, "condition n°3"),
    ("focus-2030", "thau", "depend", 3, "condition n°4"),
    ("focus-2030", "demographie", "depend", 3, "condition n°5"),
    ("scenarios-2040", "focus-2030", "depend", 3, ""),
    ("trajectoire", "focus-2030", "depend", 2, ""),
    ("scenarios-2040", "montpellier", "depend", 2, "S2 couronne métropolitaine"),
    ("scenarios-2040", "friche-mobil", "depend", 3, "S3 pôle de la transition"),
    # acteurs ↔ objets
    ("acteurs", "gouvernance", "compose", 2, ""),
    ("acteurs", "participation", "compose", 2, ""),
    ("recos", "acteurs", "depend", 2, ""),
    ("swot", "recos", "produit", 2, ""),
    ("identite", "a-cave", "produit", 3, ""),
    ("economie", "a-hexis", "compose", 2, ""),
    ("economie", "a-commercants", "compose", 2, ""),
    ("q-centre", "a-commercants", "tension", 3, "fatigue des chantiers"),
]

# Acteurs → nœuds du graphe (générés automatiquement depuis ACTEURS)
ACTEUR_LINKS = {
    "a-arrouy": [("gouvernance", "gouverne", 5), ("friche-mobil", "gouverne", 4), ("frontignan", "gouverne", 5)],
    "a-linares": [("sam", "gouverne", 5), ("frontignan", "coopere", 4), ("pem-gare", "coopere", 3), ("scot", "coopere", 3)],
    "a-adjoints": [("gouvernance", "compose", 4), ("participation", "gouverne", 3), ("q-centre", "gouverne", 2)],
    "a-services": [("budget", "gouverne", 3), ("oru", "gouverne", 3)],
    "a-opposition": [("gouvernance", "tension", 3), ("participation", "tension", 2)],
    "a-etat": [("zan", "gouverne", 4), ("trait-de-cote", "gouverne", 4), ("acv", "finance", 3), ("seveso", "gouverne", 3)],
    "a-region": [("pem-gare", "finance", 5), ("lgv", "gouverne", 4), ("port", "finance", 2)],
    "a-departement": [("mobilites-agglo", "coopere", 2), ("q-centre", "finance", 2)],
    "a-smbt": [("scot", "gouverne", 4), ("thau", "gouverne", 3), ("submersion", "gouverne", 3)],
    "a-anct": [("acv", "finance", 3), ("oru", "coopere", 2)],
    "a-sncf": [("pem-gare", "gouverne", 4)],
    "a-bdt": [("ppa", "finance", 3), ("friche-mobil", "coopere", 2)],
    "a-cave": [("identite", "produit", 3), ("economie", "compose", 2)],
    "a-vignerons": [("identite", "produit", 2), ("mas-de-chave", "tension", 2)],
    "a-hexis": [("economie", "compose", 3), ("friche-mobil", "coopere", 2)],
    "a-seveso": [("seveso", "compose", 3), ("q-peyrade", "tension", 2)],
    "a-conchyliculteurs": [("thau", "depend", 4), ("sam", "tension", 3)],
    "a-commercants": [("q-centre", "depend", 4), ("oru", "tension", 3)],
    "a-tourisme": [("identite", "coopere", 3), ("q-plage", "coopere", 3)],
    "a-promoteurs": [("mas-de-chave", "produit", 3), ("q-plage", "tension", 2)],
    "a-comites": [("participation", "compose", 4), ("friche-mobil", "coopere", 2)],
    "a-assos": [("identite", "produit", 3), ("participation", "coopere", 2)],
    "a-qpv": [("q-qpv", "compose", 3), ("participation", "depend", 3)],
    "a-seniors": [("demographie", "compose", 3), ("canicule", "expose", 3)],
    "a-jeunes": [("emploi", "depend", 3), ("participation", "depend", 2)],
    "a-navetteurs": [("pem-gare", "depend", 4), ("montpellier", "depend", 3)],
    "a-riverains": [("mas-de-chave", "tension", 4), ("q-peyrade", "compose", 3)],
    "a-presse": [("gouvernance", "coopere", 2), ("participation", "coopere", 2)],
}

# --------------------------------------------------------------------------
# Scénario de présentation (mode « slides »)
# --------------------------------------------------------------------------
SLIDES = [
    dict(id="intro", kind="cover", title="Frontignan la Peyrade",
         subtitle="Atlas interactif — acteurs, données, futurs (2026 → 2040)",
         node="frontignan",
         text="Trois lectures d'un même corpus : un graphe de connaissance façon Obsidian, une carte heuristique "
              "et un déroulé de présentation. 100 nœuds, 130 liens, 14 communes documentées, 28 acteurs positionnés."),
    dict(id="entonnoir", kind="funnel", title="L'entonnoir : de la France au quartier",
         text="Chaque palier fixe les règles du palier suivant. La France donne le cadre et les guichets, "
              "l'Occitanie et l'Hérault la démographie et le rail, l'agglo de Thau les compétences opérationnelles, "
              "Frontignan les usages.", data="echelles"),
    dict(id="portrait", kind="node", title="Portrait chiffré", node="frontignan", data="communes",
         text="Frontignan est la commune médiane du bassin : ni la richesse de Balaruc-le-Vieux, ni la pauvreté de "
              "Sète. C'est cette position centrale qui en fait un bon laboratoire de politiques publiques."),
    dict(id="communes", kind="stats", title="14 communes, un territoire très inégal", data="communes",
         text="Densité, niveau de vie, résidences secondaires, chômage : la dispersion intercommunale est forte. "
              "Les statistiques de distribution (médiane, écart-type, quartiles, étendue) disent mieux le "
              "territoire que les moyennes."),
    dict(id="demo", kind="node", title="Démographie : croissance retrouvée, vieillissement réel",
         node="demographie", data="pop_serie",
         text="+6,0 % depuis 2017, mais 25,3 % de 65 ans et plus et un solde naturel négatif."),
    dict(id="mobil", kind="node", title="Mobilités : la voiture, encore reine", node="emploi", data="mobilites",
         text="80 % des actifs en voiture, 67 % travaillant hors de la commune : le PEM est le seul projet "
              "capable de déplacer cette courbe."),
    dict(id="risque", kind="node", title="Le risque comme donnée de projet", node="submersion", data="submersion",
         text="Frontignan concentre un tiers des dommages de submersion du bassin à aléa décennal."),
    dict(id="acteurs", kind="stakeholders", title="Qui décide, qui subit, qui peut bloquer", data="acteurs",
         text="28 acteurs positionnés en influence × intérêt. Quatre quadrants, quatre postures : co-construire, "
              "tenir informés, écouter activement, surveiller."),
    dict(id="projets", kind="projects", title="Le portefeuille de projets", data="projets",
         text="13 projets datés et chiffrés, de la friche Mobil (11 ha) au groupe scolaire. Ensemble : plus de "
              "110 M€ d'investissements identifiés sur 2022-2035."),
    dict(id="futur", kind="scenarios", title="Trois futurs à 2040", data="scenarios",
         text="S1 stagnation, S2 couronne métropolitaine, S3 pôle de la transition. Les cinq conditions de succès "
              "à 2030 déterminent le basculement."),
    dict(id="reco", kind="recos", title="Ce que le design peut faire", data="recos",
         text="Dix recommandations priorisées par impact et faisabilité, séquencées de 2027 à 2030."),
]
