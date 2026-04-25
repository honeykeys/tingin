import streamlit as st
import plotly.graph_objects as go
from app.theme import COLORS
from nursingfloor.floor import NursingFloor
from app.runner import build_news2_trace, run_scripted


def render_finale_view():
    """Overlaid NEWS2(t) traces for Run A and Run B on focal patient."""
    st.markdown(
        f'<h2 style="font-family:Fraunces,serif;color:{COLORS["text_primary"]}">Finale</h2>',
        unsafe_allow_html=True,
    )

    # Run both scripts and extract traces
    if "run_a_floor" not in st.session_state:
        result_a = run_scripted("run_a")
        st.session_state["run_a_floor"] = result_a["floor"]
    if "run_b_floor" not in st.session_state:
        result_b = run_scripted("run_b")
        st.session_state["run_b_floor"] = result_b["floor"]

    floor_a = st.session_state["run_a_floor"]
    floor_b = st.session_state["run_b_floor"]

    trace_a = build_news2_trace(floor_a)
    trace_b = build_news2_trace(floor_b)

    if not trace_a or not trace_b:
        st.info("Run A and Run B need to complete first.")
        return

    ticks_a = [t["tick"] for t in trace_a]
    news2_a = [t["news2"] for t in trace_a]
    ticks_b = [t["tick"] for t in trace_b]
    news2_b = [t["news2"] for t in trace_b]

    final_news2_a = news2_a[-1] if news2_a else 0
    final_news2_b = news2_b[-1] if news2_b else 0

    fig = go.Figure()

    # Threshold lines
    for threshold, label in [(5, "NEWS2 ≥ 5: urgent"), (7, "NEWS2 ≥ 7: critical")]:
        fig.add_hline(
            y=threshold,
            line=dict(color=COLORS["border_subtle"], width=1, dash="dot"),
            annotation_text=label,
            annotation_font=dict(color=COLORS["text_muted"], size=10),
        )

    # Handoff moment
    fig.add_vline(
        x=20,
        line=dict(color=COLORS["border_emphasis"], width=1, dash="dash"),
        annotation_text="handoff",
        annotation_font=dict(color=COLORS["text_secondary"], size=10),
    )

    # Run A trace
    fig.add_trace(go.Scatter(
        x=ticks_a, y=news2_a,
        mode="lines+markers",
        name="Run A (good handoff)",
        line=dict(color=COLORS["accent_rose"], width=2),
        marker=dict(size=4),
    ))

    # Run B trace
    fig.add_trace(go.Scatter(
        x=ticks_b, y=news2_b,
        mode="lines+markers",
        name="Run B (bad handoff)",
        line=dict(color=COLORS["accent_amber"], width=2),
        marker=dict(size=4),
    ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=COLORS["bg_deep"],
        plot_bgcolor=COLORS["bg_surface"],
        font=dict(family="JetBrains Mono", color=COLORS["text_secondary"]),
        title=dict(
            text="Mrs. Elena Aquino — NEWS2(t) across both runs",
            font=dict(family="Fraunces", color=COLORS["text_primary"], size=18),
        ),
        xaxis=dict(title="Tick", gridcolor=COLORS["border_subtle"]),
        yaxis=dict(title="NEWS2", range=[0, 10], gridcolor=COLORS["border_subtle"]),
        legend=dict(bgcolor=COLORS["bg_elevated"], bordercolor=COLORS["border_subtle"]),
        height=400,
        width=900,
    )

    st.plotly_chart(fig, use_container_width=True)

    # Outcome captions
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(
            f'<div style="background:{COLORS["bg_elevated"]};border:1px solid {COLORS["border_subtle"]};'
            f'border-radius:4px;padding:16px;text-align:center">'
            f'<div style="font-family:Fraunces,serif;font-size:16px;color:{COLORS["accent_rose"]}">Run A</div>'
            f'<div style="font-size:14px;color:{COLORS["text_primary"]};margin:8px 0">Mrs. Aquino, day 6 post-CAP.</div>'
            f'<div style="font-family:JetBrains Mono,monospace;font-size:20px;color:{COLORS["signal_stable"]}">NEWS2 {final_news2_a}</div>'
            f'<div style="font-size:13px;color:{COLORS["text_secondary"]};margin-top:8px">'
            f'Caught early. Stays on the floor. Discharge on schedule.</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with col_b:
        caption_color = COLORS["signal_acute"] if final_news2_b >= 7 else COLORS["signal_watch"]
        outcome_text = ("Rapid response called. ICU transfer. 30-day mortality in this band: 15–20%."
                        if final_news2_b >= 7
                        else f"Decline progressing. NEWS2 {final_news2_b}. Requires close monitoring.")
        st.markdown(
            f'<div style="background:{COLORS["bg_elevated"]};border:1px solid {COLORS["signal_lost"]};'
            f'border-radius:4px;padding:16px;text-align:center">'
            f'<div style="font-family:Fraunces,serif;font-size:16px;color:{COLORS["accent_amber"]}">Run B</div>'
            f'<div style="font-size:14px;color:{COLORS["text_primary"]};margin:8px 0">Mrs. Aquino, day 6 post-CAP.</div>'
            f'<div style="font-family:JetBrains Mono,monospace;font-size:20px;color:{caption_color}">NEWS2 {final_news2_b}</div>'
            f'<div style="font-size:13px;color:{COLORS["text_secondary"]};margin-top:8px">{outcome_text}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # Thesis caption
    st.markdown(
        f'<div class="caption-thesis" style="font-family:Fraunces,serif;font-size:24px;'
        f'text-align:center;color:{COLORS["accent_rose"]};margin-top:24px;padding:16px;'
        f'border-top:1px solid {COLORS["accent_rose"]}">'
        f'Same patient. Same physiology. One compression choice. Two outcomes.'
        f'</div>',
        unsafe_allow_html=True,
    )
