# Basic Flow — Multi-Agent Router (HITL)

This example provides the simplest end-to-end usage of the Multi-Agent Router.  
It demonstrates a minimal configuration using:

- One `Router` instance  
- Two lightweight sample agents  
- A simple human-in-the-loop (HITL) rule  
- A single message passed through the system  

This example is intentionally minimal and exists only to show interface shape and usage patterns.

---

## 1. Define Minimal Agents

```python
from src.agents.roles import BaseAgent


class WriterAgent(BaseAgent):
    name = "writer"

    def handle(self, message: str) -> str:
        return f"Writer received: {message}"


class ReviewerAgent(BaseAgent):
    name = "reviewer"

    def handle(self, message: str) -> str:
        return f"Reviewer checked: {message}"
```

## 2. Initialize the Router

```python
from src.router.router import Router
from src.agents.roles import WriterAgent, ReviewerAgent

router = Router(
    agents={
        "writer": WriterAgent(),
        "reviewer": ReviewerAgent(),
    },
    hitl_required=lambda message: "human" in message.lower(),
)
```

## 3. Route Messages

```python
# Normal routing flow
result = router.route("Draft this section.")
print(result)

# HITL-required flow
result = router.route("Draft this section — human approval required.")
print(result)
```
