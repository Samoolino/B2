# B2 progress — 2026-11-04

**Project state: offline operations foundation. No runtime deployment. Live trading disabled.**

## Completed

- Recovered the architecture, operations runbook, proposed MCP contract, policy
  primitives and bounded model from the original foundation branch.
- Recorded six immutable upstream source candidates with selected dependency,
  container-build and license snapshots. These are not approved compatible builds.
- Documented the fresh-install sequence and full-stack credential requirements
  for API, bots, Gateway, EMQX, database, Tailscale, Condor/Telegram, Dashboard and MCP.
- Added an offline preflight command that distinguishes valid inventory from
  operational readiness. It never grants deployment or trading permission.
- Added inventory tests and the CI inventory-validation command.

## Verification

On 2026-11-04, `make verify` passed locally with Python 3.12.14:

- 12 unit tests passed.
- The simplified bounded model explored 10 states and 14 transitions.
- All six source inventory entries passed structural validation.
- `git diff --check` passed.

The operational preflight reports BLOCKED, with exit code 2 as designed.
These results do not establish upstream compatibility, service availability,
exchange correctness, formal proof or production readiness. GitHub Actions
results are recorded on the pull request separately from local results.

## Outstanding work, in order

1. Select sandbox venues/connectors and testnet targets. Resolve API-client/core
   compatibility, inspect dependency locks/licenses and approve immutable images.
2. Provision an isolated persistent Docker host, private networking and storage.
   The previous workspace Docker query was denied socket access; no runtime was verified.
3. Provision server-side secrets, identity, TLS, RBAC/MFA, durable audit and monitoring.
4. Implement the authenticated read-only B2 MCP boundary and test bypass prevention;
   the current policy function alone does not constrain upstream Condor/MCP writes.
5. Execute staging, sandbox/testnet, reconciliation, ownership fencing, Telegram
   replay, fault injection, backup/restore and rollback acceptance tests.
6. Obtain independent release review and explicit operator production authorization.

No credentials have been provisioned, funded accounts connected or orders sent.
Merging this progress is source publication only; it does not deploy services.

See [implementation plan](IMPLEMENTATION-PLAN.md), [credential requirements](CREDENTIALS.md),
[operations runbook](OPERATIONS.md) and [verification plan](../verification/VERIFICATION.md).
