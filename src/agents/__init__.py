"""
ASMA Agents Registry
multi-agent-router-hitl / src/agents/__init__.py

Purpose:
    Provide a clear, human-readable registry of the core ASMA agents
    and their responsibilities inside the multi-agent router.

    This module is deliberately descriptive:
        • It explains WHO each agent is.
        • It explains WHAT each agent is responsible for.
        • It does NOT execute anything on its own.

    Execution and governance are handled by the HITL Router.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class AgentSpec:
    """
    Canonical description of an agent.

    Fields:
        code   – short identifier used in routing (e.g., "SOL")
        title  – human-readable role name
        scope  – one-line summary of what this agent is allowed to do
    """
    code: str
    title: str
    scope: str


# ---------------------------------------------------------------------------
# Core ASMA Agents
# ---------------------------------------------------------------------------

AGENTS: Dict[str, AgentSpec] = {
    "SOL": AgentSpec(
        code="SOL",
        title="Architect",
        scope="Designs structure, sequences steps, and keeps the system coherent."
    ),
    "MANI": AgentSpec(
        code="MANI",
        title="Validator",
        scope="Checks timing, rules, and governance before anything is approved."
    ),
    "LOKI": AgentSpec(
        code="LOKI",
        title="Risk & Edge-Case Scout",
        scope="Surfaces blind spots, stress-tests assumptions, and flags failure modes."
    ),
    "MUSE": AgentSpec(
        code="MUSE",
        title="Creative Generator",
        scope="Produces variations and options without changing final decisions."
    ),
}

__all__ = ["AgentSpec", "AGENTS"]
