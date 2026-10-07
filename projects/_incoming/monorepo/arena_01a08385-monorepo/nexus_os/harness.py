"""Portabilité des agents vers les harness existants.

Un agent NEXUS·OS n'a pas à rester dans NEXUS·OS : `export_spec()` le traduit
dans le format natif de chaque harness (fichier de contexte, règle, sous-agent,
compétence). Les formats suivent les conventions publiques observées en 2026 :

=========================  ====================================================
Harness                    Fichier cible
=========================  ====================================================
Claude Code                ``.claude/agents/<id>.md`` (frontmatter YAML)
Codex CLI / OpenCode       ``AGENTS.md`` (section) — OpenCode accepte aussi
                           ``.opencode/agent/<id>.md``
Cline                      ``.clinerules``
Cursor                     ``.cursor/rules/<id>.mdc`` (frontmatter)
Goose                      ``.goosehints``
Gemini CLI                 ``GEMINI.md``
Qwen Code                  ``QWEN.md``
Hermes (Nous Research)     ``~/.hermes/skills/<id>/SKILL.md``
agentskills.io / openai    ``skills/<id>/SKILL.md``
NEXUS·OS                   ``agents/<id>.json``
=========================  ====================================================

L'export est **sans perte pour l'essentiel** : rôle, prompt système, règles,
outils et cycle de vie sont conservés ; ce qu'un harness ne sait pas exprimer
est écrit en commentaire plutôt que supprimé en silence.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from nexus_os.agents import AgentSpec

#: Ordre d'affichage dans l'UI.
TARGETS: tuple[str, ...] = (
    "claude-code", "codex", "opencode", "cline", "cursor", "goose",
    "gemini", "qwen", "hermes", "agentskills", "a2a", "nexus",
)


@dataclass(frozen=True)
class HarnessTarget:
    id: str
    name: str
    filename: str          # chemin relatif produit
    kind: str              # "subagent" | "context" | "rule" | "skill" | "json"
    description: str
    docs: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id, "name": self.name, "filename": self.filename,
            "kind": self.kind, "description": self.description, "docs": self.docs,
        }


TARGET_SPECS: dict[str, HarnessTarget] = {
    "claude-code": HarnessTarget(
        "claude-code", "Claude Code", ".claude/agents/{id}.md", "subagent",
        "Sous-agent déclaratif : frontmatter YAML (name, description, tools, model) + prompt.",
        "docs.anthropic.com/claude-code"),
    "codex": HarnessTarget(
        "codex", "Codex CLI", "AGENTS.md", "context",
        "Fichier de contexte projet, lu automatiquement par Codex CLI.",
        "github.com/openai/codex"),
    "opencode": HarnessTarget(
        "opencode", "OpenCode", ".opencode/agent/{id}.md", "subagent",
        "Agent markdown OpenCode : frontmatter (description, mode, tools) + prompt.",
        "opencode.ai"),
    "cline": HarnessTarget(
        "cline", "Cline", ".clinerules", "rule",
        "Règles de projet injectées dans chaque conversation Cline.",
        "github.com/cline/cline"),
    "cursor": HarnessTarget(
        "cursor", "Cursor", ".cursor/rules/{id}.mdc", "rule",
        "Règle Cursor au format .mdc (description, globs, alwaysApply).",
        "cursor.com/docs"),
    "goose": HarnessTarget(
        "goose", "Goose", ".goosehints", "context",
        "Indices de projet lus par Goose au démarrage d'une session.",
        "block.github.io/goose"),
    "gemini": HarnessTarget(
        "gemini", "Gemini CLI", "GEMINI.md", "context",
        "Fichier de contexte lu par Gemini CLI.", "github.com/google-gemini/gemini-cli"),
    "qwen": HarnessTarget(
        "qwen", "Qwen Code", "QWEN.md", "context",
        "Fichier de contexte lu par Qwen Code.", "github.com/QwenLM/qwen-code"),
    "hermes": HarnessTarget(
        "hermes", "Hermes Agent", "skills/{id}/SKILL.md", "skill",
        "Compétence auto-améliorable au format Hermes / agentskills.io (Nous Research).",
        "hermes-agent.nousresearch.com"),
    "agentskills": HarnessTarget(
        "agentskills", "agentskills.io / openai", "skills/{id}/SKILL.md", "skill",
        "Compétence SKILL.md standard (openai/skills, marketingskills, diagram-design…).",
        "agentskills.io"),
    "a2a": HarnessTarget(
        "a2a", "A2A (Agent2Agent)", ".well-known/agent-card.json", "card",
        "Carte d'agent signable du protocole A2A : un autre agent peut découvrir "
        "celui-ci et lui déléguer du travail.",
        "a2a-protocol.org"),
    "nexus": HarnessTarget(
        "nexus", "NEXUS·OS", "agents/{id}.json", "json",
        "Spec native, réimportable telle quelle.", ""),
}


def list_targets() -> list[dict[str, Any]]:
    return [TARGET_SPECS[t].to_dict() for t in TARGETS]


def filename_for(target: str, spec: AgentSpec) -> str:
    if target not in TARGET_SPECS:
        raise KeyError(f"harness inconnu : {target}")
    return TARGET_SPECS[target].filename.format(id=spec.id)


# --------------------------------------------------------------------------- #
# Blocs réutilisables
# --------------------------------------------------------------------------- #
def _rules_block(spec: AgentSpec) -> str:
    return "\n".join(
        [
            "## Règles de travail",
            f"- Cycle de vie : {' → '.join(spec.lifecycle)}.",
            f"- Autonomie : {spec.autonomy}.",
            "- Commence par la prochaine action concrète, jamais par un préambule.",
            "- Numérote le travail multi-étapes ; termine par une seule prochaine étape.",
            "- 5 éléments maximum par liste ; coupe les tangentes.",
            "- Ne prétends jamais avoir lu, exécuté ou vérifié ce que tu n'as pas fait.",
        ]
    )


def _capabilities(spec: AgentSpec) -> str:
    tools = ", ".join(f"`{t}`" for t in spec.tools) or "aucun"
    skills = ", ".join(spec.skills) or "aucune"
    return f"Outils : {tools}\nCompétences : {skills}"


# --------------------------------------------------------------------------- #
# Exporteurs par harness
# --------------------------------------------------------------------------- #
def _claude_code(spec: AgentSpec) -> str:
    front = "\n".join(
        [
            "---",
            f"name: {spec.id}",
            f'description: "{spec.role}. {spec.description[:140]}"',
            f"tools: {', '.join(spec.tools)}",
            f"model: {spec.model or 'inherit'}",
            "---",
        ]
    )
    return "\n".join(
        [
            front,
            "",
            f"# {spec.emoji} {spec.name} — {spec.role}",
            "",
            spec.description,
            "",
            spec.system_prompt.strip(),
            "",
            _rules_block(spec),
            "",
            f"<!-- {_capabilities(spec)} -->",
            "",
        ]
    )


def _opencode(spec: AgentSpec) -> str:
    mode = {"manuel": "subagent", "assisté": "subagent", "autonome": "primary"}[spec.autonomy]
    front = "\n".join(
        [
            "---",
            f"description: {spec.role} — {spec.description[:120]}",
            f"mode: {mode}",
            f"temperature: {spec.temperature}",
            "---",
        ]
    )
    return "\n".join(
        [front, "", f"# {spec.name}", f"<!-- agent NEXUS·OS `{spec.id}` -->", "",
         spec.system_prompt.strip(), "",
         _rules_block(spec), "", f"<!-- {_capabilities(spec)} -->", ""]
    )


def _cursor(spec: AgentSpec) -> str:
    front = "\n".join(
        [
            "---",
            f"description: {spec.role} — {spec.description[:100]}",
            "globs:",
            "alwaysApply: false",
            "---",
        ]
    )
    return "\n".join(
        [front, "", f"# {spec.name} — {spec.role}", f"// agent NEXUS·OS `{spec.id}`", "",
         spec.system_prompt.strip(), "",
         _rules_block(spec), "", f"// {_capabilities(spec)}", ""]
    )


def _context_file(spec: AgentSpec, harness: str) -> str:
    """AGENTS.md / .clinerules / .goosehints / GEMINI.md / QWEN.md — même idée :
    un bloc de contexte projet que le harness injecte dans chaque session."""
    return "\n".join(
        [
            f"# {spec.name} — {spec.role}",
            f"<!-- agent NEXUS·OS `{spec.id}` exporté pour {harness}. "
            f"Réimportable via `python -m nexus_os create`. -->",
            "",
            spec.description,
            "",
            "## Rôle",
            spec.system_prompt.strip(),
            "",
            _rules_block(spec),
            "",
            "## Capacités",
            _capabilities(spec),
            "",
            "## Déclencheurs",
            ", ".join(spec.triggers) or "—",
            "",
        ]
    )


def _skill_md(spec: AgentSpec, *, hermes: bool) -> str:
    triggers = ", ".join(spec.triggers[:10])
    tags = ", ".join(spec.tags or [spec.id])
    tools = ", ".join(spec.tools)
    head = [
        "---",
        f"name: {spec.id}",
        f"description: {spec.role}. {spec.description[:160]}",
        f"triggers: [{triggers}]",
        f"tags: [{tags}]",
        f"tools: [{tools}]",
        "license: MIT",
    ]
    if hermes:
        head += [
            "# Hermes charge ce fichier à la demande ; SOUL.md et AGENTS.md/HERMES.md",
            "# restent gérés séparément par le harness.",
        ]
    head.append("---")
    return "\n".join(
        [
            "\n".join(head),
            "",
            f"# {spec.name}",
            "",
            spec.system_prompt.strip(),
            "",
            _rules_block(spec),
            "",
            f"<!-- {_capabilities(spec)} -->",
            "",
        ]
    )


def _a2a_card(spec: AgentSpec) -> str:
    """Agent Card A2A : découverte et délégation entre agents hétérogènes."""
    card = {
        "protocolVersion": "1.0",
        "name": spec.name,
        "description": f"{spec.role}. {spec.description}"[:500],
        "version": "1.0.0",
        "url": f"http://localhost:8124/api/a2a/{spec.id}",
        "provider": {"organization": "NEXUS·OS", "url": "http://localhost:8124/os/"},
        "capabilities": {"streaming": True, "pushNotifications": False,
                         "stateTransitionHistory": True},
        "defaultInputModes": ["text/plain"],
        "defaultOutputModes": ["text/plain", "text/markdown"],
        "skills": [{
            "id": spec.id,
            "name": spec.role or spec.name,
            "description": spec.description[:400],
            "tags": list(spec.tags or []) + list(spec.skills),
            "examples": [f"{t.capitalize()}…" for t in spec.triggers[:3]],
        }],
        "securitySchemes": {"bearer": {"type": "http", "scheme": "bearer"}},
        "supportsAuthenticatedExtendedCard": False,
        "x-nexus": {"agent_id": spec.id, "autonomy": spec.autonomy,
                    "tools": list(spec.tools), "lifecycle": list(spec.lifecycle)},
    }
    return json.dumps(card, ensure_ascii=False, indent=2) + "\n"


def _nexus_json(spec: AgentSpec) -> str:
    return json.dumps(spec.to_dict(), ensure_ascii=False, indent=2) + "\n"


_EXPORTERS = {
    "claude-code": _claude_code,
    "opencode": _opencode,
    "cursor": _cursor,
    "hermes": lambda s: _skill_md(s, hermes=True),
    "agentskills": lambda s: _skill_md(s, hermes=False),
    "a2a": _a2a_card,
    "nexus": _nexus_json,
}


def export_spec(spec: AgentSpec, target: str) -> str:
    """Contenu du fichier à poser pour que le harness cible reconnaisse l'agent."""
    if target not in TARGET_SPECS:
        raise KeyError(f"harness inconnu : {target} (disponibles : {', '.join(TARGETS)})")
    if target in _EXPORTERS:
        return _EXPORTERS[target](spec)
    return _context_file(spec, TARGET_SPECS[target].name)


def export_all(spec: AgentSpec) -> dict[str, dict[str, str]]:
    """Tous les formats d'un coup : {target: {filename, content}}."""
    return {
        t: {"filename": filename_for(t, spec), "content": export_spec(spec, t)}
        for t in TARGETS
    }


def summarize(spec: AgentSpec) -> dict[str, Any]:
    """Ce qui est portable et ce qui ne l'est pas, harness par harness."""
    out = []
    for t in TARGETS:
        tgt = TARGET_SPECS[t]
        loses = []
        if tgt.kind in {"context", "rule"}:
            loses.append("outils non déclarés (le harness décide)")
            loses.append("cycle de vie non exécutable (documenté en commentaire)")
        if tgt.kind == "skill":
            loses.append("déclenchement par le harness, pas par routage interne")
        if tgt.kind in {"json", "card"}:
            loses = []
        out.append({
            **tgt.to_dict(),
            "filename": filename_for(t, spec),
            "loses": loses or ["rien — export sans perte"],
        })
    return {"agent_id": spec.id, "targets": out}
