# Bone — agent d’Olympus

Gosse-squelette en **papier construction**, même énergie que South Park.
Il habite le serveur Discord **Olympus** (le lab de [Sathancabrol](https://github.com/Sathancabrol)).

> *J’suis Bone. J’suis mort. J’m’en fous.*

![Bone](assets/bone.png)

## Ce qu’il fait

- Parle **français** (anglais s’il faut) comme un gosse de South Park : court, franc, potache.
- Connaît les repos du monorepo : Watchtower, HCSM, Cognitorium, le chantier PDF, etc.
- Commandes slash : `/bone` `/roast` `/mood` `/episode` `/projets` `/aide`
- Préfixe : `!bone …` · mention `@Bone` · réponse à ses messages
- `!bone tg` / `!bone parle` pour le faire taire

Il n’est **pas** un bot musique, ni un modérateur, ni ChatGPT en costume.

## Playground (sans Discord)

Ouvre `index.html` (ou, depuis le monorepo) :

```bash
# à la racine du monorepo
uvicorn app.main:app --host 0.0.0.0 --port 8123
# → http://localhost:8123/preview/bone/index.html
# → http://localhost:8123/bone
```

Le cerveau tourne en local (`persona.json` + `persona.py` / `assets/persona.js`). Zéro clé.

## Le coller sur Discord Olympus

1. [Discord Developer Portal](https://discord.com/developers/applications) → **New Application** → `Bone`
2. Onglet **Bot** → Add Bot
   - Reset Token → copier
   - Privileged Gateway Intents : **MESSAGE CONTENT INTENT** = ON
   - Avatar : `projects/bone/assets/bone.png`
3. Onglet **OAuth2 → URL Generator**
   - Scopes : `bot` + `applications.commands`
   - Permissions : View Channels, Send Messages, Embed Links, Attach Files, Read Message History, Add Reactions
   - Ouvrir l’URL → inviter **Bone** sur **Olympus**
4. Ici :

```bash
cd projects/bone
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# coller DISCORD_TOKEN=...
python discord_bot.py
```

Le bot doit passer **en ligne**, watching *South Park · Olympus*.

Salons bavards par défaut : `général`, `general`, `olympus`, `bone`, `chat`, `lounge`.
Ailleurs : mention ou `!bone`. Variable `BONE_CHATTY=0` pour n’autoriser que ça.

## Fichiers

```
projects/bone/
├─ index.html          playground Discord (Olympus)
├─ persona.json        identité, intents, répliques
├─ persona.py          cerveau Python (bot + tests)
├─ discord_bot.py      discord.py 2.x
├─ assets/bone.png     cut-out
├─ assets/bone.css
├─ assets/app.js
├─ assets/persona.js   cerveau JS (playground)
└─ tests/test_persona.py
```

## Tests

```bash
cd projects/bone && python3 -m pytest tests/test_persona.py -q
```
