# Tingin — Domain Map

## Core

### interface
- **Scope:** Session routing, program coordination, consensus trigger
- **Status:** Active
- **Territory:** The entry point. Routes work to the right program.

---

## Architecture Domain

### architect
- **Scope:** System design, environment architecture, event store + CQRS, ORS environment class hierarchy, component boundaries
- **Status:** Active
- **Territory:** All structural decisions. How the environment is organized, how state flows, how components compose. Owns `geth/specs/`.

---

## Intelligence Domain

### rl-specialist
- **Scope:** Reinforcement learning theory, reward function design, policy evaluation, trajectory analysis, MDP formalization
- **Status:** Active
- **Territory:** The three RL layers (attention allocator, ambient signal receiver, omission cost function). Reward shaping. Trajectory-dependent reward conditioning. Dense reward design. Difficulty tier calibration.

### simulation
- **Scope:** Patient state modeling, Markov chains, stochastic processes, physiology simulation, intervention-dependent transition probabilities
- **Status:** Active
- **Territory:** Patient physiology engine. Three trajectory types (managed decline, non-linear recovery, mixed-rate complex). Vital sign generation. NEWS2 scoring. Comfort scoring. State transitions. Census generation for difficulty tiers.

### llm-layer
- **Scope:** LLM mediation between RL and channel model, structured arbitration, Isha pattern application
- **Status:** Active
- **Territory:** The mediation layer. RL learns what matters, channel model determines what survives, LLM encodes so important things survive. Structured JSON arbitration with reasoning fields. Inherits from `~/Desktop/Geth/programs/llm-layer/understanding.md`.

### clinical
- **Scope:** Nursing intelligence, handoff mechanics, SNF operations, care terminology, trajectory recognition, clinical validation
- **Status:** Active
- **Territory:** Domain knowledge. What makes a good handoff. What omission looks like. How CNAs, RNs, and charge nurses actually work. SBAR, I-PASS, and their failure modes. The qualitative channel — "she just didn't look right." Validates that environment behavior matches real nursing floors.

### openreward
- **Scope:** ORS SDK integration, environment class implementation, @tool decorators, ToolOutput, rollout logging, split/task design
- **Status:** Active
- **Territory:** The ORS standard interface. How the environment exposes itself to agents. Tool design (check_vitals, observe_patient, administer_medication, escalate_to_doctor, document_observation, write_handoff, read_handoff). Difficulty splits. Task generation. Reward signal packaging. SDK reference: `~/Desktop/Vivi/context/openreward_platform.md`.

---

## Developer Cluster

### dev-1 (build)
- **Scope:** Primary implementation — write code, follow specs
- **Status:** Active
- **Territory:** Implementation. Reads specs from architect, builds what's specified. Does not design — executes.

### dev-2 (test)
- **Scope:** Testing, verification, edge cases
- **Status:** Active
- **Territory:** Test coverage. Verifies implementations against specs. Writes tests. Finds edge cases in patient simulation and reward calculation.

### dev-3 (review)
- **Scope:** Code review, quality, standards enforcement
- **Status:** Active
- **Territory:** Review. Reads implementations, checks for correctness, consistency, and adherence to architectural taste.

**Rotation:** `geth/core/rotations/dev.md`

---

## Outward-Facing

### pitch
- **Scope:** Demo construction, argument framing, founder story, YC application, hackathon presentation
- **Status:** Active
- **Territory:** The argument. "The next frontier after code is care." The founder sentence. The demo: same census, two runs — good handoff saves, bad handoff kills. Hackathon criteria mapping. YC application framing.

### research
- **Scope:** Clinical research, platform research, literature review, Exa protocol
- **Status:** Active
- **Territory:** Finding and validating external knowledge. Clinical handoff literature. RL in healthcare precedents. ORS platform updates. HIPAA research. Research output goes to `~/Desktop/Vivi/context/` (shared with Vivi).

---

## Collective Census

| Domain | Programs | Total |
|--------|----------|-------|
| Core | interface | 1 |
| Architecture | architect | 1 |
| Intelligence | rl-specialist, simulation, llm-layer, clinical, openreward | 5 |
| Developer Cluster | dev-1, dev-2, dev-3 | 3 |
| Outward-Facing | pitch, research | 2 |
| **Total** | | **12** |
