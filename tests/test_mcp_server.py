import io
import json
import tempfile
from pathlib import Path
import unittest

from b2_mcp.server import handle, serve


class OfflineMCPTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "inventory.json"
        self.path.write_text('{"schema_version":1}', encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    @staticmethod
    def rpc(method, params=None):
        return {"jsonrpc": "2.0", "id": 10, "method": method, "params": params or {}}

    def test_initialize_and_tools_are_read_only(self):
        self.assertEqual(handle(self.rpc("initialize"))["result"]["serverInfo"]["name"], "b2-offline-verify")
        tools = handle(self.rpc("tools/list"))["result"]["tools"]
        self.assertEqual({x["name"] for x in tools}, {"b2.offline_preflight", "b2.inventory_summary"})
        self.assertTrue(all(x["annotations"]["readOnlyHint"] for x in tools))

    def test_inventory_failure_blocks_trading(self):
        output = handle(self.rpc("tools/call", {"name": "b2.offline_preflight"}), self.path)
        result = output["result"]["structuredContent"]
        self.assertEqual(result["integration_status"], "BLOCKED")
        self.assertFalse(result["deployment_authorized"])
        self.assertFalse(result["live_trading_enabled"])
        self.assertTrue(output["result"]["isError"])

    def test_valid_inventory_still_blocks_trading(self):
        from ops.preflight import DEFAULT_INVENTORY
        output = handle(self.rpc("tools/call", {"name": "b2.inventory_summary"}), DEFAULT_INVENTORY)
        result = output["result"]["structuredContent"]
        self.assertTrue(result["source_inventory_valid"])
        self.assertEqual(result["candidate_source_count"], 6)
        self.assertFalse(result["runtime_checked"])
        self.assertFalse(result["deployment_authorized"])
        self.assertFalse(result["live_trading_enabled"])
        self.assertFalse(output["result"]["isError"])

    def test_unsafe_tools_and_arguments_rejected(self):
        for name in ("b2.propose_order", "b2.control_bot", "shell.exec", "b2.check_health"):
            self.assertEqual(handle(self.rpc("tools/call", {"name": name}))["error"]["code"], -32602)
        self.assertEqual(handle(self.rpc("tools/call", {"name": "b2.offline_preflight", "arguments": {"execute": True}}))["error"]["code"], -32602)
        self.assertEqual(handle(self.rpc("tools/call", {"name": "b2.offline_preflight", "arguments": None}))["error"]["code"], -32602)

    def test_unknown_method_invalid_json_and_notifications(self):
        self.assertEqual(handle(self.rpc("tools/discover"))["error"]["code"], -32601)
        self.assertIsNone(handle({"jsonrpc": "2.0", "method": "notifications/initialized"}))
        input_stream = io.StringIO('garbage\n' + json.dumps(self.rpc("ping")) + '\n')
        output_stream = io.StringIO()
        serve(input_stream, output_stream, self.path)
        lines = [json.loads(x) for x in output_stream.getvalue().splitlines()]
        self.assertEqual(lines[0]["error"]["code"], -32700)
        self.assertEqual(lines[1]["result"], {})

    def test_never_reflects_arbitrary_inventory_text(self):
        self.path.write_text('{"secret":"SENSITIVE_DO_NOT_ECHO"}', encoding="utf-8")
        out = handle(self.rpc("tools/call", {"name": "b2.inventory_summary"}), self.path)
        self.assertNotIn("SENSITIVE_DO_NOT_ECHO", json.dumps(out))

    def test_rejects_invalid_jsonrpc(self):
        self.assertEqual(handle({"id": 1, "method": "initialize"})["error"]["code"], -32600)


if __name__ == "__main__":
    unittest.main()
