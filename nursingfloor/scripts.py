from nursingfloor.floor import NursingFloor


def run_a_script(floor: NursingFloor) -> list:
    """Good handoff: RN1 observes Mrs. Aquino, handoff preserves ambient signal."""
    # --- Shift 1: RN1 ---
    floor.check_vitals("P1", "RN1")
    floor.check_vitals("P2", "RN1")
    floor.observe_patient("P2", "RN1")   # KEY: surfaces ambient signal
    floor.check_vitals("P3", "RN1")
    floor.administer_medication("P2", "azithromycin", "250 mg", "RN1")
    floor.administer_medication("P1", "acetaminophen", "650 mg", "RN1")
    floor.administer_medication("P3", "ceftriaxone", "1 g", "RN1")
    floor.document_observation("P2", "Pt pale withdrawn picking at breakfast not herself", "RN1")
    floor.document_observation("P3", "Confusion baseline no acute change repositioned q2h stage 2 sacral ulcer", "RN1")
    floor.check_vitals("P2", "RN1")
    floor.check_vitals("P3", "RN1")
    floor.check_vitals("P1", "RN1")

    # Write handoff at end of shift1 — preserves P2 ambient signal
    handoff_text = (
        "Census of 3.\n\n"
        "Bed 1 — Mrs. Patricia Reyes, 84, POD#4 hip ORIF. NEWS2 0. Pain 3/10, "
        "last acetaminophen 0830. Enoxaparin given. Allergies: penicillin. Full code. "
        "Daughter visiting Saturday. No issues.\n\n"
        "Bed 2 — Mrs. Elena Aquino, 78, day 6 post-CAP. NEWS2 trending 1-2 "
        "(RR 20, SpO2 94). DNR/POLST on file. Allergies: sulfa. Last azithromycin "
        "dose today done. CHF + T2DM on furosemide and metformin. "
        "**Ambient: observed 0930 pale withdrawn picking at breakfast. Not herself. "
        "Watch closely tonight consider NEWS2 recheck at 2100.**\n\n"
        "Bed 3 — Mr. Walter Goldberg, 91, UTI on dementia. NEWS2 2. DNR/DNI/DNH/POLST. "
        "NKA. Ceftriaxone 0900 done. Stage 2 sacral pressure ulcer repositioned q2h "
        "last 1500. Last BM 2 days ago bowel program if no movement by 2200.\n\n"
        "No pending consults."
    )
    floor.write_handoff(handoff_text, "RN1")

    # --- Shift 2: RN2 reads handoff, responds to P2 ---
    # Handoff preserved the ambient signal → RN2 prioritizes Mrs. Aquino
    floor.read_handoff("RN2")
    floor.check_vitals("P2", "RN2")
    floor.observe_patient("P2", "RN2")          # confirms: still pale, labored breathing
    floor.document_observation("P2", "P2 pale withdrawn as per handoff RR elevated notifying MD", "RN2")
    floor.administer_medication("P2", "furosemide", "20 mg", "RN2")  # CHF exacerbation — acts on context
    floor.check_vitals("P1", "RN2")
    floor.check_vitals("P3", "RN2")

    return floor.events


def run_b_script(floor: NursingFloor) -> list:
    """Bad handoff: RN1 skips observation, handoff lacks ambient signal."""
    # --- Shift 1: RN1 (vitals only, no bedside on P2) ---
    floor.check_vitals("P1", "RN1")
    floor.check_vitals("P2", "RN1")
    # NO observe_patient on P2
    floor.check_vitals("P3", "RN1")
    floor.administer_medication("P2", "azithromycin", "250 mg", "RN1")
    floor.administer_medication("P1", "acetaminophen", "650 mg", "RN1")
    floor.administer_medication("P3", "ceftriaxone", "1 g", "RN1")
    floor.check_vitals("P2", "RN1")
    floor.check_vitals("P3", "RN1")
    floor.check_vitals("P1", "RN1")
    floor.check_vitals("P2", "RN1")
    floor.check_vitals("P3", "RN1")

    # Vitals-only handoff — no ambient signal for P2
    handoff_text = (
        "Census of 3.\n\n"
        "Bed 1 — Mrs. Patricia Reyes, 84, POD#4 hip ORIF. NEWS2 0. Stable. "
        "Meds given. Penicillin allergy.\n\n"
        "Bed 2 — Mrs. Elena Aquino, 78, day 6 post-CAP. NEWS2 1 at 0800. "
        "On azithromycin last dose today, furosemide, metformin. DNR/POLST. "
        "Sulfa allergy. Tolerating diet.\n\n"
        "Bed 3 — Mr. Walter Goldberg, 91, UTI on dementia. NEWS2 2. "
        "DNR/DNI/DNH. NKA. Ceftriaxone done. Skin intact.\n\n"
        "No issues."
    )
    floor.write_handoff(handoff_text, "RN1")

    # --- Shift 2: RN2 reads handoff, no cue to investigate P2 ---
    floor.read_handoff("RN2")
    floor.check_vitals("P1", "RN2")
    floor.check_vitals("P2", "RN2")
    # NO observe_patient on P2 — no prompt from handoff
    floor.check_vitals("P3", "RN2")

    return floor.events
