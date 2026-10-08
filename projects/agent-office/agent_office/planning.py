"""Service PLANNING — agenda hebdo + export .ics (importable Google Calendar)."""
import argparse
import datetime as dt
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "tasks.json"
OUT = Path(__file__).resolve().parent.parent / "out"

CAPABILITY = {
    "name": "planning",
    "service": "Organisation",
    "capability": "Agenda de tâches, ajout, export .ics pour Google Calendar",
    "commands": ["planning week [--start AAAA-MM-JJ]", "planning add --titre t --date AAAA-MM-JJ [--duree 60]", "planning ics [--days 14]"],
}


def load():
    return json.loads(DATA.read_text(encoding="utf-8"))


def save(db):
    DATA.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")


def ics_escape(s):
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def build_ics(tasks, days=14, start=None):
    start = dt.date.fromisoformat(start) if start else dt.date.today()
    end = start + dt.timedelta(days=days)
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//agent-office//FR", "CALSCALE:GREGORIAN"]
    for t in tasks:
        d = dt.date.fromisoformat(t["date"])
        if not (start <= d <= end):
            continue
        dur = int(t.get("duree", 60))
        hh, mm = t.get("heure", "09:00").split(":")
        s = dt.datetime(d.year, d.month, d.day, int(hh), int(mm))
        e = s + dt.timedelta(minutes=dur)
        lines += [
            "BEGIN:VEVENT",
            f"UID:{t['id']}@agent-office",
            f"DTSTART:{s.strftime('%Y%m%dT%H%M%S')}",
            f"DTEND:{e.strftime('%Y%m%dT%H%M%S')}",
            f"SUMMARY:{ics_escape(t['titre'])}",
            "END:VEVENT",
        ]
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n"


def main(argv):
    p = argparse.ArgumentParser(prog="planning", description="Planning & export ICS")
    sub = p.add_subparsers(dest="cmd", required=True)
    w = sub.add_parser("week")
    w.add_argument("--start", help="AAAA-MM-JJ (défaut : aujourd'hui)")
    a = sub.add_parser("add")
    a.add_argument("--titre", required=True)
    a.add_argument("--date", required=True)
    a.add_argument("--heure", default="09:00")
    a.add_argument("--duree", type=int, default=60)
    i = sub.add_parser("ics")
    i.add_argument("--days", type=int, default=14)
    i.add_argument("--start")
    i.add_argument("--out")
    args = p.parse_args(argv)
    db = load()
    if args.cmd == "week":
        start = dt.date.fromisoformat(args.start) if args.start else dt.date.today()
        week = [start + dt.timedelta(days=i) for i in range(7)]
        for d in week:
            iso = d.isoformat()
            day_tasks = [t for t in db if t["date"] == iso]
            label = ["lun", "mar", "mer", "jeu", "ven", "sam", "dim"][d.weekday()]
            print(f"{label} {iso} : " + ("; ".join(t["titre"] for t in day_tasks) if day_tasks else "—"))
        return 0
    if args.cmd == "add":
        nid = max([t["id"] for t in db], default=0) + 1
        db.append({"id": nid, "titre": args.titre, "date": args.date, "heure": args.heure, "duree": args.duree})
        save(db)
        print(f"✅ tâche {nid} : « {args.titre} » le {args.date} à {args.heure}")
        return 0
    if args.cmd == "ics":
        OUT.mkdir(exist_ok=True)
        path = Path(args.out) if args.out else OUT / "agenda.ics"
        path.write_text(build_ics(db, args.days, args.start), encoding="utf-8")
        print(f"✅ {path} — à importer dans Google Calendar (Paramètres → Importer)")
        return 0
    return 2


def selftest():
    ics = build_ics(load(), days=400)
    assert "BEGIN:VCALENDAR" in ics
    n = ics.count("BEGIN:VEVENT")
    return f"planning OK — {len(load())} tâches, export ICS fonctionnel"
