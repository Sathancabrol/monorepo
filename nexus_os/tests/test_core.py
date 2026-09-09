"""Tests NEXUS·OS — exécutent le vrai code (routeur, skills, créateur, runtime, API)."""
from __future__ import annotations

import json

import pytest

from nexus_os.agents import AgentSpec, registry
from nexus_os.creator import draft
from nexus_os.providers import MODEL_INDEX, ModelRequest, Router
from nexus_os.skills import SkillLibrary, parse_frontmatter
from nexus_os.tools import ToolContext, ToolError, ToolRegistry


# -------------------------------------------------------------------------- #
# Routeur
# -------------------------------------------------------------------------- #
def test_catalogue_complet_et_indexé():
    r = Router()
    cat = r.catalog()
    assert len(cat) == len(MODEL_INDEX) >= 20
    assert {c["provider"] for c in cat} >= {"anthropic", "openai", "google", "openrouter", "local"}
    # chaque entrée expose ce dont l'UI a besoin
    for c in cat:
        assert set(c) >= {"id", "provider", "ready", "has_key", "free", "context", "style"}


def test_sans_cle_le_routeur_replie_sur_le_moteur_local():
    r = Router()
    if r.is_live():
        pytest.skip("une clé API est présente dans l'environnement")
    chosen = r.route(ModelRequest())
    assert chosen.provider.id == "local"
    assert chosen.model.id == "nexus-local"
    assert "repli" in chosen.reason


def test_chaine_de_secours_termine_toujours_par_le_local():
    chain = Router().chain_for(ModelRequest())
    assert chain[-1].provider.id == "local"
    assert len(chain) >= 1
    # sans fournisseur configuré, la chaîne se réduit au repli local
    if not Router().is_live():
        assert len(chain) == 1


def test_modele_explicite_prime_sur_le_tri_economique():
    r = Router()
    if not r.is_live():
        pytest.skip("aucune clé API : rien à router en live")
    chosen = r.route(ModelRequest(preferred="gpt-5.2"))
    assert chosen.model.id == "gpt-5.2"


def test_contraintes_capacites_filtrent_le_catalogue():
    r = Router()
    chain = r.chain_for(ModelRequest(need_vision=True, min_context=200_000))
    for routed in chain[:-1]:
        assert routed.model.vision and routed.model.context >= 200_000


def test_cooldown_ecarte_un_modele_en_erreur(monkeypatch):
    r = Router()
    r.mark_failure("nexus-local")
    assert r.cooling_down("nexus-local")
    r.mark_success("nexus-local")
    assert not r.cooling_down("nexus-local")


# -------------------------------------------------------------------------- #
# Compétences
# -------------------------------------------------------------------------- #
def test_frontmatter_parse():
    meta, body = parse_frontmatter(
        "---\nname: x\ndescription: d\ntriggers: [a, b]\ntools: [read_file]\n---\n# Corps\n"
    )
    assert meta["name"] == "x" and meta["triggers"] == ["a", "b"]
    assert meta["tools"] == ["read_file"]
    assert body.startswith("# Corps")


def test_14_competences_integrees_decouvertes():
    lib = SkillLibrary()
    names = {s.name for s in lib.all()}
    assert len(names) == 14
    assert {"research-first", "diagram-design", "marketing-copy", "adhd-output",
            "agent-design"} <= names
    for s in lib.all():
        assert s.body, f"compétence vide : {s.name}"
        assert s.description, f"pas de description : {s.name}"


def test_routage_de_competence_par_triggers():
    lib = SkillLibrary()
    got = {s.name for s in lib.match("fais-moi un diagramme d'architecture en mermaid")}
    assert "diagram-design" in got
    got2 = {s.name for s in lib.match("écris une landing page qui convertit")}
    assert "marketing-copy" in got2


# -------------------------------------------------------------------------- #
# Outils (sandbox)
# -------------------------------------------------------------------------- #
def test_ecriture_hors_sandbox_refusee():
    reg = ToolRegistry()
    with pytest.raises(ToolError):
        reg.execute("write_file", {"path": "../../evil.txt", "content": "x"}, ToolContext())
    with pytest.raises(ToolError):
        reg.execute("write_file", {"path": "/tmp/evil.txt", "content": "x"}, ToolContext())


def test_lecture_de_secret_bloquee():
    reg = ToolRegistry()
    with pytest.raises(ToolError):
        reg.execute("read_file", {"path": ".env"}, ToolContext())
    with pytest.raises(ToolError):
        reg.execute("read_file", {"path": ".nexus/secrets.env"}, ToolContext())


def test_ecriture_puis_relecture_dans_la_sandbox(tmp_path, monkeypatch):
    from nexus_os import config

    monkeypatch.setattr(config, "WORKSPACE_DIR", tmp_path)
    reg = ToolRegistry()
    out = reg.execute("write_file", {"path": "notes/a.md", "content": "# ok"}, ToolContext())
    assert "notes/a.md" in out
    assert (tmp_path / "notes" / "a.md").read_text() == "# ok"


def test_shell_desactive_par_defaut():
    reg = ToolRegistry()
    with pytest.raises(ToolError, match="NEXUS_ALLOW_SHELL"):
        reg.execute("shell", {"command": "echo hi"}, ToolContext())


def test_diagram_produit_mermaid_et_html(tmp_path, monkeypatch):
    from nexus_os import config

    monkeypatch.setattr(config, "WORKSPACE_DIR", tmp_path)
    reg = ToolRegistry()
    out = reg.execute("diagram", {"title": "Test Flux", "nodes": "A, B", "edges": "A-->B"},
                      ToolContext())
    assert "test-flux.mmd" in out
    mmd = (tmp_path / "diagrams" / "test-flux.mmd").read_text()
    assert "A --> B" in mmd
    html = (tmp_path / "diagrams" / "test-flux.html").read_text()
    assert "mermaid" in html


# -------------------------------------------------------------------------- #
# Agents
# -------------------------------------------------------------------------- #
def test_10_agents_integres_charges():
    reg = registry()
    ids = {a.id for a in reg.all()}
    assert {"orchestrator", "researcher", "coder", "writer", "architect", "analyst",
            "reviewer", "pilot", "coach", "builder"} <= ids
    for a in reg.all():
        assert a.system_prompt and a.role and a.lifecycle
        assert a.autonomy in ("manuel", "assisté", "autonome")


def test_routage_par_affinite():
    reg = registry()
    best, score = reg.best_for("rédige une landing page qui convertit")
    assert best.id == "writer", best.id
    assert score > 1.5
    best2, _ = reg.best_for("fais un diagramme d'architecture du système")
    assert best2.id == "architect"


def test_export_markdown_portable():
    md = registry().export_markdown(registry().require("coder"))
    assert "# 🛠️ Ingénieur" in md and "Prompt système" in md


def test_spec_invalide_autonomie_recalee():
    a = AgentSpec(id="x", name="X", autonomy="nimporte")
    assert a.autonomy == "assisté"
    assert a.lifecycle  # cycle par défaut


# -------------------------------------------------------------------------- #
# Créateur d'agents
# -------------------------------------------------------------------------- #
def test_draft_hors_ligne_produit_une_spec_coherente():
    res = draft("un agent qui relit les contrats, cherche les clauses risquées et produit "
                "un tableau html de synthèse", use_llm=False)
    spec = res.spec
    assert spec.id and spec.name
    assert res.engine == "offline"
    assert "html-composition" in spec.skills or "compose_html" in spec.tools
    assert "compose_html" in spec.tools
    assert spec.lifecycle and "implement" in spec.lifecycle
    assert "Mission" in spec.system_prompt
    assert res.test_recipe
    # pas d'invention : toutes les compétences existent
    lib = SkillLibrary()
    assert set(spec.skills) <= {s.name for s in lib.all()}


def test_draft_description_vide_refusee():
    with pytest.raises(ValueError):
        draft("   ", use_llm=False)


def test_outils_du_draft_tous_enregistres():
    res = draft("un agent qui cherche sur le web, lit les fichiers et mémorise les leçons",
                use_llm=False)
    reg = ToolRegistry()
    unknown = [t for t in res.spec.tools if t not in reg.names()]
    assert unknown == []
