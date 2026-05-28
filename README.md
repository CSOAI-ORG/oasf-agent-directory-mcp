# OASF Agent Directory MCP

> ## 🧱 Part of the MEOK A2A Substrate (£499/mo)
> See [meok.ai/a2a](https://meok.ai/a2a).

# Bridges Cisco OASF + AGNTCY Directory under Linux Foundation

<!-- mcp-name: io.github.CSOAI-ORG/oasf-agent-directory-mcp -->

[![PyPI](https://img.shields.io/pypi/v/oasf-agent-directory-mcp)](https://pypi.org/project/oasf-agent-directory-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## What this bridges

Cisco Outshift's **Open Agentic Schema Framework (OASF)** — under Linux Foundation governance via the AGNTCY project. OASF is an OCI-based extensible data model for describing agent capabilities. It supports A2A agents, MCP servers, and Copilot manifests.

This MCP converts MEOK MCPs (and any A2A agent-cards) into OASF manifests so they appear in Cisco's AGNTCY Directory Service — the enterprise procurement layer for agent capability discovery.

## Tools

| Tool | Purpose |
|---|---|
| `describe_agent_as_oasf(agent_id, name, capabilities, ...)` | Emit OASF manifest |
| `validate_oasf_schema(manifest)` | Schema-validate before publish |
| `publish_to_agntcy_directory(manifest, agntcy_token?)` | Submit to live AGNTCY |
| `search_oasf_directory(query, category?)` | Discover other OASF agents |
| `bridge_mcp_to_oasf(mcp_server_json)` | Convert MCP server.json |
| `bridge_a2a_to_oasf(a2a_card)` | Convert A2A agent-card |
| `list_capabilities()` | OASF capability taxonomy |

## Sister MCPs

Part of the MEOK **A2A** pack — bridges to other protocols:

- `agent-commerce-protocol-mcp` — Stripe ACP + AP2 + x402
- `agent-identity-trust-mcp` — W3C DID + Verifiable Credentials
- `agent-handoff-certified-mcp` — signed handoff chain
- `bft-progress-council-mcp` — anti-loop guardrail

Full catalogue: [meok.ai/anthropic-registry](https://meok.ai/anthropic-registry)

## Pricing

| Option | Price |
|---|---|
| Self-host MIT | £0 |
| Universal PAYG | £29/mo + £0.0002/call |
| A2A Substrate | £499/mo |
| Universe | £1,499/mo |
| Defence | £4,990/mo |

Buy: https://meok.ai/a2a

## Licence

MIT. By [MEOK AI Labs](https://meok.ai) (CSOAI LTD, UK Companies House 16939677).

<!-- BUY-LADDER:START -->

## 💸 Try MEOK in 30 seconds — instant buy ladder

| Tier | Price | What you get | Stripe |
|---|---|---|---|
| Smoke test | **£1** | Signed sample MCP-Hardening report + Article 50 PDF | <https://buy.stripe.com/dRmcN75ScdQS7oh1Uc8k90U> |
| Quick Kit | **£9** | EU AI Act Article 50 implementation guide (C2PA + EU-Icon) | <https://buy.stripe.com/cNi00la8s1460ZT0Q88k90V> |
| Founder Call | **£29** | 30-min 1-on-1 with the founder | <https://buy.stripe.com/8x228ta8s6oqbExaqI8k90W> |

> Refundable. UK Stripe — VAT-clean. Builds on the 81-MCP MEOK fleet.
> Verify any signed report at <https://meok.ai/verify>.

<!-- BUY-LADDER:END -->

