# 2026-04-25 — Interface — Build Handoff

**Date:** 2026-04-25 (hackathon day, continuing)
**Program:** interface (session coordinator)
**Body:** Tingin
**Outcome:** All pre-build work complete. Zero implementation code. Ready to build.

---

## ⚡ RESUME PROMPT

You are the orchestrator for the Tingin hackathon build. Everything is specced and ready. Your job is to build it.

**First action:** Run T1.0 OR pre-flight (exact commands in `geth/specs/2026-04-25-hackathon-demo.md` §9). Then spawn BE and FE agents in parallel.

**New session + subagents pattern.** BE and FE run in parallel from contract v1.2.0. LLM stream activates at Tier 2 (after Tier 1 ships). You are the orchestrator — manage integration checkpoints and ship-checks.

---

## State

- **Branch:** main
- **Uncommitted files:** everything except the initial commit. All spec/program files are untracked (`.claude/`, `geth/`, `.scratch/`, `assets/`, `requirements.txt`, `.env`). No implementation code exists.
- **Last commit:** `2e67c0e initial commit — Tingin body bootstrapped`
- **Note:** `.env` contains live API keys — do not commit. It's gitignored per spec §3.

---

## Done

### Session 1 (prior session, 2026-04-24): Spec bootstrapped
- Three-tier goal structure, MDP formalization, architecture, pitch skeleton, risk register, smoke-test (completed), reward hack register, handoff scoring decision. Model selection: GPT-4.1 actor + Gemini 2.5 Flash judge.

### Session 2 (this session, 2026-04-25): Full pre-build grounding + spec hardening

**Data integrity overhaul:**
- Karl rejected Galli (Italian ED, wrong setting/market) and the entire prior seed-data stack.
- New California SNF anchor stack pulled and audited via Explore agent: INTERACT SBAR + Stop and Watch + Care Paths (FAU ©2011/2014), CNAHRT Appendix B (UNC DNP, CNA-specific), MDS 3.0 NC Comprehensive Item Set v1.14.0 (federal public domain), California Title 22 §§72327/72329.1/72329.2/72311/72315 + CDPH AFL 19-16, Adler-Milstein 2021 (CC-BY), Labovic 2018 CalVet 70% (California-local), Riesenberg 2012 (JC 80% + AHRQ 50%), BMC Nursing 2025 (n=688), Cohen/Abraham 2017 (RRI ρ=0.88). All on disk at `.scratch/seed-data/snf-ca/`.
- New review doc: `geth/specs/seed-data-review-v2.md` (847 lines). Supersedes `seed-data-review.md`.
- **IASHR rubric** (INTERACT-Anchored SNF Handoff Rubric): 16 criteria, 39 points, replaces Galli HEF everywhere.
- Stat fix: "88%" not reproducible. Replaced with JC 80% + Labovic 70% (CalVet, California-local) + Adler-Milstein 49.6%.

**Spec updates:**
- `geth/specs/2026-04-25-hackathon-demo.md`: stats polished; IASHR replaces Galli in §4/§9.7/§10; §5.5 App State by Tier added (explicit per-tier UI delta); §10 verification framework [A]/[M]/[S] + all checklists tagged; OR adapter promoted to Tier 1; T1.0 OR pre-flight added to §9; deck design doc referenced in §3/§6; public URL `openreward.ai/rkarlonuyda/tingin` threaded throughout.
- `geth/specs/2026-04-25-grounding.md`: §6 rewritten (CA SNF anchor stack replaces Galli/Suominen/ISOBAR table); §8 quick-ref updated.
- Gemini 2.5 Pro → 2.5 Flash everywhere (Pro was zero-quota; Flash is free-tier-eligible, demo-adequate).

**FE/BE contract:**
- `geth/specs/2026-04-25-fe-be-contract.md`: v1.2.0 (928+ lines). Schemas: PatientProfile, ShiftState, HandoffRecord, ScoreResult, Rollout (+ ToolCallTrace, PerPatientObservation, NursingDecisions, PatientOutcome, HackClassification). 4 tools: get_floor_state, step_shift, record_handoff, score_handoff. 8 mock fixtures for immediate FE scaffolding. Karl decided: `floor_snapshots: list[FloorState] | None` included in Rollout so FE stays a pure JSON renderer. All "for Ross" language replaced with public OR URL.

**Deck design:**
- `geth/specs/2026-04-25-deck-frontend-design.md` (Karl wrote in parallel): 6-slide deck structure, Kintsugi palette (bg-deep `#0E0908`, accent-rose `#F0A6B8`, etc.), typography (Fraunces/Newsreader/JetBrains Mono), per-view Streamlit rendering rules, asset registry. Authoritative for FE worker.

**API keys:**
- `.env` var names fixed: `OPENREWARD_API_KEY`, `OPENAI_API_KEY`, `GOOGLE_API_KEY`.
- OpenAI GPT-4.1: PASS.
- Google Gemini 2.5 Flash: PASS (key stored as `GOOGLE_API_KEY`).
- OpenReward: PASS (namespace `rkarlonuyda` confirmed via `orwd whoami`).

**OR publish path confirmed:**
- `orwd` CLI is in `.venv/bin/orwd`. Use `source .venv/bin/activate && source .env` before any `orwd` command.
- GitHub is authed as `honeykeys`. OR namespace is `rkarlonuyda`. These are different — `gh repo create honeykeys/tingin`, `orwd link honeykeys/tingin rkarlonuyda/tingin`.
- OR GitHub App install on `honeykeys` not yet verified — `orwd link` will print install URL if needed.
- First build: 2–10 min. Subsequent pushes auto-redeploy.

---

## Pending

1. **T1.0 OR pre-flight** — register env, create GitHub repo, link, first build.
2. **Tier 1 build** (three parallel streams after T1.0):
   - **BE:** `nursingfloor/` (sim), `tingin_env/contract.py` v1.2.0, `tingin_env/environment.py` (4 @tools), `server.py`, `Dockerfile`, `requirements-env.txt`, `README.md` (OR landing page)
   - **FE:** `app/` Streamlit — floor view, handoff view (the killer screen), timeline, finale, MDP view. Reads `deck-frontend-design.md` + contract mock fixtures.
   - **LLM:** parks until Tier 2
3. **Tier 1 ship-check** per §10 ([A]/[M]/[S]). OR public at `openreward.ai/rkarlonuyda/tingin`.
4. **Tier 2:** reward holes patched, one GPT-4.1 rollout, timeline view extended.
5. **Tier 3 (aspirational):** Gemini Flash judge, IASHR scoring, distributions, hack register.
6. **Pitch rehearsal** against live app + OR URL.
7. **Assets:** diamond SVG, Voronoi PNG, photo filenames renamed (see `deck-frontend-design.md` §5). Images are in `assets/` already but filename convention not applied.
8. **spec/mdp.md** — needs to be written (§9 T2.2), feeds the MDP view in the app.

---

## Corrections absorbed

1. **Galli is the wrong anchor** — Italian ED data doesn't represent the California SNF market. Always anchor to US/CA SNF sources. INTERACT + CNAHRT + MDS 3.0 + Title 22 is the right stack.
2. **SNF staffing model** — charge nurse + med RN/LVN + CNAs. Not just "nurse + nurse." CNA layer is the ambient observation surface (Stop and Watch). The nurse-as-protagonist framing extends to the staffing model.
3. **OR adapter is Tier 1, not secondary** — if the env isn't public on OR, judges can't verify the implementation. "The presentation is everything."
4. **Build in parallel** — FE/BE/LLM streams run concurrently against contract v1.2.0. FE/BE contract is the primary failure mode ("often gets broken"). Lock it first, then diverge.
5. **Handoffs don't take 20 minutes** — calibrate handoff depth to what's actually needed. Resume prompts should be crisp.

---

## Context files (read in this order before doing anything)

1. `geth/specs/2026-04-25-hackathon-demo.md` — the spec. §9 T1.0 has the exact OR pre-flight commands.
2. `geth/specs/2026-04-25-fe-be-contract.md` — contract v1.2.0. BE and FE both import from `tingin_env/contract.py`.
3. `geth/specs/2026-04-25-deck-frontend-design.md` — FE agent reads this alongside the contract.
4. `geth/programs/openreward/reference.md` — OR SDK gotchas G1–G4. BE + LLM agents read this.
5. `geth/specs/seed-data-review-v2.md` — IASHR rubric (§Tier 3 Rubric Proposal) + flow sheet schema + patient profile schema. BE agent reads for NursingFloor field shapes; LLM agent reads for rubric.

---

## Next steps

1. Read the 5 context files above.
2. Run T1.0 OR pre-flight (§9 commands). Confirm `openreward.ai/rkarlonuyda/tingin` is registered.
3. **Spawn BE and FE agents in parallel** (both Sonnet 4.6 for speed):
   - BE agent prompt: read spec §2/§3/§4/§9, contract v1.2.0, OR reference. Build `nursingfloor/` + `tingin_env/` + `server.py` + `Dockerfile` + `requirements-env.txt`. Write `README.md` for OR landing page (thesis, stats, IASHR blurb). Run `git push` when done so OR redeploys.
   - FE agent prompt: read spec §5/§5.5, contract v1.2.0 mock fixtures, `deck-frontend-design.md`. Build `app/` against mock fixtures (MockMode=True). Kintsugi palette, Fraunces/Newsreader/JetBrains Mono fonts, all 6 views per §3.x of deck doc.
4. Integration checkpoint: flip MockMode → False. Run `pytest tests/test_contract.py`. Both streams must pass before Tier 1 ship-check.
5. Tier 1 ship-check §10 (all [A]+[M]+[S]).
6. Activate LLM stream at Tier 2.
