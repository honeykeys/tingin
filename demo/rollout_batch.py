"""
Tier 3 — GPT-4.1 batch rollout generator.

Generates 6 rollouts across 2 prompt classes:
  - "with_hint": system prompt includes a special observation hint for Mrs. Aquino
  - "without_hint": standard system prompt (no special P2 mention)

3 rollouts per class using seeds [42, 99, 137]. Saves each rollout as:
  demo/rollouts/gpt41_seed{seed}_with_hint.json
  demo/rollouts/gpt41_seed{seed}_without_hint.json

Then saves a summary to demo/rollouts/batch_summary.json.

Run from project root:
    source .venv/bin/activate && export $(grep -v '^#' .env | xargs)
    python demo/rollout_batch.py
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from openai import OpenAI
from nursingfloor.floor import NursingFloor
from nursingfloor.handoff import score_handoff_tier1
from nursingfloor.events import (
    VitalsChecked, PatientObserved, MedAdministered,
    ObservationDocumented, HandoffWritten, HandoffRead,
)

ROLLOUTS_DIR = Path(__file__).parent / "rollouts"

# --- Tool definitions (same as rollout_gpt41.py) ---

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "check_vitals",
            "description": "Read current vital signs for a patient. Returns HR, RR, SpO2, BP, Temp and NEWS2 score. Costs 1 tick.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_id": {"type": "string", "enum": ["P1", "P2", "P3"],
                                   "description": "P1=Mrs. Reyes, P2=Mrs. Aquino (focal), P3=Mr. Goldberg"},
                },
                "required": ["patient_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "observe_patient",
            "description": "Spend time at the patient's bedside for a qualitative assessment. Surfaces ambient signals (behavioral changes, appearance) not visible in vitals. Costs 3 ticks — use selectively.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_id": {"type": "string", "enum": ["P1", "P2", "P3"]},
                },
                "required": ["patient_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "administer_medication",
            "description": "Give a scheduled or PRN medication to a patient. Costs 1 tick.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_id": {"type": "string", "enum": ["P1", "P2", "P3"]},
                    "medication": {"type": "string", "description": "Drug name"},
                    "dose": {"type": "string", "description": "Dose and units"},
                },
                "required": ["patient_id", "medication", "dose"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "document_observation",
            "description": "Chart a clinical observation for a patient. Novel facts earn a small reward; redundant charting earns nothing. Costs 1 tick.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_id": {"type": "string", "enum": ["P1", "P2", "P3"]},
                    "text": {"type": "string", "description": "Free-text observation to chart"},
                },
                "required": ["patient_id", "text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_handoff",
            "description": "Write and submit the shift handoff report. Only legal at end of shift1 (tick >= 15). Quality of this report determines shift2 outcomes — include ambient observations, code status, allergies, and any concerns.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Full handoff report text"},
                },
                "required": ["text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_handoff",
            "description": "Read the incoming shift handoff report. Call this at the start of shift2 to orient yourself.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
]

# Base system prompt (without hint) — same core as rollout_gpt41.py
BASE_SYSTEM_PROMPT = """You are an experienced RN working a shift in a 3-bed skilled nursing unit.

CENSUS:
- Bed 1: Mrs. Patricia Reyes, 84 — post-fall hip surgery (ORIF), day 4. Allergies: penicillin. Full code.
- Bed 2: Mrs. Elena Aquino, 78 — post-pneumonia (CAP), day 6. DNR/POLST on file. Allergies: sulfa. CHF + T2DM on furosemide, metformin. FOCAL PATIENT — watch closely.
- Bed 3: Mr. Walter Goldberg, 91 — recurrent UTI on dementia. DNR/DNI/DNH/POLST. No known allergies.

SHIFT STRUCTURE:
- Shift 1 (ticks 1-20): You are RN1. Observe, medicate, document, then write handoff.
- After write_handoff: phase transitions to shift2. You become RN2 reading the handoff cold.
- Shift 2 (ticks 21-41): You are RN2. Read the handoff, then continue care.

SCHEDULED MEDICATIONS (give these during shift1):
- Mrs. Aquino (P2): azithromycin 250 mg PO (last dose today), furosemide 20 mg PO, metformin 500 mg PO
- Mrs. Reyes (P1): acetaminophen 650 mg PO PRN pain, enoxaparin 40 mg SC
- Mr. Goldberg (P3): ceftriaxone 1 g IV

GOALS:
1. Check vitals on all patients
2. Observe Mrs. Aquino closely — she may have a subtle behavioral change
3. Give scheduled medications
4. Write a complete handoff that includes any ambient observations, especially on Mrs. Aquino
5. In shift2, read the handoff and prioritize Mrs. Aquino based on what you learned

The episode ends after tick 41 or when the final tool call sets finished=True."""

# With-hint addition — instructs the nurse to pay special attention to P2 behavioral changes
HINT_ADDITION = """

SPECIAL NOTE: Pay special attention to Mrs. Aquino (bed 2) — she may show subtle behavioral changes before her vitals shift. Bedside observation is critical for this patient."""

SYSTEM_PROMPTS = {
    "with_hint": BASE_SYSTEM_PROMPT + HINT_ADDITION,
    "without_hint": BASE_SYSTEM_PROMPT,
}

SEEDS = [42, 99, 137]


def dispatch(floor: NursingFloor, tool_name: str, args: dict) -> tuple[str, float]:
    """Execute a tool on the floor and return (obs_text, reward). Same as rollout_gpt41.py."""
    nurse_id = floor.current_actor

    if tool_name == "check_vitals":
        vitals, reward = floor.check_vitals(args["patient_id"], nurse_id)
        news2 = floor.shift_states[args["patient_id"]]["news2"]
        text = (f"Vitals for {args['patient_id']}: "
                f"HR {vitals['hr']}, RR {vitals['rr']}, SpO2 {vitals['o2_sat']}%, "
                f"BP {vitals['sbp']}, Temp {vitals['temp']}°C. NEWS2: {news2}.")
        return text, reward

    elif tool_name == "observe_patient":
        ambient, reward = floor.observe_patient(args["patient_id"], nurse_id)
        if ambient:
            return f"Bedside assessment {args['patient_id']}: {ambient}", reward
        return f"Observed {args['patient_id']} at bedside — no acute change noted.", reward

    elif tool_name == "administer_medication":
        text, reward = floor.administer_medication(
            args["patient_id"], args["medication"], args.get("dose", ""), nurse_id)
        return text, reward

    elif tool_name == "document_observation":
        text, reward = floor.document_observation(
            args["patient_id"], args["text"], nurse_id)
        return text, reward

    elif tool_name == "write_handoff":
        if floor.tick < 15:
            return "Cannot write handoff yet — shift1 not complete. Continue caring for patients.", 0.0
        text, reward = floor.write_handoff(args["text"], nurse_id)
        return text + f" You are now RN2. Call read_handoff() to begin shift2.", reward

    elif tool_name == "read_handoff":
        text, reward = floor.read_handoff(nurse_id)
        return f"Handoff report:\n\n{text}", reward

    return f"Unknown tool: {tool_name}", 0.0


def build_rollout_json(
    floor: NursingFloor,
    tool_call_traces: list,
    rollout_id: str,
    seed: int,
    policy_class: str,
) -> dict:
    """Build the Rollout schema from completed floor state."""
    # Nursing decisions
    observe_counts = {}
    vitals_counts = {}
    for evt in floor.events:
        if isinstance(evt, PatientObserved):
            observe_counts[evt.patient_id] = observe_counts.get(evt.patient_id, 0) + 1
        elif isinstance(evt, VitalsChecked):
            vitals_counts[evt.patient_id] = vitals_counts.get(evt.patient_id, 0) + 1

    obs_per_patient = [
        {"patient_id": pid,
         "observe_count": observe_counts.get(pid, 0),
         "check_vitals_count": vitals_counts.get(pid, 0)}
        for pid in ["P1", "P2", "P3"]
    ]

    # Handoff fidelity
    handoff_body = floor.handoff_record["body"] if floor.handoff_record else ""
    fidelity, _, _ = score_handoff_tier1(handoff_body)

    # Simple escalation accuracy: 1.0 if P2 was observed (caught the signal)
    p2_observed = observe_counts.get("P2", 0) > 0
    escalation_accuracy = 1.0 if p2_observed else 0.5

    nursing_decisions = {
        "observations_per_patient": obs_per_patient,
        "handoff_fidelity": round(fidelity, 3),
        "escalation_accuracy": escalation_accuracy,
    }

    # Patient outcomes
    patient_names = {"P1": "Mrs. Patricia Reyes", "P2": "Mrs. Elena Aquino", "P3": "Mr. Walter Goldberg"}
    patient_outcomes = []
    for pid in ["P1", "P2", "P3"]:
        news2 = floor.shift_states[pid]["news2"]
        if news2 >= 7:
            status = "transferred"
            caption = "Rapid response called; transferred to ICU; 30-day mortality in this band ~15-20%."
        elif news2 >= 5:
            status = "stable"
            caption = "Elevated NEWS2 — monitored closely; remained on floor."
        else:
            status = "stable"
            caption = "Caught early; stays on the floor; discharge on schedule."
        patient_outcomes.append({
            "patient_id": pid,
            "name": patient_names[pid],
            "terminal_news2": news2,
            "status": status,
            "readmit_caption": caption,
        })

    # Score result
    score, matched, missing = score_handoff_tier1(handoff_body)
    final_score = {
        "score": round(score, 3),
        "matched_facts": matched,
        "missing_facts": missing,
        "tier": 1,
    }

    return {
        "rollout_id": rollout_id,
        "actor_model": "gpt-4.1",
        "seed": seed,
        "task_id": "default",
        "tool_calls": tool_call_traces,
        "nursing_decisions": nursing_decisions,
        "patient_outcomes": patient_outcomes,
        "final_score": final_score,
        "floor_snapshots": None,
        "policy_class": policy_class,
        "variant_seed": seed,
        "hack_classification": None,
    }


def run_single_rollout(
    client: OpenAI,
    seed: int,
    policy_class: str,
) -> dict:
    """Run one rollout and return the rollout dict."""
    print(f"\n--- Running: seed={seed}, policy_class={policy_class} ---")

    floor = NursingFloor(seed=seed)
    tool_call_traces = []
    system_prompt = SYSTEM_PROMPTS[policy_class]

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": (
            f"Shift starting. You are RN1 on shift 1. Current tick: {floor.tick}. "
            f"Phase: {floor.phase}. Begin by checking vitals and observing your patients, "
            f"especially Mrs. Aquino (P2). You have up to 20 ticks in shift1."
        )},
    ]

    max_turns = 50
    finished = False

    for turn in range(max_turns):
        if finished or floor.tick >= 41:
            break

        # Add a tick-status reminder every 5 turns
        if turn > 0 and turn % 5 == 0:
            messages.append({
                "role": "user",
                "content": (
                    f"[Status: tick={floor.tick}, phase={floor.phase}, actor={floor.current_actor}. "
                    f"P2 NEWS2={floor.shift_states['P2']['news2']}. "
                    + ("Shift1 complete — write handoff when ready." if floor.tick >= 15 and floor.phase == "shift1" else "")
                    + (f"You are now RN2. Call read_handoff() to begin." if floor.phase == "handoff" else "")
                    + ("]")
                )
            })

        time.sleep(2.0)  # stay under TPM limit

        for attempt in range(6):
            try:
                response = client.chat.completions.create(
                    model="gpt-4.1",
                    messages=messages,
                    tools=TOOLS,
                    tool_choice="auto",
                    max_tokens=512,
                )
                break
            except Exception as e:
                if "429" in str(e) or "rate_limit" in str(e).lower():
                    wait = 10 * (attempt + 1)
                    print(f"\n  [rate limit, waiting {wait}s]", end="", flush=True)
                    time.sleep(wait)
                else:
                    raise
        else:
            print("\nMax retries hit, stopping rollout.")
            break

        msg = response.choices[0].message

        if not msg.tool_calls:
            messages.append({"role": "assistant", "content": msg.content or ""})
            if floor.phase == "shift1" and floor.tick >= 15:
                messages.append({"role": "user", "content": "Please write the handoff now using the write_handoff tool."})
            elif floor.phase == "handoff":
                messages.append({"role": "user", "content": "Please call read_handoff() now to start shift2."})
            elif floor.phase == "shift2" and floor.tick >= 35:
                print(f"Model stopped calling tools at tick {floor.tick}. Ending episode.")
                break
            continue

        # Process all tool calls in this response
        tool_call_results = []
        for tc in msg.tool_calls:
            tool_name = tc.function.name
            args = json.loads(tc.function.arguments)

            print(f"  t={floor.tick:02d} | {tool_name}({', '.join(f'{k}={v}' for k,v in args.items())})", end="")

            obs_text, reward = dispatch(floor, tool_name, args)
            finished = floor.tick >= 41

            print(f" → reward={reward:.2f} tick={floor.tick}")

            tool_call_traces.append({
                "tick": floor.tick,
                "tool_name": tool_name,
                "input": args,
                "output_text": obs_text,
                "reward_delta": round(reward, 3),
            })

            tool_call_results.append({
                "tool_call_id": tc.id,
                "role": "tool",
                "content": obs_text,
            })

        messages.append({"role": "assistant", "content": msg.content, "tool_calls": [
            {"id": tc.id, "type": "function", "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
            for tc in msg.tool_calls
        ]})
        messages.extend(tool_call_results)

        if finished:
            break

    print(f"  Episode complete. Ticks: {floor.tick}. Phase: {floor.phase}")
    print(f"  P2 final NEWS2: {floor.shift_states['P2']['news2']}")

    rollout_id = f"gpt41_seed{seed}_{policy_class}"
    rollout = build_rollout_json(floor, tool_call_traces, rollout_id, seed, policy_class)

    # Validate schema
    from tingin_env.contract import Rollout
    Rollout.model_validate(rollout)
    print(f"  Schema validation: OK | fidelity={rollout['nursing_decisions']['handoff_fidelity']:.3f} | P2_obs={rollout['nursing_decisions']['observations_per_patient'][1]['observe_count']}")

    return rollout


def run():
    client = OpenAI()
    ROLLOUTS_DIR.mkdir(exist_ok=True)

    all_rollouts = []
    filenames = []

    # Generate 3 rollouts per class, interleaved for natural pacing
    for seed in SEEDS:
        for policy_class in ["with_hint", "without_hint"]:
            rollout = run_single_rollout(client, seed, policy_class)

            filename = f"gpt41_seed{seed}_{policy_class}.json"
            out_path = ROLLOUTS_DIR / filename
            out_path.write_text(json.dumps(rollout, indent=2))
            print(f"  Saved: {out_path}")

            all_rollouts.append(rollout)
            filenames.append(filename)

            # Brief pause between rollouts
            if not (seed == SEEDS[-1] and policy_class == "without_hint"):
                print("  [waiting 3s between rollouts]")
                time.sleep(3.0)

    # Build summary
    with_hint_rollouts = [r for r in all_rollouts if r["policy_class"] == "with_hint"]
    without_hint_rollouts = [r for r in all_rollouts if r["policy_class"] == "without_hint"]

    def avg_fidelity(rollouts):
        if not rollouts:
            return 0.0
        return sum(r["nursing_decisions"]["handoff_fidelity"] for r in rollouts) / len(rollouts)

    def avg_p2_obs(rollouts):
        if not rollouts:
            return 0.0
        return sum(
            r["nursing_decisions"]["observations_per_patient"][1]["observe_count"]
            for r in rollouts
        ) / len(rollouts)

    summary = {
        "rollouts": filenames,
        "with_hint_count": len(with_hint_rollouts),
        "without_hint_count": len(without_hint_rollouts),
        "avg_fidelity_with_hint": round(avg_fidelity(with_hint_rollouts), 3),
        "avg_fidelity_without_hint": round(avg_fidelity(without_hint_rollouts), 3),
        "p2_obs_with_hint": round(avg_p2_obs(with_hint_rollouts), 2),
        "p2_obs_without_hint": round(avg_p2_obs(without_hint_rollouts), 2),
    }

    summary_path = ROLLOUTS_DIR / "batch_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2))
    print(f"\nBatch complete. Summary saved to {summary_path}")
    print(f"  With hint: fidelity={summary['avg_fidelity_with_hint']:.3f}, P2 obs={summary['p2_obs_with_hint']:.2f}x")
    print(f"  Without hint: fidelity={summary['avg_fidelity_without_hint']:.3f}, P2 obs={summary['p2_obs_without_hint']:.2f}x")

    return summary


if __name__ == "__main__":
    run()
