import copy
import io
import json
from contextlib import redirect_stdout
from pathlib import Path
import tempfile
import unittest

from ops.preflight import DEFAULT_INVENTORY, main, report


class PreflightTests(unittest.TestCase):
    def setUp(self):
        self.inventory = json.loads(DEFAULT_INVENTORY.read_text())

    def test_pinned_sources_do_not_imply_deployment_permission(self):
        result = report(self.inventory)
        self.assertEqual(result["observed_source_count"], 6)
        self.assertEqual(result["integration_status"], "BLOCKED")
        self.assertFalse(result["deployment_authorized"])
        self.assertFalse(result["live_trading_enabled"])
        self.assertTrue(result["blockers"])

    def test_rejects_missing_duplicate_mutable_and_unrelated_sources(self):
        mutations = [
            lambda d: d["sources"].pop(),
            lambda d: d["sources"].append(d["sources"][0]),
            lambda d: d["sources"][0].update(revision="latest"),
            lambda d: d["sources"][0].update(repository="other/hummingbot"),
            lambda d: d["sources"][0].update(evidence_url="https://example.com"),
            lambda d: d["sources"][0].update(compatibility="verified"),
            lambda d: d.update(pending_inventory=[]),
            lambda d: d.update(mode="live"),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                data = copy.deepcopy(self.inventory)
                mutate(data)
                with self.assertRaises(ValueError):
                    report(data)

    def test_requires_literal_false_for_trading(self):
        for value in (True, 0, "false", None):
            with self.subTest(value=value):
                self.inventory["live_trading_enabled"] = value
                with self.assertRaises(ValueError):
                    report(self.inventory)

    def test_cli_distinguishes_valid_inventory_from_operational_readiness(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(main(["--check-inventory"]), 0)
            self.assertEqual(main([]), 2)

    def test_invalid_input_fails_without_echoing_contents(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            path.write_text('{"private_value": "DO_NOT_ECHO",')
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(["--inventory", str(path)]), 1)
            self.assertNotIn("DO_NOT_ECHO", output.getvalue())
            self.assertFalse(json.loads(output.getvalue())["deployment_authorized"])
