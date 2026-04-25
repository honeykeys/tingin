---
model: sonnet
---

Start the local development environment for Tingin.

## Execution

1. **Activate the venv** if not already active:
   ```
   source .venv/bin/activate
   ```
   If `.venv/` does not exist, run `uv venv --python 3.13` then `uv pip install -r requirements.txt` and stop to report — venv setup is not part of `/rundev`.

2. **Verify the OpenReward pin** before launching:
   ```
   pip freeze | grep openreward
   ```
   Must report `openreward==0.1.105` (or whatever `requirements.txt` pins). If it doesn't, do not launch — surface the drift.

3. **Launch the Streamlit app** (background process):
   ```
   streamlit run app/app.py --server.port 8501
   ```

4. **Wait for the URL to print** — typically `http://localhost:8501`. Report the URL.

5. **Smoke-check the app responds**: `curl -sf http://localhost:8501 > /dev/null`. If this fails the app didn't bind; check the streamlit output for import errors.

## Notes

- Streamlit auto-reloads on file changes for most edits. Some changes (new imports, decorator edits, `st.cache_*` invalidation) require a full restart — stop and rerun `streamlit run`.
- The OR adapter (`tingin_env/`) is NOT loaded by the Streamlit app on the demo path. Streamlit talks to `nursingfloor/` directly. The OR adapter is a separate notebook/script for proving the env class shape.
- For external-display rehearsal, set `--server.address 0.0.0.0` and access from another device on the same network — useful for testing how the app looks on a projector or larger screen before the venue.

## Guardrails

- Do not start the app on a port other than 8501 unless asked — Karl's bookmarks and rehearsal muscle memory live there.
- If a previous Streamlit instance is still running on 8501 (`lsof -ti:8501`), kill it first. Two instances on the same port = silent failure on launch.
