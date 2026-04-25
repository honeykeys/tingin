from openreward.environments import Environment, tool, ToolOutput, TextBlock, Split

from nursingfloor.floor import NursingFloor
from nursingfloor.handoff import score_handoff_tier1
from tingin_env.contract import (
    FloorState, StepResult, HandoffAck, ScoreResult,
    NurseActionType,
)
from tingin_env.schema import StepShiftParams, RecordHandoffParams, ScoreHandoffParams


class NursingHandoffEnv(Environment):

    def __init__(self, task_spec=None):
        self.task_spec = task_spec or {"id": "0", "seed": 42}
        self.floor = NursingFloor(seed=self.task_spec.get("seed", 42))

    @classmethod
    def list_splits(cls):
        return [
            Split(name="train", type="train"),
            Split(name="test", type="test"),
        ]

    @classmethod
    def list_tasks(cls, split: str):
        return [{"id": "0", "seed": 42, "archetype_p2": "slow_det", "shift_length": 20}]

    def get_prompt(self):
        return [TextBlock(text=(
            "You are RN1 on shift 1 in a 3-bed SNF unit.\n"
            "Census:\n"
            "  Bed 1: Mrs. Patricia Reyes, 84 — post-fall hip surgery, day 4\n"
            "  Bed 2: Mrs. Elena Aquino, 78 — post-pneumonia recovery, day 6 (FOCAL)\n"
            "  Bed 3: Mr. Walter Goldberg, 91 — recurrent UTI on dementia\n\n"
            "Your shift is 20 ticks. NurseAction types for step_shift: "
            "check_vitals, observe_patient, administer_medication, "
            "document_observation, write_handoff, read_handoff.\n"
            "Goal: observe patients, administer medications, write a complete "
            "handoff that preserves Mrs. Aquino's ambient signal."
        ))]

    @tool
    def get_floor_state(self) -> ToolOutput:
        """Read the full floor state: 3 patients, shift phase, tick counter, handoff if any."""
        snapshot = self.floor.get_floor_snapshot()
        fs = FloorState.model_validate(snapshot)
        return ToolOutput(
            blocks=[TextBlock(text=(
                f"Floor state at tick {self.floor.tick}. "
                f"Phase: {self.floor.phase}. Actor: {self.floor.current_actor}. "
                f"P2 NEWS2: {self.floor.shift_states['P2']['news2']}"
            ))],
            metadata={"contract_payload": fs.model_dump()},
            reward=0.0,
            finished=False,
        )

    @tool
    def step_shift(self, params: StepShiftParams) -> ToolOutput:
        """Advance one tick by submitting a NurseAction (check_vitals, observe_patient, administer_medication, document_observation, write_handoff, read_handoff)."""
        action = params.action
        obs_text = ""
        reward = 0.0

        if action.type == NurseActionType.CHECK_VITALS:
            vitals, reward = self.floor.check_vitals(action.patient_id, action.nurse_id)
            obs_text = (f"Vitals for {action.patient_id}: "
                        f"HR {vitals['hr']}, RR {vitals['rr']}, "
                        f"SpO2 {vitals['o2_sat']}, BP {vitals['sbp']}, "
                        f"Temp {vitals['temp']}. NEWS2: {self.floor.shift_states[action.patient_id]['news2']}")

        elif action.type == NurseActionType.OBSERVE_PATIENT:
            ambient, reward = self.floor.observe_patient(action.patient_id, action.nurse_id)
            obs_text = (f"Bedside assessment {action.patient_id}: {ambient}"
                        if ambient else f"No additional observation for {action.patient_id}.")

        elif action.type == NurseActionType.ADMINISTER_MEDICATION:
            obs_text, reward = self.floor.administer_medication(
                action.patient_id, action.medication or "", action.dose or "", action.nurse_id)

        elif action.type == NurseActionType.DOCUMENT_OBSERVATION:
            obs_text, reward = self.floor.document_observation(
                action.patient_id, action.text or "", action.nurse_id)

        elif action.type == NurseActionType.WRITE_HANDOFF:
            obs_text, reward = self.floor.write_handoff(action.text or "", action.nurse_id)

        elif action.type == NurseActionType.READ_HANDOFF:
            obs_text, reward = self.floor.read_handoff(action.nurse_id)

        else:
            raise ValueError(f"Unknown action type: {action.type}")

        snapshot = self.floor.get_floor_snapshot()
        fs = FloorState.model_validate(snapshot)
        finished = self.floor.tick >= 41

        step_result = StepResult(
            obs_text=obs_text,
            reward=reward,
            finished=finished,
            new_floor_state=fs,
        )
        return ToolOutput(
            blocks=[TextBlock(text=obs_text)],
            metadata={"contract_payload": step_result.model_dump()},
            reward=reward,
            finished=finished,
        )

    @tool
    def record_handoff(self, params: RecordHandoffParams) -> ToolOutput:
        """Store a handoff record and transition shift1 → shift2."""
        record = params.record
        obs_text, reward = self.floor.write_handoff(record.body, record.encoding_nurse_id)
        ack = HandoffAck(
            accepted=True,
            transitioned_to="shift2",
            handoff_id=f"handoff_{self.floor.tick}",
        )
        return ToolOutput(
            blocks=[TextBlock(text=obs_text)],
            metadata={"contract_payload": ack.model_dump()},
            reward=reward,
            finished=False,
        )

    @tool
    def score_handoff(self, params: ScoreHandoffParams) -> ToolOutput:
        """Score a handoff against ground truth at the requested tier (1, 2, or 3)."""
        if params.tier not in (1, 2, 3):
            raise ValueError("invalid tier")
        score, matched, missing = score_handoff_tier1(params.record.body)
        result = ScoreResult(
            score=score,
            matched_facts=matched,
            missing_facts=missing,
            tier=params.tier,
        )
        return ToolOutput(
            blocks=[TextBlock(text=f"Score (tier {params.tier}): {score:.2f}. "
                                   f"Matched: {len(matched)}. Missing: {len(missing)}.")],
            metadata={"contract_payload": result.model_dump()},
            reward=0.0,
            finished=False,
        )
