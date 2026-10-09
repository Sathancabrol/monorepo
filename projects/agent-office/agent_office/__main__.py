"""Dispatcher CLI : python3 -m agent_office <service> [args...]"""
import sys

from . import arena, budget, invoices, knowledge, maildigest, marketing, planning, prospects, registry, research, social, update

SERVICES = {
    "budget": budget,
    "invoices": invoices,
    "marketing": marketing,
    "prospects": prospects,
    "research": research,
    "mail": maildigest,
    "planning": planning,
    "arena": arena,
    "social": social,
    "knowledge": knowledge,
    "update": update,
    "registry": registry,
}

USAGE = """agent-office — l'entreprise d'IA (bureautique, mail, budget, marketing, recherche)

Usage: python3 -m agent_office <service> [options]

Services:
  budget     suivi budget (report/add) — seedé depuis USER/FINANCES
  invoices   devis & factures conformes France (franchise TVA)
  marketing  one-pager / séquence prospection / posts — offres O1,O2,O3
  prospects  mini-CRM pipeline + relances dues
  research   briefs, citations, veille (avec reaserch-engine)
  mail       digest IMAP lecture seule des non-lus
  planning   agenda hebdo + export .ics
  arena      confrontation de modèles : duels en aveugle + ELO + grille ChatEval
  social     équipe réseaux : calendrier, drafts par plateforme, checklist, écoute
  knowledge  mémoire SQLite + graphe de connaissances (ingest/graph/query)
  update     auto-mise à jour : journal, leçons, changelog, check
  registry   registre des capacités (tools.json) + doctor

Chaque service : python3 -m agent_office <service> --help
"""


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help"):
        print(USAGE)
        return 0
    name, rest = argv[0], argv[1:]
    mod = SERVICES.get(name)
    if mod is None:
        print(f"service inconnu : {name}\n\n{USAGE}")
        return 2
    return mod.main(rest)


if __name__ == "__main__":
    raise SystemExit(main())
