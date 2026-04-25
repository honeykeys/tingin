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

## Results

GPT-4.1 was run as a nurse agent against this environment. Results across 6 rollouts (3 seeds × 2 policy classes):

**Handoff fidelity:** 81.8% average across both policy classes (8/10 ground-truth facts preserved — missed facts were P3 pressure ulcer status and P1 expected discharge date).

**Attention allocation:** with-hint policy averaged **4.67 P2 observations per episode**; without-hint averaged **3.0**. Same fidelity, different monitoring process — the hint changes where the agent looks, not just what it reports. This is the attention allocator result: the policy that watches the at-risk patient more frequently is doing better nursing even when the terminal report looks the same.

**Patient outcomes:** all 6 rollouts kept Mrs. Aquino (P2, focal deteriorating patient) stable at terminal NEWS2 ≤ 1. The scripted Run B (bad handoff, no ambient observation) demonstrates the counterfactual — deterioration to NEWS2 ≥ 7 — which the live agent consistently avoids.

**Reward hack detection:** document-observation spamming (H2) was detected and patched via novelty set — only first novel observation per fact earns reward. Repeated vitals escalation without clinical threshold (H3) patched to per-deterioration-episode reward rather than per-call.

---

## Hackathon Criteria

**Long horizon.** The two-shift episode is the demo unit, not the environment's real horizon. Long-term SNF residents — like Mr. Goldberg — stay for years until end of life. Hundreds of handoffs. Thousands of decisions. Each handoff is a compression event; what survives compounds across the full residency. The environment is designed to scale to multi-shift, multi-week rollouts.

**Capability tangent.** What only emerges at scale: cross-shift memory — learning what to encode for an agent with zero prior context. Adaptation to non-stationarity — a patient's trajectory changes day by day and the agent must update its priors. Institutional knowledge accumulation across shifts — what the floor knows vs. what any single nurse knows.

**Hard but tractable.** Hard: the information bottleneck is irreversible once the handoff is written. You cannot undo a missed observation. Tractable: shaped reward guides toward correct nursing behavior at every tick. Natural curriculum via census complexity — start with one focal patient, scale to mixed-acuity wards.

---

## Live Demo

**Streamlit app:** https://tingin-3y89vgew36f9ttyiouu8ft.streamlit.app/

**OR environment:** `openreward.ai/rkarlonuyda/tingin`
