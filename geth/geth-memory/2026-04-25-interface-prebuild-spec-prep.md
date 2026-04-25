# 2026-04-25 — Interface — Pre-Build Spec Preparation

**Date:** 2026-04-25 (T, hackathon day)
**Program:** interface (acting as session coordinator; no specialist program spun up yet)
**Body:** Tingin
**Outcome:** Spec finalized end-to-end. Build has not started. Karl flagged a data-integrity concern as the first task for the next session.

---

## ⚡ FIRST TASK ON RESUME — Data Integrity Check

**Karl has concerns about the seed data we audited this session.** He has not yet articulated them. On resume:

1. Open `geth/specs/seed-data-review.md` and re-read it cold.
2. Ask Karl to articulate the specific concerns. Examples to probe if he doesn't volunteer: Galli xlsx license absence? Suominen ND clause blocking sample shipment? The reconstructed-from-headers HEF rubric (not pulled from the published paper)? The pre/post n asymmetry (526 vs 341)? The Italian-only language?
3. Ground the concerns against the spec's reliance on each dataset:
   - **Galli HEF rubric** is the anchor for Tier 3 LLM-judge scoring (`§9.7 Tier 3`, grounding §5)
   - **Suominen** is cited in grounding §6 but not used in build
   - **ISOBAR MDS** anchors the canonical handover-fields list (cited in grounding §6, used as field structure reference)
4. Decide whether any spec changes are needed before build kicks off. If concerns are about citation accuracy, the fix is in `geth/specs/seed-data-review.md` and `geth/specs/2026-04-25-grounding.md`. If concerns are about whether we *should* use this data at all, the fix is in `geth/specs/2026-04-25-hackathon-demo.md` §9.7 Tier 3 (we may need a fallback rubric source).

Do not start the build until Karl signs off on the data integrity check.

---

## What we were doing

Karl came into the session with the spec already drafted (Prime session, T-1, 2026-04-24) and the smoke-test already completed against `openreward==0.1.105`. The hackathon was today. Build had not started — zero implementation code. The session goal was: ground the spec, finalize tier structure, lock model selection, audit framing — *before* any code lands.

## What we did

In rough chronological order (the conversation was non-linear; this is the structural summary):

### 1. Verified tooling and explored panel signals
- Confirmed EXA MCP access live (Exa status page reports Search API / Websets / Exa MCP all operational).
- Karl shared notes from a hackathon panel talk. He was unfamiliar with RL terminology. I decoded each panel beat and mapped it to where Tingin sat (§grounding doc §1, §quick-reference table). Karl pushed back on three things:
  - Don't claim "long horizon" head-on (KellyBench is 500–900 tool calls; ours is 41) — but he later corrected my reframe (see "corrections absorbed" below).
  - "I don't train an agent — do they want us to train an agent?" — clarified the spectrum (scripted policy → zero-shot LLM → fine-tune); Tier 2 = Level 1 (zero-shot LLM), Tier 4 = Level 3 (fine-tune; out of scope today).
  - "We need something deeper than that" — produced the channel-mediated-coordination framing (3 nested RL properties: information bottleneck across agents + time-budgeted exploration + verifiable terminal reward).

### 2. Built `geth/programs/openreward/reference.md`
External SDK truth. Frontloaded smoke-test findings G1–G4 (RunToolOutput wrapper, async-despite-sync signature, no top-level `__version__`, Streamlit AppTest 3s timeout). Documented the local-session path (no HTTP server needed for the demo). Mapped what we use vs. don't use from the `openreward` package.

### 3. Three-tier goal structure (Karl's call)
Karl pushed back on my proposal to cut the dev cluster: "LLMs (you) have an optimism problem with their own code." The dev cluster (dev-1 build / dev-2 verify / dev-3 review) is the architectural defense, not overhead. He also flagged that LLM-assisted estimation is broken — variance is too high for hour-based planning. Result: **plan in shippable tiers, not in hours.**

Three tiers with explicit confidence:
- T1 MVP (~95%): polished demo of an env design with two scripted nursing policies.
- T2 Considered (~70%): real RL env with one observed LLM-as-nurse rollout.
- T3 Very Good Foundation (~30%): benchmark for training nurse-assist tools, distribution analysis, reward-hack writeup.

Tier transitions are state-based, not time-based. If a tier fails its ship-check, reinforce don't advance.

### 4. EXA grounding pass
Six parallel searches, results condensed into `geth/specs/2026-04-25-grounding.md` (212 lines, 8 sections):
- §1 RL env design principles (Gymnasium / MIKASA / Meta-World v2 / OGBench)
- §2 Channel-mediated multi-agent prior art (iAgents, SMACv2 EPO, IMAC) — novelty claim holds
- §3 Long horizon — choose the right unit (later corrected per Karl's note)
- §4 Reward-hack methodology — TRACE contrastive clustering, PCH
- §5 LLM-judge — HealthBench pattern (the gold standard)
- §6 Nursing seed datasets — Suominen, Galli, ISOBAR
- §7 OpenReward ecosystem — KellyBench is 500–900 tool calls, version 0.1.106 shipped overnight (we hold at 0.1.105)
- §8 Quick-reference Q&A table for pitch

### 5. Spec restructure
Spec rewritten end-to-end into three-tier structure. New sections: §0 (tier overview), §4 (scope-by-tier), §9.6 (Reward Hack Register), §9.7 (Handoff Scoring Decision). §10 split into three checklists. §9 execution order is now tier-gated. Smoke-test §8 labeled completed with outcome.

### 6. Sanity check + scan
Found and fixed (with Karl's review): `fallback.ipynb` referenced in 4 places after being cut, "Palantir but for Nurses" still in pitch close, "long-horizon multi-agent" framing that loses to KellyBench, plus several medium-priority alignment issues.

### 7. Karl's corrections — absorbed (see below for memory entries)
Three corrections this session:
- Long-horizon claims need the right unit (patient-stay, not shift)
- The tool helps the NURSE (patient outcomes are scoring/verification, not the focus)
- Tingin's core thesis: memory infrastructure that lets the human be more human, not less

### 8. Pitch personal-why
Karl drafted his "big why" — mom is a nurse, picture of him and her, "what does SF not know" → SF lacks experience with this kind of profoundly human, illegible-from-outside problem. I offered tightenings (he can take or ignore) and a sharper alternative (also optional). Final wording is his.

### 9. Seed data — fetch and quality check
Spawned an Explore agent (general-purpose) to fetch and inspect three datasets:
- **Galli 2025** (github.com/alessiagalli/Database-Galli-et-al.) — usable. The repo is just an Excel file (n=867, 526 pre / 341 post), no raw transcripts, but the column headers ARE the validated 15-point HEF rubric in Italian. Translated and tabulated. **No LICENSE file — flag.**
- **Suominen 2017** — confirmed structure (3×~101 records), CC BY-NC-ND 4.0, **cannot ship samples**. Citation only.
- **ISOBAR MDS** — Royal Hobart Hospital 2008 PDF pulled. Got the canonical 5-step minimum data set verbatim. iSoBAR acronym from companion Porteous 2009 paper.

Report at `geth/specs/seed-data-review.md`. Karl confirmed audit was sufficient for the hackathon. **Then he flagged concerns** — unarticulated as of session end. That's the next session's opening task.

### 10. Model selection
Locked: **Combo A — GPT-4.1 actor + Gemini 2.5 Pro judge.** Karl has GPT credits, doesn't have GPT-5 tier access. Gemini 2.5 Pro picked for judge (different model family from actor satisfies the HealthBench self-preference rule, free tier covers volume). `OPENREWARD_API_KEY` already in `.env`; `OPENAI_API_KEY` and `GOOGLE_API_KEY` to be added when Karl sets them up.

### 11. "Intelligible at Tier 1" — patient personhood + outcome captions + nurse-POV
Karl's call: at Tier 1, the demo must make legible *how does this help a real nurse and a real patient*. Translated into:
- Patient cards show name, age, admission reason, social context (Mrs. Reyes 84, Mrs. Aquino 78 focal, Mr. Goldberg 91)
- Outcome captions translate NEWS2 numbers ("Rapid response called; transferred to ICU; 30-day mortality ~15-20%")
- Pitch §6 steps 3+4 delivered in first-person nurse POV

### 12. Nurse-as-protagonist correction
Karl flagged that I drifted into patient-as-protagonist when extending personhood through Tier 2/3. The tool helps the **nurse**; patient outcomes are scoring/verification. I reverted the patient-protagonist Tier 2 bullet and replaced it with a nursing-performance bullet. Then audited the whole spec for protagonist drift. Fixed: §0 defensible-as descriptions, §2 MDP opening line, §3 contract, §4 Tier 3 distribution, §5 App Flow throughout, §9 T1.5 nursing-perf check, §9.7 handoff-as-encoding-output framing, §10 Tier 2/3 checklists. Plus purged stale "Claude Sonnet" model references → GPT-4.1.

### 13. The Soul — "Why This Exists"
Karl delivered the project's core thesis: nursing is deeply human; in SNF/hospice care humanity matters most; **memory infrastructure that lets the human be more human, not less.** SF builds AI to replace; we build AI to free. Added a new "Why This Exists" section at the top of the spec (between metadata and §0). This is now the first thing any reader (or any sub-agent reading for context) sees. Updated §6 step 6 to surface the memory-infrastructure framing at the "why this matters" beat.

### 14. Cosmetic finishes
- §9.6 hacks now framed as nursing-policy failure modes (nurse-agent throughout)
- §1 patient names committed (Mrs. Aquino as focal — cultural resonance is intentional)
- §6 step 7 close has Karl's original draft + sharper alternative, both clearly marked as his voice / his choice

---

## State of artifacts

```
geth/specs/
  2026-04-25-hackathon-demo.md     563 lines, three-tier structure, nurse-protagonist
  2026-04-25-grounding.md          212 lines, 8 sections, EXA citations
  seed-data-review.md              371 lines, three sources audited

geth/programs/openreward/
  reference.md                     357 lines, smoke-test findings + SDK truth
  understanding.md, memory.md, relationships.md  unchanged

geth/programs/{architect, clinical, dev-1, dev-2, dev-3, interface, llm-layer, openreward, pitch, research, rl-specialist, simulation}/
  understanding.md, memory.md, relationships.md  scaffolded but mostly unchanged this session

requirements.txt                   pinned to openreward==0.1.105 (0.1.106 shipped overnight, holding)

.scratch/seed-data/                gitignored; raw downloads from Explore agent
  galli-2025/                      cloned repo + xlsx
  RHH_2008_isobar_sop.pdf, .txt    canonical fields source
  st-john-wa-2020-isobar.pdf, .txt worked example
  suominen-csiro-20413-meta.json   metadata only (ND clause blocks samples)

NO IMPLEMENTATION CODE EXISTS. No nursingfloor/, no app/, no tingin_env/, no demo/.
```

---

## What the next Geth needs to know

### About the build
- **Build has not started.** §9 Tier 1 sequence (T1.1 architect → T1.10 dev-1 MDP view) is the planned execution order. First step is `architect` drawing module boundaries.
- Spec is finalized. Don't redesign without Karl's say-so.
- All three tiers have ship-checks in §10. Treat each as a hard gate.
- The dev cluster (dev-1/dev-2/dev-3) is non-negotiable — it's the LLM-optimism check, not overhead.

### About the framing
- **Tingin's core thesis is in `~/.claude/projects/-Users-karlnuyda-Desktop-Tingin/memory/project_tingin_thesis.md` and at the top of the spec.** Read it first. Memory infrastructure that lets the human be more human, not less.
- The nurse is the protagonist throughout. Patient personhood is context for the nurse's work; patient outcomes are scoring. Don't drift.
- Long horizon = patient-stay (weeks of SNF care, dozens of handoffs), not 41 tool calls per shift.
- Karl's mom is a nurse. This is personal, not academic.
- Karl's voice on the close is his — don't overwrite his draft.

### About model selection
- Actor: **GPT-4.1, OpenAI SDK, zero-shot.** (Karl doesn't have GPT-5 access.)
- Judge: **Gemini 2.5 Pro, Google GenAI SDK.** Different family from actor — methodology rule from HealthBench.
- Keys: `OPENREWARD_API_KEY` already in `.env`; `OPENAI_API_KEY` + `GOOGLE_API_KEY` to be added when Karl provisions them.
- `.env` must be in `.gitignore` before any commit.

### About SDK gotchas
- Pinned at `openreward==0.1.105`. Do not bump on demo day. Smoke-test (G1–G4) was against this version.
- G1: `RunToolOutput` is a wrapper — use `unwrap()` helper.
- G2: `call_session_tool` is async despite sync-looking signature — keep OR adapter out of Streamlit's hot path.
- G3: `openreward.__version__` raises; real path is `openreward._version.__version__`.
- G4: Streamlit `AppTest.run()` defaults to 3s — use `timeout=15` for headless tests.
- See `geth/programs/openreward/reference.md` for full reference.

### About the immediate next task
- **Data integrity check first.** See top of this file. Karl has concerns; he hasn't articulated them. Ask.
- Don't start `architect` until that's resolved.

---

## Corrections absorbed this session

Saved as user-level memory entries (visible across sessions in this body):

1. **`feedback_llm_optimism_dev_cluster.md`** — don't cut the Geth dev cluster under time pressure; LLMs are over-confident about their own code. Plan in tiers, not hours.
2. **`feedback_horizon_unit.md`** — for Tingin, "long horizon" means patient-stay scale (weeks, dozens of shifts), not tool-calls-per-shift. Shift = episode, stay = horizon, handoff = compression event between.
3. **`feedback_tool_helps_the_nurse.md`** — Tingin's user is the nurse. Patient outcomes are scoring/verification. Lead Tier framing with what the nurse gains from the tool.
4. **`project_tingin_thesis.md`** — memory infrastructure that lets the human be more human, not less. SF builds AI to replace; we build AI to free. The SNF/hospice context makes the humanity of the caregiver the value being delivered.

Index: `~/.claude/projects/-Users-karlnuyda-Desktop-Tingin/memory/MEMORY.md`.

---

## Open questions parked

(Things Karl might raise on resume; pre-loaded so the next instance isn't starting cold.)

- **Patient names** — committed in spec but Karl can override. Mrs. Aquino as focal patient is the only one with intentional cultural resonance.
- **Pitch close wording** — Karl's draft + my sharper alternative both in §6 step 7. He picks before pitch.
- **`architect` program understanding.md** — has not been read this session. Next instance should read it before T1.1.
- **Dev cluster member specialization** — DIRECTORY.md says dev-1/dev-2/dev-3 are sonnet, others are opus. The next instance spawning sub-agents should respect this.
- **Tier 3 LLM-judge rubric** — anchored in Galli HEF, but Galli's repo has no LICENSE. May need to cite the Menditto 2025 paper directly rather than the xlsx headers. Part of Karl's data integrity concern, possibly.

---

## Session metadata

- Spec line counts at session end: hackathon-demo.md 563 lines, grounding.md 212 lines, openreward/reference.md 357 lines, seed-data-review.md 371 lines.
- Memory entries added: 4 (3 feedback + 1 project).
- Sub-agents spawned: 1 (Explore agent for seed-data fetch — already completed).
- No code committed this session.
- Karl was alert and pushing back well throughout — corrections were sharp and the spec is stronger for them.
