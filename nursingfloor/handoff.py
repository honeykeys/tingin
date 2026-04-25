from dataclasses import dataclass


@dataclass
class Fact:
    fact_id: str
    description: str
    weight: float
    keywords: list

    def matches(self, handoff_text: str) -> bool:
        text_lower = handoff_text.lower()
        return any(kw.lower() in text_lower for kw in self.keywords)


# Ground-truth fact list for Tier 1 scoring
# Weights inspired by IASHR: ambient signal = 3, code status = 3, allergy = 3, skin = 3
GROUND_TRUTH_FACTS = [
    Fact("P1_id", "P1 identifying info (Mrs. Reyes, bed 1)", 1.0,
         ["reyes", "bed 1", "patricia", "hip", "orif", "pod"]),
    Fact("P2_id", "P2 identifying info (Mrs. Aquino, bed 2)", 1.0,
         ["aquino", "bed 2", "elena", "pneumonia", "cap"]),
    Fact("P2_ambient", "P2 ambient signal noted (withdrawn, pale)", 3.0,
         ["pale", "withdrawn", "picking", "not herself", "ambient", "observe"]),
    Fact("P2_code", "P2 DNR/POLST", 3.0,
         ["dnr", "polst"]),
    Fact("P2_allergy", "P2 allergy (sulfa)", 3.0,
         ["sulfa"]),
    Fact("P3_id", "P3 identifying info (Mr. Goldberg, bed 3)", 1.0,
         ["goldberg", "bed 3", "walter", "uti", "dementia"]),
    Fact("P3_skin", "P3 pressure ulcer noted", 3.0,
         ["pressure", "ulcer", "sacral", "stage 2", "repositioned"]),
    Fact("P3_code", "P3 code status (DNR/DNI/DNH)", 3.0,
         ["dni", "dnh"]),
    Fact("P1_allergy", "P1 allergy (penicillin)", 3.0,
         ["penicillin"]),
    Fact("P1_discharge", "P1 expected discharge date", 1.0,
         ["discharge", "pod"]),
]


def score_handoff_tier1(handoff_text: str) -> tuple:
    """Returns (score 0..1, matched_descriptions, missing_descriptions)."""
    matched = []
    missing = []
    total_weight = sum(f.weight for f in GROUND_TRUTH_FACTS)
    matched_weight = 0.0

    for fact in GROUND_TRUTH_FACTS:
        if fact.matches(handoff_text):
            matched.append(fact.description)
            matched_weight += fact.weight
        else:
            missing.append(fact.description)

    score = matched_weight / total_weight if total_weight > 0 else 0.0
    return score, matched, missing
