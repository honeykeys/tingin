import streamlit as st
from app.theme import COLORS
from nursingfloor.floor import NursingFloor
from nursingfloor.handoff import score_handoff_tier1, GROUND_TRUTH_FACTS


def render_handoff_view(floor: NursingFloor):
    """The killer screen: three-panel handoff view."""
    snapshot = floor.get_floor_snapshot()
    handoff = snapshot.get("handoff")

    if not handoff:
        st.warning("No handoff recorded yet. Run through Shift 1 first.")
        return

    st.markdown(
        f'<h2 style="font-family:Fraunces,serif;text-align:center;color:{COLORS["text_primary"]}">'
        f'The Handoff Moment</h2>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<p style="text-align:center;color:{COLORS["text_secondary"]}">'
        f'What the outgoing nurse knew · What they encoded · What the incoming nurse sees</p>',
        unsafe_allow_html=True,
    )
    st.divider()

    col_left, col_mid, col_right = st.columns(3)

    # Compute lost facts
    handoff_body = handoff.get("body", "")
    _, _, missing_facts = score_handoff_tier1(handoff_body)
    missing_set = set(missing_facts)

    with col_left:
        st.markdown(
            f'<div style="font-family:Fraunces,serif;font-size:20px;color:{COLORS["text_primary"]};margin-bottom:12px">'
            f'End of Shift 1: Ground Truth</div>',
            unsafe_allow_html=True,
        )
        _render_ground_truth(snapshot, missing_set)

    with col_mid:
        st.markdown(
            f'<div style="font-family:Fraunces,serif;font-size:20px;color:{COLORS["text_primary"]};margin-bottom:12px">'
            f'Handoff Written</div>',
            unsafe_allow_html=True,
        )
        _render_handoff_body(handoff)

    with col_right:
        st.markdown(
            f'<div style="font-family:Fraunces,serif;font-size:20px;color:{COLORS["text_primary"]};margin-bottom:12px">'
            f'What Shift 2 Sees</div>',
            unsafe_allow_html=True,
        )
        _render_shift2_view(handoff, snapshot)

    st.divider()
    score, matched, missing = score_handoff_tier1(handoff_body)

    # Score summary header
    score_color = COLORS["signal_stable"] if score >= 0.7 else COLORS["signal_watch"]
    st.markdown(
        f'<div style="text-align:center;font-family:JetBrains Mono,monospace;font-size:14px;'
        f'color:{COLORS["text_secondary"]};margin-bottom:16px">'
        f'Handoff fidelity: <span style="color:{score_color};font-size:22px;font-family:Fraunces,serif">'
        f'{score:.0%}</span>'
        f' &nbsp;·&nbsp; {len(matched)} of {len(GROUND_TRUTH_FACTS)} facts preserved</div>',
        unsafe_allow_html=True,
    )

    # Weighted fact breakdown (Tier 2)
    _render_weighted_breakdown(handoff_body)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Continue to Shift 2 →", key="continue_shift2"):
        st.session_state["view"] = "floor"
        st.rerun()


def _render_weighted_breakdown(handoff_body: str):
    """Per-fact weighted breakdown table — Tier 2 view."""
    rows = sorted(GROUND_TRUTH_FACTS, key=lambda f: f.weight, reverse=True)

    st.markdown(
        f'<div style="font-family:Fraunces,serif;font-size:16px;color:{COLORS["text_secondary"]};'
        f'margin-bottom:8px">Fact breakdown (IASHR-weighted)</div>',
        unsafe_allow_html=True,
    )

    total_weight = sum(f.weight for f in rows)
    matched_weight = 0.0

    for fact in rows:
        matched = fact.matches(handoff_body)
        if matched:
            matched_weight += fact.weight

        glyph = "✓" if matched else "✗"
        glyph_color = COLORS["signal_stable"] if matched else COLORS["signal_lost"]
        row_bg = COLORS["bg_surface"] if matched else COLORS["bg_elevated"]
        desc_color = COLORS["text_primary"] if matched else COLORS["text_secondary"]

        # Weight dots (1 dot per weight point)
        dots = "●" * int(fact.weight) + "○" * (4 - int(fact.weight))

        st.markdown(
            f'<div style="display:flex;align-items:center;gap:12px;padding:6px 10px;'
            f'background:{row_bg};border-bottom:1px solid {COLORS["border_subtle"]};'
            f'font-family:JetBrains Mono,monospace;font-size:12px">'
            f'<span style="color:{glyph_color};font-size:14px;min-width:16px">{glyph}</span>'
            f'<span style="color:{desc_color};flex:1">{fact.description}</span>'
            f'<span style="color:{COLORS["accent_amethyst"]};letter-spacing:2px;min-width:60px">{dots}</span>'
            f'<span style="color:{COLORS["text_muted"]};min-width:50px;text-align:right">'
            f'w={fact.weight:.0f}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    weighted_score = matched_weight / total_weight if total_weight else 0
    ws_color = COLORS["signal_stable"] if weighted_score >= 0.7 else COLORS["signal_watch"]
    st.markdown(
        f'<div style="text-align:right;font-family:JetBrains Mono,monospace;font-size:12px;'
        f'color:{COLORS["text_secondary"]};margin-top:6px">'
        f'weighted score: <span style="color:{ws_color}">{weighted_score:.0%}</span>'
        f' ({matched_weight:.0f} / {total_weight:.0f} pts)</div>',
        unsafe_allow_html=True,
    )


def _render_ground_truth(snapshot: dict, missing_set: set):
    shift_states = snapshot["shift_states"]
    patients = {p["identification"]["patient_id"]: p for p in snapshot["patients"]}

    for pid in ["P1", "P2", "P3"]:
        ident = patients[pid]["identification"]
        state = shift_states[pid]
        name = ident["name"]
        news2 = state["news2"]
        ambient_obs = state.get("ambient_observations", [])

        # Check if any high-weight fact for this patient is missing
        patient_facts_missing = [f for f in missing_set if pid.lower() in f.lower() or
                                  ident["name"].split()[-1].lower() in f.lower()]
        has_missing = bool(patient_facts_missing)

        card_bg = COLORS["bg_elevated"]
        border_color = COLORS["signal_lost"] if has_missing else COLORS["border_subtle"]

        st.markdown(
            f'<div style="border:1px solid {border_color};border-radius:4px;padding:12px;'
            f'background:{card_bg};margin-bottom:8px;">',
            unsafe_allow_html=True,
        )
        st.markdown(f"**{name}** (Bed {ident['bed']}) — NEWS2 {news2}")
        cv = state.get("current_vitals")
        if cv:
            st.markdown(f'<div style="font-size:11px;color:{COLORS["text_secondary"]}">HR {cv.get("hr")} RR {cv.get("rr")} SpO2 {cv.get("o2_sat")} BP {cv.get("sbp")}</div>', unsafe_allow_html=True)

        if ambient_obs:
            for obs in ambient_obs:
                st.markdown(
                    f'<div style="background:{COLORS["bg_deep"]};border-left:3px solid {COLORS["accent_rose"]};'
                    f'padding:8px;margin:6px 0;font-style:italic;font-size:13px">{obs["text"]}</div>',
                    unsafe_allow_html=True,
                )
        elif pid == "P2":
            # P2 has no ambient obs — this is Run B's loss
            st.markdown(
                f'<div class="signal-lost-highlight">⚠ No bedside observation recorded</div>',
                unsafe_allow_html=True,
            )

        for fact_desc in patient_facts_missing:
            st.markdown(
                f'<div style="background:{COLORS["signal_lost"]};color:{COLORS["text_primary"]};'
                f'font-size:11px;padding:3px 8px;border-radius:2px;margin:3px 0">✗ {fact_desc}</div>',
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)


def _render_handoff_body(handoff: dict):
    body = handoff.get("body", "")
    ts = handoff.get("timestamp", "")
    nurse = handoff.get("encoding_nurse_id", "RN1")

    st.markdown(
        f'<div style="background:{COLORS["bg_surface"]};border:1px solid {COLORS["border_subtle"]};'
        f'border-radius:4px;padding:16px;white-space:pre-wrap;font-family:Newsreader,serif;'
        f'font-size:15px;line-height:1.6;min-height:300px">{body}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div style="font-size:11px;color:{COLORS["text_secondary"]};margin-top:8px">'
        f'{ts} · {nurse}</div>',
        unsafe_allow_html=True,
    )


def _render_shift2_view(handoff: dict, snapshot: dict):
    body = handoff.get("body", "")
    st.markdown(
        f'<div style="background:{COLORS["bg_elevated"]};border:1px solid {COLORS["border_subtle"]};'
        f'border-radius:4px;padding:16px;white-space:pre-wrap;font-family:Newsreader,serif;'
        f'font-size:15px;line-height:1.6;color:{COLORS["text_secondary"]};min-height:300px">'
        f'{body}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div style="font-size:12px;color:{COLORS["text_muted"]};margin-top:8px">'
        f'+ chart history (prior shift data not included)</div>',
        unsafe_allow_html=True,
    )
