# Fresh B2 implementation: ordered operations

## Baseline

Integrate official Hummingbot core, API, Gateway, EMQX, PostgreSQL, Condor
(including Telegram), Dashboard, MCP and Tailscale. Preserve upstream code.

GitHub main contained only README.md. Documents/tests were recovered from
draft PR #1, feature/b2-operations-foundation, commit
ae0b5f059af8d1f3f7ad0479c4c4bc39f2f76ee3. This workspace is a local Git snapshot
with origin configured, not a clone preserving upstream commit history.

## 1. Source inventory — partially complete

Six immutable upstream commit candidates are in ops/inventory.json. Selected
dependency/build declarations are preserved in ops/evidence/ with source URLs.
These are evidence, not installed dependencies, an SBOM or an approved lock.

Observed compatibility gaps:

- MCP 1.0.4 pins API client 1.2.8; Condor 0.1.0 pins 1.5.9. Keep runtimes
  separate and test both against the selected API schema.
- Condor requires Python >=3.12,<3.14; MCP >=3.11; Dashboard's environment
  selects Python 3.12. Gateway 2.17.0 requires Node >=22.
- Current API Compose selects PostgreSQL 16; MCP's README example uses 15.
  Select the API-supported database and verify migration compatibility.
- API environment.yml leaves hummingbot unpinned and explicitly documents
  required unreleased core fields. Inspect utils/core_compatibility.py and
  pin a matching core build before building the API image.
- Upstream builds use floating image tags and dependency ranges. Source pins
  alone do not make container builds reproducible.
- Condor supplies Telegram and its own web dashboard. The separate legacy
  Dashboard has distinct dependencies and authentication.
- Gateway standalone examples allow development HTTP; the selected API
  documents secured API-managed Gateway. Select one owner and verify mTLS.
- MCP/Condor can mutate upstream state. B2 policy primitives do not enforce
  an authenticated service or prevent bypass.

Remaining: select connectors, venues and sandbox/testnet targets; inspect
lockfiles, licenses, schemas and core checks; record reviewed image digests
for all components. Candidate HEAD revisions are not a compatibility recommendation.

## 2. Persistent host and containerization — blocked

Provide isolated non-production Linux, Docker/Compose, storage, networking and
a secrets manager. Docker CLI is present here, but socket access was denied.
No persistent host or runtime has been provisioned or verified.

Use the pinned API's upstream Compose as the starting point, rather than the
older MCP README example. Override floating images with verified digests.
Keep DB/MQTT private, require broker authentication and topic ACLs, verify
persistent paths and backups. Review API Docker socket access as host authority;
never give that socket to MCP or browser-facing services.

The API manages bots and Gateway. Include their image digests, networking and
storage in the release manifest; do not create competing controllers/Gateways.
Condor has no root Dockerfile at the inspected revision. Containerization must
build its locked Python environment and frontend, run its foreground process,
persist config/state and verify graceful shutdown/single polling ownership.
Its tmux session is not a container health signal. Run legacy Dashboard and
MCP in separate images. MCP's inspected Dockerfile launches a stdio server;
do not invent an HTTP MCP port. Tailscale needs enrollment and reviewed routing
and ACLs; merely adding a sidecar does not configure private ingress.

## 3. Credentials and identity — blocked

Follow docs/CREDENTIALS.md. Provision non-production credentials in the host
secrets manager, TLS, RBAC/MFA, audit and monitoring. No credentials have been
generated, requested or inspected. Do not use Telegram/model prompts for intake.

## 4. Read-only startup — blocked by 1–3

Check storage, DB, MQTT, API and secured Gateway readiness, then make non-trading
exchange/RPC connectivity calls. Implement/test the authenticated B2 adapter
before connecting an agent. Start one Condor worker after sender allowlisting,
deduplication and command authorization tests. Test policy bypass prevention.
Keep funded accounts absent.

## 5. Acceptance and recovery — pending

Execute verification/VERIFICATION.md: contract/RBAC, sandbox reconciliation,
testnet signing/nonce behavior, ownership fencing, fault injection, Telegram
replay, restore drills, monitoring/kill switch and soak tests. Current Python
unit tests and the bounded toy model do not establish these runtime properties.
Attach independent evidence and reviewers for each gate.

## 6. Release — pending

Attach an immutable image manifest, staging evidence, rollback rehearsal,
limits and infrastructure/security/operator signatures. Production is NO-GO
until the runbook's human authorization requirements are met.

## Available commands

From B2:

- make verify: unit tests, bounded model, inventory structure; no services.
- make inventory: validate source pins and report outstanding operations.
- make preflight: exits 2 while integration is blocked.

Inventory validation exit 0 means well-formed data, never permission to deploy.
Preflight cannot enable trading.
