"""Smoke tests for oasf-agent-directory-mcp."""
import sys, os, inspect, traceback
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import (
    describe_agent_as_oasf,
    validate_oasf_schema,
    publish_to_agntcy_directory,
    search_oasf_directory,
    bridge_mcp_to_oasf,
    bridge_a2a_to_oasf,
    list_capabilities,
)


def test_describe_returns_manifest():
    r = describe_agent_as_oasf("acme/bot", "Acme Bot", "Does things", ["compute", "rest_api"])
    assert r["manifest"]["oasf_version"]
    assert r["manifest"]["agent_id"] == "acme/bot"


def test_validate_catches_missing_fields():
    r = validate_oasf_schema({"name": "x"})
    assert r["valid"] is False
    assert any("missing" in i for i in r["issues"])


def test_validate_passes_complete():
    m = describe_agent_as_oasf("a/b", "X", "Y", ["compute"])
    r = validate_oasf_schema(m["manifest"])
    assert r["valid"] is True


def test_publish_scaffold_no_token():
    m = describe_agent_as_oasf("a/b", "X", "Y", ["compute"])
    r = publish_to_agntcy_directory(m["manifest"])
    assert r["published"] is False
    assert r["listing_id"].startswith("agntcy_")


def test_publish_with_token():
    m = describe_agent_as_oasf("a/b", "X", "Y", ["compute"])
    r = publish_to_agntcy_directory(m["manifest"], "tok_demo")
    assert r["published"] is True


def test_search_returns_results():
    r = search_oasf_directory("compliance")
    assert len(r["results"]) >= 1


def test_bridge_mcp_extracts_compliance():
    server = {"name": "io.github.x/eu-ai-act-mcp", "description": "EU AI Act compliance + audit", "version": "1.0.0"}
    r = bridge_mcp_to_oasf(server)
    assert "compliance" in r["manifest"]["capabilities"]


def test_bridge_a2a_extracts_commerce():
    card = {"name": "Bot", "description": "x", "skills": [{"id": "invoice_generation"}], "version": "1.0.0"}
    r = bridge_a2a_to_oasf(card)
    assert "commerce" in r["manifest"]["capabilities"]


def test_list_capabilities_has_taxonomy():
    r = list_capabilities()
    assert "compliance" in r["categories"]
    assert r["total_capabilities"] > 10


if __name__ == "__main__":
    g = dict(globals())
    fns = [v for k, v in g.items() if k.startswith("test_") and inspect.isfunction(v)]
    p = f = 0
    for fn in fns:
        try:
            fn(); print(f"✓ {fn.__name__}"); p += 1
        except Exception as e:
            print(f"✗ {fn.__name__}: {type(e).__name__}: {e}"); traceback.print_exc(); f += 1
    print(f"\n{p} passed, {f} failed")
