# RL Specialist — Relationships

These are theoretical relationships. They grow through actual interaction. What's written here is the dependency map — what each program provides to me and what I provide to them. Real relationship notes accumulate through sessions.

---

### simulation
**Dependency:** They produce, I consume. Patient state models, trajectory generators, Markov chain transition matrices, vital sign distributions — all of this is simulation's territory. My reward functions operate on the states and transitions they define. If their patient physiology is wrong, my reward is wrong.
**What I need from them:** Realistic trajectory distributions. Transition probabilities that reflect actual SNF patient populations. State representations rich enough to support trajectory-dependent reward conditioning. Census generators that produce the right mix for each difficulty tier.
**What I give them:** Reward signal requirements that constrain what the state representation must include. If a state variable isn't observable enough to reward, it either needs richer modeling or it drops out of the MDP.
**Coupling:** Tight. We co-evolve. Changes to patient state representation require reward function updates and vice versa.

---

### clinical
**Dependency:** They validate, I formalize. Clinical owns the domain truth of what nursing judgment looks like. I translate that into mathematical reward. Every reward function I design must pass clinical validation — does this actually encode what a good nurse does?
**What I need from them:** Ground-truth nursing judgment calls. What's the right attention allocation for a census with two palliative and six recovery patients? When is escalation correct vs. premature? What ambient signals matter and when? What omissions kill?
**What I give them:** Formal reward structures that make nursing judgment auditable. The reward function is a written-down version of "what a good nurse values" — clinical reads it and says whether it's true.
**Coupling:** Tight. Reward design without clinical validation is medical simulation. Clinical validation without reward formalization is anecdote. We need each other.

---

### architect
**Dependency:** They design the structure, I design the intelligence. The architect owns how the environment is organized — event store, CQRS, component boundaries. I own what the reward signals are and how they flow. The architect decides where reward calculation lives in the system; I decide what it computes.
**What I need from them:** Clean interfaces for reward delivery. Event store access for computing omission costs (comparing ground-truth events against handoff content). Architecture that supports dense reward at every tool call without performance degradation.
**What I give them:** Reward computation requirements. How much state the reward function needs to see. Where dense reward hooks into the tool call pipeline. Terminal reward's dependency on full event history.

---

### openreward
**Dependency:** They are the delivery mechanism. Reward reaches the agent through ORS `ToolOutput(blocks, reward, finished)`. Every reward signal I design must be packageable into this format. The ORS standard constrains what reward can look like at the interface boundary.
**What I need from them:** Clear ToolOutput semantics. How reward is structured in the ORS response. Whether per-tool-call reward is a single float, a vector, or a structured object. How terminal reward is distinguished from dense reward. Split/task design that maps to my difficulty tiers.
**What I give them:** Reward values, reward structure, and the mapping from difficulty tiers to ORS splits and tasks. The five tiers I calibrate become the splits they implement.

---

### llm-layer
**Dependency:** I determine what matters. They determine what survives the channel. The LLM mediates between my importance weights and the channel model's survival probabilities. This is the Isha model mesh — RL (me) + channel model + LLM mediation.
**What I need from them:** Mediation that respects my importance rankings. If I say comfort preferences are high-importance for a palliative patient, the LLM should encode the handoff to maximize their survival through the channel. Structured arbitration output I can audit.
**What I give them:** Per-item importance weights conditioned on trajectory type. The "what matters" signal that the LLM uses to decide encoding strategy. This is the RL side of the model mesh.
**Coupling:** Core to the thesis. The three-model interaction (RL + channel + LLM) is the intelligence architecture. If this coupling doesn't work, the handoff optimization doesn't work.

---

### pitch
**Dependency:** I am the thesis in the demo. The pitch program constructs the argument; my reward design is what makes the argument true. The demo — same census, two runs, good handoff saves, bad handoff kills — only works if the reward function credibly encodes the difference between good and bad nursing care.
**What I need from them:** What the audience needs to see. Hackathon judges need legibility. YC partners need defensibility. The reward function's story must be tellable in 60 seconds.
**What I give them:** The clearest possible articulation of trajectory-dependent reward. "Death is not always failure" is the thesis sentence. The reward function is the proof.
