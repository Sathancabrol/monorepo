"""Fiches détaillées des biais cognitifs avec applications réelles et simulations."""

BIAS_CARDS = {
    "b_confirmation": {
        "id": "b_confirmation",
        "title": "Biais de confirmation",
        "subtitle": "La tendance à chercher ce qui nous conforte",
        "definition_complete": "Le biais de confirmation est la tendance systématique à rechercher, interpréter, favoriser et rappeler les informations qui confirment nos croyances, hypothèses ou valeurs préexistantes, tout en ignorant, minimisant ou discréditant les preuves qui les contredisent.",
        "history": "Identifié par Peter Wason (1960) via sa tâche de sélection de cartes. Les participants devinent une règle (ex: nombres pairs) et testent uniquement des exemples confirmants plutôt que des contre-exemples. Karl Popper avait théorisé la falsification comme principe scientifique, mais Wason a montré que l'esprit humain préfère naturellement la confirmation.",
        "mechanisms": [
            "Recherche sélective d'information : on consulte des sources qui partagent nos opinions",
            "Interprétation biaisée : une même preuve est lue comme confirmante par les deux camps",
            "Mémoire sélective : on se souvient mieux des informations confirmantes",
            "Test positif : on teste nos hypothèses en cherchant des confirmations plutôt que des réfutations",
            "Effet de polarisation : l'exposition à des preuves mixtes renforce les positions initiales"
        ],
        "key_experiments": [
            {"name": "Wason Selection Task (1960)", "desc": "Les participants doivent deviner une règle. Ils testent uniquement des cas confirmants. < 10% trouvent la règle par falsification."},
            {"name": "Lord, Ross & Lepper (1979)", "desc": "Des partisans et opposants à la peine de mort lisent les mêmes études mixtes. Chaque camp trouve les études confirmant sa position plus convaincantes → polarisation."},
            {"name": "Nickerson (1998)", "desc": "Revue complète montrant que le biais de confirmation est 'peut-être le plus problématique des biais cognitifs' dans le raisonnement humain."}
        ],
        "real_world_applications": [
            {"domain": "Réseaux sociaux", "desc": "Les algorithmes créent des 'chambres d'écho' en montrant du contenu aligné avec nos préférences. On ne voit que ce qui confirme nos opinions.", "impact": "Polarisation politique, radicalisation, fake news"},
            {"domain": "Médecine", "desc": "Un médecin forme un diagnostic initial puis cherche des symptômes confirmants, négligeant les diagnostics alternatifs.", "impact": "Erreurs de diagnostic, sur-traitement"},
            {"domain": "Recrutement", "desc": "Un recruteur forme une impression en 30 secondes puis pose des questions qui confirment son jugement initial.", "impact": "Discrimination, perte de talents"},
            {"domain": "Recherche scientifique", "desc": "Publier uniquement les résultats significatifs (confirmation) et archiver les résultats nuls (file drawer problem).", "impact": "Crise de la reproductibilité"},
            {"domain": "Vie quotidienne", "desc": "Après avoir acheté une voiture, on remarque surtout les avis positifs sur ce modèle.", "impact": "Rationalisation post-achat, surconfiance"}
        ],
        "debiasing_strategies": [
            "Rechercher activement des preuves contraires (avocat du diable)",
            "Pré-enregistrer les hypothèses avant de collecter les données",
            "Considérer 'et si j'avais tort ?' comme question par défaut",
            "Diversifier les sources d'information",
            "Utiliser des checklists structurées pour les décisions importantes"
        ],
        "simulation": "confirmation",
        "illustration": "/static/illustrations/bias_confirmation.jpg",
        "real_world_image": "/static/illustrations/real_confirmation.jpg",
        "schema_image": "/static/illustrations/schema_confirmation.jpg",
        "related_biases": ["b_ancrage", "b_surconfiance", "b_halo"],
        "key_articles": ["wason_1960", "lord_ross_lepper_1979"]
    },
    "b_ancrage": {
        "id": "b_ancrage",
        "title": "Biais d'ancrage",
        "subtitle": "Le premier chiffre influence tous les suivants",
        "definition_complete": "Le biais d'ancrage est la tendance à s'appuyer trop fortement sur la première information numérique reçue (l'ancre) pour prendre des décisions ou faire des estimations ultérieures, même lorsque cette ancre est arbitraire ou non pertinente.",
        "history": "Découvert par Tversky et Kahneman (1974). Dans leur expérience, une roue de fortune truquée affichait 10 ou 65, puis les participants estimaient le % de pays africains à l'ONU. L'ancre haute (65) produisait des estimations ~45%, l'ancre basse (10) ~25%. Effet robuste même quand l'ancre est explicitement aléatoire.",
        "mechanisms": [
            "Ajustement insuffisant : on part de l'ancre et on ajuste, mais pas assez",
            "Amorçage sélectif : l'ancre active des informations compatibles en mémoire",
            "Accès sélectif : l'ancre rend les informations confirmantes plus accessibles",
            "Deux processus : ancrage rapide (système 1) + ajustement lent (système 2)"
        ],
        "key_experiments": [
            {"name": "Tversky & Kahneman (1974)", "desc": "Roue de fortune → estimation % pays africains ONU. Ancre 10 → estimation 25%. Ancre 65 → estimation 45%."},
            {"name": "Strack & Mussweiler (1997)", "desc": "L'âge de Gandhi à sa mort : ancre haute (140 ans) → estimation ~67 ans. Ancre basse (9 ans) → estimation ~50 ans."},
            {"name": "Fritz (1996) — Immobilier", "desc": "Des agents immobiliers évaluent une maison. Le prix affiché (ancre) influence significativement leur évaluation, même s'ils nient l'effet."}
        ],
        "real_world_applications": [
            {"domain": "Négociation salariale", "desc": "Le premier chiffre proposé sert d'ancre. Celui qui annonce en premier fixe le cadre de la négociation.", "impact": "Écarts de salaire significatifs"},
            {"domain": "Prix et promotions", "desc": "'Prix barré' = ancre haute. Le prix réel paraît avantageux par comparaison. 'Était 199€, maintenant 99€'.", "impact": "Augmentation des ventes de 30-50%"},
            {"domain": "Justice", "desc": "La peine demandée par le procureur (ancre haute) influence la sentence du juge, même chez les juges expérimentés.", "impact": "Sentences plus sévères avec demandes élevées"},
            {"domain": "Estimations médicales", "desc": "Un premier test avec un résultat anormal sert d'ancre pour les diagnostics suivants, même si des tests ultérieurs sont normaux.", "impact": "Sur-diagnostic, examens inutiles"},
            {"domain": "Évaluation immobilière", "desc": "Le prix affiché influence l'évaluation des acheteurs ET des experts immobiliers.", "impact": "Sur-évaluation ou sous-évaluation systématique"}
        ],
        "debiasing_strategies": [
            "Générer ses propres estimations AVANT de voir l'ancre",
            "Considérer plusieurs ancres alternatives",
            "Utiliser des données objectives et des statistiques de base",
            "Prendre du temps avant de décider (l'ajustement nécessite du temps)",
            "En négociation : préparer son chiffre avant l'autre partie"
        ],
        "simulation": "anchoring",
        "illustration": "/static/illustrations/bias_anchoring.jpg",
        "real_world_image": "/static/illustrations/real_anchoring.jpg",
        "schema_image": "/static/illustrations/schema_anchoring.jpg",
        "related_biases": ["b_confirmation", "b_disponibilite", "b_framing"],
        "key_articles": ["tversky_kahneman_1974"]
    },
    "b_disponibilite": {
        "id": "b_disponibilite",
        "title": "Biais de disponibilité",
        "subtitle": "Ce qui vient facilement à l'esprit semble plus fréquent",
        "definition_complete": "Le biais de disponibilité est la tendance à estimer la probabilité ou la fréquence d'un événement en fonction de la facilité avec laquelle des exemples viennent à l'esprit, plutôt que sur des données statistiques objectives.",
        "history": "Identifié par Tversky et Kahneman (1973). Ils ont montré que les gens jugent les mots commençant par 'K' plus fréquents que ceux ayant 'K' en 3e position, car les premiers sont plus faciles à générer (bien que les seconds soient en réalité plus nombreux en anglais).",
        "mechanisms": [
            "Facilité de récupération : les événements récents, émotionnels ou médiatisés sont plus accessibles en mémoire",
            "Heuristique de disponibilité : on utilise la facilité de rappel comme proxy de fréquence",
            "Amplification médiatique : la couverture médiatique rend certains événements plus 'disponibles'",
            "Vivacité émotionnelle : les événements dramatiques laissent des traces mnésiques plus fortes"
        ],
        "key_experiments": [
            {"name": "Tversky & Kahneman (1973)", "desc": "Les participants jugent les mots commençant par K plus fréquents que ceux avec K en 3e position, alors que c'est l'inverse."},
            {"name": "Slovic, Fischhoff & Lichtenstein (1982)", "desc": "Les gens surestiment les causes de décès spectaculaires (avion, homicide) et sous-estiment les causes communes (diabète, AVC)."},
            {"name": "Schwarz et al. (1991)", "desc": "Demander 6 vs 12 exemples d'affirmation de soi. Ceux qui donnent 6 exemples (facile) se jugent plus assertifs que ceux qui en donnent 12 (difficile)."}
        ],
        "real_world_applications": [
            {"domain": "Peur de l'avion", "desc": "Les crashs aériens sont très médiatisés → surestimation du risque. En réalité, l'avion est 100x plus sûr que la voiture par km.", "impact": "Anxiété, choix de transport sous-optimaux"},
            {"domain": "Assurance", "desc": "Les souscriptions augmentent après une catastrophe naturelle (disponibilité) puis diminuent avec le temps.", "impact": "Sous-assurance chronique"},
            {"domain": "Évaluation de performance", "desc": "Un manager évalue un employé en se souvenant surtout des événements récents (biais de récence = sous-type de disponibilité).", "impact": "Évaluations injustes"},
            {"domain": "Médias et criminalité", "desc": "La couverture intensive de faits divers crée l'impression d'une augmentation de la criminalité, même quand les statistiques baissent.", "impact": "Peur disproportionnée, politiques sécuritaires"},
            {"domain": "Diagnostic médical", "desc": "Après avoir vu un cas rare, un médecin surestime sa prévalence chez les patients suivants.", "impact": "Sur-diagnostic, examens inutiles"}
        ],
        "debiasing_strategies": [
            "Consulter les statistiques officielles avant de juger",
            "Distinguer fréquence médiatique et fréquence réelle",
            "Chercher activement des contre-exemples",
            "Utiliser des taux de base (base rates) dans les estimations",
            "Attendre que l'émotion retombe avant de décider"
        ],
        "simulation": "availability",
        "illustration": "/static/illustrations/bias_availability.jpg",
        "real_world_image": "/static/illustrations/real_availability.jpg",
        "schema_image": "/static/illustrations/schema_availability.jpg",
        "related_biases": ["b_negativite", "b_recence_primacy", "b_confirmation"],
        "key_articles": []
    },
    "b_dunning_kruger": {
        "id": "b_dunning_kruger",
        "title": "Effet Dunning-Kruger",
        "subtitle": "Les incompétents ne savent pas qu'ils sont incompétents",
        "definition_complete": "L'effet Dunning-Kruger décrit la tendance des personnes les moins compétentes dans un domaine à surestimer significativement leurs capacités, tandis que les personnes les plus compétentes les sous-estiment légèrement. Le 'double fardeau' : l'incompétence empêche de reconnaître sa propre incompétence.",
        "history": "Kruger et Dunning (1999) ont testé des participants sur la logique, la grammaire et l'humour. Le quartile inférieur (score réel ~12e percentile) estimait être au ~62e percentile. Le quartile supérieur sous-estimait légèrement. Prix Ig Nobel 2000, puis confirmation robuste dans de nombreuses études.",
        "mechanisms": [
            "Métacognition défaillante : les compétences nécessaires pour bien performer sont les mêmes que celles nécessaires pour évaluer la performance",
            "Double fardeau : l'incompétence produit à la fois de mauvaises performances ET l'incapacité de le reconnaître",
            "Illusion de supériorité : tendance générale à se juger au-dessus de la moyenne",
            "Effet inverse chez les experts : ils surestiment la facilité pour les autres (malédiction du savoir)"
        ],
        "key_experiments": [
            {"name": "Kruger & Dunning (1999)", "desc": "Tests de logique, grammaire, humour. Q1 estime être au 62e percentile, est au 12e. Q4 estime 74e, est au 86e."},
            {"name": "Ehrlinger et al. (2008)", "desc": "Après formation métacognitive, les incompétents améliorent leur calibration. Preuve que le problème est métacognitif."},
            {"name": "Schlösser et al. (2018)", "desc": "Réplication bayésienne confirmant l'effet. Plus marqué dans les tâches faciles que difficiles."}
        ],
        "real_world_applications": [
            {"domain": "Réseaux sociaux", "desc": "Les amateurs publient avec confiance sur des sujets complexes, tandis que les experts hésitent et nuancent.", "impact": "Désinformation, autorité non méritée"},
            {"domain": "Entreprise", "desc": "Les employés les moins compétents demandent des promotions avec le plus d'assurance. Les plus compétents doutent.", "impact": "Promotions inappropriées, syndrome de l'imposteur"},
            {"domain": "Médecine", "desc": "Les médecins juniors surestiment leurs diagnostics. Les seniors sont plus prudents et demandent des avis.", "impact": "Erreurs médicales chez les moins expérimentés"},
            {"domain": "Éducation", "desc": "Les étudiants en difficulté surestiment leur préparation aux examens et étudient moins.", "impact": "Échec aux examens, abandon"},
            {"domain": "Conduite automobile", "desc": "80% des conducteurs se jugent au-dessus de la moyenne (impossible statistiquement).", "impact": "Prise de risque, accidents"}
        ],
        "debiasing_strategies": [
            "Formation continue : plus on apprend, plus on réalise ce qu'on ignore",
            "Feedback externe régulier et objectif",
            "Comparer ses performances à des références objectives (pas à soi-même)",
            "Humilité épistémique : 'Plus je sais, plus je sais que je ne sais pas' (Socrate)",
            "Évaluation par les pairs et mentorat"
        ],
        "simulation": "dk",
        "illustration": "/static/illustrations/bias_dunning_kruger.jpg",
        "real_world_image": "/static/illustrations/real_dunning_kruger.jpg",
        "schema_image": "/static/illustrations/schema_dunning_kruger.jpg",
        "related_biases": ["b_surconfiance", "b_auto_complaisance", "b_illusion_validite"],
        "key_articles": ["kruger_dunning_1999"]
    },
    "b_halo": {
        "id": "b_halo",
        "title": "Effet de halo",
        "subtitle": "Une qualité en éclaire d'autres",
        "definition_complete": "L'effet de halo est un biais cognitif par lequel la perception d'une caractéristique positive chez une personne (beauté physique, charisme, prestige) influence positivement le jugement de ses autres caractéristiques (compétence, intelligence, honnêteté, sympathie), créant un 'halo' généralisé.",
        "history": "Découvert par Edward Thorndike (1920) qui demandait à des officiers d'évaluer leurs soldats sur plusieurs dimensions. Les évaluations étaient fortement corrélées : un soldat jugé physiquement impressionnant était aussi jugé plus intelligent, meilleur leader, etc. Nisbett et Wilson (1977) ont montré que l'effet opère sans conscience.",
        "mechanisms": [
            "Généralisation automatique : une impression positive sur un trait 'déborde' sur les autres",
            "Cohérence cognitive : l'esprit cherche la cohérence entre les jugements",
            "Stéréotype de beauté : 'ce qui est beau est bien' (what is beautiful is good)",
            "Traitement superficiel : le halo réduit l'effort d'évaluation dimension par dimension"
        ],
        "key_experiments": [
            {"name": "Thorndike (1920)", "desc": "Les officiers corrèlent fortement toutes les dimensions d'évaluation de leurs soldats, même quand elles devraient être indépendantes."},
            {"name": "Landy & Sigall (1974)", "desc": "Un essai identique est jugé meilleur quand la photo de l'auteur est attractive vs non-attractive."},
            {"name": "Nisbett & Wilson (1977)", "desc": "Un enseignant chaleureux est jugé plus attractif physiquement qu'un enseillant froid, malgré le même visage."}
        ],
        "real_world_applications": [
            {"domain": "Recrutement", "desc": "Les candidats attractifs sont jugés plus compétents à CV égal. Prime de beauté : +10-15% de salaire.", "impact": "Discrimination apparence, perte de diversité"},
            {"domain": "Justice", "desc": "Les accusés attractifs reçoivent des peines plus clémentes et sont jugés moins coupables à preuves égales.", "impact": "Injustice judiciaire"},
            {"domain": "Marketing", "desc": "Un beau packaging améliore la perception de la qualité du produit. Les célébrités 'transfèrent' leur halo aux marques.", "impact": "Choix de consommation biaisés"},
            {"domain": "Éducation", "desc": "Les élèves attractifs ou bien habillés reçoivent des notes légèrement supérieures à travail égal.", "impact": "Inégalité scolaire"},
            {"domain": "Politique", "desc": "Les candidats perçus comme plus compétents sur la base de leur visage gagnent plus souvent les élections.", "impact": "Démocratie superficielle"}
        ],
        "debiasing_strategies": [
            "Évaluations anonymisées (CV sans photo, copies sans nom)",
            "Grilles critériées : évaluer chaque dimension séparément",
            "Conscientiser le biais : simplement savoir qu'il existe réduit son effet",
            "Évaluation par plusieurs juges indépendants",
            "Séparer l'évaluation de l'apparence de celle du contenu"
        ],
        "simulation": "halo",
        "illustration": "/static/illustrations/bias_halo.jpg",
        "real_world_image": "/static/illustrations/real_halo.jpg",
        "schema_image": None,
        "related_biases": ["b_confirmation", "b_auto_complaisance", "b_surconfiance"],
        "key_articles": ["thorndike_1920"]
    },
    "b_surconfiance": {
        "id": "b_surconfiance",
        "title": "Biais de surconfiance",
        "subtitle": "On se croit meilleurs qu'on ne l'est",
        "definition_complete": "Le biais de surconfiance est la tendance systématique à surestimer ses propres capacités, connaissances, ou la précision de ses jugements. Il se manifeste sous trois formes : surestimation de la performance absolue, surestimation relative (par rapport aux autres), et excès de précision (intervalles de confiance trop étroits).",
        "history": "Lichtenstein et Fischhoff (1977) ont montré que quand les gens sont sûrs à 90% d'avoir raison, ils n'ont raison que ~75% du temps. L'effet est particulièrement marqué pour les questions difficiles. Moore et Healy (2008) distinguent 3 formes : surestimation, surplacement, surprecision.",
        "mechanisms": [
            "Confirmation sélective : on se souvient de ses succès plus que de ses échecs",
            "Illusion de contrôle : on surestime son influence sur les événements",
            "Ancrage sur sa propre perspective : difficulté à adopter le point de vue extérieur",
            "Motivation : la surconfiance protège l'estime de soi et motive l'action"
        ],
        "key_experiments": [
            {"name": "Lichtenstein & Fischhoff (1977)", "desc": "Calibration : confiance 90% → performance 75%. L'écart augmente avec la difficulté."},
            {"name": "Svenson (1981)", "desc": "88% des conducteurs américains se jugent au-dessus de la médiane. Impossible statistiquement."},
            {"name": "Plous (1993)", "desc": "Les analystes financiers sont surconfiants : leurs prédictions à 90% de confiance ne sont correctes que 40% du temps."}
        ],
        "real_world_applications": [
            {"domain": "Finance", "desc": "Les traders surconfiants font trop de transactions et sous-performent. 80% des fonds actifs sous-performent l'indice.", "impact": "Pertes financières, bulles spéculatives"},
            {"domain": "Entrepreneuriat", "desc": "Les entrepreneurs surestiment leurs chances de succès. 90% des startups échouent, mais chaque fondateur pense être dans les 10%.", "impact": "Échec entrepreneurial, investissement excessif"},
            {"domain": "Projets", "desc": "Planning fallacy : on sous-estime systématiquement le temps et le coût des projets.", "impact": "Dépassements budgétaires, retards"},
            {"domain": "Médecine", "desc": "Les médecins surconfiants font moins de tests complémentaires et manquent des diagnostics rares.", "impact": "Erreurs de diagnostic"},
            {"domain": "Prédictions politiques", "desc": "Les experts politiques sont à peine meilleurs que le hasard, mais très confiants dans leurs prédictions.", "impact": "Mauvaises décisions stratégiques"}
        ],
        "debiasing_strategies": [
            "Tenir un journal de prédictions et vérifier la calibration",
            "Considérer systématiquement pourquoi on pourrait avoir tort",
            "Élargir les intervalles de confiance (penser aux cas extrêmes)",
            "Pre-mortem : imaginer que le projet a échoué et lister les raisons",
            "Feedback régulier et objectif sur la précision de ses jugements"
        ],
        "simulation": "overconfidence",
        "illustration": "/static/illustrations/bias_overconfidence.jpg",
        "real_world_image": "/static/illustrations/real_overconfidence.jpg",
        "schema_image": None,
        "related_biases": ["b_dunning_kruger", "b_auto_complaisance", "b_illusion_validite"],
        "key_articles": []
    },
}

def get_bias_cards():
    return BIAS_CARDS

def get_bias_card(bias_id):
    return BIAS_CARDS.get(bias_id)
