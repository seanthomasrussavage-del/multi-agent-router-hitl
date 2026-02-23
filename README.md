# multi-agent-router-hitl
*A human-in-the-loop routing layer that works with the Governance Gate (WHAT is allowed) to ensure every agent action is routed, approved, and auditable.*

---

## Purpose

`multi-agent-router-hitl` defines **WHO gets to act** in a multi-agent system by placing a controlled routing surface between:

- User intent  
- Candidate agent actions  
- Governance Gate decisions  
- Human final approval  

This router does **not** execute tasks.  
It **assigns** them—under supervision.

It ensures agents operate **within bounded authority** and that no model, tool, or subsystem acts without:

1. Classification  
2. Routing  
3. Validation  
4. Human-in-the-loop approval  

---

## The Role in the Quartet

| Repo | Function |
|------|----------|
| **llm-governance-gate** | *WHAT is allowed* |
| **multi-agent-router-hitl** | *WHO is permitted to act* |
| **drift-ledger-amendments** | *HOW changes are governed* |
| **governance-test-suite** | *Whether the whole system holds under pressure* |

This repository is **#2**.  
It assigns work, routes authority, and forces deliberation before action.

---

## Design Principles

- **Human Finality** — Routing is never automatic.  
- **Single Source of Authority** — All agent activity originates here.  
- **Schema-Driven Decisions** — Routing conforms to structured schemas.  
- **No Direct Agent-to-Agent Communication**.  
- **Auditable Trace** — All routing decisions are logged immutably.  
- **Minimal, Composable, Predictable** — No autonomous escalation.

---

## High-Level Architecture

User Input  
 ↓  
Intent Classifier (schema-bound)  
 ↓  
Governance Gate (WHAT is allowed?)  
 ↓  
Agent Router (WHO may act?)  
 ↓  
Human Approval (HITL)  
 ↓  
Selected Agent  
 ↓  
Execution Layer (outside this repo)

---

## Routing Flow

1. Input received  
2. Intent classified  
3. Governance Gate validation  
4. Candidate agent selected  
5. HITL approval checkpoint  
6. Route assignment to execution layer  

---

## Agent Model

```json
{
  "id": "agent_name",
  "capabilities": ["analysis", "retrieval", "generation"],
  "risk_profile": "low|medium|high",
  "authority_level": 1
}
