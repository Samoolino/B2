# B2 Agent Operating Instructions

1. Treat repository as NOT production-ready until release gate signed and attached.
2. Never request or print private keys, exchange API secrets, Telegram tokens or live RPC credentials.
3. Do not execute trading or signing tools from model outputs.
4. Inspect actual upstream versions and source before modifying Hummingbot, Gateway or Condor.
5. All privileged actions require separate identity authorization, policy check, audit, and operator approval.
6. On uncertain order status, reconcile by client order ID; never blind retry.
7. Record evidence in docs/TOOL-ENGAGEMENT-REGISTER.md and Linear project P-ESG-1.
8. Test in CI and staging before any deployment; no live trade without explicit human authorization.
9. Use persistent host for long-lived services; Vercel/Replit UI is not a substitute.
10. Do not claim formal proof from passing unit tests or a bounded toy model.
