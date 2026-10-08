# 🕸️ SOCIÉTÉ SURNATURELLE CACHÉE — formalisation système

> Système dérivé de **RAW 46** · statut : **FONDATION VALIDÉE, détails d'organisations à venir**
> Objectif : que le moteur puisse générer un monde où humains et surnaturels **existent, travaillent, commercent, conspirent et évoluent sans attendre le joueur**.

## 1. Les acteurs

```
ACTEUR
├── Humain (ignorant / informé)
├── Chasseur
├── Sorcier / Sorcière
├── Monstre (vampire, loup-garou, wendigo…)
├── Démon
├── Ange
├── Entité
├── Organisation
└── Hybride
```

Chaque acteur porte ces données :

| Donnée | Exemple |
|---|---|
| Identité | nom / alias |
| Nature | humain / vampire / sorcière… |
| Pouvoir | capacités réelles |
| Faiblesse | vulnérabilités |
| Activité | travail / chasse / commerce |
| Territoire | lieux fréquentés |
| Relations | alliés / ennemis / famille |
| Ressources | argent / objets / influence |
| Connaissances | ce qu'il sait |
| Réputation | humaine **et** surnaturelle (deux valeurs distinctes) |
| Objectif | ce qu'il cherche |
| Secret | ce qu'il cache |
| Puissance | niveau réel |
| Visibilité | connu / clandestin |
| Mobilité | déplacements |

> Règle de génération : un acteur sans **activité économique ou relation** n'entre pas dans la simulation (cf. README, conventions).

## 2. Les organisations
Une organisation **n'est pas** une faction avec une barre de réputation. C'est une structure vivante :

```
ORGANISATION
├── membres        ├── dirigeants      ├── ressources
├── territoires    ├── entreprises     ├── infrastructures
├── marchés        ├── ennemis         ├── alliés
├── objectifs      ├── secrets         └── opérations
```

**Règle clé** : une organisation peut contenir **humains + surnaturels** (conséquence directe de RAW 46).

## 3. Économie surnaturelle — le graphe

```
RESSOURCE → PRODUCTEUR → INTERMÉDIAIRE → VENDEUR → CLIENT → UTILISATION
```

**Ressources potentielles** : objets enchantés · ingrédients · sang · cadavres · artefacts · informations · services magiques · protections · rituels · identités · créatures · territoires.

**Exemple généré par le moteur** :
```
SORCIÈRE
├── possède une villa
├── fréquente le restaurant X
├── vend des enchantements
└── fournisseur → INTERMÉDIAIRE → VAMPIRE (cherche un cadavre précis)
```
Ce que le joueur peut découvrir : `CADAVRE → TRACE MAGIQUE → OBJET → SORCIÈRE → CLIENT → VAMPIRE → AUTRE AFFAIRE` — **la quête est beaucoup plus profonde que ce que le joueur pensait.**

## 4. Les relations sont dynamiques
Types de relations : `ALLIANCE · CONTRAT · DETTE · AMITIÉ · FAMILLE · AMOUR · RIVALITÉ · TERRITOIRE · COMMERCE · CHANTAGE · TRAHISON · PROTECTION · EMPLOI · SERVITUDE`

**Une relation évolue sans intervention du joueur** :
```
SORCIÈRE ←→ VAMPIRE : contrat commercial
   → contrat rompu → conflit → nouvelle opportunité → JOUEUR
```

## 5. Le monde tourne sans le joueur (point central)
```
JOUEUR ABSENT → SORCIÈRE VEND OBJET → VAMPIRE ACHÈTE → RITUEL → CADAVRE
→ POLICE → RUMEUR → CHASSEUR ENTEND → INTERVENTION → JOUEUR ARRIVE
```
**Le joueur arrive au milieu d'une histoire déjà commencée.** C'est ce qui donne l'impression de monde vivant.

## 6. Connexion aux autres machines
```
                    WORLD STATE
                         │
       ┌─────────────────┼─────────────────┐
       ↓                 ↓                 ↓
     PNJ             CRÉATURES         FACTIONS
       │                 │                 │
       └─────────────────┼─────────────────┘
                         ↓
                 SOCIÉTÉ SURNATURELLE   ← ce document
                         │
        ┌────────────────┼────────────────┐
        ↓                ↓                ↓
     COMMERCE         RELATIONS        TERRITOIRES
        │                │                │
        └────────────────┼────────────────┘
                         ↓
                  ÉVÉNEMENTS → MANIFESTATIONS → JOUEUR
```

## 7. Questions ouvertes (avant de détailler chaque organisation)
1. Granularité : combien d'organisations *nommées* par région vs générées ?
2. Comment les territoires se chevauchent-ils (humain/surnaturel) sans contradiction ?
3. Quelle fréquence de tick pour l'évolution des relations (§4) ?
4. Quels événements d'une chaîne §5 deviennent *visibles* pour le joueur (phénomènes) — c'est le rôle de [`PHENOMENON_ENGINE.md`](PHENOMENON_ENGINE.md).
5. Persistance de tout cela entre les parties : [`WORLD_STATE.md`](WORLD_STATE.md).
