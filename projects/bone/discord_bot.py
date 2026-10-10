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

import os
import re
import sys
import logging
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from persona import reply as bone_reply, opener, help_text, set_mood, set_quiet, channel_state, DATA

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

INTENTS = discord.Intents.default()
INTENTS.message_content = True
INTENTS.guilds = True
INTENTS.messages = True

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


@bot.event
async def on_ready():
    log.info("Bone en ligne : %s (id=%s)", bot.user, bot.user.id if bot.user else "?")
    activity = discord.Activity(type=discord.ActivityType.watching, name="South Park · Olympus")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    try:
        synced = await bot.tree.sync()
        log.info("slash commands : %s", [c.name for c in synced])
    except Exception as e:
        log.warning("sync slash : %s", e)


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
    async with msg.channel.typing():
        out = bone_reply(text, channel_id=cid, author=msg.author.display_name)
    await msg.reply(out, mention_author=False)


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
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
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
