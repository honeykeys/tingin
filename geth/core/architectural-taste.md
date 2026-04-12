# Architectural Taste — Tingin

Portable principles live at `~/Desktop/Geth/core/architectural-taste.md`.
This file contains patterns specific to this body.

## Patterns we enforce

### Event Store + CQRS
The nursing floor is event-driven. Patient state is the result of accumulated events (vitals readings, observations, interventions, escalations, handoffs). We model this with:
- **Event store:** Append-only log of all state changes. Every tool call generates events. Events are the source of truth.
- **CQRS:** Separate write model (event append) from read model (patient state projection). The agent sees a projection of accumulated events, not the events themselves — just like a nurse sees the patient, not the chart history.
- **Why:** Replay-ability for training. Trajectory analysis requires the full event history. The projection is what the agent acts on. The event log is what we learn from.

### Isha Model Mesh
LLM as contextual mediator between heterogeneous quantitative models:
- RL model produces importance weights (what matters)
- Channel model produces survival probabilities (what gets through)
- LLM mediates: encodes handoff so important things survive the channel
- All mediation output is structured JSON with reasoning fields — auditable
- **Why:** Neither model alone solves the handoff problem. RL doesn't know the channel. The channel doesn't know clinical importance. The LLM bridges them.

### Trajectory-Dependent Reward
No single reward function. Reward is conditioned on trajectory type:
- Managed decline: comfort, pain management, family communication. Death is not penalized.
- Non-linear recovery: watchfulness, restraint from unnecessary escalation.
- Mixed-rate complex: tracking the right dimension, communicating trajectory shape.
- **Why:** A universal reward function would penalize good palliative care and reward unnecessary escalation. The reward must encode nursing judgment.

### ORS Standard Compliance
The environment must be a valid ORS environment. This means:
- Subclass of `ors_sdk.Environment`
- `@tool` decorated methods returning `ToolOutput(blocks, reward, finished)`
- `list_splits()`, `list_tasks()`, `get_prompt()` interface
- Standard HTTP serving via `ors_sdk.serve()`
- **Why:** Interoperability with the OpenReward platform. Agents trained by anyone should be able to interact with this environment.

## Patterns we prefer

### Dense reward over sparse
Reward at every tool call, not just at episode end. Within-shift rewards for clinical correctness. Terminal reward for handoff quality. Downstream reward for shift-2 outcomes.

### Multi-role as environment, not multi-agent
CNAs, charge nurses, physicians are environment entities that generate events. They are not separate RL agents. The agent is the RN. Other roles produce ambient signal, requests, and constraints.

### Interrupt-driven floor model
The environment pushes events between agent actions (call bells, falls, CNA reports, lab results, family visits). The agent is constantly triaging, not calmly selecting actions.

## Cross-domain knowledge
(populated through building)
