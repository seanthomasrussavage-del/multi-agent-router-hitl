"""
Basic sanity tests for the human-in-the-loop router.

These tests are intentionally lightweight: they assert that the
public surface area exists and that a route() call produces an
auditable decision object rather than a raw model response.
"""

from dataclasses import is_dataclass
from typing import Any
import importlib


def _get_router_module():
    """Helper so imports are in one place."""
    return importlib.import_module("router.hitl_router")


def test_router_module_importable():
    """Router module can be imported as router.hitl_router."""
    module = _get_router_module()
    assert module is not None


def test_public_types_exist():
    """
    The router module should expose the core governance types that other
    systems depend on: HitlRouter, RouteDecision, and AuditRecord.
    """
    module = _get_router_module()

    assert hasattr(module, "HitlRouter")
    assert hasattr(module, "RouteDecision")
    assert hasattr(module, "AuditRecord")

    # RouteDecision and AuditRecord are expected to be dataclasses so their
    # fields are explicit and easily logged / serialized.
    assert is_dataclass(module.RouteDecision)
    assert is_dataclass(module.AuditRecord)


def test_route_produces_audit_record():
    """
    Calling route() should return an AuditRecord-like object that contains
    both the decision and a correlation identifier for logging.
    """
    module = _get_router_module()
    HitlRouter = module.HitlRouter          # type: ignore[attr-defined]
    AuditRecord = module.AuditRecord        # type: ignore[attr-defined]

    # Constructor is expected to be lightweight and safe to call with defaults.
    router = HitlRouter()

    audit: Any = router.route(
        user_input="example user question",
        candidate_role="research_agent",
    )

    # Shape, not exact implementation details.
    assert isinstance(audit, AuditRecord)
    assert getattr(audit, "decision") is not None
    assert getattr(audit.decision, "agent_role") == "research_agent"
    assert getattr(audit.decision, "allowed") in {True, False}
    assert isinstance(getattr(audit, "correlation_id"), str)
    assert getattr(audit, "correlation_id")
