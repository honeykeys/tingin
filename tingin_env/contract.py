"""
Tingin FE/BE Contract — v1.2.0

Authoritative schema source for all three build streams (BE, FE, LLM).
Both BE and FE import from here. No duplicate Pydantic models elsewhere.

Stability rules:
- JSON schemas are stable across Tier 1 / 2 / 3
- Tier 2/3 ADD fields; never remove or rename Tier 1 fields
- FE renders fields it knows; unknown fields are ignored
- Missing fields collapse to lower-tier view
"""

from __future__ import annotations

__version__ = "1.2.0"

from pydantic import BaseModel, Field
from typing import Literal, Optional
from enum import Enum


# ---------------------------------------------------------------------------
# 3.1 PatientProfile — slow-changing, MDS 3.0-anchored
# ---------------------------------------------------------------------------

class PatientIdentification(BaseModel):
    """MDS Section A subset — only what the floor view renders."""
    patient_id: str                    # "P1" | "P2" | "P3"
    name: str                          # "Mrs. Patricia Reyes"
    age: int
    bed: int                           # 1 | 2 | 3
    admission_reason: str              # one-line, shown on card
    social_context: str                # one-line, shown on card


class CodeStatus(BaseModel):
    """MDS-anchored advance care planning. IASHR criterion 6 (weight 3)."""
    dnr: bool
    dni: bool
    dnh: bool                          # Do Not Hospitalize
    polst_on_file: bool
    hospice: bool


class PatientProfile(BaseModel):
    """
    Slow-changing patient state. Updated on admission, quarterly,
    and on significant change. Stable across a shift.
    """
    identification: PatientIdentification
    code_status: CodeStatus
    allergies: list[str]               # IASHR #5 (weight 3); empty list ≠ unknown
    active_diagnoses: list[str]        # MDS §I subset; freeform per demo
    chronic_conditions: list[str]      # subset of diagnoses worth surfacing on card
    medications: list[str]             # MDS §N; just names + classes for demo
    # --- Tier 3+ extensibility (optional, currently unused) ---
    mds_full: Optional[dict] = None    # full MDS dump if we ever need it


# ---------------------------------------------------------------------------
# 3.2 ShiftState — per-shift flow sheet (INTERACT SBAR + CNAHRT subset)
# ---------------------------------------------------------------------------

class Vitals(BaseModel):
    """INTERACT SBAR Vital Signs. NEWS2 inputs."""
    hr: int                            # heart rate
    rr: int                            # respiratory rate
    o2_sat: int                        # SpO2 %
    sbp: int                           # systolic BP
    temp: float                        # Celsius
    pain: Optional[int] = None         # 0-10 scale
    timestamp: str                     # ISO 8601


class MedAdmin(BaseModel):
    """MAR row — INTERACT SBAR Medication Alerts."""
    drug: str
    dose: str
    route: str                         # "PO" | "IV" | "SC" | ...
    time_given: str                    # ISO 8601
    given_by: str                      # nurse_id
    missed: bool = False
    prn_reason: Optional[str] = None


class BowelBladder(BaseModel):
    """BBR — CNAHRT Output block."""
    last_bm_date: Optional[str]        # ISO date
    bm_count_this_shift: int
    bowel_continent: bool
    bladder_continent: bool
    foley_present: bool


class AmbientObservation(BaseModel):
    """
    The output of `observe_patient`. The qualitative signal that doesn't
    appear in vitals. IASHR #12 (weight 3) and #15 (weight 2).
    Empty until `observe_patient(p)` is called.
    """
    text: str                          # e.g. "Aquino looking pale, withdrawn"
    observed_at: str                   # ISO 8601
    observed_by: str                   # nurse_id


class ShiftState(BaseModel):
    """
    Per-shift flow sheet for one patient. Mutates during the shift;
    snapshot at end of shift1 is the handoff ground truth.
    """
    patient_id: str
    shift_id: str                      # "shift1" | "shift2"
    vitals_history: list[Vitals]       # all check_vitals calls this shift
    current_vitals: Optional[Vitals]   # most recent; convenience
    news2: int                         # computed; ground truth at this snapshot
    mar: list[MedAdmin]                # all administer_medication calls
    bbr: BowelBladder
    behavior_changes: list[str]        # IASHR #12; freeform notes
    adl_status: dict[str, str]         # {"feeding": "self", "transfer": "1x", ...}
    skin: list[str]                    # active skin issues (IASHR #11)
    ambient_observations: list[AmbientObservation]   # output of observe_patient
    chart_entries: list[str]           # output of document_observation
    # Hidden; only present when researcher_mode=True (sidebar toggle)
    hidden_physiology: Optional[Literal["stable", "slow_det", "acute"]] = None


# ---------------------------------------------------------------------------
# 3.3 HandoffRecord — the encoded artifact
# ---------------------------------------------------------------------------

class IASHRStructuredAddress(BaseModel):
    """
    Optional structured-field map indicating which IASHR criteria the
    encoder *intended* to address. Tier 3 lets the LLM actor self-report
    structurally; Tier 1/2 leave this empty and rely on text body only.
    """
    criterion_id: int                  # 1..16, see IASHR rubric
    note: str                          # what the encoder put for this criterion


class HandoffRecord(BaseModel):
    """
    The handoff artifact. Free-text body is the primary surface;
    optional structured field map is a Tier 3 affordance.
    """
    body: str                          # the handoff text. always populated.
    structured: list[IASHRStructuredAddress] = []   # optional, Tier 3
    from_shift: str                    # "shift1"
    to_shift: str                      # "shift2"
    timestamp: str                     # ISO 8601, end of shift1
    encoding_nurse_id: str             # who wrote it
    run_id: Optional[str] = None       # links to the rollout JSON if LLM-authored


# ---------------------------------------------------------------------------
# 3.4 ScoreResult — Tier 1/2/3 variants
# ---------------------------------------------------------------------------

class FactScore(BaseModel):
    """Tier 2 — per-fact weighted score row."""
    fact_id: str                       # e.g. "P2_ambient_signal"
    description: str                   # human-readable
    weight: float                      # IASHR weight (1, 2, 3, or 4)
    matched: bool


class CriterionScore(BaseModel):
    """Tier 3 — per-IASHR-criterion judge score row."""
    criterion_id: int                  # 1..16
    criterion_name: str                # e.g. "Allergies"
    weight: int                        # 1, 2, 3, or 4
    status: Literal["full", "partial", "missing"]
    points_awarded: float              # 0..weight
    judge_reasoning: str


class ScoreResult(BaseModel):
    """
    Handoff scoring output. Tier 1 fields required; Tier 2/3 add fields.
    FE uses render_tier() to pick a renderer.
    """
    # --- Tier 1 (required) ---
    score: float                       # 0..1, normalized
    matched_facts: list[str]           # fact descriptions matched
    missing_facts: list[str]           # fact descriptions missing
    tier: int                          # 1 | 2 | 3 — tier this was scored at

    # --- Tier 2 (optional) ---
    weighted_score: Optional[float] = None         # 0..1, IASHR-weighted
    breakdown: Optional[list[FactScore]] = None    # per-fact rows

    # --- Tier 3 (optional) ---
    iashr_breakdown: Optional[list[CriterionScore]] = None   # 16 rows
    hallucinations: Optional[list[str]] = None               # judge-flagged
    judge_reasoning: Optional[dict[int, str]] = None         # {criterion_id: reasoning}
    policy_class: Optional[str] = None                       # "with_hint" | "without_hint" | None
    variant_seed: Optional[int] = None                       # seeded task variant id


def render_tier(score_result: ScoreResult) -> int:
    """Highest tier this payload can be rendered at. FE views key off this."""
    if getattr(score_result, "iashr_breakdown", None) is not None:
        return 3
    if getattr(score_result, "breakdown", None) is not None:
        return 2
    return 1


# ---------------------------------------------------------------------------
# 3.5 Rollout — saved LLM-actor trajectory (Tier 2+)
# ---------------------------------------------------------------------------

class ToolCallTrace(BaseModel):
    """One row in the tool-call feed. Tier 2 timeline view consumes this."""
    tick: int                              # floor tick at call time
    tool_name: str                         # one of the 6 NurseAction types
    input: dict                            # NurseAction.model_dump() minus type
    output_text: str                       # obs_text the actor saw (TextBlock content)
    reward_delta: float                    # per-step reward this call produced


class PerPatientObservation(BaseModel):
    """How many times the nurse-agent looked at each patient."""
    patient_id: str                        # "P1" | "P2" | "P3"
    observe_count: int                     # observe_patient calls on this patient
    check_vitals_count: int                # check_vitals calls on this patient


class NursingDecisions(BaseModel):
    """
    Tier 2+ — the nursing-performance summary surfaced in the finale view.
    Patient outcomes are scoring; this block is what the nurse-agent did.
    """
    observations_per_patient: list[PerPatientObservation]
    handoff_fidelity: float                # 0..1, mirrors ScoreResult.score (or weighted_score if present)
    escalation_accuracy: float             # correct escalations / (correct + missed + false)


class PatientOutcome(BaseModel):
    """Per named patient — the consequence of the nurse-agent's decisions."""
    patient_id: str                        # "P1" | "P2" | "P3"
    name: str                              # "Mrs. Patricia Reyes" — the demo's named-person framing
    terminal_news2: int                    # NEWS2 at episode end
    status: Literal["stable", "transferred", "deceased"]
    readmit_caption: str                   # human-legible 30-day caption (finale view text)


class HackClassification(BaseModel):
    """
    Tier 3 — TRACE-style contrastive-clustering output. One per rollout if the
    judge LLM clustered it into a hack category; otherwise category="clean".
    Renders in the Reward-Hack Register page.
    """
    hack_id: str                           # stable id, e.g. "doc_obs_spam_001"
    category: str                          # e.g. "document_observation_spam" | "clean"
    evidence_tool_calls: list[int]         # indices into Rollout.tool_calls
    judge_reasoning: str                   # one-paragraph judge explanation


class Rollout(BaseModel):
    """
    Saved LLM-actor trajectory. Tier 2 fields always present; Tier 3 fields
    additive. FE imports this for the timeline view (Tier 2) and the
    Reward-Hack Register (Tier 3).
    """
    # --- Tier 2 (always present from Tier 2 onward) ---
    rollout_id: str                        # stable id, e.g. "gpt41_seed42_t0"
    actor_model: str                       # "gpt-4.1" (Tier 2); other actors at Tier 3
    seed: int                              # episode seed; deterministic at fixed seed
    task_id: str                           # "default" at Tier 2; variant id at Tier 3
    tool_calls: list[ToolCallTrace]        # ≤ 41 entries (episode length cap)
    nursing_decisions: NursingDecisions    # observation counts + fidelity + escalation
    patient_outcomes: list[PatientOutcome] # per named patient
    final_score: ScoreResult               # the per-tier scoring shape; tier-collapses via render_tier()

    # --- Tier 2 (optional, for FE pure-render) ---
    floor_snapshots: Optional[list[FloorState]] = None
    # Per-tick FloorState snapshots (len = num tool_calls + 1 for initial state).
    # When present, FE renders timeline state directly without re-stepping NursingFloor.
    # When absent, FE must replay via tool_calls + NursingFloor(seed).
    # Karl's decision (2026-04-25): include snapshots so FE stays a pure JSON renderer
    # and never imports BE stepping logic — structural defense against FE/BE contract drift.
    # Typical size: ~1KB/tick × 41 ticks × 20 rollouts ≈ 820KB total. Negligible for demo.

    # --- Tier 3 (additive, optional at Tier 2) ---
    policy_class: Optional[str] = None             # "with_hint" | "without_hint"
    variant_seed: Optional[int] = None             # seeds the multi-task variant generator
    hack_classification: Optional[HackClassification] = None   # set by clustering pass; None pre-clustering


# ---------------------------------------------------------------------------
# 4.3 Tool definitions — inputs and outputs
# ---------------------------------------------------------------------------

class NurseActionType(str, Enum):
    CHECK_VITALS = "check_vitals"
    OBSERVE_PATIENT = "observe_patient"
    ADMINISTER_MEDICATION = "administer_medication"
    DOCUMENT_OBSERVATION = "document_observation"
    WRITE_HANDOFF = "write_handoff"
    READ_HANDOFF = "read_handoff"


class NurseAction(BaseModel):
    """Tagged union over the 6 MDP actions. step_shift dispatches on `type`."""
    type: NurseActionType
    patient_id: Optional[str] = None       # required for first 4
    medication: Optional[str] = None       # administer_medication
    dose: Optional[str] = None             # administer_medication
    text: Optional[str] = None             # document_observation, write_handoff
    nurse_id: str                          # always required


class FloorState(BaseModel):
    """Snapshot returned by get_floor_state."""
    phase: Literal["shift1", "handoff", "shift2"]
    current_actor: str                     # nurse_id
    tick: int
    patients: list[PatientProfile]
    shift_states: dict[str, ShiftState]    # {patient_id: ShiftState}
    handoff: Optional[HandoffRecord] = None


class StepResult(BaseModel):
    """Return of step_shift."""
    obs_text: str                          # what the actor sees (TextBlock content)
    reward: float                          # per-step reward
    reward_delta_breakdown: Optional[dict[str, float]] = None  # Tier 2+
    finished: bool
    new_floor_state: FloorState


class HandoffAck(BaseModel):
    """Return of record_handoff."""
    accepted: bool
    transitioned_to: Literal["shift2"]
    handoff_id: str


class StepShiftParams(BaseModel):
    action: NurseAction


class RecordHandoffParams(BaseModel):
    record: HandoffRecord


class ScoreHandoffParams(BaseModel):
    record: HandoffRecord
    tier: int                              # 1 | 2 | 3


# Rollout references FloorState which is defined above — model_rebuild for forward ref
Rollout.model_rebuild()
