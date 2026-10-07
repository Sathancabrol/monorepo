# Prompt à coller (ArenaAI ou tout autre agent)

> Copier-coller le bloc ci-dessous dans une nouvelle session, **après avoir ouvert le dépôt `Sathancabrol/monorepo`** (le brief est dans `docs/recherche/00-BRIEF-ARENA-RECHERCHE.md`).
> Si l'agent n'a pas accès au dépôt : joindre `00-BRIEF-ARENA-RECHERCHE.md` + `02-MATRICE-DOMAINES.csv` en pièces jointes.

---

## Version courte (si l'agent a le dépôt)

```
Lis d'abord docs/recherche/00-BRIEF-ARENA-RECHERCHE.md en entier, puis
docs/recherche/02-MATRICE-DOMAINES.csv. Ce document te donne ta mission :
tu es l'agent de recherche technologique et d'architecture du projet Cognitorium.

Ta mission : produire l'inventaire critique des sources, outils et systèmes
existants nécessaires à la RÉORGANISATION COMPLÈTE de l'application, en
suivant les 10 chantiers P0 du §5.

Règles absolues :
1. Chaque candidat est vérifié par toi (dépôt officiel, LICENSE, activité,
   releases, issues) avec URL + date de consultation.
2. Aucun chiffre inventé. Si tu ne sais pas, écris « inconnu ».
3. Tu ne refais pas le travail déjà listé en §3 et en Annexe A : tu
   l'actualises et tu le corriges si c'est périmé.
4. Pour chaque domaine, tu tranches explicitement : CONSERVER / FUSIONNER /
   REMPLACER / ADAPTER / PLUGIN / RÉIMPLÉMENTER / ABANDONNER.
5. Tu privilégies ce qui tourne sur Windows, GTX 1060 (6 Go VRAM), 16 Go RAM,
   hors ligne, sans prérequis à installer, et à coût nul ou plafonné.

Livrables attendus, dans cet ordre :
1. FICHES-OUTILS.md      (format imposé au §7)
2. DECISIONS-ADR.md      (ADR-011 et suivants)
3. ARCHITECTURE-CIBLE.md (schéma, frontières, migration réversible, shell UI)
4. SYNTHESE-POUR-DECISION.md (30/90/180 jours, 10 décisions, écartés, coûts)

Commence par me dire en 10 lignes ton plan de recherche, les domaines où tu
as besoin d'un arbitrage de ma part, et ceux que tu traiteras en priorité.
Ensuite, travaille chantier par chantier, en t'appuyant sur les données
réelles du dépôt (notamment le corpus BTP de la racine et le registre
projects/watchtower/audit/).
```

---

## Version longue (si l'agent n'a PAS le dépôt)

```
Tu es un agent de recherche technologique et d'architecture. Je te confie un
brief complet (pièce jointe : 00-BRIEF-ARENA-RECHERCHE.md) et une matrice de
80 domaines (02-MATRICE-DOMAINES.csv).

Le projet est une application « local-first » (Windows, GTX 1060 6 Go VRAM,
16 Go RAM, hors ligne, budget 0-500 €/mois) qui vise à réunir :
cognition et compétences humaines, base de connaissances sourcée, monde
géographique (territoire, chantier, 3D), agents IA, recherche scientifique,
suivi de chantier BTP, simulation et aide à la décision. Il existe déjà sous
forme de 9 dépôts éclatés (documentés à l'Annexe A du brief) plus un corpus
réel de ~100 documents de chantier (CCTP, CCAP, BPU, DQE, plans, essais).

L'application doit être RÉORGANISÉE ENTIÈREMENT : nouveau shell unifié,
noyau de données commun, bus d'événements, recherche universelle, système de
plugins, et migration progressive des briques existantes.

Ta mission : chercher, vérifier, comparer et décider — pas résumer.
Suis les 10 chantiers P0 du §5 du brief et le format de sortie du §7.

Contraintes non négociables :
- Aucune affirmation sans source (URL + date de consultation).
- Aucun chiffre inventé : « inconnu » est une réponse acceptable.
- Licences vérifiées (⚠️ LICENCE) et projets abandonnés signalés (⚠️ ABANDON).
- Décision explicite par domaine : CONSERVER / FUSIONNER / REMPLACER /
  ADAPTER / PLUGIN / RÉIMPLÉMENTER / ABANDONNER.
- Compatibilité machine cible et fonctionnement hors ligne vérifiés.
- Ne jamais proposer de dépendance à un service payant non plafonnable.

Livrables : FICHES-OUTILS.md · DECISIONS-ADR.md · ARCHITECTURE-CIBLE.md ·
SYNTHESE-POUR-DECISION.md.

Commence par ton plan de recherche et les 5 questions sur lesquelles tu as
besoin de mon arbitrage avant de te lancer.
```

---

## Réglages utiles selon l'outil utilisé

| Outil | Ce qu'il faut activer |
|---|---|
| ArenaAI (ou agent avec outils web + GitHub) | Accès web + GitHub ; demander explicitement les vérifications `gh api` (licence, activité, archivage) |
| Agent avec terminal | Autoriser `git clone --depth=1` dans un dossier temporaire, jamais dans le dépôt |
| Agent sans accès web | Ne pas l'utiliser pour ce brief : sans vérification en ligne, la recherche produit des recommandations périmées (c'est précisément le problème à éviter) |

## Comment vérifier que l'agent a bien fait le travail

Trois signaux qui ne trompent pas :

1. **Il contredit le brief là où le brief a tort** (l'Annexe A dit « ne ré-auditez pas » ; s'il trouve une information périmée, il le dit).
2. **Il écrit des « inconnu »** : un agent qui remplit tous les champs invente.
3. **Il produit des décisions et des écartés**, pas une liste de liens.
