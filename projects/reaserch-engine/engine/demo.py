"""Offline demonstration corpus.

The demo exists to exercise the *machinery* — federation, de-duplication,
enrichment, gap-driven re-querying, stopping — without a network and without a
model. **Every record below is fictional**, tagged ``demo_fixture``, and must
never be presented as evidence about the real world. For real runs, use
``engine.settings.build_federated`` (SearXNG / OpenAlex / Crossref / Crawl4AI).
"""

from __future__ import annotations

from .federation import FederatedRetriever
from .iteration import IterativeSearch
from .query_strategy import QueryStrategist, normalize_query
from .retrieval import SearchResult

DEMO_QUESTION = "Quel est l'effet du trafic maritime sur la qualité de l'air à Sète ?"


def _doc(identifier: str, title: str, url: str | None, snippet: str, *,
         keywords: tuple[str, ...], source_type: str = "unverified_web",
         provider: str = "demo-index", metadata: dict | None = None) -> SearchResult:
    data = {"provider": provider, "demo_fixture": True,
            "keywords": list(keywords), **(metadata or {})}
    return SearchResult(id=identifier, title=title, url=url, snippet=snippet,
                        source_type=source_type, metadata=data)


def demo_corpus() -> list[SearchResult]:
    """Fictional discovery hits, tagged by the query family that finds them."""
    return [
        _doc("web:demo/rapport-thau-2024",
             "[DÉMO] Rapport annuel de surveillance de l'air — bassin de Thau (factice)",
             "https://example.org/demo/rapport-thau-2024",
             "Synthèse factice : concentrations mesurées à proximité du port, sans conclusion causale.",
             keywords=("trafic", "maritime", "qualite", "air", "sete", "port", "mesures")),
        _doc("doi:10.0000/demo.2023.001",
             "[DÉMO] Shipping emissions and urban air quality in Mediterranean ports",
             "https://doi.org/10.0000/demo.2023.001",
             "",
             keywords=("trafic", "maritime", "qualite", "air", "port", "emissions"),
             source_type="primary_study",
             metadata={"doi": "10.0000/demo.2023.001", "year": 2023}),
        _doc("doi:10.0000/demo.2021.014",
             "[DÉMO] Systematic review of port emission inventories",
             "https://doi.org/10.0000/demo.2021.014",
             "Revue systématique factice sur les inventaires d'émissions portuaires.",
             keywords=("revue", "litterature", "emissions", "port", "inventaire", "etat"),
             source_type="secondary_source",
             metadata={"doi": "10.0000/demo.2021.014", "year": 2021, "authors": ["A. Demo"]}),
        _doc("web:demo/contre-analyse-2025",
             "[DÉMO] Contre-analyse : les limites des mesures côtières (factice)",
             "https://example.org/demo/contre-analyse-2025",
             "Cette page fictive contredit la lecture dominante : biais de capteurs, vents dominants.",
             keywords=("limites", "critiques", "contre", "biais", "capteurs", "incertitudes")),
        _doc("web:demo/donnees-officielles-air",
             "[DÉMO] Données officielles régionales — inventaire des émissions (factice)",
             "https://example.org/demo/donnees-officielles-air",
             "Jeu de données institutionnel fictif, séries annuelles par secteur.",
             keywords=("donnees", "officielles", "institutionnel", "inventaire", "secteur", "series"),
             source_type="institutional_report"),
        _doc("web:demo/jeu-de-donnees-ais",
             "[DÉMO] Jeu de données AIS agrégé (factice)",
             "https://example.org/demo/jeu-de-donnees-ais",
             "Extraction fictive de positions AIS agrégées par heure pour le démonstrateur.",
             keywords=("jeu", "donnees", "dataset", "ais", "positions", "heure")),
        _doc("web:demo/retour-terrain-littoral",
             "[DÉMO] Retour de terrain : riverains du littoral (factice)",
             "https://example.org/demo/retour-terrain-littoral",
             "Témoignages fictifs situés, utiles pour la phase de qualification des observations.",
             keywords=("terrain", "retour", "riverains", "observation", "situe")),
        # Same document as the first hit, published elsewhere: the federation must
        # merge it instead of showing the analyst two records.
        _doc("web:demo/rapport-thau-2024-mirror",
             "[DÉMO] Rapport annuel de surveillance de l'air — bassin de Thau (factice)",
             "https://example.net/demo/rapport-thau-2024?utm_source=newsletter",
             "Miroir factice du rapport annuel, contenu identique.",
             keywords=("trafic", "maritime", "qualite", "air", "sete", "mesures"),
             provider="demo-mirror"),
    ]


class ScriptedRetriever:
    """Keyword-matched retriever over the demo corpus (deterministic)."""

    def __init__(self, name: str, documents: list[SearchResult], *, limit: int = 6):
        self.name = name
        self.documents = documents
        self.limit = limit
        self.last_diagnostics: dict = {}

    def search(self, request) -> list[SearchResult]:
        terms = {term for term in normalize_query(request.query).split() if len(term) > 2}
        scored = []
        for document in self.documents:
            keywords = set(document.metadata.get("keywords") or ())
            score = len(terms & keywords)
            if score:
                scored.append((score, document))
        scored.sort(key=lambda pair: (-pair[0], pair[1].id))
        results = []
        for rank, (_, document) in enumerate(scored[:min(self.limit, request.max_results)], start=1):
            clone = SearchResult(id=document.id, title=document.title, url=document.url,
                                 snippet=document.snippet, source_type=document.source_type,
                                 metadata={**document.metadata, "provider": self.name, "rank": rank})
            results.append(clone)
        self.last_diagnostics = {"provider": self.name, "returned": len(results),
                                 "query": request.query}
        return results

    def diagnostics(self) -> dict:
        return dict(self.last_diagnostics)


class DemoAbstractEnricher:
    """Stands in for OpenAlex DOI completion (no network, no invented facts)."""

    name = "openalex"

    def __init__(self):
        self.last_enrichment: dict = {}

    def enrich(self, results):
        enriched, matched = [], 0
        for result in results:
            metadata = dict(result.metadata or {})
            doi = metadata.get("doi") or (result.id[4:] if result.id.startswith("doi:") else None)
            if doi and not (result.snippet or "").strip():
                metadata["doi"] = doi
                metadata["authors"] = ["A. Demo", "B. Factice"]
                metadata["venue"] = "[DÉMO] Journal of Fictional Port Studies"
                metadata["cited_by_count"] = 7
                metadata["enriched_by"] = ["openalex"]
                metadata["abstract_source"] = "provider_text"
                result.snippet = ("Résumé factice reconstruit depuis un index inversé : "
                                  "émissions portuaires et qualité de l'air urbaine.")
                result.metadata = metadata
                matched += 1
            enriched.append(result)
        self.last_enrichment = {"provider": self.name, "candidates": matched, "matched": matched,
                                "batches": 1 if matched else 0}
        return enriched


class DemoPageReader:
    """Stands in for Crawl4AI: turns the first web hits into 'full text'."""

    name = "crawl4ai"

    def __init__(self, *, limit: int = 2):
        self.limit = limit
        self.last_enrichment: dict = {}

    def enrich(self, results):
        enriched, count = [], 0
        for result in results:
            metadata = dict(result.metadata or {})
            if count < self.limit and result.source_type == "unverified_web" and not metadata.get("full_text"):
                metadata["full_text"] = True
                metadata["enriched_by"] = sorted(set(list(metadata.get("enriched_by") or []) + [self.name]))
                metadata["providers"] = sorted(set(list(metadata.get("providers") or []) + [self.name]))
                metadata["content_sha256"] = "demo" + str(abs(hash(result.id)) % 10**10)
                metadata["content_chars"] = len(result.snippet) + 420
                result.snippet = (result.snippet + "\n\n# Section extraite (démo)\n"
                                  "Corps de page factice remplaçant le résumé de moteur de recherche.")
                result.metadata = metadata
                count += 1
            enriched.append(result)
        self.last_enrichment = {"provider": self.name, "candidates": count, "enriched": count, "errors": []}
        return enriched


def build_demo_federated(*, weights: dict[str, float] | None = None,
                         page_limit: int = 2) -> FederatedRetriever:
    documents = demo_corpus()
    index = ScriptedRetriever("demo-index", [doc for doc in documents if doc.metadata["provider"] == "demo-index"])
    mirror = ScriptedRetriever("demo-mirror", [doc for doc in documents if doc.metadata["provider"] == "demo-mirror"])
    return FederatedRetriever(
        {"demo-index": index, "demo-mirror": mirror},
        weights=weights,
        enrichers=[DemoAbstractEnricher(), DemoPageReader(limit=page_limit)],
    )


def build_demo_iteration(*, max_rounds: int = 3, results_per_query: int = 6,
                         language: str = "fr", **kwargs) -> IterativeSearch:
    strategist = QueryStrategist(language=language) if language != "fr" else None
    return IterativeSearch(build_demo_federated(), strategist=strategist,
                           max_rounds=max_rounds, results_per_query=results_per_query, **kwargs)


DEMO_SUBQUESTIONS = [
    {"id": "sq1", "text": "Que mesurent les réseaux de surveillance autour du port de Sète ?",
     "source_types": ["institutional_report", "primary_study"]},
    {"id": "sq2", "text": "Quelles preuves relient les émissions des navires aux concentrations observées ?",
     "source_types": ["primary_study", "systematic_review"]},
    {"id": "sq3", "text": "Quelles limites méthodologiques affaiblissent ces preuves ?",
     "source_types": ["secondary_source"]},
]
