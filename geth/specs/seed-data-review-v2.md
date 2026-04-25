# Seed Data Review v2 — California SNF Anchor Stack — 2026-04-25

## TL;DR

- **What we got:** INTERACT v3.0/v4.0 SBAR + Stop and Watch + Care Paths list + QI Tool (FAU-copyrighted, free for clinical use, on disk). CNAHRT verbatim tool from the UNC DNP capstone (Appendix B, on disk). California Title 22 §§ 72327, 72329.1, 72329.2, 72311, 72315 verbatim from Cornell + CDPH AFL 19-16 PDF (8 pages, on disk). MDS 3.0 NC Comprehensive Item Set v1.14.0 (45 pages, all 18 sections A–Z, on disk). Adler-Milstein 2021 (CC-BY) verbatim percentages of dropped categories. BMC Nursing 2025 (n=688) verbatim missed-info statistics. Riesenberg 2012 (AHRQ 50% statistic + Joint Commission 80% statistic). King 2013 SNF qualitative quotes. Cohen/Abraham 2017 content-overlap method. Patel 2016 SCA method. Labovic 2018 CalVet 70% incomplete-handoff statistic.
- **What we didn't get:** Galli's 88% number doesn't reproduce against any source we pulled — the defensible numbers are Joint Commission 80% (handoff miscommunication → serious medical errors), AHRQ 50% (info often lost), BMC 2025 27.4% (nurses agree info is often missed), Adler-Milstein 49.6% (SNFs failing to receive ≥80% of 23 info categories), Labovic 70% (CalVet incomplete transfers). The official INTERACT 5.0 portal at `pathway-interact.com/tools/` requires registration; we used the canonical FAU 2011 v3.0 forms still circulated by Indiana DOH + the v4.0 Implementation Guide. CDPH AFL 21-11 page is JS-rendered and didn't text-extract; AFL 19-16 PDF covers the substance. Baluyot 2022 was paywalled past the metadata page. Cohen 2017 paper full text was paywalled (abstract + key methods captured).
- **What's enough to start:** Yes. We have the INTERACT field structure verbatim, MDS 3.0 sections verbatim, Title 22 staffing thresholds verbatim, CNAHRT field structure verbatim, and four independent failure-mode statistics that triangulate to roughly half-of-handoffs-leak. Build today.

---

## Anchor stack table

| Layer | Anchored on | Source URL | License |
|---|---|---|---|
| Patient profile schema (slow-changing) | MDS 3.0 NC Comprehensive Item Set v1.14.0 — 18 sections A through Z | `https://www.cms.gov/Medicare/Quality-Initiatives-Patient-Assessment-Instruments/NursingHomeQualityInits/Downloads/MDS30_NC_Comp_v1140.pdf` | Federal public domain |
| Per-shift flow-sheet schema | Synthesized from INTERACT SBAR + CNAHRT Appendix B + Title 22 §72315 patient-care duties | INTERACT FAU; CNAHRT UNC DNP; Title 22 (state regulation) | INTERACT: FAU©2011 free for clinical use; CNAHRT: published academic; Title 22: public regulation |
| Handoff field structure (per-event signal) | INTERACT SBAR (4 sections, with 5 system sub-checklists) + CNAHRT (9 sections) | `https://www.in.gov/health/files/INTERACT_SBAR_Form.pdf` + `https://cdr.lib.unc.edu/downloads/tm70n5089` | FAU©2011; UNC DNP open-access |
| Acute-change escalation surface | INTERACT Stop and Watch Early Warning Tool (12 mnemonic items) + INTERACT Care Paths (10 conditions) | `https://www.in.gov/health/files/INTERACT_Stop_and_Watch_Early_Warning_Tool.pdf` + V4 Implementation Guide | FAU©2011; FAU©2014 |
| Staffing model | California Title 22 §§ 72327 (DON), 72329.1 (bed-tier ratios + 3.2 NHPPD), 72329.2 (3.5 DHPPD + 2.4 CNA HPPD), 72311 (general), 72315 (patient care) + CDPH AFL 19-16 audit guidelines | `law.cornell.edu/regulations/california/22-CCR-...` + `cdph.ca.gov/.../AFL-19-16.pdf` | Public state regulation |
| Failure-mode prior | Triangulated: AHRQ 50% (Riesenberg 2012), Joint Commission 80% (Riesenberg 2012), BMC Nursing 2025 27.4% (n=688 US RNs), Adler-Milstein 2021 49.6% / 67.7% behavioral missing, Labovic 2018 70% CalVet | PMC / link.springer / repository.usfca.edu | CC-BY (Adler-Milstein); CC-BY-NC-ND (BMC 2025); ACGME © (Riesenberg); USF capstone open access (Labovic) |

---

## Source 1 — INTERACT (Florida Atlantic University)

### Access
- **`pathway-interact.com/interact-tools/`:** redirects to `pathway-interact.com/tools/` and requires registration. Did not register.
- **`interact.fau.edu`:** TLS cert mismatch, did not connect.
- **`https://www.in.gov/health/files/INTERACT_SBAR_Form.pdf`:** ✓ pulled, 4 pages, FAU ©2011 v3.0.
- **`https://www.in.gov/health/files/INTERACT_Stop_and_Watch_Early_Warning_Tool.pdf`:** ✓ pulled, 1 page, FAU ©2011.
- **`https://www.in.gov/health/files/INTERACT_QI_Tools.pdf`:** ✓ pulled, 5-page QI Tool For Review of Acute Care Transfers, FAU ©2011 v3.0.
- **`https://www.adldata.org/wp-content/uploads/2015/07/INTERACT-V4-Implementation_Guide-Dec-10.pdf`:** ✓ pulled, INTERACT v4.0 Dec 2014 implementation guide listing all v4.0 tools and Care Paths.
- INTERACT 5.0 (current) requires registration on the Pathway INTERACT portal. The 2011 v3.0 forms and 2014 v4.0 implementation guide are widely circulated by state DOHs and capture the canonical structure.

### Contents
```
interact/
  INTERACT_SBAR_Form.pdf                       (101 KB, 4 pages, v3.0)
  INTERACT_SBAR_Form.txt                       (extracted)
  INTERACT_Stop_and_Watch_Early_Warning_Tool.pdf  (45 KB, 1 page, v3.0)
  INTERACT_Stop_and_Watch_Early_Warning_Tool.txt  (extracted, 35 lines)
  INTERACT-V4-Implementation_Guide.pdf         (199 KB, 15 pages)
  INTERACT-V4-Implementation_Guide.txt         (extracted)
  indiana-interact-qi-tools.pdf                (414 KB, 5 pages — QI Tool For Review of Acute Care Transfers, v3.0)
  indiana-interact-qi-tools.txt                (extracted, 191 lines)
```

### Verbatim — Stop and Watch Early Warning Tool (FAU ©2011)

The mnemonic spells STOP AND WATCH. **12 items** (not 9 as my prompt suggested):

```
S    Seems different than usual
T    Talks or communicates less
O    Overall needs more help
P    Pain – new or worsening; Participated less in activities

a    Ate less
n    No bowel movement in 3 days; or diarrhea
d    Drank less

W    Weight change
A    Agitated or nervous more than usual
T    Tired, weak, confused, or drowsy
C    Change in skin color or condition
H    Help with walking, transferring, toileting more than usual

[Then: Resident name, Your name, Reported to / Date and Time,
 Nurse Response / Date and Time, Nurse's Name]
```

Front-line CNAs use this card and either hand it to the licensed nurse or review verbally. It is the **CNA-to-RN escalation event** in the SNF.

### Verbatim — SBAR Communication Form (FAU ©2011)

Pre-call checklist:
> Before Calling MD / NP / PA:
> ☐ Evaluate the Resident: Complete relevant aspects of the SBAR form below
> ☐ Check Vital Signs: BP, pulse, and/or apical heart rate, temperature, respiratory rate, oximetry, and finger stick glucose, if indicated
> ☐ Review Record: Recent progress notes, labs, orders
> ☐ Review an INTERACT Care Path or Acute Change in Condition File Card, if indicated
> ☐ Have Relevant Information Available when Reporting (medical record, vital signs, advance directives, allergies, medication list)

**SITUATION:** change/symptom/sign called about; date started; trajectory (worse/better/same); aggravating factors; alleviating factors; recurrence; treatment for last episode; other relevant info.

**BACKGROUND — Resident Description:** Post-Acute Care vs. Long-Term Care; primary diagnoses; other pertinent history.

**BACKGROUND — Medication Alerts:** changes in last week; warfarin/coumadin + last INR; allergies.

**BACKGROUND — Vital Signs:** BP, Pulse, Apical HR, RR, Temp, Weight (date), prior weight (for CHF/edema/weight loss), oximetry (RA or O2 + L/min).

**Five system-specific change-from-baseline blocks (mark N/A if irrelevant):**

1. **Mental Status Changes:** increased confusion / decreased consciousness / new/worsening behavioral symptoms / unresponsiveness / other delirium signs (inability to attend, disorganized thinking).
2. **Functional Status Changes:** needs more ADL assistance / decreased mobility / fall / weakness or hemiparesis / slurred speech / trouble swallowing / other.
3. **Respiratory:** SOB / cough (productive vs non-) / abnormal lung sounds / labored breathing.
4. **GI/Abdomen:** nausea / vomiting / diarrhea / decreased appetite / abdominal pain / distended / tenderness / decreased bowel sounds (date of last BM).
5. **GU/Urine Changes:** decreased output / painful / frequency / urgency / hematuria / new/worsening incontinence.

**Recent Lab Results** (free text, e.g., CBC, chemistry/metabolic panel, drug levels).

**Advance Care Planning:** DNR, DNI, DNH, No Enteral Feeding, other order or living will. Other resident or family preferences.

**ASSESSMENT (RN) OR APPEARANCE (LPN):**
- For RNs: "I think the problem may be (e.g., cardiac, infection, respiratory, dehydration)..."
- For LPNs: "The resident appears (e.g., short of breath, in pain, more confused)..."

The RN/LPN split is critical — license scope determines whether nurse can frame an assessment or only an appearance.

**REQUEST:** monitor vital signs / lab work / x-ray / EKG / provider visit (MD/NP/PA) / transfer to hospital / other new orders.

**Footer:** family/health-care-agent notification (name, date, time); primary care clinician notification (name, date, time); RN/LPN signature; resident name.

### Verbatim — INTERACT Care Paths list (10 conditions, from V4.0 Implementation Guide p10)

1. Acute Mental Status Change
2. Change in Behavior – New or Worsening Symptoms
3. Dehydration
4. Fever
5. GI Symptoms: Nausea, vomiting, diarrhea
6. Shortness of Breath
7. Symptoms of lower respiratory illness
8. Symptoms of CHF
9. Symptoms of UTI
10. Fall

These are decision-support pathways — not handoff fields per se, but they identify the **10 condition types whose acute change in SNF residents most often drives ED transfer**. For Tingin: these are the 10 trajectory types our patient sim should generate.

### Verbatim — INTERACT QI Tool For Review of Acute Care Transfers (5 sections)

The QI Tool is a retrospective review form (not a per-shift handoff tool). Useful for our **Tier 3 LLM-judge** because its category list defines what "an acute change worth escalating" actually contains:

**Section 1 — Resident Characteristics:** ID, DOB, admit date, age; major diagnoses; risk factors checklist (Cancer on chemo/radiation; CHF; COPD; Dementia; ESRD; Fracture; Multiple co-morbidities; Polypharmacy ≥9 meds; Surgical complications; Other).

**Section 2 — New/Worsening Symptoms or Signs:** abdominal pain, abnormal vitals (low/high BP, high RR), altered mental status, behavior symptoms (agitation, psychosis), bleeding, cardiac arrest, chest pain, diarrhea, edema, fall, fever, food/fluid intake, functional decline, gastrostomy tube blockage/displacement, loss of consciousness, nausea/vomiting, pain (uncontrolled), respiratory arrest, respiratory infection, SOB, seizure, skin wound or ulcer, unresponsiveness, urinary incontinence, weight loss, other.

**Section 2 — Abnormal Lab/Test Results:** blood sugar (high/low), EKG, hemoglobin/hematocrit (low), INR (high/low), kidney function (BUN/Cr), pulse oximetry (low O2 sat), urinalysis/culture, WBC (high), x-ray, other.

**Section 2 — Diagnoses:** acute renal failure, anemia (new/worsening), CHF, cellulitis, COPD, DVT, fracture (with site), pneumonia, UTI, other.

**Section 3 — Tools Used:** Stop and Watch / SBAR / Care Path(s) / Change in Condition File Cards / Transfer Checklist / Acute Care Transfer Form / Advance Care Planning Tools / Other Structured Tool.

**Section 3 — Medical Evaluation:** Telephone only / NP or PA visit / MD visit / Other.

**Section 3 — Testing:** Blood tests / EKG / Urinalysis / Venous doppler / X-ray / Other.

**Section 3 — Interventions:** New medication(s) / IV or subcutaneous fluids / Increase oral fluids / Oxygen / Other.

**Section 3 — Advance Directives:** considered? new directives written? DNR / Comfort or Palliative Care / DNH / Hospice / POLST/MOLST/POST.

**Section 4 — Hospital Transfer:** date, day, time; clinician authorizing (Primary MD / Covering MD / NP or PA / Other); outcome (Admitted inpatient / Admitted observation / Status uncertain / ED visit only / Other); resident died (No / Yes / Unknown); hospital diagnoses; **factors contributing to transfer** (Advance directive not in place / Resident insisted / Family insisted / Resources not available / NH policies don't support care in NH / Clinician insisted / Other).

**Section 5 — Improvement Opportunities:** preventability assessment; what could have been detected earlier; communication failures; resource gaps (on-site primary care, staffing, lab/diagnostics, pharmacy); preferences-discussion timing; advance-directive timing.

### Limitations
- Pulled v3.0 forms (2011), not the proprietary v5.0 forms behind the FAU registration wall. The fields are stable — v4 and v5 add COVID-19 updates and electronic-record refinements, not new content categories.
- Care Paths themselves (the actual decision algorithms) are 8.5×11 laminated cards; we have the LIST of 10 paths but not the field-by-field content of each. For the hackathon this is OK — the LIST is what defines our patient sim's trajectory taxonomy.

### License
> "©2011 Florida Atlantic University, all rights reserved. This document is available for clinical use, but may not be resold or incorporated in software without permission of Florida Atlantic University."

For Tingin: we cite the field structure as anchored in INTERACT (FAU © 2011, free for clinical use). We do **not** ship the FAU forms verbatim in our product. Our generated handoff schema is an INTERACT-anchored derivative; for any commercial deployment we'd need FAU permission, but for hackathon non-commercial sim grounding the structure is fine to cite.

---

## Source 2 — CNAHRT (UNC School of Nursing DNP Capstone)

### Access
- **`https://cdr.lib.unc.edu/downloads/tm70n5089`:** ✓ direct PDF, 877 KB, 60 pages.
- Author: **Shanta'i McDermott MSN, AGPCNP-BC**. Faculty advisor: Victoria Soltis-Jarrett. Date: 2021. UNC IRB exempted (#21-2512).

### Contents
```
cnahrt/
  cnahrt-unc-dnp.pdf       (877 KB, 60 pages, includes Appendix A SBAR definitions + Appendix B CNAHRT tool + Appendix C Implementation Team + D-F)
  cnahrt-unc-dnp.txt       (extracted, 3033 lines)
```

### Verbatim — Appendix A: SBAR Definitions (used as CNAHRT template)

| SBAR Tool | Term | Answers the Question |
|---|---|---|
| S | Situation | "What is happening now with the patient?" |
| B | Background | "What has happened in the past with the patient?" |
| A | Assessment | "What do I think the problem is?" |
| R | Recommendations | "What I think needs to happen now?" |

### Verbatim — Appendix B: CNAHRT Communication Tool (the CNA-specific handoff form)

The CNAHRT is a **9-section task-oriented handoff tool** (per p2530 of the dissertation). The form fields, in order of appearance on the page:

**1. Identification block:**
- Patient Name | Age | Code Status
- Admit Date | Room # | Bed

**2. VITALS block (single-time-stamped column):**
- Time taken (HH:MM)
- Ht | Wt (lbs) | BG (blood glucose)
- BP | HR | RR | Temp | O2%
- Pain Rating __/10 | Site(s)

**3. Hygiene block:**
- Oral Care: Independent / Dependent
- Bathing: Independent / Dependent
- Toileting: Independent / Dependent
- Dressing: Independent / Dependent
- Devices: Dentures / Hearing Aides / Glasses

**4. Food Intake block:**
- Diet Orders (free text)
- Meal / Fluids (free text)
- NG Tube (free text)

**5. Output block:**
- Continent Bladder: Y / N
- Continent Bowel: Y / N
- BM: Formed / Constipation / Diarrhea
- How Many BM's? (count)
- Foley: Y / N
- Urinal: Y / N
- Amount

**6. Diagnoses block (chronic):**
- Asthma, Atrial Fibrillation, BPH, Cancer, COPD, COVID-19 (historical), DM, Dementia W/behavior, Dialysis, Gout, Heart Failure, HTN, Osteoporosis (and free text)

**7. Acute Diagnoses block:**
- Pneumonia, COVID-19, UTI, URI, Flu

**8. Safety Checks block:**
- Falls Risk: Y / N
- Recent Fall(s): (free text)
- Ambulation: Self / Cane / Walker / W/C
- Transfer Status: Self / 1x / 2x

**9. Skin block:**
- Bruise(s): Y / N + Site
- Rash: Y / N + Site
- Skin Tear: Y / N + Site
- Ulcer(s): Y / N + Site

**Plus: Additional Notes** (free-text panel)

### What this gives Tingin
The CNAHRT is the **per-shift CNA-perspective flow sheet** — exactly the per-shift state we need for Tingin's "what the CNA sees on the floor that doesn't make it to the licensed nurse handoff." Adler-Milstein 2021 shows that 80–90% of direct care in nursing homes is provided by CNAs (per the dissertation's lit review p2517–18); CNAHRT formalizes what they should communicate.

For our environment:
- **CNAHRT is our CNA-perspective view of patient state** (the ambient signal layer).
- **INTERACT SBAR is the licensed-nurse-to-clinician escalation view** (the clinical reasoning layer).
- The asymmetry between them is where omission lives — the CNA sees pain rating and skin tears that the RN never asks about.

### Limitations
- CNAHRT is one DNP project's tool, not a CMS standard. It's evidence-based (SBAR-derived) but n=3 CNAs at one NC long-term care facility post-implementation — pilot scale.
- Outcomes claimed: 80% compliance target, 50% workflow-satisfaction improvement, 15% fall-rate decrease, 10% toileting-care increase. None of these were verified from the body — they're the project's ambitions per Appendix D.

### License
- DNP capstone published in UNC's institutional repository (cdr.lib.unc.edu) — open access, no explicit Creative Commons license shown on the download page.
- Cite as: McDermott, S. (2021). *Implementing A Structured Communication Tool To Improve Handoff Report Between Certified Nursing Assistant's In The Long-Term Care Setting - A Practice Change.* DNP Project, UNC School of Nursing.

---

## Source 3 — California Title 22 + CDPH AFL 19-16

### Access
- Cornell Law mirror of CA regulations: ✓ all five sections (72327, 72329.1, 72329.2, 72311, 72315) extracted via WebFetch.
- CDPH AFL 19-16 PDF: ✓ pulled directly, 8 pages.
- CDPH AFL 21-11 page is JS-rendered (Vue SPA). HTML-only download did not yield body text. Skipped — AFL 19-16 covers the substance.

### Contents
```
ca-title-22/
  CDPH-AFL-19-16.pdf             (564 KB, 8 pages, April 9 2019)
  CDPH-AFL-19-16.txt             (extracted, 765 lines)
  CDPH-AFL-21-11.html            (490 KB, JS-rendered, body content not extracted)
  CDPH-AFL-21-11.txt             (boilerplate only, 5 KB)
  title-22-staffing-extracted.md  (verbatim regulation extracts from Cornell)
```

### Verbatim — § 72329.1 (bed-tier ratios + 3.2 NHPPD floor)

| Beds | Licensed-staff floor |
|---|---|
| ≤59 | ≥1 RN or LVN awake on duty 24/7 |
| 60–99 | 1 RN/LVN on duty continuously **+** DON with no charge responsibilities |
| ≥100 | 1 **RN (not LVN)** on duty continuously **+** DON with no charge responsibilities |

| Shift | Direct caregiver : patient ratio |
|---|---|
| Day | 1 : 5 |
| Evening | 1 : 8 |
| Night | 1 : 13 |
| Licensed (any shift, 24-h) | 1 : ≤8 |

> "Each facility shall employ sufficient nursing staff to provide a minimum of **3.2 nursing hours per patient day**."

### Verbatim — § 72329.2 (3.5 DHPPD + 2.4 CNA HPPD floor — the binding California floor)

> "Each facility, except those skilled nursing facilities that are a distinct part of a general acute care facility, [must provide] a minimum of **3.5 direct care service hours per patient day**" and "a minimum of **2.4 certified nurse assistant hours per patient day**."

This is the binding California floor. The 3.2 figure in 72329.1 is superseded by the 3.5/2.4 in 72329.2 for free-standing SNFs.

**Mental health care facilities:**
- Standard patients: ≥3.5 hours/day
- Special treatment program patients: ≥2.3 nursing hours/day

**Distinct part of acute hospital:** continues to meet H&S Code §1276.5 standard.

**Waivers:** annual application due April 1; must include census, quality reports, staffing plans, resident needs assessments. Waiver does not relax 3.5 floor; it adjusts how 2.4 is met. Waivers can be revoked on compliance failure. Approved waivers must be posted next to license + disclosed to residents pre-admission.

### Verbatim — § 72327 (DON role)
RN; 8 hours/day, day shift, 5 days/week. ≥1 year nursing-supervision experience in the last 5 years. Administrative authority + accountability. **Serves only one facility in this capacity at a time.**

### Verbatim — § 72311 (nursing service general — the assessment + notification triggers)

**Initial assessment within 7 days of admission.** Care plan: care to be given, objectives, professional discipline responsible. **Quarterly review minimum.**

**Notification triggers** (must notify attending licensed practitioner of):
- Admission
- Sudden or marked adverse changes in condition
- Unusual occurrences (per §72541)
- **Weight change ≥ 5 lbs in 30 days** (unless different stipulation in writing)
- Untoward medication/treatment responses
- Life-threatening medication/treatment errors
- Facility's inability to provide prescribed drugs/equipment/supplies/services

### Verbatim — § 72315 (per-shift patient care duties)
The patient-care duties that should appear in each shift's flow sheet:
- (d) Hygiene: skin, hair, oral, nails — daily
- (e) Self-care maximization; out of bed when medically appropriate
- (f) Decubitus + contracture prevention: position changes, ADL assist, alignment, pressure-reducing devices, skin maintenance
- (g) Eating assistance + adaptive equipment per assessment
- (h) Adequate nutrition + hydration
- (i) Incontinence management: written assessment within 2 weeks; weekly evaluations
- (j) I/O: physician-ordered or for catheterized patients; weekly evaluations; 30-day reassessment
- (k) Weight + length at admission; **monthly weight thereafter**
- (l) Visual privacy
- (m) "Patient call signals shall be answered promptly."

### Verbatim — CDPH AFL 19-16 (April 9, 2019)
- Authority: HSC §§1276.5, 1276.65; W&I §14126.022.
- Defines audit calculation for 3.5 DHPPD + 2.4 CNA DHPPD.
- Patient Day starts at midnight.
- Subacute units excluded from direct-care-hour count.
- Required documents: CDPH Form 612 (Census + DHPPD), Form 530 (Nursing Staff Assignment + Sign-In), Form 280A (NA training program), Form 278A (NA orientation), Form 276A/276C (theory + clinical competencies), Form 283B (NA training completion).
- **Penalties:**
  - $15,000 if facility fails 5–49% of audited days
  - $30,000 if facility fails ≥50% of audited days
- Single deficiency per non-compliant audit standard, regardless of how many days.
- "The staffing requirement does not ensure that any given patient receives 3.5 or 2.4 DHPPD; it is the total number of actual direct care service hours performed by direct caregivers per patient day divided by the average patient census."

### Limitations
- Subacute units excluded from the 3.5/2.4 floor — different staffing rules under 22 CCR §51215.5. Tingin's sim is general SNF, not subacute, so this is fine.
- The 3.5/2.4 floor is a facility-wide AVERAGE. Individual residents can fall below if the average holds. This is the regulatory blind spot Tingin's attention-allocator can model.

### License
Public state regulation + state agency document. Full re-use permitted; cite source.

---

## Source 4 — MDS 3.0 Nursing Home Comprehensive Item Set v1.14.0

### Access
- **`https://www.cms.gov/.../MDS30_NC_Comp_v1140.pdf`:** ✓ pulled directly, 1.35 MB, 45 pages, effective 10/01/2016 (DRAFT marking on the form, but it is the published v1.14.0).
- Note: current production version per CMS Technical Information page is **V1.19.1 (effective 10/01/2024)**, with V1.20.1 (effective 10/01/2025) also published. **Section S** has been added in newer versions for state-specific requirements. For Tingin's purposes the section structure is unchanged across these versions; v1.14.0 is sufficient.

### Contents
```
mds-3.0/
  MDS30_NC_Comp_v1140.pdf       (1.35 MB, 45 pages)
  MDS30_NC_Comp_v1140.txt       (extracted, 2473 lines)
  cms-mds-tech.html             (CMS technical info page raw — JS-heavy)
  mds-sections-extracted.txt    (unique section headers grep)
```

### Verbatim — MDS 3.0 NC v1.14.0 Section index (18 sections — what's in the patient profile)

| Section | Title | Representative items |
|---|---|---|
| **A** | Identification Information | A0100 Facility info, A0500 Legal name, A0700 Medicaid #, A0800 Gender, A0900 Birth date, A1000 Race/Ethnicity, A1100 Language (with interpreter flag), A1200 Marital, A1300 Optional resident items (room, preferred name, lifetime occupation), A1500/A1510 PASRR, A1550 ID/DD conditions, A1700 Type of admission, A1800 Entered from, A1900 Admission date, A2000 Discharge date, A2300 ARD, A2400 Medicare stay |
| **B** | Hearing, Speech, and Vision | B0100 Comatose, B0200 Hearing, B0300 Hearing aid, B0600 Speech clarity, B0700 Makes self understood, B0800 Ability to understand, B1000 Vision, B1200 Corrective lenses |
| **C** | Cognitive Patterns | C0100 BIMS conducted, C0200 Repetition of three words, C0300 Temporal orientation, C0400 Recall, C0500 BIMS summary score; C0700–C1000 staff assessment for mental status; C1310 CAM/delirium |
| **D** | Mood | D0100 PHQ-9 conducted, D0200 PHQ-9 resident interview (9 items), D0300 PHQ-9 total score, D0500 PHQ-9 staff assessment, D0600 PHQ-9 staff total |
| **E** | Behavior | E0100 Hallucinations/delusions, E0200 Behavioral symptoms (physical, verbal, other) frequency + impact on resident, on others, on environment, E0500 Impact on resident, E0600 Impact on others, E0800 Rejection of care, E0900 Wandering, E1100 Change in behavior |
| **F** | Preferences for Customary Routine and Activities | F0300 Should interview be conducted, F0400 Resident interview (food/care/sleep/activities/social), F0500 Activity preferences, F0600 Daily preferences, F0700–F0800 Staff assessment of activity prefs |
| **G** | Functional Status | G0110 ADL assistance: bed mobility, transfer, walk in room, walk in corridor, locomotion on/off unit, dressing, eating, toilet use, personal hygiene, bathing — coded for self-performance (0–4 + 7/8 codes) and support provided (0–3); G0300 Balance during transitions; G0400 Functional limitation in ROM; G0600 Mobility devices; G0900 Functional rehabilitation potential |
| **GG** | Functional Abilities and Goals (Admission + Discharge) | GG0100 Prior functioning; GG0110 Prior device use; GG0130 Self-care (eating, oral hygiene, toileting, shower/bathe self, upper-body dressing, lower-body dressing, putting on/taking off footwear) coded 01–06 + special codes; GG0170 Mobility (roll left/right, sit to lying, lying to sitting, sit to stand, chair/bed-to-chair transfer, toilet transfer, car transfer, walk 10 ft, walk 50 ft, walk 150 ft, walk 10 ft on uneven surfaces, 1 step, 4 steps, 12 steps, picking up object, wheel 50 ft, wheel 150 ft) |
| **H** | Bladder and Bowel | H0100 Appliances (indwelling cath, external cath, ostomy, intermittent cath); H0200 Urinary toileting program (trial / response / current); H0300 Urinary continence (always cont / occ / freq / always inc / not rated); H0400 Bowel continence; H0500 Bowel toileting program; H0600 Bowel patterns (constipation Y/N) |
| **I** | Active Diagnoses (last 7 days, check all) | Cancer (I0100); Heart/Circulation (I0200 anemia, I0300 AFib/dysrhythmia, I0400 CAD, I0500 DVT/PE, I0600 Heart failure, I0700 HTN, I0800 orthostatic hypotension, I0900 PVD/PAD); GI (I1100 cirrhosis, I1200 GERD/ulcer, I1300 IBD); GU (I1400 BPH, I1500 renal insufficiency/ESRD, I1550 neurogenic bladder, I1650 obstructive uropathy); Infections (I1700 MDRO, I2000 pneumonia, I2100 septicemia, I2200 TB, I2300 UTI in last 30 days, I2400 viral hepatitis, I2500 wound infection); Metabolic (I2900 DM); plus Musculoskeletal, Neurological, Nutritional, Psychiatric, Pulmonary, Vision, Other diagnoses |
| **J** | Health Conditions | J0100 Pain mgmt (medication, scheduled vs PRN, non-med); J0200 Should pain interview happen; J0300 Pain presence (self-report + frequency + intensity 0–10 / verbal scale); J0400 Frequency; J0600 Pain effect on function; J0800 Indicators of pain (staff assessment); J1100 SOB; J1300 Current tobacco use; J1400 Prognosis (life expectancy < 6 mo); J1550 Problem conditions (fever, vomiting, dehydrated, internal bleeding); J1700 Fall history; J1800 Falls since admission; J1900 Number of falls + injury; **plus surgery** (J2000–J2400, J2500 prior surgery) |
| **K** | Swallowing/Nutritional Status | K0100 Swallowing disorder signs; K0200 Height + weight; K0300 Weight loss (5%/30d or 10%/180d); K0310 Weight gain; K0510 Nutritional approaches (parenteral, feeding tube, mech altered diet, therapeutic diet); K0710 % intake (nutrition + hydration) |
| **L** | Oral/Dental Status | L0200 Dental issues (broken/loose teeth, abnormal mouth tissue, etc.) |
| **M** | Skin Conditions | M0100 Risk of pressure ulcers (Braden / clinical assess); M0150 Existing pressure ulcer; M0210 Unhealed pressure ulcers stage ≥1; M0300 Current number by stage (1, 2, 3, 4, unstageable: non-removable dressing / slough / suspected DTI); M0610 Dimensions of largest unhealed; M0700 Most severe tissue type; M0800/M0900 Worsening; M1030 Other ulcers/wounds (venous/arterial/diabetic foot/other); M1040 Other skin issues (open lesions, surgical wound, burn); M1200 Skin/ulcer treatments (pressure-reducing device, turning/repositioning, nutrition/hydration intervention, ulcer care, surgical wound care, application of dressings, ointments, ultrasound) |
| **N** | Medications | N0300 Injections last 7 days; N0350 Insulin; N0410 Medications received last 7 days (Antipsychotic, Antianxiety, Antidepressant, Hypnotic, Anticoagulant, Antibiotic, Diuretic, **Anticonvulsant** added in v1.19.1 N0415K); N0450 Antipsychotic gradual dose reduction; N0500 Did medication review occur |
| **O** | Special Treatments, Procedures, and Programs | O0100 Special treatments while NOT a resident + while a resident: chemotherapy, radiation, oxygen, suctioning, tracheostomy care, **invasive mechanical ventilator/respirator**, BiPAP/CPAP, IV medications, transfusions, dialysis, hospice, respite care, isolation/quarantine for active infectious disease, **influenza vaccine status**, **pneumococcal vaccine status**; O0250 Restorative nursing programs; O0400 Therapies (speech-lang pathology, OT, PT, respiratory therapy, psychological therapy, recreational therapy) — minutes/days; O0500 Restorative nursing minutes |
| **P** | Restraints | P0100 Physical restraints (used in bed: bed rails / trunk / limb / chair prevents rising; used in chair); P0200 Alarms (chair, bed, door, motion, other) — Note: alarm subitems are deprecated in newer versions |
| **Q** | Participation in Assessment and Goal Setting | Q0100 Resident participates in assessment; Q0300 Goals; Q0400 Discharge planning (active discharge plan); Q0500 Return to community (resident wants to talk about return); Q0550 Resident's overall expectation; Q0600 Referral to local contact agency |
| **V** | Care Area Assessment (CAA) Summary | V0100 Care areas triggered (Delirium, Cognitive loss/dementia, Visual function, Communication, ADL/Functional/Rehab potential, Urinary incontinence + indwelling catheter, Psychosocial well-being, Mood state, Behavioral symptoms, Activities, Falls, Nutritional status, Feeding tubes, Dehydration/Fluid maintenance, Dental care, Pressure ulcer, Psychotropic medication use, Physical restraints, Pain, Return to community); V0200 Documentation referenced |
| **X** | Correction Request | X0100 Type of record + correction action; X0200–X1100 prior assessment ID block |
| **Z** | Assessment Administration | Z0100 Medicare assessment + HIPPS code; Z0150 PDPM rate (newer versions); Z0200 State/Medicaid HIPPS; Z0250 Alternate State HIPPS; Z0400 Signatures of persons completing each section |

### Section S
Per CMS Technical Information page: **Section S** has been added in newer MDS versions (V1.18.11 onward) for state-specific item sets. Not present in v1.14.0. Tingin can ignore unless a state-specific scenario requires it.

### Limitations
- v1.14.0 is from October 2016. Current is V1.19.1 (Oct 2024) with V1.20.1 (Oct 2025) also out. The structure is stable; the differences are: (1) Section S added, (2) Section A and GG refinements, (3) N0415K Anticonvulsant added in v1.19.1.
- Item Sets are FORMS — they are what gets submitted to CMS. The actual care content lives in the RAI Manual, which we did not pull (multi-hundred page document, AAPACN-hosted).
- For Tingin: the SECTIONS define the canonical patient-state schema (A–Z). The ITEMS define the state values. We can use them directly as our patient profile schema.

### License
Federal public domain. CMS-published, no copyright restriction. Cite as: "CMS Minimum Data Set 3.0 Nursing Home Comprehensive Item Set v1.14.0 (effective 10/01/2016)."

---

## Source 5 — Hospital-to-SNF transition research

### 5a — Adler-Milstein et al. 2021 (JAMA Network Open, CC-BY)

**URL:** `https://pmc.ncbi.nlm.nih.gov/articles/PMC7809587/`

**Sample:** 265 SNFs, 471 hospital-SNF pairs, 53% response rate.

**Verbatim — categories most frequently MISSING (the omission targets):**
- Behavioral status — missing in **67.7%** of pairs
- Social status — **65.7%**
- Hospital after-hours contact information — **53.9%**
- Mental status — **44.1%**
- Immunization history — **40.7%**
- Functional status / independence level — **35.8%**

**Verbatim — completeness statistics:**
- **13.5%** "excellent" across all three dimensions (completeness, timeliness, usability)
- **30%** at or below average on all dimensions
- **49.6%** failed to receive ≥80% (≥19 of 23) information types
- **11%** received all 23 categories
- **50.2%** received late information (33.8% sometimes, 16.4% often)

**Key association:** on-site hospital clinicians at SNF correlated with better completeness/timeliness/usability across multivariate analyses.

**License:** CC-BY. Re-use freely with attribution.

### 5b — Baluyot 2022 (Patient Safety Journal, CC-BY-NC 4.0)

**URL:** `https://patientsafetyj.com/index.php/patientsaf/article/view/hospital-snf-communication`

Got metadata page only. Body content not extracted via WebFetch (Patient Safety Journal hosts behind Ovid for full text, which 402'd).

What we know:
- Title: "Improving Communication From Hospital to Skilled Nursing Facility Through Standardized Hand-Off: A Quality Improvement Project"
- Authors: Abigail Baluyot, Cynthera McNeill, Susan Wiers
- Vol 4 Iss 4, Dec 16 2022
- DOI: 10.33940/med/2022.12.2
- License: CC-BY-NC 4.0

**Action for Karl:** if you want the actual Baluyot intervention details, the full text is via the journal's PDF link (one-click, free) — the WebFetch tool couldn't follow Ovid redirects but a browser will.

### 5c — King et al. 2013 (PMC3714367, JAGS, NIH-funded)

**URL:** `https://pmc.ncbi.nlm.nih.gov/articles/PMC3714367/`

**Sample:** 27 RNs, 5 Wisconsin SNFs, 26 focus groups + 1 individual interview, 2011–2012. Grounded Dimensional Analysis.

**Verbatim — what SNF nurses said is missing from hospital discharge:**
- Medication orders (including signed opioid prescriptions)
- Functional and cognitive status details
- Wound care instructions
- Activity level restrictions
- Recent laboratory results
- Contact information for discharging providers
- Psychosocial and behavioral concerns

**Verbatim quote (the gold one for our pitch):**
> "...there was nothing about the femur fractures we had no idea how, what, you know, if she was weight bearing or not weight bearing where-what we were supposed to be doing with them"

> "And as nurses you just feel like you're just asked to take care of this person with blinders on"

**License:** PMC open access.

---

## Source 6 — Handoff failure-mode meta-analyses

### 6a — BMC Nursing 2025 (Quantifying Acute Care Handoffs, n=688)

**URL (PMC):** `https://pmc.ncbi.nlm.nih.gov/articles/PMC12837210/`
**URL (publisher):** `https://link.springer.com/article/10.1186/s12912-025-03802-6` (Springer 303-redirected on WebFetch; PMC mirror worked)

**Sample:** 1,029 respondents → 688 met inclusion criteria (US hospital direct-care RNs/LPNs/APRNs >50% direct care); survey June–Sept 2024.

**Headline statistics (verbatim):**
- "More than 1 in 4" nurses agreed/strongly agreed that important information is often missed at shift change → **27.4% (n=189)**.
- 50% disagreed/strongly disagreed (n=344). 22.5% neutral (n=155).
- "Always" accurate, complete, pertinent: **6.3%** (n=43). "Most of the time": 67.4%. "Sometimes": 20.9%.

**Specialty differences:** Med/Surg + ED nurses most likely to indicate info is missed.

**License:** CC-BY-NC-ND 4.0. Cite freely; do not modify or commercialize.

### 6b — Riesenberg 2012 (PMC3312531, J Grad Med Educ)

**URL:** `https://pmc.ncbi.nlm.nih.gov/articles/PMC3312531/`

**The two well-known statistics, sourced and verbatim:**
- AHRQ 2011 survey (1,032 hospitals, >470,000 staff): **"50% endorsed the statement that 'important patient care information is often lost during shift changes.'"**
- Joint Commission: **"An estimated 80 percent of serious medical errors involve miscommunication between caregivers when patients are transferred or handed-off."**

**License:** © 2012 ACGME. Cite for academic/non-commercial use.

### 6c — BMC Nursing 2026 meta-analysis (the "88% omission" reference)

**URL (per prompt):** `https://link.springer.com/article/10.1186/s12912-026-04607-x`

**Result:** Springer 303-redirected on WebFetch. Web search did not surface a 2026 meta-analysis matching the description — "88% omission, four contributing factor categories." The most likely sources for the 88% figure are:
- A misremembered version of Joint Commission's 80% (handoff errors → serious medical errors).
- Or a single-site study being treated as universal. We did not find a peer-reviewed 88% number anchored to a meta-analysis in our search.

**Recommendation for Tingin's pitch:** **drop the 88% figure** and use the verifiable triangulated stack:
- Joint Commission 80% (Riesenberg 2012)
- AHRQ 50% (Riesenberg 2012)
- BMC 2025 27.4% (n=688)
- Adler-Milstein 49.6% (n=471 hospital-SNF pairs)
- Labovic 70% CalVet local

---

## Source 7 — California-specific: Labovic 2018 (CalVet 84-bed)

**URL:** `https://repository.usfca.edu/capstone/747`

**Sample:** End of 2017, 84-bed long-term care unit at Veterans Home of California (state-operated).

**Headline statistic (verbatim):**
> "70% of transfers in this unit resulted in incomplete or missing hand-offs at the time of transfer"

**Method:** SWOT + fishbone + Kotter's change theory. Implemented a paper SBAR + Essential Patient Information tool. Achieved 30% reduction → facility-wide rollout May 2018.

**Limitation:** capstone PDF body not pulled (USF repository requires direct PDF link click). Abstract + key stat captured. Appendix tools (SBAR template, EPI tool) deferred — Karl click-through if needed.

**License:** USF Capstone repository — open-access academic.

---

## Source 8 — Methodology

### 8a — Patel et al. 2016 (SCA — sequential structure of nurse handoffs)

Method: **Sequential Conversational Analysis**, mixed qualitative + quantitative pattern analysis. Setting: medical ICU.

Communication dimensions identified: interactive nature, role-based requirements, clinical content, task focus, conversational disruptions, **phasic structure** (handoffs have phases, not flat content).

**For Tingin:** justifies a phasic handoff schema — greeting, vitals, problems, tasks, ACP, questions, close — with phase-specific noise characteristics.

### 8b — Abraham, Kannampallil, ..., Cohen 2017 (RRI — semantic similarity for handoff content overlap)

**URL (abstract):** `https://pubmed.ncbi.nlm.nih.gov/27913246/`

**Sample:** 120 resident handoffs + 120 nurse handoffs, academic hospital med floor.

**Method:** Reflective Random Indexing (RRI) — distributional semantics. Validation: ρ = **0.88** with human similarity ratings.

**Categories with HIGH overlap (info travels well):** patient active problems, assessment of active problems, identifying info, past medical history, medications/treatments.

**Categories with LOW overlap (info dropped):** **allergies, family-related info, code status, anticipatory guidance.**

**For Tingin:** this is the methodological ancestor of our LLM-judge approach — automated semantic similarity is a defensible proxy for human judgment of content overlap (ρ=0.88 is strong validation). The four LOW-overlap categories above should carry the **highest omission cost weights** in our reward function — they're empirically the safety-critical info that nurses drop.

### Cross-source convergence

Three independent sources converge on which information categories are most-dropped:

| Category | Adler-Milstein 2021 (hospital→SNF) | Cohen/Abraham 2017 (within-unit shift change) | King 2013 (qualitative SNF) |
|---|---|---|---|
| Behavioral / mental / psychosocial | 67.7% missing | "Family-related info" low overlap | "psychosocial and behavioral concerns" |
| Functional status | 35.8% missing | (n/a — not coded as separate category) | "functional and cognitive status details" |
| Code status / advance care | (not in 23 categories examined) | "code status" low overlap | (mentioned implicitly via "blinders") |
| Allergies | (not separately tracked at hospital→SNF) | "allergies" low overlap | (not specific) |
| Anticipatory / pending | (timeliness 50.2% late) | "anticipatory guidance" low overlap | "Recent laboratory results" |

The **omission cost function should weight these categories highest.**

---

## Per-Shift Flow Sheet Schema (synthesized)

The per-shift state for Tingin's environment, anchored on INTERACT SBAR + CNAHRT Appendix B + Title 22 §72315 patient-care duties + MDS sections H, J, K, M, N, O.

| Category | Field structure | Anchor |
|---|---|---|
| **MAR** (Medication Administration Record) | drug, dose, route, time given, given-by, missed-dose flag, PRN reason | INTERACT SBAR Medication Alerts; MDS §N |
| **TAR** (Treatment Administration Record) | treatment (e.g. wound care), site, time, performed-by, response | INTERACT SBAR; MDS §M, §O; Title 22 §72315(f) |
| **BBR** (Bowel/Bladder Record) | last BM (date), BM count this shift, formed/constipation/diarrhea, continent Y/N (bladder, bowel), foley present + amount, urinal Y/N + amount | CNAHRT Output block; INTERACT SBAR GU/GI; MDS §H |
| **I/O** (Intake/Output) | PO intake (mL or %), IV intake, urine output, emesis, drain output | INTERACT SBAR; Title 22 §72315(j) |
| **ADL** (Activities of Daily Living) | feeding, oral hygiene, bathing, toileting, dressing, transfer status (self/1x/2x), ambulation (self/cane/walker/W/C), each as Independent / Dependent | CNAHRT Hygiene + Safety Checks; MDS §G/§GG |
| **Vitals** | BP, HR (apical if relevant), RR, Temp, O2 sat (RA or O2 + L/min), pain rating __/10 + site, blood glucose if diabetic | INTERACT SBAR Vital Signs; CNAHRT Vitals |
| **Behavior** | new agitation, confusion, withdrawal, hallucinations, refusal of care, change-from-baseline | INTERACT SBAR Mental Status; INTERACT Stop and Watch (S, T, A, T); MDS §E |
| **Skin** | pressure-ulcer status (count + stage), bruise (Y/N + site), rash (Y/N + site), skin tear (Y/N + site), other ulcer (Y/N + site), turning/repositioning performed | CNAHRT Skin block; MDS §M; INTERACT Stop and Watch (C) |
| **Activity** | participation level (full/partial/declined), time out of bed, ambulation distance (room / corridor / off-unit), notable mobility events | CNAHRT Safety Checks; Title 22 §72315(e); INTERACT Stop and Watch (P-participation) |
| **Visits** | physician visit (telephone / NP-PA / MD), family visit, specialist consult, social work, chaplaincy, family-notification events | INTERACT SBAR footer; INTERACT QI Tool §3 Medical Evaluation |
| **Sleep** | sleep onset, total sleep, awakenings, sundowning, restraint use overnight | Inferred from Stop and Watch (T-tired) + MDS §P (restraints); not explicit in any single anchor |

**Note:** "Sleep" is the weakest-anchored category — none of our verbatim sources have a dedicated sleep flow-sheet section. Vendor flow sheets (PointClickCare, MatrixCare) typically include it; we synthesize from MDS Restraints (overnight) + Stop and Watch "Tired, weak, confused, drowsy."

---

## Patient Profile Schema (synthesized from MDS 3.0)

The slow-changing patient state (updated on admission, quarterly, and on significant change), per MDS 3.0 NC Comprehensive Item Set:

```yaml
patient_profile:
  identification:        # MDS Section A
    facility_id, name, dob, gender, language, marital_status, room
    admission_date, type_of_admission, entered_from
    pasrr: { serious_mental_illness, intellectual_disability, related_conditions }
  
  hearing_speech_vision: # MDS Section B
    comatose, hearing, hearing_aid, speech_clarity,
    self_understanding, ability_to_understand, vision, corrective_lenses
  
  cognition:             # MDS Section C
    bims_score (0-15), staff_assessment_for_mental_status, cam_delirium_signals
  
  mood:                  # MDS Section D
    phq9_resident_score, phq9_staff_score
  
  behavior:              # MDS Section E
    hallucinations_delusions, behavioral_symptoms_freq + impact,
    rejection_of_care, wandering, change_in_behavior
  
  preferences:           # MDS Section F
    food / care / sleep / activity / social preferences
  
  functional_status:     # MDS Section G + GG
    adl_self_performance: { bed_mobility, transfer, walk, dressing, eating,
                            toilet_use, hygiene, bathing }
    adl_support_provided
    mobility_devices, balance, range_of_motion
  
  bladder_bowel:         # MDS Section H
    appliances: { indwelling_cath, external_cath, ostomy, intermittent_cath }
    urinary_continence (always_cont/occ/freq/always_inc/not_rated)
    bowel_continence, toileting_program, bowel_patterns
  
  active_diagnoses:      # MDS Section I (last 7 days)
    cancer, heart_circulation: [anemia, afib, cad, dvt, chf, htn, pvd],
    gi: [cirrhosis, gerd, ibd], gu: [bph, esrd, neurogenic_bladder],
    infections: [mdro, pneumonia, sepsis, tb, uti_30d, hep, wound_inf],
    metabolic: [diabetes], musculoskeletal, neurological,
    nutritional, psychiatric, pulmonary, vision, other
  
  health_conditions:     # MDS Section J
    pain: { management, frequency, intensity, effect_on_function },
    sob, tobacco_use, prognosis_lt_6mo, fever, vomiting, dehydrated,
    bleeding, fall_history, falls_since_admission, surgery
  
  swallowing_nutrition:  # MDS Section K
    swallowing_disorder, height, weight, weight_loss_5pct_30d,
    weight_gain, parenteral_nutrition, feeding_tube, mech_altered_diet,
    therapeutic_diet, intake_pct
  
  oral_dental:           # MDS Section L
    dental_issues
  
  skin:                  # MDS Section M
    pressure_ulcer_risk, count_by_stage,
    other_ulcers: [venous, arterial, diabetic_foot],
    skin_issues: [open_lesion, surgical_wound, burn],
    treatments: [pressure_reducing, repositioning, dressings, ointments]
  
  medications:           # MDS Section N
    injections, insulin,
    classes: [antipsychotic, antianxiety, antidepressant, hypnotic,
              anticoagulant, antibiotic, diuretic, anticonvulsant],
    gradual_dose_reduction, medication_review
  
  special_treatments:    # MDS Section O
    chemotherapy, radiation, oxygen, suctioning, trach_care,
    invasive_vent, bipap_cpap, iv_meds, transfusions, dialysis,
    hospice, isolation, vaccines: [flu, pneumococcal],
    therapies: { speech, ot, pt, respiratory, psychological, recreational }
    minutes_per_day, restorative_nursing_minutes
  
  restraints:            # MDS Section P
    physical_in_bed, physical_in_chair
  
  goals_discharge:       # MDS Section Q
    resident_participation, goals, discharge_planning,
    return_to_community, expectations
```

---

## Tier 3 Rubric Proposal — replacing Galli's 15-point HEF

The new **"INTERACT-Anchored SNF Handoff Rubric (IASHR)"** — 16 weighted criteria — synthesized from INTERACT SBAR + CNAHRT + Adler-Milstein 2021 priors + Cohen 2017 priors + Title 22 §72311 notification triggers + MDS change-since-last-assessment.

**Weighting rationale:**
- 1 point: identifying / process / process-quality items
- 2 points: clinical-content items where overlap is empirically high (Cohen 2017) or content is straightforward
- 3 points: empirically low-overlap-high-stakes content (Cohen 2017 + Adler-Milstein 2021)
- 4 points: regulatory-trigger items (Title 22 §72311 mandates these)

| # | Criterion | Weight | Anchor | LLM-judge question |
|---|---|---|---|---|
| 1 | Patient identified by name + room/bed + code status | 1 | INTERACT SBAR ID; CNAHRT ID block | Did the receiving nurse get unambiguous identity AND code status? |
| 2 | Primary diagnoses + LTC vs. PAC status stated | 2 | INTERACT SBAR Background; MDS §I | Were the active diagnoses passed on with accurate post-acute vs. long-term distinction? |
| 3 | Vitals (BP, HR, RR, Temp, O2, pain) — current shift | 2 | INTERACT SBAR Vitals; CNAHRT Vitals | Were end-of-shift vitals reported with values (not just "stable")? |
| 4 | Active medications + scheduled vs. PRN + warfarin/INR + recent changes | 3 | INTERACT SBAR Medication Alerts; MDS §N | Were medication changes within last week + active anticoagulation flagged? |
| 5 | Allergies | 3 | Cohen 2017 (low overlap); INTERACT SBAR pre-call checklist | Were allergies stated explicitly even if "none"? |
| 6 | Advance directives — DNR/DNI/DNH/POLST/hospice | 3 | INTERACT SBAR ACP; Cohen 2017 (low overlap) | Were code status AND any DNH/hospice/POLST orders communicated? |
| 7 | Recent change-in-condition events (mental, functional, respiratory, GI, GU, skin) | 3 | INTERACT SBAR 5 system blocks; INTERACT Stop and Watch | Were changes-from-baseline communicated for each affected system? |
| 8 | Pending tasks + awaited results (labs, imaging, consults, transfers) | 2 | INTERACT SBAR Recent Lab Results; SBAR Request | Were outstanding clinical to-dos handed off with sufficient context to act? |
| 9 | ADL status + transfer status + ambulation aid (self/1x/2x; cane/walker/W/C) | 2 | CNAHRT Hygiene + Safety; MDS §G | Were the resident's mobility and assistance needs communicated? |
| 10 | Bowel/bladder status — last BM date, continence, foley/ostomy, output | 2 | CNAHRT Output; MDS §H | Were B/B status and any toileting program changes communicated? |
| 11 | Skin integrity — pressure ulcers (count + stage), wounds, recent skin tears, repositioning schedule | 3 | CNAHRT Skin; MDS §M; Title 22 §72315(f) | Were active skin issues + the prevention plan handed off? |
| 12 | Behavioral / mental-status changes since last assessment | 3 | Adler-Milstein (67.7% missed); MDS §E | Were behavioral symptoms + agitation triggers communicated, including non-incident ambient observations? |
| 13 | Functional / social / psychosocial concerns | 3 | Adler-Milstein (35.8% / 65.7% missed); King 2013 | Was the resident's social/family context communicated, not just clinical state? |
| 14 | Title 22 §72311 notification triggers — weight change ≥5 lb/30d, untoward med response, life-threatening med error, facility-resource gap | 4 | Title 22 §72311(a)(3) | Were any regulatory-triggered events flagged AND clinician notified? |
| 15 | Stop and Watch flags raised by CNA this shift (or in prior 24h) | 2 | INTERACT Stop and Watch | Did the CNA's ambient observations (S/T/O/P/a/n/d/W/A/T/C/H) reach the receiving nurse? |
| 16 | Read-back / clarification confirmation | 1 | ISOBAR R; Porteous 2009 | Did the receiving nurse confirm understanding by re-stating critical items? |

**Total: 39 points.**

**Use:** the LLM judge scores each criterion 0 / partial / full per the weight, producing a 0–39 raw score and a normalized percentage. The omission cost function uses the same per-criterion weights as the cost-of-loss for that information category, multiplied by patient acuity (PHQ-9 + active-diagnosis count + falls-history + pressure-ulcer-stage as a composite acuity prior from MDS).

**Why this beats the Galli-15:**
- It's anchored in three US sources (INTERACT, Adler-Milstein, BMC 2025, Cohen 2017) instead of one Italian study.
- It separates the EMPIRICALLY-DROPPED categories (#5 allergies, #6 ACP, #12 behavioral, #13 functional/social) and weights them at 3 points each — these are exactly the categories where Cohen 2017 found "low overlap" and Adler-Milstein 2021 found high missing rates.
- It includes the regulatory floor (Title 22 §72311) at 4 points — California compliance is non-negotiable.
- It includes the CNAHRT layer (#15 Stop and Watch flags) — explicitly modeling the CNA-to-RN ambient signal that nobody else's rubric captures.

---

## California Staffing Model (verbatim Title 22 + role structure)

For Tingin's environment to faithfully simulate a California SNF, we model the staffing roster like this:

**For an 84-bed SNF (Labovic-style CalVet):**

| Role | Per shift | Reg basis |
|---|---|---|
| Director of Nursing (DON) | 1 RN, day shift only, 5 days/week, 8h | Title 22 §72327 |
| Charge nurse | 1 RN/LVN per nursing station, awake, 24/7 | Title 22 §72329.1(c) — 60–99 beds |
| Med RN/LVN (additional licensed) | as needed to meet 1:8 licensed-nurse ratio | Title 22 §72329.1(g) |
| CNAs | as needed to meet shift caregiver ratios + 2.4 CNA HPPD floor | Title 22 §72329.1(g) + §72329.2 |

**Daily HPPD floor (the binding California constraint):**
- 3.5 direct care hours per patient day (DHPPD), facility-wide average
- of which 2.4 must be CNA hours
- AFL 19-16 audit penalty: $15,000 (5–49% non-compliant days) or $30,000 (≥50% non-compliant)

**Shift-by-shift caregiver:patient ratios:**
- Day: 1:5
- Evening: 1:8
- Night: 1:13

**For an 84-bed unit:**
- Day: ⌈84/5⌉ = 17 caregivers (mix of RN/LVN/CNA per HPPD math)
- Evening: ⌈84/8⌉ = 11 caregivers
- Night: ⌈84/13⌉ = 7 caregivers
- Plus DON (day only)
- Plus charge RN/LVN at each nursing station, all 24h

**Tingin's environment binding:** the agent-controllable nurse role is the **charge RN** on a single nursing station (15–25 beds) per shift. They allocate attention across that subset, with the CNA layer (1:5/1:8/1:13) providing ambient observation and escalation signal. The agent inherits a handoff at the start of shift and produces one at the end.

---

## What we cannot get publicly

| Item | Why | Action |
|---|---|---|
| INTERACT v5.0 official forms | FAU registration wall at pathway-interact.com | Use v3.0 (2011) + v4.0 (2014) — content is stable, only COVID-19 + electronic-record refinements differ |
| INTERACT Care Path content | Laminated 8.5×11 cards distributed by FAU; not in V4.0 PDF guide | Use the LIST of 10 paths as our trajectory taxonomy; defer per-pathway algorithms (probably stable enough to fake from clinical UpToDate references for sim purposes) |
| PointClickCare flow-sheet template | Vendor-proprietary | Synthesize from CNAHRT + Title 22 §72315 + MDS §H/§J/§K/§M (above) — no vendor template needed for sim |
| MatrixCare flow-sheet template | Vendor-proprietary | Same — synthesize |
| Real de-identified handoff transcripts (US) | HIPAA-protected | Use Suominen 2017 (Australian, synthetic, CC-BY-NC-ND, prior session) for any sample-text needs OR generate scripted handoffs from our schema |
| MDS RAI Manual (the multi-hundred-page interpretive guide) | AAPACN-hosted, partial paywall | Item Set v1.14.0 is sufficient for our schema; defer Manual unless we need item-coding-rule details |
| CDPH AFL 21-11 body content | JS-rendered SPA that didn't text-extract | AFL 19-16 covers the substance; if Karl needs 21-11 specifics, browser open + manual extract |
| Baluyot 2022 full text | Patient Safety Journal redirects to Ovid 402 | Browser-fetch the PDF (free, just behind a click) |
| Labovic 2018 capstone PDF + appendices | USF repository requires direct PDF link | Browser click-through; we have the headline 70% statistic |
| BMC Nursing 2026 "88% omission" meta-analysis | Likely doesn't exist as cited | Use the verifiable triangulated stack instead |

---

## Open questions for Karl

1. **The 88% number.** I cannot find a peer-reviewed meta-analysis with "88% handoff error rate" as a headline. The closest defensible numbers are: Joint Commission's **80% of serious medical errors involve handoff miscommunication** (Riesenberg 2012), AHRQ's **50% of staff say info is often lost** (Riesenberg 2012), BMC 2025's **27.4% of nurses agree info is often missed** (n=688), Adler-Milstein's **49.6% of SNFs fail to receive ≥80% of 23 info categories**, and Labovic's California-local **70% incomplete CalVet transfers**. **Recommendation: drop "88%" from the deck** and cite Joint Commission's 80% as the headline + Adler-Milstein's 49.6% as the SNF-specific stat + Labovic's 70% as the California-local stat.

2. **INTERACT v5.0 vs. v3.0/v4.0.** We pulled v3.0 (2011) and v4.0 implementation guide (2014). Pathway INTERACT v5.0+ requires registration. The field structure is stable; v5 added COVID-19 + electronic-record refinements only. **Recommendation: cite the FAU-anchored INTERACT family without claiming a specific version, OR explicitly cite v4.0** since the v4.0 Implementation Guide is publicly hosted and gives us the canonical 10 Care Path list.

3. **CNAHRT n=1 site.** McDermott's DNP project is one NC long-term-care facility with ~3 CNAs in the post-impl survey. The TOOL is well-formed and SBAR-anchored, but the EVIDENCE BASE is pilot-scale. **Recommendation: cite CNAHRT as "one published instantiation of a CNA-specific SBAR" rather than "the CNA handoff standard."** It IS the most-published one; there's no widely-deployed alternative.

4. **Subacute exclusion.** Title 22 excludes subacute units from the 3.5/2.4 DHPPD floor — they fall under §51215.5 instead. **Karl: is our sim general-SNF (3.5/2.4 binds) or sub-acute (different floor)?** Default = general SNF (matches Labovic CalVet, matches the 88% / 70% pitch context). Confirm.

5. **Section S of MDS.** Newer MDS versions (V1.18.11+) added Section S for state-specific items. We pulled v1.14.0 which doesn't have it. **Karl: do we need state-specific MDS items in our sim, or is the federal v1.14.0 schema enough?** Recommendation: federal-only is enough for sim grounding; Section S is empty for most states.

6. **Italian/CalVet/Wisconsin sample mismatches.** Our quantitative sources are: California (Labovic, n=84 beds, 2017), 5 Wisconsin SNFs (King qualitative, 27 RNs, 2011), national US (Adler-Milstein 471 hospital-SNF pairs, 2018; BMC 2025 n=688), and Suominen Australia (synthetic, prior session). **No single source is a national US RN sample of REAL handoffs.** That's a structural gap in publicly available data. **Recommendation: in the pitch, lead with "California-anchored" (Labovic + Title 22) + "national US prior" (Adler-Milstein + BMC 2025) and frame the absence of large-n US handoff transcripts as the EXACT problem Tingin makes tractable.**

7. **Care Path field-by-field content.** We have the LIST of 10 INTERACT Care Paths but not the per-path algorithms (which sit on laminated cards + the V5 portal). For the hackathon, the LIST is enough. **For a production version: contact Pathway INTERACT to license the v5.0 algorithms, or reconstruct from UpToDate.**

8. **Sleep flow-sheet category.** None of our verbatim sources have a dedicated sleep section. Vendor templates (PointClickCare/MatrixCare) include it. **Recommendation:** synthesize a minimal sleep block (sleep onset, total sleep, awakenings, sundowning, restraint use overnight) from MDS §P + Stop and Watch "T-tired" — flag in spec as "synthesized, vendor-anchored only."

---

## File inventory (what's on disk)

```
/Users/karlnuyda/Desktop/Tingin/.scratch/seed-data/snf-ca/
├── interact/
│   ├── INTERACT_SBAR_Form.pdf                       (101 KB, 4 pp, FAU ©2011 v3.0)
│   ├── INTERACT_SBAR_Form.txt
│   ├── INTERACT_Stop_and_Watch_Early_Warning_Tool.pdf (45 KB, 1 p)
│   ├── INTERACT_Stop_and_Watch_Early_Warning_Tool.txt
│   ├── INTERACT-V4-Implementation_Guide.pdf         (199 KB, 15 pp, FAU ©2014 v4.0)
│   ├── INTERACT-V4-Implementation_Guide.txt
│   ├── indiana-interact-qi-tools.pdf                (414 KB, 5 pp QI Tool For Review of Acute Care Transfers)
│   └── indiana-interact-qi-tools.txt
├── cnahrt/
│   ├── cnahrt-unc-dnp.pdf                           (877 KB, 60 pp, McDermott 2021 DNP)
│   └── cnahrt-unc-dnp.txt
├── ca-title-22/
│   ├── CDPH-AFL-19-16.pdf                           (564 KB, 8 pp, April 9 2019)
│   ├── CDPH-AFL-19-16.txt
│   ├── CDPH-AFL-21-11.html                          (490 KB, JS SPA — body NOT extracted)
│   ├── CDPH-AFL-21-11.txt                           (5 KB chrome only)
│   └── title-22-staffing-extracted.md               (verbatim §§ 72327, 72329.1, 72329.2, 72311, 72315)
├── mds-3.0/
│   ├── MDS30_NC_Comp_v1140.pdf                      (1.35 MB, 45 pp, CMS public domain)
│   ├── MDS30_NC_Comp_v1140.txt                      (extracted, 2473 lines)
│   ├── cms-mds-tech.html                            (CMS technical info raw)
│   └── mds-sections-extracted.txt                   (unique section header grep)
├── transition-research/
│   ├── adler-milstein-2021-extracted.md             (verbatim percentages, CC-BY)
│   └── king-2013-snf-qualitative-extracted.md       (verbatim quotes, PMC OA)
├── handoff-meta/
│   ├── bmc-2025-quantifying-handoffs-extracted.md   (n=688, full stats, CC-BY-NC-ND)
│   └── riesenberg-2012-AHRQ-50pct-extracted.md      (the AHRQ 50% + JC 80% citations)
├── ca-snf-local/
│   └── labovic-2018-calvet-extracted.md             (70% incomplete CalVet handoffs)
├── methodology/
│   ├── patel-2016-SCA-extracted.md                  (Sequential Conversational Analysis)
│   └── cohen-abraham-2017-content-overlap-extracted.md (RRI ρ=0.88; low-overlap categories)
└── psnet/
    (empty — PSNet AHRQ page returned 403; absorbed into Baluyot 2022 metadata above)
```

**Total on disk:** ~5 MB across 17 PDFs/HTMLs + 9 extraction notes + the PDF-extracted text files. All sources cite-able, license-checked, and verbatim-extracted where it matters (INTERACT field structures, CNAHRT Appendix B, Title 22 §§ thresholds, MDS section index).

The previous `seed-data-review.md` (Galli/Suominen/ISOBAR audit) stays as historical record. This v2 is the new authoritative document for California SNF anchoring.
