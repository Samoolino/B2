# B2 Tool Engagement and Evidence Register — 2026-11-03

## Authority
A tool responding is **not** evidence that B2 runs, has credentials, or is production ready. Record commands, environment, timestamp, result, artifact and independent reviewer. Unknown means NOT VERIFIED. Trading disabled by default.

| Integration | Assigned role | Observed evidence | Gate |
|---|---|---|---|
| GitHub | source, PR, CI and release provenance | repo writable, draft PR #1 with 8 files verified before additions | verify CI checks and review |
| Linear | accountable tasks and release approvals | B2 project P-ESG-1 created; issues ESG-5 through ESG-11 created | close only with evidence |
| Datadog | host, API, EMQX, Gateway and trade observability | no hosts returned; no B2 monitors returned | ingest telemetry and test alerts |
| Datadog Experiments | flags for paper/live capability and canary controls | no environments returned | create and verify fail-closed controls |
| Replit | prototype Condor/control UI and developer workflow | accessible apps ARBX Arbitrage Bot and Carbon Bridge Gateway; B2 mapping not established | review source and do not assume either is B2 |
| Vercel | stateless Condor frontend delivery | account/team Git context accessible; B2 project not established | connect reviewed UI, not persistent engine |
| Engineering Project OS | checkpoint and evidence handoff | skill loaded; repository-local control plane not installed | add/validate when full repository is accessible |
| Blockscout | public chain, verified contract and transaction inspection | session initialized; chain registry returned | exact chain/contracts and test tx needed |
| Cryptography Research Skills | primary-source review of signing, key custody and TLS claims | skill guidance loaded; no crypto proof executed | key management threat model and audit |
| FiraQuantumSafe | HTTPS/TLS assessment of public B2 host | no B2 hostname supplied; no scan performed | scan only actual B2 deployment hostname |
| Figma | Condor UX and design-to-code review | tools discovered; no existing Condor design file identified | attach original design or approved new file |
| Proxyman | HTTP/TLS troubleshooting in controlled test environment | guidance loaded; no accessible capture or local runtime | sanitized traces, no secrets |
| ShardX Proxy Advisor | optional proxy diagnosis; not a trading requirement | guidance loaded; no proxy configuration provided | avoid unapproved proxy routing |
| OnChainDiligence | policy comparisons and signed receipt verification for supported payments | tools discovered; no payment or receipt reference supplied | not a replacement for order or wallet audit |
| Agentic Atlas | agent tool effect/retry safety patterns | effect-discipline concept consulted (release v1.1.0) | map effects and review approval policy |

## Evidence protocol
Each gate has fields: id, exact source revision, environment, owner, timestamp, method, result (PASS/FAIL/BLOCKED), artifact URL, limitations, reviewer, approval date. Never use PASS for an unexecuted test.

## Deployment split
Replit/Vercel may host UI and prototypes. Persistent Hummingbot, Gateway, EMQX, DB, Telegram and risk controller require an explicitly provisioned persistent runtime. Do not route secrets through UI builders or public proxy services.

## Formal limitations
The Python state-space model enumerates a small abstract order lifecycle only. It does not model exchange matching, distributed consistency, race timing, nonce allocation, key compromise or economic losses. Future TLA+/PlusCal, property-based testing, sandbox tests and chaos testing are separate gates.

## Agent effect discipline
Read-only calls: discard/retry permitted. Idempotent metadata writes: retry with stable request IDs. Order creation, wallet signing and on-chain transfers: treat as potentially irreversible; obtain authorization before effect, record intent and reconcile uncertain outcomes instead of replaying. Atlas: effect-discipline (v1.1.0).

## Go/no-go
Production authorization remains NO-GO until all critical tests have independent evidence, human release approval, safe halt, reconciled venue state, rollback, monitoring and restricted credentials.
