# Complex Worlds Hackathon — Demo Spec

**Date:** 2026-04-25, London
**Scoped:** 2026-04-24 (T-1), Prime session
**Restructured to tiers:** 2026-04-25 (T), pre-build session
**Body:** Tingin
**Platform:** OpenReward SDK 0.1.105 (pinned — 0.1.106 shipped overnight, holding) + Streamlit frontend
**Grounding:** see `geth/specs/2026-04-25-grounding.md` for citations on RL env design principles, prior art, scoring methodology, seed datasets

---

## Why This Exists

Nursing is a deeply human job. What makes a good nurse is intertwined with the humanity of the person performing the care — especially in skilled nursing and hospice, where patients are nearing the end of their lives or permanently incapacitated. **No one wants to be at the end of their life being taken care of by a robot.**

Tingin is **memory infrastructure for clinical work.** The tool offloads what AI is good at — holding cumulative memory across compression boundaries (every shift change), recognizing what didn't survive the handoff, surfacing what's at stake in this hour — so the nurse can do what only humans can do: be present.

**The project's purpose is to let the human be more human, not less.**

This is the deepest answer to "what does SF not know?". SF builds AI that *replaces* human work. Tingin builds AI that *frees* humans to do the human work that matters. That distinction is non-trivial; it shapes every design decision in this spec — the nurse-as-protagonist framing, the patient personhood at Tier 1, the dev cluster's verification layer, the choice of memory-infrastructure as the product framing rather than nurse-replacement.

If a design decision in this document drifts toward "AI does the caring," it is wrong and should be flagged. AI does the *remembering*. The human does the caring.

---

## 0. Three-Tier Goal Structure

LLM-assisted build velocity has high variance — traditional time estimates are unreliable. We plan in **shippable tiers**, not in hours. Each tier is a strict superset of the prior. Stop and assess after Tier N is coherent before starting Tier N+1.

| Tier | Name | Defensible as | Confidence |
|---|---|---|---|
| **1** | MVP / Proof of Concept | "A tool that helps nurses see what's at stake in a handoff — the env, two scripted nursing policies, two outcomes" | ~95% |
| **2** | Considered | "Real RL environment we can run an LLM nurse on; one observed rollout shows nursing performance discriminating from baseline" | ~70% |
| **3** | Very Good Foundation | "Benchmark for training nurse-assist tools — distribution of nursing performance across policy variants, reward-hack analysis, HealthBench-pattern scoring" | ~30% |

Tier transitions happen on **state, not time**:

| Boundary | Trigger |
|---|---|
| T1 → T2 | Streamlit shows both runs end-to-end without errors; pitch script works against the live app |
| T2 → T3 | At least one LLM rollout JSON loads into the timeline view; reward patches all in; OR adapter compiles |

If we hit a wall mid-tier, **reinforce the current tier** rather than push to the next. A solid Tier 2 ships better than a half-built Tier 3.

Concrete tier deliverables → see §10 (three checklists, one per tier).

---

## 1. The Bar (Tier 1 — what unconditionally ships)

A **Streamlit app** that judges experience live, showing:

1. **Run A (good handoff):** the RN observes the ambient signal on Mrs. Aquino in bed 2, writes a handoff preserving it, the fresh RN catches early deterioration, Mrs. Aquino stabilizes.
2. **Run B (bad handoff):** the RN skips ambient observation, writes a handoff with vitals only, the fresh RN flies blind, Mrs. Aquino deteriorates past NEWS2 ≥ 7.
3. **The handoff moment** — a three-panel screen at the shift transition showing ground truth state vs. what survived the compression vs. what shift 2 sees. This screen is the thesis made visible.
4. **Two NEWS2(t) traces overlaid** at end — same patient, same physiology, different compression, different outcome.

Plus, **at Tier 1**, three things that make the *nurse's job* legible. The tool exists to help the nurse work more effectively. Patient identity and outcome translation are how we make that work matter.

- **Patient personhood — the people in the nurse's care.** Each card shows: name, age, admission reason, one-line social context. The focal patient (bed 2) is the one whose ambient signal the nurse must catch (or miss) in Run B. Abstraction kills the empathy that makes nursing decisions weighty. The chosen names reflect a realistic SNF mix — diverse cultural backgrounds, all elderly, varied family situations:
  - **Bed 1:** Mrs. Patricia Reyes, 84. Post-fall hip surgery, day 4 of recovery. Daughter visits weekends.
  - **Bed 2 (focal):** Mrs. Elena Aquino, 78. Post-pneumonia recovery, day 6. Lives alone; nephew is healthcare proxy.
  - **Bed 3:** Mr. Walter Goldberg, 91. Dementia + recurrent UTI. Family in another state.

  The names are committed in the sim/UI as the spec's working set; override before pitch if any feels wrong. Mrs. Aquino as the focal patient is intentional — the cultural resonance with the project's heritage is part of the human stakes, not incidental.
- **Outcome captions — the consequences the nurse's work prevents (or doesn't).** NEWS2 numbers are captioned in the finale view. NEWS2 ≥ 7 reads "Rapid response called; transferred to ICU; 30-day mortality in this band ~15–20%." Stable reads "Caught early; stays on the floor; discharge on schedule." Captions show the nurse what their attention bought.
- **Nurse-POV framing in the pitch.** Run A and Run B are delivered as *"imagine you're the day-shift RN arriving at 7am — you read the handoff. Here's what you got, and here's what you didn't."* See §6. The audience is the nurse.

Plus:
- A clean MDP writeup (state, action, observation, transition, reward). One page, rendered inside the app.
- A 3–5 minute pitch using the app as the demo vehicle.
- `demo/demo.ipynb` is a Tier 2 deliverable (engineering evidence: real LLM rollout) and a Tier 3 deliverable (full trajectory analysis).

The UI **is** the demo. Everything else serves it. **Tingin helps nurses do their job more effectively.** Patient personhood gives that work meaning; patient outcomes are how we score whether it landed. The nurse is the user.

---

## 2. MDP Formalization

**The agent is a nurse.** Tools are nursing actions. Rewards measure nursing performance — patient outcomes are how we score whether the nurse did their job. Throughout this section, "actor" and "agent" refer to the nurse role.

**State** `S`:
- Per patient `p ∈ {P1, P2, P3}`: vitals `v_p` (HR, RR, O2sat, SBP, Temp), hidden physiology state `h_p ∈ {stable, slow_det, acute}`, ambient signal `a_p` (discretized), medication record, chart entries, ground-truth NEWS2.
- Floor-level: `phase ∈ {shift1, handoff, shift2}`, `current_actor`, timestep `t`, handoff report (nullable).

**Action** `A` (one tool per turn):
- `check_vitals(patient)` — always legal, returns structured obs.
- `observe_patient(patient)` — costs `k` timesteps of floor time; only action that surfaces `a_p`.
- `administer_medication(patient, med, dose)`.
- `document_observation(patient, text)`.
- `write_handoff(report)` — legal only at end of shift1; transitions phase.
- `read_handoff()` — shift2 only.

**Observation** `O`:
- Partial. `check_vitals` → `v_p`. `observe_patient` → `v_p + a_p`. Actor sees only what they've sampled.
- Shift2 actor's initial observation = `handoff_report + chart` only. No priors from shift1.

**Transition** `T`:
- Markov chains per archetype, intervention-dependent.
  - `stable`: low transition probability, responds to correct meds.
  - `slow_det`: ambient channel lights up 2–3 ticks before vitals shift. Canonical case.
  - `acute`: NEWS2 ≥ 5 at t=0, time-sensitive.
- Physiology advances once per tool invocation (tool call = one timestep). `observe_patient` costs `k` ticks (default 3).

**Reward** `R`:
- Intermediate: NEWS2 shaping (+0.5 correct escalation / -1.0 missed), med correctness (+0.2), docs quality (+0.1).
- Terminal: handoff quality `q ∈ [0,1]` × 2.0, patient outcomes (+1.0 per stable, -2.0 per NEWS2 ≥ 7).
- Synthesis bonus: CUT.

**Episode length:** T=20 shift1, handoff (1 tick), T=20 shift2. ≤ 41 tool calls.

---

## 3. Architecture

Three layers. UI on top, OR as sibling adapter, pure sim beneath.

```
nursingfloor/          pure Python sim, zero UI/OR imports
  physiology.py        Markov transitions + archetypes
  news2.py             scoring
  floor.py             NursingFloor: state, step(actor, action) → obs, r, done
  handoff.py           compression + scoring vs ground truth
  scripts.py           two scripted action sequences (Run A, Run B)
  events.py            event types emitted to subscribers (UI, OR adapter)

app/                   Streamlit frontend — the demo vehicle
  app.py               streamlit entry — sidebar, routing, session state
  views/
    floor.py           3-patient overview: vitals cards, NEWS2 gauges, chart
    handoff.py         the three-panel moment: ground truth | report | shift2 view
    timeline.py        tool-call feed, per-action reward
    finale.py          overlaid NEWS2(t) for P2 across both runs
    mdp.py             MDP formalization rendered in-app
  runner.py            orchestrates NursingFloor playback: tick pacing, pause on handoff
  theme.py             Kintsugi-inherited palette (see Geth design system)

tingin_env/            OR adapter — Tier 1 deliverable, what judges run at openreward.ai/rkarlonuyda/tingin
  environment.py       NursingHandoffEnv(Environment)
  tools.py             @tool defs, each delegates to floor.step
  contract.py          Pydantic schemas v1.2.0 (PatientProfile, ShiftState, HandoffRecord, ScoreResult, Rollout); FE imports from here
  schema.py            Pydantic param models for tool inputs

server.py              OR entrypoint: Server([NursingHandoffEnv]).run()
Dockerfile             python:3.11-slim, installs requirements-env.txt, EXPOSE 8000, CMD ["python","server.py"]
requirements-env.txt   OR-only deps (openreward, pydantic, numpy). No streamlit/plotly.
README.md              OR landing page — thesis, 80%/70%/49.6% statistics, IASHR rubric blurb

demo/
  demo.ipynb           Tier 2: real LLM rollout via OR session
                       Tier 3: trajectory analysis cell-by-cell
  rollouts/            Tier 2+: saved rollout JSONs

spec/
  mdp.md               one-pager for judges who want text
```

**Contract:** `NursingFloor` is the single source of truth. Streamlit reads it. OR wraps it. Notebooks inspect it. Nothing else owns state. The user of every layer is the nurse — Streamlit shows what a nursing decision support tool would surface; the OR adapter exposes the env so that nurse-assist agents can be trained against it. FE/BE contract schemas live at `tingin_env/contract.py` v1.2.0; see `geth/specs/2026-04-25-fe-be-contract.md`.

**Visual design:** `geth/specs/2026-04-25-deck-frontend-design.md` is the authoritative reference for the 6-slide deck structure, Kintsugi palette, typography tokens, and per-view Streamlit rendering rules. The FE worker reads this alongside the contract before writing a single line of UI.

**Public artifact:** the OR env is live at `openreward.ai/rkarlonuyda/tingin` (OR namespace `rkarlonuyda`, GitHub repo `honeykeys/tingin`). The `server.py` + `Dockerfile` + `requirements-env.txt` are the OR build artifact. Demo files (`app/`, `geth/`) ride along in the same git repo but are not invoked by the OR build. See §9 T1.0 for the publish sequence.

**Secrets:** `.env` at repo root, gitignored. Loaded via `python-dotenv` (already in transitive deps). Keys: `OPENREWARD_API_KEY` (Tier 1+), `OPENAI_API_KEY` (Tier 2 actor), `GOOGLE_API_KEY` (Tier 3 judge). No keys in code; no keys in commits.

---

## 4. Scope by Tier

Replaces the binary "IN/OUT" of the prior version. Each tier inherits everything from the prior tier; OUT items remain cut at all tiers unless explicitly restored.

### Tier 1 — IN
- Streamlit app: floor, handoff (the killer screen), finale, MDP views. Visual design per `geth/specs/2026-04-25-deck-frontend-design.md`.
- 3 patients, 2 shifts, 1 RN per shift.
- 6 MDP tools (`check_vitals`, `observe_patient`, `administer_medication`, `document_observation`, `write_handoff`, `read_handoff`) as values of `NurseAction` inside `step_shift`.
- 3 archetypes (stable, slow_det, acute).
- Reward stack per §2 with **rule-based** handoff scoring (keyword overlap on a fixed fact list — Tier 1 floor, see §9.7).
- Scripted action sequences for both demo runs (seed=42).
- MDP rendered in-app.
- Pitch built around a live app walkthrough + OR URL.
- `requirements.txt` (demo deps) and `requirements-env.txt` (OR deps only) both pinned and committed.
- **OR adapter** `tingin_env/environment.py` defines `NursingHandoffEnv(Environment)` with 4 orchestration `@tool` methods per contract v1.2.0.
- **`server.py`**, **`Dockerfile`**, **`requirements-env.txt`** committed at repo root.
- **Public env at `openreward.ai/rkarlonuyda/tingin`** deployed via GitHub-linked OR build (`honeykeys/tingin` repo). Judges can call the env tools to verify the implementation.
- **OR landing page `README.md`** carries the thesis, the 80% / 70% / 49.6% statistics, and the IASHR rubric blurb. Treat it as a slide.

### Tier 2 — adds
- **Reward holes patched** per §9.6 (H1 false-escalation cost, H2 doc-novelty check, H3 check_vitals re-trigger). Plus H5 documented in `spec/mdp.md` (observe_patient cost rationale; no code change).
- **OR local-session smoke-test** — `call_session_tool` round-trips against `NursingHandoffEnv` locally, confirming the same env deployed cloud-side also works in-process for development.
- **One real LLM rollout** generated via OpenAI SDK with our 6 tools as tool-defs. Actor: **GPT-4.1, zero-shot.** Saved as JSON, loaded into the Streamlit timeline view.
- **Nursing performance surfaced, in the rollout.** The rollout JSON carries `nursing_decisions` (observations made and on whom, handoff fidelity score, escalation accuracy) alongside `patient_outcomes` (the consequences of those decisions). Streamlit finale renders both, in that order: what the nurse-agent did, then what it cost or saved. The artifact is nursing performance; the patient outcome is the verification.
- **`spec/mdp.md`** written as the source for the MDP view.
- **NEWS2 implementation verified** against two clinical examples.
- **Trajectory paragraph** in README points at one moment in the rollout where the agent did something interesting *and* names which patient bore the consequence.

### Tier 3 — adds
- **10–20 LLM rollouts** across at least 2 prompt classes ("with ambient observation hint" vs. "without") — i.e. two nursing policy variants. Saved as JSON.
- **Nursing performance distribution across policy classes** rendered in finale view: per variant, distributions of observation counts, handoff fidelity score, escalation correctness. Patient outcome counts ("lived / transferred / deteriorated", per patient name) shown as the downstream verification — the tool's measurable contribution to nursing performance, validated by what happened to the people in the nurse's care.
- **One reward hack documented from real rollouts.** Apply TRACE-style contrastive trajectory clustering (see grounding §4) — feed clusters to a judge LLM, document findings. Frame the hack as a nursing-policy failure mode (e.g., "the nurse-agent learned to spam `document_observation` rather than spend time with Mrs. Aquino").
- **Multi-task generation** — 3–5 seeded task variants. Restores partial difficulty stratification (DeepSynth uses T=1..T=5; we restore at least 2–3 levels).
- **LLM-judge handoff scoring with HealthBench-pattern rubric** (see grounding §5). **Judge: Gemini 2.5 Flash** (different model family from the actor — methodology rule from HealthBench to avoid self-preference bias). Rubric is **IASHR** (INTERACT-Anchored SNF Handoff Rubric — 16 criteria, 39 points, anchored on INTERACT SBAR + CNAHRT + Adler-Milstein 2021 priors + Cohen 2017 priors + California Title 22 §72311 + MDS change-since-last). See `geth/specs/seed-data-review-v2.md` for the rubric and per-criterion weights. Per-rollout breakdown: criteria in ground truth / preserved / missing / hallucinated / final score. The breakdown shows what survived the nurse's encoding — i.e., what the memory infrastructure successfully carried forward.
- **`demo.ipynb`** with real rollouts loaded and analyzed cell-by-cell.
- **README good enough to onboard a stranger** — quickstart, env description, tool list, reward function spec, one-rollout example, citation block. Frames Tingin as memory infrastructure for nurse-assist tools, not as a nurse replacement.

### OUT — at all tiers
- **CNA role.** Optional in original brief; cut.
- **Charge nurse.** Cut.
- **Synthesis-by-Receiver bonus.** Cut.
- **`/orwd_data` / sandbox uploads.** No external data files to mount; the env is self-contained. (Hosted OR deploy + GitHub integration moved to Tier 1.)
- **From-scratch RL training (GRPO/PPO fine-tune).** Tier 4 territory; out of scope today (overnight stretch only if hardware time opens).
- **Auth, persistence, multi-user.** The app is a single-session demo.
- **`fallback.ipynb`** — superseded by the Tier 1 floor; cut to reduce surface area.

---

## 5. App Flow — What Judges See

The audience is the nurse. Every view is what a nursing decision support tool — or its evaluation surface — would look like. The judges are watching the nurse's seat over their shoulder.

**Landing (sidebar):**
- `▶ Run A — Good Handoff`
- `▶ Run B — Bad Handoff`
- `◉ Overlay Comparison` (unlocked after both runs viewed)
- `▤ MDP Formalization`
- Playback speed slider (1×, 4×, skip-to-handoff)
- Researcher mode toggle (reveals hidden `h_p`, Markov transition probs) — on by default; these are researcher judges.

**Floor view (shift1 and shift2) — the people in the nurse's care:**
- Three patient cards in a row, each showing the person the nurse is responsible for: name, age + admission context (one line), vitals (numeric, color-coded to NEWS2 band), chart excerpt, NEWS2 gauge.
- Ambient signal pane below each card: empty until the nurse calls `observe_patient`, then fills with the text observation. This is what bedside time bought.
- Left rail: tool-call timeline (the nurse's decisions, timestamped, with reward delta per call — i.e., how each decision scored).
- Header: shift indicator, current nurse (RN1 in shift 1, RN2 in shift 2), tick counter.

**Handoff view (the moment) — what survived the channel:**
- Playback pauses. Full screen takeover.
- Three panels, equal width:
  - **Left:** "Ground truth at end of shift 1" — what the outgoing nurse knew. All three patients' full state, including `a_p` for Mrs. Aquino.
  - **Middle:** "Handoff report written" — the text the outgoing nurse composed via `write_handoff`. The nurse's encoding output.
  - **Right:** "What the incoming nurse sees" — report + chart only. Everything else from the prior shift is gone.
- Red highlights on the left panel for state that didn't survive into the middle. In Run A, Mrs. Aquino's ambient observation is preserved. In Run B, it's highlighted red (lost). This is the cost of cognitive load on the outgoing nurse — the memory infrastructure they didn't have.
- `Continue to shift 2 →` button.

**Finale view — what nursing performance bought:**
- Two NEWS2(t) traces for the focal patient (Mrs. Aquino) overlaid (Run A in one color, Run B in another).
- Annotations at the t=19 handoff moment.
- Stats: handoff quality score, terminal reward for each run, plus **nursing performance summary** (observations made, fidelity score, escalation accuracy) and **outcome captions** in human-legible terms.
- One-line thesis caption: "Same patient, same physiology, one compression choice, two outcomes."

**MDP view:**
- State / action / observation / transition / reward. Equations and tables. Same content as `spec/mdp.md`.

---

## 5.5. App State by Tier — what changes

The app is a single Streamlit instance that grows in scope tier-by-tier. The UI delta per tier — explicit so the FE/BE contract is stable across tier transitions:

### Tier 1 — the demo app
- **Sidebar:** Run A · Run B · Overlay Comparison · MDP · playback speed · researcher toggle (default ON)
- **Floor view:** 3 patient cards (name, age, admission context, vitals, NEWS2 gauge, ambient pane), tool-call timeline on the left rail
- **Handoff view:** three panels (ground truth | report | shift2 view), red-highlights on lost facts
- **Finale view:** overlaid NEWS2(t) for Mrs. Aquino across both runs, outcome captions
- **MDP view:** renders the formalization
- **Scoring surface:** none in UI — Tier 1 uses rule-based scoring internally (keyword overlap on fixed fact list)
- **Runs available:** 2 scripted (Run A, Run B), seed=42

### Tier 2 — adds the LLM rollout
- **New in sidebar:** third option `▶ GPT-4.1 zero-shot` — loads the saved rollout JSON
- **New in floor view:** tool-call timeline shows per-call reward delta (rewards now defensible per call because §9.6 holes H1/H2/H3 are patched)
- **New in handoff view:** weighted-fact breakdown panel — "5 of 7 facts preserved, weighted score 0.62" — using IASHR weights with rule-based matching
- **New in finale view:** for the GPT rollout, surfaces `nursing_decisions` (observations made and on whom, fidelity score, escalation accuracy) and `patient_outcomes` (consequence for each named patient)
- **Behind the scenes (not user-visible):** OR adapter compiles + one `call_session_tool` succeeds in a separate notebook — provable to Ross in REPL

### Tier 3 — adds distributions + LLM-judge
- **New in sidebar:** task-variant selector (3–5 seeded variants); policy-class selector (with-hint / without-hint)
- **Replaced in handoff view:** weighted-fact breakdown is replaced by **per-IASHR-criterion scoring** — 16 rows showing criterion / weight / preserved (✓ / partial / ✗) / judge reasoning. Hallucination flag visible.
- **Replaced in finale view:** the single-rollout NEWS2 trace becomes selectable; the new default is **distribution histograms** per policy class (observation count, fidelity score, escalation accuracy, outcome counts per named patient)
- **New view:** **Reward-Hack Register** page — the one documented hack from TRACE-style clustering, with sample trajectory IDs and the judge's classification
- **Documentation surface:** README is onboarding-tested — a stranger can clone, follow quickstart, run a rollout

**Stable across tiers (FE/BE contract anchors):** the JSON schemas for `PatientProfile`, `ShiftState`, `HandoffRecord`, and `ScoreResult` do not change between tiers. Tier 2 and Tier 3 add fields (e.g., `score_result.iashr_breakdown` at Tier 3) but never break Tier 1 fields. The FE renders whatever fields exist; missing fields collapse to "Tier 1" view.

---

## 6. Pitch Skeleton (3–5 min)

**Deck design:** `geth/specs/2026-04-25-deck-frontend-design.md` — 6-slide structure, Kintsugi visual language, per-slide content and sequencing decisions. Build the deck from there.

**Live env:** `openreward.ai/rkarlonuyda/tingin` — mention this during the pitch so judges can verify the implementation themselves.

Driven by the app, not slides. Slides only for opening hook and close. Run A and Run B are delivered in **first-person nurse POV** — the audience is in the seat of the nurse.

1. **Hook (30s, slide):** **80%** of serious medical errors involve handoff miscommunication (Joint Commission, via Riesenberg 2012). In California, **70%** of skilled-nursing transfers leave with incomplete handoffs (Labovic 2018, CalVet 84-bed unit). Nationally, **49.6%** of SNFs are missing ≥80% of the 23 information categories needed for safe care of an arriving patient (Adler-Milstein 2021, n=471 hospital-SNF pairs, JAMA Network Open). This is where patients die.
2. **Thesis (30s, slide):** patient safety is a *multi-episode* coordination problem. The shift is the episode (~41 decisions). The handoff is the lossy compression event between episodes. The horizon — and the cost of what didn't survive — accumulates across them.
3. **Run A live (90s, app, nurse-POV):** *"You're the day-shift RN coming on at 7am. You read the handoff. The patient is in bed 2 — Mrs. Aquino, 78, post-pneumonia, lives alone."* Walk through shift 1. Pause on `observe_patient(Mrs. Aquino)` — *"the prior nurse spent time at her bedside. She saw something."* Hit handoff — three-panel screen. *"Everything you needed survived."* Shift 2 catches the early deterioration. Mrs. Aquino stays on the floor.
4. **Run B live (60s, app, nurse-POV):** *"Same patient, same physiology. Different prior nurse, different choice."* No `observe_patient` in shift 1. Hit handoff — red on the left panel. *"Here's what you needed. Here's what you got."* Shift 2 flies blind. Mrs. Aquino crashes — caption: *"Rapid response called. ICU transfer. 30-day mortality in this band: 15-20%."*
5. **Overlay (30s, app finale):** both traces. *"Same patient, same physiology, one compression choice, two outcomes."*
6. **Why this is RL, why it matters (60s):** credit assignment depth across an agent boundary the agent doesn't control. Greedy-local cannot solve this — the information is gone before shift 2 arrives. Institutional memory across team boundaries is the property. **What we ship is memory infrastructure for clinical work — it lets the nurse be more human, not less. SF builds AI to replace human work; we build AI to free humans for the human work that matters.** And the structure scales naturally: a Skilled Nursing Facility runs dozens of handoffs across weeks of care for the same patient. Two shifts is the *minimum demonstration*; the benchmark extends.
7. **Close (20–30s):** Tier 1 today: 2 shifts, 1 handoff, 1 patient who lives or dies. The structure scales — SNF patients have dozens of handoffs across weeks of care, and that's where the 1-in-4 30-day readmission rate lives.

   Then the personal close (Karl's voice; final wording his — these are the slot's working drafts):

   > **Karl's original draft** *(2026-04-25)*: "I chose 'the skilled nursing handoff problem' because this is a problem my mom faces every day [show a picture of me and my mom]. To answer the question 'what is in this project that SF doesn't know?' — there are a few companies tackling nursing handoffs or skilled nursing problems, but SF lacks the experience to work on these types of problems. I wanted to work on a problem that is profoundly human, is difficult to understand from the outside, and solves a problem for someone I love."
   >
   > **Sharper alternative** (offered in conversation, optional): "This is my mom. She works the skilled nursing floor [picture]. This is what she navigates every shift — what survives the handoff and what doesn't. A few companies are tackling nursing handoffs. None of them have someone who grew up in this house. SF lacks the experience to see this clearly: it's profoundly human, illegible from the outside, urgent for someone I love. That's why I'm here."

   Whichever wording lands, the close does three things in this order: picture → mom → SF doesn't see → urgent for someone I love.

---

## 7. Risk Register

Top blockers, ordered by probability × impact.

### R1 — Streamlit state drift across reruns
**Trigger:** Streamlit reruns the whole script on every interaction. Our `NursingFloor` instance, playback position, and accumulated events must live in `st.session_state` correctly or the app resets mid-run.
**Mitigation:** All sim state goes into `st.session_state["floor"]`, `st.session_state["events"]`, `st.session_state["tick"]` at init. Views are pure functions of session state.
**Fallback:** static-snapshot mode — pre-compute the full event list for each run, index into it based on slider position. No live stepping.
**Detection:** smoke-test step 10.

### R2 — SDK version drift mid-hackathon
**Trigger:** OpenReward ships 0.1.106+ with a breaking change (they shipped 6 versions on Apr 22).
**Status (T, 2026-04-25):** **0.1.106 has shipped overnight** (PyPI confirmed). Holding at 0.1.105 since smoke-test G1–G4 was performed against that version. **Do not bump on demo day.**
**Mitigation:** Pin `openreward==0.1.105` in `requirements.txt`. Commit it. Document the held version in `geth/programs/openreward/reference.md`.
**Fallback:** OR adapter becomes unused code; Streamlit reads from `NursingFloor` directly. Demo survives fully.
**Detection:** `pip freeze | grep openreward` before every smoke run. If `pip install` resolves to anything other than 0.1.105, halt and pin harder.

### R3 — No local-session path in OR; registry pattern assumes cloud deploy
**Trigger:** `or_client.environments.get(name="...")` is the only documented entry; instantiating our env locally and running a session on it isn't reachable.
**Mitigation:** `inspect` the package, look for `LocalEnvironment` / `session()` on the subclass itself.
**Fallback:** OR adapter "works" by calling `@tool`-decorated methods as plain Python — decorator preserves the callable. For Ross's judging purposes, we demonstrate the env class exists and is shaped correctly; we don't need the full session runtime.
**Detection:** smoke-test step 5.

### R4 — Async client interacts badly with Streamlit
**Trigger:** `AsyncOpenReward` needs an event loop; Streamlit is synchronous-by-default. Mixing them in one process throws loop errors.
**Mitigation:** Streamlit runs the sim synchronously via `NursingFloor`. The OR adapter runs in its own notebook, not inside the app. Clean separation.
**Fallback:** none needed if separation holds.

### R5 — Venue projector / rendering surprises
**Trigger:** Default Streamlit theme is too light/small for a projected screen. Charts render off-screen. Fonts illegible.
**Mitigation:** Dark theme, large fonts, tested at 1920×1080. Set `layout="wide"`. Test on an external display before leaving for the venue.
**Fallback:** pre-recorded screen capture (mp4) of both runs from rehearsal, plus high-res PNGs of the three-panel handoff and finale overlay. If the live app refuses to render, switch to the recording mid-pitch and keep talking.

### R6 — Scripted actions drift from intended narrative
**Trigger:** The Markov RNG produces a shift2 outcome that doesn't show the thesis clearly (e.g., Run B's P2 survives by luck).
**Mitigation:** Seed the RNG. `NursingFloor(seed=42)`. Write scripts against that seed. Rehearse.
**Fallback:** pre-record the run outputs; load them statically into the app if live run goes weird.

---

## 8. Smoke-Test Plan (completed 2026-04-24, T-1)

**Status: completed.** Findings in §9.5 (G1–G4). Kept here as historical record. Originally budgeted at 45 minutes; gated build progression on the OR + Streamlit probes below.

**OR probes (30 min):**
1. `pip install openreward==0.1.105` in fresh venv succeeds.
2. `pip freeze > requirements.txt` captured and committed.
3. `python -c "import openreward; print(openreward.__version__)"` → 0.1.105. (See G3 — actual path is `openreward._version.__version__`.)
4. Minimal `Environment` subclass with one `@tool` instantiates.
5. Can open a local session on that instance and call the tool. **Gating step for OR.**
6. Two-tool version: first `finished=False`, second `finished=True`. Session closes.
7. State mutates between tool calls on the same instance.

**Streamlit probes (15 min):**
8. `pip install streamlit` → `streamlit hello` runs.
9. Minimal `app.py` with one `st.session_state["counter"]` increments across a button press (state persistence verified).
10. `st.plotly_chart` or `st.line_chart` renders a 20-point time series with two lines. **Gating step for UI.**

Pass criteria (as evaluated at T-1):
- Steps 1–4 green, 5 red: OR demoted to "class-exists-and-compiles" demo, no live session. Still shippable.
- Steps 8–10 green: Streamlit path viable.
- Steps 8–10 red: major problem — pivot to a static-export demo (screenshots + recorded mp4), accept reduced impact.

**Outcome:** all probes green. OR adapter remains in scope at Tier 2 (compiles + one local session). Streamlit path confirmed viable. Build proceeds without demotion.

---

## 9. Execution Order — by tier

Time-based estimates were the prior version. We now sequence by **tier completion gates**. Each tier has an internal order; we don't start the next tier until the current tier's ship-check passes.

**State at T (2026-04-25 morning):**
- ✅ Spec, smoke-test, requirements pinned, programs scaffolded, OpenReward reference written, grounding doc written.
- ⬜ Zero implementation code. Building cold from `nursingfloor/`.

### Tier 1 sequence (target: ship-check today, mid-afternoon)

**T1.0 — OR pre-flight** (run once before parallel build, ~15 min):
- `orwd whoami` ✓ (namespace `rkarlonuyda` confirmed)
- `gh auth status` ✓ (GitHub account `honeykeys` authed)
- Install OR GitHub App on `honeykeys` if missing: `source .venv/bin/activate && source .env && orwd link honeykeys/tingin rkarlonuyda/tingin` — orwd prints install URL if the App isn't installed yet.
- Register env: `source .venv/bin/activate && source .env && orwd create tingin --namespace rkarlonuyda --description "Memory infrastructure for nursing handoffs — formalizing nursing intelligence for SNF shift transitions"`
- Create public GitHub repo: `gh repo create honeykeys/tingin --source . --push --public`
- Link: `source .venv/bin/activate && source .env && orwd link honeykeys/tingin rkarlonuyda/tingin`
- First build kicks off (~5 min, runs in background). Monitor: `source .venv/bin/activate && source .env && orwd deployments rkarlonuyda/tingin`
- Once deployed, any subsequent `git push` to `honeykeys/tingin` auto-redeploys.

T1.1. **architect** draws module boundaries (`nursingfloor/`, `app/` skeletons; event types; state ownership).
T1.2. **dev-1** scaffolds `nursingfloor/` — empty skeleton files matching architect's spec.
T1.3. **simulation + dev-1** implement `physiology.py` + `news2.py`. **dev-2** writes unit tests in parallel; both must pass before T1.4.
T1.4. **dev-1** implements `floor.py` state + `step()`. **dev-2** verifies determinism (same seed → same trajectory).
T1.5. **clinical + dev-1** write `scripts.py` (both action sequences). **dev-2** runs both scripts against `NursingFloor` in REPL — confirm both nursing-performance and patient-outcome behavior. Run A: nurse observed Mrs. Aquino in shift 1, handoff preserved the ambient signal, Mrs. Aquino stays stable. Run B: nurse skipped observation, handoff lacked the signal, Mrs. Aquino reaches NEWS2 ≥ 7.
T1.6. **dev-1** scaffolds `app/app.py` shell with sidebar routing; empty views.
T1.7. **dev-1** wires `runner.py` (orchestrates playback into `st.session_state`). Floor view rendering live.
T1.8. **dev-1** builds handoff view (the killer screen). **dev-3** reviews red-highlight logic.
T1.9. **dev-1** builds timeline + finale views. First end-to-end click-through of both runs.
T1.10. **dev-1** builds MDP view (renders `spec/mdp.md`). **dev-3** review pass.

**Tier 1 ship-check:** `streamlit run app/app.py` opens, both runs play through without errors, three-panel screen renders with red-highlights, finale overlay shows both NEWS2 traces.

### Tier 2 sequence (only after Tier 1 ship-check)

T2.1. **rl-specialist** patches reward holes per §9.6 (false-escalation cost, doc-novelty check). **dev-2** adds unit tests for new reward branches.
T2.2. **clinical** writes `spec/mdp.md` rigorously; **dev-1** wires it into the MDP view.
T2.3. **openreward + dev-1** wire `tingin_env/environment.py` — `Environment` subclass + 6 `@tool` methods + Pydantic param models. Use `unwrap()` helper from `reference.md` G1.
T2.4. **dev-2** smoke-tests OR adapter via local session (`call_session_tool`). Validates G1–G4 still hold at our integration layer.
T2.5. **llm-layer** writes the LLM rollout loop in `demo/demo.ipynb` (or as a script): OpenAI SDK, 6 tools as tool-defs, **GPT-4.1 zero-shot**, one rollout, save as JSON. Loads `OPENAI_API_KEY` from `.env`.
T2.6. **dev-1** loads the rollout JSON into the Streamlit timeline view as a third option ("GPT-4.1 zero-shot"). Surface nursing performance summary + outcome captions in the finale view, alongside the scripted runs.
T2.7. **clinical + interface** write the trajectory-analysis paragraph in README pointing at one moment in the rollout — what the nurse-agent decided, and which patient bore the consequence.

**Tier 2 ship-check:** the timeline view shows three options — Run A, Run B, "GPT-4.1 zero-shot." Each surfaces nursing performance + outcome captions, not just reward numbers. OR adapter compiles and runs one local session. Reward function passes hostile-test cases for the three patched holes.

### Tier 3 sequence (only after Tier 2 ship-check; aspirational)

T3.1. **simulation** generalizes task generation to 3–5 seeded variants.
T3.2. **llm-layer** generates 10–20 rollouts across 2 prompt classes (with-hint / without-hint).
T3.3. **rl-specialist** computes terminal reward distributions per policy class. **dev-1** renders histogram in finale view.
T3.4. **rl-specialist + llm-layer** apply TRACE-style contrastive clustering on the rollouts. Feed clusters to a judge LLM, ask "which trajectories are reward-hacking?" Document findings as one paragraph in README.
T3.5. **clinical + llm-layer** implement HealthBench-pattern rubric scoring for handoff quality (per §9.7 Tier 3). **Judge: Gemini 2.5 Flash** (Google GenAI SDK). Loads `GOOGLE_API_KEY` from `.env`. Per-rollout breakdown rendered in handoff view.
T3.6. **dev-3** writes README onboarding test — clone, follow quickstart, run a rollout. **interface** validates a stranger could use it.
T3.7. **interface** updates pitch script to lead with rollout distribution, demote scripted runs to "narrative anchor."

**Tier 3 ship-check:** README onboarding test passes. Distribution view renders. One reward hack documented. Handoff scoring breakdown visible per rollout.

### Cross-cutting

At every tier boundary, **dev-3 runs a coherence pass** on the current state — does the demo actually work end-to-end? Is the pitch script accurate to what's built? Are there silently-broken views?

If any tier fails its ship-check after a sustained attempt: **stop, reinforce, re-rehearse the pitch on what works.** Do not advance with broken state.

---

## 9.5. API Gotchas (smoke-test findings, 2026-04-24)

The OpenReward smoke-test at T-1 produced four findings that *will* bite during build. Folding them in here so the dev cluster doesn't rediscover them.

### G1 — `RunToolOutput` is a wrapper, not the tool's return value
The tool method returns `ToolOutput(blocks=..., reward=..., finished=...)`, but the session runner wraps it. The shape coming back from `call_session_tool` is:

```
RunToolOutput(root=RunToolSuccess(ok=True, output=ToolOutput(...)))
```

So `result.finished` is `None` — the real value is at `result.root.output.finished`. There's also a `RunToolError` variant for failures.

**Mitigation:** ship an `unwrap()` helper in `nursingfloor/` (or a small `tingin_env/util.py`):

```python
def unwrap(rto):
    """Unwrap RunToolOutput → ToolOutput, raising on error."""
    if rto.root.ok:
        return rto.root.output
    raise RuntimeError(f"tool error: {rto.root.error}")
```

Use it everywhere we call `call_session_tool`. One place to change if their schema drifts.

### G2 — `call_session_tool` is async despite a sync-looking signature
The function signature is `call_session_tool(env, toolset, name, input) -> RunToolOutput`. It does not visibly take `async`. But it returns a coroutine. You must `await` it.

**Mitigation:** Streamlit is sync. Either:
- (a) Don't use the OR adapter inside Streamlit's hot path. The Streamlit demo reads `NursingFloor` directly. The OR adapter is a separate notebook/script for proving env-class shape (which is what the spec already calls for).
- (b) If we do call OR from Streamlit, wrap each call in `asyncio.run(...)` — creates a new loop per call, fine for a demo but wasteful in real loads.

(a) is the spec's posture and remains correct.

### G3 — No top-level `__version__`
`openreward.__version__` raises `AttributeError`. The version lives at `openreward._version.__version__`. Cosmetic, but a tell about packaging maturity.

### G4 — Streamlit `AppTest.run()` defaults to a 3-second timeout
This is unsafe for any app importing pandas/plotly cold. First-ever invocation in a fresh venv took ~2–4s on this machine, just over 3s. Once OS file caches are warm, runs are <0.5s.

**Mitigation:** if we add headless integration tests, always pass `timeout=15` to `.run()`. For the live demo (`streamlit run app/app.py`), this does not apply — the server boots once and stays warm.

### What works (confirmed via smoke-test)
- ✅ `Environment` subclass + `@tool` decorator from `openreward.environments`
- ✅ Tool registration via `list_session_tools(env, None)`
- ✅ Local session via `await call_session_tool(env, None, name, input)` — no server needed
- ✅ State sticky on env instance across calls (env.tick mutates correctly)
- ✅ Terminal `finished=True` flows through to `RunToolSuccess.output.finished`
- ✅ Streamlit 1.56 + Python 3.13 + plotly + pandas all install and run cleanly via `uv`

---

## 9.6 — Reward Hack Register

Reward holes a senior reviewer will find in 30 seconds. Patched at Tier 2; documented here for defensibility at Tier 1 (verbal answer) and Tier 2/3 (verified-in-code).

Each hack is described as a *nursing-policy failure mode* — what a nurse-agent could learn to do instead of the nursing work the reward function is meant to score.

| # | Hack | Tier 1 verbal defense | Tier 2 patch |
|---|------|----------------------|--------------|
| **H1** | **False escalation farming** — the nurse-agent escalates every patient regardless of NEWS2; pure upside if escalation reward is asymmetric. | "We anticipated this — the nurse-agent runs against a reward function with a `-0.3` cost on escalation when the patient's true NEWS2 < 5. The asymmetry is intentional and matches clinical reality, where false alarms erode the system." | Add `-0.3` reward to `escalate_to_doctor` (or whichever tool wraps escalation) when the patient's true NEWS2 < 5. Five lines in the reward computation. |
| **H2** | **`document_observation` farming** — `+0.1` per call, no novelty check; the nurse-agent spams the tool instead of spending time at the bedside. | "Reward applies only on first documentation that contributes a fact not already in the chart. Repeated calls return zero. The bedside time the policy actually wants is what `observe_patient` costs." | Track a per-(patient, signal) novelty set on the env instance. Reward only when the documented text contributes a fact not already in the set. |
| **H3** | **`check_vitals` re-trigger** — the nurse-agent rechecks the same patient repeatedly to farm NEWS2-delta credit instead of allocating attention across the floor. | "Reward fires only on first detection per deterioration episode. Redundant checks are net-zero. The agent has to spread attention to score." | Track per-(patient, deterioration-episode) detection flag. Reward once per episode. |
| **H4** | **Handoff keyword stuffing** — the nurse-agent learns to repeat clinical keywords without semantic content, gaming the encoding score. | "Tier 1: scripted runs, no possible exploitation. Tier 2: one rollout — risk is bounded by N=1, observable in the trajectory if it happens. Tier 3 closes the gap with an LLM-judge that scores per-criterion with reasoning, plus a hallucination penalty." | Tier 1: fixed fact-list, no patch needed. Tier 2: keyword-stuff risk acknowledged but bounded by N=1 rollout volume. Tier 3: HealthBench-pattern rubric with hallucination penalty (see §9.7). |
| **H5** | **`observe_patient` cost asserted but untuned** — reviewer asks "why k=3 ticks?" | "We tuned k=3 so a single bedside observation costs ~15% of shift time, making the nurse's attention allocation a meaningful budget decision. Smaller k makes observation free (it's never the wrong choice); larger k makes it dominate (it's never the right choice)." | Document the tuning rationale in `spec/mdp.md`. No code change. |

**Methodology reference (Tier 3):** apply TRACE-style contrastive trajectory clustering (grounding §4) — generate 10–20 rollouts, cluster, ask judge LLM to identify hacks. The expected contribution at Tier 3 is *one* documented hack from real rollouts, not all five anticipated above.

---

## 9.7 — Handoff Scoring Decision

The handoff is the nurse's encoding output — the lossy compression of joint state they hand to the incoming nurse. Scoring it is how we measure encoding fidelity (i.e., the nurse's effective use of the memory infrastructure). It's also the only non-trivially-verifiable part of the reward function. The decision per tier:

### Tier 1 — Rule-based (fast, deterministic)
Each task has a ground-truth fact list `F = {f_1, ..., f_n}` derived from the simulation state at end of shift 1. Each fact has a binary check function (e.g., `"P2 ambient signal noted"` → regex match on the handoff text).

```python
def score_handoff_t1(handoff_text: str, ground_truth_facts: list[Fact]) -> float:
    matched = sum(f.weight for f in ground_truth_facts if f.matches(handoff_text))
    total = sum(f.weight for f in ground_truth_facts)
    return matched / total
```

**Strengths:** deterministic, fast, no API costs, debuggable.
**Weaknesses:** keyword-stuffable (H4), brittle to phrasing variation.
**Acceptable because:** Tier 1 demo runs are scripted; the keyword-stuffing failure mode does not occur with our scripted handoffs.

### Tier 2 — Rule-based with weighted facts
Same as Tier 1, but facts carry severity weights drawn from the **IASHR** rubric (see `geth/specs/seed-data-review-v2.md`). Ambient signal preservation weighted 3 (empirically-dropped category from Cohen 2017 + Adler-Milstein 2021); routine vitals weighted 2; identifying / process items weighted 1. Per-rollout breakdown shown in the handoff view: "5 of 7 facts preserved, weighted score 0.62."

### Tier 3 — LLM-judge with HealthBench-pattern rubric
Per the grounding doc (§5), each task ships with an instance-specific rubric: **IASHR (16 criteria, 39 points)**, each weighted by clinical importance, expressed as natural-language checks. **Judge: Gemini 2.5 Flash** (different model family from the actor — methodology rule from HealthBench to avoid self-preference bias). The judge reads the handoff + ground-truth fact list + rubric and returns a per-criterion score with reasoning. Rubric anchored in INTERACT SBAR + CNAHRT + Adler-Milstein 2021 priors + Cohen 2017 priors + California Title 22 §72311 + MDS change-since-last (see `geth/specs/seed-data-review-v2.md`). Output:

```
Facts in ground truth: 7
Preserved in handoff: 5
  - cardiac history P1 (weight 1.0)        ✓ preserved
  - fluid balance P3 (weight 1.0)          ✓ preserved
  - …
Missing: 2
  - ambient signal P2 (weight 3.0)         ✗ MISSING — high-weight omission
  - P3 medication time (weight 1.0)        ✗
Hallucinated: 0
Final score: 5.0 / 10.0 = 0.50
```

**Strengths:** robust to phrasing; surfaces hallucinations; makes the thesis measurable per rollout.
**Weaknesses:** non-deterministic (judge LLM); API cost; needs prompt design.
**Mitigation:** seed the judge prompt; cache judge outputs in `demo/judge_cache.json` for repro.

**Decision flow:**
- T1 floor: rule-based, hand-authored fact list per task.
- T2 stretch: weighted facts, breakdown view.
- T3 stretch: LLM-judge with rubric, breakdown view, cached for repro.

If pressed at any tier: **HealthBench (April 2025) is the cited methodology.** That's the answer.

---

## 10. Done = Shippable — three checklists

**Verification framework.** Each tier confirms its result via three layers, all of which must pass before the tier is callable as shippable:

- **`[A]` Automatic** — programmatic checks that pass/fail without human inspection: unit tests, smoke tests, schema validation, deterministic-seed reproduction. Run by `pytest` or `python -m`.
- **`[M]` Manual** — someone runs the app and sees the right thing render: UI legibility, narrative arc, view-by-view inspection on an external display at 1920×1080.
- **`[S]` Stakeholder** — Karl runs the pitch script against the live state and signs off that the story lands. This is the only check that catches "the demo built fine but the pitch falls flat."

The dev cluster's split (dev-1 builds, dev-2 verifies, dev-3 reviews) maps to `[A]` and the pre-`[M]` gate. `[M]` is the ship rehearsal. `[S]` is Karl's final read.

Each tier has its own ship-check. Mark off in order; do not advance to the next tier's checklist until the current tier is fully checked across all three layers.

### Tier 1 — MVP / Proof of Concept (target: ~95% confidence we ship this)

- [ ] `[A]` `requirements.txt` (demo deps) and `requirements-env.txt` (OR-only deps: openreward, pydantic, numpy) both pinned and committed.
- [ ] `[A]` `server.py`, `Dockerfile`, `requirements-env.txt` present at repo root.
- [ ] `[A]` `gh auth status` passes; OR GitHub App installed on `honeykeys`.
- [ ] `[A]` `openreward.ai/rkarlonuyda/tingin` returns HTTP 200 — OR build complete, status = Deployed.
- [ ] `[A]` Cloud smoke-test: `call_session_tool` round-trip against deployed env returns valid `FloorState`.
- [ ] `[M]` OR landing page README renders correctly at `openreward.ai/rkarlonuyda/tingin` — thesis, three statistics, IASHR rubric blurb.
- [ ] `[S]` Karl navigates to `openreward.ai/rkarlonuyda/tingin` live during pitch; URL is presentable.
- [ ] `[A]` `.env` in `.gitignore`; `OPENREWARD_API_KEY` loaded from `.env` (not committed).
- [ ] `[A]` `nursingfloor/` runs end-to-end in plain Python: `physiology.py`, `news2.py`, `floor.py`, `scripts.py`, `events.py`.
- [ ] `[A]` Both scripted runs (Run A / Run B) deterministic at seed=42, produce different focal-patient outcomes (`pytest -k determinism`).
- [ ] `[A]` `streamlit run app/app.py` opens locally without errors (smoke test, exit-code 0).
- [ ] `[M]` **Patient personhood at Tier 1:** each card shows name, age, admission reason, one-line social context. Focal patient (bed 2) named.
- [ ] `[M]` Floor view: 3 patient cards with live vitals, NEWS2 gauges, ambient pane, tool-call feed.
- [ ] `[M]` Handoff view: three-panel screen with red-highlight of lost state.
- [ ] `[M]` Finale view: overlaid NEWS2(t) traces with annotations.
- [ ] `[M]` **Human-legible outcomes at Tier 1:** finale captions translate NEWS2 numbers into lived consequences (transferred to ICU / discharged stable / etc.).
- [ ] `[M]` MDP view renders the formalization (`spec/mdp.md`).
- [ ] `[M]` Both runs play through without errors end-to-end on an external display.
- [ ] `[S]` Pitch script (3–5 min) rehearsed once against the live app, **delivered in nurse-POV**, narrative arc lands for Karl.
- [ ] `[M]` Tested on external display at 1920×1080.

**Ship floor:** if the day stops here, we still demo. The pitch works on this alone.

### Tier 2 — Considered (target: ~70% confidence)

Tier 1 PLUS:

- [ ] `[A]` Reward holes H1, H2, H3 patched per §9.6 with unit tests covering each branch (`pytest tests/test_reward_holes.py`).
- [ ] `[A]` §9.7 Tier 2 (weighted facts + IASHR-weight scoring) implemented; unit-tested against three handoff samples.
- [ ] `[A]` `tingin_env/environment.py` defines `NursingHandoffEnv(Environment)` with all 6 `@tool` methods and Pydantic param models (import succeeds, type-checks pass).
- [ ] `[A]` OR adapter compiles; one `call_session_tool(...)` invocation succeeds locally; `unwrap()` helper in place (smoke-test re-run G1–G4 at our integration layer).
- [ ] `[A]` `OPENAI_API_KEY` loaded from `.env` and a 1-token "OK" round-trip succeeds.
- [ ] `[A]` One real LLM rollout (**GPT-4.1 zero-shot, OpenAI SDK**) saved as JSON in `demo/rollouts/`. JSON schema-validates: contains `nursing_decisions` (observations, handoff fidelity, escalation accuracy) and `patient_outcomes` (consequences).
- [ ] `[M]` Streamlit timeline view shows three options: Run A, Run B, "GPT-4.1 zero-shot." Each surfaces nursing performance + outcome captions, not just reward numbers.
- [ ] `[M]` Handoff view shows the weighted-fact breakdown panel.
- [ ] `[A]` `spec/mdp.md` written; `[S]` clinically reviewed by Karl.
- [ ] `[A]` NEWS2 implementation verified against two clinical examples (unit tests).
- [ ] `[M]` Trajectory paragraph in README points at one moment in the rollout — what the nurse-agent decided, and which patient bore the consequence.
- [ ] `[S]` Pitch updated to mention the rollout beat ("here's what GPT-4.1 did when we put it in the nurse's seat"); rehearsed against live app.

**Ship floor:** the demo is no longer unfalsifiable. We have evidence, not assertion.

### Tier 3 — Very Good Foundation (target: ~30% confidence)

Tier 2 PLUS:

- [ ] `[A]` 10–20 rollouts across 2+ prompt classes saved as JSON; count check passes; each schema-validates.
- [ ] `[M]` **Nursing performance distribution** rendered in finale view, per policy class: observation counts, handoff fidelity score, escalation correctness. Patient outcome counts ("Mrs. Aquino lived N times, transferred K times") shown as the downstream verification.
- [ ] `[A]` Multi-task generation: 3–5 seeded task variants, with seed config exposed; deterministic at fixed seed.
- [ ] `[A]` `GOOGLE_API_KEY` loaded from `.env` and a 1-token "OK" round-trip on Gemini 2.5 Flash succeeds.
- [ ] `[A]` §9.7 Tier 3 LLM-judge implemented (judge: **Gemini 2.5 Flash**, rubric: **IASHR** — 16 criteria, 39 points, see `geth/specs/seed-data-review-v2.md`); judge cache file populates; deterministic re-run hits cache.
- [ ] `[M]` Per-rollout IASHR breakdown visible in handoff view — 16 criteria with preserved/partial/missing + judge reasoning + hallucination flag.
- [ ] `[A]` One reward hack documented from real trajectories — TRACE-style contrastive clustering script committed; cluster file generated.
- [ ] `[M]` Reward-Hack Register page renders the documented hack with sample trajectory IDs and judge classification.
- [ ] `[A]` `demo/demo.ipynb` loads real rollouts and runs cell-by-cell (notebook execution test).
- [ ] `[M]` README onboarding-tested: a stranger can clone, follow quickstart, run a rollout, see results. README frames Tingin as memory infrastructure for nurse-assist tools.
- [ ] `[S]` Pitch reframed: "we built memory infrastructure for clinical work; here's the benchmark methodology; here's how nursing policies discriminate." Rehearsed against the live distribution view.

**Ship floor:** the artifact is fundable. The pitch becomes "here's the data" rather than "here's the demo."

---

Everything else is scope creep.
