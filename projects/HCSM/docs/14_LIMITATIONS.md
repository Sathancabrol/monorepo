# 14 — Limites

**Statut du document :** auto-critique obligatoire  
**Couche :** SCIENTIFIC KNOWLEDGE  
**Version :** 0.1.0 · 2026-08-25

---

## 1. Limites de la version 0.1

1. **Pas de données.** Rien n'est estimé sur personne. Le modèle est un contrat, pas un résultat.
2. **Pas de revue systématique achevée.** L'état de l'art est une cartographie. Des antériorités peuvent manquer. La matrice de nouveauté est donc provisoire.
3. **Noyau étroit.** Six construits / modulateurs. Toute généralisation à « la cognition » est abusive.
4. **Estimateur placeholder.** La fusion bayésienne par voie est un working model, pas une contribution statistique.
5. **Document source incomplet dans ce dépôt.** Le texte Cognition Hub de 2 091 lignes n'est pas recopié ici ; l'audit porte sur le diagnostic et les formulations transmises dans le travail de repositionnement.
6. **Langue.** Documentation en français, identifiants en anglais. Un article soumissible exigera une version anglaise.
7. **Pas d'implémentation.** Les spécifications peuvent cacher des impossibilités d'ingénierie.

## 2. Limites structurelles (même après validation)

1. **Dépendance aux cadres amont.** Si le Cognitive Atlas découpe mal un construit, HCSM aligne un mauvais objet. HCSM n'est pas une machine à réviser les ontologies cognitives (Poldrack, Price & Friston, débats sur la révision ontologique).
2. **Validité écologique non garantie par le contexte déclaré.** Un champ `sleep_hours` n'est pas le sommeil.
3. **Refus vs utilité.** Un système qui refuse souvent est scientifiquement plus honnête et pratiquement moins séduisant. La pression produit-t-elle des scores.
4. **Incommensurabilité des voies.** Fusionner comportement et physiologie reste un problème ouvert. HCSM le nomme, il ne le résout pas.
5. **Personne opaque ≠ personne protégée.** Un identifiant technique ne remplace pas une gouvernance des données.
6. **Projection ICF fragile.** Les ponts construits → codes ICF sont partiels et parfois pauvres (mémoire de travail notamment).
7. **WEIRD et normes.** Toute `population_reference` reproduira les biais de la population de calibration.

## 3. Risques d'usage

Même si le dépôt interdit l'usage décisionnel, un lecteur peut :

- extraire `value` et jeter le reste ;
- vendre un « état cognitif temps réel » ;
- coller un `ConstructEstimate` sur un dossier RH, scolaire ou clinique.

Ces usages **ne sont pas HCSM**. Ils sont prévisibles. La seule mitigation documentaire est la rigidité du schéma et la répétition des interdits. Ce n'est pas suffisant.

## 4. Ce qui serait une surinterprétation de *ce* dépôt

- « HCSM a montré que l'état cognitif est un graphe. » — Non, HCSM le propose.
- « On peut maintenant mesurer l'état cognitif humain à T0. » — Non.
- « Cognition Hub remplace RDoC. » — Non.
- « L'ontologie v0.1 est une ontologie de la cognition. » — Non.

## 5. Dette scientifique assumée

| Dette | Où elle se paie |
|---|---|
| Revue de portée des modèles d'état individuel | Phase B |
| Étude de juges | Phase C |
| Estimateur réellement spécifié et comparé | `model/` v0.2+ |
| Jeux synthétiques publics de validation V1/V5 | à créer |
| Version anglaise du working paper | `papers/` |
| Alignements IRI Atlas / ICF / HPO vérifiés un par un | `ontology/` |

Tant que cette dette n'est pas payée, le statut global du projet reste `PROPOSED`.
