"""
Slide deck view — 6 slides rendered within Streamlit.

Pitch arc: Hook → Thesis → Why (photo) → How (demo) → Results → What this becomes.
Navigation: prev/next at the bottom, slide indicator in sidebar.
"""
import streamlit as st
from pathlib import Path
from app.theme import COLORS

ASSETS_DIR = Path(__file__).parent.parent.parent / "assets"
SLIDE_COUNT = 6


def render_deck_view():
    if "slide" not in st.session_state:
        st.session_state["slide"] = 1

    slide = st.session_state["slide"]

    _render_slide(slide)
    _render_navigation(slide)


def _render_navigation(slide: int):
    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
    col_prev, col_indicator, col_next = st.columns([1, 3, 1])

    with col_prev:
        if slide > 1:
            if st.button("← prev", key="deck_prev", use_container_width=True):
                st.session_state["slide"] = slide - 1
                st.rerun()

    with col_indicator:
        dots = "  ".join(
            f'<span style="color:{COLORS["accent_rose"] if i == slide else COLORS["text_muted"]}">◆</span>'
            for i in range(1, SLIDE_COUNT + 1)
        )
        st.markdown(
            f'<div style="text-align:center;font-size:14px">{dots}</div>',
            unsafe_allow_html=True,
        )

    with col_next:
        if slide < SLIDE_COUNT:
            if st.button("next →", key="deck_next", use_container_width=True):
                st.session_state["slide"] = slide + 1
                st.rerun()


# ── Slide renderers ──────────────────────────────────────────────────────────

def _render_slide(slide: int):
    if slide == 1:
        _slide_title()
    elif slide == 2:
        _slide_problem()
    elif slide == 3:
        _slide_why()
    elif slide == 4:
        _slide_how()
    elif slide == 5:
        _slide_results()
    elif slide == 6:
        _slide_close()


def _slide_title():
    st.markdown("<div style='height:80px'></div>", unsafe_allow_html=True)

    # Diamond mark
    st.markdown(
        f'<div style="text-align:center;font-size:48px;color:{COLORS["accent_rose"]};'
        f'margin-bottom:24px">◆</div>',
        unsafe_allow_html=True,
    )

    # Wordmark
    st.markdown(
        f'<div style="text-align:center;font-family:Fraunces,serif;font-size:76px;'
        f'font-weight:700;color:{COLORS["text_primary"]};letter-spacing:-0.02em;'
        f'line-height:1">Tingin</div>',
        unsafe_allow_html=True,
    )

    # Tagline
    st.markdown(
        f'<div style="text-align:center;font-family:Newsreader,serif;font-size:24px;'
        f'color:{COLORS["text_secondary"]};margin-top:16px">'
        f'Memory infrastructure for nursing handoffs.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)

    # Spoken note
    st.markdown(
        f'<div style="text-align:center;font-family:Newsreader,serif;font-style:italic;'
        f'font-size:14px;color:{COLORS["text_muted"]}">'
        f'"Tingin. It\'s Filipino for <em>the way you see</em>. '
        f'We built memory infrastructure for nursing handoffs."</div>',
        unsafe_allow_html=True,
    )


def _slide_problem():
    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

    stats = [
        ("80%", "of serious medical errors involve handoff miscommunication.",
         "Joint Commission, via Riesenberg 2012"),
        ("70%", "of California skilled-nursing transfers leave with incomplete handoffs.",
         "Labovic 2018, CalVet 84-bed unit"),
        ("49.6%", "of US SNFs are missing 80%+ of the information needed for safe care of an arriving patient.",
         "Adler-Milstein 2021, JAMA Network Open, n=471 hospital-SNF pairs"),
    ]

    for number, text, citation in stats:
        col_num, col_text = st.columns([1, 3])
        with col_num:
            st.markdown(
                f'<div style="font-family:JetBrains Mono,monospace;font-size:76px;'
                f'font-weight:700;color:{COLORS["accent_rose"]};line-height:1;'
                f'text-align:right;padding-right:24px">{number}</div>',
                unsafe_allow_html=True,
            )
        with col_text:
            st.markdown(
                f'<div style="font-family:Newsreader,serif;font-size:22px;'
                f'color:{COLORS["text_primary"]};padding-top:16px">{text}</div>'
                f'<div style="font-family:Newsreader,serif;font-size:12px;'
                f'color:{COLORS["text_muted"]};font-style:italic;margin-top:4px">{citation}</div>',
                unsafe_allow_html=True,
            )
        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    st.divider()
    st.markdown(
        f'<div style="font-family:Newsreader,serif;font-size:20px;'
        f'color:{COLORS["text_secondary"]};font-style:italic">'
        f'The dominant error type isn\'t misjudgment. It\'s <strong style="color:{COLORS["text_primary"]}">omission</strong> — '
        f'what the outgoing nurse knew that didn\'t survive into the next shift.'
        f'</div>',
        unsafe_allow_html=True,
    )


def _slide_why():
    photo_path = ASSETS_DIR / "us.jpeg"

    col_photo, col_text = st.columns([2, 1])

    with col_photo:
        if photo_path.exists():
            st.image(str(photo_path), use_container_width=True)
        else:
            st.markdown(
                f'<div style="height:500px;background:{COLORS["bg_elevated"]};'
                f'border:1px solid {COLORS["border_subtle"]};border-radius:4px;'
                f'display:flex;align-items:center;justify-content:center;'
                f'color:{COLORS["text_muted"]};font-size:14px">photo: assets/us.jpeg</div>',
                unsafe_allow_html=True,
            )

    with col_text:
        st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
        st.markdown(
            f'<div style="font-family:Fraunces,serif;font-size:32px;'
            f'color:{COLORS["text_primary"]};line-height:1.2;margin-bottom:24px">'
            f'This is my mom.</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div style="font-family:Newsreader,serif;font-size:18px;'
            f'color:{COLORS["text_secondary"]};line-height:1.6">'
            f'She works the skilled nursing floor. '
            f'What survives the handoff and what doesn\'t is what she navigates every shift.'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
        st.markdown(
            f'<div style="font-family:Newsreader,serif;font-size:14px;'
            f'color:{COLORS["text_muted"]};font-style:italic;line-height:1.6">'
            f'"SF lacks the experience to see this clearly — it\'s profoundly human, '
            f'illegible from the outside, urgent for someone I love."'
            f'</div>',
            unsafe_allow_html=True,
        )


def _slide_how():
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown(
        f'<h2 style="font-family:Fraunces,serif;font-size:47px;'
        f'color:{COLORS["text_primary"]};line-height:1.2">How</h2>',
        unsafe_allow_html=True,
    )

    # Row 1 — MDP structure
    col_a, col_b, col_c = st.columns(3)
    for col, header, body in [
        (col_a, "The shift is the episode.", "~41 decisions. 3 patients. One nurse, 20 ticks."),
        (col_b, "The handoff is the compression event.", "One encoding. One channel. Everything lost is gone."),
        (col_c, "What the nurse encoded survives — or doesn't.", "The incoming nurse starts from the report alone."),
    ]:
        with col:
            st.markdown(
                f'<div style="background:{COLORS["bg_elevated"]};border:1px solid {COLORS["border_subtle"]};'
                f'border-radius:4px;padding:20px;height:150px">'
                f'<div style="font-family:Fraunces,serif;font-size:17px;'
                f'color:{COLORS["accent_rose"]};margin-bottom:10px">{header}</div>'
                f'<div style="font-family:Newsreader,serif;font-size:14px;'
                f'color:{COLORS["text_secondary"]}">{body}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # Row 2 — Hackathon criteria
    col_d, col_e, col_f = st.columns(3)
    criteria = [
        (col_d, "Long horizon.",
         "accent_amethyst",
         "The two-shift demo is the unit. Long-term SNF residents — like Mr. Goldberg — are in care for years, until end of life. Hundreds of handoffs. Thousands of decisions. The horizon compounds across the full residency."),
        (col_e, "Capability tangent.",
         "accent_amethyst",
         "What only emerges at scale: cross-shift memory — learning what to encode for an agent with zero prior context. Adaptation to non-stationarity — a patient changes day by day. Institutional knowledge that accumulates across shifts."),
        (col_f, "Hard but tractable.",
         "accent_amethyst",
         "Hard: the information bottleneck is irreversible once the handoff is written. You cannot undo a missed observation. Tractable: shaped reward guides toward correct nursing at every tick. Natural curriculum via census complexity."),
    ]
    for col, header, color_key, body in criteria:
        with col:
            st.markdown(
                f'<div style="background:{COLORS["bg_deep"]};border:1px solid {COLORS[color_key]}44;'
                f'border-radius:4px;padding:20px;height:160px">'
                f'<div style="font-family:Fraunces,serif;font-size:16px;'
                f'color:{COLORS[color_key]};margin-bottom:8px">{header}</div>'
                f'<div style="font-family:Newsreader,serif;font-size:13px;'
                f'color:{COLORS["text_muted"]};line-height:1.5">{body}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown(
        f'<div style="font-family:Newsreader,serif;font-size:16px;'
        f'color:{COLORS["text_muted"]};text-align:center;margin-bottom:16px">'
        f'↓ Run the demo live ↓</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("▶ Run A: Good Handoff", key="deck_run_a", use_container_width=True):
            from app.runner import run_scripted, get_tool_call_feed
            result = run_scripted("run_a")
            st.session_state["run_a_floor"] = result["floor"]
            st.session_state["active_floor"] = result["floor"]
            st.session_state["current_run"] = "run_a"
            st.session_state["tool_call_feed"] = get_tool_call_feed(result["floor"])
            st.session_state["view"] = "floor"
            st.rerun()
    with col2:
        if st.button("▶ Run B: Bad Handoff", key="deck_run_b", use_container_width=True):
            from app.runner import run_scripted, get_tool_call_feed
            result = run_scripted("run_b")
            st.session_state["run_b_floor"] = result["floor"]
            st.session_state["active_floor"] = result["floor"]
            st.session_state["current_run"] = "run_b"
            st.session_state["tool_call_feed"] = get_tool_call_feed(result["floor"])
            st.session_state["view"] = "floor"
            st.rerun()
    with col3:
        if st.button("▤ Handoff view", key="deck_handoff", use_container_width=True):
            st.session_state["view"] = "handoff"
            st.rerun()


def _slide_results():
    st.markdown(
        f'<h2 style="font-family:Fraunces,serif;font-size:47px;'
        f'color:{COLORS["text_primary"]}">Results</h2>',
        unsafe_allow_html=True,
    )

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(
            f'<div style="background:{COLORS["bg_elevated"]};border:1px solid {COLORS["border_subtle"]};'
            f'border-radius:4px;padding:24px;text-align:center">'
            f'<div style="font-family:Fraunces,serif;font-size:20px;color:{COLORS["accent_rose"]};margin-bottom:8px">Run A</div>'
            f'<div style="font-family:Newsreader,serif;font-size:16px;color:{COLORS["text_primary"]}">Mrs. Aquino, day 6 post-CAP.</div>'
            f'<div style="font-family:JetBrains Mono,monospace;font-size:32px;color:{COLORS["signal_stable"]};margin:12px 0">NEWS2 ≤ 3</div>'
            f'<div style="font-family:Newsreader,serif;font-size:14px;color:{COLORS["text_secondary"]}">Caught early. Stays on the floor.<br>Discharge on schedule.</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with col_b:
        st.markdown(
            f'<div style="background:{COLORS["bg_elevated"]};border:1px solid {COLORS["signal_lost"]};'
            f'border-radius:4px;padding:24px;text-align:center">'
            f'<div style="font-family:Fraunces,serif;font-size:20px;color:{COLORS["accent_amber"]};margin-bottom:8px">Run B</div>'
            f'<div style="font-family:Newsreader,serif;font-size:16px;color:{COLORS["text_primary"]}">Mrs. Aquino, day 6 post-CAP.</div>'
            f'<div style="font-family:JetBrains Mono,monospace;font-size:32px;color:{COLORS["signal_acute"]};margin:12px 0">NEWS2 ≥ 7</div>'
            f'<div style="font-family:Newsreader,serif;font-size:14px;color:{COLORS["text_secondary"]}">Rapid response called.<br>ICU transfer. 30-day mortality ~15–20%.</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    st.markdown(
        f'<div style="font-family:Fraunces,serif;font-size:28px;text-align:center;'
        f'color:{COLORS["accent_rose"]};padding:20px;'
        f'border-top:1px solid {COLORS["accent_rose"]};border-bottom:1px solid {COLORS["accent_rose"]}">'
        f'Same patient. Same physiology. One compression choice. Two outcomes.'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    if st.button("◉ Open overlay comparison", key="deck_finale", use_container_width=False):
        st.session_state["view"] = "finale"
        st.rerun()


def _slide_close():
    photo_path = ASSETS_DIR / "mom.jpeg"

    col_text, col_photo = st.columns([2, 1])

    with col_text:
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

        # Top beat — scaling argument
        st.markdown(
            f'<div style="font-family:Newsreader,serif;font-size:20px;'
            f'color:{COLORS["text_secondary"]};line-height:1.7;margin-bottom:24px">'
            f'<strong style="color:{COLORS["text_primary"]}">The shift is one link.</strong><br>'
            f'Long-term SNF residents don\'t leave in weeks — they stay for <em>years</em>, '
            f'until end of life or hospice. Mr. Goldberg is one of them. '
            f'Hundreds of handoffs. Thousands of decisions. Every one a compression event.<br><br>'
            f'The structure scales. The cost compounds. '
            f'<strong style="color:{COLORS["accent_rose"]}">1 in 4</strong> Medicare SNF patients '
            f'are readmitted within 30 days. Two-thirds preventable. '
            f'Two shifts is the minimum demonstration of a problem that runs for years.'
            f'</div>',
            unsafe_allow_html=True,
        )

        # Amber rule
        st.markdown(
            f'<div style="border-top:1px solid {COLORS["accent_amber"]};margin:24px 0"></div>',
            unsafe_allow_html=True,
        )

        # Bottom beat — the spine
        st.markdown(
            f'<div style="font-family:Fraunces,serif;font-size:24px;'
            f'color:{COLORS["text_primary"]};line-height:1.4;margin-bottom:16px">'
            f'What we ship is memory infrastructure for clinical work —<br>'
            f'so the nurse can be more human, not less.'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div style="font-family:Newsreader,serif;font-size:17px;'
            f'color:{COLORS["text_secondary"]};line-height:1.6">'
            f'SF builds AI to replace human work.<br>'
            f'Tingin builds AI to free humans for the human work that matters.'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

        # OR URL
        st.markdown(
            f'<div style="font-family:JetBrains Mono,monospace;font-size:13px;'
            f'color:{COLORS["accent_amethyst"]}">'
            f'openreward.ai/rkarlonuyda/tingin</div>',
            unsafe_allow_html=True,
        )

    with col_photo:
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        if photo_path.exists():
            st.image(str(photo_path), use_container_width=True)
        else:
            # Fallback: try mom2.jpeg
            alt = ASSETS_DIR / "mom2.jpeg"
            if alt.exists():
                st.image(str(alt), use_container_width=True)
