"""Deny-by-default policy gate for proposed MCP trading actions.

This module is intentionally independent of exchange connectivity.
"""
from dataclasses import dataclass
from enum import Enum


class Decision(str, Enum):
    DENY = "deny"
    ALLOW_READ = "allow_read"
    REQUIRE_APPROVAL = "require_approval"


READ_TOOLS = frozenset({
    "b2.check_health", "b2.list_bots",
    "b2.inspect_gateway", "b2.validate_strategy"
})
PRIVILEGED_TOOLS = frozenset({
    "b2.propose_deployment", "b2.control_bot", "b2.propose_order"
})


@dataclass(frozen=True)
class Principal:
    identity: str
    roles: frozenset[str]
    authenticated: bool


def authorize(principal: Principal, tool: str, *, production: bool = True) -> Decision:
    """No state-changing tool returns ALLOW; independent approval is mandatory."""
    if not principal.authenticated or not principal.identity.strip():
        return Decision.DENY
    if tool in READ_TOOLS and "viewer" in principal.roles.union({"viewer"} if "operator" in principal.roles or "admin" in principal.roles else set()):
        return Decision.ALLOW_READ
    if tool in PRIVILEGED_TOOLS and ("operator" in principal.roles or "admin" in principal.roles):
        return Decision.REQUIRE_APPROVAL
    return Decision.DENY
