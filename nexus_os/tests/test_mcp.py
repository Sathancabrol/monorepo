"""Le client MCP est testé contre un **vrai serveur MCP**, pas une maquette.

Le serveur ci-dessous implémente la révision 2026-07-28 : cœur stateless,
`server/discover`, `tools/list`, `tools/call`, Server Card en `.well-known/mcp.json`,
et les en-têtes de routage `MCP-Protocol-Version` / `Mcp-Method` / `Mcp-Name`.
Il tourne sur un port réel, donc `urllib` (le transport de `nexus_os.mcp`) est
exercé pour de vrai.
"""
from __future__ import annotations

import contextlib
import json
import socket
import threading
import time

import pytest
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from nexus_os import config, context as ctxmod, mcp
from nexus_os.instincts import InstinctBook
from nexus_os.tools import ToolContext, ToolRegistry

GROS_PAYLOAD = "\n".join(f'ligne {i}: donnée de démonstration {"x" * 40}' for i in range(120))


# -------------------------------------------------------------------------- #
# Serveur MCP de référence
# -------------------------------------------------------------------------- #
def make_server() -> FastAPI:
    app = FastAPI()
    seen: list[dict] = []
    app.state.seen = seen

    @app.get("/.well-known/mcp.json")
    def card():
        return {"name": "Démo MCP", "description": "Serveur de test NEXUS·OS",
                "version": "1.0.0", "url": "http://test/mcp",
                "capabilities": {"tools": {"listChanged": False}},
                "securitySchemes": {"bearer": {"type": "http", "scheme": "bearer"}}}

    @app.post("/mcp")
    async def rpc(request: Request):
        body = await request.json()
        seen.append({"headers": dict(request.headers), "body": body})
        method = body.get("method")
        params = body.get("params", {})
        meta = params.get("_meta", {})

        # Le serveur refuse une requête qui ne se décrit pas (cœur stateless).
        if meta.get("io.modelcontextprotocol/protocolVersion") != mcp.PROTOCOL_VERSION:
            return JSONResponse({"jsonrpc": "2.0", "id": body.get("id"),
                                 "error": {"code": -32602, "message": "_meta.protocolVersion requis"}})

        if method == "server/discover":
            return {"jsonrpc": "2.0", "id": body.get("id"), "result": {
                "protocolVersion": mcp.PROTOCOL_VERSION,
                "serverInfo": {"name": "demo-mcp", "version": "1.0.0"},
                "capabilities": {"tools": {"listChanged": False}},
                "instructions": "Deux outils de démonstration."}}

        if method == "tools/list":
            return {"jsonrpc": "2.0", "id": body.get("id"), "result": {"tools": [
                {"name": "echo", "description": "Répète le texte reçu.",
                 "inputSchema": {"type": "object",
                                 "properties": {"text": {"type": "string"}},
                                 "required": ["text"]}},
                {"name": "big_dump", "description": "Renvoie un volumineux rapport.",
                 "inputSchema": {"type": "object", "properties": {}}},
                {"name": "boom", "description": "Échoue toujours.",
                 "inputSchema": {"type": "object", "properties": {}}},
            ]}}

        if method == "tools/call":
            name = params.get("name")
            args = params.get("arguments", {})
            if name == "echo":
                return {"jsonrpc": "2.0", "id": body.get("id"), "result": {
                    "content": [{"type": "text", "text": f"écho : {args.get('text', '')}"}],
                    "structuredContent": {"reçu": args.get("text", "")},
                    "isError": False}}
            if name == "big_dump":
                return {"jsonrpc": "2.0", "id": body.get("id"), "result": {
                    "content": [{"type": "text", "text": GROS_PAYLOAD}], "isError": False}}
            if name == "boom":
                return {"jsonrpc": "2.0", "id": body.get("id"), "result": {
                    "content": [{"type": "text", "text": "panne volontaire"}],
                    "isError": True}}
            return JSONResponse({"jsonrpc": "2.0", "id": body.get("id"),
                                 "error": {"code": -32601, "message": f"outil inconnu : {name}"}})

        return JSONResponse({"jsonrpc": "2.0", "id": body.get("id"),
                             "error": {"code": -32601, "message": f"méthode inconnue : {method}"}})

    return app


def _free_port() -> int:
    with contextlib.closing(socket.socket()) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="module")
def mcp_server():
    app = make_server()
    port = _free_port()
    srv = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=port,
                                        log_level="critical", lifespan="off"))
    thread = threading.Thread(target=srv.run, daemon=True)
    thread.start()
    deadline = time.time() + 15
    while time.time() < deadline and not srv.started:
        time.sleep(0.05)
    assert srv.started, "le serveur MCP de test n'a pas démarré"
    yield app, f"http://127.0.0.1:{port}/mcp"
    srv.should_exit = True
    thread.join(timeout=5)


@pytest.fixture(autouse=True)
def isolated_mcp(tmp_path, monkeypatch):
    """Registre MCP, références et instincts dans une sandbox jetable."""
    monkeypatch.setattr(mcp, "REGISTRY_FILE", tmp_path / "mcp.json")
    monkeypatch.setattr(config, "WORKSPACE_DIR", tmp_path / "workspace")
    monkeypatch.setattr(config, "ALLOW_NETWORK", True)
    (tmp_path / "workspace").mkdir(parents=True, exist_ok=True)
    yield tmp_path


# -------------------------------------------------------------------------- #
# Protocole
# -------------------------------------------------------------------------- #
def test_le_client_parle_la_revision_2026_07_28(mcp_server):
    _, url = mcp_server
    assert mcp.PROTOCOL_VERSION == "2026-07-28"
    cfg = mcp.ServerConfig("demo", url)
    info = mcp.discover(cfg)
    assert info["protocol_version"] == "2026-07-28"
    assert info["server_info"]["name"] == "demo-mcp"
    assert "tools" in info["capabilities"]


def test_chaque_requete_est_auto_descriptive(mcp_server):
    """Stateless : pas de handshake, `_meta` + en-têtes sur chaque message."""
    app, url = mcp_server
    cfg = mcp.ServerConfig("demo", url)
    mcp.call_tool(cfg, "echo", {"text": "ping"})
    last = app.state.seen[-1]
    meta = last["body"]["params"]["_meta"]
    assert meta["io.modelcontextprotocol/protocolVersion"] == "2026-07-28"
    assert meta["io.modelcontextprotocol/clientInfo"]["name"] == "nexus-os"
    assert "io.modelcontextprotocol/clientCapabilities" in meta
    # En-têtes de routage : un proxy peut router sans lire le corps.
    assert last["headers"]["mcp-protocol-version"] == "2026-07-28"
    assert last["headers"]["mcp-method"] == "tools/call"
    assert last["headers"]["mcp-name"] == "echo"
    # Aucun identifiant de session nulle part.
    assert "mcp-session-id" not in last["headers"]
    assert "initialize" not in {s["body"]["method"] for s in app.state.seen}


def test_server_card_lue_sans_connexion(mcp_server):
    _, url = mcp_server
    cfg = mcp.ServerConfig("demo", url)
    card = mcp.fetch_card(cfg)
    assert card["name"] == "Démo MCP" and card["version"] == "1.0.0"
    assert mcp.card_url(url).endswith("/.well-known/mcp.json")


def test_outils_listes_et_appelables(mcp_server):
    _, url = mcp_server
    cfg = mcp.ServerConfig("demo", url)
    assert [t["name"] for t in mcp.list_tools(cfg)] == ["echo", "big_dump", "boom"]
    out = mcp.call_tool(cfg, "echo", {"text": "bonjour"})
    assert "écho : bonjour" in out
    assert "```json" in out, "structuredContent doit être remonté"


def test_une_erreur_outil_devient_une_erreur(mcp_server):
    _, url = mcp_server
    with pytest.raises(mcp.MCPError, match="panne volontaire"):
        mcp.call_tool(mcp.ServerConfig("demo", url), "boom", {})


def test_methode_inconnue_remonte_l_erreur_jsonrpc(mcp_server):
    _, url = mcp_server
    with pytest.raises(mcp.MCPError, match="méthode inconnue"):
        mcp.rpc(mcp.ServerConfig("demo", url), "prompts/list")


def test_reseau_coupe_refuse_l_appel(mcp_server, monkeypatch):
    monkeypatch.setattr(config, "ALLOW_NETWORK", False)
    with pytest.raises(mcp.MCPError, match="réseau désactivé"):
        mcp.discover(mcp.ServerConfig("demo", "http://127.0.0.1:1/mcp"))


def test_serveur_injoignable_ne_fait_pas_tomber_l_os(mcp_server):
    cfg = mcp.ServerConfig("fantôme", "http://127.0.0.1:1/mcp")
    info = mcp.probe(cfg)
    assert info["status"] == "erreur" and info["error"]
    assert info["tools"] == []


# -------------------------------------------------------------------------- #
# Registre et intégration au runtime
# -------------------------------------------------------------------------- #
def test_registre_persistant(mcp_server, isolated_mcp):
    _, url = mcp_server
    mcp.add_server("demo", url, description="serveur de test")
    assert [s.name for s in mcp.list_servers()] == ["demo"]
    assert mcp.get_server("demo").url == url
    assert mcp.remove_server("demo") is True
    assert mcp.remove_server("demo") is False
    assert mcp.list_servers() == []


def test_url_invalide_refusee(isolated_mcp):
    with pytest.raises(ValueError):
        mcp.add_server("x", "ftp://mauvais")
    with pytest.raises(ValueError):
        mcp.add_server("", "http://ok/mcp")


def test_outils_mcp_exposes_au_registre(mcp_server, isolated_mcp):
    _, url = mcp_server
    mcp.add_server("demo", url)
    reg = ToolRegistry()
    names = reg.names()
    assert {"mcp__demo__echo", "mcp__demo__big_dump", "mcp__demo__boom"} <= set(names)
    out = reg.execute("mcp__demo__echo", {"text": "via le registre"}, ToolContext())
    assert "écho : via le registre" in out


def test_serveur_desactive_n_expose_rien(mcp_server, isolated_mcp):
    _, url = mcp_server
    mcp.add_server("demo", url, enabled=False)
    assert "mcp__demo__echo" not in ToolRegistry().names()


def test_namespacing_evite_l_ecrasement():
    assert mcp.tool_name("demo", "echo") == "mcp__demo__echo"
    assert mcp.tool_name("demo", "search issues") == "mcp__demo__search_issues"
    assert mcp.split_tool_name("mcp__demo__echo") == ("demo", "echo")
    assert mcp.split_tool_name("grep") is None
    assert mcp.split_tool_name("mcp__demo") is None


# -------------------------------------------------------------------------- #
# Résultats référencés
# -------------------------------------------------------------------------- #
def test_un_gros_resultat_mcp_devient_une_reference(mcp_server, isolated_mcp):
    _, url = mcp_server
    mcp.add_server("demo", url)
    reg = ToolRegistry()
    ctx = ToolContext(workspace=isolated_mcp / "workspace")
    out = reg.execute("mcp__demo__big_dump", {}, ctx)
    assert len(out) < len(GROS_PAYLOAD)
    assert out.startswith("[référence ref-0001")
    assert "tokens économisés" in out
    assert "read_file(" in out
    st = ctxmod.stats()
    assert st["references"] == 1 and st["tokens_saved"] > 100
    # Le contenu complet reste accessible dans la sandbox.
    fichiers = list((isolated_mcp / "workspace" / "references").glob("ref-0001-*.txt"))
    assert len(fichiers) == 1 and fichiers[0].read_text() == GROS_PAYLOAD


def test_un_resultat_court_reste_inline(isolated_mcp):
    ctx = ToolContext(workspace=isolated_mcp / "workspace")
    assert ctxmod.reference(ctx, "court") == "court"
    assert ctxmod.stats()["references"] == 0


def test_l_empreinte_decrit_la_forme(isolated_mcp):
    ctx = ToolContext(workspace=isolated_mcp / "workspace")
    gros = json.dumps([{"id": i, "nom": f"élément {i}"} for i in range(200)],
                      ensure_ascii=False)
    out = ctxmod.reference(ctx, gros, kind="test")
    assert "JSON array, 200 éléments" in out and "id" in out


def test_clear_supprime_les_references(isolated_mcp):
    ctx = ToolContext(workspace=isolated_mcp / "workspace")
    ctxmod.reference(ctx, "x" * 5000, kind="test")
    assert ctxmod.stats()["references"] == 1
    assert ctxmod.clear() == 1
    assert ctxmod.stats()["references"] == 0
    assert list((isolated_mcp / "workspace" / "references").glob("ref-*.txt")) == []


def test_compaction_d_historique():
    from nexus_os.context import compact, compaction_ratio

    events = [
        {"type": "tool_call", "name": "grep", "args": {"pattern": "TODO"}},
        {"type": "tool_result", "name": "grep", "ok": True, "result": "3 occurrences"},
        {"type": "artifact", "path": "workspace/rapport.md"},
        {"type": "approval_required", "name": "shell", "reason": "outil sensible"},
        {"type": "message", "text": "Fait : 3 TODO restants.\nDétail ignoré.",
         "confidence": "confiant"},
        {"type": "thinking", "text": "bruit qui ne doit pas survivre " * 40},
    ]
    out = compact(events, task="audite les TODO")
    assert "audite les TODO" in out and "grep" in out and "rapport.md" in out
    assert "bruit qui ne doit pas survivre" not in out
    assert compaction_ratio(events, out) < 0.2


# -------------------------------------------------------------------------- #
# Instincts
# -------------------------------------------------------------------------- #
def test_instincts_appris_d_un_echec(isolated_mcp):
    from nexus_os.runtime import RunResult

    book = InstinctBook(isolated_mcp / "instincts.json")
    res = RunResult(run_id="r1", agent_id="coder")
    res.events = [
        {"type": "tool_call", "name": "shell", "args": {}},
        {"type": "tool_result", "name": "shell", "ok": False, "result": "refusé : non autorisé"},
        {"type": "approval_required", "name": "shell", "reason": "outil sensible"},
    ]
    learned = book.learn_from_result(res, "lance un test shell")
    assert len(learned) >= 2
    assert any("shell" in i.rule and "échoué" in i.rule for i in learned)
    assert any("autorisation" in i.rule for i in learned)


def test_un_instinct_se_renforce_au_lieu_de_se_dupliquer(isolated_mcp):
    book = InstinctBook(isolated_mcp / "instincts.json")
    a = book.add("Vérifie la migration avant de déployer.", triggers=["deploy"], agent_id="devops")
    b = book.add("Vérifie la migration avant de déployer.", triggers=["deploy"], agent_id="devops")
    assert a.id == b.id and b.hits == 2 and b.confidence > a.confidence
    assert book.count() == 1


def test_injection_ciblee_par_agent_et_tache(isolated_mcp):
    book = InstinctBook(isolated_mcp / "instincts.json")
    book.add("Cite la page du contrat.", triggers=["contrat", "clause"], agent_id="jurist")
    book.add("Ne jamais pousser sur main.", triggers=["deploy"], agent_id="devops")
    picked = book.for_task("relis cette clause de contrat", "jurist")
    assert [i.agent_id for i in picked] == ["jurist"]
    assert book.for_task("relis cette clause", "devops") == []
    assert "Instincts" in book.render("relis cette clause", "jurist")
    assert book.render("rien à voir", "coder") == ""


def test_regle_trop_courte_refusee(isolated_mcp):
    book = InstinctBook(isolated_mcp / "instincts.json")
    with pytest.raises(ValueError):
        book.add("trop court")


def test_le_runtime_injecte_et_apprend(isolated_mcp, monkeypatch):
    from nexus_os import instincts as inst_mod
    from nexus_os.runtime import Runtime

    book = InstinctBook(isolated_mcp / "instincts.json")
    monkeypatch.setattr(inst_mod, "_book", book)
    rt = Runtime()
    events, res = _drain(rt.run("relis cette clause de contrat et cite la page", "jurist"))
    assert any(e["type"] == "instincts_learned" for e in events)
    assert book.count() > 0

    # Seconde exécution : ce qui a été appris revient dans le prompt système.
    prompt = rt.agents.require("jurist").base_prompt(
        "", "", book.render("relis cette clause de contrat", "jurist"))
    assert "## Instincts" in prompt


def _drain(gen):
    events = []
    try:
        while True:
            events.append(next(gen))
    except StopIteration as stop:
        return events, stop.value


# -------------------------------------------------------------------------- #
# A2A
# -------------------------------------------------------------------------- #
def test_carte_a2a_valide():
    from nexus_os.agents import registry
    from nexus_os.harness import export_spec

    card = json.loads(export_spec(registry().require("researcher"), "a2a"))
    assert card["protocolVersion"] == "1.0"
    assert card["skills"][0]["id"] == "researcher"
    assert card["capabilities"]["streaming"] is True
    assert card["x-nexus"]["agent_id"] == "researcher"
    assert card["securitySchemes"]["bearer"]["scheme"] == "bearer"


# -------------------------------------------------------------------------- #
# Rafraîchissement à chaud et remontée du travail délégué
# -------------------------------------------------------------------------- #
def test_un_serveur_ajoute_devient_utilisable_sans_redemarrer(mcp_server, isolated_mcp):
    _, url = mcp_server
    reg = ToolRegistry()
    assert "mcp__demo__echo" not in reg.names()
    mcp.add_server("demo", url)
    assert reg.refresh_mcp() == 3
    assert "mcp__demo__echo" in reg.names()
    mcp.remove_server("demo")
    reg.refresh_mcp()
    assert "mcp__demo__echo" not in reg.names()


def test_le_cache_ne_rappelle_pas_le_reseau_a_chaque_run(mcp_server, isolated_mcp):
    _, url = mcp_server
    mcp.add_server("demo", url)
    first = mcp.registry_tools(force=True)
    second = mcp.registry_tools()          # doit sortir du cache
    assert [t.name for t in first] == [t.name for t in second]


def test_le_travail_delegue_remonte_au_parent():
    """Sans remontée, l'apprentissage ne voit qu'une délégation vide."""
    from nexus_os.runtime import RunResult, _merge

    parent = RunResult(run_id="p", agent_id="orchestrator")
    sub = RunResult(run_id="s", agent_id="coder")
    sub.events = [
        {"type": "tool_call", "name": "grep", "args": {}},
        {"type": "tool_result", "name": "grep", "ok": True, "result": "3"},
        {"type": "thinking", "text": "bruit interne"},
        {"type": "context_reference", "name": "grep", "chars": 9000},
        {"type": "artifact", "path": "workspace/r.md"},
    ]
    sub.tool_failures = 1
    sub.pending_approvals = ["shell"]
    sub.tokens, sub.steps = 500, 3
    _merge(parent, sub)

    types = [e["type"] for e in parent.events]
    assert {"tool_call", "tool_result", "context_reference", "artifact"} <= set(types)
    assert "thinking" not in types, "le raisonnement interne ne doit pas remonter"
    assert parent.tool_failures == 1 and parent.pending_approvals == ["shell"]
    assert parent.tokens == 500 and parent.steps == 3


def test_un_run_orchestre_apprend_quelque_chose(isolated_mcp, monkeypatch):
    from nexus_os import instincts as inst_mod
    from nexus_os.runtime import Runtime

    monkeypatch.setattr(inst_mod, "_book", InstinctBook(isolated_mcp / "i.json"))
    rt = Runtime()
    events, res = _drain(rt.run("audite ce dépôt et produis un rapport détaillé",
                                "orchestrator"))
    assert any(e["type"] == "handoff" for e in events), "l'orchestrateur devait déléguer"
    assert any(e["type"] == "instincts_learned" for e in events), \
        "un run délégué doit quand même produire un apprentissage"
