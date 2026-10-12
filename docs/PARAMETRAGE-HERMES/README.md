# Paramétrage Hermes — finir le montage maintenant

> **Objectif** : Hermes répond **gratuitement** (OmniRoute + Ollama local), le quota payant
> (Codex / ChatGPT) est **réservé au travail difficile**, et rien de sensible ne sort de la machine.
>
> **Réglé pour toi** : machine **Windows native** (`%LOCALAPPDATA%\hermes`), **palier A**
> (pas de GPU, ≤ 8 Go RAM), **bot Discord** à la fin, purge des dépôts **avant** changement de
> visibilité. Le plan ci-dessous en tient compte.
>
> **Statut** : kit d'exécution. Je n'ai pas accès à ton PC : l'étape 0 (5 min) produit l'état réel.
> Tout vient des dépôts **Hermes Agent** (`cli-config.yaml.example`, `website/docs/`) et
> **OmniRoute** (`README.md`, `docs/`) lus le 2026-10-12 — pas de mémoire.

---

## 🔴 Avant tout le reste : dépôts publics + documents privés

Vérifié avec ton compte le 2026-10-12 : `Sathancabrol/monorepo` (**public**, `size-pack` 305 Mo,
1818 fichiers suivis) contient **268 documents / 276 Mo** et **300 images** suivis, dont
**210 documents à la racine** (DCE, CCAP/CCTP, BPU, DQE, métrés, devis d'entreprise, factures de
situation, recours, grilles de salaires) ; `Sathancabrol/proto-cognitorium` (**public**) en contient
50 dont des **CV de tiers**. Aucun secret ni `.env` exposé (vérifié), **0 fork / 0 star** sur `monorepo`.

Tu as choisi l'ordre **purge → visibilité**. C'est le bon ordre sur le fond, avec une nuance :
mettre en privé est **réversible et n'empêche aucune purge** — tu peux couper l'accès en 2 min
et réécrire l'historique ensuite sans rien perdre.

| Document | Contenu |
|---|---|
| `ALERTE-VISIBILITE-DEPOTS.md` | constat, preuves reproductibles, ce qui est exposé, options |
| `PURGE-HISTORIQUE.md` | procédure mesurée : zones, tailles, publication, re-clone, support GitHub |
| `scripts/purger-documents-git.sh` | `--inventaire` / `--plan` / `--executer` sur **clone miroir** (testé) |
| `docs/PURGE-MOTIFS.txt` | motifs actifs (zone A = CV/données de tiers, zone B = documents racine) |
| `scripts/garde-fou-donnees.sh` | hook `pre-commit` qui refuse les documents dans git (testé) |

Ordre conseillé : **copier** vers `prive\` → `--plan` → `--executer` → publier → **re-cloner** chaque
machine → support GitHub → installer le hook → décider la visibilité.

---

## Fichiers de ce dossier

| Fichier | Rôle | Quand |
|---|---|---|
| `README.md` | le plan d'action ordonné (ce fichier) | maintenant, puis à chaque reprise |
| `verifier-hermes.ps1` | état des lieux + `hermes doctor` + ports + quota (exit 0/1) | étape 0, et avant/après chaque install |
| `verifier-hermes.sh` | idem pour WSL2/Linux | si tu changes de machine |
| `config.hermes.extrait.yaml` | extrait de config à fusionner (OmniRoute, Ollama, fallback, aux) | étapes 2 et 4 |
| `ROUTAGE.md` | règle de routage manuelle + hygiène de requête | en continu |
| `STRUCTURE-HYBRIDE.md` | `public\` / `prive\`, permissions, sauvegarde, profils | étape 5 |
| `CARTE.template.md` · `CARTE.monorepo.md` | carte d'un dépôt (exemple déjà rempli : ce dépôt) | étape 5 |
| `quota-log.csv` | journal de calibration (écrit par `-Log`) | en continu |
| `ALERTE-VISIBILITE-DEPOTS.md` · `PURGE-HISTORIQUE.md` | 🔴 dépôts publics + purge | **maintenant** |

---

## Ce que change ce kit par rapport au plan précédent (vérifié dans les dépôts)

| Point | Avant | Réel (source) |
|---|---|---|
| Fournisseurs sans clé dans OmniRoute | « OpenCode Free / Felo sont pré-configurés en auto » | **Faux** : marqués `tos: avoid`, **exclus du routage `auto`** ; « une installation neuve peut n'avoir aucune cible sans clé éligible » |
| Modèle `auto` | « marche tout seul » | `auto` **exige** au moins une connexion éligible → brancher **un** compte d'abord |
| Route principale Hermes | `model.base_url` + `OPENAI_API_KEY` | fournisseur **nommé** (`providers.omniroute` + `key_env`) : la clé va dans `.env`, et `OPENAI_API_KEY` n'est pas écrasée |
| Tâches auxiliaires | « il faut les re-router » | défaut `auto` = **le modèle principal** → déjà gratuit si le principal est OmniRoute |
| Liste `custom_providers:` | présentée comme la forme normale | **héritée** ; la forme courante est le dictionnaire `providers:` (migration auto depuis la config v12) |
| Mesurer le quota | « relève le pourcentage à l'œil » | `hermes usage --provider openai-codex --json` → `windows[].used_percent` + `resets_at` |
| Changer de modèle | « switche quand ça rame » | un switch **en cours de session** jette le cache de prompt (relecture plein tarif) |
| Palier A local | « un petit modèle suffit » | un modèle 1-3 B n'a pas de tool-calling fiable : il **ne conduit pas l'agent**, il dépanne (voir étape 3) |

---

## Étape 0 — État des lieux (5 min)

```powershell
powershell -ExecutionPolicy Bypass -File .\docs\PARAMETRAGE-HERMES\verifier-hermes.ps1 -Quota
```

Affiche : version de Hermes, chemins `config.yaml` / `.env`, route provider/modèle, `hermes doctor`
(code de sortie réel), OmniRoute `127.0.0.1:20128`, Ollama `127.0.0.1:11434` + modèles, présence des
variables **par nom** (jamais la valeur), et le quota. **Exit 1** si le socle est incomplet
(règle n°8 de `projects/watchtower/AGENTS.md`).

---

## Étape 1 — OmniRoute : un seul point d'accès pour le gratuit (20–30 min)

**1.1 Installer** — Docker est le plus propre et écoute sur `127.0.0.1` (règle « aucun binding 0.0.0.0 ») :

```powershell
docker run -d --name omniroute --restart unless-stopped --stop-timeout 40 `
  -p 127.0.0.1:20128:20128 -v omniroute-data:/app/data diegosouzapw/omniroute:latest

# ou npm (Node >= 22)
npm install -g --allow-scripts=omniroute,keytar,onnxruntime-node,@parcel/watcher,@swc/core,protobufjs,esbuild omniroute
omniroute
```

**1.2 Brancher au moins un fournisseur** — Dashboard `http://localhost:20128` → **Providers**.
Prends tes clés dans **ton** registre (`projects/watchtower/audit/REFERENCE.md` : Groq, Google AI
Studio, OpenRouter `:free`, GitHub Models…), pas dans une vidéo. Vérifie les conditions du moment
(limite, entraînement sur tes données) et **exige une carte bancaire → non**.

**1.3 Copier la clé OmniRoute** — Dashboard → **Endpoints** (ce n'est pas la clé du fournisseur amont).

**1.4 Vérifier** :

```powershell
curl.exe http://localhost:20128/v1/models -H "Authorization: Bearer TA_CLE_OMNIROUTE"
```

**Pièges confirmés** : `tos: avoid` → exclus de `auto` même après connexion ; le mode « sans clé »
n'est pas garanti ; les paliers gratuits bougent (règle n°9 : re-vérifier à la date d'écriture).

---

## Étape 2 — Brancher Hermes sur OmniRoute (10 min)

```powershell
Copy-Item (hermes config path) ((hermes config path) + ".bak-2026-10-12")

hermes config set model.provider "custom:omniroute"
hermes config set model.default  "auto"
hermes config set providers.omniroute.base_url "http://127.0.0.1:20128/v1"
hermes config set providers.omniroute.key_env  "OMNIROUTE_API_KEY"

# la clé va dans .env (jamais dans config.yaml) — un nom UPPER_SNAKE est écrit dans .env
hermes config set OMNIROUTE_API_KEY "<clé OmniRoute → Dashboard → Endpoints>"

hermes doctor            # doit finir sur exit 0
hermes status
hermes config get model.provider
```

Si `custom:omniroute` est refusé par ta version : repli A dans `config.hermes.extrait.yaml`.
Test réel : `hermes chat "réponds juste OK"`, puis côté OmniRoute regarde l'en-tête
`X-OmniRoute-Decision` (stratégie + fournisseur qui ont servi la requête).

---

## Étape 3 — Filet local, version **palier A** (30 min)

Sans GPU et avec ≤ 8 Go de RAM, le local **ne peut pas** porter l'agent : les modèles 1-3 B des
paliers A de ton propre audit (`qwen3:0.6b`, `gemma3:1b`, `llama3.2:3b`) n'ont pas de tool-calling
fiable et tournent à quelques jetons/seconde. On l'utilise donc pour ce qu'il sait faire :
**dépannage quand OmniRoute tombe**, et **travail privé simple** (lecture, résumé, classement).

```powershell
ollama pull qwen3:4b        # ~2,5 Go : le meilleur compromis texte/tool-calling sur 8 Go de RAM
# alternatives palier A : qwen3:1.7b (~1,2 Go), gemma3:1b (~0,8 Go) — plus rapides, moins capables
ollama ps                   # vérifie ce qui est chargé (0 = tout CPU, c'est attendu)
```

```powershell
hermes config set providers.ollama-local.base_url "http://127.0.0.1:11434/v1"
hermes config set model.ollama_num_ctx 16384      # pas 64000 : 64k de contexte sur CPU = inutilisable
hermes fallback add      # interactif : provider "custom", base_url http://127.0.0.1:11434/v1, modèle local
hermes fallback list
```

```powershell
# ~/.hermes/.env  (ou: hermes config set HERMES_API_TIMEOUT 1800)
HERMES_API_TIMEOUT=1800
```

```powershell
# garder le modèle en mémoire (sinon 5 min d'inactivité = rechargement complet avant chaque réponse)
[Environment]::SetEnvironmentVariable("OLLAMA_KEEP_ALIVE","24h","User")
```

| Symptôme | Cause | Correctif |
|---|---|---|
| `provider 'ollama' has no endpoint configured` | aucun `base_url` déclaré | `providers.ollama.base_url` (fait ci-dessus) |
| réponses vides / coupées | contexte Ollama 2048 par défaut | `model.ollama_num_ctx` (16 k ici) ou un Modelfile `PARAMETER num_ctx 16384` |
| le modèle recrache du JSON au lieu d'appeler l'outil | pas de tool-calling | c'est structurel en palier A : garde ce modèle pour le texte, pas pour l'agentique |
| 2-5 min de silence au 1er tour | prefill CPU du prompt + schémas d'outils | `hermes prompt-size` puis `hermes tools` pour désactiver les outils inutiles |
| il tourne dans le vide | `max_turns: 500` par défaut | `hermes config set agent.max_turns 30` |

**Ne mets pas Codex/ChatGPT dans la chaîne de fallback** : une route gratuite instable brûlerait ton
quota payant sans trace. Le payant reste un choix **manuel** (`/model`, voir `ROUTAGE.md`).

---

## Étape 4 — Tâches auxiliaires (5 min)

Défaut = `auto` = le modèle principal → **rien à faire pour la gratuité**. En palier A :

- **profil par défaut** : laisse `auto` (les auxiliaires passent par OmniRoute, gratuit et rapide) ;
- **profil `prive`** : épingle-les au local, sinon tes compressions partent dans le cloud :

```powershell
hermes -p prive config set auxiliary.compression.provider      "custom:ollama-local"
hermes -p prive config set auxiliary.compression.model         "qwen3:4b"
hermes -p prive config set auxiliary.title_generation.provider "custom:ollama-local"
hermes -p prive config set auxiliary.session_search.provider   "custom:ollama-local"
```

⚠️ Documenté comme **expérimental** hors OpenRouter/Nous Portal : vérifie par une longue session, et
remets `"auto"` (`hermes config unset auxiliary.compression.provider`) au premier comportement bizarre.
Ne touche pas à **vision** : il faut un modèle multimodal.

---

## Étape 5 — Deux mondes séparés : `public\` et `prive\` (30 min, Windows)

```powershell
hermes profile create prive --clone
hermes -p prive config set terminal.cwd "G:\PERSO\PROJET COGNITORIUM\prive"
hermes -p prive config set model.provider "custom"
hermes -p prive config set model.base_url "http://127.0.0.1:11434/v1"
hermes -p prive config set model.default  "qwen3:4b"
hermes -p prive config set model.ollama_num_ctx 16384
hermes -p prive config set agent.max_turns 20
hermes profile list          # le profil actif est marqué d'une étoile
hermes -p prive              # session privée, 0 % cloud
```

Chemins à connaître (Windows natif) :

| Quoi | Où |
|---|---|
| `config.yaml` / `.env` du profil par défaut | `%LOCALAPPDATA%\hermes\` (source de vérité : `hermes config path`, `hermes config env-path`) |
| profil `prive` | `%LOCALAPPDATA%\hermes\profiles\prive\` |
| skills / mémoire / sessions | `%LOCALAPPDATA%\hermes\skills|memories|sessions\` |
| workspace multi-dossiers | `hermes project create cognitorium` puis `add-folder` (état par profil) |

Détail complet (arborescence `public\`/`prive\`, `icacls`, sauvegarde `robocopy`, ce qui ne doit
jamais être synchronisé) : `STRUCTURE-HYBRIDE.md`.

---

## Étape 6 — Hygiène des requêtes et budget (en continu)

1. **Une tâche = une session**, puis le résultat **écrit dans le dépôt** (rien ne survit à une fenêtre).
2. `/compress` à chaque jalon ; `hermes prompt-size` si un modèle local rame ; `hermes tools` pour
   désactiver les outils inutiles (gain direct sur **chaque** requête).
3. Mesurer, pas deviner :

```powershell
hermes usage --provider openai-codex --json
.\docs\PARAMETRAGE-HERMES\verifier-hermes.ps1 -Quota -Log    # ajoute une ligne à quota-log.csv
```

4. Quota restant (69 % jusqu'au 19/10, fenêtre 5 h) : ~35–40 % spécifications, 15–20 % bugs
   difficiles, 15 % tampon, le reste **avant** l'échéance. Une spec qui sort du quota finit en
   fichier dans le dépôt, jamais dans la conversation.
5. Ne change pas de modèle au milieu d'une longue session (cache de prompt jeté = relecture plein tarif).

---

## Étape 7 — Bot Discord (30–40 min, à faire après 0→6)

Création côté Discord : **Developer Portal** → nouvelle application → **Bot** → copie le token →
active les intents nécessaires → **OAuth2 → URL Generator** (scope `bot`, permission *Send Messages*)
→ invite-le sur ton serveur. Puis récupère ton **User ID** (Discord : Paramètres → Avancés →
Mode développeur → clic droit sur ton nom → Copier l'identifiant).

```powershell
hermes gateway setup     # choisis Discord : le wizard vérifie le token, les intents, la liste blanche
# ou manuellement, dans %LOCALAPPDATA%\hermes\.env :
#   DISCORD_BOT_TOKEN=…
#   DISCORD_ALLOWED_USERS=<ton user id>
hermes gateway           # démarre la passerelle
hermes pairing           # appairage/contrôle d'accès (sécurise les MP)
```

Points qui évitent les mauvaises surprises (comportements documentés) :

| Réglage | Défaut | À savoir |
|---|---|---|
| salons | le bot ne répond que sur **@mention** | `DISCORD_FREE_RESPONSE_CHANNELS` pour un salon « chat libre » |
| MP | il répond à tout | d'où l'intérêt de `DISCORD_ALLOWED_USERS` (sans liste, tout est refusé par défaut) |
| messages proactifs (cron, rappels) | — | `DISCORD_HOME_CHANNEL` = salon cible |
| sessions partagées | isolées par utilisateur | `group_sessions_per_user: false` = une seule conversation pour tout le salon (coûts et contexte partagés) |
| visionneuse | threads automatiques | `DISCORD_AUTO_THREAD` (défaut `true`) |

**Sécurité** : un bot Discord, en palier A, tourne sur ton **modèle principal** = OmniRoute (cloud).
Donc : le bot sert pour `public\` et les questions courantes, **jamais** pour les documents de `prive\`
→ ceux-là passent par `hermes -p prive` en local. (Si tu veux un bot qui ne sort pas de la machine,
il faut le palier B : un modèle local capable de tool-calling.)

Optionnel utile : `hermes mcp add omniroute --url http://127.0.0.1:20128/api/mcp/stream --auth header`
puis `hermes mcp test omniroute` (OmniRoute expose MCP : routage, providers, combos).

---

## Ce que je fais / ce que tu fais

| Qui | Quoi |
|---|---|
| **Moi (agent)** | écrire les configs, scripts, procédures ; générer les `CARTE.md` des autres dépôts ; adapter si tu me donnes un retour d'exécution |
| **Toi (clics)** | OmniRoute : créer la clé + brancher **un** fournisseur (accepter ses CGU) ; Discord : créer le bot et coller le token ; publier la purge (`push --mirror`) ; re-cloner |
| **Personne** | exposer un port en `0.0.0.0`, committer `.env`, envoyer un document de `prive\` à un palier gratuit |

---

## Rollback

```powershell
Copy-Item ((hermes config path) + ".bak-2026-10-12") (hermes config path) -Force
hermes config unset auxiliary.compression.provider
hermes fallback clear
hermes profile delete prive
```

---

## Ce qui reste ouvert

1. **OmniRoute est-il déjà installé** (Docker ou npm) ? Si oui saute 1.1 → 1.2.
2. **Quel fournisseur gratuit** tu vas brancher (le choix t'appartient : CGU + usage des données).
3. **La purge** : tu la lances quand personne d'autre ne pousse ; je peux préparer la commande finale
   dès que tu me dis « go ».
