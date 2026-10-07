# Contrat de module — Carré d'As (plug in / plug out)

**Statut :** `PROPOSED` — spécification, aucune implémentation.
**Base :** prolonge `core/contracts/module.schema.json` et `data/module_registry.json` créés sur la branche `feat/tool-data-catalog-2026-10`, plus les constats de `projects/watchtower/audit/RND-PROPOSITIONS-2026.md` (registre implicite, état diffus, absence de bus, clés côté navigateur).

---

## 1. Pourquoi un contrat

Le projet a déjà vécu le problème deux fois :
- **Watchtower** : ≈100 modules qui s'auto-déclarent (`window.WT.*`), sans registre → un module cassé est invisible jusqu'au clic ;
- **le monorepo** : 8 projets qui ne se parlent pas, 3 bases de connaissances concurrentes, un `localStorage` par application.

Le contrat de module est la réponse structurelle : **le shell ne connaît pas les modules, il connaît le contrat**. Ajouter, retirer ou remplacer un module ne doit pas toucher au shell ni aux autres modules.

## 2. Anatomie d'un module

```
modules/chantier/
├─ module.json          manifeste (contrat, lisible par la machine)
├─ README.md            ce que fait le module, comment l'utiliser, limites
├─ LICENCE              licence propre si différente du cœur
├─ ui/                  interface déclarée (points d'extension)
├─ core/                logique métier
├─ data/                schémas, migrations, jeux de référence embarqués
├─ tests/               tests du module (obligatoires)
└─ docs/                décisions locales, dette, feuille de route du module
```

Un module **ne se déclare pas tout seul dans le shell** : il est **découvert par le registre**, qui lit `module.json`.

## 3. Le manifeste (`module.json`)

Extension du schéma existant (`module.schema.json`) avec ce qui manque pour le plug in/out réel.

```jsonc
{
  "id": "chantier",
  "name": "Chantier BTP / TP",
  "version": "1.0.0",
  "coreVersion": ">=1.0 <2.0",          // compatibilité : refus explicite sinon
  "domain": "btp",
  "kind": "embedded",                    // embedded | service | wasm | adapter | external
  "status": "active",                    // active | prototype | planned | deprecated
  "entrypoint": "core/index.js",         // ce que le shell charge
  "ui": { "panels": ["chantier.dashboard", "chantier.documents"], "routes": ["/chantier"] },
  "capabilities": ["dce", "bpu", "dqe", "metre", "planning", "qualite", "doe"],
  "permissions": {                       // rien n'est accordé par défaut
    "files.read":  ["${PROJECT_DIR}/**"],
    "files.write": ["${MODULE_DATA}/**"],
    "network":     ["gouv.fr", "googleapis.com"],
    "execute":     [],
    "accounts":    ["google"]
  },
  "events": {
    "consumes": ["document.indexed", "project.created"],
    "produces": ["chantier.lot.created", "chantier.ecart.detected"]
  },
  "owns": ["chantier", "lot", "metre", "prix_unitaire", "non_conformite"],
  "reads": ["document", "place", "project", "agent"],
  "dependsOn": ["documents", "carte"],
  "provides": { "sql": "data/migrations/*.sql", "seeds": "data/reference/*.json" },
  "license": "Apache-2.0",
  "source": { "repo": "self", "path": "modules/chantier" }
}
```

**Règles de validation (bloquantes) :**

1. `id` unique, en minuscules, sans espace.
2. `coreVersion` incompatible → le module est **refusé** avec un message lisible (pas d'échec silencieux).
3. Toute permission utilisée doit être déclarée ; toute permission déclarée doit être justifiée dans le README.
4. Toute entité dans `owns` ne peut être possédée que par **un seul** module installé (détection de conflit au chargement).
5. Tout événement produit doit exister dans le schéma d'événements du cœur, ou être déclaré en extension.
6. `tests/` non vide et exécutable par la Quality Gate.

## 4. Cycle de vie (ce que « plug in/out » veut dire)

```
découverte → validation → installation → activation → exécution → désactivation → désinstallation
   (scan)      (contrat)     (copie)      (chargement)   (runtime)    (décharge)      (purge)
```

| Étape | Exigence | Vérification |
|---|---|---|
| **Découverte** | le shell scanne `modules/` + les modules installés par l'utilisateur ; aucun code exécuté à ce stade | liste affichée avec version, source, statut |
| **Validation** | manifeste conforme, `coreVersion` compatible, permissions listées, conflits d'entités détectés | rapport d'installation **avant** toute exécution |
| **Installation** | copie isolée, migrations de données du module, aucune écriture hors de son périmètre | journal d'installation |
| **Activation** | chargement du module, enregistrement des capacités et des vues, abonnements aux événements | **≤ 300 ms**, sans recharger l'application |
| **Désactivation** | désabonnement, purge mémoire, fermeture des vues ; **les données du module sont conservées** | l'app reste utilisable sans le module |
| **Désinstallation** | suppression du code ; les données sont **proposées** à l'export avant purge | confirmation explicite, jamais de perte silencieuse |
| **Échec** | un module qui lève est **désactivé isolément** ; le shell continue et affiche un bandeau | « 1 module sur 6 n'a pas démarré — voir Diagnostic » |

**Critère d'acceptation V1 :** un module factice s'installe, s'active, se désactive et se désinstalle **sans redémarrer** l'application, avec ses données intactes après désactivation.

## 5. Communication : bus d'événements, pas d'appels directs

**Interdit :** un module qui importe le code d'un autre module.
**Autorisé :** un module qui **publie** un événement, ou **appelle une capacité** déclarée dans le registre.

```jsonc
// Événement (schéma versionné, immuable, journalisé)
{
  "id": "evt_01H...",
  "type": "document.indexed",
  "version": 1,
  "at": "2026-10-07T12:34:56Z",
  "origin": "documents",
  "project": "proj_barbazan",
  "payload": { "documentId": "doc_42", "pages": 12, "source": "dqe.pdf" },
  "trace": { "correlationId": "c_88", "actor": "user|agent:researcher" }
}
```

Règles :
- un événement **ne se modifie jamais** (nouvelle version si le format change) ;
- les 500 derniers événements sont consultables (mode diagnostic + timeline) ;
- un événement peut être **rejoué** en mode simulation pour tester un module ;
- toute écriture de donnée passe par une commande du module propriétaire, jamais par une écriture directe dans la base d'un autre.

## 6. Permissions : « rien par défaut »

Modèle inspiré des navigateurs et de WASI :

| Permission | Portée | Exemple de refus |
|---|---|---|
| `files.read` / `files.write` | chemins explicites (`${PROJECT_DIR}`, `${MODULE_DATA}`, `${TEMP}`) | un module de carte ne lit pas les CV |
| `network` | liste de domaines | un module d'étude de prix ne parle pas à un service inconnu |
| `execute` | liste de binaires autorisés | photogrammétrie : `odm` uniquement |
| `accounts` | fournisseurs autorisés | un module BTP n'accède pas au compte Google pour lire les mails |
| `notifications` | oui/non | — |
| `clipboard` | oui/non | — |

- Toute utilisation est **journalisée** (qui, quand, quoi) et consultable dans Diagnostic.
- Une permission demandée à l'exécution alors qu'elle n'est pas déclarée **échoue** et remonte une erreur explicite.
- Les modules **tiers** s'exécutent en **WebAssembly** (sandbox WASI/Extism) : pas d'accès au système hors des hôtes fournis par le shell.

## 7. Interface : points d'extension, pas de HTML libre

Un module ne décrit pas son interface par du HTML arbitraire — il **déclare** des éléments que le shell rend avec son propre design system :

| Point d'extension | Ce que le module fournit | Ce que le shell garantit |
|---|---|---|
| `panels` | titre, icône, composants, état | cadre, taille, accessibilité, thème |
| `routes` | chemins, titre, garde d'accès | navigation, fil d'Ariane |
| `commands` | commandes pour le Ctrl+K (verbe, cible, portée) | recherche, raccourcis, historique |
| `cards` | résumé sur l'accueil (titre, 3 chiffres, action) | grille, position, cohérence |
| `notifications` | types d'alerte, priorité | centre de notifications, regroupement |
| `settings` | schéma de préférences | formulaire, validation, persistance |
| `imports/exports` | formats acceptés/produits | glisser-déposer, dialogues, progression |

**Conséquence :** un module n'a pas besoin de connaître le CSS ni le framework du shell — et le shell peut changer de framework sans casser les modules. C'est le point qui rend la V1 maintenable.

## 8. Données : un propriétaire, des lecteurs

| Règle | Exemple |
|---|---|
| **Un seul module écrit** une entité | `chantier` écrit `metre` ; `documents` ne fait que le lire |
| Les entités communes viennent du **cœur** | `project`, `document`, `place`, `event`, `agent`, `user` |
| Toute entité porte le **socle épistémique** | provenance, confiance, date d'observation, statut (`fact`/`inference`/`hypothesis`/`unknown`), licence |
| Les migrations sont **versionnées par module** | `data/migrations/001_init.sql`, appliquées à l'installation |
| L'export est **toujours possible** | un dossier lisible (JSON/SQLite/CSV + fichiers) même sans l'application |

Modèle canonique minimal (prolonge `canonical-record.schema.json` de la branche) : `id, type, label, source, source_url, retrieved_at, observed_at, valid_from, valid_to, geometry, provenance, confidence, license, status, relations`.

## 9. Versionnement et compatibilité

| Version | Règle |
|---|---|
| **Cœur** (`coreVersion`) | SemVer ; une rupture majeure force une compatibilité explicite ou une migration documentée |
| **Module** | SemVer indépendant ; le manifeste déclare la plage de cœurs supportée |
| **Événements** | versionnés individuellement, jamais modifiés après publication |
| **Manifeste** | son schéma est lui-même versionné (`$schema`) |
| **Dépréciation** | un module `deprecated` reste installable 2 versions du cœur, avec avertissement |

## 10. Qualité : ce qu'un module doit fournir pour être accepté

| Exigence | Seuil |
|---|---|
| Tests | au moins un test d'installation/activation + tests métier ; exécutables par la Quality Gate |
| Documentation | `README.md` (usage, limites, permissions) + décisions locales |
| Licence | déclarée, compatible avec la matrice de licences du projet |
| Performances | budget déclaré (mémoire cible, temps de démarrage) et mesuré |
| Accessibilité | les composants déclarés passent l'audit automatisé du shell |
| Sécurité | aucune clé en clair, aucun accès hors périmètre, journalisation des accès sensibles |
| Internationalisation | tous les textes externalisés (FR d'abord, EN ensuite) |
| Désinstallation | propre : code supprimé, données conservées ou exportées, aucune trace ailleurs |

## 11. Modules internes et modules tiers : deux régimes

| | **Module interne** (fait par l'équipe) | **Module tiers** (contributeur, partenariat) |
|---|---|---|
| Exécution | processus du shell (JS/TS) ou service local | **WASM sandboxé** |
| API | complète (SDK interne) | sous-ensemble stable du SDK |
| Publication | dans `modules/` | paquet signé, registre local |
| Mise à jour | avec l'application | indépendante, avec compatibilité vérifiée |
| Accès aux données | selon propriété déclarée | uniquement les capacités exposées |

> Principe de cohérence : **l'équipe utilise le même contrat que les tiers** (dogfooding). Si un module interne a besoin d'une porte dérobée, c'est le contrat qui est incomplet.

## 12. Migration depuis l'existant

| Existant | Voie de migration |
|---|---|
| `projects/watchtower` (≈100 modules, JS global, CSS global) | **adaptateur** puis découpage progressif : d'abord une seule « application hébergée » (iframe ou route dédiée), puis extraction module par module selon le contrat. Ne pas réécrire : mesurer (366 `getElementById`, 866 `querySelector`, 162 `window.__godsEyeView`) et extraire à la demande |
| `nexus_os/` (Python, complet) | module `agents` en `kind: "service"` (processus local supervisé), interface déclarée |
| `projects/btp-conduite-travaux/` | module `chantier` : reprise des données, des rapports et du dashboard |
| `projects/frontignan`, `projects/ETAT-DE-LART-…`, `projects/HCSM`, `projects/reaserch-engine` | adaptateurs puis modules (territoire, cognition, recherche) |
| `projects/COGNITORIUM/learning` | module `learning` (v2), données à migrer vers le schéma canonique |
| `app/` (FastAPI + Jinja actuel) | **déprécié** : sert de référence pour l'API du shell, puis retiré |

## 13. Critères d'acceptation du contrat (V1)

1. Un module peut être **ajouté** (nouveau dossier + manifeste) sans modifier une ligne du shell.
2. Un module peut être **retiré** sans casser les autres ; ses données survivent ou sont exportées.
3. Un module **défaillant** est isolé, signalé, et n'empêche pas l'application de fonctionner.
4. Un module déclare et obtient **uniquement** les permissions dont il a besoin.
5. Deux modules **ne peuvent pas** posséder la même entité.
6. L'interface d'un module est rendue par le shell (design system unique, accessibilité garantie).
7. Un module tiers s'exécute **sans accès** au système au-delà de ses permissions.
8. `carré-das --check` (ou l'équivalent) valide le manifeste, les permissions, les conflits et les tests **avant** installation.
