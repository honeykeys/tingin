# 2026-04-25 — Interface — Deploy and Polish

**Date:** 2026-04-25 (hackathon day, final session)
**Program:** interface
**Body:** Tingin
**Outcome:** Streamlit Community Cloud deployed. OR landing page fully dressed for judges. Repo metadata set. Session closed clean.

---

## HANDOFF

**Branch:** main
**Last commit:** `65cab3d docs: scrub em dashes and LLM writing patterns from README`
**Pending:**
- `assets/` photos (mom + Karl) are gitignored and did not appear on Streamlit Cloud. Karl is fine with the placeholder. If he wants them live: `git add assets/ && git commit && git push` — Streamlit redeploys automatically.
- YC deck referenced in spec §1.2. Separate artifact, not built. Mentioned as a May 2026 deliverable.
- Reward hack register still shows synthetic fixture (real data requires IRB-approved SNF access). Flagged explicitly in the UI.

**Next steps:** No immediate build work. If continuing, either commit the photos or start the YC deck.
**Context files:**
- `geth/geth-memory/2026-04-25-interface-build-complete.md` — full build state
- `README.md` — OR landing page (the primary judging surface)
- `spec/pitch-script.md` — pitch script with Q&A
- `app/views/deck.py` — 6-slide pitch deck
**Recommended program:** pitch (if YC deck), interface (if general continuation)

---

## Context

Picked up from the build-complete handoff. The app was running locally and the OR was deployed. Karl wanted the Streamlit app live publicly so judges could see it.

---

## What Was Done

### Streamlit Community Cloud deployment
- Karl deployed manually at share.streamlit.io (browser extension not connected for automation)
- Repo: `honeykeys/tingin`, main file: `app/app.py`
- Confirmed: app runs in MockMode for the sim without any API keys. Only `GOOGLE_API_KEY` needed for the live IASHR judge button. `OPENAI_API_KEY` and `OPENREWARD_API_KEY` are not needed at runtime (OpenAI used only in local rollout generation scripts; OR SDK imported but not called at runtime).
- Live at: https://tingin-3y89vgew36f9ttyiouu8ft.streamlit.app/

### GitHub repo metadata
- Description set: "RL environment for nursing handoff intelligence. Memory infrastructure for clinical work."
- Homepage set to Streamlit URL (shows as globe icon on repo page)
- Both set via `gh repo edit`

### README / OR landing page — five commits
1. **Streamlit link added** (`d1e61b7`) — Live Demo section with both Streamlit URL and OR environment URL
2. **Results + Hackathon Criteria sections** (`4363b59`) — GPT-4.1 rollout numbers (81.8% fidelity, 4.67 vs 3.0 P2 observation split), reward hack patches called out; Long Horizon / Capability Tangent / Hard but Tractable mapped explicitly
3. **How This Was Built section** (`0a43818`) — three-LLM roles (Claude builder, GPT-4.1 actor, Gemini judge), parallel build streams, collective intelligence framing
4. **Rename: Geth → collective intelligence** (`061bab2`) — Karl didn't want the internal name surfaced
5. **Em dash scrub + LLM pattern scrub** (`65cab3d`) — all em dashes replaced with colons/semicolons/periods/commas; removed tricolon summaries, rhetorical chiasmata, staccato fragment pairs, self-pointing phrases

### Hack register flag (`f4b6f33`)
- Replaced the silent mock caption with an `st.info` banner explaining the fixture is synthetic because real patient clustering data requires IRB-approved SNF access. Turned the gap into a credibility signal.

---

## Key Findings This Session

**On the results story:** fidelity was identical (81.8%) between with-hint and without-hint policy classes — potentially weak for a Tier 3 comparison story. But P2 observation count diverged (4.67 vs 3.0). Framed as the attention allocator result: the hint changes where the agent looks, not just what it reports. This is the stronger and more honest framing.

**On API keys for Streamlit Cloud:** none strictly required for the demo. GOOGLE_API_KEY gates only the live Gemini judge button. The rest of the app (sim, scripted runs, deck, timeline, finale, rollout loading) is self-contained.

**On photos:** `assets/` is intentionally gitignored (personal photos, public repo). The graceful fallback in deck.py means the slides render without crashing. Karl was fine with this.

---

## Corrections Absorbed

1. **Don't expose internal names publicly** — "Geth" was in the README; Karl asked it removed. "Collective intelligence as the builder" is the right framing for an external audience.
2. **Scrub LLM writing patterns** — em dashes are a tell. So are tricolon summaries ("Builder, actor, judge — each a different system"), rhetorical pairs ("The specialists built; the orchestrator held the line"), and staccato fragments ("Hundreds of handoffs. Thousands of decisions."). Karl caught all of them. Write like a human.

---

## State of Repo

All committed and pushed. Working tree clean. No stranded work.

```
README.md                          fully dressed OR landing page
app/views/hack_register.py         synthetic fixture flagged with IRB note
geth/geth-memory/                  this log + 3 prior session logs
```
