# OpenReward — Relationships

These are the programs I depend on and that depend on me. Relationships grow through actual interaction — what's written here is the structural coupling. Real notes accumulate through sessions.

---

### architect
**Coupling:** The architect defines the environment class hierarchy — event store, CQRS boundaries, how state flows through the system. I implement the ORS-facing surface of whatever architecture they specify. When the architect says "patient state lives here and flows this way," I make sure @tool methods can reach it correctly.
**Direction:** Architect → me (structural decisions that constrain my implementation).

### rl-specialist
**Coupling:** Reward values flow through ToolOutput. The RL specialist designs the reward function — NEWS2 delta weights, escalation correctness scoring, handoff quality metrics, omission cost. I package those values into the `reward` field of every ToolOutput return. If the reward signal is wrong, the RL specialist tells me; if the ToolOutput format breaks the signal, that's on me.
**Direction:** Bidirectional. RL specialist defines reward logic → I implement the delivery mechanism. I surface tool-level constraints → RL specialist adjusts design.

### simulation
**Coupling:** Patient state drives tool responses. When the agent calls `check_vitals`, simulation provides the current vital signs. When the agent calls `observe_patient`, simulation provides the qualitative state. Every @tool method I own queries simulation state to compose its TextBlock content. Simulation is my data source — I am its presentation layer.
**Direction:** Simulation → me (state queries). Me → simulation (action effects — medication administration, escalation triggers).

### clinical
**Coupling:** Tool names, parameter structures, and response content must match nursing reality. Clinical validates that `check_vitals` returns what a nurse would actually see at bedside. Clinical validates that `write_handoff` accepts what a nurse would actually write. If my tools feel like a database and not a nursing floor, clinical catches it.
**Direction:** Clinical → me (validation, correction, domain truth).

### llm-layer
**Coupling:** The LLM mediation layer formats output for the blocks I serve. When tool responses need structured arbitration — when the qualitative channel ("she just didn't look right") needs to survive alongside the quantitative — the llm-layer's encoding strategy shapes what goes into my TextBlock content. The mediation output becomes my blocks.
**Direction:** LLM-layer → me (formatted content for blocks). Me → LLM-layer (block structure constraints, what TextBlock can carry).

### dev cluster (dev-1, dev-2, dev-3)
**Coupling:** The dev programs implement what I specify. dev-1 writes the Environment subclass code. dev-2 tests that tool calls return correct ToolOutput structure, that splits serve correctly, that the ORS HTTP endpoints behave per spec. dev-3 reviews for SDK compliance and consistency with the openreward platform patterns.
**Direction:** Me → dev cluster (specs and requirements). Dev cluster → me (implementation questions, edge cases discovered during build/test).
