import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from perms import bits_for, invite_url, PACKS


def test_base_has_send_and_slash():
    n = bits_for("base")
    assert n & (1 << 11)  # send
    assert n & (1 << 31)  # slash
    assert n & (1 << 10)  # view


def test_admin_is_just_admin():
    assert bits_for("admin") == 8


def test_invite_adds_base():
    url = invite_url("42", "moderation")
    assert "client_id=42" in url
    assert "scope=bot%20applications.commands" in url
    assert str(bits_for("base", "moderation")) in url


def test_all_packs_named():
    for k in ("base", "moderation", "vocal", "salons", "roles", "webhooks", "admin"):
        assert k in PACKS
        assert bits_for(k) > 0
