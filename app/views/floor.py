import streamlit as st
from app.theme import COLORS, news2_color, kintsugi_css
from nursingfloor.floor import NursingFloor


PATIENT_ORDER = ["P1", "P2", "P3"]
FOCAL_PATIENT = "P2"


def render_floor_view(floor: NursingFloor, researcher_mode: bool = True):
    """Render the 3-patient floor view."""
    snapshot = floor.get_floor_snapshot()
    shift_states = snapshot["shift_states"]
    patients = {p["identification"]["patient_id"]: p for p in snapshot["patients"]}

    # Header bar
    col_h1, col_h2, col_h3 = st.columns([3, 3, 2])
    with col_h1:
        phase_label = {"shift1": "Shift 1", "handoff": "Handoff", "shift2": "Shift 2"}[snapshot["phase"]]
        st.markdown(f"**{phase_label}** &nbsp;·&nbsp; Actor: `{snapshot['current_actor']}` &nbsp;·&nbsp; `t = {snapshot['tick']} / 20`",
                    unsafe_allow_html=True)

    st.divider()

    # Left rail + patient cards
    left_col, cards_col = st.columns([1, 4])

    with left_col:
        st.markdown("**Tool calls**")
        feed = st.session_state.get("tool_call_feed", [])
        for row in feed[-15:]:  # last 15 calls
            reward_color = COLORS["signal_stable"] if row["reward"] > 0 else (
                COLORS["signal_acute"] if row["reward"] < 0 else COLORS["text_muted"])
            reward_str = f"+{row['reward']:.2f}" if row["reward"] > 0 else f"{row['reward']:.2f}"
            st.markdown(
                f'<div class="tool-call-row">'
                f'<span style="color:{COLORS["text_muted"]}">t={row["tick"]}</span> '
                f'<span style="color:{COLORS["text_primary"]}">{row["tool"]}</span> '
                f'<span style="color:{COLORS["text_secondary"]}">{row.get("patient","")}</span> '
                f'<span style="color:{reward_color}">{reward_str}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    with cards_col:
        cols = st.columns(3)
        for i, pid in enumerate(PATIENT_ORDER):
            with cols[i]:
                render_patient_card(pid, patients[pid], shift_states[pid], researcher_mode)


def render_patient_card(pid: str, profile: dict, state: dict, researcher_mode: bool):
    ident = profile["identification"]
    is_focal = pid == FOCAL_PATIENT
    card_border = COLORS["border_emphasis"] if is_focal else COLORS["border_subtle"]

    news2 = state["news2"]
    n2_color = news2_color(news2)

    # Card header
    focal_marker = " ◆" if is_focal else ""
    st.markdown(
        f'<div style="border:1px solid {card_border}; border-radius:4px; padding:16px; background:{COLORS["bg_surface"]};">'
        f'<div style="font-family:Fraunces,serif;font-size:20px;color:{COLORS["text_primary"]}">'
        f'{ident["name"]}{focal_marker}</div>'
        f'<div style="font-size:12px;color:{COLORS["text_secondary"]}">'
        f'Age {ident["age"]} · Bed {ident["bed"]} · {ident["admission_reason"]}</div>'
        f'<div style="font-size:12px;color:{COLORS["text_secondary"]};font-style:italic">'
        f'{ident["social_context"]}</div>',
        unsafe_allow_html=True,
    )

    # NEWS2 gauge
    st.markdown(
        f'<div class="news2-number" style="color:{n2_color};margin:12px 0 4px">{news2}</div>'
        f'<div style="font-size:11px;color:{COLORS["text_muted"]}">NEWS2</div>',
        unsafe_allow_html=True,
    )

    # Vitals strip
    cv = state.get("current_vitals")
    if cv:
        st.markdown(
            f'<div class="vitals-strip">'
            f'HR {cv.get("hr","—")} · RR {cv.get("rr","—")} · '
            f'SpO2 {cv.get("o2_sat","—")}% · BP {cv.get("sbp","—")} · '
            f'T {cv.get("temp","—")}°C'
            f'</div>',
            unsafe_allow_html=True,
        )

    # Ambient signal pane
    ambient_obs = state.get("ambient_observations", [])
    if ambient_obs:
        for obs in ambient_obs:
            st.markdown(
                f'<div class="ambient-text">{obs["text"]}</div>',
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            f'<div style="font-size:12px;color:{COLORS["text_muted"]};padding:8px;border:1px dashed {COLORS["border_subtle"]};border-radius:4px">no bedside observation yet</div>',
            unsafe_allow_html=True,
        )

    # Chart entries
    chart = state.get("chart_entries", [])
    if chart:
        st.markdown("**Chart**")
        for entry in chart[-3:]:
            st.markdown(f'<div class="chart-entry">{entry}</div>', unsafe_allow_html=True)

    # Researcher mode badge
    if researcher_mode:
        hp = state.get("hidden_physiology", "?")
        badge_color = {"stable": COLORS["signal_stable"], "slow_det": COLORS["signal_watch"],
                       "acute": COLORS["signal_acute"]}.get(hp, COLORS["text_muted"])
        st.markdown(
            f'<div style="margin-top:8px">'
            f'<span style="background:{badge_color};color:#000;font-size:10px;padding:2px 8px;border-radius:10px;font-family:JetBrains Mono,monospace">'
            f'{hp}</span></div>',
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)
