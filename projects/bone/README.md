# Bone — agent d’Olympus

Gosse-squelette en **papier construction**, énergie South Park.
Il tourne **tout seul** : pas besoin du reste du monorepo.

> *J’suis Bone. J’suis mort. J’m’en fous.*

![Bone](assets/bone.png)

---

## Windows : ZIP + installeur (recommandé)

1. Télécharge **`Bone-Olympus-Install.zip`**
2. Clic droit → Extraire tout
3. Double-clic **`INSTALLER.bat`**
4. L’installeur ouvre Discord : **tu choisis le serveur** (Olympus ou un autre) → Autoriser
5. Boom. Bone est en ligne. Raccourci Bureau.

Le ZIP est autonome (pas le monorepo). Rebuild : `python packaging/build-zip.py`

---

## Installer SEULEMENT Bone sur ton PC (Git / Linux)

Ne clone **pas** tout le monorepo (il est énorme, plein de PDF).
Tu n’as besoin que de ce dossier.

### 0. Une fois : Python + Git

- **Python 3.11+** : https://www.python.org/downloads/  
  Sur Windows : coche **« Add python.exe to PATH »** avant Install.
- **Git** : https://git-scm.com/downloads

### 1. Récupérer uniquement ce module (~400 Ko)

```bash
git clone --depth 1 --filter=blob:none --sparse -b arena/0d411b29-monorepo https://github.com/Sathancabrol/monorepo.git bone
cd bone
git sparse-checkout set projects/bone
cd projects/bone
```

Tu es maintenant dans le dossier de Bone. C’est tout ce qu’il faut.

Sans Git : télécharge le dossier  
https://download-directory.github.io/?url=https://github.com/Sathancabrol/monorepo/tree/arena/0d411b29-monorepo/projects/bone  
Dézippe-le, ouvre-le.

### 2. Créer le bot sur Discord (2 min)

1. https://discord.com/developers/applications → **New Application** → nom `Bone`
2. Menu **Bot** → Add Bot
   - **Reset Token** → copier (tu ne le reverras plus)
   - Privileged Gateway Intents : **MESSAGE CONTENT INTENT** = ON
   - Avatar optionnel : `assets/bone.png`
3. Menu **OAuth2 → URL Generator**
   - Scopes : `bot` **et** `applications.commands`
   - Permissions : View Channels, Send Messages, Embed Links, Attach Files, Read Message History, Add Reactions
   - Copier l’URL en bas → l’ouvrir dans le navigateur → inviter **Bone** sur le serveur **Olympus**
   - Il faut les droits **Gérer le serveur** (ou Owner) sur Olympus

### 3. Lancer Bone

**Windows** — double-clic sur `lancer.bat`  
La première fois, le Bloc-notes ouvre `.env` : colle le token

```
DISCORD_TOKEN=colle_le_token_ici
```

Enregistre, relance `lancer.bat`. Laisse la fenêtre noire ouverte.

**Linux / macOS**

```bash
chmod +x lancer.sh
./lancer.sh
```

Même chose : il ouvre `.env`, tu colles le token, tu relances.

Quand ça marche tu vois :

```
Bone en ligne : Bone#xxxx
```

et dans Discord il est **en ligne**, *watching South Park · Olympus*.

### 4. Lui parler

Dans `#général` (ou un salon listé dans `.env`) :

- `@Bone salut`
- `!bone t'es qui`
- `/roast` `/mood` `/episode` `/projets` `/aide`
- `!bone tg` pour le faire taire · `!bone parle` pour le ranimer

---

## Playground sans Discord

Juste chatter avec Bone dans le navigateur, sans token :

- Windows : double-clic `playground.bat`
- Linux/macOS : `python3 -m http.server 8765` puis http://127.0.0.1:8765

---

## Commandes à la main (si tu n’utilises pas les scripts)

```bash
cd projects/bone          # ou le dossier dézippé
python3 -m venv .venv
# Windows : .venv\Scripts\activate
# Linux/mac : source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # Windows : copy .env.example .env
# éditer .env → DISCORD_TOKEN=...
python discord_bot.py
```

Arrêter : `Ctrl+C`. Relancer : même commande (ou `lancer.bat`).

---

## Fichiers

```
bone/
├─ lancer.bat / lancer.sh     ← installe + démarre le bot
├─ playground.bat / .sh       ← UI Discord locale
├─ discord_bot.py
├─ persona.py + persona.json  ← cerveau
├─ .env.example               ← copie vers .env (jamais git)
├─ assets/bone.png
└─ index.html
```

`.env` reste sur **ton** PC. Ne le commite pas, ne l’envoie pas.

## Désinstaller

Supprime le dossier `bone`. Rien d’autre n’est installé (sauf le venv dedans).
Sur Discord : Developer Portal → application Bone → Delete.
