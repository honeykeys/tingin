# Seed Data Review — 2026-04-25

## TL;DR
- **Galli 2025** — usable. Repo cloned. Contents are **scored numeric data only (no raw handover text)** — but the column headers ARE the HEF rubric, so we have a 15-point Italian-ED-validated nursing handover scoring instrument verbatim. Sample n = 867 handover events (526 pre, 341 post). License: not stated (no LICENSE file, no README content).
- **Suominen 2017** — usable in principle, but **redistribution forbidden by CC BY-NC-ND 4.0** + "All Rights NICTA 2014". Open access to view + non-commercial use, no derivative works. We have the metadata, structure, file inventory by folder; the actual TXT/DOCX corpus would require pulling from CSIRO portal interactively. **Karl needs to make the call** on whether to download samples for sim grounding (allowed under CC-NC-ND for academic use as long as we don't redistribute or modify), but we cannot ship samples in the demo or the repo.
- **ISOBAR MDS** — partially usable. Got the Royal Hobart Hospital overarching SOP (Sept 2008) — gives the 5-step minimum data set verbatim. Got a real worked-example template (St John WA 2020 ISOBAR Patient Handover form) that shows the canonical letter expansion populated as fillable form fields. **The RHH SOP itself does not include a worked-example handover with patient-specific text** — that would require obtaining the unit-specific SOPs (nursing-ED, nursing-general-medicine, etc.) directly from ACSQHC.

**Quality assessment for our use:** Sufficient for sim grounding and Tier 3 rubric design. Sufficient for an honest pitch citation of "real-world-derived rubric structure." Not sufficient for "we trained on real handover transcripts" claims (Galli has no transcripts; Suominen has corpus but ND license blocks training-data redistribution; ISOBAR is a spec, not a corpus).

---

## Source 1 — Galli et al. 2025

### Access
- Original URL given (`https://github.com/alessiagalli/Database-Galli-et-al`) is **404**. Correct URL has a trailing dot: `https://github.com/alessiagalli/Database-Galli-et-al.` — that surprised the WebSearch + initial git clone.
- Cloned successfully to `/Users/karlnuyda/Desktop/Tingin/.scratch/seed-data/galli-2025/`.
- Repo created 2024-10-21, last pushed 2024-10-21. No commits since. No license file. No GitHub topics. README is just the repo name — no documentation.

### Contents
```
galli-2025/
  README.md          23 bytes  ("# Database-Galli-et-al.")
  PRE_POST.xlsx     157 KB    (3 sheets, Italian)
```

The xlsx has three sheets:
- **Foglio1** — 994 rows × 30 columns. The actual scored handover data, one row per observed handover. All numeric (no free-text handover transcripts). 526 PRE rows + 341 POST rows = **867 scored handover events total**.
- **Foglio2** — pre/post counts split by shift type (cross-tab summary).
- **Foglio3** — 298 rows × 5 columns. Score percentages stratified by experience level (≤5 years vs >5 years).

**Critical finding:** there are no raw handover transcripts here. Only numeric scores per HEF item. The column headers ARE the rubric.

### HEF Rubric (verbatim, then translated)

Reconstructed from `Foglio1` row 1 column headers — these are the items each handover was scored against:

| # | Italian header (verbatim) | English | Max points |
|---|---|---|---|
| 1 | PUNTEGGIO CONSEGNA SCRITTA | Written handover present | 1 |
| 2 | PUNTEGGIO IDENTIFICAZIONE PZ | Patient identification | 1 |
| 3 | PUNTEGGIO LOCALIZZAZIONE PZ | Patient location | 1 |
| 4 | PUNTEGGIO PROBLEMA PRINCIPALE | Main (presenting) problem | 1 |
| 5 | PUNTEGGIO COMORBIDITA' | Comorbidities | 2 |
| 6 | PUNTEGGIO PRESIDI | Devices / lines / catheters | 2 |
| 7 | PUNTEGGIO INFUSIONI | Infusions / IV drips | 2 |
| 8 | PUNTEGGIO COSA HA FATTO | What has been done | 1 |
| 9 | PUNTEGGIO COSA E' EMERSO | What has emerged (new findings during shift) | 1 |
| 10 | PUNTEGGIO COSA ATTENDE | What is awaited (pending results, transfers, consults) | 1 |
| 11 | PUNTEGGIO ATTIVITA' IN CONSEGNA | Active tasks in handover (e.g. ongoing care) | 2 |

**Total: 15 points** (column header confirms: `TOT PUNTEGGIO (in quindicesimi)` = "TOTAL SCORE in fifteenths").
Reported as raw, partial-fraction, percentage of 15.

Other recorded covariates per handover row:
- Shift type (1=morning→afternoon, 2=afternoon→night, 3=night→morning)
- Postazione / station (1=box, 2=ex-OBI, 3=sala 6, 4=OBI, 5=sala 4, 6=sala EM)
- Number of patients present
- Time spent per single patient handover (minutes)
- Years of service of donating nurse (DE) and receiving nurse (PS), 6-bucket scale
- Age bucket and sex of nurses

### Sample records (raw quoted)

Foglio1 row 1 (a PRE handover):
```
PRE/POST=1, shift=3 (night→morning), station=1 (box), n_patients=4,
time_min=1, written=1, ID=1, location=1, main_problem=1, comorbidities=None,
devices=None, infusions=0, what_done=1, what_emerged=1, what_awaited=1,
active_tasks=None  →  partial=7, total_points=9, normalized=11.67/15 (77.8%)
nurse_DE_yrs=6 (>10y), nurse_PS_yrs=6, age=4 (>50), sex=2 (F)
```

Foglio1 row 2:
```
PRE/POST=1, shift=1 (morning→afternoon), station=2, n_patients=8, time_min=1.5,
written=1, ID=1, loc=1, main=1, comorb=1, devices=0, infusions=None,
done=1, emerged=None, awaited=1, active=2  →  partial=9, total=10, 13.5/15 (90%)
nurse_DE=5 (5-10y), PS=5, age=2 (30-39), sex=1 (M)
```

Foglio1 row 7:
```
PRE=1, shift=3, station=1, n_patients=5, time=1, written=1, ID=1, loc=1, main=1,
comorb=None, devices=0, infusions=0, done=1, emerged=1, awaited=1, active=2
→ partial=9, total=13, 10.38/15 (69.2%)
nurse_DE=6 (>10y), PS=6, age=2, sex=1
```

**Texture note:** the data is dense and clean. Nurses with >10 years of service skipped 'comorbidities' and 'devices' on busy night→morning handovers. The 'what is awaited' field was almost always populated. The 'active tasks in handover' field had the most missing data — that's a signal of where omission lives in this ED.

### Limitations
- **No raw handover text.** This is purely a scoring dataset, not a transcript corpus. Cannot use for LLM training-data citations.
- **Italian only**, single-site (one ED, in Italy — the paper says Ancona ED based on Menditto's affiliation, but I could not verify the specific city from the repo or from accessible paper sections).
- **Headers in Italian** — translation above is mine, not authoritative.
- No raw audio, no demographics about patients (only nurses).

### License
**No LICENSE file in repo. No license statement in README.** This is a flag — public GitHub repos without a license are technically "all rights reserved" under default copyright. Karl should not redistribute the xlsx without contacting the authors. Internal use for analysis is fine; quoting the rubric structure (which is published in the open-access paper) is fine.

The companion paper (Springer Discover Health Systems) appears to be open-access based on the journal model, but I could not pull the body text — Springer is rate-limiting / 303-redirecting WebFetch attempts. **Karl should manually verify the paper's CC license and check its supplementary materials for the official HEF table** — a reproduction in the paper itself would be more authoritative than my reconstruction from xlsx headers.

---

## Source 2 — Suominen 2017 Synthetic Nursing Handover

### Access
- Page fetched. Dataset is "Open" / "Accessible for free" / "Accessible online."
- **DOI (audio):** `10.4225/08/58d0977ab4888` — handle `http://hdl.handle.net/102.100.100/44207`
- **DOI (text):** `10.4225/08/58d097ee92e95` — handle `http://hdl.handle.net/102.100.100/44208`
- **Companion text-only collection URL:** `https://data.csiro.au/collection/csiro:20413` (audio is `csiro:20372`)
- CSIRO portal landing page is a Vue SPA — required browser to render. Metadata accessible via DAP API (`https://data.csiro.au/dap/ws/v2/collections/{id}`).
- The CSIRO download link is direct (no login mentioned in metadata), but the landing page interaction would be needed to actually pull individual files. **No institutional auth required**, but the SPA is browser-only — I did not pull individual record files. If Karl wants samples, the cleanest path is to open the URL in a browser and download a Set 1 ZIP.

### Contents (per CSIRO collection metadata, verbatim from API response)

> "Both collections together comprise an open clinical dataset of three sets of 101 nursing handover records, very similar to real documents in Australian English. Each record consists of a patient profile, spoken free-form text document, written free-form text document, and written structured document."

**Set 1 (released June 2014) — folder structure:**
- `initialisation/` — DOCX + WMA files for Dragon Medical 11.0 speech-recognition initialisation
- `100profiles/` — 100 patient profiles (DOCX)
- `101writtenfreetextreports/` — 101 written, free-form text documents (TXT)
- `100x6speechrecognised/` — 100 speech-recognized written text outputs across six Dragon vocabularies (TXT)
- `101informationextraction/` — 101 written structured documents in CRF++ format with reference-standard text, features, and form categories

**Set 2 (April + November 2015):** 100 patient profiles + 100 written + 100 speech-recognized + 100 structured. Used as test set for CLEFeHealth 2015 Task 1a (clinical speech recognition) and validation for CLEFeHealth 2016 Task 1 (handover information extraction). The page warns: "please avoid its repeated use in evaluation – we do not wish to overfit."

**Set 3 (April 2016):** another 100 synthetic cases for evaluation.

**Total ≈ 300 records across 3 sets.** (Note: the audio collection's description redundantly says "3 X 100 audio files in WAV" while also saying "10 records" elsewhere on the page — that's a wording inconsistency in the source metadata, not in our data. Karl should treat ~300 records as the working number for the text corpus.)

### Sample records
**I did not download individual records.** The CSIRO portal is a Vue SPA and direct file downloads via API kept hitting 429 / 400 from this environment. Karl can pull samples by:
1. Browser → `https://data.csiro.au/collection/csiro:20413?tab=data`
2. Click "Download all data" or descend into folders.

The published reference standard (Suominen 2014) provides a written example schema. Per CSIRO description, each record's "structured document" is a CRF++-formatted information extraction reference — meaning the structured form has token-level labels for canonical handover slots. That's gold-standard structure for our Tier 2 (information-survival) layer.

### Limitations
- **Synthetic, not real** — built to mirror real Australian English handovers, intentionally HIPAA-clean. Good for building, not for clinical claims.
- **Australian English** — local idioms, drug names, ward conventions may differ from US/UK.
- **Limited free-form audio** — most analytical value is in the parallel structured-vs-free-form text pairs.
- **Not pulled to disk** — see access notes above.

### License
**Creative Commons Attribution-Noncommercial-No Derivatives 4.0 International Licence** with "All Rights (including copyright) NICTA 2014."

What this means for us:
- **Allowed:** view, download for non-commercial use, cite, paraphrase findings in academic/non-commercial settings.
- **Forbidden:** commercial use, derivative works, modifications, redistribution of files (including in our git repo).
- **Pitch:** can cite the dataset and our use for grounding ("we modeled topic coverage on Suominen 2017's reference-standard schema"). Cannot say we trained or fine-tuned on it without explicit permission.
- **Demo:** cannot ship sample text files or quote verbatim records (ND clause). Can describe the structure and quote tiny snippets under fair-dealing / quotation exception, but redistribution of the corpus is out.

---

## Source 3 — ISOBAR MDS

### Access
- Original URL was the safetyandquality.gov.au resource-library page. Curl had HTTP/2 errors and timeouts; WebFetch timed out. Worked around via Python urllib.
- **Pulled successfully:** Royal Hobart Hospital overarching SOP (Sept 2008), 484 KB, 79 pages → `/Users/karlnuyda/Desktop/Tingin/.scratch/seed-data/isobar-rhh-sop.pdf`. Text extracted to `isobar-rhh-sop.txt`.
- **Pulled successfully (via WebFetch indirection):** St John WA Ambulance ISOBAR Patient Handover form (Aug 2020 revision), 340 KB → `isobar-stjohn-wa-handover-form.pdf`. This is a real worked template showing the canonical letter expansion populated as fillable form fields.
- **Failed:** the supporting ISBAR-toolkit.pdf, Handover-ID-card.pdf, iSoBAR.pdf — all timed out from this environment after multiple retries. These are pocket-card / training materials, not the spec; the SOP and the St John WA form are sufficient.

### Contents

**File:** `isobar-rhh-sop.pdf` — "Royal Hobart Hospital National Clinical Handover Initiative: Nursing and Medical Handover in General Surgery, Emergency Medicine and General Medicine at the Royal Hobart Hospital — Overarching Standardised Operating Protocol (SOP)" — September 2008. Funded by ACSQHC. RHH-UTAS Clinical Handover Project. Acknowledges Dr. Christine Jorm.

**Coverage:** all three target domains (general surgery, emergency medicine, general medicine), both nursing and medical handovers — six handover scenarios in total. Per the document's own section 7 ("Examples of Working Documents"), the unit-specific SOPs (e.g., "Nursing handover (Department of Emergency Medicine)") are **not bundled** with this overarching SOP — must be requested from ACSQHC directly.

### Canonical fields (verbatim from RHH SOP Table 7 — "Overarching minimum data set")

> **Step 1: Environmental awareness**
> - Alert and safety
> - Advanced notice (especially high risk patient movements)
> - Attention (to sick/deteriorating patients)
>
> **Step 2: Patient identification**
> - Textual identification (at least surname)
> - Numerical identification (hospital unique identifier or date of birth)
> - Wrist band check or other demographic data
>
> **Step 3: History, evaluation and management**
> - History (presenting problem, relevant past history and current issues)
> - Evaluation (physical examination findings, investigation findings and current diagnosis)
> - Management to date
>
> **Step 4: Responsibility, risk management and action plan**
> - Tasks to be completed (include the tasks as well as recommendations)
> - Outstanding or abnormal results and observations (include a list, as well as actions and recommendations)
> - Risk management
>
> **Step 5: Accountability**
> - Patient (code status, MET status, other relevant information)
> - Organisation (discharge planning)
> - Profession and colleagues (treating and responsible doctors, charts and clarifications)

The 9-step **Process flowchart** (Figure 6, p43–44) wraps these content steps with: (1) Prepare, (2) Time and place, (3) Attendance and leadership, (4) Environmental awareness, (5) Patient identification, (6) Information transfer, (7) Responsibility / risk / action plan, (8) Accountability, (9) Clarification.

### ISOBAR letter expansion

The RHH SOP itself is a meta-protocol and **does not stamp the ISOBAR acronym on its minimum data set table**. The acronym was crystallised in the companion paper Porteous et al. 2009 (MJA), which states:

> i — **i**dentify yourself and the patient
> S — **S**ituation
> o — **o**bservations
> B — **B**ackground
> A — **A**greed plan, **A**ccountability
> R — **R**ead back

Note the lower-case "i" and "o" — the canonical Hobart formulation. The "A" was deliberately changed from SBAR's "Assessment" to "Agreed plan" to emphasise shared mental model, and "R" was changed from "Recommendation" to "Read back" to enforce bidirectional confirmation.

### Worked example (verbatim from St John WA 2020 form)

```
ISOBAR Patient Handover

IDENTIFY                         (sticker fields: Name / Age / Gender / DOB)

SITUATION
  - Purpose of transfer
  - Anticipated course and complications
  - Advanced care directives

OBSERVATIONS                     HEART RATE         _____/min
  Time taken: ___:___ AM/PM      RESPIRATORY RATE   _____/min
                                 OXYGEN SATURATION  ____% RA / O2 > __L/min
                                 BLOOD PRESSURE     ___ / ___ mmHG
                                 TEMPERATURE        _____°C

BACKGROUND
  - Patient assessment
  - History relevant to presenting complaint/injury and mechanism
  - Medications
  - Medical history

AGREE TO PLAN
  - Interventions
  - Response to treatment
  - Mental Health Transfers — sedation per SJWA guidelines: [ ] YES [ ] NO
  - Special medication authority section (if authorised)
  - Name and contact of attending doctor
  - Signature: Ambulance staff / Attending doctor/nurse

READ BACK
  All concerned understand and are happy with the plan

SPECIAL MEDICATION AUTHORITY
  - Indications for administration
  - Medication name
  - Medication dosage
  - Repeated / subsequent dosage(s)
```

**Domain:** This particular form is St John WA Ambulance → ED transfer (paramedic-to-ED-nurse handover, with mental-health-transfer flag). Not nurse-to-nurse shift change, but the field structure is the canonical ISOBAR family applied to a real clinical scenario — useful as a worked example of how the abstract fields get populated.

### Limitations
- **The RHH overarching SOP is a *spec*, not a corpus.** It tells us what fields *should* be present; it gives no transcripts.
- The unit-specific Nursing-ED SOP (the doc most directly relevant to our sim) is not publicly downloadable — must be requested from ACSQHC.
- Worked example we obtained is paramedic→ED, not nurse-to-nurse shift change. The structure transfers; the topics overlap heavily but not perfectly (e.g., shift-change handover emphasises pending tasks and code/MET status more than transfer-of-care does).

### License / copyright
- RHH SOP: no explicit license/copyright statement in the body text. Hosted on safetyandquality.gov.au, an Australian government site — typically Crown copyright with permissive re-use policy under the Australian Government IP framework. Karl should verify before any production redistribution; for grounding/citation it is unambiguously safe.
- St John WA form: footer says "UNCONTROLLED WHEN PRINTED" — internal procedural document. Public on stjohnwa.com.au. Use for citation and structural reference; don't pretend it's our IP.
- iSoBAR / Porteous 2009 (MJA): copyright-assigned to MJA. Acronym structure itself is not copyrightable; the specific tabular form is.

---

## What this means for Tingin

### For sim design (topics our scripted handoffs should include)

Topics that appear in real handovers, ranked by how consistently they show up across all three sources:

**Universal (in all three):**
- Patient identification (name + numeric ID, wristband)
- Patient location (bed, ward, station)
- Main / presenting problem
- Vitals as observations (HR, RR, SpO2, BP, temp)
- Background (history, comorbidities, medications, mechanism if trauma)
- What has been done so far / interventions / management to date
- Pending tasks, awaited results, anticipated movements

**High-value but more variable:**
- Comorbidities (separate slot in Galli)
- Devices and lines (Galli "presidi") — IVs, catheters, drains, telemetry leads
- Active infusions (Galli "infusioni") — drug, rate, started-when
- "What has emerged" during the shift — new findings, deterioration episodes
- Code status / MET status / advanced care directives
- Mental-health-transfer flag (St John form)
- Risk-management notes
- Discharge planning (RHH Step 5)

**Process-only (not content):**
- Read-back / confirmation step
- Identify-yourself step (the lowercase "i" of iSoBAR)
- Time taken (Galli logged this — median ~1 min/patient pre, similar post)

**Topic specifically tied to omission research:** Galli's headers reveal the things that *don't* survive the gap most often — `comorbidities`, `devices`, `infusions`, `active tasks`. These are exactly the slots Galli scored as worth 2 points (vs 1 for ID/location/main-problem). The weighting tells us the authors saw these as both higher-stakes AND more frequently dropped.

### For pitch citation (truthfulness of "seed data exists")

Honest claims we can make:
- "Tingin's handover schema is grounded in the canonical iSoBAR / ISBAR minimum data set developed by Royal Hobart Hospital under the Australian Commission on Safety and Quality in Health Care National Clinical Handover Initiative (2008)."
- "Our Tier 3 LLM-judge rubric is anchored in the 15-point Handover Evaluation Form validated by Galli et al. (2025) on n=867 ED handover events in Italy."
- "We modeled handover topic coverage on the Suominen 2017 synthetic nursing handover corpus (CC BY-NC-ND 4.0, 3 × 101 records, Australian English) — a CLEFeHealth-validated reference standard for handover information extraction."

Claims we should NOT make:
- "We trained on real handover transcripts" — Galli has no transcripts; Suominen license blocks training redistribution.
- "Our scenarios are de-identified versions of real handovers" — Suominen is synthetic; Galli has no narrative text to de-identify.
- "Our rubric was developed by clinicians" — it's adapted from Galli's; we did not co-design with practicing nurses.

### For Tier 3 rubric (HealthBench-pattern criteria)

Galli's 15-point HEF is directly transplantable. Recommended starting point for the LLM-judge rubric, rebadged in English:

| Criterion | Weight | Question for the judge |
|---|---|---|
| Patient identified by name + ID | 1 | Did the receiving nurse get unambiguous patient identity? |
| Patient location stated | 1 | Bed / ward / station mentioned? |
| Main presenting problem stated | 1 | Single-line summary of why the patient is here? |
| Comorbidities transferred | 2 | Were chronic conditions and active diagnoses passed on? |
| Devices / lines / catheters | 2 | IVs, drains, telemetry, urinary catheter, etc. mentioned? |
| Active infusions / drips | 2 | Drug + rate + start time for each running infusion? |
| What has been done | 1 | Interventions completed during the outgoing shift? |
| What has emerged | 1 | New findings, deteriorations, or events since last handover? |
| What is awaited | 1 | Pending labs, imaging, consults, transfers, scheduled events? |
| Active tasks in handover | 2 | Live work the receiving nurse must continue? |
| Written handover present | 1 | Is there a written backup to the verbal handover? |

That's 15 points exactly. Add two ISOBAR-specific process criteria from Hobart/Porteous for a Tingin-native extension:
- "Read-back confirmation" — did the receiver re-state and confirm? (binary)
- "Code/MET/ACD status mentioned for unstable patients" — (binary, weighted by patient acuity)

This anchors our rubric in clinically-validated weights from a 867-handover study, with two process-quality additions that match the ISOBAR philosophy.

For the omission cost function specifically: weight loss-of-information by Galli's HEF point values. Losing "comorbidities" costs 2 cost-units; losing "patient identification" costs 1 — but multiply by acuity / trajectory severity. Galli's weighting reflects "what nurses think matters"; the trajectory-dependent multiplier reflects "what the patient's biology says matters."

---

## Open questions for Karl

1. **Galli license ambiguity.** Repo has no LICENSE file. Default = all rights reserved. Do you want to (a) email the authors before referencing the rubric in the pitch, (b) cite from the published paper instead (if it's CC-BY OA, that's safer), or (c) note "rubric reconstructed from open repo column headers" in the spec? Recommend (b) — pull the paper through your institutional access and verify the HEF is published verbatim there.

2. **Suominen samples in the demo.** CC BY-NC-ND 4.0 forbids redistribution and derivative works. Demo is non-commercial (hackathon) but we'd be redistributing if we ship samples. Two options: (a) cite the dataset's existence and structure but use only our scripted scenarios for the demo, or (b) request explicit permission from CSIRO / NICTA to use samples. Recommend (a) for today; (b) is a post-hackathon question.

3. **ISOBAR unit-specific SOPs.** The nursing-ED-specific SOP (the most relevant to us) is not in the public PDF — must be requested from ACSQHC. For a hackathon today, the overarching SOP is enough. For a paper or production version of Tingin, request the unit-specific one.

4. **Italian-only data.** Galli is Italian. Our LLM judge will work in English. The HEF column headers translate cleanly, but if you cite the dataset in the pitch, do you want to flag the language barrier (1 sentence in the methods slide) or treat the rubric as language-agnostic (the items are universal nursing concepts)?

5. **Sample-size mismatch.** Galli pre = 526 vs post = 341 — the post-intervention sample is smaller, which is the *opposite* of the typical pre/post design. The Springer abstract says "all indicators improved significantly," but with imbalanced n the comparison needs to be checked. Probably nothing for the pitch, but flag if anyone asks "why the asymmetric n."

6. **Ambulance-vs-shift-change semantics.** The St John WA worked example is paramedic→ED-nurse, not nurse→nurse shift change. The fields overlap but the use case differs (transfer-of-care vs continuity-of-care). For our sim the fields are valid; just don't mis-attribute the form as "this is what nurses do at shift change."

---

## File inventory (what's on disk)

```
/Users/karlnuyda/Desktop/Tingin/.scratch/seed-data/
├── galli-2025/
│   ├── .git/
│   ├── README.md                            (23 bytes)
│   └── PRE_POST.xlsx                        (157 KB, 3 sheets, Italian)
├── isobar-rhh-sop.pdf                       (484 KB, 79 pages, RHH 2008 SOP)
├── isobar-rhh-sop.txt                       (extracted text, 3429 lines)
├── isobar-stjohn-wa-handover-form.pdf       (340 KB, 1-page worked template)
├── isobar-stjohn-wa-handover-form.txt       (extracted text)
├── suominen-20413-meta.json                 (CSIRO text-collection metadata)
└── suominen-20372-meta.json                 (CSIRO audio-collection metadata)
```

(Suominen TXT/DOCX corpus files **not on disk** — pull from CSIRO browser if needed; flagged for Karl's go/no-go in Open question 2.)
