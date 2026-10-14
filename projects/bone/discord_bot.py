#!/usr/bin/env python3
"""
Bone — agent Discord pour le serveur Olympus.
South Park construction-paper kid. Stagiaire squelette de Satan.

Lancer :
  cd projects/bone
  python3 -m venv .venv && source .venv/bin/activate
  pip install -r requirements.txt
  cp .env.example .env   # coller DISCORD_TOKEN
  python discord_bot.py
"""
from __future__ import annotations

import json
import os
import re
import sys
import logging
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from persona import think as bone_reply, opener, help_text, set_mood, set_quiet, channel_state, DATA
from perms import PACKS, invite_url, portal_bot_url

try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
except ImportError:
    pass

import discord
from discord import app_commands
from discord.ext import commands

log = logging.getLogger("bone")

TOKEN = os.getenv("DISCORD_TOKEN", "").strip()
GUILD_NAME = os.getenv("BONE_GUILD", "Olympus").strip() or "Olympus"
CHATTY = os.getenv("BONE_CHATTY", "1").strip() not in {"0", "false", "no"}
CHATTY_CHANNELS = {
    c.strip().lower().lstrip("#")
    for c in os.getenv("BONE_CHANNELS", "général,general,olympus,bone,chat,lounge").split(",")
    if c.strip()
}

def _flag(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}


INTENTS = discord.Intents.default()
INTENTS.message_content = True
INTENTS.guilds = True
INTENTS.messages = True
INTENTS.members = _flag("BONE_MEMBERS_INTENT")
INTENTS.presences = _flag("BONE_PRESENCE_INTENT")

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!bone ", "!bone", "!b "), intents=INTENTS, help_command=None)


def _chan_id(msg: discord.Message) -> str:
    return str(msg.channel.id)


def _should_talk(msg: discord.Message) -> bool:
    if msg.author.bot:
        return False
    st = channel_state(_chan_id(msg))
    if st.get("quiet"):
        # only wake on explicit prefix / mention
        if bot.user and bot.user.mentioned_in(msg):
            return True
        raw = msg.content.lower()
        return raw.startswith("!bone") or raw.startswith("!b ")
    if bot.user and bot.user.mentioned_in(msg):
        return True
    if msg.reference and msg.reference.resolved:
        ref = msg.reference.resolved
        if isinstance(ref, discord.Message) and ref.author.id == bot.user.id:
            return True
    raw = msg.content.lower().strip()
    if raw.startswith("!bone") or raw.startswith("!b ") or raw.startswith("!b"):
        return True
    # first word is bone
    if re.match(r"^bone[\s,!?]", raw) or raw == "bone":
        return True
    if CHATTY:
        name = getattr(msg.channel, "name", "") or ""
        if name.lower() in CHATTY_CHANNELS:
            # don't reply to every message — only if addressed or short ping
            if "bone" in raw or len(raw) < 80:
                return True
    return False


def _clean(msg: discord.Message) -> str:
    text = msg.content or ""
    if bot.user:
        text = text.replace(f"<@{bot.user.id}>", "").replace(f"<@!{bot.user.id}>", "")
    text = re.sub(r"^(!bone|!b)\s*", "", text, flags=re.I)
    return text.strip()


def _write_ready() -> None:
    payload = {
        "user": str(bot.user) if bot.user else None,
        "id": bot.user.id if bot.user else None,
        "guilds": [
            {"id": g.id, "name": g.name, "members": g.member_count}
            for g in bot.guilds
        ],
    }
    (ROOT / "ready.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (ROOT / "bone.pid").write_text(str(os.getpid()), encoding="utf-8")


async def _sync_guild(guild: discord.Guild) -> None:
    try:
        synced = await bot.tree.sync(guild=guild)
        log.info("slash @ %s : %s", guild.name, [c.name for c in synced])
    except Exception as e:
        log.warning("sync %s : %s", guild.name, e)


async def _hello_channel(guild: discord.Guild):
    me = guild.me
    if me is None:
        return None
    if guild.system_channel and guild.system_channel.permissions_for(me).send_messages:
        return guild.system_channel
    for c in guild.text_channels:
        if c.permissions_for(me).send_messages:
            return c
    return None


@bot.event
async def on_ready():
    log.info("Bone en ligne : %s (id=%s)", bot.user, bot.user.id if bot.user else "?")
    names = ", ".join(g.name for g in bot.guilds) or "(aucun serveur — invite le bot)"
    log.info("Serveurs : %s", names)
    watching = GUILD_NAME if len(bot.guilds) != 1 else bot.guilds[0].name
    activity = discord.Activity(type=discord.ActivityType.watching, name=f"South Park · {watching}")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    for g in bot.guilds:
        await _sync_guild(g)
    try:
        await bot.tree.sync()
    except Exception as e:
        log.warning("sync global : %s", e)
    _write_ready()


@bot.event
async def on_guild_join(guild: discord.Guild):
    log.info("Nouveau serveur : %s (%s)", guild.name, guild.id)
    try:
        await guild.me.edit(nick="Bone")
    except Exception:
        pass
    await _sync_guild(guild)
    _write_ready()
    ch = await _hello_channel(guild)
    if ch is None:
        return
    intro = opener("fr")
    text = (
        f"{intro}\n\n"
        f"On m'a installé sur **{guild.name}**. J'suis Bone. "
        f"Ping-moi, tape `!bone` ou `/aide`."
    )
    try:
        await ch.send(text)
    except Exception as e:
        log.warning("hello %s : %s", guild.name, e)


@bot.event
async def on_message(msg: discord.Message):
    if msg.author.bot:
        return
    await bot.process_commands(msg)
    if not _should_talk(msg):
        return
    # skip if a slash already handled
    text = _clean(msg)
    if not text:
        text = "salut"
    # local commands
    low = text.lower().strip()
    cid = _chan_id(msg)
    if low in {"aide", "help", "?"}:
        await msg.channel.send(help_text())
        return
    if low.startswith("mood ") or low.startswith("humeur "):
        mood = low.split(None, 1)[1]
        set_mood(cid, mood)
        await msg.channel.send(f"Mood : **{channel_state(cid)['mood']}**. J'essaie.")
        return
    if low in {"tg", "silence", "chut"}:
        set_quiet(cid, True)
        await msg.reply("Ok. J'me tais. `!bone parle` pour me ranimer.", mention_author=False)
        return
    if low in {"parle", "speak"}:
        set_quiet(cid, False)
        await msg.reply("Re-bonjour. L'os est chaud.", mention_author=False)
        return
    if low in {"autorisations", "permissions", "perms", "droits"}:
        await _send_autorisations(msg.channel, ephemeral_user=None)
        return
    async with msg.channel.typing():
        out = bone_reply(text, channel_id=cid, author=msg.author.display_name)
    await msg.reply(out, mention_author=False)


class AutorisationsView(discord.ui.View):
    def __init__(self, client_id: int):
        super().__init__(timeout=180)
        combos = [
            ("Lecture + parler", ("base",)),
            ("+ Modération", ("base", "moderation")),
            ("+ Vocal", ("base", "vocal")),
            ("+ Salons & rôles", ("base", "salons", "roles")),
            ("Admin ⚠ tout", ("admin",)),
        ]
        for label, packs in combos:
            self.add_item(discord.ui.Button(label=label, url=invite_url(client_id, *packs)))
        self.add_item(discord.ui.Button(label="Intents (portail Bot)", url=portal_bot_url(client_id)))


def _perm_lines(guild: discord.Guild | None) -> str:
    if guild is None or guild.me is None:
        return "Hors serveur : je vois pas mes droits."
    p = guild.me.guild_permissions
    flags = [
        ("Parler", p.send_messages),
        ("Slash", p.use_application_commands),
        ("Lire l'historique", p.read_message_history),
        ("Kick", p.kick_members),
        ("Ban", p.ban_members),
        ("Timeout", p.moderate_members),
        ("Gérer messages", p.manage_messages),
        ("Gérer salons", p.manage_channels),
        ("Gérer rôles", p.manage_roles),
        ("Vocal", p.connect),
        ("Admin", p.administrator),
    ]
    rows = [("✅" if ok else "❌") + " " + name for name, ok in flags]
    return "\n".join(rows)


async def _send_autorisations(dest, ephemeral_user=None):
    cid = bot.user.id if bot.user else 0
    embed = discord.Embed(
        title="Autorisations de Bone",
        description=(
            "Clique un bouton = Discord s'ouvre, tu **re-choisis le serveur**, Autoriser.\n"
            "Ça **ajoute** des droits, ça n'enlève rien.\n\n"
            f"**Droits actuels**\n{_perm_lines(getattr(dest, 'guild', None))}"
        ),
        color=0xE0A100,
    )
    view = AutorisationsView(cid)
    if ephemeral_user is not None:
        await dest.response.send_message(embed=embed, view=view, ephemeral=True)
    else:
        await dest.send(embed=embed, view=view)


@bot.tree.command(name="autorisations", description="Ajouter des droits / connexions Discord à Bone (après install)")
async def slash_autorisations(interaction: discord.Interaction):
    await _send_autorisations(interaction, ephemeral_user=True)


@bot.tree.command(name="cerveau", description="Quelle IA parle : papier, Groq, OpenAI, Ollama")
async def slash_cerveau(interaction: discord.Interaction):
    try:
        from llm import describe
        txt = describe()
    except Exception:
        txt = "papier"
    await interaction.response.send_message(
        f"Cerveau actuel : **{txt}**\n"
        "Pour brancher une vraie IA : `autorisations.bat` → option 3 (clé) puis relance Bone.",
        ephemeral=True,
    )


@bot.tree.command(name="aide", description="Bone explique (très mal) comment il marche")
async def slash_aide(interaction: discord.Interaction):
    await interaction.response.send_message(help_text(), ephemeral=True)


@bot.tree.command(name="bone", description="Parler à Bone")
@app_commands.describe(texte="Ce que tu lui dis")
async def slash_bone(interaction: discord.Interaction, texte: str):
    out = bone_reply(texte, channel_id=str(interaction.channel_id or "slash"), author=interaction.user.display_name)
    await interaction.response.send_message(out)


@bot.tree.command(name="roast", description="Bone te vanne, South Park style")
async def slash_roast(interaction: discord.Interaction):
    out = bone_reply("roast", channel_id=str(interaction.channel_id or "slash"), author=interaction.user.display_name)
    await interaction.response.send_message(out)


@bot.tree.command(name="mood", description="Humeur de Bone : chill, agace, mort, hype, high")
@app_commands.describe(humeur="chill | agace | mort | hype | high")
@app_commands.choices(humeur=[
    app_commands.Choice(name="chill", value="chill"),
    app_commands.Choice(name="agacé", value="agace"),
    app_commands.Choice(name="mort", value="mort"),
    app_commands.Choice(name="hype", value="hype"),
    app_commands.Choice(name="high (Servietsky)", value="high"),
])
async def slash_mood(interaction: discord.Interaction, humeur: app_commands.Choice[str]):
    set_mood(str(interaction.channel_id or "slash"), humeur.value)
    await interaction.response.send_message(f"Mood **{humeur.value}**. Ça va durer deux messages, max.")


@bot.tree.command(name="episode", description="Titre d'épisode South Park / Olympus")
async def slash_episode(interaction: discord.Interaction):
    out = bone_reply("épisode", channel_id=str(interaction.channel_id or "slash"))
    await interaction.response.send_message(out)


@bot.tree.command(name="projets", description="Bone récite les repos de Satan")
async def slash_projets(interaction: discord.Interaction):
    out = bone_reply("projets", channel_id=str(interaction.channel_id or "slash"))
    await interaction.response.send_message(out)


def main() -> None:
    log_file = ROOT / "bone.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file, encoding="utf-8"),
        ],
    )
    if not TOKEN:
        raise SystemExit(
            "DISCORD_TOKEN manquant.\n"
            "1. https://discord.com/developers/applications → New Application « Bone »\n"
            "2. Bot → Add Bot → Reset Token → copier\n"
            "3. Privileged Gateway Intents : MESSAGE CONTENT INTENT = ON\n"
            "4. projects/bone/.env → DISCORD_TOKEN=...\n"
            "5. OAuth2 → URL Generator → scopes bot + applications.commands\n"
            "   permissions : Send Messages, Read History, Embed Links, Add Reactions, View Channels\n"
            "6. Inviter l'URL sur le serveur Olympus, puis relancer."
        )
    log.info("Cible : serveur %s · chatty=%s · salons=%s", GUILD_NAME, CHATTY, ",".join(sorted(CHATTY_CHANNELS)))
    bot.run(TOKEN, log_handler=None)


if __name__ == "__main__":
    main()
