# Paramétrage Hermes — finir le montage maintenant

> **Objectif** : Hermes répond **gratuitement** (OmniRoute + Ollama local), le quota payant
> (Codex / ChatGPT) est **réservé au travail difficile**, et rien de sensible ne sort de la machine.
>
> **Statut** : ce dossier est un **kit d'exécution**. Je n'ai pas accès à ton PC : l'étape 0
> (5 min) produit l'état réel, les étapes 1→7 sont dans l'ordre de rentabilité.
> Tout ce qui est écrit ici vient des dépôts **Hermes Agent** (`cli-config.yaml.example`,
> `website/docs/`) et **OmniRoute** (`README.md`, `docs/`) lus le 2026-10-12 — pas de mémoire.

---

## 🔴 Avant tout le reste : deux dépôts sont publics

Vérifié avec ton compte le 2026-10-12 : `Sathancabrol/monorepo` (**public**, 335 Mo) contient
**480 fichiers bureautiques suivis** (DCE, CCAP/CCTP, BPQ, DQE, métrés, devis d'entreprise,
factures de situation, recours, grilles de salaires) et `Sathancabrol/proto-cognitorium`
(**public**, 94 Mo) en contient 50, dont des **CV de tiers** et des questionnaires.
Aucun secret ni `.env` exposé (vérifié), et **0 fork / 0 star** sur `monorepo`.

→ Détail, preuves reproductibles et plan de remédiation : **`ALERTE-VISIBILITE-DEPOTS.md`**
(3 commandes pour passer en privé, puis purge d'historique si la suppression réelle est visée,
puis garde-fou `scripts/garde-fou-donnees.sh` pour ne pas récidiver).

C'est cohérent avec le reste de ce kit : ce sont **les mêmes documents** que la règle n°1 de
`ROUTAGE.md` interdit d'envoyer à un palier gratuit. L'ordre correct est donc :
**1)** ces documents hors de tout dépôt et hors de tout cloud, **2)** ensuite OmniRoute/Hermes
sur `public\` seul.

---

## Fichiers de ce dossier

| Fichier | Rôle | Quand l'utiliser |
|---|---|---|
| `README.md` | le plan d'action ordonné (ce fichier) | maintenant, puis à chaque reprise |
| `verifier-hermes.ps1` / `.sh` | état des lieux + `hermes doctor` + ports + quota (exit 0/1) | étape 0, puis avant/après chaque install |
| `config.hermes.extrait.yaml` | extrait de config à fusionner (OmniRoute, Ollama, fallback, aux) | étape 2 et 4 |
| `ROUTAGE.md` | la règle de routage manuelle + l'hygiène de requête | en continu |
| `STRUCTURE-HYBRIDE.md` | arborescence `public\` / `prive\`, sauvegarde, profils | étape 5 |
| `CARTE.template.md` | carte d'un dépôt (1 fichier par dépôt, lu en début de session) | étape 5 |
| `CARTE.monorepo.md` | exemple déjà rempli pour **ce** dépôt | tout de suite |
| `quota-log.csv` | journal de calibration du quota (créé par le script avec `-Log`) | en continu |
| `ALERTE-VISIBILITE-DEPOTS.md` | 🔴 dépôts publics + documents privés : constat, preuves, remédiation | **maintenant** |
| `docs/PUBLIC-AUTORISE.txt` | exceptions explicites du garde-fou | à l'installation du hook |
| `scripts/garde-fou-donnees.sh` | hook `pre-commit` qui refuse les documents dans git | à installer une fois |

---

## Ce qui change par rapport au plan précédent (vérifié dans les dépôts)

| Point | Avant | Réel (source) |
|---|---|---|
| Fournisseurs sans clé dans OmniRoute | « OpenCode Free / Felo sont pré-configurés en auto » | **Faux** : OpenCode Free et Kiro sont marqués `tos: avoid` et **exclus du routage `auto`** ; « une installation neuve peut n'avoir aucune cible sans clé éligible » (`README.md` OmniRoute) |
| Modèle `auto` | « marche tout seul » | `auto` **exige** au moins une connexion éligible : il faut d'abord brancher **un** compte/une clé |
| Route principale Hermes | `model.base_url` + `OPENAI_API_KEY` | la clé va dans `~/.hermes/.env` (600) via `hermes config set OMNIROUTE_API_KEY …` ; un **fournisseur nommé** (`providers.omniroute`) évite d'écraser `OPENAI_API_KEY` |
| Tâches auxiliaires | « il faut les re-router » | leur défaut est `auto` = **le modèle principal** → déjà gratuit si le principal est OmniRoute. On ne les épingle qu'en cas de besoin (privacy) |
| Liste `custom_providers:` | présentée comme la forme normale | **héritée** : la forme courante est le dictionnaire `providers:`, migré automatiquement depuis la config v12 |
| Mesurer le quota Codex | « relève le pourcentage à l'œil » | `hermes usage --provider openai-codex --json` renvoie `windows[].used_percent` + `resets_at` (libellés Session / Weekly) |
| Casser une session | « change de modèle quand ça rame » | tout changement de modèle **en cours de session** jette le cache de prompt (relecture plein tarif) → décider au début, sinon `/compress` puis switcher |

---

## Étape -1 — Stopper l'exposition des documents (2 min)

```bash
gh repo edit Sathancabrol/monorepo          --visibility private --accept-visibility-change-consequences
gh repo edit Sathancabrol/proto-cognitorium --visibility private --accept-visibility-change-consequences
gh api repos/Sathancabrol/monorepo --jq .visibility     # → private

# garde-fou pour ne pas récidiver (une fois par clone)
cp scripts/garde-fou-donnees.sh .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
```

Si l'objectif est la **suppression réelle** (données personnelles de tiers) et pas seulement
l'arrêt de l'accès, il faut en plus purger l'historique : voir `ALERTE-VISIBILITE-DEPOTS.md` § Étape C.

---

## Étape 0 — État des lieux (5 min, à faire en premier)

```powershell
# Windows (PowerShell) — depuis ton clone du monorepo
powershell -ExecutionPolicy Bypass -File .\docs\PARAMETRAGE-HERMES\verifier-hermes.ps1 -Quota
```

```bash
# Linux / WSL
bash docs/PARAMETRAGE-HERMES/verifier-hermes.sh --quota
```

Le script affiche : version de Hermes, chemin de `config.yaml`, provider/modèle courants, `hermes doctor`
(code de sortie), OmniRoute `127.0.0.1:20128`, Ollama `127.0.0.1:11434` + modèles, présence des variables
d'environnement **par nom** (jamais leur valeur), et le quota. **Exit 1** si le socle est incomplet
(aligné sur la règle n°8 de `projects/watchtower/AGENTS.md`).

> Note la sortie : c'est ta ligne de base. Les étapes suivantes la font passer au vert.

---

## Étape 1 — OmniRoute : un seul point d'accès pour le gratuit (20–30 min)

**1.1 Installer** (au choix — Docker est le plus propre, et il écoute sur `127.0.0.1` par défaut, ce qui
respecte la règle « aucun binding `0.0.0.0` » du dépôt) :

```bash
# Docker (recommandé) : dashboard + API sur le même port
docker run -d --name omniroute --restart unless-stopped --stop-timeout 40 \
  -p 127.0.0.1:20128:20128 -v omniroute-data:/app/data diegosouzapw/omniroute:latest

# ou npm (nécessite Node ≥ 22)
npm install -g --allow-scripts=omniroute,keytar,onnxruntime-node,@parcel/watcher,@swc/core,protobufjs,esbuild omniroute
omniroute
```

**1.2 Brancher au moins un fournisseur** — Dashboard `http://localhost:20128` → **Providers** → ajoute
la clé d'un compte que tu as déjà. Choisis dans **ton** registre (`projects/watchtower/audit/REFERENCE.md`),
pas dans une vidéo : Groq, Google AI Studio, OpenRouter (modèles `:free`), GitHub Models, Mistral…
Vérifie **les conditions courantes** : limite, usage des données pour l'entraînement, et **exige une carte
bancaire → non** (règle du dépôt : 0 €/mois).

**1.3 Copier la clé** — Dashboard → **Endpoints** → copie la clé OmniRoute (elle n'est **pas** celle du
fournisseur amont).

**1.4 Vérifier** :

```bash
curl http://localhost:20128/v1/models -H "Authorization: Bearer TA_CLE_OMNIROUTE"
```

**Pièges confirmés** : les fournisseurs marqués `tos: avoid` sont exclus de `auto` même après connexion ;
le mode « sans clé » n'est pas garanti ; les paliers gratuits bougent (re-vérification à date d'écriture,
comme la règle n°9 du dépôt).

---

## Étape 2 — Brancher Hermes sur OmniRoute (10 min)

```powershell
# Sauvegarde d'abord (Hermes migre son config.yaml à chaque `hermes update`)
Copy-Item (hermes config path) ((hermes config path) + ".bak-2026-10-12")

# Route principale = fournisseur nommé "omniroute" (garde OPENAI_API_KEY intacte)
hermes config set model.provider "custom:omniroute"
hermes config set model.default  "auto"
hermes config set providers.omniroute.base_url "http://127.0.0.1:20128/v1"
hermes config set providers.omniroute.key_env  "OMNIROUTE_API_KEY"

# La clé va dans ~/.hermes/.env (jamais dans config.yaml) — un nom UPPER_SNAKE est écrit dans .env
hermes config set OMNIROUTE_API_KEY "<clé OmniRoute → Dashboard → Endpoints>"

# Vérifier
hermes doctor          # doit finir sur 0
hermes status
hermes config get model.provider
```

Si `custom:omniroute` est refusé par ta version, replie-toi sur la forme « documentée Ollama »
(`model.provider: custom` + `model.base_url`) et vois `config.hermes.extrait.yaml` § Repli A.
Puis un vrai test : `hermes chat "réponds juste OK"` et, sous OmniRoute, regarde l'en-tête de réponse
`X-OmniRoute-Decision` (il nomme la stratégie et le fournisseur qui a servi la requête).

---

## Étape 3 — Filet local gratuit (15–30 min)

```bash
ollama pull qwen3:4b          # adapte : voir paliers A/B/C de audit/REFERENCE.md
ollama ps                     # combien de couches sur GPU
curl http://localhost:11434/api/tags
```

Puis :

```powershell
hermes config set providers.ollama-local.base_url "http://127.0.0.1:11434/v1"
hermes fallback add      # interactif : provider "custom", base_url http://127.0.0.1:11434/v1, modèle local
hermes fallback list
```

Points qui font échouer un montage local (tous documentés côté Hermes) :

| Symptôme | Cause | Correctif |
|---|---|---|
| `provider 'ollama' has no endpoint configured` | aucun `base_url` déclaré | `providers.ollama.base_url` (fait ci-dessus) |
| Réponses vides / coupées | contexte Ollama 2048 par défaut, Hermes veut ≥ 64 k pour l'agentique | `model.ollama_num_ctx` ou un Modelfile avec `PARAMETER num_ctx 64000` |
| Le modèle recrache du JSON au lieu d'appeler l'outil | pas de tool-calling | choisir un modèle à tool-calling ; Hermes auto-répare les appels malformés |
| Il « réfléchit » 3 minutes au 1er tour | prefill sans GPU | `HERMES_API_TIMEOUT=1800` dans `.env`, `OLLAMA_KEEP_ALIVE=24h` |

**Ne mets pas Codex/ChatGPT dans la chaîne de fallback automatique** : une route gratuite instable
brûlerait ton quota payant sans que tu le voies. Le payant reste un `/model` **manuel** (voir `ROUTAGE.md`).

---

## Étape 4 — Tâches auxiliaires (10 min) — seulement si tu veux du local pour le privé

Défaut = `auto` = le modèle principal. Donc **rien à faire** pour la gratuité.

À faire seulement pour le **profil privé** (les résumés de compression contiennent tout ton contexte) :

```powershell
hermes config set auxiliary.compression.provider            "custom:ollama-local"
hermes config set auxiliary.compression.model               "qwen3:4b"
hermes config set auxiliary.title_generation.provider       "custom:ollama-local"
hermes config set auxiliary.session_search.provider         "custom:ollama-local"
```

⚠️ Documenté comme **expérimental** hors OpenRouter/Nous Portal ; si un side-task casse, remets
`"auto"` (`hermes config unset auxiliary.compression.provider`). Ne touche pas à **vision** :
il faut un modèle multimodal, et un petit modèle local rendrait l'analyse d'image inutilisable.

---

## Étape 5 — Deux mondes séparés : `public\` et `prive\` (30 min)

```powershell
hermes profile create prive --clone                    # copie config/.env/SOUL.md/skills/mémoire
hermes -p prive config set terminal.cwd "G:\PERSO\PROJET COGNITORIUM\prive"
hermes -p prive config set model.provider "custom"     # profil privé = 100 % local
hermes -p prive config set model.base_url "http://127.0.0.1:11434/v1"
hermes -p prive config set model.default  "qwen3:4b"
hermes -p prive config set auxiliary.compression.provider "custom:ollama-local"

hermes project create cognitorium                      # workspace multi-dossiers (état par profil)
hermes project add-folder cognitorium "G:\PERSO\PROJET COGNITORIUM\public"
```

Le détail (arborescence, `.gitignore`, sauvegarde hors-ligne, ce qui ne doit **jamais** être synchronisé)
est dans `STRUCTURE-HYBRIDE.md`.

---

## Étape 6 — Hygiène des requêtes et budget (en continu, gain immédiat)

1. **Une tâche = une session**, puis le résultat est **écrit dans le dépôt** (rien ne survit à une fenêtre).
2. `/compress` à chaque jalon ; `hermes prompt-size` quand un modèle local rame (le prompt fixe = système
   + schémas d'outils) ; `hermes tools` pour **désactiver les outils inutiles** (gain direct sur chaque
   requête, surtout en local).
3. **Mesurer, pas deviner** :

```powershell
hermes usage --provider openai-codex --json          # windows[].used_percent + resets_at
.\docs\PARAMETRAGE-HERMES\verifier-hermes.ps1 -Quota -Log   # ajoute une ligne à quota-log.csv
```

4. Répartition du quota restant (69 % jusqu'au 19/10, fenêtre 5 h) : ~35–40 % spécifications,
  15–20 % bugs difficiles, 15 % tampon, le reste **avant** l'échéance. Une spec qui sort du quota
   finit en fichier dans le dépôt, jamais dans la conversation.
5. Ne change pas de modèle au milieu d'une longue session : le cache de prompt est perdu
   (relecture plein tarif). Décide au début, ou `/compress` d'abord.

---

## Étape 7 — Optionnel (à faire seulement après que 0→6 est vert)

| Envie | Commande | Remarque |
|---|---|---|
| Bot Telegram/Discord (« router bot ») | `hermes gateway setup` puis `hermes gateway start` | `platforms.telegram.enabled: true` + token BotFather ; vérifie `hermes pairing` (appairage des MP) avant de l'exposer |
| Piloter la passerelle depuis l'agent | `hermes mcp add omniroute --url http://127.0.0.1:20128/api/mcp/stream --auth header` puis `hermes mcp test omniroute` | OmniRoute expose MCP (110 outils : routage, providers, combos) |
| Veille / rapports nocturnes | `hermes cron create …` puis `hermes cron doctor` | c'est le « P8 pendant que tu dors » de `audit/REFERENCE.md` |
| Éviter le cloud pour Codex (CLI) | `hermes codex-runtime migrate --dry-run` | réécrit le bloc géré de `~/.codex/config.toml` |

---

## Ce que je fais / ce que tu fais

| Qui | Quoi |
|---|---|
| **Moi (agent, ici)** | écrire les configs et scripts, générer les `CARTE.md` par dépôt, rédiger les 3 skills Hermes, adapter les commandes si tu me dis ton OS/répertoire exact |
| **Toi (3 clics)** | créer la clé OmniRoute, brancher **un** fournisseur (accepter ses CGU), coller le token de bot si tu en veux un — je ne saisis ni tes mots de passe ni tes clés |
| **Personne** | exposer un port en `0.0.0.0`, committer `.env`, envoyer un document `TP`/perso à un palier gratuit |

---

## Rollback

```powershell
Copy-Item ((hermes config path) + ".bak-2026-10-12") (hermes config path) -Force   # restaure
hermes config unset auxiliary.compression.provider                                   # une clé à la fois
hermes fallback clear                                                                # vide la chaîne
hermes profile delete prive                                                          # supprime le profil
```

---

## Questions ouvertes (elles changent le détail, pas le plan)

1. **OS** : Windows natif (`%LOCALAPPDATA%\hermes`) ou WSL2 (`~/.hermes`) ? Les chemins des scripts
   et de `terminal.cwd` en dépendent.
2. **GPU** : lequel / combien de VRAM ? C'est ce qui décide du modèle local (paliers A/B/C).
3. **Bot** : OmniRoute seul, ou un bot Telegram/Discord branché sur la passerelle Hermes ?
   (Deux configurations différentes, l'une n'implique pas l'autre.)
4. **OmniRoute est-il déjà installé** ? Si oui, saute l'étape 1.1 et va directement au 1.2.

Dis-moi (1)(2)(3) et je réécris les étapes 3, 5 et 7 avec tes chemins et ton matériel exacts.
