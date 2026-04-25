# OpenReward — Reference

External documentation reference. Pinned to **`openreward==0.1.105`** (the version in `requirements.txt`).

Our self-description lives in `understanding.md`. Session notes live in `memory.md`. This file is for SDK truth — what the package actually does, what bit us, and the code patterns we use.

---

## 0. TL;DR for build

| Question | Answer |
|---|---|
| What package? | `openreward==0.1.105` (not `ors-sdk`) |
| Imports | `from openreward.environments import Environment, tool, ToolOutput, TextBlock` |
| Server? | **No.** We use local sessions (`call_session_tool`) — no HTTP server needed for the demo |
| Async? | Yes. `call_session_tool` returns a coroutine despite a sync-looking signature |
| Streamlit? | Read `NursingFloor` directly. OR adapter is a **sibling** to the app, not inside it |
| Version of source-read doc | Vivi's `~/Desktop/Vivi/context/openreward_platform.md` documents **v0.1.94** — schemas may have shifted at 0.1.105. Smoke-test below was run against 0.1.105 |

---

## 1. Smoke-test learnings (G1–G4) — THE NON-OBVIOUS PARTS

These are folded into the spec at section 9.5, but they live here as the canonical engineering reference. **Read these before writing tool code.** Discovered T-1 (2026-04-24).

### G1 — `RunToolOutput` is a wrapper, not your tool's return value

When you call `call_session_tool(...)`, you get back a wrapper object:

```python
RunToolOutput(root=RunToolSuccess(ok=True, output=ToolOutput(...)))
```

So `result.finished` is `None`. The real value is at `result.root.output.finished`. There's also a `RunToolError` variant for failures.

**Always unwrap.** Ship this helper once and use it everywhere:

```python
def unwrap(rto):
    """Unwrap RunToolOutput → ToolOutput, raising on error."""
    if rto.root.ok:
        return rto.root.output
    raise RuntimeError(f"tool error: {rto.root.error}")
```

Suggested home: `tingin_env/util.py`.

### G2 — `call_session_tool` is async despite a sync-looking signature

The signature reads `call_session_tool(env, toolset, name, input) -> RunToolOutput`. No visible `async`. But it returns a coroutine — you must `await` it.

**Streamlit is sync.** Two options:

- **(a) [our choice]** The Streamlit app reads `NursingFloor` directly. The OR adapter runs in a separate notebook/script — proves env-class shape for Ross, doesn't run inside the demo's hot path.
- (b) Wrap each call in `asyncio.run(...)`. Creates a new loop per call — fine for a demo, bad for real loads.

(a) matches the spec's posture. Stick with it unless something forces a change.

### G3 — No top-level `__version__`

```python
import openreward
openreward.__version__   # AttributeError
openreward._version.__version__   # → "0.1.105"
```

Cosmetic, but a tell about packaging maturity. If you need version checks at runtime, hit `_version`.

### G4 — Streamlit `AppTest.run()` defaults to a 3-second timeout

This is unsafe for any app that imports pandas/plotly cold. First-ever invocation in a fresh venv took ~2–4s on this machine, just over 3s. Once OS file caches are warm, runs are <0.5s.

**If you add headless integration tests, always pass `timeout=15` to `.run()`.**

For the live demo (`streamlit run app/app.py`), this does not apply — the server boots once and stays warm.

### What works (confirmed at 0.1.105)

- ✅ `Environment` subclass + `@tool` decorator from `openreward.environments`
- ✅ Tool registration via `list_session_tools(env, None)`
- ✅ Local session via `await call_session_tool(env, None, name, input)` — **no server needed**
- ✅ State sticky on env instance across calls (e.g. `env.tick` mutates correctly)
- ✅ Terminal `finished=True` flows through to `RunToolSuccess.output.finished`
- ✅ Streamlit 1.56 + Python 3.13 + plotly + pandas all install cleanly via `uv`

---

## 2. Two packages — which to use

There are two packages, separable like HTTP-vs-Apache:

| Package | What it is | Used here? |
|---|---|---|
| `ors-sdk` v0.1.0 | The open standard. Apache 2.0. Run-anywhere. `from ors import Environment, ...` | No |
| `openreward` v0.1.105 (pinned) | Commercial client built on ORS. Adds managed hosting, rollout logging, sandboxes, CLI. `from openreward.environments import Environment, ...` | **Yes** |

Use `openreward`. The hackathon is theirs. The `Environment` class is identical to `ors-sdk`'s — same `@tool`, `ToolOutput`, `TextBlock` pattern. Only the import path differs.

---

## 3. Minimal environment pattern

Copy-paste skeleton. Fill in tool methods. Class name lowercases for URL routing if you serve it (`MyEnvironment` → `/myenvironment/call`).

```python
from pydantic import BaseModel
from openreward.environments import Environment, tool, ToolOutput, TextBlock, Split


class CheckVitalsParams(BaseModel):
    patient_id: str


class NursingHandoffEnv(Environment):

    @classmethod
    def list_splits(cls):
        return [
            Split(name="train", type="train"),
            Split(name="test", type="test"),
        ]

    @classmethod
    def list_tasks(cls, split: str):
        # Returns list of dicts. Structure is ours to define.
        return [
            {"id": "0", "seed": 42, "archetype_p2": "slow_det", ...},
        ]

    def get_prompt(self):
        # self.task_spec is set by `create`. Available here and in tools.
        return [TextBlock(text="You are RN on shift 1. Census: ...")]

    @tool
    def check_vitals(self, params: CheckVitalsParams) -> ToolOutput:
        """Read vital signs for a single patient at the bedside."""
        # ... query NursingFloor state ...
        return ToolOutput(
            blocks=[TextBlock(text="HR 92, RR 22, SpO2 94, BP 118/76, T 37.4")],
            reward=0.0,
            finished=False,
        )
```

Rules baked in by the SDK:

- `list_splits` and `list_tasks` are **classmethods** — no instance state available
- `get_prompt` is an **instance method** — `self.task_spec` is available (set by `create`)
- Every `@tool` is an instance method — `self.task_spec` available, plus you can store state on `self`
- Tool methods must return `ToolOutput`
- If a tool takes a parameter, it must be a `pydantic.BaseModel` — schema auto-generated via `model_json_schema()`
- Tool description comes from the docstring
- `finished=True` on any tool call ends the episode

---

## 4. Local session pattern (no server)

This is how we run the env in `demo/demo.ipynb` and in tests. **No HTTP server, no FastAPI process.**

```python
import asyncio
from openreward.environments import list_session_tools, call_session_tool
from tingin_env.environment import NursingHandoffEnv

env = NursingHandoffEnv(task_spec={"id": "0", "seed": 42, ...})

# Discover tools registered on this env instance
tools = list_session_tools(env, None)
# → list of tool descriptors (name, schema, description)

# Call a tool. NOTE: this is async (G2).
async def run():
    rto = await call_session_tool(
        env,
        None,                                 # toolset (None = env-only)
        "check_vitals",                        # tool name
        {"patient_id": "P2"},                  # input dict
    )
    output = unwrap(rto)                       # G1
    print(output.blocks[0].text, output.reward, output.finished)

asyncio.run(run())
```

State is sticky on the `env` instance across calls. `env.tick` (or whatever we name it) mutates between tool calls — this is confirmed.

---

## 5. The four primitives

| Primitive | Definition | Tingin's instance |
|---|---|---|
| **Tools** | Decorated methods returning `ToolOutput`. Actions the agent can take. | `check_vitals`, `observe_patient`, `administer_medication`, `document_observation`, `write_handoff`, `read_handoff` |
| **Tasks** | JSON dicts. Structure is yours to define. | `{"id": ..., "seed": ..., "archetype_p2": ..., "shift_length": 20}` |
| **Splits** | Named groups of tasks (train / validation / test). | At minimum `train` + `test`. We may not use them today. |
| **Prompts** | Initial instructions delivered via `get_prompt()`. | Shift briefing + initial census + role assignment ("you are RN, shift 1"). |

Episodes = sessions:

1. Create session → get session ID
2. Bind task to session
3. `get_prompt` → agent receives initial state
4. Tool calls → agent receives `(blocks, reward, finished)` per call
5. Loop until `finished=True`
6. Delete session → cleanup (or for local: just drop the env reference)

---

## 6. `ToolOutput` schema

```python
ToolOutput(
    blocks: Sequence[TextBlock | ImageBlock],   # what the agent sees
    metadata: Optional[dict] = None,             # arbitrary, not RL-visible
    reward: Optional[float] = None,              # RL signal
    finished: bool = False,                       # episode termination
)

TextBlock(text: str, detail: Optional[dict] = None)
ImageBlock(data: str, mimeType: str, detail: Optional[dict] = None)
Split(name: str, type: Literal["train", "validation", "test"])
```

**Design taste:** TextBlock content is the agent's perceptual field. Vitals should read like a bedside assessment, not a JSON dump. Observations should carry the qualitative ("she just didn't look right") next to the quantitative. Rich enough to learn from, structured enough to parse.

---

## 7. Reward design — patterns

Per-tool reward goes in `ToolOutput.reward`. Three shapes:

**Sparse** (terminal only):
```python
return ToolOutput(blocks=[...], reward=1.0, finished=True)   # success
return ToolOutput(blocks=[...], reward=0.0, finished=True)   # failure
```

**Dense** (every step + terminal):
```python
return ToolOutput(blocks=[...], reward=0.05, finished=False)  # intermediate
return ToolOutput(blocks=[...], reward=1.0,  finished=True)   # terminal
```

**Shaped** — guide toward solution with progress signals. Useful for long-horizon. **This is what we're doing.**

Tingin's reward stack (from spec §2):

| When | Signal | Magnitude |
|---|---|---|
| `check_vitals` | NEWS2 catch correctness | +0.5 / -1.0 |
| `administer_medication` | Med correctness | +0.2 |
| `document_observation` | Doc quality | +0.1 |
| `write_handoff` (terminal shift1) | Handoff quality `q ∈ [0,1]` × 2.0 | up to +2.0 |
| Shift 2 outcome (terminal) | Patient-by-patient | +1.0 stable / -2.0 NEWS2 ≥ 7 |

Synthesis-by-Receiver bonus is **CUT** for the demo (spec §4).

---

## 8. What we're NOT using

The `openreward` client has a lot. Most of it is irrelevant for the demo. Quick map so we don't get distracted:

| Feature | Use it? | Why |
|---|---|---|
| `Server.run()` HTTP serving | No | Local sessions cover the demo |
| Rollout API (`client.rollout.create`) | No (today) | Useful for hosted demo visibility, requires `OPENREWARD_API_KEY`, off-path |
| Sandbox API | No | We're pure Python, no code execution |
| `orwd` CLI scaffolding | No | We have the spec |
| Pre-built toolsets (`claude_code`, `excel`, …) | No | None match nursing |
| Provider format conversion (`session.list_tools(format="anthropic")`) | **Maybe** | If we run Level-1 LLM rollouts, this saves tool-schema work |
| Managed hosting | No | Local-only per spec §4 |

---

## 9. Server architecture (if anyone asks)

We're not running the server, but judges may probe.

- FastAPI app with SSE streaming for tool calls
- Session reaping: stale sessions (no ping for 900s = 15 min) auto-deleted
- SSE reconnect: tool calls stream via SSE with 4096-byte chunks and task IDs for resumability
- Async-first under the hood; sync wrappers run their own event loop
- Structured logging via `structlog`

HTTP control plane (for reference, not used by us):

```
GET  /list_environments          → list available envs
GET  /{env}/tools                → list tools + schemas
GET  /{env}/splits               → list splits
POST /{env}/tasks                → list tasks for a split
POST /create_session             → returns session_id (SSE)
POST /create                     → bind task to session (X-Session-ID header)
GET  /{env}/prompt               → initial prompt for current episode
POST /{env}/call                 → call a tool (X-Session-ID header), SSE response
POST /delete                     → end session
```

---

## 10. Tool introspection (how `@tool` works internally)

The `@tool` decorator sets `_env_tool = True` on the function. `list_tools()` introspects the class at startup:

- Function must return `ToolOutput`
- If it takes a parameter, the parameter must be a `pydantic.BaseModel`
- Schema auto-generated from the BaseModel via `model_json_schema()`
- Description comes from the docstring

`@tool(shared=False)` marks a tool as task-specific (not in global list, only in `/task_tools`). We probably don't need this; all six Tingin tools are shared across tasks.

Toolset variant (we don't use this either):

```python
class MyToolset(Toolset):
    def __init__(self, env):
        self.env = env

    @tool
    def my_tool(self, params: MyParams) -> ToolOutput:
        return ToolOutput(...)

class MyEnv(Environment):
    toolsets = [MyToolset]   # ClassVar
```

---

## 11. ORS vs MCP

Adjacent question, in case it comes up:

- **MCP** — general tool access for agents. No rewards, no episode structure.
- **ORS** — RL training environments. Rewards, episode termination, task splits.

Complementary, not competing. An agent in an ORS env *can* use MCP tools to access external resources while operating in the RL loop. Doesn't apply to us (pure Python sim, no external resources needed).

---

## 12. Sources

| Source | URL | Date |
|---|---|---|
| Vivi's full source-read | `~/Desktop/Vivi/context/openreward_platform.md` | 2026-04-12 |
| Tingin smoke-test (G1–G4) | `geth/specs/2026-04-25-hackathon-demo.md` §9.5 | 2026-04-24 |
| OpenReward announcement | https://www.gr.inc/releases/introducing-openreward | 2026-03-24 |
| OpenReward platform | https://openreward.ai/ | live |
| ORS spec | https://openrewardstandard.io/ | live |
| ORS Quickstart | https://openrewardstandard.io/quickstart | live |
| `openreward` PyPI | https://pypi.org/project/openreward/ | pinned 0.1.105 |
| `ors-sdk` PyPI | https://pypi.org/project/ors-sdk/ | not used |
| ORS GitHub | https://github.com/openreward/ors-sdk | reference |
| OpenReward Cookbook | https://github.com/OpenRewardAI/openreward-cookbook | thin (29 ⭐, README-only) |

If you need to verify something against a live source, hit the docs site or `pip show openreward` first. If a behavior contradicts this file, **update this file** and note the discrepancy in `memory.md`.
