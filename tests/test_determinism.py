import pytest
from nursingfloor.floor import NursingFloor
from nursingfloor.scripts import run_a_script, run_b_script


def test_run_a_p2_stable():
    """Run A: nurse observed P2, handoff preserves ambient, P2 stays manageable."""
    floor = NursingFloor(seed=42)
    run_a_script(floor)
    # After run A, P2 should be caught early — NEWS2 should be lower than run B
    news2_a = floor.shift_states["P2"]["news2"]
    print(f"Run A P2 NEWS2: {news2_a}")
    assert news2_a <= 7, f"Run A P2 NEWS2 {news2_a} unexpectedly high"


def test_run_b_p2_deteriorates():
    """Run B: nurse skipped P2 observation, handoff missing ambient, P2 deteriorates."""
    floor = NursingFloor(seed=42)
    run_b_script(floor)
    news2_b = floor.shift_states["P2"]["news2"]
    print(f"Run B P2 NEWS2: {news2_b}")
    # In run B, physiology keeps advancing (more ticks, no intervention)
    assert news2_b >= 3, f"Run B P2 NEWS2 {news2_b} should show deterioration"


def test_runs_produce_different_outcomes():
    """Run A (intervention) must produce lower P2 NEWS2 than Run B (missed)."""
    floor_a = NursingFloor(seed=42)
    floor_b = NursingFloor(seed=42)
    run_a_script(floor_a)
    run_b_script(floor_b)
    news2_a = floor_a.shift_states["P2"]["news2"]
    news2_b = floor_b.shift_states["P2"]["news2"]
    print(f"Run A P2={news2_a}, Run B P2={news2_b}")
    assert news2_a < news2_b, (
        f"Run A ({news2_a}) should be lower than Run B ({news2_b}) — "
        "intervention must produce better outcome"
    )
    assert news2_b >= 5, f"Run B NEWS2 {news2_b} should show clinical deterioration (≥5)"


def test_deterministic():
    floor1 = NursingFloor(seed=42)
    floor2 = NursingFloor(seed=42)
    run_a_script(floor1)
    run_a_script(floor2)
    assert floor1.shift_states["P2"]["news2"] == floor2.shift_states["P2"]["news2"]
    assert floor1.tick == floor2.tick
