"""
HITL Router (Human-In-The-Loop)
ASMA-Aligned Multi-Agent Control Surface

Purpose:
    Define WHO gets to act in a multi-agent system and under what
    governed conditions. All agent outputs must pass through this
    router before being surfaced, executed, or stored.

Principles:
    • No agent executes without validation.
    • All agent proposals are treated as suggestions, not decisions.
    • Routing is transparent, replayable, and auditable.
    • Human authority (ASTA) is the final gate of execution.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Any, Dict, Optional


# ---------------------------------------------------------------------------
# 1. Agent Registry (ASMA Roles)
# ---------------------------------------------------------------------------

class AgentRole(Enum):
    SOL = "architect"       # structure, synthesis
    MANI = "validator"      # governance, rules, timing
    LOKI = "risk"           # edge-case detection, pressure tests
    MUSE = "creative"       # variation, generative ideation
    UNKNOWN = "unknown"     # fallback


# ---------------------------------------------------------------------------
# 2. Agent Proposal Object
# ---------------------------------------------------------------------------

@dataclass
class AgentProposal:
    role: AgentRole
    content: str
    metadata: Optional[Dict[str, Any]] = None


# ---------------------------------------------------------------------------
# 3. HITL Router Core
# ---------------------------------------------------------------------------

class HITLRouter:
    """
    Central governance router.

    Enforces:
        • Role validation
        • Proposal normalization
        • Optional risk scanning
        • Human-final review
    """

    def __init__(self):
        self.log = []  # append-only governance ledger (in-memory stub)

    # 3.1 Normalize input to AgentProposal
    def normalize(self, role: AgentRole, content: str,
                  metadata: Optional[Dict[str, Any]] = None) -> AgentProposal:
        return AgentProposal(role=role, content=content.strip(), metadata=metadata or {})

    # 3.2 Validate agent identity + allowed domains
    def validate_role(self, proposal: AgentProposal) -> bool:
        return proposal.role in AgentRole

    # 3.3 Risk Scan (stub for future Loki integration)
    def risk_scan(self, proposal: AgentProposal) -> bool:
        """Return False if content looks unsafe, hype-driven, or overreaching."""
        flagged_terms = ["guarantee", "promise", "unstoppable", "perfect accuracy"]
        return not any(term in proposal.content.lower() for term in flagged_terms)

    # 3.4 Append-only ledger
    def log_proposal(self, proposal: AgentProposal) -> None:
        self.log.append({
            "role": proposal.role.value,
            "content": proposal.content,
            "metadata": proposal.metadata
        })

    # 3.5 Human Review Gate (placeholder)
    def human_review(self, proposal: AgentProposal) -> bool:
        """
        HITL Gate.
        True = approved by Human Authority.
        False = rejected or returned for revision.
        In production this routes to UI, CLI, or signed approval layer.
        """
        return True  # placeholder (always approved for now)

    # 3.6 Execution path
    def route(self, proposal: AgentProposal) -> Dict[str, Any]:
        """Full governance pipeline."""

        # Step 1: Validate
        if not self.validate_role(proposal):
            return {"status": "rejected", "reason": "invalid-role"}

        # Step 2: Risk Scan
        if not self.risk_scan(proposal):
            return {"status": "rejected", "reason": "risk-detected"}

        # Step 3: Ledger
        self.log_proposal(proposal)

        # Step 4: Human Review
        if not self.human_review(proposal):
            return {"status": "rejected", "reason": "human-rejected"}

        # Step 5: Approved
        return {
            "status": "approved",
            "role": proposal.role.value,
            "content": proposal.content
        }


# ---------------------------------------------------------------------------
# 4. Module-Level Helper
# ---------------------------------------------------------------------------

def submit(role: AgentRole, content: str, metadata: Optional[Dict[str, Any]] = None):
    """Convenience helper for quickly submitting proposals to router."""
    router = HITLRouter()
    proposal = router.normalize(role, content, metadata)
    return router.route(proposal)
