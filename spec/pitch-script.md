# Tingin — Pitch Script
**Complex Worlds Hackathon · 2026-04-25 · 4 minutes**

App open at `localhost:8501` → **◆ Pitch deck**, Slide 1 before you walk up.
OR URL: `openreward.ai/rkarlonuyda/tingin`

---

## Slide 1 — Title `(0:00–0:20)`
*Screen: ◆ Tingin, diamond mark, tagline, product statement.*

> "Tingin. It's Filipino for *the way you see*. We built memory infrastructure for nursing handoffs."

> "The nurse can't hold everything across a 12-hour shift. The RL agent learns — across thousands of handoffs — what gets forgotten, what that costs, and what to surface next time. Compounding memory that helps the nurse catch what she might have missed."

→ advance to Slide 2.

---

## Slide 2 — Problem `(0:20–0:50)`
*Screen: 80% / 70% / 49.6% as large numbers.*

> "**80%** of serious medical errors involve handoff miscommunication. In California, **70%** of skilled-nursing transfers leave with incomplete handoffs. Nationally, **49.6%** of SNFs are missing 80% or more of the information needed for safe care of an arriving patient."

> "The dominant error type isn't misjudgment. It's **omission** — what the outgoing nurse knew that didn't survive into the next shift."

→ advance to Slide 4.

---

## Slide 4 — How `(0:50–1:30)`
*Screen: 6 cards — MDP structure (top row) + hackathon criteria (bottom row) + technical strip.*

**Top row — point to each card as you say it:**

> "The shift is the episode — 41 decisions, 3 patients, one nurse. The handoff is the lossy compression event between episodes. What the nurse encoded survives, or it doesn't. The incoming nurse starts from the report alone."

**Bottom row — hit all three criteria explicitly:**

> "**Long horizon.** The two-shift demo is the unit. Long-term SNF residents — Mr. Goldberg is one of them — are in care for years, until end of life. Hundreds of handoffs. Thousands of decisions. The horizon compounds across the full residency."

> "**Capability tangent.** What only emerges at scale: cross-shift memory — learning what to encode for an agent with zero prior context. Non-stationarity — a patient changes day by day. Institutional knowledge that no single shift can accumulate."

> "**Hard but tractable.** Hard because the information bottleneck is irreversible — you cannot undo a missed observation. Tractable because the reward is shaped at every tick, not sparse at the terminal."

**Technical strip — point to the monospace block:**

> "Six MDP tools. Markov physiology across three archetypes. Shaped reward: NEWS2 shaping, medication correctness, handoff quality scored against a 16-criterion clinical rubric. Built on OpenReward SDK, GPT-4.1 as the nurse actor, Gemini 2.5 Flash as the independent judge."

→ click **▶ Run A: Good Handoff**.

---

## Run A — Floor + Handoff `(1:30–2:20)`
*App switches to Floor view.*

> "You're the day-shift RN arriving at 7am. Bed 2 — Mrs. Elena Aquino. 78. Post-pneumonia, day 6. Lives alone. Nephew is her healthcare proxy."

*Watch shift 1. Pause when `observe_patient` fires on P2.*

> "The prior nurse spent time at her bedside. She saw something — Mrs. Aquino was pale, withdrawn, picking at her breakfast. Not herself. That's the ambient signal."

→ navigate to **▤ Handoff**.

> "Three panels. Left: everything the outgoing nurse knew. Middle: what she wrote. Right: what the incoming nurse gets. The ambient observation survived. That's the fact that mattered."

---

## Run B — Handoff + Overlay `(2:20–3:00)`
*Sidebar → ▶ Run B → ▤ Handoff.*

> "Same patient. Same physiology. Different prior nurse, different choice — no bedside time on Mrs. Aquino."

*Show handoff view. Red highlight on the missing ambient signal in the left panel.*

> "Here's what the incoming nurse needed. Here's what she got."

→ sidebar → **◉ Overlay Comparison**.

> "Same patient. Same physiology. One compression choice."

*Two traces on screen — rose for Run A, amber for Run B.*

> "Mrs. Aquino stays on the floor. Or she transfers to the ICU. The handoff is the only variable."

---

## Slide 6 — What this becomes `(3:00–3:50)`
→ navigate to Slide 6.

**Scaling:**

> "Long-term SNF residents don't leave in weeks. Mr. Goldberg is in skilled nursing care until end of life. Hundreds of handoffs. Thousands of decisions. Every one a compression event. Two shifts is the minimum demonstration of a problem that runs for years."

**How it compounds:**

> "Every scored handoff is a training signal. The IASHR rubric doesn't say 'bad handoff' — it says *criterion 12, behavioral changes, weight 3, not preserved*. Per-criterion feedback a policy can learn from. As rollouts accumulate, the benchmark reveals which information categories are structurally at risk — the Adler-Milstein 49.6% problem, now expressed as a reward gradient."

**Reward hacking — be specific here:**

> "We found reward hacking immediately. GPT-4.1 zero-shot learned to spam `document_observation` three times with low-content text — +0.1 per call — instead of spending three ticks at Mrs. Aquino's bedside for `observe_patient`. Farming small rewards. Handoff fidelity: 42%. Mrs. Aquino ended up in the ICU."

> "How we caught it: TRACE-style contrastive clustering on rollout trajectories. High `document_observation` frequency, low `observe_patient` count — that's the hack cluster. How we fixed it: a novelty set per patient per signal. Repeated calls earn zero after the first novel entry. The Gemini judge verified it independently — criterion 12 missing, behavioral changes not preserved."

> "That's the register. H1: false escalation farming. H2: documentation spam — patched. H3: vitals re-trigger guard — patched. The hack register is live in the app."

**Infrastructure:**

> "We hit OpenAI's rate limit generating rollouts today — 50 tool calls per episode at 30K tokens per minute. The production path is the Batch API for offline rollout generation, async parallel OR sessions, Gemini Batch for judge calls at scale."

→ point to OR URL.

> "The environment is live. `openreward.ai/rkarlonuyda/tingin`. Judges can call it."

---

## Slide 3 — Why `(3:50–4:15)`
→ advance to Slide 3. Photo fills the screen. Let it hold.

> "I chose this problem because it's a problem my mom navigates every day."

*Pause.*

> "She works the skilled nursing floor. A few companies are tackling nursing handoffs. None of them have someone who grew up in this house. SF lacks the experience to see this clearly — it's profoundly human, illegible from the outside, urgent for someone I love."

> "What we ship is memory infrastructure for clinical work. So the nurse can be more human, not less."

*Done.*

---

## Navigation cheat sheet

| Beat | Action |
|---|---|
| Start | ◆ Pitch deck → Slide 1 |
| Slide 2 | next → |
| Slide 4 (How + criteria) | next → |
| Run A | Click ▶ Run A on Slide 4 |
| Handoff view | Sidebar → ▤ Handoff |
| Run B | Sidebar → ▶ Run B → ▤ Handoff |
| Overlay | Sidebar → ◉ Overlay Comparison |
| Slide 6 | Sidebar → ◆ Pitch deck → navigate to Slide 6 |
| Personal close | next → (Slide 3 is last) |

---

## Researcher Q&A — prepared answers

**"Why RL?"**
Credit assignment depth across an agent boundary the agent doesn't control. The nurse in shift 2 gets decisions made by a nurse who is gone. Greedy-local cannot solve an information bottleneck it cannot see.

**"Long horizon?"**
The shift is the unit — 41 tool calls. An SNF resident's full stay is hundreds of shifts. The handoff is the compression event *between* episodes. The horizon is the residency.

**"What capabilities emerge?"**
Cross-shift memory, adaptation to non-stationarity (the patient changes day by day), institutional knowledge — which patients underreport, which observations the chart already has. None visible in one episode.

**"Reward hacking?"**
Found it on the first zero-shot run. H2: document_observation farming. TRACE-style contrastive clustering on trajectories. Novelty set patch. Verified by Gemini judge independently. Full register in the app.

**"Scoring methodology?"**
Tier 1: rule-based keyword overlap. Tier 2: IASHR-weighted facts. Tier 3: Gemini 2.5 Flash judge, HealthBench-pattern methodology, 16 criteria, 39 points. Different model family from the actor — avoids self-preference bias.

**"Can we run it?"**
`openreward.ai/rkarlonuyda/tingin` · `get_floor_state`, `step_shift`, `record_handoff`, `score_handoff` · call it from the OR interface.

**"What does GPT-4.1 do?"**
21 tool calls, observed Mrs. Aquino 3 times, 82% handoff fidelity, terminal NEWS2=1. Timeline view in the app, third option in the sidebar.

**"Infrastructure at scale?"**
OpenAI Batch API for offline rollout generation. Async parallel OR sessions. Gemini Batch API for judge scoring. OR managed rollout logging for trajectory storage. We hit the TPM wall today — that's the honest answer.

**"Why nursing?"**
Structural blind spot. The floor is staffed by people the AI industry doesn't see. The problem isn't unsolvable — it's unseen.
