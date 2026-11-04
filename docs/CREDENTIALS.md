# Full-stack credential contract

Fresh installation uses official Hummingbot components and Condor as the Telegram
controller. These are names and destinations only. No credentials have been
provisioned or verified. Populate them through a server-side secrets manager on
the chosen non-production host, separately from production.

| Component | Required material | Consumer / relationship |
|---|---|---|
| Hummingbot API | USERNAME, PASSWORD, CONFIG_PASSWORD | API authentication and bot credential encryption; independent generated values |
| PostgreSQL | database user/password and DATABASE_URL | API URL must match provisioned DB; URL-encode password characters |
| EMQX | BROKER_USERNAME, BROKER_PASSWORD, separate BROKER_DASHBOARD_PASSWORD | API/bot MQTT credentials, bootstrap user file and deny-by-default topic ACL |
| Tailscale | scoped enrollment identity or TS_AUTHKEY | Tailscale only; define device tags and least-privilege tailnet ACLs |
| Telegram / Condor | TELEGRAM_TOKEN, allowlisted ADMIN_USER_ID | Exactly one Condor polling worker |
| Condor API connection | API URL and authentication in Condor server configuration | Match API credentials; do not assume environment variables configure Condor servers |
| Gateway | TLS CA/client/server certificates and encryption passphrase | API-managed secured Gateway; verify certificate paths and secret mapping at pinned revision |
| MCP upstream | HUMMINGBOT_API_URL, HUMMINGBOT_USERNAME, HUMMINGBOT_PASSWORD | Initial config only; upstream persists connection configuration in server.yml |
| Dashboard | server-side credentials.yml, signing cookie secret and API connection | Enable AUTH_SYSTEM_ENABLED=True; validate backend compatibility |
| Exchange sandbox | venue sandbox key with withdrawals disabled | Approved backend intake only; no live keys in this phase |
| DEX testnet | test-only signing identity and RPC access | Dedicated signing boundary; keys never exposed to MCP/browser |
| B2 policy gateway | identity-provider configuration, audience and audit-store identity | Not implemented by the existing policy function; required before connecting agents |
| Optional AI provider | provider credential | Condor server-side only; do not enable autonomous trading loops |

The API Tailscale setup helper uses TAILSCALE_AUTH_KEY; the Tailscale container
uses TS_AUTHKEY. Map the selected deployment method explicitly.

Secret files, backups and container metadata need restricted access. .gitignore
is not a secrets manager. Do not log expanded Docker Compose configuration with
real credentials; use quiet validation. Never include secret values in evidence.

Before startup, prove API authentication rejects defaults/anonymous requests,
MQTT rejects anonymous clients and unauthorized topics, dashboard authentication
is enabled, tailnet access is restricted and Gateway requires certificates.
Rehearse restore before changing CONFIG_PASSWORD, which protects existing bot
credentials. Configure monitoring and audit retention before credential intake.

Upstream Condor and MCP expose trading and credential-management operations.
Starting them with API credentials does not enforce B2's proposed read-only
contract. Do not connect them to funded accounts or an agent until the actual
authenticated B2 boundary and bypass prevention are tested.
