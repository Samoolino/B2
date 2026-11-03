import unittest
from verification.state_space import check, State, transitions

class ModelTests(unittest.TestCase):
    def test_bounded_model(self):
        states, edges = check()
        self.assertGreaterEqual(states, 5)
        self.assertGreater(edges, states)
    def test_unknown_ack_cannot_resubmit(self):
        s = State(phase="unknown", approved=True, risk_ok=True, submissions=1)
        for event, next_state in transitions(s):
            self.assertLessEqual(next_state.submissions, 1)
            self.assertNotEqual(event, "submit")
    def test_owner_fencing(self):
        s = State(phase="ready", approved=True, risk_ok=True, owner=2, controller=1)
        self.assertNotIn("submit", [e for e, _ in transitions(s)])
