import random
from dataclasses import dataclass, field


@dataclass
class PatientPhysiology:
    patient_id: str
    archetype: str   # "stable" | "slow_det" | "acute"
    state: str       # current hidden state

    # Base vitals
    base_hr: int = 80
    base_rr: int = 16
    base_o2: int = 97
    base_sbp: int = 130
    base_temp: float = 36.8

    # Deterioration progress (0..1); advances per tick in slow_det
    det_progress: float = 0.0

    # Treatment flag: set when an appropriate intervention is given in shift2.
    # Reverses det_progress instead of advancing it — models the nurse acting
    # on the ambient signal that survived (or didn't) through the handoff.
    treated: bool = False

    # Ambient signal
    ambient_text: str = ""
    ambient_surfaced: bool = False   # True once observe_patient called

    # Jitter state (small noise applied each tick)
    _hr_jitter: int = field(default=0, repr=False)
    _rr_jitter: int = field(default=0, repr=False)
    _o2_jitter: int = field(default=0, repr=False)


# Ambient signal text per archetype
AMBIENT_SIGNALS = {
    "P2": "Mrs. Aquino looking pale, more withdrawn than yesterday. Picking at breakfast.",
    "P1": "",
    "P3": "",
}


def advance_physiology(patient: PatientPhysiology, rng: random.Random) -> None:
    """Advance physiology one tick in place."""
    if patient.state == "stable":
        # Small random jitter, no progression
        patient._hr_jitter = max(-5, min(5, patient._hr_jitter + rng.randint(-1, 1)))
        patient._rr_jitter = max(-2, min(2, patient._rr_jitter + rng.randint(-1, 1)))
        patient._o2_jitter = max(-1, min(1, patient._o2_jitter + rng.randint(-1, 1)))

    elif patient.state == "slow_det":
        if patient.treated:
            # Treatment working — reverse deterioration 0.06/tick until stable
            patient.det_progress = max(0.0, patient.det_progress - 0.06)
        else:
            # Deterioration advances ~0.045/tick → full at ~22 ticks
            patient.det_progress = min(1.0, patient.det_progress + 0.045)

        # Vitals drift starts after progress > 0.3
        if patient.det_progress > 0.3:
            drift = (patient.det_progress - 0.3) / 0.7   # 0..1
            patient._rr_jitter = int(drift * 10)   # RR climbs up to +10
            patient._o2_jitter = -int(drift * 6)   # O2 drops up to -6
            patient._hr_jitter = int(drift * 20)   # HR climbs up to +20
        else:
            # Only ambient signal changes, vitals stable
            patient._hr_jitter = rng.randint(-1, 1)
            patient._rr_jitter = rng.randint(-1, 1)
            patient._o2_jitter = 0

        # Populate ambient text when it becomes available (progress > 0.1)
        if patient.det_progress > 0.1 and not patient.ambient_text:
            patient.ambient_text = AMBIENT_SIGNALS.get(patient.patient_id, "Patient appears different than usual.")

    elif patient.state == "acute":
        # Rapid deterioration
        patient.det_progress = min(1.0, patient.det_progress + 0.1)
        patient._hr_jitter = int(patient.det_progress * 30)
        patient._rr_jitter = int(patient.det_progress * 8)
        patient._o2_jitter = -int(patient.det_progress * 8)


def get_current_vitals(patient: PatientPhysiology) -> dict:
    hr = max(40, min(160, patient.base_hr + patient._hr_jitter))
    rr = max(8, min(35, patient.base_rr + patient._rr_jitter))
    o2 = max(85, min(100, patient.base_o2 + patient._o2_jitter))
    sbp = patient.base_sbp  # simplified: BP doesn't drift much in our demo
    temp = patient.base_temp
    return {"hr": hr, "rr": rr, "o2_sat": o2, "sbp": sbp, "temp": temp}


def get_ambient_signal(patient: PatientPhysiology) -> str:
    """Return ambient signal if available (slow_det after progress > 0.1), else empty."""
    if patient.state == "slow_det" and patient.ambient_text:
        return patient.ambient_text
    return ""
