# Tingin — Grounding Document

External citations supporting the hackathon demo spec. All findings retrieved 2026-04-25 via EXA. Cite from here when the pitch Q&A goes deep.

---

## 1. What "good" means for an RL environment (2025–2026 consensus)

Five design principles repeatedly invoked across recent benchmark papers (OGBench arxiv:2410.20092 §6, MIKASA NeurIPS 2025, Meta-World v2 arxiv:2505.11289, Gymnasium NeurIPS 2025):

1. **Realistic + exciting** — models real-world challenges, not contrived puzzles.
2. **Appropriate difficulty** — neither too easy nor too hard; *distinguishes between more and less effective methods*. The exact phrase the panel used.
3. **Controllable datasets** — tools to adjust task difficulty / dataset size for repro.
4. **Minimal compute** — focus on algorithmic challenges, not infrastructure cost.
5. **High code quality** — clean reference implementations, well-tuned, easy to set up.

Plus, from Meta-World v2 (arxiv:2505.11289): **explicit versioning, reward-function consistency, documentation of design decisions** are now considered table-stakes after years of irreproducibility incidents.

**Implication for Tingin:**
- Our scope-locked MVP satisfies (1), (2), (4), (5). 
- (3) is partly satisfied via seeded tasks; multi-task generation is Tier 3.
- Versioning: pin `openreward==0.1.105`, document smoke-test findings (G1–G4) in `geth/programs/openreward/reference.md`.

**Sources:**
- Gymnasium @ NeurIPS 2025 — https://neurips.cc/virtual/2025/poster/121446
- Robust-Gymnasium — https://arxiv.org/abs/2502.19652
- Meta-World v2 — https://arxiv.org/pdf/2505.11289
- OGBench — https://arxiv.org/pdf/2410.20092
- MIKASA — https://openreview.net/pdf/aca8a023e2ea071454ac04a88a14eee450e40138.pdf

---

## 2. Channel-mediated multi-agent coordination — prior art and novelty claim

### What exists

| Work | Property | Limitation vs. Tingin |
|---|---|---|
| **iAgents / InformativeBench** (arxiv:2406.14928, Feb 2026) | First benchmark for collaboration *under information asymmetry* in social networks. Best models 50.48% avg, hardest task 22.8%. | Asymmetry is *static* — different agents see different info. Tingin's asymmetry is *temporally enforced through compression*. |
| **SMACv2 EPO** (arxiv:2212.07489) | Extends SMAC with stochastically masked enemy observations — meaningful partial observability. | Spatial-only; agents act simultaneously. No channel between sequential actors. |
| **IMAC** (Wang et al., ICML 2020) | Information-bottleneck principle applied to multi-agent communication; agents learn low-entropy messages under bandwidth limits. | The bottleneck is on *learned message protocols*, not a structurally enforced lossy artifact. Agents are co-temporal. |
| **InfoBot / RL with Information Bottlenecks** | Tishby IB principle applied in RL for representation learning. | About internal compression, not inter-agent compression. |
| **Long-Horizon Multi-Turn RL** (arxiv:2510.24126) | Demonstrates RL on legal-document search; 14B model beats frontier 85 vs 78%. Endorses long horizons. | Single-agent. No cross-agent compression boundary. |

### Tingin's novelty claim

**Three properties co-occur in Tingin and in no prior benchmark:**

1. **Temporal separation between agents** — shift1 RN and shift2 RN never co-exist; they cannot query each other.
2. **Lossy artifact as the only channel** — a free-text handoff report compresses joint state.
3. **Verifiable terminal cost paid by a third party** — patient outcome (NEWS2, survival) is the ground-truth check, paid by neither agent.

The closest prior art (iAgents) tests asymmetric info in synchronous networks; Tingin tests asymmetric info induced by *enforced compression across time*. That's a different RL property.

### How to phrase this in the pitch

> "We're testing a property no current benchmark measures: agents separated by a channel they don't control, where the cost of what didn't survive the channel is paid by a third party. It's the structure of code review, on-call handoffs, doctor-to-doctor referrals. Nursing is just where the cost is most legible."

---

## 3. Long horizon — choose the right unit

KellyBench (General Reasoning's own benchmark, Grady et al. 2026) is **500–900 tool calls per episode**, $300M–500M tokens per seed. That's their unit of horizon.

Tingin is **41 tool calls per shift episode**. Comparing on tool-calls-per-episode loses head-to-head.

**But that's the wrong unit for Tingin.** The natural horizon is at the *patient-stay* scale, not the *shift* scale.

### The structural framing

| Unit | Tingin |
|---|---|
| **Episode** | One shift (~41 tool calls, ~12 hours of clinical time) |
| **Horizon** | Patient stay — dozens of shifts across weeks; in Skilled Nursing Facilities, sometimes hundreds of shifts across years |
| **Compression event** | The handoff between episodes — lossy by structure |
| **Cost accumulation** | Information lost at shift N is gone when shift N+14 needs it; omissions compound |

This is where the **1-in-4 Medicare SNF 30-day readmission rate** lives — institutional memory degrades across handoff chains, two-thirds of those readmissions are preventable, and the cost is paid by patients across weeks of care.

### How to phrase this in the pitch

> "KellyBench tests endurance within one trajectory. Tingin tests endurance across compression boundaries. Same underlying property — credit assignment over depth — different unit. We measure horizon in *episodes per patient*, connected by lossy compression at every shift boundary. Two shifts is the minimum demonstration of the structure. The benchmark scales naturally to a patient's full stay."

### Why the MVP is two shifts, not twelve

The minimum demonstration of the *structural* property — temporally separated agents + lossy compression channel + verifiable third-party cost — requires exactly two shifts and one handoff. Adding shifts 3..N compounds the same compression event repeatedly without adding new structure. For the pitch, two shifts is the cleanest demonstration; for a full benchmark, the natural extension is N shifts of compounding compression. That's a Tier 4+ (out of scope today) extension, not a hidden gap.

**Source:** KellyBench — https://openreward.ai/GeneralReasoning/KellyBench

---

## 4. Reward-hack analysis — methodology

### Published frameworks (2026)

- **TRACE** (arxiv:2601.20103) — 517 human-verified trajectories spanning 54 reward-hack subcategories in code environments. Defines **contrastive trajectory clustering**: give an evaluator LLM N trajectories (mix of benign + hacked), ask it to identify hacks. Cluster size N and benign-to-hack ratio B influence detection. **Direct citation for our trajectory analysis methodology.**

- **Reward Hacking Survey** (arxiv:2604.13602, April 2026) — proposes the *Proxy Compression Hypothesis*: reward hacking is the consequence of optimizing expressive policies against compressed reward representations. Lifecycle detection: training-time online monitoring → inference-time safeguards → post-hoc mechanistic auditing.

- **School of Reward Hacks** (arxiv:2508.17511, Aug 2025) — fine-tuning on harmless reward-hacking tasks generalizes to misaligned behavior. Caution against treating reward hacks as "interesting curiosities."

### Implication for Tingin

Tier 2: hand-trace one rollout, document one anticipated reward hack with our defense.

Tier 3: run 10–20 rollouts across two policy variants. Apply contrastive trajectory clustering — feed the clusters to a judge LLM, ask "which trajectories are reward-hacking the env?" Document findings.

**Sources:**
- TRACE — https://arxiv.org/pdf/2601.20103
- Reward Hacking survey — https://arxiv.org/abs/2604.13602
- School of Reward Hacks — https://arxiv.org/abs/2508.17511

---

## 5. LLM-as-judge for handoff scoring — HealthBench is the model

**HealthBench** (OpenAI, April 2025, arxiv:2505.08775): the gold standard for clinical free-text rubric evaluation.

| HealthBench property | Our application |
|---|---|
| 48,562 *physician-authored* criteria across 5,000 conversations | Tingin: 5–8 ground-truth facts per shift1 state (which patient has which ambient signal, which med is due, etc.) |
| Per-conversation **adaptive rubrics** — each scenario has bespoke rubric | Per-task rubric: each task seed has its own ground-truth fact-list |
| Each criterion **weighted by clinical importance** | Ambient signal preservation > med timing > general communication |
| Model-based grader **validated against physician judgment** | LLM-judge prompt with explicit rubric; we don't validate today (Tier 3 fast-follow) |
| Failure-mode-first design — ask "what is the worst thing this could do?" | Worst case: handoff omits ambient signal that would have saved P2. That is the criterion with highest weight. |

### Concrete scoring schema for Tingin

Per task, ground-truth state contains a fact list `F = {f_1, ..., f_n}`, each with weight `w_i`. The handoff `H` is scored:

```
score(H) = Σ_i w_i × [f_i ∈ H according to LLM-judge] - α × |hallucinated_facts(H)|
```

Per-rollout breakdown shown to the judge:

```
Facts in ground truth: 7
Preserved in handoff: 5  (cardiac history P1, fluid balance P3, ...)
Missing: 2               (ambient on P2 ⚠ HIGH-WEIGHT, P3 medication time)
Hallucinated: 0
Final score: 0.62
```

That breakdown is the thesis made measurable. It also sidesteps "is your reward function gameable?" by making the judge's reasoning visible.

**Decision for Tingin:**
- **Tier 1**: rule-based scoring — keyword overlap on a fixed fact list, fast and deterministic.
- **Tier 2**: same rule-based scoring, but with the fact-list authored from the ground-truth simulation state. Defensible.
- **Tier 3**: LLM-judge with explicit rubric, per-rollout breakdown, HealthBench pattern.

**Sources:**
- HealthBench paper — https://arxiv.org/pdf/2505.08775
- HealthBench rubric methodology overview — https://medium.com/@adnanmasood/rubric-based-evals-llm-as-a-judge-methodologies-and-empirical-validation-in-domain-context-71936b989e80
- LLM-as-judge guide — https://engineersofai.com/docs/ai-engineering/ai-evaluation/llm-as-judge

---

## 6. Nursing handoff seed data — what's public (California SNF anchor stack)

Tingin's environment is anchored on a stack of publicly-accessible US/California sources. Verbatim extractions, per-source license review, and the synthesized rubric are in `geth/specs/seed-data-review-v2.md`. The prior Italian-ED / Australian-synthetic / Australian-spec stack (Galli / Suominen / ISOBAR) was rejected as wrong setting and wrong market — the prior review remains at `geth/specs/seed-data-review.md` as historical record.

| Layer | Anchored on | License |
|---|---|---|
| **Patient profile schema** (slow-changing) | MDS 3.0 NC Comprehensive Item Set v1.14.0 — 18 sections A through Z | Federal public domain |
| **Per-shift flow-sheet schema** | Synthesized from INTERACT SBAR + CNAHRT Appendix B + Title 22 §72315 + MDS §H/§J/§K/§M | INTERACT FAU©2011 free for clinical use; CNAHRT open-access; Title 22 public |
| **Handoff field structure** | INTERACT SBAR (4 sections + 5 system-specific change-from-baseline blocks) + CNAHRT (9 sections, CNA-specific) | FAU©2011; UNC open-access |
| **Acute-change escalation surface** | INTERACT Stop and Watch (12 mnemonic items) + INTERACT Care Paths (10 conditions) | FAU©2011 / FAU©2014 |
| **Staffing model** | California Title 22 §§ 72327, 72329.1, 72329.2, 72311, 72315 + CDPH AFL 19-16 | Public state regulation |
| **Failure-mode prior** | Joint Commission **80%** (Riesenberg 2012); AHRQ **50%** (Riesenberg 2012); Adler-Milstein **49.6%** + **67.7%** behavioral missing (2021, n=471 hospital-SNF pairs); Labovic **70%** CalVet (2018, 84-bed); BMC Nursing 2025 **27.4%** (n=688) | Mixed (see v2) |
| **Tier 3 LLM-judge rubric (IASHR)** | 16 criteria, 39 points, anchored on INTERACT SBAR + CNAHRT + Adler-Milstein priors + Cohen 2017 priors + Title 22 §72311 + MDS change-since-last | Per-source license inherited |

**Pitch line:**
> "The environment is anchored in California-codified clinical reality. Patient state follows MDS 3.0 — the federal SNF assessment standard. Handoff structure follows INTERACT, the CMS-funded SNF toolkit from Florida Atlantic, and CNAHRT, the CNA-specific handoff tool from UNC. Staffing follows California Title 22 §§72329.1/2: charge RN plus med RN/LVN plus CNAs at 2.4 hours per patient day. Real handoff transcripts cannot be published under HIPAA — but the structure they would be filled into is real, codified, and California-specific."

**On the "88%" statistic:** the figure cited in early Tingin drafts does not reproduce in any peer-reviewed meta-analysis we located. The verifiable triangulated stack replaces it — Joint Commission 80%, Labovic 70% (California-local), Adler-Milstein 49.6% (US SNFs).

**Sources** (full review at `geth/specs/seed-data-review-v2.md`):
- INTERACT SBAR / Stop and Watch / QI Tool — `https://www.in.gov/health/files/INTERACT_SBAR_Form.pdf` (FAU ©2011 v3.0, Indiana DOH mirror)
- INTERACT v4.0 Implementation Guide — `https://www.adldata.org/wp-content/uploads/2015/07/INTERACT-V4-Implementation_Guide-Dec-10.pdf`
- CNAHRT — `https://cdr.lib.unc.edu/downloads/tm70n5089` (McDermott UNC DNP, 2021)
- MDS 3.0 NC Comprehensive Item Set v1.14.0 — `https://www.cms.gov/Medicare/Quality-Initiatives-Patient-Assessment-Instruments/NursingHomeQualityInits/Downloads/MDS30_NC_Comp_v1140.pdf`
- California Title 22 §§ 72327/72329.1/72329.2/72311/72315 — Cornell LII regulations
- CDPH AFL 19-16 — `https://www.cdph.ca.gov/Programs/CHCQ/LCP/CDPH%20Document%20Library/AFL-19-16.pdf`
- Adler-Milstein 2021 (CC-BY) — `https://pmc.ncbi.nlm.nih.gov/articles/PMC7809587/`
- Labovic 2018 CalVet — `https://repository.usfca.edu/capstone/747`
- Riesenberg 2012 (Joint Commission 80%, AHRQ 50%) — PMC3312531
- BMC Nursing 2025 (n=688) — `https://link.springer.com/article/10.1186/s12912-025-03802-6`
- Cohen / Abraham 2017 (RRI ρ=0.88; low-overlap categories empirically dropped most often) — `https://pubmed.ncbi.nlm.nih.gov/27913246/`

---

## 7. OpenReward / ORS ecosystem — current state

- **General Reasoning's own benchmarks** on the platform: DeepSynth (program synthesis, 1,353 train tasks, **5 difficulty tiers T=1..T=5**), BountyBench (cybersecurity, 138 tasks, binary verifiable rewards), KellyBench (sports betting, 500–900 tool calls/episode, full Premier League season, $300M+ tokens per seed).
- **Adoption beyond GR:** Meta's OpenEnv (PyTorch-affiliated) opened RFC #468 on 2026-03-26 to add ORS support — the standard is being adopted outside GR's own ecosystem.
- **Scale:** 200+ environments in EnvCommons, 330+ on OpenReward platform.
- **Latest version:** `openreward==0.1.106` shipped 2026-04-24 (one version drift from our pinned 0.1.105). Staying pinned for the demo.

### What this implies for Tingin's design choices

1. **Difficulty tiers** — DeepSynth does T=1..T=5. We cut ours; restore 2–3 tiers at Tier 3 to match the host's own pattern.
2. **Verifiable rewards** — DeepSynth and BountyBench are fully binary-verifiable. Tingin's reward stack is mixed (NEWS2 verifiable; handoff quality LLM-judge). Defend this: clinical handoff scoring is *fundamentally not* a binary-verifier domain — it's why HealthBench-style rubric eval exists.
3. **Episode length** — KellyBench at 500–900 tool calls is the host's "long horizon." We're 41. Frame Tingin as "channel-depth" not "horizon-length" (see §3).

**Sources:**
- DeepSynth — https://openreward.ai/GeneralReasoning/DeepSynth
- BountyBench — https://openreward.ai/GeneralReasoning/BountyBench
- KellyBench — https://openreward.ai/GeneralReasoning/KellyBench
- Meta OpenEnv RFC — https://github.com/meta-pytorch/OpenEnv/issues/468
- Bemiagent ORS overview — https://bemiagent.com/agents/open-reward-standard-an-http-protocol-for-rl-environments-what-it-is-and-whether-you-should-care
- PyPI release stream — https://pypi.org/project/openreward/

---

## 8. Quick-reference citations for pitch Q&A

If asked... | Cite this:
---|---
"Is this novel?" | iAgents (info asymmetry, but synchronous), SMACv2 EPO (partial obs, but spatial), IMAC (info bottleneck, but co-temporal). None combine temporal separation + compression + third-party-paid cost.
"How do you score handoffs?" | HealthBench pattern — instance-specific physician-authored rubric, model-based grader validated against expert judgment.
"How would you find reward hacks?" | TRACE methodology — contrastive trajectory clustering. Cluster size N, benign-to-hack ratio B.
"Where's the seed data?" | California-anchored stack: MDS 3.0 (federal SNF schema, public), INTERACT SBAR + Stop and Watch (FAU ©2011, free for clinical use), CNAHRT (UNC DNP, CNA-specific), CA Title 22 §§72329.1/2 (staffing), Adler-Milstein 2021 (CC-BY, US SNF transitions). Full stack: `geth/specs/seed-data-review-v2.md`.
"What makes this RL and not a simulator?" | Greedy-local can't solve it. The cost is paid across an agent boundary the agent doesn't control — the information is gone before shift 2 arrives. Credit-assignment depth across a compression channel is the property.
"Why not 500 tool calls like KellyBench?" | Different unit. KellyBench measures horizon as tool-calls-per-episode within one trajectory. Tingin measures horizon as episodes-per-patient — dozens of shifts across weeks of SNF care, connected by lossy compression at every handoff. Two shifts is the minimum demonstration; the benchmark extends naturally.
"Did you train an agent?" | Tier 1: scripted policies (demo). Tier 2: one Claude rollout via tool-calling (evidence env runs an agent). Tier 3: 10–20 rollouts across policy variants, distribution comparison. From-scratch fine-tune is Tier 4 (out of scope today, hardware-permitting overnight).
