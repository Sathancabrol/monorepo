"""Plugins — « everything is a plugin » (DeepSeek Harness, 244 k★).

Un plugin NEXUS·OS est un **dossier de données**, pas du code : il apporte des
compétences (`SKILL.md`) et des agents (JSON), et déclare ce dont il a besoin.
Aucun plugin n'exécute de Python et ne modifie le cœur — c'est la condition pour
qu'un plugin tiers puisse être installé sans audit de code.

Contrat (celui que documente la compétence `plugin-authoring`) :

    mon-plugin/
      plugin.json          ← manifeste
      skills/ma-methode/SKILL.md
      agents/mon-agent.json

    {
      "name": "mon-plugin",
      "version": "0.1.0",
      "description": "Ce que ça apporte, en une ligne",
      "skills": ["skills/ma-methode"],
      "agents": ["agents/mon-agent.json"],
      "requires": ["read_file", "grep"]
    }

Un plugin dont le manifeste est invalide est **signalé, pas chargé** : un plugin
qui échoue en silence est pire qu'un plugin absent. Et le désactiver doit
redonner exactement l'OS d'avant — c'est vérifié par les tests.
"""
from __future__ import annotations

import json
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from nexus_os import config

#: Dossier où vivent les plugins installés dans cet OS.
PLUGINS_DIR = config.NEXUS_HOME / "plugins"
#: Chemins enregistrés hors de ce dossier (développement local).
REGISTRY_FILE = config.NEXUS_HOME / "plugins.json"

MANIFEST_NAME = "plugin.json"
REQUIRED_FIELDS = ("name", "version", "description")


class PluginError(RuntimeError):
    """Manifeste invalide ou plugin introuvable."""


@dataclass
class PluginInfo:
    name: str
    version: str = ""
    description: str = ""
    path: str = ""
    skills: list[str] = field(default_factory=list)
    agents: list[str] = field(default_factory=list)
    requires: list[str] = field(default_factory=list)
    enabled: bool = True
    status: str = "ok"            # ok | erreur | inactif
    problems: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "version": self.version, "description": self.description,
                "path": self.path, "skills": self.skills, "agents": self.agents,
                "requires": self.requires, "enabled": self.enabled,
                "status": self.status, "problems": self.problems}


# -------------------------------------------------------------------------- #
# Registre des chemins
# -------------------------------------------------------------------------- #
def _load_registry() -> dict[str, dict[str, Any]]:
    if not REGISTRY_FILE.exists():
        return {}
    try:
        raw = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
        return raw if isinstance(raw, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _save_registry(data: dict[str, dict[str, Any]]) -> None:
    REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8")


# -------------------------------------------------------------------------- #
# Validation
# -------------------------------------------------------------------------- #
def read_manifest(directory: Path) -> dict[str, Any]:
    manifest = Path(directory) / MANIFEST_NAME
    if not manifest.exists():
        raise PluginError(f"{MANIFEST_NAME} absent dans {directory}")
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise PluginError(f"{MANIFEST_NAME} illisible : {e}") from e
    if not isinstance(data, dict):
        raise PluginError(f"{MANIFEST_NAME} doit contenir un objet JSON")
    return data


def validate(directory: Path) -> tuple[dict[str, Any], list[str]]:
    """Vérifie le manifeste **et** ce qu'il annonce. Retourne (manifeste, problèmes)."""
    problems: list[str] = []
    try:
        data = read_manifest(directory)
    except PluginError as e:
        return {}, [str(e)]

    for f in REQUIRED_FIELDS:
        if not str(data.get(f, "")).strip():
            problems.append(f"champ `{f}` manquant")
    for key in ("skills", "agents", "requires"):
        if key in data and not isinstance(data[key], list):
            problems.append(f"`{key}` doit être une liste")

    base = Path(directory)
    for rel in data.get("skills", []) if isinstance(data.get("skills"), list) else []:
        skill_md = base / rel / "SKILL.md"
        if not skill_md.exists():
            problems.append(f"compétence annoncée introuvable : {rel}/SKILL.md")
    for rel in data.get("agents", []) if isinstance(data.get("agents"), list) else []:
        target = base / rel
        if not target.exists():
            problems.append(f"agent annoncé introuvable : {rel}")
            continue
        try:
            json.loads(target.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            problems.append(f"agent illisible : {rel} ({e})")

    if isinstance(data.get("requires"), list) and data["requires"]:
        from nexus_os.tools import TOOL_BY_NAME

        unknown = [t for t in data["requires"] if t not in TOOL_BY_NAME]
        if unknown:
            problems.append(f"outils requis inexistants : {', '.join(unknown)}")
    return data, problems


# -------------------------------------------------------------------------- #
# Installation
# -------------------------------------------------------------------------- #
def register(source: str, *, copy: bool = True) -> PluginInfo:
    """Installe un plugin : copié dans `.nexus/plugins/`, ou référencé sur place."""
    src = Path(source).expanduser().resolve()
    if not src.is_dir():
        raise PluginError(f"dossier introuvable : {source}")
    data, problems = validate(src)
    if problems:
        raise PluginError(" ; ".join(problems))

    name = str(data["name"]).strip()
    if copy:
        PLUGINS_DIR.mkdir(parents=True, exist_ok=True)
        target = PLUGINS_DIR / name
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(src, target)
    else:
        target = src

    reg = _load_registry()
    reg[name] = {"path": str(target), "enabled": True}
    _save_registry(reg)
    return describe(name)


def unregister(name: str, *, delete_files: bool = False) -> bool:
    reg = _load_registry()
    entry = reg.pop(name, None)
    if entry is None:
        # Peut exister seulement comme dossier installé.
        folder = PLUGINS_DIR / name
        if not folder.exists():
            return False
        entry = {"path": str(folder), "enabled": True}
    _save_registry(reg)
    if delete_files:
        path = Path(entry["path"])
        if path.exists() and PLUGINS_DIR in path.parents:
            shutil.rmtree(path, ignore_errors=True)
    return True


def set_enabled(name: str, enabled: bool) -> bool:
    reg = _load_registry()
    if name not in reg:
        return False
    reg[name]["enabled"] = bool(enabled)
    _save_registry(reg)
    return True


def _installed() -> dict[str, dict[str, Any]]:
    """Registre + dossiers présents dans `.nexus/plugins/` non référencés."""
    reg = dict(_load_registry())
    if PLUGINS_DIR.exists():
        for child in sorted(PLUGINS_DIR.iterdir()):
            if child.is_dir() and (child / MANIFEST_NAME).exists():
                reg.setdefault(child.name, {"path": str(child), "enabled": True})
    return reg


def describe(name: str) -> PluginInfo:
    entry = _installed().get(name)
    if not entry:
        raise PluginError(f"plugin inconnu : {name}")
    data, problems = validate(Path(entry["path"]))
    enabled = bool(entry.get("enabled", True))
    return PluginInfo(
        name=str(data.get("name", name)),
        version=str(data.get("version", "")),
        description=str(data.get("description", "")),
        path=entry["path"],
        skills=list(data.get("skills", []) or []),
        agents=list(data.get("agents", []) or []),
        requires=list(data.get("requires", []) or []),
        enabled=enabled,
        status="erreur" if problems else ("ok" if enabled else "inactif"),
        problems=problems,
    )


def discover() -> list[PluginInfo]:
    """Tous les plugins connus, avec leur état réel."""
    out: list[PluginInfo] = []
    for name in sorted(_installed()):
        try:
            out.append(describe(name))
        except PluginError as e:
            out.append(PluginInfo(name=name, status="erreur", problems=[str(e)]))
    return out


def active() -> list[PluginInfo]:
    return [p for p in discover() if p.status == "ok"]


# -------------------------------------------------------------------------- #
# Ce que les plugins actifs apportent à l'OS
# -------------------------------------------------------------------------- #
def skill_dirs() -> list[Path]:
    """Dossiers de compétences à ajouter à la bibliothèque."""
    dirs: list[Path] = []
    for p in active():
        base = Path(p.path)
        for rel in p.skills:
            d = base / rel
            if (d / "SKILL.md").exists():
                dirs.append(d)
    return dirs


def agent_files() -> list[Path]:
    """Fichiers d'agents à ajouter au registre."""
    files: list[Path] = []
    for p in active():
        base = Path(p.path)
        for rel in p.agents:
            f = base / rel
            if f.exists():
                files.append(f)
    return files


def summarize() -> dict[str, Any]:
    plugins = discover()
    return {
        "plugins_dir": str(PLUGINS_DIR),
        "count": len(plugins),
        "active": sum(1 for p in plugins if p.status == "ok"),
        "broken": sum(1 for p in plugins if p.status == "erreur"),
        "skills": len(skill_dirs()),
        "agents": len(agent_files()),
        "items": [p.to_dict() for p in plugins],
    }


def make_sample(target: Path | str) -> Path:
    """Génère un plugin d'exemple valide — sert de gabarit et de fixture de test."""
    root = Path(target) / "exemple"
    (root / "skills" / "methode-exemple").mkdir(parents=True, exist_ok=True)
    (root / "agents").mkdir(parents=True, exist_ok=True)
    (root / MANIFEST_NAME).write_text(json.dumps({
        "name": "exemple",
        "version": "0.1.0",
        "description": "Plugin d'exemple : une méthode et un agent.",
        "skills": ["skills/methode-exemple"],
        "agents": ["agents/lecteur.json"],
        "requires": ["read_file", "grep"],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (root / "skills" / "methode-exemple" / "SKILL.md").write_text("""---
name: methode-exemple
description: Méthode apportée par le plugin d'exemple.
triggers: [exemple, plugin, démonstration]
tags: [plugin]
tools: [read_file]
license: MIT
---
# Méthode d'exemple

1. Lire avant d'écrire.
2. Citer le chemin exact.
3. Terminer par une seule prochaine étape.
""", encoding="utf-8")
    (root / "agents" / "lecteur.json").write_text(json.dumps({
        "id": "lecteur",
        "name": "Lecteur",
        "emoji": "📖",
        "role": "Lecture à haute voix du dépôt",
        "description": "Lit un fichier et le résume en trois lignes, sans inventer.",
        "skills": ["methode-exemple"],
        "tools": ["read_file", "grep", "list_dir"],
        "triggers": ["lis", "résume", "lecteur", "exemple"],
        "tags": ["plugin", "lecture"],
        "lifecycle": ["plan", "research", "review"],
        "system_prompt": ("Tu lis le fichier demandé et tu le résumes en trois lignes. "
                          "Tu cites le chemin et les lignes. Tu n'inventes rien : si le "
                          "fichier est introuvable, tu le dis."),
        "autonomy": "assisté",
        "temperature": 0.2,
        "max_steps": 4,
        "model": "",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return root
