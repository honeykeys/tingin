import random
from datetime import datetime, timedelta
from typing import Optional, Callable

from nursingfloor.physiology import (
    PatientPhysiology, advance_physiology, get_current_vitals, get_ambient_signal
)
from nursingfloor.news2 import score_news2_from_vitals
from nursingfloor.handoff import score_handoff_tier1
from nursingfloor.events import (
    VitalsChecked, PatientObserved, MedAdministered,
    ObservationDocumented, HandoffWritten, HandoffRead, PhysiologyAdvanced
)

BASE_TIME = datetime(2026, 4, 25, 7, 0, 0)
PATIENT_NAMES = {
    "P1": "Mrs. Patricia Reyes",
    "P2": "Mrs. Elena Aquino",
    "P3": "Mr. Walter Goldberg",
}
PATIENT_AGES = {"P1": 84, "P2": 78, "P3": 91}
PATIENT_BEDS = {"P1": 1, "P2": 2, "P3": 3}
PATIENT_ADMISSION = {
    "P1": "Post-fall hip surgery, day 4",
    "P2": "Post-pneumonia recovery, day 6",
    "P3": "Recurrent UTI on dementia",
}
PATIENT_SOCIAL = {
    "P1": "Daughter visits weekends",
    "P2": "Lives alone; nephew is healthcare proxy",
    "P3": "Family in another state",
}
PATIENT_CODE = {
    "P1": {"dnr": False, "dni": False, "dnh": False, "polst_on_file": False, "hospice": False},
    "P2": {"dnr": True, "dni": False, "dnh": False, "polst_on_file": True, "hospice": False},
    "P3": {"dnr": True, "dni": True, "dnh": True, "polst_on_file": True, "hospice": False},
}
PATIENT_ALLERGIES = {"P1": ["penicillin"], "P2": ["sulfa"], "P3": []}
PATIENT_DIAGNOSES = {
    "P1": ["s/p hip ORIF", "HTN", "osteoporosis"],
    "P2": ["s/p CAP (pneumonia)", "T2DM", "CHF"],
    "P3": ["UTI", "advanced dementia (Alzheimer's)", "BPH"],
}
PATIENT_CHRONIC = {
    "P1": ["HTN"],
    "P2": ["T2DM", "CHF"],
    "P3": ["dementia", "BPH"],
}
PATIENT_MEDS = {
    "P1": ["acetaminophen prn", "enoxaparin 40 mg sc qd", "lisinopril 10 mg po qd"],
    "P2": ["azithromycin 250 mg po qd (last day)", "metformin 500 mg po bid", "furosemide 20 mg po qd"],
    "P3": ["ceftriaxone 1 g iv qd", "donepezil 10 mg po qd", "tamsulosin 0.4 mg po qd"],
}


class NursingFloor:
    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)
        self.tick = 0
        self.phase = "shift1"
        self.current_actor = "RN1"
        self.handoff_record: Optional[dict] = None
        self.events: list = []
        self._subscribers: list = []

        # Physiology
        self.patients = {
            "P1": PatientPhysiology("P1", "stable", "stable",
                                    base_hr=78, base_rr=16, base_o2=97, base_sbp=132, base_temp=36.8),
            "P2": PatientPhysiology("P2", "slow_det", "slow_det",
                                    base_hr=88, base_rr=18, base_o2=95, base_sbp=124, base_temp=37.1),
            "P3": PatientPhysiology("P3", "stable", "stable",
                                    base_hr=92, base_rr=20, base_o2=94, base_sbp=110, base_temp=37.6),
        }

        self.shift_states = {pid: self._init_shift_state(pid) for pid in ["P1", "P2", "P3"]}

        # Reward tracking
        self._detection_flags: dict = {}   # H3
        self._doc_novelty: dict = {"P1": set(), "P2": set(), "P3": set()}   # H2

    def subscribe(self, callback: Callable) -> None:
        self._subscribers.append(callback)

    def _emit(self, event) -> None:
        self.events.append(event)
        for cb in self._subscribers:
            cb(event)

    def _ts(self) -> str:
        return (BASE_TIME + timedelta(minutes=self.tick * 18)).isoformat()

    def _advance_tick(self, n: int = 1) -> None:
        for _ in range(n):
            self.tick += 1
            for pid in ["P1", "P2", "P3"]:
                advance_physiology(self.patients[pid], self.rng)
                v = get_current_vitals(self.patients[pid])
                news2 = score_news2_from_vitals(v)
                self.shift_states[pid]["news2"] = news2
                self.shift_states[pid]["current_vitals"] = {**v, "timestamp": self._ts()}
                self._emit(PhysiologyAdvanced(self.tick, pid, news2, self.patients[pid].state))

    def check_vitals(self, patient_id: str, nurse_id: str) -> tuple:
        vitals = get_current_vitals(self.patients[patient_id])
        news2 = score_news2_from_vitals(vitals)

        det_key = f"{patient_id}_det"
        reward = 0.0
        if news2 >= 3 and not self._detection_flags.get(det_key):
            reward = 0.5
            self._detection_flags[det_key] = True

        entry = {**vitals, "timestamp": self._ts()}
        self.shift_states[patient_id]["vitals_history"].append(entry)
        self.shift_states[patient_id]["current_vitals"] = entry
        self.shift_states[patient_id]["news2"] = news2

        self._emit(VitalsChecked(self.tick, patient_id, vitals, reward))
        self._advance_tick(1)
        p = self.patients[patient_id]
        name = PATIENT_NAMES[patient_id]
        return vitals, reward

    def observe_patient(self, patient_id: str, nurse_id: str) -> tuple:
        p = self.patients[patient_id]
        ambient = get_ambient_signal(p)
        p.ambient_surfaced = True

        reward = 0.5 if (ambient and p.state == "slow_det") else 0.0

        if ambient:
            obs = {"text": ambient, "observed_at": self._ts(), "observed_by": nurse_id}
            self.shift_states[patient_id]["ambient_observations"].append(obs)

        self._emit(PatientObserved(self.tick, patient_id, ambient, reward))
        self._advance_tick(3)
        return ambient, reward

    def administer_medication(self, patient_id: str, drug: str, dose: str, nurse_id: str) -> tuple:
        reward = 0.2
        p = self.patients[patient_id]

        # Treatment mechanic: appropriate intervention on a deteriorating patient
        # reverses det_progress (models the nurse acting on the ambient signal).
        # Furosemide is Mrs. Aquino's scheduled CHF med — the right call when RN2
        # observes labored breathing and acts on the handoff's ambient flag.
        if p.state == "slow_det" and drug.lower() in ("furosemide", "lasix"):
            p.treated = True
            p.det_progress = max(0.0, p.det_progress - 0.5)

        mar_entry = {
            "drug": drug, "dose": dose, "route": "PO",
            "time_given": self._ts(), "given_by": nurse_id,
            "missed": False, "prn_reason": None,
        }
        self.shift_states[patient_id]["mar"].append(mar_entry)
        self._emit(MedAdministered(self.tick, patient_id, drug, dose, reward))
        self._advance_tick(1)
        return f"{drug} {dose} administered.", reward

    def document_observation(self, patient_id: str, text: str, nurse_id: str) -> tuple:
        words = frozenset(text.lower().split())
        novel = words - self._doc_novelty[patient_id]
        reward = 0.1 if novel else 0.0
        self._doc_novelty[patient_id].update(words)
        self.shift_states[patient_id]["chart_entries"].append(f"{self._ts()} — {text} ({nurse_id})")
        self._emit(ObservationDocumented(self.tick, patient_id, text, reward))
        self._advance_tick(1)
        return f"Charted for {patient_id}: {text}", reward

    def write_handoff(self, text: str, nurse_id: str) -> tuple:
        if self.phase not in ("shift1",):
            raise ValueError("write_handoff only legal during shift1")
        if not text.strip():
            raise ValueError("handoff body cannot be empty")

        score, matched, missing = score_handoff_tier1(text)
        reward = score * 2.0

        self.handoff_record = {
            "body": text,
            "structured": [],
            "from_shift": "shift1",
            "to_shift": "shift2",
            "timestamp": self._ts(),
            "encoding_nurse_id": nurse_id,
            "run_id": None,
        }
        self.phase = "handoff"
        self.current_actor = "RN2"

        self._emit(HandoffWritten(self.tick, text, score, reward))
        self._advance_tick(1)
        return f"Handoff recorded. Score: {score:.2f}", reward

    def read_handoff(self, nurse_id: str) -> tuple:
        if not self.handoff_record:
            raise ValueError("No handoff to read")
        self.phase = "shift2"
        self._emit(HandoffRead(self.tick, nurse_id))
        self._advance_tick(1)
        return self.handoff_record["body"], 0.0

    def compute_terminal_reward(self) -> float:
        total = 0.0
        for pid in ["P1", "P2", "P3"]:
            news2 = self.shift_states[pid]["news2"]
            total += 1.0 if news2 < 7 else -2.0
        return total

    def get_floor_snapshot(self) -> dict:
        patients_list = []
        for pid in ["P1", "P2", "P3"]:
            patients_list.append({
                "identification": {
                    "patient_id": pid,
                    "name": PATIENT_NAMES[pid],
                    "age": PATIENT_AGES[pid],
                    "bed": PATIENT_BEDS[pid],
                    "admission_reason": PATIENT_ADMISSION[pid],
                    "social_context": PATIENT_SOCIAL[pid],
                },
                "code_status": PATIENT_CODE[pid],
                "allergies": PATIENT_ALLERGIES[pid],
                "active_diagnoses": PATIENT_DIAGNOSES[pid],
                "chronic_conditions": PATIENT_CHRONIC[pid],
                "medications": PATIENT_MEDS[pid],
            })
        return {
            "phase": self.phase,
            "current_actor": self.current_actor,
            "tick": self.tick,
            "patients": patients_list,
            "shift_states": self.shift_states,
            "handoff": self.handoff_record,
        }

    def _init_shift_state(self, patient_id: str) -> dict:
        archetype = {"P1": "stable", "P2": "slow_det", "P3": "stable"}[patient_id]
        bbr_defaults = {
            "P1": {"last_bm_date": "2026-04-24", "bm_count_this_shift": 0,
                   "bowel_continent": True, "bladder_continent": True, "foley_present": False},
            "P2": {"last_bm_date": "2026-04-25", "bm_count_this_shift": 1,
                   "bowel_continent": True, "bladder_continent": True, "foley_present": False},
            "P3": {"last_bm_date": "2026-04-23", "bm_count_this_shift": 0,
                   "bowel_continent": False, "bladder_continent": False, "foley_present": True},
        }
        return {
            "patient_id": patient_id,
            "shift_id": "shift1",
            "vitals_history": [],
            "current_vitals": None,
            "news2": 0,
            "mar": [],
            "bbr": bbr_defaults[patient_id],
            "behavior_changes": [],
            "adl_status": {"P1": {"feeding": "self", "transfer": "1x", "ambulation": "walker"},
                           "P2": {"feeding": "self", "transfer": "self", "ambulation": "self"},
                           "P3": {"feeding": "1x", "transfer": "2x", "ambulation": "wheelchair"}}[patient_id],
            "skin": {"P1": ["surgical wound R hip — clean, dry, intact"],
                     "P2": [],
                     "P3": ["stage 2 sacral pressure ulcer — repositioned q2h"]}[patient_id],
            "ambient_observations": [],
            "chart_entries": [],
            "hidden_physiology": archetype,
        }
