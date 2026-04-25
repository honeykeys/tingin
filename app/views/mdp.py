import streamlit as st
from pathlib import Path
from app.theme import COLORS


def render_mdp_view():
    """Static rendering of spec/mdp.md."""
    st.markdown(
        f'<h2 style="font-family:Fraunces,serif;color:{COLORS["text_primary"]}">MDP Formalization</h2>',
        unsafe_allow_html=True,
    )

    mdp_path = Path("spec/mdp.md")
    if mdp_path.exists():
        content = mdp_path.read_text()
        # Strip the H1 since we already rendered it
        lines = content.split("\n")
        if lines and lines[0].startswith("# "):
            lines = lines[2:]  # skip H1 and blank line
        st.markdown("\n".join(lines))
    else:
        # Inline fallback if spec/mdp.md doesn't exist yet
        st.markdown("""
**State S**

Per patient p ∈ {P1, P2, P3}: vitals v_p (HR, RR, O2sat, SBP, Temp), hidden physiology state h_p ∈ {stable, slow_det, acute}, ambient signal a_p, medication record, chart entries, ground-truth NEWS2.

Floor-level: phase ∈ {shift1, handoff, shift2}, current_actor, timestep t, handoff report (nullable).

**Action A**

| Tool | Cost | Description |
|---|---|---|
| check_vitals(p) | 1 tick | Returns structured vitals obs |
| observe_patient(p) | 3 ticks | Surfaces ambient signal a_p |
| administer_medication(p, med, dose) | 1 tick | MAR entry + reward |
| document_observation(p, text) | 1 tick | Chart entry; +0.1 if novel |
| write_handoff(text) | 1 tick | End of shift1 only; q × 2.0 reward |
| read_handoff() | 1 tick | Shift2 only |

**Reward R**

| Event | Magnitude |
|---|---|
| First NEWS2 deterioration detection | +0.5 |
| Ambient signal captured (slow_det) | +0.5 |
| Correct medication | +0.2 |
| Novel observation documented | +0.1 |
| Handoff quality q × 2.0 | up to +2.0 |
| Stable patient terminal | +1.0 each |
| NEWS2 ≥ 7 terminal | −2.0 each |

**Episode Length:** T=20 shift1 · handoff (1 tick) · T=20 shift2 · ≤ 41 tool calls.

**Why this is RL:** Credit assignment depth across an agent boundary the agent doesn't control. The information bottleneck between shifts is the thesis — greedy-local cannot solve it.
        """)
