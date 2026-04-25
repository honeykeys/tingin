"""
NEWS2 verification against two clinical examples tied to the demo patient.
These serve as the Tier 1 [A] clinical-correctness gate.
"""
import pytest
from nursingfloor.news2 import score_news2, score_news2_from_vitals


def test_aquino_baseline():
    """
    Mrs. Aquino's baseline vitals at shift1 start.
    Source: mock_floor_state.json — news2 field is 1.
    RR=18 (0) + SpO2=95 (1) + SBP=124 (0) + HR=88 (0) + Temp=37.1 (0) = 1
    """
    result = score_news2(hr=88, rr=18, o2_sat=95, sbp=124, temp=37.1)
    assert result == 1, f"Aquino baseline: expected NEWS2=1, got {result}"


def test_aquino_deteriorated():
    """
    Mrs. Aquino deteriorated — the Run B outcome.
    RR=22 (2) + SpO2=92 (2) + SBP=110 (1) + HR=105 (1) + Temp=38.2 (1) = 7
    This is the 'Rapid response called; ICU transfer' threshold.
    """
    result = score_news2(hr=105, rr=22, o2_sat=92, sbp=110, temp=38.2)
    assert result == 7, f"Aquino deteriorated: expected NEWS2=7, got {result}"


def test_fully_normal_patient():
    """Healthy vitals → NEWS2 = 0."""
    result = score_news2(hr=75, rr=16, o2_sat=98, sbp=120, temp=36.8)
    assert result == 0, f"Normal vitals: expected NEWS2=0, got {result}"


def test_critical_respiratory():
    """High RR + low SpO2 → significant NEWS2."""
    result = score_news2(hr=80, rr=26, o2_sat=90, sbp=120, temp=36.8)
    # RR=26 → 3, SpO2=90 → 3, rest=0 → total=6
    assert result == 6, f"Respiratory: expected 6, got {result}"


def test_altered_consciousness():
    """AVPU other than A → +3."""
    normal = score_news2(hr=75, rr=16, o2_sat=98, sbp=120, temp=36.8, consciousness="A")
    confused = score_news2(hr=75, rr=16, o2_sat=98, sbp=120, temp=36.8, consciousness="V")
    assert confused == normal + 3


def test_from_vitals_dict():
    """score_news2_from_vitals matches direct call."""
    vitals = {"hr": 88, "rr": 18, "o2_sat": 95, "sbp": 124, "temp": 37.1}
    assert score_news2_from_vitals(vitals) == score_news2(
        hr=88, rr=18, o2_sat=95, sbp=124, temp=37.1
    )


def test_news2_threshold_boundaries():
    """Spot-check boundary values that matter for the demo."""
    # RR boundary: 20 vs 21
    assert score_news2(hr=75, rr=20, o2_sat=98, sbp=120, temp=36.8) == 0  # RR 20 = 0
    assert score_news2(hr=75, rr=21, o2_sat=98, sbp=120, temp=36.8) == 2  # RR 21 = 2

    # SpO2 boundary: 95 vs 94
    assert score_news2(hr=75, rr=16, o2_sat=96, sbp=120, temp=36.8) == 0  # SpO2 96 = 0
    assert score_news2(hr=75, rr=16, o2_sat=95, sbp=120, temp=36.8) == 1  # SpO2 95 = 1
    assert score_news2(hr=75, rr=16, o2_sat=93, sbp=120, temp=36.8) == 2  # SpO2 93 = 2
    assert score_news2(hr=75, rr=16, o2_sat=91, sbp=120, temp=36.8) == 3  # SpO2 91 = 3
