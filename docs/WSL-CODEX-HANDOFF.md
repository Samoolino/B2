# B2 WSL / Codex handoff — 2026-11-04

## Verified repository continuity

- Repository: `https://github.com/Samoolino/B2`.
- At inspection, `main` was merge commit `44aec60dae76b8fc8da018badcac98a9da7b6258` (PR #1 merged).
- GitHub Actions for this commit: policy unit tests [success](https://github.com/Samoolino/B2/actions/runs/41752901238) and bounded verification [success](https://github.com/Samoolino/B2/actions/runs/41752901212).
- Existing checkpoint: `docs/PROGRESS.md`, inventory in `ops/inventory.json`, preflight `ops/preflight.py`, implementation plan in `docs/IMPLEMENTATION-PLAN.md`.
- All six upstream commits are **observed candidates** and compatibility remains **pending**. This B2 repository does not contain the imported Hummingbot engine.
- No running Docker/Hummingbot/Gateway/Condor/Telegram service, testnet exchange engagement, remote host or live trading is verified.

### First-run inside the actual WSL2 Ubuntu shell

Check that the terminal is WSL, and prefer the Linux filesystem rather than `/mnt/c`:

```bash
printf '%s\n' "${WSL_DISTRO_NAME:-not-wsl}"
mkdir -p ~/code && cd ~/code
git clone https://github.com/Samoolino/B2.git
cd B2
git status --short --branch
make verify
set +e
make preflight
preflight_status=$?
set -e
printf 'preflight exit status: %s (expected 2 while blocked)\n' "$preflight_status"
test "$preflight_status" -eq 2
```

If an existing `~/code/B2` clone exists, **do not overwrite it**: inspect `git status`, save uncommitted work safely, `git fetch origin` and reconcile before switching branches.

Install Codex in WSL using the [official Linux installer](https://github.com/openai/codex/blob/main/README.md) (if not already present):

```bash
command -v codex || { curl -fsSL https://chatgpt.com/codex/install.sh | sh; }
codex --version
codex login
```

From the B2 repository, register the local-only MCP endpoint. The launcher changes directory to the repository root, irrespective of the invoking directory:

```bash
codex mcp add b2-offline -- bash "$PWD/scripts/b2-mcp"
codex mcp list
```

Use `codex mcp add` only after this feature branch has been merged or checked out, because `scripts/b2-mcp` is a new artifact. This MCP advertises two offline inventory tools, and **no** order, bot-control, Docker or credential tools. It cannot validate running service health.

### Let Codex implement the next stages on a dedicated development branch

```bash
git switch main
git pull --ff-only
git switch -c feat/runtime-integration
codex --sandbox workspace-write --ask-for-approval on-request
```

Paste the task in [CODEX-EXECUTION-TASK.md](CODEX-EXECUTION-TASK.md) into the Codex session. For noninteractive use, the [Codex CLI documentation](https://learn.chatgpt.com/docs/cli/reference) describes `codex exec`:

```bash
codex exec -C "$PWD" --sandbox workspace-write "$(cat docs/CODEX-EXECUTION-TASK.md)"
```

The local Codex CLI is not running in this chat. Its results must be confirmed in WSL logs and PR checks before being reported as executed. Do not enable autonomous execution, provide funded credentials or bypass sandbox approvals.

## MCP transport boundary

`b2_mcp.server` uses a local JSON-RPC stdio transport. It does not connect to any exchange or expose an HTTP port. The underlying shell/session user is the trust boundary; do not turn it into an unauthenticated internet endpoint. At runtime `b2.offline_preflight` and `b2.inventory_summary` only validate and summarize local inventory with all release gates BLOCKED.

## Definition of a successful follow-up

A follow-up result needs a commit SHA and tests, exact image hashes, service inventory, authenticated API smoke tests, one-worker Condor Telegram test, Gateway TLS test, CEX sandbox/DEX testnet evidence, independent reconciliation and recovery proof, plus human operator signoff. Unit-test success alone is not live operational authorization.
