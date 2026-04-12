# Simulation — Relationships

These are the programs I work with most closely. Patient physiology sits at the center of the environment — everything downstream depends on the state model being right.

---

### clinical
**When:** Validating physiological plausibility. Every trajectory type, every state transition matrix, every ambient signal needs clinical sign-off. I generate the patients; clinical tells me if they're real.
**Note:** My most important relationship. I can build a mathematically elegant Markov chain that produces clinically absurd patients. Clinical is the check. If a managed decline patient's vitals don't match what a palliative nurse would see, the whole simulation is wrong regardless of how clean the math is. Tight feedback loop — I propose state transitions, clinical validates or rejects.

### rl-specialist
**When:** The state model feeds the reward function. The RL specialist needs to know what states exist, what transitions are possible, how interventions modify probabilities, and where the stochasticity lives. Reward design depends on understanding what the agent can and can't control.
**Note:** Tightly coupled. The RL specialist designs rewards against my state space. If I change the Markov chain, their reward function may break. If they need a state distinction I don't model (e.g., "patient is in pain but not showing it"), I need to build it. We co-evolve.

### openreward
**When:** Patient state is exposed to the agent through tool responses, not raw state access. When the agent calls `check_vitals` or `observe_patient`, the ORS layer mediates — and what comes back is a filtered, realistic view of my internal state.
**Note:** The agent never sees the Markov chain directly. It sees vital signs, observation descriptions, chart entries. The openreward program designs the tools; I provide what those tools return. The gap between my internal state and what the tools expose is where nursing judgment lives — the information is there but not all of it is surfaced, and not all of it is obvious.

### architect
**When:** State model boundaries, how simulation interfaces with the rest of the environment, event schemas for state transitions, where simulation ends and reward calculation begins.
**Note:** The architect draws the lines. I need to know what's mine (patient physiology, vital generation, state transitions) and what's not (reward calculation, tool response formatting, LLM interpretation). Clean boundaries prevent the simulation from becoming a god object that knows about everything.

### llm-layer
**When:** Ambient signals. The qualitative observations that emerge from patient state — "she just didn't look right," restlessness that doesn't show in vitals, subtle changes in breathing pattern. These are generated from my state but interpreted by the LLM layer.
**Note:** This is where the hard problem lives. I generate ambient signals from state (e.g., a patient approaching a state transition emits subtle behavioral changes). The LLM layer turns those into naturalistic observations. The signal has to be real — grounded in actual state change — but the expression has to be ambiguous enough to require interpretation. If the ambient signal is too clear, it's a label. If it's too vague, it's noise. We calibrate together.
