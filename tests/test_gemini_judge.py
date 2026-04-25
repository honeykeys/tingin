"""
Gemini judge smoke-test — verifies GOOGLE_API_KEY works and judge output validates.
Skips if no API key (CI-safe).
"""
import pytest
import os

pytestmark = pytest.mark.skipif(
    not os.environ.get("GOOGLE_API_KEY"),
    reason="GOOGLE_API_KEY not set"
)


def test_gemini_available():
    import google.generativeai as genai
    api_key = os.environ.get("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content("Reply with only the word: OK")
    assert "OK" in response.text


def test_judge_scores_good_handoff():
    from nursingfloor.scorer_gemini import score_with_judge
    good_body = (
        "Mrs. Aquino bed 2, 78F post-CAP day 6. DNR/POLST. Sulfa allergy. "
        "Observed pale withdrawn picking at breakfast — behavioral change vs baseline. "
        "CHF + T2DM on furosemide and metformin. NEWS2 trending 1-2. "
        "Mrs. Reyes bed 1, penicillin allergy, hip ORIF POD4, stable. "
        "Mr. Goldberg bed 3 DNR/DNI/DNH, sacral pressure ulcer repositioned q2h."
    )
    ground_truth = "P2 slow_det physiology. P2 DNR/POLST. P2 sulfa allergy. P1 penicillin allergy. P3 DNR/DNI/DNH. P3 stage 2 sacral ulcer."
    result = score_with_judge(good_body, ground_truth, use_cache=False)
    assert 0.0 <= result["score"] <= 1.0
    assert result["tier"] == 3
    assert len(result["iashr_breakdown"]) == 16
    assert result["score"] > 0.4, "Good handoff should score >40%"


def test_judge_penalizes_bad_handoff():
    from nursingfloor.scorer_gemini import score_with_judge
    bad_body = "Mrs. Aquino stable. Mr. Goldberg UTI. Mrs. Reyes hip surgery."
    ground_truth = "P2 slow_det physiology. P2 DNR/POLST. P2 sulfa allergy. P1 penicillin allergy. P3 DNR/DNI/DNH. P3 stage 2 sacral ulcer."
    result = score_with_judge(bad_body, ground_truth, use_cache=False)
    assert result["score"] < 0.5, f"Bare handoff should score <50%, got {result['score']:.0%}"
