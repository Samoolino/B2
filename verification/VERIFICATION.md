# B2 Formal Verification and Acceptance Plan

**Current result: NOT VERIFIED.** These are specifications, not completed proofs.

## Safety properties
- AUTH: Every state-changing command has authenticated principal, role and approval policy.
- UNIQUE: For each (account, venue, client_order_id), at most one intended submission exists.
- RISK: No order is sent if post-trade exposure exceeds configured hard limits.
- OWNERSHIP: At most one active controller owns a bot instance at any moment.
- SECRET: No secret or signing key appears in agent-visible results, browser responses or logs.
- RECOVERY: After uncertain exchange response, reconcile before retrying.
- HALT: If risk engine or order-state reconciliation is unavailable, new order submission stops.

## Suggested formal models
Model a state machine in TLA+ or PlusCal with variables: orderState, requestId, principal, approvals, exposure, controllerEpoch, exchangeStatus. Model retries, duplicate Telegram updates, worker crashes, network partitions and stale leases. Check invariant preservation and eventual recovery under explicitly stated fairness assumptions. Document what the model excludes.

## Test matrix
| Gate | Evidence | Pass criterion |
|---|---|---|
| Source audit | version manifest + dependency graph | every component pinned |
| Static checks | lint, type checks, secret scan, SCA | no critical unresolved findings |
| MCP contract | schema + RBAC tests | read-only operations cannot mutate |
| CEX sandbox | create/cancel/reject/reconcile | no duplicate or untracked orders |
| Gateway testnet | chain/RPC failover, nonce/signing tests | safe recovery, no unintended signing |
| Fault injection | kill API/EMQX/worker; partition RPC | safe halt and reconciliation |
| Telegram | replay, unauthorized sender, out-of-order updates | reject/dedupe correctly |
| Backup/restore | restore DB/config/identity | documented recovery works |
| Load/uptime | monitoring, latency, soak tests | SLO agreed and measured |
| Production pilot | explicit human approval + low limits | no breached hard invariant |

## Release decision
Go-live requires signed review by infrastructure, security and trading operator, evidence links, exchange permissions checked, kill switch tested, and rollback runbook rehearsed. A model-check pass alone is insufficient for live-trading authorization.
