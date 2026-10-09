# 🗼 WATCHTOWER — Registre des signaux du bassin de Thau (09/10/2026)

> Watchtower (fork God's Eye View, `projects/watchtower/`) devient notre **couche « screen »** pour le bassin de Thau : une carte des signalements reliée à un registre. Ce doc = le registre de départ, vérifié et enrichi. Données seed : `projects/watchtower/data/thau-signaux.json`.

## 1. ✅ Vérifications & enrichissements des pistes remontées

**Projet de territoire — dialogue citoyen** (vérifié, dates complètes) : après le panel filmé de 80 habitants (juin, agence Grand Public) et la réunion de lancement du 26/09 à Balaruc-le-Vieux, **7 réunions publiques à 18h30** : **Mèze 10/11 · Loupian 12/11 · Frontignan 17/11 · Balaruc-les-Bains 24/11 · Sète 26/11 · Marseillan 01/12 · Gigean 08/12**. Contributions analysées → orientations débattues au **Conseil communautaire fin janvier 2027** → restitution février 2027, grande réunion publique rentrée 2027. Le film documentaire des 80 habitants sert de déclencheur de débat. → **Présence physique = écoute + réseau + matière première pour notre offre.**

**ZIFMAR 2 — extension du port de Sète-Frontignan** (vérifié + détails) : 33 ha en continuité de ZIFMAR 1, base logistique/maintenance **éolien offshore** ; digue d'enclôture + 3 casiers remblayés par **1,7 M m³ de sédiments de dragage** (port + canal du Rhône à Sète) ; co-maîtrise d'ouvrage Région + Port de Sète Sud de France + VNF ; consultation publique (autorisation environnementale) **du 12/10/2026 9h au 12/01/2027 17h** ; registre dématérialisé : democratie-active.fr/dae-zifmar2-port-sete ; enjeux cités : mas conchylicole + prise d'eau de mer à l'est, RD 612, canalisations GDH/SAIPOL.
⚠️ **Réunion d'ouverture : vendredi 16/10/2026 à 18h, salle Voltaire, Frontignan** — dans une semaine. Réunion de clôture : 07/01/2027 à Sète.

**Odeurs industrielles** (vérifié) : Observatoire des odeurs du bassin de Thau (ATMO Occitanie) — **bilan 2026 T2 publié** ; plateforme **Signal'Air** ; le désengagement des « Nez référents » (126 signalements en 2021 → 20 en 2026) rend la baisse des signalements non interprétable comme une baisse des nuisances ; **4 familles persistantes** : égout/œuf pourri/soufre, excréments (en forte hausse), cuisson de graines, hydrocarbures (au plus bas depuis 2021, −81 % vs 2024). Sites industriels autour de Frontignan : GDH, ancienne raffinerie Mobil, Saipol, Timac-Agro, Hexis, Scori.

**ISDI / Pech Michel** (prudence conservée, dossier étoffé) : l'ISDI chemin du Pech Michel existe depuis **décembre 1999** (exploitant historique : CA du Bassin de Thau ; toujours répertoriée sur frontignan.fr, accès pro sur carte agglo). La préemption de sept. 2020 sur **AK 136 + AK 227 (4 000 m², « La Peyrière et Pech Michel »)** est motivée par la protection des espaces naturels sensibles — **rien ne prouve qu'elle recouvre l'emprise de l'ISDI**. Étapes pour trancher : cadastre exact de l'ISDI → croisement AK 136/227 → PLU via **Géoportail de l'urbanisme** → arrêtés préfectoraux (ISDI = autorisation/enregistrement ICPE). *(Faisable depuis un navigateur ; hors de portée des outils sandbox.)*

## 2. 📚 Les 5 dossiers de veille (confirmés)

| Dossier | Source structurée | Notre angle |
|---|---|---|
| Nuisances industrielles / odeurs | ATMO Signal'Air (bilans trimestriels) | carte signalements × vent × horaires ; le désengagement des Nez = un problème de mobilisation qu'un outil simple peut résoudre |
| Déchets / dépôts sauvages | rapport annuel déchets agglo (2025 publié 09/2026) | signalement géolocalisé photo + statut de résolution |
| Mobilité | bilan mobilités agglo (navettes maritimes >200 k voyages/an), PEM 2028 | « carte temps modes doux » = action PCAET déjà budgétée |
| Eau / lagune | SMBT, rapports eau potable/assainissement | suivi + alerte (voir module géospatial) |
| Logement / aménagement | rapport d'activité 2025 (Maison de l'Habitat, 438 logements sociaux) | croiser volumes annoncés vs besoins non satisfaits |

**Sources continues** : Midi Libre / Hérault Tribune / Thau Infos · conseils municipaux + communautaires · consultations (Région, Préfecture 34, data.gouv.fr) · groupes Facebook publics (avec règle : 1 publication = 1 témoignage, jamais une preuve de fréquence) · registre démocratie-active.fr (observations ZIFMAR 2).

## 3. 🔬 Niveaux de preuve (règle du registre)

- **A — plainte sociale** : une publication/commentaire public daté et localisé → « une personne rapporte ».
- **B — récurrence** : plusieurs signalements indépendants, dates différentes → « le problème semble récurrent ».
- **C — vérification** : rapport public, donnée, réponse officielle ou constat terrain → « corroboré, dans les limites de la source ».

Règles : lien original conservé ; jamais de données personnelles aspirées ; nombre de commentaires ≠ nombre de personnes concernées ; chaque signal garde sa piste de solution éventuelle.

## 4. 🗂 Schéma du registre (`projects/watchtower/data/thau-signaux.json`)

```json
{
  "id": "YYYY-NN", "date": "ISO", "commune": "", "quartier": "",
  "theme": "odeurs|dechets|mobilite|eau|logement|urbanisme|sante|energie",
  "fait": "résumé fidèle", "niveau": "A|B|C",
  "temoignages_independants": 0, "source": "URL ou référence",
  "reponse_officielle": "…ou null", "statut": "ouvert|suivi|resolu|a_verifier",
  "liaison_produit": "quel produit/feature du portefeuille y répond"
}
```

## 5. 📅 Échéances Watchtower (aussi au planning)

- **16/10/2026 18h** — réunion d'ouverture ZIFMAR 2, salle Voltaire, Frontignan *(y aller)*.
- **17/11/2026 18h30** — dialogue citoyen Projet de territoire, Frontignan *(y aller)*.
- **26/11/2026 18h30** — idem, Sète *(optionnel)*.
- **12/01/2027 17h** — fin consultation ZIFMAR 2 (dépôt observations possible jusque-là).
- **fin 01/2027** — Conseil communautaire : orientations du Projet de territoire.

---
*09/10/2026 — croisement : recherches utilisateur + vérifications web (agglopole.fr, vnf.fr, laregion.fr, midilibre.fr 08/09 & 25/09/2026, atmo-occitanie.org, lagazettedemontpellier.fr, frontignan.fr, dechetsbtplr.free.fr, cercoccitanie.fr).*
