# B2 Reference Architecture (v0.1)

## Goal
Preserve Hummingbot's original code and connector semantics while making its management remote, auditable and safe. The B2 MCP plugin is a control-plane adapter, **not** a replacement for Hummingbot or Gateway.

## Service map
| Service | Runtime | Exposure | State |
|---|---|---|---|
| Condor / Dashboard | web frontend | HTTPS + identity provider | backend DB |
| B2 Policy API | persistent container | authenticated HTTPS/private tailnet | audit DB |
| Hummingbot API | persistent container | private Docker network | PostgreSQL/config volumes |
| Hummingbot bots | API-managed instances | private network | config + exchange reconciliation |
| Gateway DEX | persistent container | private network | certs, wallet integration, config |
| EMQX | persistent container | private network | broker volume if required |
| Telegram controller | persistent worker | outbound polling or verified webhook | update offsets/deduplication |
| Tailscale | host or sidecar | tailnet | persisted identity |
| MCP adapter | private service | authenticated agent access | no long-lived trading keys |
| Monitoring | independent telemetry | restricted | durable logs/alerts |

## Trust boundaries
1. Browser may submit credentials over TLS but must never receive stored secret values.
2. Credential intake terminates at a backend with RBAC, MFA, encryption and audit.
3. MCP tools must not directly expose unrestricted shell, Docker socket, database writes or wallet signing.
4. Read-only agent operations are separate from privileged operations.
5. Trading intents pass policy engine, limits, approval (as configured), idempotency ledger and Hummingbot API.
6. Only a single active controller owns each bot; reconnect must reconcile exchange orders before resumption.
7. No assumption that a cloud AI builder is an always-on worker.

## Order intent lifecycle
PROPOSED -> VALIDATED -> AUTHORIZED -> SUBMITTED -> ACKNOWLEDGED -> RECONCILED.
On timeout: UNKNOWN -> RECONCILE (never blindly resubmit).
Any rejected validation: DENIED; any failed reconciliation: HALTED/OPERATOR_REVIEW.

## Telegram
Use a single remote polling worker initially; retain existing bot token only if uncompromised. Enforce allowlisted identities, dedupe update_id, require approval for risk-changing commands, persist command results.

## Version inventory (must complete before integration)
Pin commits/images for hummingbot/hummingbot, hummingbot/gateway, hummingbot/hummingbot-api, hummingbot/mcp, hummingbot/dashboard and existing Condor. Record connector list, Python/Node versions, protocol versions and breaking changes. Never merge upstream libraries blindly.

## Deployment
GitHub CI -> security/test gates -> reviewed immutable image -> staging -> production deployment. Production secrets stay outside GitHub source. Maintain independent backups and rollback artifacts.
