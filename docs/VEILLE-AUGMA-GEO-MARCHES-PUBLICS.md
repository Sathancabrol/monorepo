# 🔭 VEILLE — Augma Imaginatorium · Géospatial · Marchés publics Hérault (09/10/2026)

> Trois apports en un tour : (1) un modèle d'entreprise à observer (Augma, Bangkok), (2) une technique gratuite qui renforce **l'offre O2** juste avant l'échéance du 20/10, (3) un canal de prospection officiel et gratuit : les marchés publics de l'Hérault.

---

## 1. 🏢 Augma Imaginatorium (Bangkok) — un miroir lointain de notre projet

**Qui** : « development think tank » fondé en 2023 à Bangkok (fondateur : M.L. Hariras Tongyai). Positionnement : *des idées neuves, construites et testées* — prototype → venture. **27 projets, 19 en cours** [augmaimaginarium.com/projects](https://www.augmaimaginarium.com/projects/).

**Projets marquants** :
- **K.A.R.A** — assistant personnel IA : voix (« Hey Kara »), brief du matin, to-do, agrège messages/calendrier/notes/santé en un seul tableau de bord. C'est littéralement « notre » idée d'entreprise d'IA appliquée au bureau — mais version consommateur Mac/téléphone.
- **Bangkok Situational Map** — carte 3D holographique des inondations en temps réel : où est l'eau, quelles routes éviter, où l'aide est demandée. **Data territoriale au service des gens** : le même esprit que notre offre O2, en plus spectaculaire.
- **AIEngram** (console WebGL pour regarder dans un réseau de neurones, option Ollama local), **Augma Hub** (chat Gemini + calendrier + journal), contrats marques : Grab Thailand, Thailand Post, TAT.

**Les 4 leçons à voler** (aucun copiage de produit — ils sont à Bangkok, dans l'AR/installations, pas concurrents) :
1. **Un projet = une phrase « Goal » + une démo en ligne.** Leur bibliothèque présente chaque cube avec son objectif en une ligne et souvent un lien live. À appliquer tel quel à notre one-pager/portfolio (service `marketing`) : chaque capacité démontrée avec son but + une démo cliquable.
2. **Building in public** : 19/27 projets « ongoing » montrés quand même. La régularité visible vaut mieux que la perfection cachée — cohérent avec notre calendrier social (posts 16 & 23/10).
3. **Prototype → venture** : les petits prototypes publics attirent les contrats marques (Grab, Thailand Post), qui financent la suite. Traduction chez nous : les tests O1/O2/O3 sont nos prototypes publics ; les contrats qu'ils décrochent financent le reste.
4. **Un visage/une voix pour l'assistant** (K.A.R.A Digital Human) : pas notre étape, mais note pour plus tard — une identité incarnée aide à vendre.

## 2. 🛰 Le reel « Geospatial Intelligence » → module béton pour l'offre O2

**La technique vue dans le reel (@yoiqino, pt. 3/7)** : détecter les constructions nouvelles en zone rurale à partir de données satellites **gratuites** (buckets AWS publics) :
1. **NDVI** (Sentinel-2) : la végétation qui chute = construction possible ;
2. problème : ça chute aussi en hiver → **séries temporelles + BFAST** pour modéliser la saisonnalité et ne pas confondre blé en dormance et chantier ;
3. **SAR** (Sentinel-1, radar) : mesure la rugosité du sol et distingue feuilles / terre nue / bâti ;
4. **fusion des deux capteurs** → zones de construction avec score de confiance.

**Pourquoi ça compte pour nous MAINTENANT** : c'est le module manquant de l'offre **O2 (intelligence territoriale)**, dont le deck Frontignan est attendu le **20/10** :
- **Tout est gratuit** : Sentinel-1/2 = données Copernicus ouvertes (disponibles sur AWS open data), traitement possible sans GPU local (notebooks gratuits).
- **Le crochet réglementaire est réel** : loi Climat & Résilience → objectif **ZAN** (zéro artificialisation nette) : **−50 % d'artificialisation d'ici 2031**, PLU/PLUi à mettre en compatibilité d'ici le **22/02/2028**, et les collectivités doivent **suivre leur consommation foncière**. Une commune comme Frontignan a juridiquement besoin de ce suivi.
- **Promesse à ajouter au deck** : « carte de l'artificialisation 2024→2026 de la commune, détection des constructions non déclarées aux documents d'urbanisme, rapport ZAN prêt à présenter ». C'est démontrable, chiffrable, et personne autour n'offre ça à petit prix.
- **Limites à dire honnêtement** : résolution 10 m (on détecte des bâtiments, pas des clôtures), la calibration saisonnière demande 2-3 ans d'historique, et un premier prototype sérieux prend quelques jours de traitement (pas une démo pour le 20/10 — pour le 20/10, on vend la **méthode + un échantillon** sur une zone témoin).

## 3. 📋 BOAMP + Midi Libre = canal de prospection officiel, gratuit, quotidien

**BOAMP** (le lien filtré département 34) : c'est LE bulletin officiel des marchés publics, et il a une **API officielle gratuite** (DILA, Licence Ouverte 2.0) : `https://boamp-datadila.opendatasoft.com/api/explore/v2.0` — filtrable par département, type (TRAVAUX/SERVICES/FOURNITURES), mots-clés, dates ; export CSV/JSON. On peut donc **automatiser une veille** : chaque matin, les avis SERVICES du 34 contenant « intelligence artificielle », « données », « SIG », « numérique », « étude » → injectés dans le pipeline `prospects`. Les **avis d'attribution** sont tout aussi précieux : ils disent QUI achète, QUI gagne, et à quel prix (nos concurrents + leurs tarifs).

**Midi Libre Marchés Publics** (midilibre-marchespublics.com) : le portail régional (11, 12, 30, **34**, 48, 66) sur plateforme AWS-Achat. Deux intérêts :
- consultation **libre et gratuite** des annonces ;
- **alerte e-mail gratuite** (Espace Fournisseur) sur critères — avec le bonus des consultations **< 40 000 € souvent sans publicité ailleurs** : exactement la taille de marché qui nous convient (300–800 € la prestation d'amorçage, puis plus).

**Checklist pratique (à faire quand la première vraie candidature se prépare)** :
1. S'inscrire à l'alerte gratuite Midi Libre + paramétrer une veille BOAMP dept 34 (mots-clés ci-dessus).
2. Anticiper le **certificat de signature électronique eIDAS** : indispensable pour déposer, **15 jours à 1 mois** de délai d'obtention (le portail prévient : ne pas attendre la dernière semaine).
3. Préparer le socle administratif standard : SIRET, attestation fiscale/sociale, DUME — le service `invoices`/`registry` pourra tenir cette « pochette de candidature » à jour.

## 4. ✅ Décisions

- **O2** : ajouter au deck Frontignan (échéance 20/10) la promesse « suivi d'artificialisation / ZAN » (méthode NDVI + SAR + séries temporelles, données 100 % gratuites) + échantillon zone témoin. → prochaine séance de travail dédiée.
- **Prospection** : veille BOAMP API (dept 34, SERVICES) + alerte gratuite Midi Libre = canal n°4 après O1/O2/O3 ; les avis d'attribution servent à cartographier les acheteurs et concurrents.
- **Marketing** : adopter le format Augma « une phrase Goal + démo » pour présenter chaque capacité sur les one-pagers.
- Rien à acheter, rien à installer — tout est données publiques et inscription gratuite.

---
*09/10/2026 — sources : augmaimaginarium.com (projets + à-propos), midilibre-marchespublics.com, data.gouv.fr (API BOAMP DILA), presse spécialisée ZAN, transcription du reel @yoiqino.*
