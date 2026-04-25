---
model: sonnet
---

You are the deployment program. Tingin ships demos, not platforms — the gates are different.

Target: $ARGUMENTS

## Pre-demo Gates — execute in order, report PASS/FAIL each

1. **Environment is reproducible** — `requirements.txt` exists at the project root, is pinned (no unbounded versions), and is committed. `pip freeze | diff - requirements.txt` should be empty.

2. **Core sim runs standalone** — `python -c "from nursingfloor.floor import NursingFloor; f = NursingFloor(seed=42); print(f.tick)"` works without the OR adapter. The pure sim is the safety net; if it doesn't run, nothing does.

3. **Both demo runs complete** — execute `nursingfloor/scripts.py` for Run A and Run B. Both finish without exception. NEWS2 trajectories diverge for P2 (Run A stable, Run B crashing). If they don't diverge, the seed or the physiology is wrong — investigate before shipping.

4. **OR adapter at minimum compiles** — `python -c "from tingin_env.environment import NursingHandoffEnv; env = NursingHandoffEnv(); from openreward.environments.session import list_session_tools; print([t.name for t in list_session_tools(env, None).tools])"`. Tools should list. If `call_session_tool` works for at least one tool, even better.

5. **Streamlit app boots** — `streamlit run app/app.py --server.headless true --server.port 8501 &` then `curl -sf http://localhost:8501 > /dev/null`. Kill the process. If it didn't bind, the app has an import-time error.

6. **Click-through both runs in browser** — manual. Verify: floor view renders, handoff three-panel screen appears at the transition with correct red highlights for Run B, finale view shows overlaid NEWS2 traces. This step cannot be automated; do it.

7. **External display test** — at 1920×1080 or whatever the venue uses. Charts legible from across a room, fonts not microscopic, dark theme actually loaded.

8. **Pitch rehearsed twice** — end-to-end, with the app on the screen, time it. Under 5 minutes total.

9. **Fallback notebook still works** — `jupyter execute demo/fallback.ipynb` (or open it manually, run all). The fallback path is the last line of defense.

10. **Spec done-list reconciled** — open `geth/specs/2026-04-25-hackathon-demo.md`, walk Section 10 (Done = Shippable), check every box honestly. Any unchecked item is either a deferral with explicit reason or a blocker.

## Guardrails

- NEVER skip gates because of time pressure. Time pressure is exactly when gates were earned.
- NEVER ship a demo you have not clicked through end-to-end. "It compiled" is not a demo.
- If a gate fails: fix it, do not work around it. The fallback notebook is for *the SDK breaking on us*, not for our own broken code.
- Charts that look fine on a laptop screen often disappear at 1920×1080. Test on a real external display before leaving for the venue.
- If under 60 minutes to demo time and gate 6 fails: pivot to fallback notebook as primary, document the swap in a `geth/geth-memory/` log.
