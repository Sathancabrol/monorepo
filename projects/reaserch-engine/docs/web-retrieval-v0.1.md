# Web, scholarly and page-reading retrieval v0.1

The engine core performs no network I/O. This increment adds three adapters
behind the existing `Retriever` protocol, plus the machinery that keeps their
combined output usable: identity-based de-duplication, provenance-preserving
merging, and corpus enrichment.

```text
SearXNG   ── discovery (self-hosted, keyless)     ─┐
OpenAlex  ── scholarly discovery + DOI completion  ├─▶ FederatedRetriever ──▶ corpus
Crossref  ── DOI discovery (already in v0.1)      ─┘        │
Crawl4AI  ── page reader (enricher, not discovery) ─────────┘
```

## Adapters

| Module | Adapter | Role | Network |
|---|---|---|---|
| `engine/web_retrieval.py` | `SearxngRetriever` | Web discovery through a local SearXNG (`format=json` required) | only on `search()` |
| `engine/web_retrieval.py` | `OpenAlexRetriever` | Scholarly discovery **and** `enrich()` from DOIs (abstract, authors, venue, citations, OA link) | only on `search()`/`enrich()` |
| `engine/web_retrieval.py` | `Crawl4AiRetriever` | URL → markdown (`fetch`), snippet → full text (`enrich`) | only on `fetch()` |
| `engine/retrieval.py` | `CrossrefRetriever` | DOI discovery (unchanged from v0.1) | only on `search()` |

Every adapter accepts an injected transport (`http_get` / `http_post`) and builds
real URL parameters, so tests observe the *actual request* without networking.

**Honest states.** Transport problems, non-JSON payloads and a SearXNG instance
without `format=json` raise `RetrievalError`. An empty corpus and a broken
provider are different states, and the engine never confuses them: at
federation level a failure is reported per provider instead of silently
shrinking the corpus.

**Source taxonomy.** Adapters map provider vocabularies onto the engine's own
`SOURCE_TYPES` (OpenAlex `article` → `primary_study`, `review` →
`secondary_source`, `dissertation` → `thesis`, a SearXNG hit → `unverified_web`,
a crawled page → `secondary_source`). `peer_reviewed` is set to `None`, never
inferred from a venue name — the lifecycle forbids that shortcut (Phase 7).

**Traceability.** A crawled page keeps `content_sha256`, `content_chars`,
`fetched_at`, `markdown_variant` and a `truncated` flag, so a later reader knows
exactly which bytes were read.

## Identity, de-duplication, merging

`engine/source_identity.py` defines what "the same source" means:

1. normalized DOI (`10.1000/xyz`, lowercase, prefixes stripped);
2. canonical URL (scheme/host lowercased, tracking parameters removed, query
   sorted, trailing slash and fragment dropped);
3. normalized title (accent- and case-insensitive, refused below 12 characters).

`merge_results()` folds duplicates into the first-seen record while keeping both
identities: `metadata["providers"]`, `metadata["provider_ranks"]`,
`metadata["merged_from"]`. The richer snippet wins (full text beats an abstract
beats a search snippet), missing fields are filled, and the most *specific*
source type is kept — an OpenAlex `primary_study` survives a generic
`academic_record` placeholder. Nothing is silently dropped: `MergeOutcome.groups`
records which ids were folded together.

## Federated retrieval

`engine/federation.py` runs every configured provider for one query and returns
both the corpus and the audit trail:

- **isolation** — one provider failing (or raising) never fails the round; its
  error and diagnostics are reported per provider;
- **determinism** — providers are interleaved round-robin (weighted, then
  alphabetical), so the same corpus yields the same order twice;
- **enrichment** — enrichers run over the merged corpus (OpenAlex fills DOI
  records; Crawl4AI replaces the top web snippets with page text). An enricher
  that explodes is reported, not fatal.

`search_with_report()` returns a `FederatedSearch` (`results`, `corpus_size`,
`duplicates_merged`, `providers[]`, `enrichment[]`); `search()` keeps the plain
protocol signature and stores the same report on `last_report`.

## Configuration

`engine/settings.py` reads the environment once:

| Variable | Default | Effect |
|---|---|---|
| `SEARXNG_BASE_URL` (or `SEARCH_BASE_URL`) | `http://127.0.0.1:8080` | empty ⇒ SearXNG disabled |
| `CRAWL4AI_BASE_URL` | `http://127.0.0.1:11235` | empty ⇒ page reading disabled |
| `SEARXNG_LANGUAGE`, `SEARXNG_CATEGORIES`, `SEARXNG_ENGINES` | `fr`, —, — | SearXNG query shaping |
| `OPENALEX_MAILTO`, `CROSSREF_MAILTO` | — | polite pool only; never required |
| `SEARXNG_DISABLED`, `CRAWL4AI_DISABLED`, `OPENALEX_DISABLED`, `CROSSREF_DISABLED` | unset | turn a provider off |
| `RESEARCH_LANGUAGE` | `fr` | follow-up query language (`fr`/`en`) |
| `RESEARCH_MAX_ROUNDS`, `RESEARCH_RESULTS_PER_QUERY` | `3`, `10` | search budget |
| `RESEARCH_CRAWL4AI_ENRICH_LIMIT` | `3` | pages read per round |

`build_federated()` wires discovery providers and enrichers; the page reader is
deliberately **not** a discovery provider (it cannot answer a query). With every
provider disabled the engine still runs and reports an empty corpus instead of
crashing.

## Boundaries

- Retrieval decides **what is read**, never what is true: every result still goes
  through screening, evidence extraction and claim construction.
- No API key is required anywhere. SearXNG and Crawl4AI run locally (see the
  Watchtower audit stack); OpenAlex and Crossref are public.
- No caching or mirroring of third-party content is introduced here; page text is
  read for one run and stays identifiable by hash.
