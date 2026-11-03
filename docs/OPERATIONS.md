# B2 Standard Operating Procedure (SOP v0.1)

## 1. Provisioning
1. Inventory existing working Condor, Telegram and Hummingbot deployments; do not overwrite.
2. Provision hardened Linux host, Docker Engine/Compose, private network, Tailscale and restricted SSH.
3. Create separate non-production and production environments.
4. Configure secrets manager, TLS, RBAC, MFA, audit log and external monitoring.
5. Pin upstream Hummingbot API, Gateway, MCP, EMQX and database images. Verify licenses and compatibility.
6. Restore approved configurations; keep wallet keys in dedicated signing boundary.

## 2. Start-up
1. Confirm storage, secrets, DB, EMQX, Gateway and API readiness.
2. Validate exchange/RPC connectivity with non-trading calls.
3. Start one Telegram worker and MCP read-only adapter.
4. Compare remote exchange balances/open orders against local records.
5. Enable bot monitoring; leave execution disabled until operator authorization.

## 3. Daily checks
- Confirm host resources, container health, DB backups, EMQX connectivity, Tailscale and TLS expiry.
- Compare order state and positions with each venue; investigate discrepancies.
- Check RPC latency/errors, rate limits, exchange status, wallet balances and gas.
- Review alerts, pending approvals, rejected requests and audit logs.
- Verify kill switch and risk limit configuration without triggering trades.

## 4. Incident response
**Unknown order status:** block retry, query venue using idempotency/client order ID, reconcile, then release halt.
**RPC or Gateway failure:** stop new DEX submissions; inspect pending transactions and nonce state.
**EMQX or API failure:** mark dependent bots degraded; avoid optimistic state changes.
**Compromised credential:** disable affected account, revoke/rotate secret, review activity and reconcile.
**Host failure:** restore on standby only after lease/ownership fencing prevents split-brain.

## 5. Change management
Every change requires issue/PR, pinned dependency versions, automated checks, staging test, approval, scheduled rollout, rollback procedure and post-deploy observation. AI agents may propose changes but cannot self-approve production execution.

## 6. Credential operations
Create exchange keys at venue with minimum permissions, withdrawals disabled where possible, IP restrictions if supported. Enter via secured backend, encrypt at rest, test permissions, audit rotation and revocation. Never put private keys or tokens in Telegram, GitHub issues, ChatGPT prompts or frontend local storage.

## 7. Recovery and rollback
Back up DB/config and verify restores. Keep last known-good image manifests. On rollback, first stop/fence active execution, reconcile orders and balances, then redeploy. Do not assume restarting a container resolves unknown exchange state.

## 8. Production authorization
Human operator signs a release record including account/venue, permitted strategy, notional limits, loss limits, escalation contacts, kill switch test, incident playbook and monitoring coverage. Initial deployment defaults to paper/read-only mode.
