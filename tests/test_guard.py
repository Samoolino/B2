import unittest
from b2_policy.guard import Principal, Decision, authorize


class PolicyTests(unittest.TestCase):
    def test_anonymous_denied(self):
        p = Principal("", frozenset({"admin"}), False)
        self.assertEqual(authorize(p, "b2.list_bots"), Decision.DENY)

    def test_viewer_read_only(self):
        p = Principal("reader", frozenset({"viewer"}), True)
        self.assertEqual(authorize(p, "b2.list_bots"), Decision.ALLOW_READ)
        self.assertEqual(authorize(p, "b2.propose_order"), Decision.DENY)

    def test_operator_requires_approval(self):
        p = Principal("operator1", frozenset({"operator"}), True)
        self.assertEqual(authorize(p, "b2.propose_order"), Decision.REQUIRE_APPROVAL)

    def test_unknown_tool_denied(self):
        p = Principal("admin1", frozenset({"admin"}), True)
        self.assertEqual(authorize(p, "b2.execute_shell"), Decision.DENY)


if __name__ == "__main__":
    unittest.main()
