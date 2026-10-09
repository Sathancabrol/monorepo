# Sources, outils et données — recensement du 9 octobre 2026

**Objet.** Un balayage des 9 dépôts a révélé un ensemble de documents déjà
présents dans le monorepo et jamais exploités par Carré d'As. Ce fichier est
l'index qui évite de les perdre une deuxième fois.

**Règle appliquée partout** (celle de la branche `feat/tool-data-catalog-2026-10`) :
**référencer → adapter → normaliser → extraire**. On ne recopie jamais. On lit
là où c'est, ou on branche un adaptateur. Aucune divergence possible.

---

## 1. Ce qui a été intégré à Carré d'As

| Source trouvée | Ce que c'est | Intégration |
|---|---|---|
| `projects/watchtower/audit/reference/REGISTRE-OUTILS.json` | 86 outils, 25 besoins, 12 catégories, commandes d'installation et de vérification | `carredas/modules/osint/registries.py` — lu sur place, normalisé, servi avec le registre local. **120 outils** au total. |
| `projects/watchtower/docs/SOURCES-FR.md` | Sources françaises classées 🟢 libre / 🟡 compte / 🔴 payant | `carredas/modules/watchtower/data/sources.json` — 34 sources avec licence, accès, URL, attribution |
| `projects/watchtower/DATA_SOURCES.md` | Sources live + registre de risque de licence (OpenSky et TeleGeography *non commercial*) | `sources.json`, champ `usage` : oui / condition / **non** |
| `projects/HCSM/specs/data-schema.md` | Contrat V1 avec validateur implémenté (`projects/HCSM/validator/`) : 9 règles de rejet | `carredas/core/admissibilite.py` — 6 règles transposées |
| `core/contracts/canonical-record.schema.json` (branche `feat/tool-data-catalog-2026-10`) | Modèle canonique à 15 champs | `carredas/core/canonical.py` + schémas publiés |
| `projects/reaserch-engine/schemas/source.schema.json` | Schéma de source avec `source_id`, `provenance`, `quality` | Référencé ; le contrat canonique en tient compte |

---

## 2. Ce qui reste à exploiter (documenté, non intégré)

Ces documents existent et sont bons. Ils n'ont pas encore été branchés parce
qu'ils décrivent un chantier plus large que ce que le 16 octobre exige.

| Fichier | Lignes | Intérêt |
|---|---|---|
| `projects/watchtower/audit/REFERENCE.md` | 1801 | La « source de vérité pour les agents » derrière les 86 outils. Règles d'ingénierie, 3 paliers matériels, index par besoin. |
| `projects/watchtower/audit/CAPACITES-AGENT.md` | 62 | **25 tâches** avec taux d'automatisation, livrable, coût et ce qui reste obligatoirement humain. C'est le cahier des charges du système agentique. |
| `projects/watchtower/audit/RND-PROPOSITIONS-2026.md` | 399 | 12 diagnostics, 6 chantiers, gabarits, 14 tâches calibrées, **10 anti-patterns** (« les dix pièges où ce genre de projet meurt ») |
| `projects/watchtower/audit/COUTS-LICENCES-LEGAL.md` | 68 | L'ardoise honnête : **0 €/mois** tout compris, et les seuls coûts réels |
| `projects/watchtower/audit/CATALOGUE-OUTILS.md` | 118 | Le catalogue d'outils en prose, section H = les 4 briques « Jarvis » à piocher sans cloner |
| `projects/watchtower/audit/stack/` | — | `docker-compose.yml` + `install-stack.ps1/.sh` + `gen-secrets.sh` : la pile complète déjà écrite |
| `projects/watchtower/audit/reference/{cherche,doctor,generate-reference}.py` | — | Trois outils exécutables : chercher dans le registre, constater l'état réel, régénérer |
| `projects/COGNITORIUM/watchtower-mods/src/osint/osintRegistry.js` | — | Registre OSINT en JS (branche `watchtower/osint-workbench-v0.1`) |
| `projects/HCSM/validator/` | — | Validateur V1 forme + V5 admissibilité, réellement implémenté |

---

## 3. Le point le plus sensible pour le 16 octobre

Quatre sources sont **écartées pour un usage collectivité**, et il fallait le
savoir avant de les montrer :

| Source | Licence | Pourquoi |
|---|---|---|
| OpenSky Network | recherche/éducation **non commercial** | Un usage opérationnel peut exiger un accord écrit, **même associatif ou de collectivité** |
| Google News RSS | ToS Google : **usage personnel non commercial** | À remplacer par GDELT, qui autorise l'usage commercial avec citation |
| TeleGeography (câbles sous-marins) | CC BY-**NC**-SA 3.0 | Clause NonCommercial. Dossier autonome : le reste tourne sans. |
| Google Photorealistic 3D Tiles | propriétaire, payant | Les tuiles ne peuvent être ni mises en cache ni stockées ; usage live uniquement |

`GET /api/carto/sources?usage=oui` renvoie les 14 sources sans restriction.
C'est la liste à utiliser pour une présentation publique.

---

## 4. Les six règles d'admissibilité

Deux niveaux distincts, et c'est tout l'intérêt :

- **`valider()`** vérifie la **forme** — l'enregistrement est-il bien construit ?
- **`admissible()`** vérifie le **droit** — a-t-on le droit de présenter ça comme un fait ?

Une estimation et un chiffre nu passent la forme et sont bloqués au droit. Les
règles viennent de `projects/HCSM/specs/data-schema.md` (contrat V1) et de
l'anti-pattern n°7 de `RND-PROPOSITIONS-2026.md` : « la tour doit afficher
*pourquoi* elle n'est pas sûre, sinon elle devient une machine à convictions. »

| Règle | Gravité | Refuse |
|---|---|---|
| `fait_sans_source` | bloquant | un fait sans source |
| `fait_estime` | bloquant | une estimation présentée comme une observation |
| `score_nu` | bloquant | un nombre sans unité |
| `donnee_personnelle` | bloquant | courriel, téléphone, n° de sécurité sociale, IBAN, carte bancaire |
| `inference_sans_base` | bloquant | une hypothèse qui ne dit pas d'où elle vient |
| `incertitude_non_expliquee` | signalement | un statut « inconnu » qui n'explique pas pourquoi |

---

## 5. Commandes

```bash
python3 main.py --serve                          # lancer
python3 scripts/test-carre-d-as.py               # scénario complet
curl -s localhost:8733/api/carto/sources | jq    # les 34 sources
curl -s 'localhost:8733/api/carto/sources?usage=oui' | jq
curl -s localhost:8733/api/osint/registres | jq  # les 120 outils
curl -s localhost:8733/api/canonique/admissibilite | jq
```
