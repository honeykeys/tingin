from dataclasses import dataclass

@dataclass
class VitalsChecked:
    tick: int
    patient_id: str
    vitals: dict
    reward_delta: float

@dataclass
class PatientObserved:
    tick: int
    patient_id: str
    ambient_text: str
    reward_delta: float

@dataclass
class MedAdministered:
    tick: int
    patient_id: str
    drug: str
    dose: str
    reward_delta: float

@dataclass
class ObservationDocumented:
    tick: int
    patient_id: str
    text: str
    reward_delta: float

@dataclass
class HandoffWritten:
    tick: int
    body: str
    score: float
    reward_delta: float

@dataclass
class HandoffRead:
    tick: int
    nurse_id: str

@dataclass
class PhysiologyAdvanced:
    tick: int
    patient_id: str
    news2: int
    hidden_physiology: str
