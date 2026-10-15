"""Reference provider adapters and boundaries for v0.1."""

from dataclasses import dataclass
from .retrieval import Retriever, SearchRequest, SearchResult


@dataclass
class RetrievalProvider:
    name: str
    retriever: Retriever

    def search(self, request: SearchRequest) -> list[SearchResult]:
        return self.retriever.search(request)


class ProviderRegistry:
    """Named retrieval backends, interchangeable at run time."""

    def __init__(self):
        self._providers: dict[str, RetrievalProvider] = {}

    def register(self, provider: RetrievalProvider):
        self._providers[provider.name] = provider

    def register_retriever(self, name: str, retriever: Retriever):
        """Convenience wrapper so callers can register a bare retriever."""
        self.register(RetrievalProvider(name=name, retriever=retriever))

    def get(self, name: str) -> RetrievalProvider:
        try:
            return self._providers[name]
        except KeyError as exc:
            raise KeyError(f"Unknown retrieval provider: {name}") from exc

    def names(self) -> list[str]:
        return list(self._providers)

    def as_dict(self) -> dict[str, RetrievalProvider]:
        return dict(self._providers)

    def __contains__(self, name: object) -> bool:
        return name in self._providers

    def __len__(self) -> int:
        return len(self._providers)
