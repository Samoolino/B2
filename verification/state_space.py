"""Bounded exhaustive verification of a *simplified* B2 order lifecycle.

This is not a TLA+ proof, exchange test or guarantee of real-world behavior.
Run: python -m verification.state_space
"""
from dataclasses import dataclass, replace
from collections import deque

@dataclass(frozen=True)
class State:
    phase: str = "proposed"
    approved: bool = False
    risk_ok: bool = False
    owner: int = 1
    controller: int = 1
    submissions: int = 0
    reconciled: bool = False
    halted: bool = False

def transitions(s):
    if s.phase == "proposed":
        yield "approve", replace(s, approved=True, phase="approved")
        yield "deny", replace(s, halted=True, phase="halted")
    if s.phase == "approved":
        yield "risk_pass", replace(s, risk_ok=True, phase="ready")
        yield "risk_fail", replace(s, halted=True, phase="halted")
    if s.phase == "ready":
        if s.approved and s.risk_ok and s.owner == s.controller:
            yield "submit", replace(s, phase="unknown", submissions=s.submissions+1)
        yield "lose_ownership", replace(s, owner=s.owner+1, phase="halted", halted=True)
    if s.phase == "unknown":
        yield "retry_blocked", s
        yield "reconcile", replace(s, phase="reconciled", reconciled=True)
        yield "halt", replace(s, phase="halted", halted=True)
    if s.phase == "reconciled":
        yield "complete", replace(s, phase="complete")
    if s.phase == "halted":
        yield "stay_halted", s

def check(max_states=10000):
    initial = State()
    queue = deque([initial])
    seen = {initial}
    edges = 0
    while queue:
        state = queue.popleft()
        assert state.submissions <= 1, "duplicate submission"
        assert not state.submissions or (state.approved and state.risk_ok), "unauthorized order"
        assert not state.submissions or state.controller == state.owner, "unfenced controller"
        for event, next_state in transitions(state):
            edges += 1
            if next_state not in seen:
                seen.add(next_state)
                assert len(seen) <= max_states, "state bound exceeded"
                queue.append(next_state)
    return len(seen), edges

if __name__ == "__main__":
    states, edges = check()
    print(f"PASS bounded model: {states} states, {edges} transitions")
