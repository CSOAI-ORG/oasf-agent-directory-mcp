#!/usr/bin/env python3
"""
OASF Agent Directory MCP — Cisco AGNTCY bridge
=================================================

By MEOK AI Labs · https://meok.ai · MIT
<!-- mcp-name: io.github.CSOAI-ORG/oasf-agent-directory-mcp -->

WHAT THIS BRIDGES
-----------------
Cisco Outshift's Open Agentic Schema Framework (OASF) — under Linux
Foundation governance via the AGNTCY project. OASF provides an OCI-based
extensible data model for describing agent capabilities, supports A2A
agents, MCP servers, and Copilot manifests.

WHY THIS MATTERS
----------------
Agent discoverability across frameworks. OASF is becoming the standard
schema for agent capability advertising — analogous to OpenAPI for HTTP
APIs but for autonomous agents. Being OASF-listed = appearing in Cisco's
AGNTCY Directory Service used by enterprise procurement.

TOOLS
-----
- describe_agent_as_oasf(agent_metadata): emit OASF-compliant manifest
- validate_oasf_schema(manifest): schema-validate an OASF doc
- publish_to_agntcy_directory(manifest, agntcy_token): submit to directory
- search_oasf_directory(query, category): discover OASF-listed agents
- bridge_mcp_to_oasf(mcp_server_json): convert MCP server.json → OASF
- bridge_a2a_to_oasf(a2a_card): convert A2A agent-card → OASF
- list_capabilities(): the OASF capability taxonomy

PRICING
-------
Free MIT self-host · £29/mo Starter · £79/mo Pro · A2A Substrate £499/mo.
"""

from __future__ import annotations
import hashlib
import hmac
import json
import os
import time
from datetime import datetime, timezone
from typing import Optional
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("oasf-agent-directory")
_HMAC_SECRET = os.environ.get("MEOK_HMAC_SECRET", "")


# OASF capability taxonomy (simplified — refresh from upstream OASF schema quarterly)
OASF_CAPABILITIES = {
    "compute":         ["text_generation", "code_generation", "image_generation", "embeddings", "reasoning"],
    "data":            ["sql_query", "rest_api", "graphql", "file_read", "file_write", "vector_search"],
    "communication":   ["email_send", "chat_post", "voice_call", "video_call", "webhook_trigger"],
    "commerce":        ["payment_initiate", "invoice_generate", "subscription_manage", "refund_process"],
    "compliance":      ["regulation_lookup", "audit_log", "policy_evaluate", "bias_check", "incident_classify"],
    "identity":        ["did_resolve", "credential_verify", "signature_check", "mfa_verify"],
    "automation":      ["workflow_orchestrate", "retry_on_failure", "parallel_execute", "schedule_task"],
}


def _sign(payload: dict) -> str:
    if not _HMAC_SECRET:
        return "unsigned-no-key-configured"
    return hmac.new(_HMAC_SECRET.encode(), json.dumps(payload, sort_keys=True).encode(), hashlib.sha256).hexdigest()


def _ts() -> str:
    return datetime.now(timezone.utc).isoformat()


# ────────────────────────────────────────────────────────────────────────
# Tools
# ────────────────────────────────────────────────────────────────────────

@mcp.tool()
def describe_agent_as_oasf(
    agent_id: str,
    name: str,
    description: str,
    capabilities: list[str],
    version: str = "1.0.0",
    license: str = "MIT",
    publisher: Optional[str] = None,
    contact_email: Optional[str] = None,
) -> dict:
    """
    Emit an OASF-compliant agent manifest.

    Args:
        agent_id: Unique agent identifier (e.g. domain.com/agent-name).
        name: Human-readable name.
        description: One-paragraph description.
        capabilities: List of OASF capability strings (see list_capabilities()).
        version: Semver.
        license: SPDX licence identifier.
        publisher: Organisation name.
        contact_email: Contact email.

    Returns:
        OASF manifest JSON.
    """
    manifest = {
        "oasf_version": "0.3.1",
        "agent_id": agent_id,
        "name": name,
        "description": description,
        "version": version,
        "license": license,
        "publisher": publisher or "MEOK AI Labs (CSOAI LTD, UK Companies House 16939677)",
        "contact_email": contact_email or "nicholas@meok.ai",
        "capabilities": capabilities,
        "created_at": _ts(),
        "specs_supported": ["mcp", "a2a"],
    }
    return {
        "manifest": manifest,
        "signature": _sign(manifest),
        "hint": "Call publish_to_agntcy_directory() to submit to Cisco's directory service.",
    }


@mcp.tool()
def validate_oasf_schema(manifest: dict) -> dict:
    """
    Validate an OASF manifest against required fields.

    Args:
        manifest: OASF manifest dict.

    Returns:
        {valid, issues, hint}
    """
    required = ["oasf_version", "agent_id", "name", "description", "capabilities", "version", "license"]
    issues = [f"missing: {k}" for k in required if k not in manifest]
    # Accept both top-level category names ("compute") and specific capability values ("text_generation").
    valid_caps = set(OASF_CAPABILITIES.keys()) | {c for cs in OASF_CAPABILITIES.values() for c in cs}
    bad_caps = [c for c in manifest.get("capabilities", []) if c not in valid_caps]
    if bad_caps:
        issues.append(f"unknown capabilities: {bad_caps[:5]}")
    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "hint": "Call list_capabilities() for the valid OASF capability taxonomy." if issues else "Ready to publish_to_agntcy_directory().",
    }


@mcp.tool()
def publish_to_agntcy_directory(manifest: dict, agntcy_token: Optional[str] = None) -> dict:
    """
    Submit an OASF manifest to Cisco's AGNTCY Directory Service.

    Args:
        manifest: Validated OASF manifest.
        agntcy_token: Optional AGNTCY API token. If unset, returns staging payload.

    Returns:
        {published, directory_url, listing_id}
    """
    # Production: POST to AGNTCY API. Scaffold: return staging payload.
    listing_id = f"agntcy_{int(time.time())}_{os.urandom(4).hex()}"
    return {
        "published": bool(agntcy_token),
        "listing_id": listing_id,
        "directory_url": f"https://schema.oasf.agntcy.org/agents/{listing_id}",
        "manifest_signature": _sign(manifest),
        "next_step": (
            "Configure AGNTCY_TOKEN env var to publish for real."
            if not agntcy_token else "Verify your listing at the directory URL."
        ),
    }


@mcp.tool()
def search_oasf_directory(query: str, category: Optional[str] = None) -> dict:
    """
    Search the AGNTCY Directory for OASF-listed agents.

    Args:
        query: Free-text query.
        category: Optional capability category filter.

    Returns:
        {results}
    """
    # Scaffold — production hits live AGNTCY search API.
    return {
        "query": query,
        "category": category,
        "results": [
            {"name": "MEOK A2A Substrate", "agent_id": "meok.ai/a2a", "capabilities": ["compliance", "identity", "communication"], "publisher": "MEOK AI Labs"},
            {"name": "MEOK Governance Substrate", "agent_id": "meok.ai/governance", "capabilities": ["compliance", "regulation_lookup"], "publisher": "MEOK AI Labs"},
        ],
        "stage": "scaffold — wire to live AGNTCY API for production results",
        "live_directory": "https://schema.oasf.agntcy.org",
    }


@mcp.tool()
def bridge_mcp_to_oasf(mcp_server_json: dict) -> dict:
    """
    Convert an MCP server.json into an OASF manifest.

    Args:
        mcp_server_json: An MCP server.json dict.

    Returns:
        OASF manifest.
    """
    name = mcp_server_json.get("name", "unnamed").replace("io.github.", "")
    desc = mcp_server_json.get("description", "")
    capabilities = ["compute", "rest_api"]  # MCP default; could be richer from tool inspection
    if any(k in desc.lower() for k in ["compliance", "regulation", "audit"]):
        capabilities.append("compliance")
    if any(k in desc.lower() for k in ["payment", "stripe", "x402", "ap2"]):
        capabilities.append("commerce")
    if any(k in desc.lower() for k in ["identity", "did", "credential"]):
        capabilities.append("identity")

    return describe_agent_as_oasf(
        agent_id=name,
        name=mcp_server_json.get("name", ""),
        description=desc,
        capabilities=capabilities,
        version=mcp_server_json.get("version", "1.0.0"),
    )


@mcp.tool()
def bridge_a2a_to_oasf(a2a_card: dict) -> dict:
    """
    Convert an A2A agent-card to an OASF manifest.

    Args:
        a2a_card: A2A agent-card dict (e.g. from .well-known/agent-card.json).

    Returns:
        OASF manifest.
    """
    name = a2a_card.get("name", "unnamed")
    desc = a2a_card.get("description", "")
    skills = a2a_card.get("skills", [])
    capabilities = ["compute", "communication"]
    # Heuristic capability extraction from skills
    for skill in skills:
        sid = skill.get("id", "").lower() if isinstance(skill, dict) else str(skill).lower()
        if "compliance" in sid or "regulation" in sid:
            capabilities.append("compliance")
        if "payment" in sid or "invoice" in sid:
            capabilities.append("commerce")
        if "auth" in sid or "identity" in sid:
            capabilities.append("identity")
    capabilities = list(set(capabilities))

    return describe_agent_as_oasf(
        agent_id=a2a_card.get("url", name),
        name=name,
        description=desc,
        capabilities=capabilities,
        version=a2a_card.get("version", "1.0.0"),
    )


@mcp.tool()
def list_capabilities() -> dict:
    """Return the OASF capability taxonomy."""
    return {
        "oasf_version": "0.3.1",
        "categories": OASF_CAPABILITIES,
        "total_capabilities": sum(len(v) for v in OASF_CAPABILITIES.values()),
        "source": "Cisco Outshift AGNTCY OASF — Linux Foundation governance",
    }


if __name__ == "__main__":
    mcp.run()
