"""Packs d'autorisations Discord + URL d'invitation (ré-auth après install)."""
from __future__ import annotations

# bits Discord (Permissions)
P = {
    "create_invite": 1 << 0,
    "kick": 1 << 1,
    "ban": 1 << 2,
    "admin": 1 << 3,
    "manage_channels": 1 << 4,
    "manage_guild": 1 << 5,
    "add_reactions": 1 << 6,
    "view_audit": 1 << 7,
    "priority_speaker": 1 << 8,
    "stream": 1 << 9,
    "view_channel": 1 << 10,
    "send_messages": 1 << 11,
    "manage_messages": 1 << 13,
    "embed_links": 1 << 14,
    "attach_files": 1 << 15,
    "read_history": 1 << 16,
    "mention_everyone": 1 << 17,
    "external_emojis": 1 << 18,
    "connect": 1 << 20,
    "speak": 1 << 21,
    "mute": 1 << 22,
    "deafen": 1 << 23,
    "move": 1 << 24,
    "vad": 1 << 25,
    "change_nick": 1 << 26,
    "manage_nicks": 1 << 27,
    "manage_roles": 1 << 28,
    "manage_webhooks": 1 << 29,
    "slash": 1 << 31,
    "manage_events": 1 << 33,
    "manage_threads": 1 << 34,
    "public_threads": 1 << 35,
    "private_threads": 1 << 36,
    "send_in_threads": 1 << 38,
    "moderate": 1 << 40,
    "send_voice_messages": 1 << 46,
}

PACKS: dict[str, tuple[str, tuple[str, ...]]] = {
    "base": (
        "Lecture + parler + slash (install par défaut)",
        (
            "view_channel", "send_messages", "embed_links", "attach_files",
            "read_history", "add_reactions", "external_emojis", "slash",
            "send_in_threads", "change_nick", "public_threads", "private_threads",
        ),
    ),
    "moderation": (
        "Modération (kick, timeout, messages, audit)",
        ("kick", "ban", "manage_messages", "moderate", "view_audit"),
    ),
    "vocal": (
        "Vocal (rejoindre, parler, mute, move)",
        ("connect", "speak", "mute", "deafen", "move", "vad", "stream"),
    ),
    "salons": (
        "Salons & threads (créer / gérer)",
        ("manage_channels", "manage_threads", "manage_events"),
    ),
    "roles": (
        "Rôles & pseudos",
        ("manage_roles", "manage_nicks"),
    ),
    "webhooks": (
        "Webhooks",
        ("manage_webhooks",),
    ),
    "admin": (
        "Administrateur (tout) — à éviter",
        ("admin",),
    ),
}


def bits_for(*pack_ids: str) -> int:
    acc = 0
    for pid in pack_ids:
        if pid not in PACKS:
            continue
        _label, keys = PACKS[pid]
        for k in keys:
            acc |= P[k]
    return acc


def invite_url(client_id: str | int, *pack_ids: str) -> str:
    packs = pack_ids or ("base",)
    if "admin" in packs:
        n = P["admin"]
    else:
        ids = []
        if "base" not in packs:
            ids.append("base")
        ids.extend(packs)
        n = bits_for(*ids)
    return (
        "https://discord.com/oauth2/authorize"
        f"?client_id={client_id}&permissions={n}"
        "&scope=bot%20applications.commands"
    )


def portal_bot_url(client_id: str | int) -> str:
    return f"https://discord.com/developers/applications/{client_id}/bot"


def portal_oauth_url(client_id: str | int) -> str:
    return f"https://discord.com/developers/applications/{client_id}/oauth2/url-generator"
