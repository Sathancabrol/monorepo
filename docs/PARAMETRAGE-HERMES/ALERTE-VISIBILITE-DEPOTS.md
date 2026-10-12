# ⚠️ ALERTE — tes dépôts GitHub sont PUBLICS et contiennent des documents privés

> Constat fait le **2026-10-12** avec ton compte (`gh` authentifié), en préparant la structure
> hybride `public\` / `prive\`. C'est **antérieur** à ce travail et indépendant de Hermes : je le
> signale parce que la question « qu'est-ce qui sort de la machine ? » a déjà une réponse, et
> qu'elle est mauvaise.

## 1. Ce qui est constaté (preuves : commandes `gh` reproductibles)

| Dépôt | Visibilité | Taille | Fichiers binaires documentaires suivis |
|---|---|---|---|
| **`monorepo`** | 🔴 **public** | 305 Mo (`size-pack`), 1818 fichiers | **268 documents (276 Mo)** + **300 images (64 Mo)** |
| **`proto-cognitorium`** | 🔴 **public** | 94 Mo | **50 documents** (dont des CV de tiers et des devis) |
| `COGNITORIUM` · `ETAT-DE-LART-PSYCHOLOGIE` · `HCSM` · `Language-decoder` · `animation-chronos` · `reaserch-engine` · `watchtower` | 🔴 public | 0,1–22 Mo | 0 (sauf 1 pptx côté état de l'art) |

Répartition exacte dans `monorepo` (comptage `git ls-files -z`, insensible aux accents) :

| Emplacement | Documents |
|---|---|
| **racine du dépôt** | **210** (dont devis, facture de situation, recours, marché, grille de salaires, plannings, DCE…) |
| `projects/proto-cognitorium/raw/` | 56 (+ 5 images) |
| `projects/ETAT-DE-LART-PSYCHOLOGIE/` | 1 pptx (ta présentation — à conserver) |
| `docs/synthese-talbot-2026/` | 1 docx (ta synthèse — à conserver) |

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
| Salaires / RH | `salaire_minima_hierarchiques_occitanie_2022_0.pdf`, `CHANTIER EN COURS-Nathan (2).xlsx` |
| Images de terrain (racine) | `satellite.PNG`, `satellite 85.PNG`, `streetview.PNG`, `aret.jpeg`, `essai hydraulique.JPG` |
| **Données personnelles de tiers** (`projects/proto-cognitorium/raw/`) | **CV** de plusieurs personnes (Gianni, Amélie Cruagnes, Benoit Bonnamant, Pierre DENIAUD), questionnaires d'information, rapport de stage, mémoires TER |

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

Procédure complète, mesurée et testée : **`PURGE-HISTORIQUE.md`**. En résumé, avec l'outil fourni :

```bash
bash scripts/purger-documents-git.sh --inventaire    # reconnaissance, lecture seule
bash scripts/purger-documents-git.sh --plan          # ce que les motifs retireraient réellement
pip install git-filter-repo
bash scripts/purger-documents-git.sh --executer --sortie "G:/PERSO/purge-2026-10-12"
# → imprime la commande de publication ; il ne pousse rien tout seul
```

- Le script travaille sur un **clone miroir** : ton clone de travail n'est pas modifié.
- Les motifs vivent dans `docs/PURGE-MOTIFS.txt` (zone A = CV/données de tiers, zone B = les
  210 documents de la racine, zone C = images, à décommenter).
- La publication (`push --mirror`) puis le **re-clone de chaque machine** et le ticket
  **GitHub Support « removal of cached views »** restent à ta main (voir `PURGE-HISTORIQUE.md` § 3-5).
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
