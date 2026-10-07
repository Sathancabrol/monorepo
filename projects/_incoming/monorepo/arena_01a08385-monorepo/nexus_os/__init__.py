"""NEXUS·OS — Agentic Operating System.

Un "OS" pour agents IA : routeur de modèles multi-fournisseurs (façon OmniRoute),
runtime d'agents avec cycle de vie plan → test → implémente → review → vérifie →
mémorise → améliore (façon ECC), framework de compétences SKILL.md (façon
superpowers / openai-skills), créateur d'agents intégré et catalogue d'agents
spécialisés prêts à l'emploi.

Usage rapide::

    from nexus_os.runtime import Runtime
    rt = Runtime()
    for ev in rt.run("Audite la structure du dépôt", agent_id="orchestrator"):
        print(ev)
"""

__version__ = "1.0.0"

__all__ = ["__version__", "Runtime", "Router", "AgentRegistry", "SkillLibrary"]


def __getattr__(name: str):  # lazy exports (évite les imports circulaires)
    if name == "Runtime":
        from nexus_os.runtime import Runtime

        return Runtime
    if name == "Router":
        from nexus_os.providers import Router

        return Router
    if name == "AgentRegistry":
        from nexus_os.agents import AgentRegistry

        return AgentRegistry
    if name == "SkillLibrary":
        from nexus_os.skills import SkillLibrary

        return SkillLibrary
    raise AttributeError(name)
