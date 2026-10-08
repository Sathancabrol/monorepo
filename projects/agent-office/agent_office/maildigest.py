"""Service MAIL — digest IMAP en LECTURE SEULE.

Jamais de suppression, jamais de déplacement : on lit, on groupe, on résume.
Config via .env local (comme mail-organizer) : MAIL_HOST, MAIL_USER, MAIL_APP_PASSWORD.
`--demo` montre le format de sortie sans connexion.
"""
import argparse
import email
import imaplib
from collections import Counter
from email.header import decode_header, make_header
from pathlib import Path

ENV = Path(__file__).resolve().parent.parent / ".env"

CAPABILITY = {
    "name": "mail",
    "service": "Courrier",
    "capability": "Digest des mails non lus groupés par expéditeur (IMAP lecture seule, zéro suppression)",
    "commands": ["mail digest [--limit 30]", "mail digest --demo"],
}

SETUP_HELP = """ℹ️  Non configuré : créez projects/agent-office/.env :
   MAIL_HOST=imap.gmail.com
   MAIL_USER=votre.adresse@gmail.com
   MAIL_APP_PASSWORD=mot-de-passe-application
(ou réutilisez la config de projects/mail-organizer/.env)"""


def load_env(path=ENV):
    if not path.exists():
        alt = Path(__file__).resolve().parent.parent.parent / "mail-organizer" / ".env"
        if alt.exists():
            path = alt
        else:
            return {}
    env = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


def decode_subject(raw):
    try:
        return str(make_header(decode_header(raw or "")))
    except Exception:
        return raw or "(sans objet)"


def digest(limit=30):
    env = load_env()
    if not all(k in env for k in ("MAIL_HOST", "MAIL_USER", "MAIL_APP_PASSWORD")):
        print(SETUP_HELP)
        return 1
    try:
        box = imaplib.IMAP4_SSL(env["MAIL_HOST"])
        box.login(env["MAIL_USER"], env["MAIL_APP_PASSWORD"])
        box.select("INBOX")
        _, data = box.search(None, "UNSEEN")
        ids = data[0].split()[-limit:]
        senders, subjects = Counter(), []
        for mid in ids:
            _, msg = box.fetch(mid, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])")
            m = email.message_from_bytes(msg[0][1])
            frm = str(make_header(decode_header(m.get("From", "?"))))
            senders[frm] += 1
            subjects.append((frm, decode_subject(m.get("Subject")), m.get("Date", "")))
        box.logout()
    except Exception as e:
        print(f"❌ erreur IMAP : {e}")
        return 1
    print(f"📬 {len(ids)} non-lus (derniers)\n\nPar expéditeur :")
    for frm, n in senders.most_common(10):
        print(f"  {n:>3} × {frm}")
    print("\nDerniers sujets :")
    for frm, subj, date in subjects[-15:]:
        print(f"  • [{date[:16]}] {subj} — {frm.split('<')[0].strip()}")
    return 0


def demo():
    print("""📬 12 non-lus (démo — format réel)

Par expéditeur :
    4 × France Travail <noreply@francetravail.fr>
    3 → EDENRED / newsletters
    2 → Sobeca réseau
    3 → divers

Derniers sujets :
  • [2026-10-08 09:12] Votre actualisation du mois — France Travail
  • [2026-10-07 18:40] Actualisation hebdo n°42 — Sobeca
→ jamais de suppression ; le tri réel se fait avec projects/mail-organizer.""")
    return 0


def main(argv):
    p = argparse.ArgumentParser(prog="mail", description="Digest mails non lus (lecture seule)")
    sub = p.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("digest")
    d.add_argument("--limit", type=int, default=30)
    d.add_argument("--demo", action="store_true")
    args = p.parse_args(argv)
    return demo() if args.demo else digest(args.limit)


def selftest():
    env = load_env()
    state = "configuré" if all(k in env for k in ("MAIL_HOST", "MAIL_USER", "MAIL_APP_PASSWORD")) else "non configuré (.env attendu)"
    return f"mail OK — digest lecture seule, {state}"
