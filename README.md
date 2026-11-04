# B2 — Hummingbot Operations and Verification

**Status: architecture scaffold, not a production trading deployment. LIVE TRADING DISABLED.**

This repository is intended to integrate the upstream Hummingbot core, Hummingbot API, Gateway, MCP, EMQX, Condor, Dashboard, Telegram and Tailscale without replacing their implementations.

## Deployment boundaries
- **Execution plane:** persistent Docker host for Hummingbot API, Gateway, EMQX, PostgreSQL, bots and Telegram controller.
- **Control plane:** Condor, dashboard and an authenticated B2 policy gateway.
- **Agent plane:** read-only MCP operations initially; write operations require independent authorization, risk checks, audit and approval.
- **Secrets:** server-side secret manager only. No exchange secrets or wallet keys in browser, Git or LLM prompts.

## State
This repository initially contained no application code. The present scaffold documents contracts and safety gates; it does not include the upstream Hummingbot code, a deployed plugin, or a verified exchange connector.

Read [the architecture](docs/ARCHITECTURE.md), [operations runbook](docs/OPERATIONS.md), and [verification plan](verification/VERIFICATION.md) before integration.

## Non-negotiable
Do not activate live trading until upstream source/version inventory, test environment, threat model, exchange sandbox tests, formal model checks, fault injection, human authorization and rollback drills are complete.

## Fresh installation checkpoint

See [current progress and outstanding work](docs/PROGRESS.md).

Start with [the ordered implementation plan](docs/IMPLEMENTATION-PLAN.md) and
[full-stack credential requirements](docs/CREDENTIALS.md). Condor supplies the
Telegram controller; the legacy Dashboard remains a separate component.

Run `make verify` for offline tests and inventory validation. Run `make preflight`
to report integration blockers (exit 2 is expected while blocked). Six upstream
commit candidates are recorded in `ops/inventory.json`; they are not an approved
compatibility lock. No runtime or credentials have been deployed.
