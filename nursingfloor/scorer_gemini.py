"""
Gemini 2.5 Flash IASHR handoff judge.
Loads GOOGLE_API_KEY from .env. Scores a handoff against the 16-criterion IASHR rubric.
Caches results to demo/judge_cache.json.

Rubric anchored in:
  INTERACT SBAR (FAU ©2011) + CNAHRT (McDermott 2021) + Adler-Milstein 2021 (JAMA, CC-BY)
  + Cohen/Abraham 2017 (low-overlap categories) + California Title 22 §72311
  + MDS 3.0 change-since-last-assessment.

Full rubric spec: geth/specs/seed-data-review-v2.md § "Tier 3 Rubric Proposal"
"""
import json
import hashlib
from pathlib import Path

CACHE_PATH = Path(__file__).parent.parent / "demo" / "judge_cache.json"

# The 16 IASHR criteria with weights.
# Source: geth/specs/seed-data-review-v2.md § "Tier 3 Rubric Proposal"
# Total: 39 points.
# Weighting rationale:
#   1 point: identifying / process items
#   2 points: clinical-content items (empirically high overlap, Cohen 2017)
#   3 points: empirically low-overlap, high-stakes (Cohen 2017 + Adler-Milstein 2021)
#   4 points: regulatory-trigger items (California Title 22 §72311 mandates)
IASHR_CRITERIA = [
    (1,  "Patient ID + name + room/bed + code status",                                          1),
    (2,  "Primary diagnoses + LTC vs. PAC designation",                                         2),
    (3,  "Vitals — BP, HR, RR, Temp, O2 sat, pain — current shift values",                     2),
    (4,  "Active medications + scheduled vs. PRN + warfarin/INR + recent changes",              3),
    (5,  "Allergies (stated explicitly, even if NKA)",                                          3),
    (6,  "Advance directives — DNR/DNI/DNH/POLST/hospice",                                     3),
    (7,  "Recent change-in-condition (mental, functional, respiratory, GI, GU, skin)",          3),
    (8,  "Pending tasks + awaited results (labs, imaging, consults, transfers)",                 2),
    (9,  "ADL status + transfer status + ambulation aid",                                       2),
    (10, "Bowel/bladder status — last BM date, continence, foley/ostomy, output",               2),
    (11, "Skin integrity — pressure ulcers (count + stage), wounds, repositioning schedule",    3),
    (12, "Behavioral / mental-status changes since last assessment (ambient observations)",      3),
    (13, "Functional / social / psychosocial concerns (family context, not just clinical)",     3),
    (14, "Title 22 §72311 notification triggers — weight change, untoward med response, etc.", 4),
    (15, "Stop and Watch / CNA ambient observations from this shift or prior 24h",              2),
    (16, "Read-back / verbal confirmation of critical items",                                   1),
]

JUDGE_PROMPT_TEMPLATE = """You are a clinical nurse educator scoring a nursing shift handoff report.

Score the following handoff against each IASHR criterion.

HANDOFF REPORT:
{handoff_body}

GROUND TRUTH STATE (what the outgoing nurse knew):
{ground_truth}

For each criterion below, score as:
- "full" (full points): criterion clearly addressed
- "partial" (half points): criterion partially addressed or implied
- "missing" (0 points): criterion absent from handoff

Also flag any "hallucinations": claims in the handoff that contradict the ground truth.

Respond ONLY with valid JSON in this exact format:
{{
  "scores": [
    {{"criterion_id": 1, "status": "full"|"partial"|"missing", "reasoning": "brief explanation"}},
    ...
  ],
  "hallucinations": ["claim 1", ...] or []
}}

CRITERIA:
{criteria_list}
"""


def score_with_judge(handoff_body: str, ground_truth_summary: str, use_cache: bool = True) -> dict:
    """
    Score a handoff using Gemini 2.5 Flash as judge.
    Returns a dict matching ScoreResult Tier 3 shape.

    Args:
        handoff_body: The full text of the handoff report to score.
        ground_truth_summary: What the outgoing nurse actually knew (ground truth state).
        use_cache: If True, check/populate demo/judge_cache.json for reproducibility.

    Returns:
        dict with keys: score, matched_facts, missing_facts, tier,
        iashr_breakdown, hallucinations, judge_reasoning.
    """
    # Cache key — hash of handoff body + ground truth
    cache_key = hashlib.sha256(f"{handoff_body}{ground_truth_summary}".encode()).hexdigest()[:16]

    # Check cache
    if use_cache and CACHE_PATH.exists():
        cache = json.loads(CACHE_PATH.read_text())
        if cache_key in cache:
            return cache[cache_key]

    import google.generativeai as genai
    import os

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not set. Load from .env: "
            "export $(grep -v '^#' .env | xargs)"
        )

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

    criteria_list = "\n".join(
        f"{c[0]}. {c[1]} (weight: {c[2]})" for c in IASHR_CRITERIA
    )

    prompt = JUDGE_PROMPT_TEMPLATE.format(
        handoff_body=handoff_body,
        ground_truth=ground_truth_summary,
        criteria_list=criteria_list,
    )

    response = model.generate_content(prompt)
    text = response.text.strip()

    # Strip markdown code blocks if present
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    text = text.strip()

    raw = json.loads(text)

    # Build ScoreResult Tier 3 shape
    iashr_breakdown = []
    total_points = 0.0
    max_points = sum(c[2] for c in IASHR_CRITERIA)  # 39

    for score_item in raw["scores"]:
        cid = score_item["criterion_id"]
        criterion = next((c for c in IASHR_CRITERIA if c[0] == cid), None)
        if not criterion:
            continue
        weight = criterion[2]
        status = score_item["status"]
        points = weight if status == "full" else (weight * 0.5 if status == "partial" else 0.0)
        total_points += points
        iashr_breakdown.append({
            "criterion_id": cid,
            "criterion_name": criterion[1],
            "weight": weight,
            "status": status,
            "points_awarded": points,
            "judge_reasoning": score_item["reasoning"],
        })

    hallucinations = raw.get("hallucinations", [])
    normalized_score = total_points / max_points if max_points > 0 else 0.0

    result = {
        "score": round(normalized_score, 3),
        "matched_facts": [b["criterion_name"] for b in iashr_breakdown if b["status"] == "full"],
        "missing_facts": [b["criterion_name"] for b in iashr_breakdown if b["status"] == "missing"],
        "tier": 3,
        "iashr_breakdown": iashr_breakdown,
        "hallucinations": hallucinations,
        "judge_reasoning": {str(b["criterion_id"]): b["judge_reasoning"] for b in iashr_breakdown},
    }

    # Cache result
    cache = {}
    if CACHE_PATH.exists():
        cache = json.loads(CACHE_PATH.read_text())
    cache[cache_key] = result
    CACHE_PATH.parent.mkdir(exist_ok=True)
    CACHE_PATH.write_text(json.dumps(cache, indent=2))

    return result
