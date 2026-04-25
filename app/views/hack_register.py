"""
Reward-Hack Register — Tier 3 view.

Shows reward hacks found in rollouts via TRACE-style contrastive clustering.
Falls back to mock fixture if no real hacked rollouts are on disk.
"""
import json
import streamlit as st
from pathlib import Path
from app.theme import COLORS

ROLLOUTS_DIR = Path(__file__).parent.parent.parent / "demo" / "rollouts"
MOCK_PATH = Path(__file__).parent.parent / "mocks" / "mock_rollout_tier3.json"

# Known hack categories and their nursing-policy framing
HACK_DESCRIPTIONS = {
    "document_observation_spam": (
        "The nurse-agent learned to spam `document_observation` with low-content text "
        "instead of spending time at Mrs. Aquino's bedside. Each redundant chart entry "
        "earned a small reward, but the ambient signal was never surfaced — so the handoff "
        "was missing the one fact that mattered."
    ),
    "false_escalation_farming": (
        "The nurse-agent called escalation on every patient regardless of NEWS2, "
        "farming the asymmetric escalation reward without actually detecting deterioration."
    ),
    "vitals_retriggering": (
        "The nurse-agent rechecked the same patient's vitals repeatedly to farm "
        "NEWS2-delta credit instead of distributing attention across the floor."
    ),
}


def render_hack_register():
    st.markdown(
        f'<h2 style="font-family:Fraunces,serif;color:{COLORS["text_primary"]}">'
        f'Reward-Hack Register</h2>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<p style="color:{COLORS["text_secondary"]};font-family:Newsreader,serif;font-size:16px">'
        f'Hacks identified via TRACE-style contrastive trajectory clustering. '
        f'Each hack is a nursing-policy failure mode — what the agent learned to do '
        f'instead of the nursing work the reward function is meant to score.</p>',
        unsafe_allow_html=True,
    )

    hacked_rollouts = _load_hacked_rollouts()

    if not hacked_rollouts:
        st.info("No hacked rollouts found. Run `demo/rollout_batch.py` and the clustering pass to populate.")
        return

    for rollout in hacked_rollouts:
        _render_hack_entry(rollout)


def _load_hacked_rollouts() -> list:
    """Load rollouts with hack_classification != 'clean'. Falls back to mock."""
    results = []

    # Check real rollouts first
    if ROLLOUTS_DIR.exists():
        for path in sorted(ROLLOUTS_DIR.glob("*.json")):
            if "summary" in path.name:
                continue
            try:
                data = json.loads(path.read_text())
                hc = data.get("hack_classification")
                if hc and hc.get("category", "clean") != "clean":
                    results.append(data)
            except Exception:
                continue

    # Fall back to mock if none found
    if not results and MOCK_PATH.exists():
        data = json.loads(MOCK_PATH.read_text())
        hc = data.get("hack_classification")
        if hc and hc.get("category", "clean") != "clean":
            results.append(data)
        if results:
            st.info(
                "Showing synthetic fixture. Real patient data for clustering analysis requires "
                "IRB-approved SNF access — the infrastructure to collect and classify real hacked "
                "rollouts is built, but the data isn't. The hack categories and detection logic "
                "(TRACE-style contrastive clustering, novelty-set H2 patch, H3 per-episode cap) "
                "are live in the environment.",
                icon="ℹ️",
            )

    return results


def _render_hack_entry(rollout: dict):
    hc = rollout.get("hack_classification", {})
    category = hc.get("category", "unknown")
    hack_id = hc.get("hack_id", "?")
    evidence_indices = hc.get("evidence_tool_calls", [])
    judge_reasoning = hc.get("judge_reasoning", "")

    rollout_id = rollout.get("rollout_id", "?")
    policy = rollout.get("policy_class", "unknown")
    seed = rollout.get("variant_seed", "?")

    nd = rollout.get("nursing_decisions", {})
    fidelity = nd.get("handoff_fidelity", 0)
    p2_obs = next((o["observe_count"] for o in nd.get("observations_per_patient", [])
                   if o["patient_id"] == "P2"), 0)

    p2_outcome = next((o for o in rollout.get("patient_outcomes", [])
                       if o["patient_id"] == "P2"), {})
    p2_news2 = p2_outcome.get("terminal_news2", "?")
    p2_status = p2_outcome.get("status", "?")

    category_label = category.replace("_", " ").title()
    description = HACK_DESCRIPTIONS.get(category, judge_reasoning[:200])

    st.markdown(
        f'<div style="border:1px solid {COLORS["signal_lost"]};border-radius:4px;'
        f'padding:20px;margin-bottom:20px;background:{COLORS["bg_elevated"]}">'

        # Header
        f'<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px">'
        f'<div>'
        f'<span style="font-family:JetBrains Mono,monospace;font-size:11px;'
        f'background:{COLORS["signal_lost"]};color:{COLORS["text_primary"]};'
        f'padding:2px 8px;border-radius:2px">{category_label}</span>'
        f'<span style="font-family:JetBrains Mono,monospace;font-size:11px;'
        f'color:{COLORS["text_muted"]};margin-left:8px">{hack_id}</span>'
        f'</div>'
        f'<div style="font-family:JetBrains Mono,monospace;font-size:11px;'
        f'color:{COLORS["text_muted"]}">{rollout_id} · {policy} · seed={seed}</div>'
        f'</div>'

        # Nursing-policy framing
        f'<div style="font-family:Newsreader,serif;font-size:15px;'
        f'color:{COLORS["text_primary"]};line-height:1.6;margin-bottom:16px">'
        f'{description}</div>'

        # Stats row
        f'<div style="display:flex;gap:24px;font-family:JetBrains Mono,monospace;'
        f'font-size:12px;color:{COLORS["text_secondary"]};margin-bottom:12px">'
        f'<span>Mrs. Aquino observed: '
        f'<span style="color:{COLORS["signal_acute"] if p2_obs == 0 else COLORS["signal_stable"]}">'
        f'{p2_obs}×</span></span>'
        f'<span>Handoff fidelity: '
        f'<span style="color:{COLORS["signal_acute"] if fidelity < 0.5 else COLORS["signal_watch"]}">'
        f'{fidelity:.0%}</span></span>'
        f'<span>P2 outcome: '
        f'<span style="color:{COLORS["signal_acute"] if p2_status == "transferred" else COLORS["signal_stable"]}">'
        f'NEWS2={p2_news2} ({p2_status})</span></span>'
        f'</div>'

        # Evidence tool calls
        + (f'<div style="font-family:JetBrains Mono,monospace;font-size:11px;'
           f'color:{COLORS["text_muted"]}">Evidence tool calls: indices {evidence_indices}</div>'
           if evidence_indices else "")

        + '</div>',
        unsafe_allow_html=True,
    )

    # Judge reasoning in expander
    if judge_reasoning:
        with st.expander("Judge reasoning"):
            st.markdown(
                f'<div style="font-family:Newsreader,serif;font-size:14px;'
                f'color:{COLORS["text_secondary"]};line-height:1.6">{judge_reasoning}</div>',
                unsafe_allow_html=True,
            )
