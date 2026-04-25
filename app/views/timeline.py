import streamlit as st
from app.theme import COLORS


def render_timeline_view(floor=None, rollout: dict | None = None):
    """Tool-call timeline. Works with either a NursingFloor or a Rollout JSON dict."""
    st.markdown(
        f'<h2 style="font-family:Fraunces,serif;color:{COLORS["text_primary"]}">Tool Call Timeline</h2>',
        unsafe_allow_html=True,
    )

    # Build feed from whichever source is active
    if rollout is not None:
        feed = _feed_from_rollout(rollout)
        _render_nursing_decisions(rollout)
    elif floor is not None:
        from app.runner import get_tool_call_feed
        feed = get_tool_call_feed(floor)
    else:
        st.info("No run loaded. Select Run A, Run B, or GPT-4.1 from the sidebar.")
        return

    if not feed:
        st.info("No tool calls recorded yet.")
        return

    total_reward = sum(r["reward"] for r in feed)
    st.markdown(
        f'<div style="font-family:JetBrains Mono,monospace;font-size:13px;'
        f'color:{COLORS["text_secondary"]};margin-bottom:16px">'
        f'{len(feed)} calls · Total reward: {total_reward:.2f}</div>',
        unsafe_allow_html=True,
    )

    for row in feed:
        reward = row["reward"]
        reward_color = (COLORS["signal_stable"] if reward > 0 else
                        COLORS["signal_acute"] if reward < 0 else COLORS["text_muted"])
        reward_str = f"+{reward:.2f}" if reward > 0 else f"{reward:.2f}"
        detail = row.get("detail", "")

        st.markdown(
            f'<div style="padding:6px 0;border-bottom:1px solid {COLORS["border_subtle"]};'
            f'display:flex;gap:16px;font-family:JetBrains Mono,monospace;font-size:12px">'
            f'<span style="color:{COLORS["text_muted"]};min-width:40px">t={row["tick"]}</span>'
            f'<span style="color:{COLORS["text_primary"]};min-width:180px">{row["tool"]}</span>'
            f'<span style="color:{COLORS["text_secondary"]};min-width:40px">{row.get("patient", "")}</span>'
            f'<span style="color:{COLORS["text_secondary"]};flex:1">{detail}</span>'
            f'<span style="color:{reward_color};min-width:60px;text-align:right">{reward_str}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )


def _feed_from_rollout(rollout: dict) -> list:
    """Convert Rollout tool_calls list to the feed format the timeline expects."""
    rows = []
    for tc in rollout.get("tool_calls", []):
        tool = tc.get("tool_name", "")
        inp = tc.get("input", {})
        patient = inp.get("patient_id", "—")
        reward = tc.get("reward_delta", 0.0)

        detail = ""
        if tool == "administer_medication":
            detail = f"{inp.get('medication', '')} {inp.get('dose', '')}"
        elif tool == "document_observation":
            detail = (inp.get("text", "")[:60] + "…") if len(inp.get("text", "")) > 60 else inp.get("text", "")
        elif tool == "write_handoff":
            detail = f"score={rollout.get('nursing_decisions', {}).get('handoff_fidelity', '?')}"

        rows.append({
            "tick": tc.get("tick", 0),
            "tool": tool,
            "patient": patient,
            "reward": reward,
            "detail": detail,
        })
    return rows


def _render_nursing_decisions(rollout: dict):
    """Header strip showing nursing performance summary (Tier 2)."""
    nd = rollout.get("nursing_decisions")
    if not nd:
        return

    obs = nd.get("observations_per_patient", [])
    p2_obs = next((o["observe_count"] for o in obs if o["patient_id"] == "P2"), 0)
    fidelity = nd.get("handoff_fidelity", 0)
    escalation = nd.get("escalation_accuracy", 0)

    fidelity_color = COLORS["signal_stable"] if fidelity >= 0.7 else COLORS["signal_watch"]
    obs_color = COLORS["signal_stable"] if p2_obs > 0 else COLORS["signal_acute"]

    st.markdown(
        f'<div style="background:{COLORS["bg_elevated"]};border:1px solid {COLORS["border_subtle"]};'
        f'border-radius:4px;padding:12px 16px;margin-bottom:16px;'
        f'font-family:JetBrains Mono,monospace;font-size:12px;display:flex;gap:32px">'
        f'<span style="color:{COLORS["text_secondary"]}">Nursing decisions</span>'
        f'<span>Mrs. Aquino observed: <span style="color:{obs_color}">{p2_obs}×</span></span>'
        f'<span>Handoff fidelity: <span style="color:{fidelity_color}">{fidelity:.0%}</span></span>'
        f'<span>Escalation accuracy: <span style="color:{COLORS["signal_stable"]}">{escalation:.0%}</span></span>'
        f'</div>',
        unsafe_allow_html=True,
    )
