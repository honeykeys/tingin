import json
from pathlib import Path
from typing import Optional

from nursingfloor.floor import NursingFloor
from nursingfloor.scripts import run_a_script, run_b_script


MOCKS_DIR = Path(__file__).parent / "mocks"


def load_mock(filename: str) -> dict:
    return json.loads((MOCKS_DIR / filename).read_text())


def run_scripted(run_id: str) -> dict:
    """Execute a scripted run and return the full event log + final snapshot.
    run_id: 'run_a' | 'run_b'
    """
    floor = NursingFloor(seed=42)
    if run_id == "run_a":
        run_a_script(floor)
    else:
        run_b_script(floor)
    return {
        "floor": floor,
        "events": floor.events,
        "snapshot": floor.get_floor_snapshot(),
        "handoff": floor.handoff_record,
    }


def build_news2_trace(floor: NursingFloor) -> list:
    """Extract P2 NEWS2 over time from events."""
    trace = []
    for evt in floor.events:
        if hasattr(evt, "patient_id") and evt.patient_id == "P2" and hasattr(evt, "news2"):
            trace.append({"tick": evt.tick, "news2": evt.news2})
    return trace


def get_tool_call_feed(floor: NursingFloor) -> list:
    """Extract tool call rows for the timeline view."""
    from nursingfloor.events import (
        VitalsChecked, PatientObserved, MedAdministered,
        ObservationDocumented, HandoffWritten, HandoffRead
    )
    rows = []
    for evt in floor.events:
        if isinstance(evt, VitalsChecked):
            rows.append({"tick": evt.tick, "tool": "check_vitals", "patient": evt.patient_id, "reward": evt.reward_delta})
        elif isinstance(evt, PatientObserved):
            rows.append({"tick": evt.tick, "tool": "observe_patient", "patient": evt.patient_id, "reward": evt.reward_delta})
        elif isinstance(evt, MedAdministered):
            rows.append({"tick": evt.tick, "tool": "administer_medication", "patient": evt.patient_id, "reward": evt.reward_delta, "detail": f"{evt.drug} {evt.dose}"})
        elif isinstance(evt, ObservationDocumented):
            rows.append({"tick": evt.tick, "tool": "document_observation", "patient": evt.patient_id, "reward": evt.reward_delta})
        elif isinstance(evt, HandoffWritten):
            rows.append({"tick": evt.tick, "tool": "write_handoff", "patient": "—", "reward": evt.reward_delta, "detail": f"score={evt.score:.2f}"})
        elif isinstance(evt, HandoffRead):
            rows.append({"tick": evt.tick, "tool": "read_handoff", "patient": "—", "reward": 0.0})
    return rows
