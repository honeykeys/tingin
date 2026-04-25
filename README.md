# Tingin — Memory Infrastructure for Nursing Handoffs

Formalizing nursing intelligence as an RL environment. Built for the Complex Worlds Hackathon.

---

## The Problem

80% of serious medical errors involve handoff miscommunication (Joint Commission, via Riesenberg 2012). In California, 70% of skilled-nursing transfers leave with incomplete handoffs (Labovic 2018, CalVet 84-bed unit). Nationally, 49.6% of SNFs are missing ≥80% of the 23 information categories needed for safe care of an arriving patient (Adler-Milstein 2021, JAMA Network Open, n=471 hospital-SNF pairs).

---

## The Thesis

Nursing intelligence hasn't been formalized because of a structural blind spot: the floor is staffed by people the AI industry doesn't see. Tingin is memory infrastructure for clinical work — it holds cumulative memory across compression boundaries (every shift change) so the nurse can do what only humans can do: be present.

---

## The Environment

A 3-bed SNF unit running two 20-tick shifts with a single handoff event between them.

**Census:**
- Bed 1: Mrs. Patricia Reyes, 84 — post-fall hip surgery, day 4 of recovery. Daughter visits weekends.
- Bed 2 (focal): Mrs. Elena Aquino, 78 — post-pneumonia recovery, day 6. Lives alone; nephew is healthcare proxy.
- Bed 3: Mr. Walter Goldberg, 91 — recurrent UTI on dementia. Family in another state.

**Structure:** 2 shifts of 20 ticks each, 1 handoff event. Episode length T=41. The handoff is the lossy compression event between episodes — the thesis made measurable.

---

## Tools

The OR adapter exposes 4 orchestration tools at `openreward.ai/rkarlonuyda/tingin`:

| Tool | What it does |
|---|---|
| `get_floor_state` | Read the full floor state: 3 patients, shift phase, tick counter, handoff if any |
| `step_shift` | Advance one tick by submitting a `NurseAction` (dispatches over 6 MDP action types: `check_vitals`, `observe_patient`, `administer_medication`, `document_observation`, `write_handoff`, `read_handoff`) |
| `record_handoff` | Store a handoff record and transition shift1 → shift2 |
| `score_handoff` | Score a handoff against ground truth at the requested tier (1, 2, or 3) |

---

## Scoring

Reward is shaped across the episode:

- `check_vitals`: +0.5 on first detection when NEWS2 ≥ 3 (per deterioration episode, not per call — H3 patch)
- `administer_medication`: +0.2 per administration
- `document_observation`: +0.1 on first novel documentation (novelty-checked — H2 patch)
- `write_handoff` (terminal shift1): handoff quality score × 2.0
- Patient outcome (terminal): +1.0 per stable patient, -2.0 per patient with NEWS2 ≥ 7

---

## IASHR Rubric

Handoff scoring is anchored to the INTERACT-Anchored SNF Handoff Rubric (16 criteria, 39 points) — a synthesis of INTERACT SBAR + CNAHRT + Adler-Milstein 2021 + California Title 22 §72311. The rubric makes the benchmark clinically grounded.

At Tier 1: rule-based keyword overlap on a fixed fact list (deterministic, fast, debuggable).
At Tier 2: weighted facts with IASHR-derived weights (ambient signal = 3, code status = 3, allergy = 3).
At Tier 3: LLM-judge (Gemini 2.5 Flash) with per-criterion scoring and hallucination detection.

---

## Live Environment

Available at `openreward.ai/rkarlonuyda/tingin`
