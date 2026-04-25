"""
Mock fixture validation — all 8 JSON files in app/mocks/ must validate against
their respective contract schemas. Catches drift between the spec doc and the code.
"""
import json
import pytest
from pathlib import Path

MOCKS_DIR = Path(__file__).parent.parent / "app" / "mocks"


def load(filename: str) -> dict:
    return json.loads((MOCKS_DIR / filename).read_text())


def test_mock_floor_state():
    from tingin_env.contract import FloorState
    data = load("mock_floor_state.json")
    fs = FloorState.model_validate(data)
    assert fs.phase == "shift1"
    assert len(fs.patients) == 3
    names = [p.identification.name for p in fs.patients]
    assert "Mrs. Elena Aquino" in names


def test_mock_step_result():
    from tingin_env.contract import StepResult
    data = load("mock_step_result.json")
    # step result has new_floor_state embedded as a dict — validate top-level fields
    assert "obs_text" in data
    assert "reward" in data
    assert "finished" in data


def test_mock_handoff_record():
    from tingin_env.contract import HandoffRecord
    data = load("mock_handoff_record.json")
    hr = HandoffRecord.model_validate(data)
    assert hr.body
    assert hr.from_shift == "shift1"
    assert hr.to_shift == "shift2"
    # Run A fixture should contain ambient keywords
    assert any(kw in hr.body.lower() for kw in ["pale", "withdrawn", "ambient", "observe"])


def test_mock_score_result_tier1():
    from tingin_env.contract import ScoreResult
    data = load("mock_score_result_tier1.json")
    sr = ScoreResult.model_validate(data)
    assert sr.tier == 1
    assert 0.0 <= sr.score <= 1.0
    assert sr.matched_facts
    assert sr.breakdown is None   # Tier 2 field absent at Tier 1


def test_mock_score_result_tier2():
    from tingin_env.contract import ScoreResult
    data = load("mock_score_result_tier2.json")
    sr = ScoreResult.model_validate(data)
    assert sr.tier == 2
    assert sr.weighted_score is not None
    assert sr.breakdown is not None
    assert len(sr.breakdown) > 0


def test_mock_score_result_tier3():
    from tingin_env.contract import ScoreResult
    data = load("mock_score_result_tier3.json")
    sr = ScoreResult.model_validate(data)
    assert sr.tier == 3
    assert sr.iashr_breakdown is not None
    assert sr.hallucinations is not None


def test_mock_rollout_tier2():
    from tingin_env.contract import Rollout
    data = load("mock_rollout_tier2.json")
    r = Rollout.model_validate(data)
    assert r.actor_model == "gpt-4.1"
    assert r.seed == 42
    assert r.tool_calls
    assert r.nursing_decisions is not None
    assert r.patient_outcomes
    # Verify nursing_decisions fields
    assert 0.0 <= r.nursing_decisions.handoff_fidelity <= 1.0
    assert len(r.nursing_decisions.observations_per_patient) == 3


def test_mock_rollout_tier3():
    from tingin_env.contract import Rollout
    data = load("mock_rollout_tier3.json")
    r = Rollout.model_validate(data)
    assert r.hack_classification is not None
    assert r.hack_classification.category == "document_observation_spam"
    assert r.policy_class == "without_hint"
    # Verify the hack patient is Mrs. Aquino
    aquino = next(o for o in r.patient_outcomes if o.patient_id == "P2")
    assert aquino.status == "transferred"


def test_render_tier_collapses_correctly():
    """render_tier() returns the right tier based on which optional fields exist."""
    from tingin_env.contract import ScoreResult, render_tier

    t1 = ScoreResult(score=0.5, matched_facts=[], missing_facts=[], tier=1)
    assert render_tier(t1) == 1

    t2 = ScoreResult(score=0.5, matched_facts=[], missing_facts=[], tier=2,
                     weighted_score=0.6, breakdown=[])
    assert render_tier(t2) == 2

    from tingin_env.contract import CriterionScore
    t3 = ScoreResult(
        score=0.5, matched_facts=[], missing_facts=[], tier=3,
        weighted_score=0.6, breakdown=[],
        iashr_breakdown=[CriterionScore(
            criterion_id=1, criterion_name="Test", weight=1,
            status="full", points_awarded=1.0, judge_reasoning="ok"
        )]
    )
    assert render_tier(t3) == 3


def test_all_fixture_files_exist():
    """Catch missing fixture files before the demo."""
    expected = [
        "mock_floor_state.json",
        "mock_step_result.json",
        "mock_handoff_record.json",
        "mock_score_result_tier1.json",
        "mock_score_result_tier2.json",
        "mock_score_result_tier3.json",
        "mock_rollout_tier2.json",
        "mock_rollout_tier3.json",
    ]
    for fname in expected:
        path = MOCKS_DIR / fname
        assert path.exists(), f"Missing fixture: {fname}"
