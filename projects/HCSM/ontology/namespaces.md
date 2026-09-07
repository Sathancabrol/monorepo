# Espaces de noms

**Statut :** `PROPOSED` · v0.1.0

## Préfixes HCSM

| Préfixe | IRI | Usage |
|---|---|---|
| `hcsm` | `https://github.com/Sathancabrol/HCSM/ontology/0.1.0#` | classes et propriétés |
| `hcsmk` | `...#knowledge/` | module knowledge |
| `hcsme` | `...#evidence/` | module evidence |
| `hcsmi` | `...#inference/` | module inference |
| `hcsmt` | `...#time/` | module time |
| `hcsmf` | `...#function/` | module function |
| `hcsma` | `...#align/` | alignements |

## Préfixes externes

| Préfixe | IRI / ressource | Rôle |
|---|---|---|
| `cogatlas` | `https://www.cognitiveatlas.org/` | construits et tâches |
| `cogpo` | Cognitive Paradigm Ontology | paradigmes |
| `rdoc` | NIMH RDoC matrix | domaines, construits, unités |
| `icf` | WHO ICF | fonctions, activités, environnement |
| `hp` | `http://purl.obolibrary.org/obo/HP_` | phénotypes |
| `prov` | `http://www.w3.org/ns/prov#` | provenance |
| `skos` | `http://www.w3.org/2004/02/skos/core#` | exactMatch / closeMatch |
| `owl` | `http://www.w3.org/2002/07/owl#` | équivalences prudentes |
| `xsd` | `http://www.w3.org/2001/XMLSchema#` | types de données |

## Politique d'alignement

- `skos:exactMatch` seulement si la portée est jugée identique.
- `skos:closeMatch` par défaut dès qu'il y a un écart (ex. working memory HCSM vs b144 ICF).
- `owl:sameAs` interdit en v0.1 entre un `Construct` HCSM et une entité externe.
- Les IRI Cognitive Atlas de type `trm_*` / `tsk_*` sont conservés tels quels dans `source_iri`.

## Identifiants locaux

```
hcsm:<module>/<class>/<slug>
```

Pas de PII, pas de nom, pas de date de naissance, pas de géolocalisation précise dans l'IRI.
