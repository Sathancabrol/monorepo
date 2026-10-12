# Purge d'historique — sortir les documents de git pour de bon

> Tu as choisi d'organiser la purge **avant** de toucher à la visibilité. C'est cohérent, mais
> une précision utile : **rendre privé n'empêche rien de la purge** et c'est réversible.
> Tu peux donc passer en privé d'abord (2 min, ça coupe l'accès tout de suite) et faire la
> réécriture ensuite tranquillement — les deux opérations sont indépendantes dans les deux sens.

## Ce que « supprimer » veut dire ici

| Action | Effet réel |
|---|---|
| Supprimer le fichier dans un commit | ❌ il reste dans l'historique, accessible par son SHA |
| Passer le dépôt en privé | 🟡 coupe l'accès futur ; ne retire rien de l'historique |
| Réécrire l'historique (filter-repo) + force-push | ✅ les commits ne contiennent plus les fichiers (nouveaux SHA) |
| Ticket GitHub Support « removal of cached views » | ✅ demande la purge des vues en cache des commits devenus inaccessibles |
| Rotation de secrets | à faire **seulement** si un secret a fuité — ici : aucun trouvé |

Ce qui est déjà sorti du périmètre (robots, caches tiers, clones) n'est jamais rattrapable :
d'où l'intérêt d'agir tôt et de traiter le cas des **données personnelles de tiers** en priorité.

## Périmètre mesuré dans `monorepo` (2026-10-12)

| Zone | Contenu | Volume |
|---|---|---|
| **A** | `projects/proto-cognitorium/raw/**` — CV de personnes, questionnaires, devis, mémoires | 61 fichiers |
| **B** | documents à la **racine** — DCE, CCAP/CCTP, BPU, DQE, métrés, devis, factures, recours, plannings, salaires, guides | **210 fichiers · 276 Mo** |
| **C** | 10 images de la racine (satellite, streetview, arrêtés, essai hydraulique) | 10 fichiers |
| total dépôt | 1818 fichiers suivis, dont 268 documents + 300 images | `size-pack` ≈ **305 Mo** |

Zones A et B sont actives dans `docs/PURGE-MOTIFS.txt` (le script les lit) ; la zone C est
prête à décommenter. Les documents qui **restent** volontairement : `docs/synthese-talbot-2026/`,
`Cognition_Distribuee_2025.pptx`, les `projects/*/figures|visuals|docs/`, les textures CesiumJS.

## Procédure (dans cet ordre)

### 0. Copier ce qu'on garde, AVANT tout

La purge travaille sur un clone miroir : ton arbre de travail n'est pas modifié. Mais après le
`force-push`, un **re-clone** ne contiendra plus ces fichiers. Donc :

```powershell
robocopy "G:\PERSO\PROJET COGNITORIUM\monorepo" "G:\PERSO\PROJET COGNITORIUM\prive\monorepo-documents" `
  *.pdf *.xls *.xlsx *.xlsm *.doc *.docx *.ppt *.pptx *.rtf /S /XD node_modules .git .venv dist
```

### 1. Reconnaissance et plan (lecture seule, rien n'est modifié)

```bash
bash scripts/purger-documents-git.sh --inventaire     # ce qui existe, par dossier
bash scripts/purger-documents-git.sh --plan           # ce que les motifs ACTIFS retireraient
```

`--plan` affiche la liste, le nombre de chemins et la commande exacte qui serait lancée.

### 2. Réécriture sur un clone miroir

```bash
pip install git-filter-repo
bash scripts/purger-documents-git.sh --executer --sortie "G:/PERSO/purge-2026-10-12"
```

- ton clone de travail n'est **pas** touché ;
- le script imprime la taille avant/après et vérifie qu'il ne reste **aucun** chemin visé ;
- **il ne pousse rien** : il te donne la commande de publication.

### 3. Publier (seul à pousser, personne d'autre ne doit travailler sur le dépôt)

```bash
git -C "G:/PERSO/purge-2026-10-12/depot-mirror.git" remote add origin git@github.com:Sathancabrol/monorepo.git
git -C "G:/PERSO/purge-2026-10-12/depot-mirror.git" push --mirror origin
```

À faire aussi pour `proto-cognitorium` (mêmes motifs, `docs/PURGE-MOTIFS.txt` s'applique :
`projects/*/raw/*` y est la racine `raw/`, ajoute `glob:raw/*` si le fichier de motifs est
utilisé tel quel depuis ce dépôt).

### 4. Nettoyer les autres copies

**Tout clone existant contient encore les documents** — c'est le piège classique :

| Où | Quoi faire |
|---|---|
| Ton PC (`G:\...`) — le clone de travail | supprimer le dossier et **re-cloner** (pas de `git pull`) |
| Tes autres machines / disques | idem |
| Ce dépôt dans Arena (agent) | l'agent retirera les gros artefacts ou repartira d'un clone propre |
| Github Actions / CI, fork, zip téléchargé | supprimer ou régénérer |

### 5. Faire purger les caches côté GitHub

Ticket **GitHub Support** → « removal of cached views », en donnant : le dépôt, les chemins
concernés, et les SHA (le support sait retrouver les commits devenus inaccessibles après
force-push). C'est l'étape qui couvre les vues mises en cache par GitHub.

### 6. Empêcher la récidive

```bash
cp scripts/garde-fou-donnees.sh .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
```

Le hook refuse tout ajout de PDF/office/image hors des zones de documentation autorisées
(`docs/`, `projects/*/docs|audit|figures|visuals/`), avec exceptions explicites dans
`docs/PUBLIC-AUTORISE.txt`. Complément utile : ajouter le même fichier `.gitattributes`
ou la même consigne dans `AGENTS.md` pour les autres agents.

### 7. Décider la visibilité **après**

- Recommandation : **privé** pour `monorepo` et `proto-cognitorium` (les documents de marché et les
  CV n'ont rien à faire dans un dépôt public, même purgés).
- Si tu tiens à publier du code : crée un dépôt **nouveau**, dédié, sans historique — et laisse
  l'ancien privé. Réutiliser un historique purgé pour repartir en public est un mauvais pari.

## Économie mesurable

Indépendamment du privé : `monorepo` pèse **305 Mo** de `size-pack` pour ~1800 fichiers dont
**276 Mo de documents** qui n'ont rien à faire là. Après purge, le dépôt retombe à quelques
dizaines de Mo — clone plus rapide sur chaque machine, sauvegardes plus légères, et plus rien
de sensible à la racine à se demander s'il faut l'envoyer à un palier gratuit.
