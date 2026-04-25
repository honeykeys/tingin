# Tingin — Pitch Script
**Complex Worlds Hackathon · 2026-04-25 · 3–5 minutes**

App: `localhost:8501` → open to **◆ Pitch deck**, Slide 1.
OR URL live: `openreward.ai/rkarlonuyda/tingin`

---

## Slide 1 — Title `(0:00–0:30)`
*Screen: Tingin wordmark, pink diamond, tagline*

> "Tingin. It's Filipino for *the way you see*. We built memory infrastructure for nursing handoffs."

*Advance to Slide 2.*

---

## Slide 2 — Problem `(0:30–1:00)`
*Screen: 80% / 70% / 49.6% as large display numbers*

> "**80%** of serious medical errors involve handoff miscommunication — Joint Commission. In California, **70%** of skilled-nursing transfers leave with incomplete handoffs. Nationally, **49.6%** of SNFs are missing 80% or more of the information needed for safe care of an arriving patient."

> "The dominant error type isn't misjudgment. It's **omission** — what the outgoing nurse knew that didn't survive into the next shift."

*Advance to Slide 4 (How) — skip Why for now, come back at the close.*

---

## Slide 4 — How `(1:00–1:30)`
*Screen: 6 cards. Top row = MDP structure. Bottom row = hackathon criteria.*

**Address the three criteria here, before the demo. Point to each bottom card.**

> "The shift is the episode. ~41 decisions. The handoff is the compression event between episodes — one encoding, one channel, everything lost is gone."

> "**Long horizon.** The two-shift demo is the unit. Long-term SNF residents — Mr. Goldberg is one of them — are in care for years, until end of life. Hundreds of handoffs. Thousands of decisions. The horizon compounds across the full residency."

> "**Capability tangent.** What only emerges at scale: cross-shift memory, adaptation to non-stationarity as a patient's condition changes day by day, institutional knowledge that no single shift can accumulate."

> "**Hard but tractable.** Hard because the information bottleneck is irreversible — you cannot undo a missed observation. Tractable because the reward is shaped, not sparse."

*Click **▶ Run A: Good Handoff**. App switches to Floor view.*

## Slide 4 — Run A `(1:30–2:30)`

> "You're the day-shift RN arriving at 7am. Three patients. Your shift is 20 ticks."

> "Bed 2 — Mrs. Elena Aquino. 78. Post-pneumonia, day 6. Lives alone. Her nephew is her healthcare proxy."

*Watch shift 1 play through. Pause briefly when `observe_patient` fires on P2.*

> "The prior nurse spent time at her bedside. She saw something — Mrs. Aquino was pale, withdrawn, picking at her breakfast. Not herself."

*Navigate to Handoff view.*

> "Here's the handoff moment. Three panels. Left: everything the outgoing nurse knew. Middle: what she wrote. Right: what the incoming nurse gets."

> "The ambient observation survived. That's the fact that matters."

*Navigate to Finale — or click Slide 5.*

---

## Slide 5 — Results / Run B `(2:30–3:15)`
*Click **▶ Run B: Bad Handoff**. Switch to Handoff view.*

> "Same patient. Same physiology. Different prior nurse, different choice."

*Show the handoff view — the left panel has the red highlight on the missing ambient signal.*

> "Here's what you needed. Here's what you got. The ambient observation isn't there."

*Navigate to Finale — Overlay Comparison.*

> "Same patient. Same physiology. One compression choice."

*Two traces on screen — Run A in rose, Run B in amber.*

> "Mrs. Aquino stays on the floor. Or she transfers to the ICU with a 15–20% 30-day mortality. The handoff is the only variable."

---

## Slide 6 — Close `(3:45–4:00)`
*Navigate to Slide 6.*

> "Long-term SNF residents don't leave in weeks. Mr. Goldberg is in skilled nursing care until end of life. Hundreds of handoffs. Thousands of decisions. Every one a compression event."

> "Two shifts is the minimum demonstration. The benchmark extends naturally — and the 1-in-4 readmission rate is where the cost of those thousands of decisions lives."

*Point to OR URL.*

> "It's live. `openreward.ai/rkarlonuyda/tingin`. Judges can call it."

---

## Slide 3 — Why / Personal close `(3:45–4:30)`
*Navigate to Slide 3. Photo fills the screen.*

> "I chose this problem because it's a problem my mom navigates every day."

*Pause. Let the photo hold.*

> "She works the skilled nursing floor. What survives the handoff and what doesn't is what she navigates every shift."

> "A few companies are tackling nursing handoffs. None of them have someone who grew up in this house. SF lacks the experience to see this clearly — it's profoundly human, illegible from the outside, urgent for someone I love."

> "That's why we built Tingin. Memory infrastructure for clinical work — so the nurse can be more human, not less."

*Done.*

---

## Navigation cheat sheet

| Beat | App action |
|---|---|
| Open | Sidebar → ◆ Pitch deck → Slide 1 |
| Run A | Slide 4 → ▶ Run A → Floor view auto-loads |
| Handoff moment | Sidebar → ▤ Handoff |
| Run B | Sidebar → ▶ Run B → then ▤ Handoff |
| Overlay | Sidebar → ◉ Overlay Comparison → Finale |
| OR URL | Slide 6 shows it; navigate live to openreward.ai/rkarlonuyda/tingin |
| Personal close | Sidebar → ◆ Pitch deck → Slide 3 |

## If the projector dies
Pre-recorded fallback: take screenshots of Floor view (tick 12), Handoff view for Run A and Run B, and the Finale overlay before you leave. Keep them on your desktop. The deck slides 4 and 5 host the screenshots as backdrops.

## Researcher Q&A hooks
- **"Why RL?"** — credit assignment across an agent boundary; greedy-local can't solve an information bottleneck it can't see
- **"How is the reward function verified?"** — 46 automated tests including clinical NEWS2 examples anchored to Mrs. Aquino's actual vitals; H1/H2/H3 reward holes documented in the hack register
- **"What's the scoring methodology?"** — Tier 1: rule-based keyword overlap. Tier 2: IASHR-weighted facts. Tier 3: Gemini 2.5 Flash judge against the 16-criterion INTERACT-Anchored SNF Handoff Rubric (HealthBench-pattern methodology)
- **"Can we run it?"** — `openreward.ai/rkarlonuyda/tingin` · 4 tools · call `get_floor_state`, then `step_shift` with NurseAction
- **"What does GPT-4.1 do?"** — Timeline view, third option. 21 tool calls, 82% handoff fidelity, observed Mrs. Aquino 3×, terminal NEWS2=1
- **"Why nursing?"** — structural blind spot: the floor is staffed by people the AI industry doesn't see. Filipino, predominantly female, disproportionately immigrant. The problem isn't unsolvable — it's unseen.
