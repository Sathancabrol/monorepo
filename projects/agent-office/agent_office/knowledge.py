"""Service KNOWLEDGE — mémoire SQLite + graphe de connaissances de l'agent.

Pattern « AI Agent + SQLite + knowledge graph » (veille 09/10) : une base
unique et requêtable qui unifie prospects, budget, ELO arena, leçons et
citations, plus un graphe nœuds/arêtes (style Cognitorium). Stdlib sqlite3.
"""
import argparse
import csv
import json
import sqlite3
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
DB = DATA / "agent_office.db"

CAPABILITY = {
    "name": "knowledge",
    "service": "Mémoire",
    "capability": "Base SQLite + graphe de connaissances : ingestion des données agent-office, requêtes, visualisation du graphe",
    "commands": ["knowledge init", "knowledge ingest", "knowledge graph [--type t]", "knowledge query --texte t"],
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS nodes(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  label TEXT NOT NULL, type TEXT NOT NULL, attrs TEXT DEFAULT '{}',
  UNIQUE(label, type)
);
CREATE TABLE IF NOT EXISTS edges(
  src INTEGER NOT NULL, dst INTEGER NOT NULL, type TEXT NOT NULL,
  FOREIGN KEY(src) REFERENCES nodes(id), FOREIGN KEY(dst) REFERENCES nodes(id),
  UNIQUE(src,dst,type)
);
"""


def connect(path=DB):
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(path))
    con.executescript(SCHEMA)
    return con


def upsert_node(con, label, type_, attrs=None):
    con.execute(
        "INSERT INTO nodes(label,type,attrs) VALUES(?,?,?) "
        "ON CONFLICT(label,type) DO UPDATE SET attrs=excluded.attrs",
        (label, type_, json.dumps(attrs or {}, ensure_ascii=False)),
    )
    return con.execute("SELECT id FROM nodes WHERE label=? AND type=?", (label, type_)).fetchone()[0]


def add_edge(con, src, dst, type_):
    con.execute("INSERT OR IGNORE INTO edges(src,dst,type) VALUES(?,?,?)", (src, dst, type_))


def load(path, default):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def ingest(con, base=None):
    base = base or DATA
    n = 0
    # offres (source : marketing)
    from .marketing import OFFERS
    for k, o in OFFERS.items():
        upsert_node(con, f"{k} — {o['titre']}", "offre", {"promesse": o["promesse"], "prix": o["prix"]})
        n += 1
    # prospects
    for p in load(base / "prospects.json", []):
        nid = upsert_node(con, p["nom"], "prospect", {"org": p.get("org", ""), "etape": p["etape"]})
        oid = upsert_node(con, f"{p['offre']} — offre", "offre", {})
        add_edge(con, nid, oid, "vise")
        n += 1
    # ELO arena (modèles)
    for modele, score in load(base / "arena_elo.json", {}).items():
        upsert_node(con, modele, "modele", {"elo": score})
        n += 1
    # leçons (update lessons)
    for l in load(base / "update_lessons.json", []):
        upsert_node(con, l["lecon"], "lecon", {"date": l["date"]})
        n += 1
    # citations (research)
    for c in load(base / "citations.json", []):
        upsert_node(con, c["titre"], "source", {"url": c["url"]})
        n += 1
    # budget (csv)
    csv_path = base / "budget_transactions.csv"
    if csv_path.exists():
        with open(csv_path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                upsert_node(con, row["libelle"], "flux_budget",
                            {"montant": row["montant"], "type": row["type"], "statut": row["statut"]})
                n += 1
    con.commit()
    return n


def cmd_init(args):
    con = connect()
    con.close()
    print(f"✅ base prête : {DB}")
    return 0


def cmd_ingest(args):
    con = connect()
    n = ingest(con)
    total = con.execute("SELECT COUNT(*) FROM nodes").fetchone()[0]
    con.close()
    print(f"✅ {n} éléments ingérés — {total} nœuds au total dans {DB.name}")
    return 0


def cmd_graph(args):
    con = connect()
    q = "SELECT label,type FROM nodes" + (" WHERE type=?" if args.type else "")
    rows = con.execute(q, (args.type,) if args.type else ()).fetchall()
    print(f"🕸 GRAPHE — {len(rows)} nœuds" + (f" (type {args.type})" if args.type else ""))
    for label, t in rows[:40]:
        edges = con.execute(
            "SELECT n.label, e.type FROM edges e JOIN nodes n ON n.id=e.dst WHERE e.src=("
            "SELECT id FROM nodes WHERE label=? AND type=?)", (label, t)).fetchall()
        suite = " → " + ", ".join(f"{tt}:{ll}" for ll, tt in edges) if edges else ""
        print(f"  [{t}] {label}{suite}")
    con.close()
    return 0


def cmd_query(args):
    con = connect()
    like = f"%{args.texte}%"
    rows = con.execute(
        "SELECT label,type,attrs FROM nodes WHERE label LIKE ? OR attrs LIKE ?", (like, like)).fetchall()
    for label, t, attrs in rows:
        print(f"  [{t}] {label} — {attrs}")
    print(f"({len(rows)} résultat(s))")
    con.close()
    return 0


def main(argv):
    p = argparse.ArgumentParser(prog="knowledge", description="Mémoire SQLite + graphe")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init").set_defaults(fn=cmd_init)
    sub.add_parser("ingest").set_defaults(fn=cmd_ingest)
    g = sub.add_parser("graph")
    g.add_argument("--type")
    g.set_defaults(fn=cmd_graph)
    q = sub.add_parser("query")
    q.add_argument("--texte", required=True)
    q.set_defaults(fn=cmd_query)
    args = p.parse_args(argv)
    return args.fn(args)


def selftest():
    con = connect()
    n = ingest(con)
    assert n > 0
    con.close()
    return f"knowledge OK — SQLite + graphe, {n} éléments ingérables"
