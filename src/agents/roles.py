"""
roles.py

Neutral, governance-safe agent role definitions for the
multi-agent-router-hitl project.

These roles describe *what* each agent is responsible for, not *who* they are.
There is no lore, no personality layer, and no provider-specific coupling.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class AgentRole:
    """
    Declarative description of an agent role inside a HITL multi-agent system.

    The router can use these definitions to:
      - decide which agent is eligible to handle a given task
      - enforce human-in-the-loop approval rules
      - keep responsibilities and escalation paths explicit
    """

    key: str  # short identifier used by the router (e.g. "architect")
    title: str  # human-facing label
    purpose: str  # one-line summary of why this role exists
    responsibilities: List[str] = field(default_factory=list)
    escalation_policy: str = ""
    allow_autonomous_actions: bool = False  # if False → human approval required

    @property
    def requires_human_approval(self) -> bool:
        """
        True when this role must route through a human before any side-effecting
        action is taken.
        """
        return not self.allow_autonomous_actions


def default_roles() -> Dict[str, AgentRole]:
    """
    Return the default set of agent roles used by the router.

    Keys in the returned dict are stable identifiers that can be referenced
    in configuration files, tests, or orchestration logic.
    """
    return {
        "architect": AgentRole(
            key="architect",
            title="Architect Agent",
            purpose="Decompose user goals into a governed, testable plan.",
            responsibilities=[
                "Clarify the user goal and constraints.",
                "Break work into discrete, routable steps.",
                "Assign proposed steps to roles without executing them.",
                "Document assumptions for human review.",
            ],
            escalation_policy=(
                "Escalate to a human whenever requirements are ambiguous, "
                "conflicting, or outside the declared scope of the system."
            ),
            allow_autonomous_actions=False,
        ),
        "validator": AgentRole(
            key="validator",
            title="Validator Agent",
            purpose="Check agent outputs against schemas and governance rules.",
            responsibilities=[
                "Validate structure against expected schemas.",
                "Flag missing fields, type mismatches, or policy violations.",
                "Summarize issues in plain language for the human reviewer.",
            ],
            escalation_policy=(
                "Fail closed on uncertainty. When in doubt, require a human "
                "decision instead of silently accepting output."
            ),
            allow_autonomous_actions=False,
        ),
        "risk": AgentRole(
            key="risk",
            title="Risk & Safety Agent",
            purpose="Scan content for risk, overreach, or policy conflict.",
            responsibilities=[
                "Detect unsafe, non-compliant, or high-risk recommendations.",
                "Highlight language that overstates certainty or guarantees.",
                "Propose safer alternatives without executing them.",
            ],
            escalation_policy=(
                "Route any medium or high-risk findings to a human approver. "
                "Never auto-execute actions that change external state."
            ),
            allow_autonomous_actions=False,
        ),
        "creative": AgentRole(
            key="creative",
            title="Creative Agent",
            purpose="Generate options, drafts, and variations within constraints.",
            responsibilities=[
                "Produce alternative drafts or solution options.",
                "Stay within the brief, schemas, and routing constraints.",
                "Label speculative content clearly as exploratory.",
            ],
            escalation_policy=(
                "All creative outputs are treated as drafts. A human or "
                "validator must approve before anything is executed or published."
            ),
            allow_autonomous_actions=False,
        ),
    }


def get_role_registry() -> Dict[str, AgentRole]:
    """
    Convenience accessor used by the router to obtain the role registry.

    Separated into its own function so future versions can load roles from
    configuration while keeping a simple import path for small demos.
    """
    return default_roles()
