
# Multi-Agent Router (HITL) — Specification

## 1. Overview
The Multi-Agent Router (HITL) is a modular orchestration layer that evaluates an incoming message, determines which agent should handle it, and performs deterministic routing with optional Human-In-The-Loop (HITL) escalation.  
It is lightweight, dependency-minimal, and designed for transparent routing rather than autonomous decision-making.

---

## 2. Core Responsibilities

### **Task Evaluation**
- Inspect the incoming request  
- Validate required fields  
- Determine available agents  

### **Routing Logic**
- Select a single agent or distribute across multiple agents  
- Enforce deterministic, testable routing rules  

### **HITL Escalation**
- Trigger human approval when conditions are met  
- Provide structured fallback behavior  

### **Execution Flow**
- Pass the message + metadata to the selected agent  
- Return the agent’s response  

---

## 3. Architecture

### 3.1 Components

#### **BaseAgent**
Defines the minimal interface all agents must implement:
- `name` (string identifier)
- `handle(message: str) -> str`

#### **Router**
Primary orchestration unit. Responsibilities include:
- Maintaining agent registry (`agents={name: instance}`)
- Evaluating HITL rules
- Routing messages deterministically
- Delegating execution to the selected agent

#### **HITL Rule**
A callable:
```
hitl_required: Callable[[str], bool]
```
If `True`, the system returns a HITL-gated result instead of executing the agent.

---

## 4. Routing Rules & Flow

### 4.1 Deterministic Routing
Routing must always produce the same result for the same:
- Input message  
- Agent registry  
- HITL rule  

### 4.2 Routing Algorithm (Simplified)
1. Receive message  
2. Check `hitl_required(message)`  
3. If HITL required → return `"HITL_REQUIRED"` or equivalent  
4. Otherwise:
   - Select default agent (or rule-based agent)
   - Call `agent.handle(message)`
   - Return agent response

### 4.3 Agent Selection
Current implementation:  
- Direct dictionary lookup  
- Provides clear, predictable mapping  

Future expansion (not implemented but allowed):
- Pattern-based selection  
- Multi-agent fan-out  
- Priority routing  

---

## 5. HITL Logic Specification

### 5.1 Purpose
Prevent automatic execution of messages requiring human approval.

### 5.2 Behavior
If `hitl_required(message)` returns `True`:
- Router must NOT execute any agent
- Router must return a structured HITL gate response

### 5.3 Requirements
- Must be externally visible (no hidden routing)
- Must be testable and deterministic
- Must be impossible to bypass without code modification

---

## 6. Error Handling & Safeguards

### 6.1 Missing Agent
If a referenced agent does not exist:
- Router must raise a clear exception  
- No fallback or silent failure allowed  

### 6.2 Invalid HITL Rule
If the HITL rule throws an error:
- Router must fail explicitly  
- No unsafe defaults or silent passing  

### 6.3 Agent Failure
If an agent raises an exception:
- The Router propagates the exception upward  
- No mutation of internal Router state  

---

## 7. Repository Structure

```
multi-agent-router-hitl/
│
├── docs/
│   └── spec.md
│
├── examples/
│   └── basic_flow.md
│
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   └── roles.py
│   │
│   └── router/
│       ├── __init__.py
│       └── hitl_router.py
│
└── tests/
    └── test_router.py
```

Each directory plays a clear role:
- **docs/** — specifications  
- **examples/** — runnable demonstrations  
- **src/** — implementation source  
- **tests/** — validation  

---

## 8. Basic Usage Example

```python
from src.router.hitl_router import Router
from src.agents.roles import BaseAgent

class WriterAgent(BaseAgent):
    name = "writer"
    def handle(self, message: str) -> str:
        return f"Writer received: {message}"

router = Router(
    agents={"writer": WriterAgent()},
    hitl_required=lambda msg: "human" in msg.lower(),
)

print(router.route("Draft this section."))
# → Writer received: Draft this section.

print(router.route("Draft this section — human approval needed."))
# → HITL_REQUIRED
```

---

This document defines the authoritative behavior of the HITL Router and ensures clarity, transparency, and testability across all layers of the system.
