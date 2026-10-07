"""Fiches détaillées d'articles scientifiques fondateurs en psychologie cognitive."""

ARTICLES = {
    "tversky_kahneman_1974": {
        "id": "tversky_kahneman_1974",
        "title": "Judgment under Uncertainty: Heuristics and Biases",
        "authors": "Amos Tversky & Daniel Kahneman",
        "year": 1974,
        "journal": "Science",
        "volume": "185(4157)",
        "pages": "1124-1131",
        "doi": "10.1126/science.185.4157.1124",
        "citations": 45000,
        "illustration": "/static/illustrations/exp_tversky_kahneman_1974.jpg",
        "bias_id": "b_ancrage",
        "abstract": "Cet article séminal identifie trois heuristiques majeures — disponibilité, représentativité, et ancrage-ajustement — que les individus utilisent pour juger sous incertitude. Chaque heuristique est associée à des biais systématiques et prévisibles qui s'écartent des normes de rationalité bayésienne. L'article démontre que ces biais ne résultent ni de l'ignorance ni de la motivation, mais de l'architecture même du système cognitif humain.",
        "introduction": "Comment les gens estiment-ils la probabilité d'un événement ou la fréquence d'une classe ? La théorie normative prescrit l'application du théorème de Bayes et des règles de probabilité. Pourtant, Tversky et Kahneman proposent que les individus utilisent des raccourcis cognitifs (heuristiques) qui, bien qu'économiques, produisent des erreurs systématiques. Cet article fondateur a révolutionné la compréhension du jugement humain et valu à Kahneman le Prix Nobel d'Économie en 2002.",
        "method": {
            "participants": "Multiples échantillons : étudiants universitaires, médecins, analystes. Pas de N fixe car l'article est une revue de plusieurs expériences.",
            "design": "Série d'expériences illustrant chaque heuristique. Plans expérimentaux variés selon l'heuristique testée.",
            "procedure_anchoring": "Expérience d'ancrage : une roue de fortune truquée affiche un nombre aléatoire (10 ou 65). Les participants estiment ensuite le pourcentage de pays africains à l'ONU. L'ancre influence significativement les estimations malgré son caractère aléatoire explicite.",
            "procedure_availability": "Expérience de disponibilité : les participants jugent si les mots commençant par K sont plus fréquents que ceux ayant K en 3ème position. La facilité de génération d'exemples biaise le jugement.",
            "procedure_representativeness": "Description de 'Linda' (féministe, philosophe) → les participants jugent plus probable 'Linda est caissière de banque ET féministe' que 'Linda est caissière de banque' (violation de la conjonction)."
        },
        "results": {
            "anchoring": "Ancre basse (10) → estimation médiane = 25%. Ancre haute (65) → estimation médiane = 45%. Différence de 20 points de pourcentage. Indice d'ancrage = 0.44.",
            "availability": "70% des participants jugent les mots commençant par K plus fréquents, alors que les mots avec K en 3ème position sont en réalité 2x plus nombreux en anglais.",
            "representativeness": "85% des participants jugent 'Linda caissière ET féministe' plus probable que 'Linda caissière' seule, violant la règle de conjonction P(A∩B) ≤ P(A).",
            "effect_sizes": "Effets robustes et de grande amplitude. d de Cohen > 1.0 pour la plupart des comparaisons.",
            "data_chart": {
                "type": "bar",
                "title": "Effet d'ancrage : estimation du % de pays africains à l'ONU",
                "labels": ["Ancre basse (10)", "Ancre haute (65)"],
                "values": [25, 45],
                "y_label": "Estimation médiane (%)",
                "highlight": "Différence de 20 points malgré l'ancre aléatoire"
            }
        },
        "discussion": "Les heuristiques ne sont pas des erreurs aléatoires mais des biais systématiques prévisibles. Elles reflètent l'architecture du système cognitif : le Système 1 (rapide, intuitif) utilise ces raccourcis automatiquement, tandis que le Système 2 (lent, analytique) peut les corriger mais ne le fait pas toujours. L'ancrage est particulièrement robuste : même les experts et les incitations financières ne l'éliminent pas complètement. Ces résultats remettent en question le modèle de l'homo economicus rationnel.",
        "conclusion": "Les jugements sous incertitude sont guidés par un nombre limité d'heuristiques qui produisent des biais systématiques. La compréhension de ces mécanismes a des implications majeures pour la médecine, le droit, la finance et les politiques publiques. L'article fonde le programme de recherche 'Heuristiques et Biais' qui dominera la psychologie du jugement pendant 50 ans.",
        "impact": "45 000+ citations. Article fondateur de l'économie comportementale. A conduit au Prix Nobel de Kahneman (2002). A influencé le 'nudge' de Thaler & Sunstein (2008).",
        "key_figure_description": "Graphique en barres montrant les estimations médianes selon l'ancre : barre basse à 25% (ancre 10) vs barre haute à 45% (ancre 65), illustrant l'effet massif de l'ancrage.",
        "simulation_type": "anchoring",
        "related_articles": ["strack_mussweiler_1997", "fritz_1996"]
    },
    "wason_1960": {
        "id": "wason_1960",
        "title": "On the Failure to Eliminate Hypotheses in a Conceptual Task",
        "authors": "Peter C. Wason",
        "year": 1960,
        "journal": "Quarterly Journal of Experimental Psychology",
        "volume": "12(3)",
        "pages": "129-140",
        "doi": "10.1080/17470216008416716",
        "citations": 5200,
        "illustration": "/static/illustrations/exp_wason_1960.jpg",
        "bias_id": "b_confirmation",
        "abstract": "Dans cette tâche conceptuelle, les participants doivent découvrir une règle gouvernant des triplets de nombres. L'expérimentateur confirme que '2, 4, 6' obéit à la règle. La règle réelle est 'nombres en ordre croissant'. Les participants forment des hypothèses trop spécifiques (ex: 'nombres pairs croissants de 2 en 2') et les testent uniquement avec des exemples confirmants plutôt que des contre-exemples. Moins de 20% découvrent la règle au premier essai.",
        "introduction": "Karl Popper (1934) avait soutenu que la science progresse par falsification : on ne peut jamais prouver qu'une théorie est vraie, mais on peut prouver qu'elle est fausse. Wason teste si le raisonnement humain suit naturellement ce principe de falsification ou s'il préfère la confirmation. La tâche des '2-4-6' devient le paradigme classique pour étudier le biais de confirmation.",
        "method": {
            "participants": "29 étudiants universitaires britanniques.",
            "design": "Tâche individuelle. L'expérimentateur présente le triplet '2, 4, 6' comme conforme à une règle secrète.",
            "procedure": "Le participant propose des triplets de nombres. L'expérimentateur répond 'oui' ou 'non' selon la règle (nombres croissants). Le participant annonce sa conjecture sur la règle quand il pense l'avoir trouvée. Il peut faire autant d'essais que souhaité.",
            "key_measure": "Proportion de tests confirmants vs falsifiants. Nombre d'annonces avant de trouver la règle correcte."
        },
        "results": {
            "main_finding": "Seulement 21% (6/29) trouvent la règle correcte au premier essai. Après plusieurs annonces, 79% finissent par trouver, mais beaucoup persistent dans des hypothèses erronées.",
            "confirmation_rate": "Les participants produisent en moyenne 72% de tests confirmants et seulement 28% de tests potentiellement falsifiants.",
            "typical_pattern": "Un participant typique : conjecture 'nombres pairs croissants de 2 en 2' → teste 4,6,8 (oui) → 10,12,14 (oui) → 20,22,24 (oui) → annonce la règle → FAUX. N'a jamais testé un contre-exemple comme 1,3,5.",
            "data_chart": {
                "type": "bar",
                "title": "Tâche 2-4-6 : taux de découverte de la règle",
                "labels": ["1er essai", "2ème essai", "3ème essai", "Jamais trouvé"],
                "values": [21, 34, 24, 21],
                "y_label": "% des participants",
                "highlight": "Seulement 21% trouvent la règle au premier essai"
            }
        },
        "discussion": "Les participants montrent une 'préférence pour la confirmation' : ils testent leurs hypothèses en cherchant des exemples positifs plutôt que des contre-exemples. Ce biais n'est pas dû à un manque d'intelligence (participants universitaires) ni à la complexité de la tâche (la règle est simple). Il reflète une tendance cognitive fondamentale à chercher la confirmation plutôt que la réfutation. Wason note que même les participants informés du biais persistent à le manifester.",
        "conclusion": "Le raisonnement humain est naturellement orienté vers la confirmation plutôt que la falsification. Cette tendance a des implications profondes pour la science, le diagnostic médical, les enquêtes judiciaires et toute activité nécessitant un test rigoureux d'hypothèses. La falsification nécessite un effort cognitif délibéré qui ne vient pas naturellement.",
        "impact": "5 200+ citations. Fondement du concept de 'biais de confirmation'. Paradigme utilisé dans des milliers d'études ultérieures. Cité par Nickerson (1998) comme la démonstration la plus pure du biais.",
        "key_figure_description": "Schéma montrant le cheminement typique d'un participant : hypothèse → tests confirmants (flèches vertes) → fausse annonce → nouveau cycle. Absence de tests falsifiants (flèches rouges manquantes).",
        "simulation_type": "wason_246",
        "related_articles": ["lord_ross_lepper_1979", "nickerson_1998"]
    },
    "lord_ross_lepper_1979": {
        "id": "lord_ross_lepper_1979",
        "title": "Biased Assimilation and Attitude Polarization: The Effects of Prior Theories on Subsequently Considered Evidence",
        "authors": "Charles G. Lord, Lee Ross & Mark R. Lepper",
        "year": 1979,
        "journal": "Journal of Personality and Social Psychology",
        "volume": "37(11)",
        "pages": "2098-2109",
        "doi": "10.1037/0022-3514.37.11.2098",
        "citations": 7800,
        "bias_id": "b_confirmation",
        "abstract": "Des partisans et opposants à la peine de mort lisent les mêmes études scientifiques (une favorable, une défavorable). Chaque camp évalue l'étude confirmant sa position comme méthodologiquement supérieure et se sent renforcé dans ses convictions initiales. L'exposition à des preuves mixtes polarise les attitudes au lieu de les rapprocher, démontrant l'assimilation biaisée de l'information.",
        "introduction": "Si les gens évaluaient les preuves objectivement, l'exposition à des informations mixtes devrait rapprocher les opinions opposées (convergence bayésienne). Lord, Ross et Lepper testent l'hypothèse inverse : le biais de confirmation produit une 'assimilation biaisée' où chaque camp interprète les mêmes preuves comme supportant sa position, menant à une polarisation des attitudes.",
        "method": {
            "participants": "48 étudiants de Stanford : 24 favorables et 24 opposés à la peine de mort (sélectionnés par questionnaire préalable).",
            "design": "Plan 2 (attitude initiale : pro vs anti) × 2 (ordre des études). Chaque participant lit deux études fictives sur l'effet dissuasif de la peine de mort.",
            "procedure": "Phase 1 : Mesure de l'attitude initiale. Phase 2 : Lecture d'une étude montrant que la peine de mort réduit les homicides (méthode : comparaison entre états). Évaluation de la qualité méthodologique. Phase 3 : Lecture d'une étude montrant l'absence d'effet dissuasif (méthode : comparaison avant/après). Évaluation. Phase 4 : Mesure finale de l'attitude.",
            "key_measure": "Évaluation de la qualité méthodologique (échelle 1-15). Changement d'attitude (avant vs après)."
        },
        "results": {
            "biased_evaluation": "Les participants pro-peine de mort évaluent l'étude favorable comme significativement meilleure (M=8.3) que l'étude défavorable (M=5.6). Les anti évaluent l'étude défavorable comme meilleure (M=7.9) que la favorable (M=5.4).",
            "polarization": "Après lecture des deux études, les pro sont DEVENUS PLUS pro (+0.8 sur échelle 16 points) et les anti sont DEVENUS PLUS anti (-0.7). L'exposition à des preuves mixtes a élargi l'écart entre les deux camps.",
            "methodology_critique": "Chaque camp critique davantage la méthodologie de l'étude qui contredit sa position. Les pro trouvent la méthode 'avant/après' faible, les anti trouvent la méthode 'comparaison entre états' faible.",
            "data_chart": {
                "type": "grouped_bar",
                "title": "Évaluation biaisée des études (Lord, Ross & Lepper, 1979)",
                "groups": ["Pro peine de mort", "Anti peine de mort"],
                "labels": ["Étude favorable", "Étude défavorable"],
                "values": [[8.3, 5.6], [5.4, 7.9]],
                "y_label": "Qualité perçue (/15)",
                "highlight": "Chaque camp trouve l'étude confirmante supérieure"
            }
        },
        "discussion": "L'assimilation biaisée explique pourquoi les débats sur des sujets controversés (peine de mort, avortement, changement climatique) ne convergent pas malgré l'accumulation de preuves. Chaque camp 'voit' dans les mêmes données la confirmation de ses croyances. L'effet est d'autant plus fort que l'attitude est ancrée et liée à l'identité. La polarisation n'est pas due à l'ignorance mais au traitement biaisé de l'information disponible.",
        "conclusion": "L'exposition à des preuves scientifiques mixtes peut paradoxalement renforcer les attitudes préexistantes et augmenter la polarisation. Ce résultat a des implications majeures pour le débat public, l'éducation scientifique et la communication des preuves. Simplement 'donner les faits' ne suffit pas à changer les opinions.",
        "impact": "7 800+ citations. Démonstration classique de la polarisation des attitudes. Fondement des recherches sur les chambres d'écho et les bulles de filtres sur les réseaux sociaux.",
        "key_figure_description": "Graphique montrant la divergence des attitudes : deux lignes qui s'écartent après l'exposition aux preuves mixtes, illustrant la polarisation.",
        "simulation_type": "polarization",
        "related_articles": ["wason_1960", "nickerson_1998"]
    },
    "kruger_dunning_1999": {
        "id": "kruger_dunning_1999",
        "title": "Unskilled and Unaware of It: How Difficulties in Recognizing One's Own Incompetence Lead to Inflated Self-Assessments",
        "authors": "Justin Kruger & David Dunning",
        "year": 1999,
        "journal": "Journal of Personality and Social Psychology",
        "volume": "77(6)",
        "pages": "1121-1134",
        "doi": "10.1037/0022-3514.77.6.1121",
        "citations": 12000,
        "illustration": "/static/illustrations/exp_kruger_dunning_1999.jpg",
        "bias_id": "b_dunning_kruger",
        "abstract": "Quatre études montrent que les participants du quartile inférieur en humour, logique et grammaire surestiment massivement leur performance (estiment être au 62ème percentile alors qu'ils sont au 12ème). Cette surestimation résulte d'un double fardeau : l'incompétence produit à la fois de mauvaises performances et l'incapacité métacognitive de reconnaître cette incompétence. Quand les incompétents reçoivent une formation, leur calibration s'améliore — preuve que le déficit est métacognitif.",
        "introduction": "Le psychologue McArthur Wheeler avait braqué deux banques en plein jour, le visage enduit de jus de citron, convaincu que cela le rendrait invisible aux caméras (le jus de citron étant utilisé comme encre invisible). Dunning fut frappé par le fait que Wheeler n'avait 'pas la moindre idée' de son erreur. Cet article teste systématiquement l'hypothèse que les incompétents souffrent d'un double déficit : ils performent mal ET ne peuvent pas le savoir.",
        "method": {
            "participants": "Étude 1 : 65 étudiants Cornell (humour). Étude 2 : 45 étudiants (logique). Étude 3 : 45 étudiants (grammaire). Étude 4 : réplication avec formation.",
            "design": "Chaque participant complète un test de 20 items dans un domaine, puis estime sa performance absolue (nombre de bonnes réponses) et relative (percentile par rapport aux autres).",
            "procedure": "Phase 1 : Test objectif (20 items). Phase 2 : Estimation du percentile (0-100). Phase 3 (Études 2-3) : Révélation des résultats réels + ré-estimation. Phase 4 (Étude 4) : Formation métacognitive pour les incompétents → re-test de calibration.",
            "key_measure": "Écart entre percentile estimé et percentile réel (biais de surestimation). Calibration (corrélation entre estimation et performance)."
        },
        "results": {
            "quartile_1": "Performance réelle : 12ème percentile. Estimation : 62ème percentile. Surestimation : +50 points de percentile.",
            "quartile_2": "Performance réelle : 34ème percentile. Estimation : 68ème percentile. Surestimation : +34 points.",
            "quartile_3": "Performance réelle : 58ème percentile. Estimation : 72ème percentile. Surestimation : +14 points.",
            "quartile_4": "Performance réelle : 86ème percentile. Estimation : 74ème percentile. Sous-estimation : -12 points.",
            "training_effect": "Après formation métacognitive (Étude 4), les incompétents améliorent leur calibration : l'écart entre estimation et performance se réduit de 50 à 20 points.",
            "data_chart": {
                "type": "line",
                "title": "Effet Dunning-Kruger : estimation vs performance réelle par quartile",
                "x_label": "Quartile de performance réelle",
                "y_label": "Percentile",
                "lines": [
                    {"label": "Estimation subjective", "x": ["Q1 (12e)", "Q2 (34e)", "Q3 (58e)", "Q4 (86e)"], "y": [62, 68, 72, 74]},
                    {"label": "Performance réelle", "x": ["Q1 (12e)", "Q2 (34e)", "Q3 (58e)", "Q4 (86e)"], "y": [12, 34, 58, 86]}
                ],
                "highlight": "Les incompétents surestiment de 50 points de percentile"
            }
        },
        "discussion": "L'effet Dunning-Kruger n'est pas un simple optimisme irréaliste : il est spécifique aux incompétents. Les compétences nécessaires pour bien performer sont les mêmes que celles nécessaires pour évaluer la performance (métacognition). L'incompétence crée un double fardeau : elle dégrade la performance ET la capacité d'auto-évaluation. La formation métacognitive réduit l'effet, confirmant son origine cognitive plutôt que motivationnelle. Les experts sous-estiment légèrement car ils supposent (à tort) que les autres trouvent la tâche aussi facile qu'eux.",
        "conclusion": "L'incompétence est un double fardeau : elle produit de mauvaises performances et prive de la capacité métacognitive de le reconnaître. Ce résultat explique pourquoi les incompétents ne cherchent pas à s'améliorer (ils ne voient pas le problème) et pourquoi les experts doutent d'eux-mêmes (ils surestiment la facilité pour les autres). L'effet a des implications majeures pour l'éducation, le management et l'auto-évaluation.",
        "impact": "12 000+ citations. Prix Ig Nobel 2000 (parodie) puis confirmation robuste. Concept devenu culturellement viral ('Dunning-Kruger'). Répliqué dans de nombreux domaines : finance, conduite, politique, médecine.",
        "key_figure_description": "Graphique en lignes montrant deux courbes : la ligne 'estimation subjective' (plate à ~65-75%) vs la ligne 'performance réelle' (diagonale de 12 à 86%). L'écart maximal est au Q1 (50 points de surestimation).",
        "simulation_type": "dk_simulation",
        "related_articles": ["ehrlinger_2008", "schlosser_2018"]
    },
    "stroop_1935": {
        "id": "stroop_1935",
        "title": "Studies of Interference in Serial Verbal Reactions",
        "authors": "John Ridley Stroop",
        "year": 1935,
        "journal": "Journal of Experimental Psychology",
        "volume": "18(6)",
        "pages": "643-662",
        "doi": "10.1037/h0054651",
        "citations": 18000,
        "illustration": "/static/illustrations/exp_stroop_1935.jpg",
        "bias_id": "b_confirmation",
        "abstract": "Trois expériences mesurent l'interférence entre la lecture automatique de mots et la dénomination de couleurs. Quand le mot 'ROUGE' est imprimé en encre bleue, les participants mettent ~200ms de plus à nommer la couleur d'encre que dans la condition congruente (mot 'ROUGE' en rouge). Cet effet d'interférence (effet Stroop) démontre l'automaticité de la lecture et le coût du contrôle exécutif nécessaire pour inhiber la réponse dominante.",
        "introduction": "La lecture est un processus hautement automatisé chez l'adulte alphabétisé. Stroop teste si cette automaticité interfère avec une tâche concurrente (nommer la couleur d'encre). L'hypothèse est que la lecture du mot (processus automatique) entre en conflit avec la dénomination de couleur (processus contrôlé), produisant un coût temporel mesurable. Ce paradigme deviendra l'un des tests les plus utilisés en psychologie cognitive et clinique.",
        "method": {
            "participants": "Expérience 1 : 70 participants. Expérience 2 : 100 participants. Expérience 3 : 240 participants (réplication étendue).",
            "design": "Plan intra-sujets à 3 conditions : (1) Lecture de mots de couleurs imprimés en noir, (2) Dénomination de carrés de couleur, (3) Dénomination de la couleur d'encre de mots de couleurs incongruents.",
            "procedure": "Chaque condition présente 100 stimuli sur une carte. Le participant doit répondre le plus vite possible sans erreur. Chronométrage au centième de seconde. Les conditions sont contrebalancées.",
            "key_measure": "Temps total de complétion par condition. Taux d'erreurs."
        },
        "results": {
            "reading_words": "Temps moyen de lecture de 100 mots de couleurs en noir : 41 secondes. (Processus automatique, rapide)",
            "naming_colors": "Temps moyen de dénomination de 100 carrés de couleur : 63 secondes. (Processus contrôlé, plus lent)",
            "stroop_interference": "Temps moyen de dénomination de la couleur d'encre de 100 mots incongruents : 86 secondes. Soit +23 secondes (+37%) par rapport aux carrés de couleur.",
            "reverse_stroop": "Lire les mots de couleurs imprimés en encre incongruente : pas d'interférence significative. L'asymétrie confirme que la lecture est plus automatique que la dénomination de couleur.",
            "practice_effect": "Avec la pratique (10 sessions), l'interférence se réduit de 37% à 14% mais ne disparaît jamais complètement.",
            "data_chart": {
                "type": "bar",
                "title": "Effet Stroop : temps de complétion (secondes pour 100 items)",
                "labels": ["Lecture de mots", "Dénomination couleurs", "Stroop (incongruent)"],
                "values": [41, 63, 86],
                "y_label": "Temps (secondes)",
                "highlight": "+37% de temps en condition incongruente (effet Stroop)"
            }
        },
        "discussion": "L'effet Stroop démontre que la lecture est un processus automatique qui interfère avec le contrôle exécutif. L'asymétrie (l'encre n'interfère pas avec la lecture, mais le mot interfère avec la dénomination) reflète la différence de degré d'automatisation entre les deux processus. L'interférence persiste malgré la pratique, suggérant qu'elle est inhérente à l'architecture cognitive. Le test Stroop deviendra un outil clinique majeur pour évaluer les fonctions exécutives, le TDAH, les lésions frontales et la schizophrénie.",
        "conclusion": "L'interférence Stroop est un phénomène robuste et persistant qui reflète le conflit entre un processus automatique (lecture) et un processus contrôlé (dénomination de couleur). Le paradigme offre une fenêtre unique sur les mécanismes de contrôle exécutif et d'inhibition cognitive.",
        "impact": "18 000+ citations. Test le plus utilisé en neuropsychologie. Applications cliniques : TDAH, lésions frontales, schizophrénie, démence. Variantes : Stroop émotionnel, Stroop spatial (Simon), Stroop numérique.",
        "key_figure_description": "Graphique en barres montrant les 3 conditions : barre courte (lecture, 41s), barre moyenne (couleurs, 63s), barre haute (Stroop, 86s). L'écart entre les deux dernières barres illustre l'interférence.",
        "simulation_type": "stroop",
        "related_articles": ["macLeod_1991"]
    },
    "thorndike_1920": {
        "id": "thorndike_1920",
        "title": "A Constant Error in Psychological Ratings",
        "authors": "Edward L. Thorndike",
        "year": 1920,
        "journal": "Journal of Applied Psychology",
        "volume": "4(1)",
        "pages": "25-29",
        "doi": "10.1037/h0071663",
        "citations": 3800,
        "bias_id": "b_halo",
        "abstract": "Deux officiers évaluent leurs soldats sur des dimensions supposées indépendantes : intelligence, leadership, caractère, physique, tactique. Les corrélations entre dimensions sont systématiquement élevées (r = .51 à .84), bien supérieures aux corrélations attendues. Thorndike identifie une 'erreur constante' : une impression globale positive ou négative 'déborde' d'une dimension à l'autre, créant un effet de halo.",
        "introduction": "Les évaluations de personnel supposent que les juges peuvent évaluer indépendamment différentes qualités. Thorndike teste cette hypothèse en analysant les évaluations militaires. Si les dimensions sont réellement indépendantes, les corrélations entre elles devraient être faibles. Thorndike découvre qu'elles sont au contraire massivement corrélées, révélant un biais systématique qu'il nomme 'effet de halo'.",
        "method": {
            "participants": "2 officiers évaluant respectivement 128 et 85 soldats subordonnés.",
            "design": "Évaluation sur 5 dimensions : intelligence, leadership, caractère (fiabilité), physique, valeur tactique.",
            "procedure": "Chaque officier classe ses soldats par rang sur chaque dimension. Les rangs sont convertis en scores standardisés. Les corrélations entre dimensions sont calculées.",
            "key_measure": "Corrélations inter-dimensions. Si les dimensions sont indépendantes, r devrait être ~0. Si le halo opère, r sera élevé."
        },
        "results": {
            "correlations": "Corrélations entre dimensions : Intelligence-Leadership r=.51, Intelligence-Caractère r=.58, Physique-Leadership r=.52, Physique-Caractère r=.51, Intelligence-Physique r=.84.",
            "halo_effect": "Toutes les corrélations sont significativement supérieures à 0. Le halo est particulièrement fort entre Intelligence et Physique (r=.84), suggérant que les officiers jugent les soldats physiquement impressionnants comme aussi plus intelligents.",
            "constant_error": "L'erreur n'est pas aléatoire mais systématique : elle va toujours dans le sens d'une généralisation de l'impression globale.",
            "data_chart": {
                "type": "heatmap",
                "title": "Matrice de corrélations entre dimensions (Thorndike, 1920)",
                "dimensions": ["Intelligence", "Leadership", "Caractère", "Physique", "Tactique"],
                "values": [[1,.51,.58,.84,.49],[.51,1,.64,.52,.55],[.58,.64,1,.51,.47],[.84,.52,.51,1,.43],[.49,.55,.47,.43,1]],
                "highlight": "Toutes les corrélations > .40, démontrant l'effet de halo"
            }
        },
        "discussion": "L'effet de halo révèle que les évaluations humaines sont contaminées par une impression globale qui 'teinte' toutes les dimensions. Ce biais n'est pas dû à la malveillance ou à l'incompétence des juges (officiers expérimentés), mais à l'architecture du jugement social. Thorndike note que même en demandant explicitement d'évaluer chaque dimension séparément, le halo persiste. Le biais a des implications majeures pour le recrutement, l'évaluation scolaire et la recherche en psychologie.",
        "conclusion": "Une 'erreur constante' contamine les évaluations psychologiques : l'impression globale d'une personne influence le jugement de chacune de ses qualités. Cet effet de halo est systématique, robuste et résistant aux instructions de correction. Il représente un défi fondamental pour toute évaluation humaine.",
        "impact": "3 800+ citations. Article fondateur du concept d'effet de halo. Nisbett & Wilson (1977) montrent que l'effet opère sans conscience. Applications : recrutement (CV anonymes), justice (apparence des accusés), éducation (notes).",
        "key_figure_description": "Matrice de corrélation en heatmap montrant des valeurs élevées (.51 à .84) entre toutes les dimensions, illustrant la généralisation du halo.",
        "simulation_type": "halo_evaluation",
        "related_articles": ["nisbett_wilson_1977", "landy_sigall_1974"]
    },
}

def get_articles():
    return ARTICLES

def get_article(article_id):
    return ARTICLES.get(article_id)
