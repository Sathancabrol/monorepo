# Structure hybride : ce qui peut sortir, ce qui reste

> Principe : **un seul routeur** (OmniRoute), **un seul agent** (Hermes), **une seule mémoire**,
> **un dossier à deux étages**. Deux profils Hermes, deux périmètres : le cloud ne voit que `public\`.

---

## 1. Arborescence

```text
G:\PERSO\PROJET COGNITORIUM\
├── public\                     → versionné (dépôt privé GitHub)
│   ├── monorepo\               ← ce dépôt (clone local)
│   ├── docs\                   → specs, CARTE.md par dépôt, notes de décision
│   └── AGENTS.md               → règles pour les agents (règles 0-9 de la tour)
├── prive\                      → LOCAL UNIQUEMENT (jamais commité, jamais synchronisé)
│   ├── marche-tp\              → DCE, DQE, BPU, métrés, prix fournisseurs
│   ├── perso\                  → documents personnels
│   └── sauvegardes\            → export de `prive\` (disque que tu contrôles)
└── outils\                     → binaires/scripts d'installation (hors git)
```

Règles « versionné / pas versionné » :

| Chemin | Git | Cloud (OmniRoute ou autre palier gratuit) | Sauvegarde |
|---|---|---|---|
| `public\**` | oui (dépôt privé) | oui (aucun document sensible) | GitHub + disque |
| `prive\**` | **non** (dans `.gitignore`) | **jamais** | disque/disque externe que tu contrôles |
| `outils\**` | non | non | inutile (retéléchargeable) |
| `%USERPROFILE%\.hermes\` | **non** | **non** (identifiants, sessions, cookies) | `hermes profile export` |
| `~/.hermes/.env` | **non** | **non** | gestionnaire de secrets ou rien |

> `hermes backup` exclut déjà les arbres régénérables et **tous les magasins d'identifiants**
> (`browser-profile/`, cookies, `Login Data`) — mais ne t'en sers pas comme excuse pour
> synchroniser `~/.hermes` : il contient tes sessions et tes clés.

---

## 2. Profils Hermes (le mur, côté agent)

| Profil | Dossier de travail | Modèle | Auxiliaires | Ce qu'il peut lire |
|---|---|---|---|---|
| **défaut** | `public\` | OmniRoute (`auto`) | `auto` (= principal, gratuit) | `public\` |
| **prive** | `G:\PERSO\PROJET COGNITORIUM\prive` | Ollama local (0 cloud) | `custom:ollama-local` | tout |

```powershell
hermes profile create prive --clone
hermes -p prive config set terminal.cwd "G:\PERSO\PROJET COGNITORIUM\prive"
hermes -p prive config set model.provider "custom"
hermes -p prive config set model.base_url "http://127.0.0.1:11434/v1"
hermes -p prive config set model.default  "qwen3:4b"
hermes -p prive config set auxiliary.compression.provider "custom:ollama-local"
hermes profile list          # le profil actif est marqué d'une étoile
hermes -p prive chat         # session privée
```

`hermes project` (workspace multi-dossiers) complète le tableau sans mélanger les profils :

```powershell
hermes project create cognitorium
hermes project add-folder cognitorium "G:\PERSO\PROJET COGNITORIUM\public"
hermes project list
```

---

## 3. Le `.gitignore` de `prive\` (à poser une fois)

```gitignore
# tout est local : le dépôt ne suit rien de ce dossier
*
!.gitignore
!README.md
```

Et dans le dépôt `public\monorepo`, on garde la convention existante : `.env` ignoré,
`node_modules/`, `__pycache__/`, `venv/` hors index (déjà en place dans ce dépôt).

---

## 4. Permissions (Windows)

```powershell
# .env : toi seul
icacls "$env:USERPROFILE\.hermes\.env" /inheritance:r /grant:r "$env:USERNAME:(F)"

# dossier privé : retirer l'héritage des groupes larges
icacls "G:\PERSO\PROJET COGNITORIUM\prive" /inheritance:r /grant:r "$env:USERNAME:(OI)(CI)(F)"
```

Linux/WSL : `chmod 700` sur `prive/`, `chmod 600` sur `.env`.

---

## 5. Sauvegarde de `prive\` (sans le mettre dans le cloud)

```powershell
# miroir vers un disque que tu contrôles (lettre à adapter) :
robocopy "G:\PERSO\PROJET COGNITORIUM\prive" "E:\SAUVEGARDES\cognitorium-prive" /MIR /R:2 /W:5 /XD node_modules .git /XF *.tmp /LOG+:sauvegarde.log /TEE
```

- **Interdit** : synchroniser `prive\` vers un service grand public non chiffré (le document part
  chez un tiers, exactement ce que la structure empêche).
- Si tu veux malgré tout du hors-site : conteneur **chiffré** (outil à choisir dans
  `projects/watchtower/audit/REFERENCE.md`), jamais un dossier en clair.
- Teste la restauration **au moins une fois** : une sauvegarde jamais relue n'est pas une sauvegarde.

---

## 6. Checklist avant toute session sur un dépôt

1. `verifier-hermes.ps1` → verdict vert (Hermes + OmniRoute + Ollama).
2. Lire `CARTE.md` du dépôt (`CARTE.template.md` pour le modèle) — pas tout le code.
3. Vérifier le profil : `hermes profile list` (défaut = `public\`, `prive` = local).
4. Une tâche, un résultat écrit dans le fichier concerné, puis `/compress`.
5. `verifier-hermes.ps1 -Quota -Log` en fin de bloc de travail (calibration du quota).
