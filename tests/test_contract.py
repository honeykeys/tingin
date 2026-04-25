import pytest
from nursingfloor.floor import NursingFloor
from tingin_env.contract import FloorState, ScoreResult, __version__


def test_contract_version():
    assert __version__ == "1.2.0"


def test_floor_snapshot_validates():
    floor = NursingFloor(seed=42)
    snapshot = floor.get_floor_snapshot()
    fs = FloorState.model_validate(snapshot)
    assert fs.phase == "shift1"
    assert fs.tick == 0
    assert len(fs.patients) == 3


def test_patient_names():
    floor = NursingFloor(seed=42)
    snapshot = floor.get_floor_snapshot()
    fs = FloorState.model_validate(snapshot)
    names = [p.identification.name for p in fs.patients]
    assert "Mrs. Elena Aquino" in names
    assert "Mrs. Patricia Reyes" in names
    assert "Mr. Walter Goldberg" in names


def test_check_vitals_advances_tick():
    floor = NursingFloor(seed=42)
    floor.check_vitals("P2", "RN1")
    assert floor.tick == 1


def test_score_result_validates():
    result = ScoreResult(score=0.86, matched_facts=["P2 ambient"], missing_facts=[], tier=1)
    assert result.score == 0.86
    assert result.tier == 1
