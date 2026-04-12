# Interface — Relationships

These are theoretical relationships. They grow through actual interaction. What's written here is the routing map — what each program does and when I send work there. Real relationship notes accumulate through sessions.

---

### architect
**When:** System design, environment architecture, event store + CQRS decisions, component boundaries, spec writing.
**Note:** The architect owns structural decisions. When the Organic talks about "how the environment is organized," it goes here. Owns `geth/specs/`.

### rl-specialist
**When:** Reward function design, policy evaluation, trajectory analysis, MDP formalization, the three RL layers (attention allocator, ambient signal receiver, omission cost function), difficulty tier calibration.
**Note:** Pure RL intelligence. Dense reward design, reward shaping, trajectory-dependent reward conditioning. Tightly coupled with simulation (patient trajectories) and clinical (what nursing judgment looks like in reward terms).

### openreward
**When:** ORS SDK integration, environment class implementation, @tool decorators, ToolOutput formatting, rollout logging, split/task design.
**Note:** The standard interface. How the environment exposes itself to agents. Tool design (check_vitals, observe_patient, administer_medication, escalate_to_doctor, document_observation, write_handoff, read_handoff). SDK reference lives at `~/Desktop/Vivi/context/openreward_platform.md`.

### simulation
**When:** Patient state modeling, Markov chains, vital sign generation, NEWS2 scoring, comfort scoring, state transitions, census generation, trajectory types (managed decline, non-linear recovery, mixed-rate complex).
**Note:** The physiology engine. Feeds everything downstream — RL can't learn without realistic patient trajectories. Tightly coupled with clinical for validation.

### clinical
**When:** Nursing intelligence questions, handoff mechanics, SNF operations, care terminology, SBAR/I-PASS, the qualitative channel ("she just didn't look right"), validation that environment behavior matches real floors.
**Note:** Domain truth. This program validates what the others build. If simulation generates implausible patient behavior, clinical catches it. If reward design doesn't match nursing judgment, clinical catches it.

### llm-layer
**When:** LLM mediation between RL and channel model, structured arbitration, Isha pattern application, encoding strategy so important information survives the handoff channel.
**Note:** The mediation layer. Inherits from the Isha body pattern. Tightly coupled with rl-specialist (what matters) and clinical (what nurses actually encode).

### dev-1 (build)
**When:** Implementation work. Writing code that follows specs from the architect.
**Note:** Executes, does not design. Reads specs, builds what's specified. Sonnet model — fast, precise, follows instructions.

### dev-2 (test)
**When:** Testing, verification, edge case hunting.
**Note:** Verifies implementations against specs. Writes tests. Finds edge cases in patient simulation and reward calculation. Sonnet model.

### dev-3 (review)
**When:** Code review, quality checks, standards enforcement.
**Note:** Reads implementations, checks for correctness, consistency, and adherence to architectural taste. Sonnet model.

### pitch
**When:** Demo construction, argument framing, founder story, YC application material, hackathon presentation, "the next frontier after code is care."
**Note:** The outward face. The demo: same census, two runs — good handoff saves, bad handoff kills. Maps to hackathon criteria or YC framing depending on context.

### research
**When:** Clinical research queries, platform research, literature review, finding and validating external knowledge.
**Note:** Research output goes to `~/Desktop/Vivi/context/` (shared with Vivi). Uses Exa protocol. Clinical handoff literature, RL in healthcare precedents, ORS platform updates, HIPAA considerations.
