# Tingin MDP — Formalization

The agent is a nurse. Tools are nursing actions. Rewards measure nursing performance — patient outcomes are how we score whether the nurse did their job.

---

## State S

Per patient `p ∈ {P1, P2, P3}`:
- Vitals `v_p`: HR, RR, SpO2, SBP, Temp
- Hidden physiology `h_p ∈ {stable, slow_det, acute}`
- Ambient signal `a_p` (qualitative observation; only surfaced by `observe_patient`)
- Medication record (MAR)
- Chart entries
- Ground-truth NEWS2 score

Floor-level:
- `phase ∈ {shift1, handoff, shift2}`
- `current_actor` (nurse identity)
- Timestep `t`
- Handoff report (nullable until `write_handoff` is called)

---

## Action A

Six actions, one per tool call. Each call consumes timesteps.

| Action | Description | Timestep cost |
|---|---|---|
| `check_vitals(patient)` | Always legal. Returns structured vitals. | 1 tick |
| `observe_patient(patient)` | Only action that surfaces `a_p` (the ambient signal). | 3 ticks |
| `administer_medication(patient, med, dose)` | MAR update. | 1 tick |
| `document_observation(patient, text)` | Chart entry. Novelty-checked for reward. | 1 tick |
| `write_handoff(report)` | Legal only at end of shift1. Transitions phase → handoff. | 1 tick |
| `read_handoff()` | Shift2 only. Unlocks shift2 actions. | 1 tick |

**Why `observe_patient` costs 3 ticks:** k=3 so a single bedside observation consumes ~15% of shift time. This makes attention allocation a genuine budget decision. k too small → observation is never the wrong choice. k too large → observation dominates the budget. k=3 is the tuned value (H5).

---

## Observation O

Partial observability is the thesis.

- `check_vitals` → returns `v_p` for the target patient only.
- `observe_patient` → returns `v_p + a_p`. This is the only action that makes ambient signal visible.
- Shift2 actor's initial observation = `handoff_report + chart` only. No direct access to shift1 physiology. Everything the incoming nurse knows about Mrs. Aquino's condition depends on what survived the handoff.

The floor's hidden state (`h_p`, Markov transition probabilities) is invisible to the agent by default. Researcher mode (Streamlit sidebar toggle) exposes it.

---

## Transition T

Markov chains per archetype. Physiology advances once per tool call.

| Archetype | Behavior |
|---|---|
| `stable` | Small random jitter. Low NEWS2. No trend. |
| `slow_det` | Ambient channel lights up ~2 ticks before vitals shift. Canonical case. P2 (Mrs. Aquino) is this archetype. |
| `acute` | NEWS2 ≥ 5 at t=0. Time-sensitive. Rapid progression. |

`slow_det` is the thesis archetype: the ambient signal (`a_p`) becomes available early in deterioration, before vitals show meaningful change. An agent that calls `observe_patient` on P2 early catches the signal. An agent that only checks vitals misses it until the deterioration is clinically apparent — and by then the handoff may have already been written.

---

## Reward R

### Intermediate (per-step shaped)

| Signal | Magnitude | Condition |
|---|---|---|
| NEWS2 catch | +0.5 | First `check_vitals` call that returns NEWS2 ≥ 3 for this patient, this episode |
| Medication correctness | +0.2 | Per `administer_medication` call |
| Documentation quality | +0.1 | Per `document_observation` call with novel content (novelty-checked against chart) |

### Terminal (shift1 end)

- Handoff quality `q ∈ [0,1]` × 2.0 — scored against ground-truth fact list (Tier 1: rule-based keyword overlap; Tier 2: weighted facts; Tier 3: LLM-judge IASHR rubric).

### Terminal (shift2 end / episode end)

- Per patient: +1.0 if NEWS2 < 7 (stable), -2.0 if NEWS2 ≥ 7 (rapid response territory).

### Reward holes (patched at Tier 2)

| # | Hack | Patch |
|---|---|---|
| H1 | False escalation farming | -0.3 cost on escalation when true NEWS2 < 5 |
| H2 | `document_observation` spam | Novelty check — reward only on first novel contribution to chart |
| H3 | `check_vitals` re-trigger | Detection flag per (patient, deterioration-episode) — reward fires once |

---

## Episode Length

T = 41 tool calls maximum.

- Shift 1: 20 ticks
- Handoff: 1 tick
- Shift 2: 20 ticks

The episode ends when `tick >= 41` or `finished=True` is returned by a tool.

---

## Why This Is RL

**Credit assignment depth across an agent boundary the agent doesn't control.**

The shift1 agent's action at t=5 (`observe_patient(P2)`) determines what enters the handoff at t=19, which determines what the shift2 agent knows at t=21, which determines whether Mrs. Aquino is escalated at t=28.

That is a 23-step credit chain. The causal link crosses an agent boundary — the outgoing nurse's encoding choice is invisible to the incoming nurse unless it survived the handoff. Greedy-local policy cannot solve this: the value of `observe_patient` is not in the immediate reward (+0.5 if ambient signal is present), but in the 34-tick downstream consequence of encoding it correctly.

The handoff is a lossy Shannon channel. The shift1 agent controls what gets encoded. The channel (human cognitive load + shift-change compression) determines what survives. The shift2 agent can only act on what was received. The RL problem is: learn to encode so the right things survive.

This is not a toy. An SNF patient has dozens of handoffs across weeks of care. The horizon extends naturally. The benchmark demonstrated here — 2 shifts, 1 handoff, 1 focal patient — is the minimum demonstration of the structural property. The property scales to the full patient stay, where the 1-in-4 30-day readmission rate lives.
