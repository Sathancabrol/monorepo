# ⚠️ ALERTE — tes dépôts GitHub sont PUBLICS et contiennent des documents privés

> Constat fait le **2026-10-12** avec ton compte (`gh` authentifié), en préparant la structure
> hybride `public\` / `prive\`. C'est **antérieur** à ce travail et indépendant de Hermes : je le
> signale parce que la question « qu'est-ce qui sort de la machine ? » a déjà une réponse, et
> qu'elle est mauvaise.

## 1. Ce qui est constaté (preuves : commandes `gh` reproductibles)

| Dépôt | Visibilité | Taille | Fichiers bureautiques suivis |
|---|---|---|---|
| **`monorepo`** | 🔴 **public** | 335 Mo | **480** (PDF, XLS/XLSX, DOC, PPT, RTF, images) |
| **`proto-cognitorium`** | 🔴 **public** | 94 Mo | **50** (dont des CV de tiers et des devis) |
| `COGNITORIUM` · `ETAT-DE-LART-PSYCHOLOGIE` · `HCSM` · `Language-decoder` · `animation-chronos` · `reaserch-engine` · `watchtower` | 🔴 public | 0,1–22 Mo | 0 (sauf 1 pptx côté état de l'art) |

Contrôle : `gh api repos/Sathancabrol/monorepo --jq .visibility` → `public`.

**Bonnes nouvelles, à garder en tête pour doser l'urgence**
- `forks = 0`, `stars = 0`, `watchers = 0` sur `monorepo` : **aucun miroir connu**, la mise en privé
  est donc efficace pour l'essentiel.
- **Aucun secret** trouvé dans les fichiers suivis (`git grep` sur `sk-…`, `ghp_…`, `AIza…`, `AKIA…`,
  clés privées PEM → zéro résultat) et aucun `.env` suivi (seulement des `.env.example`).
- Le problème est **documentaire et personnel**, pas un vol de clés.

## 2. Ce que ça expose concrètement

| Catégorie | Exemples présents dans l'historique suivi |
|---|---|
| Marchés / chantiers TP | DCE, CCAP, CCTP, BPU, DQE, métrés, devis d'entreprise (`23-LGPM-044_LABASTIDE D'ANJOU_DEVIS EXE ENTREPRISE`), factures de situation |
| Litiges | `Recours Barbazan.docx/.pdf`, comptes-rendus de réunion n°1→n°9 |
| Salaires / RH | `salaire_minima_hierarchiques_occitanie_2022_0.pdf`, `chantier en cours-Nathan` |
| **Données personnelles de tiers** (`proto-cognitorium/raw/`) | **CV** de plusieurs personnes (Gianni, Amélie Cruagnes, Benoit Bonnamant, Pierre DENIAUD), questionnaires d'information, rapport de stage, mémoires TER |

Les CV et questionnaires de tiers relèvent de données personnelles : publiés, ils te mettent en
situation de non-conformité, et toute personne concernée qui demanderait leur suppression y a droit.
C'est le point le plus sérieux du lot.

## 3. Plan de remédiation (dans l'ordre, du plus urgent au plus complet)

### Étape A — Stopper l'exposition (2 min, réversible)

```bash
gh repo edit Sathancabrol/monorepo          --visibility private --accept-visibility-change-consequences
gh repo edit Sathancabrol/proto-cognitorium --visibility private --accept-visibility-change-consequences
# au choix, par cohérence :
for r in COGNITORIUM ETAT-DE-LART-PSYCHOLOGIE HCSM Language-decoder animation-chronos reaserch-engine watchtower; do
  gh repo edit "Sathancabrol/$r" --visibility private --accept-visibility-change-consequences
done

# vérifier
gh api repos/Sathancabrol/monorepo --jq .visibility      # → private
```

⚠️ Passer en privé **empêche les accès futurs** mais ne supprime pas ce qui a déjà été aspiré
(caches, robots, éventuels clones). C'est un pansement immédiat, pas une gomme.

### Étape B — Décider la cible (10 min)

| Option | Pour qui | Conséquence |
|---|---|---|
| **Tout privé** | le plus simple ici | tu ne partages rien de public pour l'instant ; aucun coût |
| **Code public / documents privés** | si tu veux publier un projet | il faut sortir les documents de **l'historique**, pas seulement de l'index (étape C), et déplacer le reste dans `prive\` |
| Garder tel quel | — | **non** : CV de tiers + devis d'entreprise publics |

### Étape C — Purger l'historique (si l'objectif est la suppression réelle)

```bash
pip install git-filter-repo
cp -r monorepo monorepo-backup                # copie de sûreté AVANT toute réécriture
cd monorepo
git filter-repo --path-glob '*.pdf' --path-glob '*.xls' --path-glob '*.xlsx' \
                --path-glob '*.doc' --path-glob '*.docx' --path-glob '*.ppt' --path-glob '*.pptx' \
                --path-glob '*.rtf' --invert-paths
git push --force --tags                      # réécrit tout : à faire seul, sans collaborateur
```

- La réécriture **change tous les SHA** : trousseaux, CI, liens d'issues et copies locales deviennent
  caducs. À faire sur une copie, jamais sur l'unique exemplaire.
- Ensuite, ouvre un ticket **GitHub Support** (« removal of cached views ») en donnant le dépôt et
  les SHA concernés : GitHub peut purger le cache des vues des commits devenus inaccessibles.
- Si une personne concernée demande la suppression → même procédure, et c'est la réponse à lui faire.

### Étape D — Empêcher la récidive (5 min, automatique)

Un garde-fou est fourni dans ce dépôt : `scripts/garde-fou-donnees.sh`.
Il **refuse** un commit qui ajoute un PDF/office/image hors des dossiers de documentation autorisés.

```bash
# installation (une fois par clone)
cp scripts/garde-fou-donnees.sh .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit

# autoriser volontairement un fichier (rare) : l'ajouter à docs/PUBLIC-AUTORISE.txt
```

Complété par les règles déjà écrites dans `STRUCTURE-HYBRIDE.md` :
`prive\` n'est **jamais** dans un dépôt ; la documentation qui doit être versionnée vit sous
`docs/` et `projects/*/docs/` ; un document tiers (CV, questionnaire, devis) ne rentre **jamais**
dans git, même dans un dépôt privé — il va dans `prive\`.

## 4. À retenir pour le montage Hermes

Cette alerte ne change pas le plan mais **renforce la règle de routage** : tant que ces documents sont
quelque part dans un dépôt ou un dossier synchronisé, ils sont accessibles à tout outil qui lit ce
dossier. D'où l'ordre correct : **d'abord** `prive\` hors de tout dépôt et hors de tout cloud,
**ensuite** OmniRoute/Hermes sur `public\` seul (`ROUTAGE.md`, règle n°1).
