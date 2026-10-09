# 09 — Plan de marche jusqu'au 16 octobre

**Échéance :** vendredi 16 octobre 2026 — utilisation **en situation réelle** lors d'un rendez-vous avec l'Agglo.
**Établi le :** vendredi 9 octobre 2026. **Reste : 7 jours.**

---

## 1. Ce que « utilisable de façon correcte » veut dire le 16

Ce n'est pas « tout est terminé ». C'est : **je peux m'en servir devant quelqu'un, sans avoir honte et sans risquer la panne.**

| # | Exigence | Test de vérité |
|---|---|---|
| 1 | Ça démarre | Double-clic sur le raccourci bureau. Aucune console, aucune ligne de commande. |
| 2 | Ça capture | Je dis ou je tape une phrase, une proposition apparaît dans le bac en moins de 2 s. |
| 3 | Ça décide | J'accepte d'un clic. Refus d'un clic. Rien n'entre dans le compte rendu sans moi. |
| 4 | Ça produit | À la fin, un compte rendu qui s'ouvre dans Word et un diaporama qui s'ouvre dans PowerPoint. |
| 5 | Ça survit | Je coupe le réseau : tout continue. Je ferme et je rouvre : rien n'est perdu. |
| 6 | Ça se répare | Un plantage = je relance, la session est intacte. |

Le point 6 est le plus important et le plus souvent oublié. C'est pour ça que
tout est stocké en JSON lisible, écrit de façon atomique, dans un dossier qu'on
peut ouvrir avec l'explorateur.

---

## 2. État au soir du 9 octobre — ce qui est déjà fait

| Module | État | Ce qui marche vraiment |
|---|---|---|
| **Réunion** (prioritaire) | **opérationnel** | Création, verbatim en direct, extraction décisions/actions/risques/questions, bac à suggestions, acceptation, budget, planning, **29 formats de documents** dont .docx et .pptx valides |
| **Cartographie** | catalogue | 32 couches territoriales du Bassin de Thau avec **licence vérifiée**, points d'observation, vues mémorisées |
| **Cognitorium** | opérationnel | Fiches individus/structures/partenaires, indexeur de l'état de l'art du dépôt |
| **Prévision** | opérationnel | 26 indicateurs (météo, social, géopolitique, économie, psychologie), scénarios, note de prévision |
| **OSINT** | opérationnel | 41 outils et sources (France d'abord), conduite de cas, chaîne de preuves avec fiabilité A→X |
| **Système / MAJ** | opérationnel | Canal Git, sauvegarde, retour arrière, installeur Windows, CI |

**Aucune dépendance obligatoire.** Le cœur tourne avec la seule bibliothèque
standard de Python. Conséquence : l'installation ne peut pas échouer à cause
d'un paquet introuvable, et tout fonctionne hors ligne.

**Vérification automatique :** `python3 scripts/test-carre-d-as.py` → 29 documents, 0 échec.

---

## 3. Les sept jours

### ▸ Vendredi 9 — Fondations *(fait)*

- [x] Cœur applicatif : serveur, configuration, journal, flux temps réel
- [x] Les 5 modules obligatoires câblés
- [x] Génération de documents sans dépendance (.docx, .pptx, .csv, .svg, .md, .html, .txt)
- [x] Installeur Windows + canal de mise à jour Git
- [x] Intégration continue : scénario complet rejoué à chaque poussée
- [x] **Territoire paramétré** : Sète Agglopôle, 14 communes, 131 000 habitants

**À faire de ton côté ce soir :** exécuter `install.ps1` sur ton poste Windows et
me dire si ça passe. C'est le seul point que je ne peux pas vérifier moi-même.

### ▸ Samedi 10 — Installation réelle + voix

- [ ] Valider l'installation sur Windows (raccourci, démarrage, données)
- [ ] Brancher la **reconnaissance vocale** : `faster-whisper` (modèle `small`, ~1 Go) ou `whisper.cpp`
- [ ] Test de dictée en continu sur 5 minutes de parole réelle
- [ ] Premier compte rendu généré depuis une vraie discussion

*Repli si la voix ne tient pas :* saisie clavier pendant la réunion. L'extraction
est identique. Une personne qui tape les phrases essentielles obtient un
compte rendu excellent — c'est moins confortable, ce n'est pas moins bon.

### ▸ Dimanche 11 — Durcir la réunion

- [ ] Sauvegarde automatique de la session toutes les 30 s (indépendante de l'acceptation)
- [ ] Reprise après coupure : rouvrir l'appli retrouve la réunion en cours
- [ ] Export d'urgence : un bouton « tout sortir en .md » qui marche même si le reste casse
- [ ] Relire un compte rendu généré comme si on était le destinataire — et corriger les formulations

### ▸ Lundi 12 — Cognitorium + préparation du RDV

- [ ] Créer les **profils des personnes** que tu vas rencontrer (nom, rôle, structure, commune)
- [ ] Relier chaque profil à ce qu'on sait déjà (délibérations, prises de position, sujets)
- [ ] Préparer l'ordre du jour du RDV dans l'application
- [ ] Indexer `projects/COGNITORIUM` et `projects/ETAT-DE-LART-PSYCHOLOGIE`

### ▸ Mardi 13 — Cartographie + OSINT

- [ ] Pointer les lieux dont on va parler (Frange Sud, ZAE, Salins de Villeroy, RD2)
- [ ] Vérifier les structures partenaires : Annuaire des Entreprises, Pappers, JOAFE — traçable
- [ ] Constituer un dossier de 3 ou 4 sources **fiabilité A** sur le sujet du RDV

*Rappel de discipline :* une donnée accessible n'est pas une donnée librement
réutilisable, et toute donnée personnelle déclenche le RGPD. Le module exige
une source pour chaque élément — c'est volontaire.

### ▸ Mercredi 14 — Répétition générale

- [ ] Simulation complète du RDV, chrono en main : installation → réunion → documents → envoi
- [ ] Mesurer : combien de temps entre la fin de la réunion et le compte rendu envoyé ? *(cible : 10 min)*
- [ ] Corriger tout ce qui a coincé

### ▸ Jeudi 15 — Gel

- [ ] **Gel des fonctionnalités** : plus aucune nouveauté après 18 h
- [ ] Installation propre sur le poste qui servira le 16 (désinstaller / réinstaller)
- [ ] Sauvegarde complète du dossier de données sur un second support
- [ ] Préparer le **plan B** : les documents sortent aussi en `.html`, ouvrables dans n'importe quel navigateur

### ▸ Vendredi 16 — Le rendez-vous

- [ ] Poste branché sur secteur, Application lancée 15 min avant
- [ ] Une réunion créée à l'avance, participants déjà saisis
- [ ] Mode avion essayé une fois pour vérifier que rien ne dépend du réseau
- [ ] Après le RDV : générer le compte rendu, le relire **avant** de l'envoyer

---

## 4. Ce qu'on ne fera pas avant le 16 — et pourquoi

Assumer ces renoncements maintenant évite de les découvrir à 23 h le 15.

| Repoussé | Raison |
|---|---|
| Vue 3D Cesium | `projects/watchtower` contient déjà le moteur ; le brancher prend plusieurs jours à lui seul. Le catalogue de couches est prêt et utile immédiatement. |
| Carte interactive dans l'application | Le catalogue, les points et les vues sont là. Le rendu cartographique (MapLibre) arrive juste après — Mapbox est exclu, sa licence v2 est propriétaire. |
| Modèle IA embarqué | Ollama reste un service externe qu'on installe une fois. L'application le détecte et s'en sert ; sans lui, elle produit quand même tout. |
| Application mobile | Après. Le 16, c'est un poste fixe. |
| Synchronisation entre postes | Après. Le format JSON s'y prête, ce n'est pas le sujet de la semaine. |

---

## 5. Risques et parades

| Risque | Probabilité | Parade |
|---|---|---|
| L'installation échoue sur ton Windows | moyenne | Le cœur n'a aucune dépendance : `python main.py` suffit. `install.ps1` n'est qu'un confort. |
| La reconnaissance vocale est trop lente | **haute** sur GTX 1060 | Modèle `small` plutôt que `medium`. Repli : saisie clavier. L'extraction est la même. |
| Le modèle local ne rentre pas en mémoire | moyenne | Le mode déterministe ne charge aucun modèle. Il sort les documents. |
| Un .docx s'ouvre mal dans Word | faible | Structure OPC validée automatiquement dans le test ; à confirmer sur ton Word. |
| Panne réseau pendant la RDV | faible | Rien dans la chaîne critique ne dépend du réseau. |
| Oubli de sauvegarder | moyenne | Sauvegarde automatique (dimanche) + une sauvegarde manuelle le 15. |

---

## 6. Trois décisions à prendre de ton côté

1. **Reconnaissance vocale — oui ou non pour le 16 ?**
   Oui = il faut installer ~1 Go et tester samedi. Non = tu tapes les phrases
   essentielles, et le compte rendu est tout aussi bon.

2. **Modèle local (Ollama) — oui ou non ?**
   Oui = ~5 Go sur le disque, meilleure extraction, aucune donnée ne sort du
   poste. Non = extraction déterministe seule, qui couvre déjà l'essentiel.

3. **Le RDV du 16 : plutôt présentation de l'outil, ou outil au service d'un
   sujet précis ?** La deuxième option est bien plus convaincante — on vient
   avec un dossier déjà instruit, pas avec une démonstration.

---

## 7. Après le 16

`v0.2` — branchement du moteur cartographique MapLibre, branchement du moteur 3D
de `projects/watchtower`, passerelles vers Nexus OS (22 agents, 30 compétences
déjà écrits dans le dépôt), et mise à jour depuis le site dédié en plus de Git.
