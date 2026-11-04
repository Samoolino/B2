"""Minimal local, offline, read-only MCP server for B2.

This process has no network client, exchange connector, credential intake, or
order submission. Only run it as a local stdio child, never behind a remote
stdio-to-HTTP adapter without an independently reviewed auth boundary.
"""
import json
import sys
from pathlib import Path
from typing import TextIO

INVENTORY = Path(__file__).resolve().parents[1] / "ops" / "inventory.json"
PROTOCOL_VERSION = "2025-03-26"
MAX_LINE_BYTES = 1024 * 1024
TOOLS = [
    {
        "name": "b2.offline_preflight",
        "title": "B2 offline deployment preflight",
        "description": (
            "Read-only offline check of source inventory structure. "
            "Does not probe services or authorize deployment."
        ),
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False},
    },
    {
        "name": "b2.inventory_summary",
        "title": "B2 source inventory summary",
        "description": (
            "Returns the number of candidate upstream components and outstanding "
            "inventory/operations items. Never returns credentials or raw config."
        ),
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False},
    },
]


def summary(inventory_path: Path = INVENTORY) -> dict:
    """Fail closed, returning sanitized counts but never user-provided strings."""
    result = {
        "source_inventory_valid": False,
        "runtime_checked": False,
        "integration_status": "BLOCKED",
        "deployment_authorized": False,
        "live_trading_enabled": False,
    }
    try:
        from ops.preflight import report

        inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
        validated = report(inventory)
        if validated.get("integration_status") != "BLOCKED" or validated.get("deployment_authorized") is not False:
            return result
        if validated.get("live_trading_enabled") is not False:
            return result
        result.update(
            source_inventory_valid=True,
            candidate_source_count=validated["observed_source_count"],
            outstanding_inventory_items=len(inventory["pending_inventory"]),
            outstanding_operations_items=len(inventory["pending_operations"]),
        )
    except (ValueError, OSError, KeyError, TypeError, ImportError):
        pass
    return result


def response(id_, result=None, error=None):
    payload = {"jsonrpc": "2.0", "id": id_}
    if error is not None:
        payload["error"] = error
    else:
        payload["result"] = result
    return payload


def handle(message, inventory_path: Path = INVENTORY):
    if not isinstance(message, dict) or message.get("jsonrpc") != "2.0":
        return response(None, error={"code": -32600, "message": "Invalid Request"})
    if "id" not in message:
        return None  # Notifications never receive a JSON-RPC response.
    id_ = message["id"]
    if id_ is None or isinstance(id_, (dict, list, bool)):
        return response(None, error={"code": -32600, "message": "Invalid Request"})
    method = message.get("method")
    if method == "initialize":
        return response(id_, {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": "b2-offline-verify", "version": "0.1.0"},
            "instructions": "Local/offline verification only. No Hummingbot API, Gateway, or exchange access.",
        })
    if method == "ping":
        return response(id_, {})
    if method == "tools/list":
        return response(id_, {"tools": TOOLS})
    if method == "tools/call":
        params = message.get("params")
        if not isinstance(params, dict):
            return response(id_, error={"code": -32602, "message": "Invalid params"})
        name = params.get("name")
        args = params.get("arguments", {})
        if not isinstance(args, dict) or args or name not in {t["name"] for t in TOOLS}:
            return response(id_, error={"code": -32602, "message": "Unsupported tool or arguments"})
        info = summary(inventory_path)
        if name == "b2.offline_preflight":
            output = {key: info[key] for key in (
                "source_inventory_valid", "runtime_checked", "integration_status",
                "deployment_authorized", "live_trading_enabled")}
        else:
            output = info
        return response(id_, {
            "content": [{"type": "text", "text": json.dumps(output, sort_keys=True)}],
            "structuredContent": output,
            "isError": not info["source_inventory_valid"],
        })
    return response(id_, error={"code": -32601, "message": "Method not found"})


def serve(input_stream: TextIO = sys.stdin, output_stream: TextIO = sys.stdout,
          inventory_path: Path = INVENTORY):
    for line in input_stream:
        try:
            if len(line.encode("utf-8")) > MAX_LINE_BYTES:
                reply = response(None, error={"code": -32700, "message": "Message too large"})
            else:
                reply = handle(json.loads(line), inventory_path)
        except (ValueError, UnicodeError):
            reply = response(None, error={"code": -32700, "message": "Parse error"})
        if reply is not None:
            output_stream.write(json.dumps(reply, separators=(",", ":")) + "\n")
            output_stream.flush()


if __name__ == "__main__":
    serve()
