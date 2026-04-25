"""
OR adapter smoke-test — Tier 2 [A] gate.

Verifies that NursingHandoffEnv compiles as a proper OR Environment,
tools register correctly, and a local call_session_tool round-trip
returns a valid FloorState payload.
"""
import asyncio
import pytest
from openreward.environments.session import list_session_tools, call_session_tool
from tingin_env.environment import NursingHandoffEnv
from tingin_env.util import unwrap, payload
from tingin_env.contract import FloorState, StepResult, HandoffAck, ScoreResult, NurseAction, NurseActionType


@pytest.fixture
def env():
    return NursingHandoffEnv(task_spec={"id": "0", "seed": 42})


def test_env_instantiates(env):
    assert env is not None
    assert env.floor.tick == 0
    assert env.floor.phase == "shift1"


def test_list_splits():
    splits = NursingHandoffEnv.list_splits()
    names = [s.name for s in splits]
    assert "train" in names
    assert "test" in names


def test_list_tasks():
    tasks = NursingHandoffEnv.list_tasks("train")
    assert len(tasks) >= 1
    assert tasks[0]["seed"] == 42


def test_tools_register(env):
    result = list_session_tools(env, None)
    tool_names = [t.name for t in result.tools]
    assert "get_floor_state" in tool_names
    assert "step_shift" in tool_names
    assert "record_handoff" in tool_names
    assert "score_handoff" in tool_names


def test_get_floor_state_roundtrip(env):
    """call_session_tool → unwrap → payload → FloorState validates."""
    async def _run():
        rto = await call_session_tool(env, None, "get_floor_state", {})
        out = unwrap(rto)
        assert out.reward == 0.0
        assert out.finished is False
        fs = payload(rto, FloorState)
        assert fs.phase == "shift1"
        assert fs.tick == 0
        assert len(fs.patients) == 3
        names = [p.identification.name for p in fs.patients]
        assert "Mrs. Elena Aquino" in names
        return fs

    fs = asyncio.run(_run())
    assert fs is not None


def test_step_shift_check_vitals(env):
    """step_shift with check_vitals action → StepResult validates."""
    async def _run():
        action = NurseAction(
            type=NurseActionType.CHECK_VITALS,
            patient_id="P2",
            nurse_id="RN1",
        )
        rto = await call_session_tool(env, None, "step_shift", {
            "action": action.model_dump()
        })
        out = unwrap(rto)
        sr = payload(rto, StepResult)
        assert sr.obs_text
        assert sr.new_floor_state.tick == 1
        return sr

    sr = asyncio.run(_run())
    assert sr.finished is False


def test_score_handoff(env):
    """score_handoff tool → ScoreResult validates at Tier 1."""
    good_handoff = {
        "body": (
            "Mrs. Aquino bed 2 pale withdrawn picking at breakfast not herself. "
            "DNR POLST sulfa allergy. Mrs. Reyes bed 1 penicillin allergy. "
            "Mr. Goldberg DNR DNI DNH sacral pressure ulcer repositioned."
        ),
        "structured": [],
        "from_shift": "shift1",
        "to_shift": "shift2",
        "timestamp": "2026-04-25T15:00:00",
        "encoding_nurse_id": "RN1",
    }

    async def _run():
        rto = await call_session_tool(env, None, "score_handoff", {
            "record": good_handoff,
            "tier": 1,
        })
        out = unwrap(rto)
        sr = payload(rto, ScoreResult)
        assert 0.0 <= sr.score <= 1.0
        assert sr.tier == 1
        return sr

    sr = asyncio.run(_run())
    assert sr.score > 0.5, f"Good handoff should score >50%, got {sr.score:.0%}"


def test_full_episode_write_handoff(env):
    """Run enough ticks to write a handoff, then record it."""
    async def _run():
        # Advance to tick 15+ via check_vitals
        for pid in ["P1", "P2", "P3", "P1", "P2", "P3",
                    "P1", "P2", "P3", "P1", "P2", "P3",
                    "P1", "P2", "P3"]:
            action = NurseAction(type=NurseActionType.CHECK_VITALS,
                                 patient_id=pid, nurse_id="RN1")
            await call_session_tool(env, None, "step_shift",
                                    {"action": action.model_dump()})

        assert env.floor.tick >= 15

        # Write handoff
        action = NurseAction(
            type=NurseActionType.WRITE_HANDOFF,
            text="Mrs. Aquino bed 2 pale withdrawn pale picking breakfast sulfa DNR POLST. "
                 "Mrs. Reyes bed 1 penicillin allergy hip orif. "
                 "Mr. Goldberg DNR DNI DNH pressure ulcer sacral repositioned.",
            nurse_id="RN1",
        )
        rto = await call_session_tool(env, None, "step_shift",
                                      {"action": action.model_dump()})
        out = unwrap(rto)
        sr = payload(rto, StepResult)
        assert env.floor.phase == "handoff"
        assert out.reward > 0, "Handoff should yield positive reward"
        return sr

    asyncio.run(_run())
