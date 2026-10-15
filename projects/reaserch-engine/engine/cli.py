"""Command line entry point for the iterative retrieval layer.

    python3 -m engine.cli "ma question"                 # providers from the environment
    python3 -m engine.cli "ma question" --demo          # offline fictional corpus
    python3 -m engine.cli --check                       # are my providers reachable?
    python3 -m engine.cli "ma question" --json out.json # full machine-readable report

Fail-soft by design: a provider that is down is reported, the run continues with
the others, and the exit code stays 0 unless the question itself was unusable
(exit 2). ``--check`` exits 1 when no provider answered, which is what a cron
job or ``doctor.py``-style probe needs.
"""

from __future__ import annotations

import argparse
import json
import sys

from .iteration import IterativeSearch
from .settings import RetrievalSettings, build_federated

EXIT_OK = 0
EXIT_NO_PROVIDER = 1
EXIT_BAD_USAGE = 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python3 -m engine.cli",
        description="Research Engine — itérer la recherche : requêtes → couverture → manques → enrichissement.",
    )
    parser.add_argument("question", nargs="?", help="question de recherche (français ou anglais)")
    parser.add_argument("--demo", action="store_true", help="corpus fictif hors-ligne (aucun réseau)")
    parser.add_argument("--check", action="store_true", help="sonder les fournisseurs configurés puis sortir")
    parser.add_argument("--rounds", type=int, default=None, help="nombre de tours (défaut: RESEARCH_MAX_ROUNDS ou 3)")
    parser.add_argument("--per-query", type=int, default=None, help="résultats visés par requête et par fournisseur")
    parser.add_argument("--max-queries", type=int, default=None, help="plafond de requêtes distinctes")
    parser.add_argument("--language", default=None, choices=["fr", "en"], help="langue des requêtes de relance")
    parser.add_argument("--no-enrich", action="store_true", help="désactiver l'enrichissement du corpus")
    parser.add_argument("--json", metavar="CHEMIN", help="écrire le rapport complet en JSON")
    parser.add_argument("--top", type=int, default=8, help="nombre de sources affichées (défaut: 8)")
    return parser


def run(args, *, out=print) -> tuple[int, dict]:
    settings = RetrievalSettings.from_env()
    language = args.language or settings.language
    max_rounds = args.rounds or settings.max_rounds
    per_query = args.per_query or settings.results_per_query

    if args.check:
        return _check(settings, max_rounds=max_rounds, per_query=per_query, language=language, out=out)

    if not args.question:
        out("erreur : indique une question, ou --check pour sonder les fournisseurs")
        return EXIT_BAD_USAGE, {}

    if args.demo:
        from .demo import DEMO_QUESTION, DEMO_SUBQUESTIONS, build_demo_iteration
        question = args.question if args.question != "demo" else DEMO_QUESTION
        search = build_demo_iteration(max_rounds=max_rounds, results_per_query=per_query, language=language)
        subquestions = DEMO_SUBQUESTIONS
        out("MODE DÉMO — corpus fictif, aucune valeur de preuve (aucun réseau utilisé).\n")
    else:
        federated = build_federated(settings)
        search = IterativeSearch(federated, max_rounds=max_rounds, results_per_query=per_query,
                                 max_queries=args.max_queries, enrich=not args.no_enrich)
        subquestions = ()
        out(f"fournisseurs : {', '.join(federated.provider_names()) or '(aucun)'}")
        out(f"réglages      : {json.dumps(settings.as_dict(), ensure_ascii=False)}\n")

    report = search.run(question, subquestions=subquestions)
    _print_report(report, out=out, top=args.top)
    payload = report.as_dict()

    if args.json:
        with open(args.json, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
        out(f"\nrapport écrit : {args.json}")

    if not report.corpus and not args.demo:
        out("\naucune source récupérée : vérifie que SearXNG et Crawl4AI tournent en local "
            "(audit/stack/docker-compose.yml) puis relance --check.")
        return EXIT_NO_PROVIDER, payload
    return EXIT_OK, payload


def _check(settings, *, max_rounds: int, per_query: int, language: str, out) -> tuple[int, dict]:
    """Probe each configured provider with one real query and report honestly."""
    from .retrieval import SearchRequest
    retrievers = {}
    try:
        from .settings import build_retrievers
        retrievers = build_retrievers(settings, )
    except Exception as exc:  # noqa: BLE001 - a broken configuration must not traceback
        out(f"configuration invalide : {type(exc).__name__}: {exc}")
        return EXIT_BAD_USAGE, {}

    out(f"réglages : {json.dumps(settings.as_dict(), ensure_ascii=False)}\n")
    reachable = 0
    results_map = {}
    for name, retriever in retrievers.items():
        request = SearchRequest(query="test", max_results=1)
        try:
            if name == "crawl4ai":
                # Probe the reader itself: search() intentionally swallows per-URL
                # failures, which would hide a server that is not running.
                page = retriever.fetch("https://example.com")
                status = f"ok (lecteur de page, {page.metadata['content_chars']} caractères lus)"
            else:
                results = retriever.search(request)
                status = f"ok ({len(results)} résultat(s) sur la sonde)"
            reachable += 1
            results_map[name] = status
        except Exception as exc:  # noqa: BLE001 - the probe reports, it does not raise
            results_map[name] = f"INDISPONIBLE — {type(exc).__name__}: {str(exc)[:160]}"
        out(f"  {name:<10} {results_map[name]}")
    if not retrievers:
        out("  (aucun fournisseur activé)")
    out(f"\n{reachable}/{len(retrievers)} fournisseur(s) ont répondu")
    return (EXIT_OK if reachable else EXIT_NO_PROVIDER), {"providers": results_map}


def _print_report(report, *, out, top: int) -> None:
    out(f"question : {report.question}\n")
    for record in report.rounds:
        out(f"── tour {record.index} — {record.results_new} nouveau(x) / {record.results_returned} reçu(s)"
            f" (corpus {record.corpus_size})")
        for proposal in record.queries:
            out(f"   requête  « {proposal.query} »")
            out(f"            ↳ {proposal.reason}")
        for provider in record.providers:
            marker = "ok " if provider.get("ok") else "KO "
            detail = provider.get("returned", 0)
            if provider.get("error"):
                detail = str(provider["error"])[:120]
            out(f"   {marker}{provider.get('name'):<9} {detail}")
        if record.duplicates_merged:
            out(f"   doublons fusionnés : {record.duplicates_merged}")
        for summary in record.enrichment:
            if summary.get("error"):
                out(f"   enrichissement {summary.get('provider')}: {summary['error']}")
            else:
                out(f"   enrichissement {summary.get('provider')}: "
                    f"{summary.get('matched', summary.get('enriched', 0))} fiche(s) complétée(s)")
        out("")

    metrics = report.metrics
    out(f"arrêt : {report.stop_reason} — {report.stop_detail}")
    out(f"corpus : {metrics.get('corpus_size', 0)} source(s) unique(s), "
        f"{metrics.get('unique_domains', 0)} domaine(s), {metrics.get('duplicates_merged', 0)} doublon(s) fusionné(s)")
    out(f"types  : {json.dumps(metrics.get('sources_by_type', {}), ensure_ascii=False)}")
    out(f"apports : {metrics.get('new_results_per_round')} (nouveaux par tour)")
    hints = report.sufficiency_hints
    out("signaux pour l'arrêt du moteur : "
        f"critical_gaps={hints.get('critical_gaps')} "
        f"unsearched_high_value_categories={hints.get('unsearched_high_value_categories')} "
        f"saturation={hints.get('evidence_saturation')}")

    if report.corpus:
        out(f"\n→ {min(top, len(report.corpus))} source(s) sur {len(report.corpus)} :")
        for result in report.corpus[:top]:
            providers = ",".join((result.metadata or {}).get("providers") or [])
            flags = []
            if (result.metadata or {}).get("full_text"):
                flags.append("texte intégral")
            if (result.metadata or {}).get("enriched_by"):
                flags.append("enrichi")
            if (result.metadata or {}).get("demo_fixture"):
                flags.append("DÉMO")
            out(f"   [{result.source_type}] {result.title}")
            out(f"      {result.url or result.id}  ·  {providers}{'  ·  ' + ', '.join(flags) if flags else ''}")


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    code, _ = run(args)
    return code


if __name__ == "__main__":  # pragma: no cover - module entry point
    sys.exit(main())
