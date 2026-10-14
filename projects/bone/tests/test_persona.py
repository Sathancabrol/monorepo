import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from persona import reply, match_intent, detect_lang, opener, help_text, set_mood, channel_state


def test_greet_mentions_bone():
    t = reply("salut", channel_id="t-greet")
    assert t
    assert len(t) > 8


def test_who():
    t = reply("t'es qui ?", channel_id="t-who")
    low = t.lower()
    assert "bone" in low or "os" in low or "squelette" in low or "south park" in low


def test_intent_roast():
    intent = match_intent("roast-moi fort")
    assert intent and intent["id"] == "roast"


def test_intent_watchtower():
    intent = match_intent("c'est quoi watchtower")
    assert intent and intent["id"] == "watchtower"
    t = reply("c'est quoi watchtower", channel_id="t-wt")
    assert "tour" in t.lower() or "globe" in t.lower() or "œil" in t.lower() or "oeil" in t.lower() or "watchtower" in t.lower()


def test_lang_en():
    assert detect_lang("who are you and what is this") == "en"
    t = reply("who are you", channel_id="t-en")
    assert t


def test_quiet_toggle():
    a = reply("tg", channel_id="t-q")
    assert "tais" in a.lower() or "silence" in a.lower() or "parle" in a.lower()
    b = reply("parle", channel_id="t-q")
    assert b


def test_opener_and_help():
    o = opener()
    assert isinstance(o, str) and len(o) > 10
    h = help_text()
    assert "/roast" in h and "!bone" in h


def test_mood():
    set_mood("t-m", "high")
    assert channel_state("t-m")["mood"] == "high"


def test_no_assistant_voice():
    t = reply("qui es-tu", channel_id="t-voice")
    assert "en tant qu" not in t.lower()
    assert "as an ai" not in t.lower()
