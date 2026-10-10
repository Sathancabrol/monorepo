"""Bone — cerveau partagé (playground + bot Discord)."""
from __future__ import annotations

import json
import random
import re
import unicodedata
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent / "persona.json"
DATA = json.loads(DATA_PATH.read_text(encoding="utf-8"))

FR_HINTS = (
    " le ", " la ", " les ", " un ", " une ", " des ", " je ", " tu ", " on ",
    " pas ", " que ", " et ", " c'est ", " ça", " ca ", "oui", "non", "quoi",
    "wesh", "putain", "salut", "merci", "chef", "ouais", "t'es", "j'suis",
)
EN_HINTS = (
    " the ", " you ", " are ", " is ", " and ", " what ", " who ", " how ",
    "hey", "hello", "thanks", "please", "what's", "i'm ",
)

_CHANNEL_MEM: dict[str, dict] = {}


def _strip(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", s).strip()


def detect_lang(text: str) -> str:
    t = f" {_strip(text)} "
    fr = sum(1 for h in FR_HINTS if h in t)
    en = sum(1 for h in EN_HINTS if h in t)
    if en > fr + 1:
        return "en"
    return "fr"


def _score(text_n: str, keys: list[str]) -> int:
    score = 0
    for k in keys:
        kn = _strip(k)
        if not kn:
            continue
        if kn in text_n:
            score += max(3, len(kn))
    return score


def match_intent(text: str) -> dict | None:
    tn = f" {_strip(text)} "
    best, best_s = None, 0
    for intent in DATA["intents"]:
        s = _score(tn, intent["keys"])
        if s > best_s:
            best, best_s = intent, s
    if best_s < 3:
        return None
    return best


def _pick(seq: list[str], avoid: str | None = None) -> str:
    if not seq:
        return "Ouais."
    choices = [x for x in seq if x != avoid] or seq
    return random.choice(choices)


def channel_state(channel_id: str) -> dict:
    st = _CHANNEL_MEM.setdefault(
        channel_id,
        {"mood": "chill", "last": None, "history": [], "quiet": False},
    )
    return st


def set_mood(channel_id: str, mood: str) -> str:
    if mood not in DATA["moods"]:
        mood = "chill"
    channel_state(channel_id)["mood"] = mood
    return mood


def set_quiet(channel_id: str, quiet: bool) -> None:
    channel_state(channel_id)["quiet"] = quiet


def opener(lang: str = "fr") -> str:
    bag = DATA["openers"].get(lang) or DATA["openers"]["fr"]
    return random.choice(bag)


def _decorate(text: str, mood: str) -> str:
    info = DATA["moods"].get(mood) or DATA["moods"]["chill"]
    prefixes = info.get("prefix") or []
    if prefixes and random.random() < 0.45:
        p = random.choice(prefixes)
        if not text.startswith(p):
            return f"{p} {text}"
    return text


def system_prompt(lang: str = "fr", author: str | None = None, mood: str = "chill") -> str:
    ident = DATA.get("identity", {})
    style = "\n".join(f"- {s}" for s in DATA.get("style", []))
    kn = "\n".join(f"- {k}: {v}" for k, v in DATA.get("knowledge", {}).items())
    who = author or "un humain"
    if lang == "en":
        return (
            f"You are {ident.get('name', 'Bone')}, {ident.get('species')}. "
            f"You live on Discord server {ident.get('server')}. Boss: {ident.get('owner')}. "
            f"Job: {ident.get('job')}. Catchphrase: {ident.get('catchphrase')}. "
            f"Mood now: {mood}. Talking to: {who}.\n"
            f"Style:\n{style}\n"
            f"You know these projects:\n{kn}\n"
            "You are a real AI agent wearing this character. Short answers (1–4 sentences). "
            "Never say you are ChatGPT, Claude, Groq, or Llama. You are Bone."
        )
    return (
        f"Tu es {ident.get('name', 'Bone')}, {ident.get('species')}. "
        f"Tu habites le serveur Discord {ident.get('server')}. Patron : {ident.get('owner')}. "
        f"Job : {ident.get('job')}. Punchline : {ident.get('catchphrase')}. "
        f"Humeur : {mood}. Tu parles à : {who}.\n"
        f"Style :\n{style}\n"
        f"Tu connais ces projets :\n{kn}\n"
        "Tu es un VRAI agent IA, déguisé en ce perso. Réponses courtes (1 à 4 phrases). "
        "Jamais dire que tu es ChatGPT, Claude, Groq ou Llama. T'es Bone."
    )


def think(text: str, channel_id: str = "default", author: str | None = None) -> str:
    """Cerveau : vraie IA si une clé est là, sinon répliques papier."""
    st = channel_state(channel_id)
    raw = (text or "").strip()
    lowered = _strip(raw)
    if lowered in {"tg", "silence", "chut", "quiet", "parle", "speak", "reviens"}:
        return reply(text, channel_id=channel_id, author=author)

    try:
        from llm import complete, provider
    except Exception:
        return reply(text, channel_id=channel_id, author=author)

    if not provider():
        return reply(text, channel_id=channel_id, author=author)

    lang = detect_lang(raw)
    sys = system_prompt(lang=lang, author=author, mood=st.get("mood") or "chill")
    messages = [{"role": "system", "content": sys}]
    for h in st.get("history") or []:
        role = "assistant" if h.get("role") == "bone" else "user"
        content = (h.get("text") or "").strip()
        if content:
            messages.append({"role": role, "content": content})
    messages.append({"role": "user", "content": raw if not author else f"{author}: {raw}"})
    out = complete(messages)
    if not out:
        return reply(text, channel_id=channel_id, author=author)
    # coupe si le modèle bavarde
    if len(out) > 800:
        out = out[:797] + "…"
    st["last"] = out
    hist = st["history"]
    hist.append({"role": "user", "text": raw})
    hist.append({"role": "bone", "text": out})
    del hist[:-16]
    return out


def reply(text: str, channel_id: str = "default", author: str | None = None) -> str:
    """Réponse Bone. Déterministe-ish : intent + mood + anti-répétition."""
    st = channel_state(channel_id)
    raw = (text or "").strip()
    if not raw:
        return opener()

    lowered = _strip(raw)
    if lowered in {"tg", "silence", "chut", "quiet"}:
        st["quiet"] = True
        return "Ok. J'me tais. Rappelle-moi avec !bone parle."
    if lowered in {"parle", "speak", "reviens"}:
        st["quiet"] = False
        return "Ok. J'parle. Ça t'étonne ?"

    lang = detect_lang(raw)
    intent = match_intent(raw)

    # mood nudges
    if intent and intent["id"] in {"insult"}:
        st["mood"] = "agace"
    elif intent and intent["id"] in {"towelie"}:
        st["mood"] = "high"
    elif intent and intent["id"] in {"love", "thanks"}:
        st["mood"] = "chill"
    elif intent and intent["id"] in {"episode", "hype"}:
        st["mood"] = "hype"
    elif intent and intent["id"] in {"death"}:
        st["mood"] = "mort"

    if intent:
        bag = intent.get(lang) or intent.get("fr") or []
        text_out = _pick(bag, avoid=st.get("last"))
    else:
        # knowledge snippets
        kn = None
        for key, blurb in DATA["knowledge"].items():
            if _strip(key) in lowered:
                kn = blurb
                break
        if kn:
            if lang == "en":
                text_out = kn
            else:
                text_out = kn if kn[:1].isupper() else kn
            # wrap in voice
            wraps_fr = [
                f"{kn} Voilà. J'ai lu le README. T'es fier ?",
                f"Ouais. {kn}",
                f"{kn} Demande-moi le roast si tu veux la version méchante.",
            ]
            wraps_en = [kn, f"Yeah. {kn}"]
            text_out = _pick(wraps_en if lang == "en" else wraps_fr, avoid=st.get("last"))
        else:
            bag = DATA["fallback"].get(lang) or DATA["fallback"]["fr"]
            text_out = _pick(bag, avoid=st.get("last"))

    if author and random.random() < 0.18 and intent and intent["id"] in {"greet", "how"}:
        name = author.split("#")[0]
        if lang == "en":
            text_out = f"{name}. {text_out}"
        else:
            text_out = f"{name}. {text_out}"

    text_out = _decorate(text_out, st["mood"])
    st["last"] = text_out
    hist = st["history"]
    hist.append({"role": "user", "text": raw})
    hist.append({"role": "bone", "text": text_out})
    del hist[:-16]
    return text_out


def help_text(lang: str = "fr") -> str:
    if lang == "en":
        return (
            "**Bone** — South Park skeleton intern on Olympus.\n"
            "Ping me, reply, or `!bone …`\n"
            "`/aide` `/roast` `/mood` `/episode` `/projets` `/autorisations` `/cerveau`\n"
            "`!bone tg` silence · `!bone parle` resume"
        )
    return (
        "**Bone** — stagiaire squelette d'Olympus, construction paper.\n"
        "Ping-moi, réponds-moi, ou `!bone …`\n"
        "`/aide` `/roast` `/mood` `/episode` `/projets` `/autorisations` `/cerveau`\n"
        "`!bone tg` je me tais · `!bone parle` je reviens\n"
        "IA : colle une clé (Groq / OpenAI / Ollama) dans autorisations.bat → 3. "
        "`/cerveau` dit si c'est du papier ou une vraie IA."
    )
