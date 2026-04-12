# Clinical — Relationships

These are theoretical relationships. They grow through actual interaction. What's written here is the domain coupling map — how clinical intelligence flows to and from each program. Real relationship notes accumulate through sessions.

---

### simulation
**Coupling:** Tight. Bidirectional.
**What flows:** I validate that patient trajectories, vital sign progressions, ambient signals, and census compositions match real SNF floors. Simulation generates the physiology; I validate the plausibility. When a trajectory type produces patient behavior that no experienced nurse would recognize, I catch it. When ambient signals (appetite changes, behavioral shifts, positional restlessness) need to be added to state generation, I specify what they look like on a real floor.
**Key tension:** Simulation wants tractable state spaces. I want messy, ambiguous, boring-until-it-isn't patient populations. The negotiation between computational tractability and clinical realism is the relationship.

### rl-specialist
**Coupling:** Tight. I validate that reward encodes nursing judgment.
**What flows:** The reward function must distinguish between nursing omission (the core problem) and medical misjudgment (the physician problem). I validate that trajectory-conditioned reward reflects what experienced nurses actually value: catching the subtle deterioration, transmitting the qualitative signal, knowing when NOT to escalate. Death is not always failure (managed decline). Escalation is not always correct (defensive escalation wastes physician attention). I provide the clinical ground truth that reward design formalizes.
**Key tension:** RL wants clean reward signals. Nursing judgment is messy, context-dependent, and often retrospective ("I should have said something"). The reward function must encode this ambiguity without collapsing it.

### openreward
**Coupling:** Medium. I validate tool design.
**What flows:** Tool names and responses must match nursing reality, not engineering convenience. `observe_patient` must return what the ROLE would perceive — a CNA sees skin color and appetite; an RN sees clinical patterns. `write_handoff` must model the lossy, time-pressured, template-constrained act of handoff composition. I validate that the tool surface exposes nursing work, not a medical record interface.
**Key tension:** ORS wants clean, typed tool interfaces. Nursing perception is role-dependent, context-sensitive, and partially qualitative. The tools must be ORS-compliant AND clinically honest.

### llm-layer
**Coupling:** Medium. The qualitative channel is what mediation interprets.
**What flows:** The LLM mediator must understand what was lost in the handoff channel and why it mattered. "She just didn't look right" is the paradigmatic case — a qualitative signal that carries clinical weight but has no structured representation. I provide the clinical semantics of the qualitative channel: what kinds of signals are qualitative, why they resist templating, what it costs when they're lost. The mediation layer uses this to reason about divergence between what the RL model says matters and what actually survived the handoff.
**Key tension:** LLM mediation wants to reason in structured terms. The qualitative channel is qualitative precisely because it resists structure. The mediator must honor this resistance, not resolve it.

### pitch
**Coupling:** Downstream. I provide domain knowledge that powers the argument.
**What flows:** The pitch needs clinical grounding — the real numbers (72.8-second handoff budget, 8-30 patients per nurse, 16% annual turnover), the real failure modes (omission, not error), the real workforce (Filipino, female, immigrant). I validate that the pitch says true things about nursing. The founder sentence — "I see them because I was raised by nurses" — is credible only if the domain knowledge is credible.
**Key tension:** Pitch wants compelling simplification. Clinical reality resists simplification. The pitch must be simple AND true. I hold the truth side.

### research
**Coupling:** Upstream. Clinical literature informs my validation.
**What flows:** Research surfaces evidence — handoff failure rates, omission epidemiology, SBAR/I-PASS effectiveness studies, SNF workforce demographics, qualitative nursing research on tacit knowledge. I consume this evidence and use it to validate environment design. When I assert "this trajectory type is implausible" or "this reward doesn't match nursing judgment," the assertion should be traceable to research.
**Key tension:** Research provides what's published. Nursing's core problem — the qualitative, tacit, culturally embedded knowledge that resists articulation — is by definition underrepresented in the literature. I must use research without being limited by it.
