# Dossier de prévision — La Palanquée, FabLab et IA locale
**Version de travail : 0.1 — 10 octobre 2026**  
**Statut : PROPOSITION À VALIDER — ne constitue ni un devis ni un engagement de La Palanquée.**

## 1. Intention

Étudier comment relier trois leviers :  
1. les capacités de fabrication numérique du FabLab de La Palanquée à Sète ;
2. une IA personnelle fonctionnant localement sur l'ordinateur du porteur de projet, avec données et documents conservés en local par défaut ;
3. des prototypes logiciels et matériels utiles au Bassin de Thau, articulés avec Watchtower, Atlas, Cognitorium et Nexus.

Le projet doit partir des problèmes réellement exprimés par les usagers, associations, acteurs économiques et collectivités. Chaque problème sera documenté avant de proposer une solution. La Palanquée est ici considérée comme un partenaire potentiel à rencontrer, pas comme un partenaire déjà engagé.

## 2. Éléments vérifiés et limites

- Le site officiel de La Palanquée décrit un FabLab fixe d'environ 80 m², un FabLab mobile et un parc comprenant découpe laser, imprimantes 3D, scanner 3D, découpe vinyle, thermoformeuse, brodeuse numérique, impression grand format et kits Arduino/Raspberry Pi/capteurs/robotique.
- Le site indique une adhésion associative de 10 € valable pour l'année civile, des initiations collectives à 30 €/personne pour 2 h, des initiations personnalisées à 40 €/h, ainsi que des tarifs machine spécifiques. Tarifs à reconfirmer au moment de réserver.
- L'accès aux machines requiert une initiation ; des créneaux autonomes sont ensuite réservables selon les règles du FabLab.
- Le site présente aussi un accompagnement à l'entrepreneuriat et un incubateur. Les dates, critères et disponibilités doivent être confirmés directement.
- Le matériel personnel de référence communiqué pour l'étude est un PC Windows avec Intel i7-6700, GTX 1060 6 Go et 16 Go de RAM. Cette configuration permet des prototypes d'IA locale modestes, mais la VRAM et la RAM limitent la taille des modèles et le traitement simultané. La faisabilité doit être testée sur la machine réelle avant tout achat.

Sources officielles à revérifier :
- https://www.lapalanquee.org/fablab/
- https://www.lapalanquee.org/incubateur-aac-2026/

## 3. Questions-problèmes à instruire avant de concevoir

Ces points sont des axes d'enquête, pas des constats déjà démontrés.

| Axe | Questions à poser | Livrable de preuve |
|---|---|---|
| Accès aux outils | Quels publics n'accèdent pas aux équipements, formations ou logiciels ? Pourquoi : prix, horaires, transport, compétences, handicap, information ? | Entretiens courts, parcours usager, fréquence et gravité |
| Prototypage | Quels besoins récurrents demandent une pièce, un boîtier, une maquette ou un capteur ? | Liste de cas d'usage priorisés et fiche technique |
| Compétences numériques | Quels freins reviennent : démarches, bureautique, code, IA, cybersécurité, recherche d'emploi ? | Atelier-test et questionnaire simple |
| Données et confidentialité | Quelles données ne doivent jamais être envoyées à un service cloud ? | Classification des données et règles de traitement |
| Territoire | Quels problèmes concrets peuvent être étudiés à l'échelle de Sète/Frontignan/Bassin de Thau ? | Jeu de données sourcé, limites et responsables |
| Viabilité | Qui utilise, maintient et finance la solution après le prototype ? | Partenaires pressentis, coût récurrent et modèle d'exploitation |
| Inclusion | Comment éviter une solution réservée aux personnes déjà technophiles ? | Test avec débutants, accessibilité et accompagnement humain |

## 4. Architecture proposée

### Poste local IA
- Moteur local : Ollama ou llama.cpp ; interface locale simple ; modèles quantifiés adaptés aux 6 Go de VRAM et 16 Go de RAM.
- Documents privés : indexation locale, recherche augmentée par récupération (RAG), citations vers les fichiers sources et indication des incertitudes.
- OCR et extraction : commencer par PDF texte et formats courants ; ajouter l'OCR seulement quand un besoin réel le justifie.
- Cloud facultatif et explicitement activé, jamais requis pour le fonctionnement de base. Ne pas présenter le système comme « totalement privé » sans auditer télémétrie, journaux, extensions, mises à jour et connexions sortantes.
- Sauvegardes locales chiffrées et gestion séparée des secrets/API ; ne jamais committer clés, documents privés ou données personnelles dans Git.

### Fabrication numérique
- Démarrer par des objets simples : support de capteur, boîtier, support caméra, pièce de remplacement ou maquette territoriale.
- Utiliser d'abord les machines existantes du FabLab plutôt que d'acheter immédiatement des équipements équivalents.
- Documenter les fichiers sources, matériaux, temps machine, coûts, tolérances, risques et licences de chaque prototype.

### Modules logiciels
- **Watchtower** : collecte et observation du présent, sources traçables et actualisation.
- **Atlas** : scénarios passés/futurs, comparaisons explicites et hypothèses séparées des faits.
- **Cognitorium** : profil de compétences, connaissances, preuves et apprentissage.
- **Nexus** : orchestration des modules, agents, matériel et workflows.
- Chaque module reste remplaçable ; les données utilisent des formats ouverts et des interfaces documentées.

## 5. Budget de cadrage — enveloppe cible 4 000 à 5 000 €

Ce tableau est une **hypothèse de répartition**, pas un devis fournisseur. Les montants doivent être affinés après test de la machine actuelle et inventaire de l'atelier.

| Poste | Enveloppe indicative | Règle de décision |
|---|---:|---|
| Diagnostic, stockage et sauvegarde locale (SSD/NVMe selon compatibilité, disque de sauvegarde) | 250–500 € | Priorité aux données et à la fiabilité |
| Mise à niveau informatique éventuelle (RAM/plateforme ou GPU) | 700–1 500 € | N'acheter qu'après benchmark ; comparer remplacement ciblé et nouvelle tour |
| Prototypage FabLab, initiations et consommables | 250–600 € | Acheter du temps machine avant d'acheter les machines |
| Capteurs, microcontrôleurs, alimentation, câblage et boîtiers | 250–600 € | Kits modulaires, documentation et pièces remplaçables |
| Ergonomie, réseau local et sécurité électrique | 150–350 € | Aucun montage dangereux ni batterie improvisée |
| Développement, tests, documentation et démonstrateur | 500–900 € | Prioriser un cas d'usage livré de bout en bout |
| Réserve pour imprévus | 500–800 € | Ne pas engager sans validation d'étape |
| **Total cible** | **2 600–5 250 €** | Ajuster à 4 000–5 000 € après devis et arbitrage |

**Principe budgétaire :** ne pas dépenser les 4–5 k€ d'un coup. D'abord un audit gratuit/peu coûteux et un prototype logiciel local ; ensuite un test FabLab ; enfin seulement les achats justifiés par les mesures. Prévoir séparément les frais récurrents éventuels (connexion, consommables, déplacements, maintenance).

## 6. Phasage proposé

1. **Semaine 1 — découverte et preuves :** entretien avec l'équipe de La Palanquée ; confirmer équipements, tarifs, calendrier, besoins et règles d'accès ; recueillir 3 à 5 problèmes concrets.
2. **Semaines 2–3 — preuve de faisabilité locale :** benchmark sur le PC existant, essai d'un modèle compact, recherche dans un petit corpus de documents non sensibles, vérification hors ligne et mesure des temps.
3. **Semaines 3–5 — prototype FabLab :** choisir un seul besoin prioritaire ; produire une maquette ou un petit objet connecté ; documenter coût, limites et mode d'emploi.
4. **Semaines 5–6 — évaluation :** test par des personnes non techniques ; mesurer temps gagné, taux d'erreur, facilité d'utilisation, coût par usage et besoins de maintenance.
5. **Après validation — dossier consolidé :** budget sur devis, partenaires confirmés, plan de financement, indicateurs d'impact et décision poursuivre/arrêter.

Les durées sont des estimations de planification, non des délais promis.

## 7. Indicateurs de réussite

- Au moins 3 problèmes utilisateurs documentés avec preuves et priorité.
- Un prototype local fonctionnel démontré sans connexion Internet pour ses fonctions principales.
- Un prototype physique ou une maquette fabriquée avec coût et fichiers reproductibles.
- Sources et incertitudes visibles ; aucun résultat IA présenté comme un fait sans preuve.
- Budget réel comparé au budget prévisionnel ; dépenses engagées par jalon.
- Test d'usage par des personnes débutantes ; retours et corrections tracés.
- Aucun secret ni document personnel dans le dépôt public ; sauvegarde et procédure de restauration testées.

## 8. Audit initial des trois outils OSINT mentionnés

Règle : ne conserver un outil que s'il apporte une fonction distincte, maintenable, licite et testable. Une fonction simple et stable doit de préférence être réimplémentée ou fournie par une bibliothèque maintenue plutôt que dépendre d'un script fragile.

| Nom transmis | Verdict initial | Décision |
|---|---|---|
| [Osintgram](https://github.com/Datalux/Osintgram) | **À conserver comme candidat isolé, pas comme dépendance du cœur.** Vérification GitHub du 10/10/2026 : dépôt non archivé, dernier push visible le 28/09/2026, licence GPL-3.0, Python. Le README annonce une interface locale et une intégration Ollama, mais les recherches Instagram dépendent des mécanismes de la plateforme et peuvent casser ou nécessiter une authentification. | Sauver la référence dans le registre ; test en environnement isolé, audit des dépendances et vérification des conditions Instagram avant toute intégration. GPL-3.0 à prendre en compte si modification/distribution. |
| WhatsAppTool | **Non identifié avec certitude** : nom trop générique et aucun dépôt exact fourni. Certains outils de ce domaine peuvent dépendre de sessions, d'API non officielles ou de données privées. | Ne pas installer ni archiver comme dépendance avant obtention de l'URL exacte et audit de sécurité/licence. |
| PhoneNumberChecker | **Non identifié avec certitude** : le nom seul ne permet pas d'établir le dépôt. La validation de format ne prouve ni l'existence actuelle d'un compte ni l'identité de son propriétaire. | Pour la validation hors ligne, évaluer une bibliothèque maintenue comme Google libphonenumber ; pour toute recherche complémentaire, documenter la source, la base légale et les faux positifs. |

Un outil rejeté peut être consigné dans le registre d'audit avec motif et date ; cela évite de le réévaluer par erreur. Ne jamais automatiser l'accès à des comptes privés, contourner une protection ou compiler des profils de personnes sans base légitime et garanties adaptées.

## 9. Décisions encore ouvertes

- Quel problème local précis doit être résolu en premier ?
- La Palanquée souhaite-t-elle un projet individuel, un atelier collectif, une prestation, un partenariat ou une candidature à un accompagnement ?
- Le budget de 4–5 k€ est-il entièrement disponible, et couvre-t-il le matériel personnel, le prototypage ou aussi les frais de vie/déplacement ?
- Quelle donnée peut rester locale et quelle donnée, le cas échéant, peut être partagée ?
- Qui assurera maintenance, support et responsabilité après la démonstration ?
- Quels dépôts exacts correspondent à « WhatsAppTool » et « PhoneNumberChecker » ?

## 10. Sources et traçabilité

- Site officiel du FabLab : https://www.lapalanquee.org/fablab/
- Page incubateur (calendrier à confirmer) : https://www.lapalanquee.org/incubateur-aac-2026/
- Registre et audits OSINT existants du monorepo : `projects/watchtower/AUDIT-OUTILS-2026.md`, `projects/watchtower/audit/CATALOGUE-OUTILS.md`, `projects/watchtower/audit/COUTS-LICENCES-LEGAL.md`.
- Les montants du budget et les étapes sont des estimations de travail, pas des informations vérifiées auprès de La Palanquée ou de fournisseurs.
