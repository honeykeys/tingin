# 2026-04-25 — Interface — Build Complete Handoff

**Date:** 2026-04-25 (hackathon day, final session)
**Program:** interface (orchestrator)
**Body:** Tingin
**Outcome:** Full Tier 1+2 shipped, Tier 3 scaffolded and partially live. Presentation delivered. App running locally. OR deployed.

---

## State

- **Branch:** main
- **Uncommitted files:** 7 batch rollout JSONs in `demo/rollouts/` (6 policy-variant rollouts + batch_summary.json) — these are data artifacts, not committed by design (large JSON, local only)
- **Last commit:** `13f9c30 fix: deck slide state persists when navigating to demo and back`
- **OR deployment:** `c85a497a completed` on `13f9c30d` — live at `openreward.ai/rkarlonuyda/tingin`
- **Local app:** `streamlit run app/app.py --server.port 8501` (may not be running; restart with `/rundev`)

---

## Done

### Full implementation built this session

**Backend sim (`nursingfloor/`):**
- `physiology.py` — Markov chains per archetype (stable, slow_det, acute), treatment mechanic (furosemide reverses det_progress for narrative)
- `news2.py` — full NEWS2 scoring algorithm, verified against 2 Mrs. Aquino-anchored clinical examples
- `floor.py` — NursingFloor state machine, 6 MDP actions, H2/H3 reward hole patches (novelty set + detection flags)
- `handoff.py` — IASHR-weighted Tier 1 scoring, 10-fact ground truth list
- `scripts.py` — Run A (good handoff, ambient preserved, P2 stable) + Run B (bad handoff, ambient missing, P2 deteriorates)
- `events.py` — event dataclasses for all floor actions
- `scorer_gemini.py` — Gemini 2.5 Flash IASHR judge (16 criteria, 39 pts), SHA-256 cache

**OR adapter (`tingin_env/`):**
- `contract.py` — all Pydantic v2 schemas at v1.2.0 (PatientProfile, ShiftState, HandoffRecord, ScoreResult, Rollout, FloorState, StepResult, etc.)
- `environment.py` — NursingHandoffEnv(Environment) with 4 OR tools (get_floor_state, step_shift, record_handoff, score_handoff)
- `util.py` — unwrap() and payload() helpers (G1 fix)

**Streamlit app (`app/`):**
- `app.py` — entry point, sidebar routing, session state, MockMode, GPT-4.1 rollout loading, Tier 3 policy selector
- `theme.py` — warm light mode Kintsugi palette (switched from dark mode at Karl's request), Google Fonts
- `runner.py` — run_scripted, build_news2_trace, get_tool_call_feed
- `views/floor.py` — 3-patient card grid, NEWS2 gauges, ambient pane, researcher badge, tool-call rail
- `views/handoff.py` — 3-panel killer screen, lost-fact red highlights, IASHR judge toggle (Gemini on demand), rollout variant support
- `views/timeline.py` — tool-call feed, nursing-decisions header strip, rollout JSON support
- `views/finale.py` — Plotly dual NEWS2(t) overlay, outcome captions, Tier 3 distribution section
- `views/mdp.py` — renders spec/mdp.md
- `views/deck.py` — **6-slide pitch deck** rendered in Streamlit: Title (+ product statement), Problem (3 stats), Why (mom photo), How (MDP structure + 3 hackathon criteria + technical strip), Results (outcome cards), Close (years/end-of-life + learning flywheel + reward hacking + infrastructure note)
- `views/hack_register.py` — Reward-Hack Register page, TRACE-style framing, falls back to mock

**OR artifacts (root):**
- `server.py`, `Dockerfile`, `requirements-env.txt` — OR build artifacts
- `README.md` — OR landing page (thesis, 80%/70%/49.6% stats, IASHR rubric, tool list)

**Demo artifacts (`demo/`):**
- `rollout_gpt41.py` — generates single GPT-4.1 rollout (seed=42, 21 tool calls, 82% fidelity, P2 observed 3×, terminal NEWS2=1)
- `rollout_batch.py` — generates 6 rollouts across with_hint/without_hint policy classes (seeds 42/99/137)
- `rollouts/gpt41_seed42_t0.json` — committed Tier 2 rollout
- `rollouts/gpt41_seed{42,99,137}_{with,without}_hint.json` — local only, not committed
- `rollouts/batch_summary.json` — avg fidelity: with_hint=81.8%, without_hint=81.8%; P2 obs: with_hint=4.67×, without_hint=3.0×

**Tests (`tests/`):**
- 49/49 passing across: test_contract, test_determinism, test_fixtures, test_news2_clinical, test_or_adapter, test_sim_narrative, test_gemini_judge

**Spec artifacts:**
- `spec/mdp.md` — MDP one-pager (State, Action, Observation, Transition, Reward)
- `spec/pitch-script.md` — full 4-minute rehearsal script with navigation cheat sheet and 9 Q&A answers

---

## Pending

1. **Deploy Streamlit app publicly** — Karl wants the app hosted somewhere so the next agent can work on it. Options: Streamlit Community Cloud (free, connects to GitHub), Hugging Face Spaces, or a simple VPS. Streamlit Cloud is the path of least resistance — repo is already public at `honeykeys/tingin`.

2. **Commit batch rollouts** — the 6 policy-variant rollouts + batch_summary.json are local only. Next agent should decide whether to commit them (they're ~60KB total, reasonable).

3. **Tier 3 distribution view needs data** — `_render_distribution_section()` in finale.py renders the policy comparison when `batch_summary.json` exists. It's on disk locally but not committed. Commit the batch summary to make this live in the app.

4. **IASHR handoff breakdown UX** — the "Run IASHR judge" button works but Gemini calls are slow (~10s). Could pre-cache the scores for the scripted runs.

5. **Reward hack register with real data** — currently falls back to mock. Real hacked rollouts from the batch (without_hint policy class) may qualify — needs clustering pass.

6. **YC deck** — referenced in deck design doc §1.2. Separate artifact, not built. May 4 deadline mentioned in project memory.

---

## Corrections absorbed

1. **Dark mode → light mode** — Karl doesn't like dark mode. Switched to warm light Kintsugi palette. Future sessions: default to light mode.
2. **"Weeks of care" is wrong** — long-term SNF residents stay for YEARS until end of life. Slide 6 and pitch script corrected. Mr. Goldberg is the named example. Never say "weeks."
3. **Hackathon criteria (Long Horizon, Capability Tangent, Hard but Tractable)** — must be addressed explicitly in the presentation. Belong on Slide 4 (How), not Slide 6. Karl identified these as completely missing from the original pitch.
4. **Product framing missing** — "how does this help the nurse" was absent. Added to Slide 1: "The nurse can't hold everything. The RL agent learns what gets forgotten, what that costs, and what to surface next time."
5. **Reward hacking must be explicit** — judges specifically look for trajectory analysis and quality filtering. Added concrete H2 example (doc_obs_spam, 42% fidelity, ICU) with TRACE clustering detection and novelty-set fix to Slide 6.

---

## Context files (read these first)

1. `geth/specs/2026-04-25-hackathon-demo.md` — the full spec; §10 ship-checks are the authoritative done criteria
2. `app/views/deck.py` — the presentation app (6 slides); most active file for any further presentation work
3. `spec/pitch-script.md` — full pitch script with Q&A; read before any pitch-adjacent work
4. `geth/specs/2026-04-25-fe-be-contract.md` — contract v1.2.0; read before any schema changes
5. `demo/rollout_batch.py` — if running more rollouts or extending Tier 3

---

## Next steps

1. **Deploy to Streamlit Community Cloud:**
   - Go to `share.streamlit.io`, connect `honeykeys/tingin`, set main file to `app/app.py`
   - Add secrets: `OPENREWARD_API_KEY`, `OPENAI_API_KEY`, `GOOGLE_API_KEY` in the Streamlit secrets manager
   - The app will run in MockMode for the sim (no API keys needed for the demo), but the IASHR judge button needs `GOOGLE_API_KEY`
   - Note: `assets/` photos (mom, Karl) are gitignored — they won't appear on the hosted version. Either commit them (Karl's call) or handle gracefully in deck.py (already has fallback)

2. **Commit batch rollouts** so the Tier 3 distribution section renders on any machine:
   ```
   git add demo/rollouts/ && git commit -m "data: Tier 3 batch rollouts (6 policy-variant GPT-4.1 runs)"
   ```

3. **If continuing Tier 3:** run `demo/rollout_batch.py` to regenerate if needed, then wire the clustering pass to produce real hack classifications for the register.

4. **Photos for Streamlit Cloud:** the `assets/` directory is gitignored (correct — personal photos). For the cloud deployment, the deck.py photo slides will show a placeholder. Karl can decide whether to commit the photos to the private repo branch or accept the placeholder.
