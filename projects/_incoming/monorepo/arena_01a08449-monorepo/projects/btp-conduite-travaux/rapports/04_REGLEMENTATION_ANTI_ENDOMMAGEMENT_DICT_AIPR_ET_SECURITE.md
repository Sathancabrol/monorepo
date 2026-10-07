# RAPPORT THÉMATIQUE 04 : RÉGLEMENTATION ANTI-ENDOMMAGEMENT (DT-DICT), AIPR ET SÉCURITÉ ROUTIÈRE

> **Domaine :** Prévention des Risques Liés aux Réseaux Enterrés, Habilitations AIPR, Sécurité SPS et Signalisation Temporaire  
> **Textes de référence :** Code de l'Environnement (L554-1 à L554-5, R554-1 à R554-39), Arrêté du 15 février 2012 modifié, Arrêté du 29 octobre 2018, IISR Livre 1 8e partie  
> **Date de référence :** 2026  

---

## 1. Le Dispositif Réglementaire Anti-Endommagement

Le corpus contient l'intégralité de la chaîne documentaire réglementaire obligatoire :
- **Déclaration de projet de Travaux (DT) :** Établie par le Maître d'Ouvrage (MOA) en phase conception via le Guichet Unique (*reseaux-et-canalisations.gouv.fr*). Exemple : Les 14 récépissés DT du projet PUP de Saint-Nicolas-de-la-Grave (Enedis, GRDF, Orange, SIVOM, etc.).
- **Déclaration d'Intention de Commencement de Travaux (DICT) :** Émise par l'entreprise adjudicataire au moins 9 jours ouvrés (téléservice) avant le coup de pioche (Cerfa 14434*03).
- **Récépissés et Cartographies :** Analyse des plans d'exploitants et détermination des classes de précision.

```
+----------------------------------------------------------------------------------------------------+
|                                 CLASSES DE PRÉCISION DES RÉSEAUX ENTERRÉS                          |
+=========+================================================+=========================================+
| CLASSE  | INCERTITUDE MAXIMALE POSITIONNEMENT HORIZONTAL | MODE OPÉRATOIRE D'EXCAVATION AUTORISÉ   |
+---------+------------------------------------------------+-----------------------------------------+
| CLASSE A| <= 40 cm (ouvrage rigide : béton, fonte)       | Engin mécanique autorisé avec précaution|
|         | <= 50 cm (ouvrage flexible : PEHD, câble)      | Godet lisse sans dents à proximité      |
+---------+------------------------------------------------+-----------------------------------------+
| CLASSE B| > 40/50 cm et <= 1,50 mètre                    | Sondages préliminaires manuels requis   |
|         |                                                | Terrassement doux / Aspiratrice déblais |
+---------+------------------------------------------------+-----------------------------------------+
| CLASSE C| > 1,50 mètre ou tracé imprécis                 | Fouille mécanique STRICTEMENT INTERDITE |
|         | (Cas fréquent sur réseaux anciens d'eau/gaz)   | Détection non destructive ou arrêt      |
+---------+------------------------------------------------+-----------------------------------------+
```

---

## 2. Analyse de la Base QCM AIPR du Corpus (Fichiers `AIPR CORRECTION.xlsx` & `QCM AIPR Encadrant.xls`)

Le corpus intègre plus de **300 questions-réponses officielles** ventilées selon les 3 profils d'habilitation :
1. **Profil Concepteur (C) :** Établissement des DT, intégration des investigations complémentaires (IC), clauses de sécurité dans les marchés.
2. **Profil Encadrant (E - Conducteur de Travaux / Chef de Chantier) :** Analyse des réponses DICT, préparation du piquetage, gestion des constats d'arrêt et de dommage.
3. **Profil Opérateur (O - Conducteur d'engins / Ouvrier) :** Respect du marquage-piquetage, gestes d'urgence en cas d'accrochage de câble ou fuite de gaz.

### Code Couleur Normalisé du Marquage-Piquetage (Arrêté du 15/02/2012)
- 🔴 **Rouge :** Électricité (BT, HTA, HTB) et Éclairage Public.
- 🟡 **Jaune :** Gaz combustible et Hydrocarbures.
- 🔵 **Bleu :** Eau potable.
- 🟢 **Vert :** Télécommunications, Fibre optique et Vidéoprotection.
- 🟤 **Marron :** Assainissement et Eaux Pluviales.
- ⚪ **Blanc :** Zone d'emprise des travaux et repères géomètres.

---

## 3. Signalisation Temporaire et Police de la Circulation

### 3.1. Autorisations Administratives Obligatoires
- **Cerfa 14023*01 :** Demande de permission ou d'autorisation de voirie (délivrée par le gestionnaire de voirie : Département pour RD, Maire pour voie communale).
- **Cerfa 14024*01 :** Demande d'arrêté de police de la circulation fixant les restrictions (vitesse, alternat, déviation).

### 3.2. Dispositifs Opérationnels Déployés (Manuel Chef de Chantier OPPBTP)
- **Alternat par feux tricolores de chantier (KR11j) :** Réglage du temps de vert et de rouge en fonction de la longueur de la zone neutralisée et du trafic moyen journalier annuel (TMJA).
- **Alternat manuel par piquets K10 :** Présence obligatoire de 2 agents équipés d'EPI haute visibilité classe 3 reliés par liaison radio.
- **Présignalisation réglementaire :** Panneau AK5 (Travaux) à 150m, suivi de AK17 (Feux tricolores), limitation dégressive BK14 (70 km/h puis 50 km/h), interdiction de dépasser BK31, fin d'interdiction BK31 en sortie de zone.

---

## 4. Confrontation In-Situ : Réalités du Terrain et Gestion d'Urgence

1. **La découverte d'un réseau non répertorié ou en classe C :** En cas d'anomalie sur le terrain (câble non cartographié à l'emplacement de la fouille de Barbazan), le chef de chantier doit immédiatement suspendre le terrassement mécanique et établir un **Constat d'arrêt ou de sursis de travaux** contresigné par le MOE. Ce constat suspend le délai d'exécution et justifie l'indemnisation des temps d'attente.
2. **L'accrochage accidentel d'une conduite de gaz :**
   - Règle d'or : Ne jamais tenter de boucher la fuite ni remblayer.
   - Évacuation immédiate de la zone sous le vent dans un rayon de 100 mètres.
   - Interdiction formelle de toute source d'ignition (moteurs d'engins coupés, pas de téléphone dans la zone d'exclusion).
   - Appel d'urgence aux Sapeurs-Pompiers (18/112) et au gestionnaire de réseau (Urgence Sécurité Gaz GRDF : 0 800 47 33 33).
   - Rédaction obligatoire d'un **Constat de Dommage** transmis sous 24 heures.
