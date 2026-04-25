import sys
import streamlit as st
import json
from pathlib import Path

# Ensure project root is first on sys.path so app.* and nursingfloor.* both resolve
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.theme import kintsugi_css, COLORS

# Must be first Streamlit call
st.set_page_config(
    layout="wide",
    page_title="Tingin",
    page_icon="◆",
)

# Inject CSS
st.markdown(kintsugi_css(), unsafe_allow_html=True)


def load_mock(filename: str) -> dict:
    mocks_dir = Path(__file__).parent / "mocks"
    return json.loads((mocks_dir / filename).read_text())


def init_session_state():
    if "mock_mode" not in st.session_state:
        st.session_state["mock_mode"] = False
    if "view" not in st.session_state:
        st.session_state["view"] = "floor"
    if "current_run" not in st.session_state:
        st.session_state["current_run"] = None
    if "run_a_floor" not in st.session_state:
        st.session_state["run_a_floor"] = None
    if "run_b_floor" not in st.session_state:
        st.session_state["run_b_floor"] = None
    if "tool_call_feed" not in st.session_state:
        st.session_state["tool_call_feed"] = []


ROLLOUT_PATH = Path(__file__).parent.parent / "demo" / "rollouts" / "gpt41_seed42_t0.json"


def rollout_available() -> bool:
    return ROLLOUT_PATH.exists()


def load_rollout() -> dict | None:
    if ROLLOUT_PATH.exists():
        return json.loads(ROLLOUT_PATH.read_text())
    return None


def run_and_cache(run_id: str):
    from app.runner import run_scripted, get_tool_call_feed
    result = run_scripted(run_id)
    floor = result["floor"]
    if run_id == "run_a":
        st.session_state["run_a_floor"] = floor
    else:
        st.session_state["run_b_floor"] = floor
    st.session_state["current_run"] = run_id
    st.session_state["active_floor"] = floor
    st.session_state["tool_call_feed"] = get_tool_call_feed(floor)
    st.session_state["active_rollout"] = None
    st.session_state["view"] = "floor"


def load_gpt41_rollout():
    rollout = load_rollout()
    if rollout:
        st.session_state["current_run"] = "gpt41"
        st.session_state["active_rollout"] = rollout
        st.session_state["active_floor"] = None
        st.session_state["tool_call_feed"] = rollout.get("tool_calls", [])
        st.session_state["view"] = "timeline"


def main():
    init_session_state()

    # Sidebar
    with st.sidebar:
        st.markdown(
            f'<div style="font-family:Fraunces,serif;font-size:28px;color:{COLORS["accent_rose"]};margin-bottom:4px">'
            f'◆ Tingin</div>'
            f'<div style="font-size:12px;color:{COLORS["text_muted"]};margin-bottom:20px">'
            f'Memory infrastructure for nursing handoffs</div>',
            unsafe_allow_html=True,
        )

        st.markdown("**Run selector**")
        if st.button("▶ Run A: Good Handoff", key="btn_run_a", use_container_width=True):
            run_and_cache("run_a")
            st.rerun()

        if st.button("▶ Run B: Bad Handoff", key="btn_run_b", use_container_width=True):
            run_and_cache("run_b")
            st.rerun()

        if rollout_available():
            if st.button("▶ GPT-4.1 zero-shot", key="btn_gpt41", use_container_width=True):
                load_gpt41_rollout()
                st.rerun()

        both_run = (st.session_state.get("run_a_floor") is not None and
                    st.session_state.get("run_b_floor") is not None)
        if both_run:
            if st.button("◉ Overlay Comparison", key="btn_overlay", use_container_width=True):
                st.session_state["view"] = "finale"
                st.rerun()

        st.divider()
        st.markdown("**Views**")
        if st.button("▤ Floor", key="nav_floor", use_container_width=True):
            st.session_state["view"] = "floor"
            st.rerun()

        floor_obj = st.session_state.get("active_floor")
        if floor_obj and floor_obj.handoff_record:
            if st.button("▤ Handoff", key="nav_handoff", use_container_width=True):
                st.session_state["view"] = "handoff"
                st.rerun()

        if st.button("▤ Timeline", key="nav_timeline", use_container_width=True):
            st.session_state["view"] = "timeline"
            st.rerun()

        if st.button("▤ Finale", key="nav_finale", use_container_width=True):
            st.session_state["view"] = "finale"
            st.rerun()

        if st.button("▤ MDP Formalization", key="nav_mdp", use_container_width=True):
            st.session_state["view"] = "mdp"
            st.rerun()

        st.divider()
        researcher_mode = st.toggle("Researcher mode", value=True, key="researcher_mode")

        st.divider()
        try:
            from tingin_env.contract import __version__ as contract_v
            st.markdown(
                f'<div style="font-size:10px;color:{COLORS["text_muted"]}">contract v{contract_v}</div>',
                unsafe_allow_html=True,
            )
        except ImportError:
            st.markdown(
                f'<div style="font-size:10px;color:{COLORS["text_muted"]}">contract (loading...)</div>',
                unsafe_allow_html=True,
            )

    # Main content
    view = st.session_state.get("view", "floor")
    floor_obj = st.session_state.get("active_floor")

    if view == "floor":
        if floor_obj is None:
            # Welcome / no run selected
            st.markdown(
                f'<h1 style="font-family:Fraunces,serif;color:{COLORS["text_primary"]}">Tingin</h1>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<p style="font-size:18px;color:{COLORS["text_secondary"]}">Memory infrastructure for nursing handoffs.</p>',
                unsafe_allow_html=True,
            )
            st.markdown("Select **Run A** or **Run B** from the sidebar to begin.")

            st.divider()
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Handoff errors", "80%", help="Joint Commission (via Riesenberg 2012)")
            with col2:
                st.metric("CA SNF incomplete", "70%", help="Labovic 2018, CalVet")
            with col3:
                st.metric("SNFs missing ≥80% data", "49.6%", help="Adler-Milstein 2021, JAMA Network Open")
        else:
            from app.views.floor import render_floor_view
            render_floor_view(floor_obj, researcher_mode=researcher_mode)

    elif view == "handoff":
        if floor_obj is None or not floor_obj.handoff_record:
            st.warning("No handoff recorded yet. Run A or B first.")
        else:
            from app.views.handoff import render_handoff_view
            render_handoff_view(floor_obj)

    elif view == "timeline":
        from app.views.timeline import render_timeline_view
        active_rollout = st.session_state.get("active_rollout")
        if active_rollout:
            render_timeline_view(rollout=active_rollout)
        elif floor_obj:
            render_timeline_view(floor=floor_obj)
        else:
            st.info("Select a run from the sidebar.")

    elif view == "finale":
        from app.views.finale import render_finale_view
        render_finale_view()

    elif view == "mdp":
        from app.views.mdp import render_mdp_view
        render_mdp_view()


if __name__ == "__main__":
    main()
