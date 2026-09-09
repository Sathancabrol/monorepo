"""Créateur d'agents intégré.

Une description en langage naturel → une spec d'agent complète (prompt système,
compétences, outils, cycle de vie, triggers). Deux moteurs :

* **live** : le modèle écrit le prompt système et renvoie du JSON ;
* **offline** : analyse lexicale + composition par gabarits — fonctionne sans
  clé API et reste déterministe.
"""
from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field
from typing import Any

from nexus_os.agents import LIFECYCLE, AgentSpec, registry
from nexus_os.llm import complete
from nexus_os.providers import ModelRequest
from nexus_os.skills import library

#: Compétences indexées par mots-clés (moteur hors-ligne).
SKILL_HINTS: dict[str, tuple[str, ...]] = {
    "research-first": ("cherche", "recherche", "source", "veille", "état de l'art", "enquête",
                       "documente", "compare", "benchmark"),
    "code-implementation": ("code", "développ", "implémente", "script", "api", "fonction", "bug",
                            "python", "javascript", "refactor"),
    "test-and-verify": ("test", "vérif", "qualité", "non régression", "pytest", "validation"),
    "code-review": ("revue", "review", "relis", "audit", "dette"),
    "security-review": ("sécurité", "vulnérab", "injection", "secret", "conformité", "rgpd"),
    "marketing-copy": ("marketing", "vente", "landing", "copywriting", "accroche", "conversion",
                       "email", "slogan", "pitch", "commercial"),
    "seo-content": ("seo", "référencement", "mot-clé", "blog", "article", "trafic organique"),
    "diagram-design": ("diagramme", "schéma", "architecture", "flux", "modélis", "mermaid"),
    "data-analysis": ("donnée", "data", "csv", "métrique", "statistique", "kpi", "dashboard",
                      "analyse chiffrée", "sql"),
    "browser-automation": ("navigateur", "browser", "scrape", "site", "formulaire", "clic",
                           "page web", "e2e"),
    "html-composition": ("html", "page", "rapport visuel", "rendu", "présentation", "slide"),
    "adhd-output": ("clair", "concis", "focus", "priorit", "résume", "lisible", "simple"),
    "memory-and-improve": ("mémor", "retiens", "historique", "apprend", "améliore", "contexte"),
    "agent-design": ("agent", "assistant", "bot", "automatis"),
}

#: Outils indexés par mots-clés.
TOOL_HINTS: dict[str, tuple[str, ...]] = {
    "list_dir": ("dossier", "structure", "arborescence", "dépôt", "projet", "fichiers"),
    "read_file": ("lis", "lit", "fichier", "code", "document", "rapport", "contrat"),
    "grep": ("cherche dans", "trouve où", "occurrence", "motif", "référence"),
    "write_file": ("écris", "produis", "génère", "rédige", "livre", "sauvegarde", "exporte"),
    "web_search": ("web", "internet", "en ligne", "actualité", "concurrent", "marché"),
    "http_get": ("url", "api", "endpoint", "page web", "flux", "webhook"),
    "python_exec": ("calcule", "traite", "csv", "json", "statistique", "script", "exécute"),
    "shell": ("commande", "shell", "build", "déploie", "docker", "npm", "pip"),
    "diagram": ("diagramme", "schéma", "architecture", "flux", "mermaid"),
    "compose_html": ("html", "page", "rapport visuel", "landing", "présentation"),
    "memory_remember": ("mémor", "retiens", "historique", "apprend"),
    "memory_recall": ("contexte", "déjà vu", "historique", "réutilise"),
    "handoff": ("délègue", "équipe", "orchestr", "autre agent", "transmet"),
    "create_agent": ("crée un agent", "nouvel agent", "fabrique un agent"),
}

#: Phases du cycle de vie déduites du vocabulaire.
PHASE_HINTS: dict[str, tuple[str, ...]] = {
    "plan": ("plan", "stratégie", "roadmap", "étape", "découp", "organise"),
    "research": ("cherche", "source", "analyse", "enquête", "veille", "explore"),
    "implement": ("produis", "produit", "produire", "écris", "écrit", "génère", "générer",
                  "implémente", "crée", "fabrique", "construis", "livre", "compose", "rédige"),
    "review": ("revue", "relis", "audit", "contrôle", "vérifie la qualité"),
    "verify": ("test", "vérif", "valide", "preuve", "mesure"),
    "remember": ("mémor", "retiens", "historique", "apprend"),
    "improve": ("améliore", "optimis", "itère", "rétro"),
}

DEFAULT_TOOLS = ("read_file", "write_file", "memory_recall", "memory_remember")


@dataclass
class CreationResult:
    spec: AgentSpec
    rationale: list[str] = field(default_factory=list)
    engine: str = "offline"  # "live" | "offline"
    test_recipe: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "spec": self.spec.to_dict(),
            "rationale": self.rationale,
            "engine": self.engine,
            "test_recipe": self.test_recipe,
        }


def slugify(text: str, fallback: str = "agent") -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return s[:32] or fallback


def _pick(hints: dict[str, tuple[str, ...]], text: str, *, minimum: int = 2,
          maximum: int = 4, defaults: tuple[str, ...] = ()) -> list[str]:
    low = text.lower()
    scored: list[tuple[int, str]] = []
    for key, kws in hints.items():
        n = sum(1 for k in kws if k in low)
        if n:
            scored.append((n, key))
    scored.sort(key=lambda x: (-x[0], x[1]))
    out = [k for _, k in scored[:maximum]]
    if len(out) < minimum:
        for d in defaults:
            if d not in out:
                out.append(d)
            if len(out) >= minimum:
                break
    return out


def _phases(text: str) -> list[str]:
    """Déduit le cycle de vie du vocabulaire, puis le normalise.

    Normalisation : un agent planifie toujours ; s'il ne fait ni production ni
    revue, il produit ; toute production se vérifie.
    """
    low = text.lower()
    hits = {p for p in LIFECYCLE if any(k in low for k in PHASE_HINTS.get(p, ()))}
    hits.add("plan")
    if not ({"implement", "review"} & hits):
        hits.add("implement")
    if "implement" in hits:
        hits.add("verify")
    return [p for p in LIFECYCLE if p in hits]


def _triggers(description: str, name: str) -> list[str]:
    """Mots déclencheurs pour le routage : verbes + noms du domaine."""
    words = [w for w in re.findall(r"[a-zà-ÿ][a-zà-ÿ0-9-]{3,}", (description + " " + name).lower())
             if w not in {"avec", "pour", "dans", "dont", "plus", "sans", "sous", "être", "agent",
                          "nexus", "vous", "votre", "notre", "faire", "tout", "tous", "toute"}]
    seen: list[str] = []
    for w in words:
        if w not in seen:
            seen.append(w)
    return seen[:8]


_OFFLINE_PROMPT = """Tu es l'agent {name} de NEXUS·OS.

## Mission
{mission}

## Méthode
1. Commence par comprendre la demande réelle : quel résultat, pour qui, sous quelle contrainte.
2. Consulte ce qui existe déjà (fichiers, mémoire) avant de produire quoi que ce soit.
3. Produis le livrable dans le format attendu, sans remplissage.
4. Vérifie le livrable contre la demande initiale, point par point.
5. Termine par : ce qui est livré, ce qui reste ouvert, la prochaine action.

## Interdit
- Prétendre avoir lu, exécuté ou vérifié ce que tu n'as pas fait.
- Ajouter une étape, un outil ou un livrable non demandé.
- Les préambules, les récapitulatifs et les formules de politesse creuses.

## Format de sortie
- Ligne 1 : la prochaine action.
- Corps : le livrable, structuré, 5 items maximum par liste.
- Dernière ligne : une seule prochaine étape.
"""


def draft(description: str, *, name: str = "", emoji: str = "", model: str = "",
          autonomy: str = "assisté", use_llm: bool = True) -> CreationResult:
    """Construit une spec d'agent à partir d'une description libre."""
    description = (description or "").strip()
    if not description:
        raise ValueError("description requise")

    available_skills = {s.name for s in library().all()}
    rationale: list[str] = []

    skills = [s for s in _pick(SKILL_HINTS, description, minimum=2, maximum=4,
                               defaults=("adhd-output", "memory-and-improve"))
              if s in available_skills]
    tools = _pick(TOOL_HINTS, description, minimum=3, maximum=6, defaults=DEFAULT_TOOLS)
    phases = _phases(description)
    name = (name or "").strip() or _title_from(description)
    agent_id = slugify(name)
    triggers = _triggers(description, name)

    mission = description.rstrip(". ") + "."
    prompt = _OFFLINE_PROMPT.format(name=name, mission=mission)
    engine = "offline"

    rationale.append(f"compétences retenues : {', '.join(skills) or 'aucune'} (mots-clés de la demande)")
    rationale.append(f"outils minimaux : {', '.join(tools)}")
    rationale.append(f"cycle de vie : {' → '.join(phases)}")

    if use_llm:
        live = _llm_draft(name=name, mission=mission, skills=skills, tools=tools,
                          model=model)
        if live:
            prompt = live.get("system_prompt") or prompt
            if live.get("role"):
                rationale.append(f"rôle reformulé par le modèle : {live['role']}")
            engine = "live"
            if live.get("test_recipe"):
                rationale.append(f"recette de test proposée par le modèle : {live['test_recipe']}")
            description_out = live.get("description") or mission
            spec = _spec(agent_id, name, emoji, live.get("role") or _role_from(description),
                         description_out, prompt, skills, tools, triggers, model, autonomy, phases)
            return CreationResult(spec, rationale, engine,
                                  live.get("test_recipe") or _recipe(name, description))

    spec = _spec(agent_id, name, emoji, _role_from(description), mission, prompt, skills, tools,
                 triggers, model, autonomy, phases)
    return CreationResult(spec, rationale, engine, _recipe(name, description))


def _spec(agent_id: str, name: str, emoji: str, role: str, description: str, prompt: str,
          skills: list[str], tools: list[str], triggers: list[str], model: str, autonomy: str,
          phases: list[str]) -> AgentSpec:
    return AgentSpec(
        id=agent_id,
        name=name,
        role=role,
        description=description,
        emoji=emoji or "🧩",
        system_prompt=prompt,
        skills=skills,
        tools=tools,
        triggers=triggers,
        model=model,
        temperature=0.4,
        max_steps=6,
        autonomy=autonomy if autonomy in ("manuel", "assisté", "autonome") else "assisté",
        lifecycle=phases,
        builtin=False,
        source="user",
        created_at=time.time(),
        tags=["créé"],
    )


def _title_from(description: str) -> str:
    words = re.findall(r"[A-Za-zÀ-ÿ0-9][A-Za-zÀ-ÿ0-9'-]*", description)[:5]
    return " ".join(words).strip().title() or "Nouvel agent"


def _role_from(description: str) -> str:
    m = re.search(r"(?:qui|pour)\s+([a-zà-ÿ0-9 ,\-]{4,60})", description.lower())
    return (m.group(1).strip().rstrip(".") if m else description[:70]).capitalize()


def _recipe(name: str, description: str) -> str:
    return (f"Tâche de recette : demande à « {name} » de produire un livrable sur "
            f"« {description[:60].strip()} » et vérifie que les 5 règles de sortie sont respectées.")


def _llm_draft(*, name: str, mission: str, skills: list[str], tools: list[str],
               model: str) -> dict[str, Any] | None:
    """Demande au modèle un prompt système + rôle + recette, en JSON strict."""
    payload = {
        "role": "system",
        "content": (
            "Tu conçois des agents IA. Réponds UNIQUEMENT avec un objet JSON valide, sans "
            "markdown, avec les clés : role (<= 60 caractères), description (<= 160 caractères), "
            "system_prompt (règles numérotées et vérifiables, en français, 15 à 30 lignes), "
            "test_recipe (une tâche qui prouve que l'agent fonctionne)."
        ),
    }
    user = {
        "role": "user",
        "content": (
            f"Agent à concevoir : {name}\nMission : {mission}\n"
            f"Compétences disponibles pour cet agent : {', '.join(skills) or 'aucune'}\n"
            f"Outils disponibles pour cet agent : {', '.join(tools)}"
        ),
    }
    comp = complete(
        [payload, user],
        request=ModelRequest(preferred=model or None, need_tools=False, min_context=8000),
        temperature=0.5,
        max_tokens=900,
    )
    if comp.mode != "live":
        return None
    raw = comp.text.strip()
    raw = re.sub(r"^```(?:json)?|```$", "", raw, flags=re.M).strip()
    try:
        start, end = raw.index("{"), raw.rindex("}") + 1
        data = json.loads(raw[start:end])
    except (ValueError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict) or not str(data.get("system_prompt", "")).strip():
        return None
    return data


def create_and_save(description: str, **kwargs: Any) -> CreationResult:
    """Crée puis enregistre l'agent dans le registre utilisateur."""
    result = draft(description, **kwargs)
    existing = registry().get(result.spec.id)
    if existing and not existing.builtin:
        result.spec.id = f"{result.spec.id}-{int(time.time()) % 10000}"
    registry().save(result.spec)
    result.rationale.append(f"agent enregistré : .nexus/agents/{result.spec.id}.json")
    return result
