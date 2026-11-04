"""Validate the offline inventory and report blockers, without contacting services.

Exit 0: inventory structure valid (--check-inventory only).
Exit 1: invalid inventory. Exit 2: integration remains blocked.
This command never authorizes deployment or trading.
"""
import argparse
import json
from pathlib import Path
import re


REPOSITORIES = {
    "hummingbot", "hummingbot-api", "gateway", "mcp", "dashboard", "condor"
}
DEFAULT_INVENTORY = Path(__file__).with_name("inventory.json")


def report(data):
    if not isinstance(data, dict) or type(data.get("schema_version")) is not int or data["schema_version"] != 1:
        raise ValueError("unsupported inventory schema")
    if data.get("mode") != "read_only" or data.get("live_trading_enabled") is not False:
        raise ValueError("inventory must keep read-only mode and trading disabled")
    sources = data.get("sources")
    if not isinstance(sources, list):
        raise ValueError("sources must be a list")
    seen = set()
    for source in sources:
        if not isinstance(source, dict):
            raise ValueError("source must be an object")
        name = source.get("component")
        if not isinstance(name, str) or name not in REPOSITORIES or name in seen:
            raise ValueError("unknown or duplicate source component")
        seen.add(name)
        if source.get("repository") != f"hummingbot/{name}":
            raise ValueError("unexpected upstream repository")
        revision = source.get("revision")
        if not isinstance(revision, str) or not re.fullmatch(r"[0-9a-f]{40}", revision):
            raise ValueError("every upstream requires a full immutable commit SHA")
        expected_url = f"https://github.com/hummingbot/{name}/commit/{revision}"
        if source.get("evidence_url") != expected_url:
            raise ValueError("source evidence must reference the pinned commit")
        if source.get("status") != "observed_candidate" or source.get("compatibility") != "pending":
            raise ValueError("this bootstrap supports observed candidates only; release review is separate")
    if seen != REPOSITORIES:
        raise ValueError("required upstream components are missing")
    blockers = []
    for field in ("pending_inventory", "pending_operations"):
        items = data.get(field)
        if not isinstance(items, list) or not items or any(not isinstance(x, str) or not x.strip() for x in items):
            raise ValueError(f"{field} must contain explicit outstanding work")
        blockers.extend(items)
    return {
        "inventory_valid": True,
        "observed_source_count": len(sources),
        "integration_status": "BLOCKED",
        "deployment_authorized": False,
        "live_trading_enabled": False,
        "blockers": ["Candidate source compatibility has not been verified", *blockers],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--check-inventory", action="store_true", help="Check inventory structure only; does not clear operational gates")
    args = parser.parse_args(argv)
    try:
        result = report(json.loads(args.inventory.read_text(encoding="utf-8")))
    except (OSError, ValueError) as error:
        # Do not echo file contents or JSON values, which could contain secrets.
        print(json.dumps({"inventory_valid": False, "error_type": type(error).__name__, "deployment_authorized": False}))
        return 1
    print(json.dumps(result, indent=2))
    return 0 if args.check_inventory else 2


if __name__ == "__main__":
    raise SystemExit(main())
