# Tingin: Deck and Frontend Design Reference

**Date:** 2026-04-25
**Body:** Tingin
**Audience:** (a) Karl, building the pitch deck. (b) the FE Geth worker (`dev-1` / `interface`), building the Streamlit app.
**Status:** Authoritative design reference. Both surfaces share the same language.

Read alongside:
- `geth/specs/2026-04-25-hackathon-demo.md`. The build spec. Pitch script in §6.
- `geth/specs/2026-04-25-fe-be-contract.md`. The schemas the FE consumes.

This doc covers what those two don't: the visual language and the deck structure. Tier rendering rules and per-view content live here at the level the FE needs to hit them.

---

## 1. The Deck: 6 slides

The deck is the bookends around the live demo. Slides 1 to 3 set up. Slide 4 hands off to the Streamlit app. Slide 5 lands the result. Slide 6 closes. Slides 4 and 5 may be near-empty if the live walk does the work. They exist as fallback if the projector fails (R5).

Pitch arc per spec §6: Hook, Thesis, Run A live, Run B live, Overlay, Why this is RL, Personal close.

Map of pitch beat to slide:

| Pitch beat | Slide |
|---|---|
| Hook (numbers) | **Slide 2: Problem** |
| Thesis | **Slide 1: Title** holds the thesis tagline. Expanded at the close on Slide 6. |
| Run A live (90s) | **Slide 4: How** (silent backdrop while the app runs) |
| Run B live (60s) | (continues on Slide 4 backdrop) |
| Overlay (30s) | **Slide 5: Results** (silent backdrop while finale view runs) |
| Why this is RL, what it scales to | **Slide 6: What this becomes** |
| Personal close | **Slide 3: Why** revealed at end, OR Slide 6 hosts the close. See §1.3 below. |

Slide 3 is the "Why," the personal beat. Whether it carries the close or whether Slide 6 does is a sequencing choice (§1.3).

### 1.1 Slide-by-slide

#### Slide 1: Title

> **Tingin**
> Memory infrastructure for nursing handoffs.

- **Visual:** softened pink diamond mark, centered above the wordmark. Voronoi grain at low opacity across the slide background. No icons, no logos, no clutter.
- **Body:** title plus one-line tagline. Nothing else.
- **Note:** the tagline IS the thesis. The deck announces what we built before the problem. The audience knows what they're being asked to evaluate.
- **Spoken:** "Tingin. It's Filipino for *the way you see*. We built memory infrastructure for nursing handoffs."

#### Slide 2: Problem

> **80%** of serious medical errors involve handoff miscommunication.[^jc]
> **70%** of California skilled-nursing transfers leave with incomplete handoffs.[^cv]
> **49.6%** of US SNFs are missing 80%+ of the information needed for safe care of an arriving patient.[^am]
>
> The dominant error type isn't misjudgment. It's **omission**. What the outgoing nurse knew that didn't survive into the next shift.

- **Visual:** the three numbers as the focal element. Large. Each on its own line. Citations as footnotes in small caps below.
- **Layout:** left-justified type, generous whitespace. The numbers are the whole slide.
- **Spoken:** Hook beat from spec §6 step 1.
- **Citations** (read these out only if asked):
  [^jc]: Joint Commission, via Riesenberg 2012.
  [^cv]: Labovic 2018, CalVet 84-bed unit.
  [^am]: Adler-Milstein 2021, JAMA Network Open, n=471 hospital-SNF pairs.

#### Slide 3: Why

> **This is my mom.**
> She works the skilled nursing floor.
> What survives the handoff and what doesn't is what she navigates every shift.

- **Visual:** photograph of Karl and his mom, full-bleed or close to it. The picture is the slide. Caption sits low and small.
- **Asset:** `assets/us.jpeg`. The two mom-alone alternates (`assets/mom.jpeg`, `assets/mom2.jpeg`) can live on Slide 6.
- **Spoken:** spec §6 step 7, Karl's voice. "I chose this problem because it's a problem my mom navigates every day. SF lacks the experience to see this clearly. It's profoundly human, illegible from the outside, urgent for someone I love."
- **Note:** the photo carries the slide. Don't compete with it. If the photo is portrait orientation, half-bleed is fine. Leave warm dark on one side for breathing room.

#### Slide 4: How (live demo backdrop)

> **The shift is the episode.**
> **The handoff is the lossy compression event between episodes.**
> What the nurse encoded, what survived, what shift 2 sees.

- **Visual:** the three-panel handoff view from the Streamlit app, screenshot or live. The slide is mostly the app. Text exists only as fallback.
- **Backdrop discipline:** if running live, this slide stays open behind the Streamlit window (or projects the app directly). If projection breaks, the screenshot here carries the demo.
- **Layout:** dark Kintsugi background, three columns matching the app's panel layout: ground truth, handoff text, shift 2 view. Pink highlights for what survived. Muted red for what didn't.
- **Spoken:** Run A live (nurse-POV), then handoff three-panel, then Run B live, then handoff three-panel.

#### Slide 5: Results

> **Same patient. Same physiology. One compression choice. Two outcomes.**
>
> Run A: Mrs. Aquino stays on the floor.
> Run B: Mrs. Aquino transfers to ICU. 30-day mortality in this band: 15-20%.

- **Visual:** the finale overlay from the Streamlit app. The two NEWS2(t) traces, one in rose quartz pink (Run A), one in muted amber (Run B). Annotations at the t=19 handoff moment. Outcome captions in plain warm-white type below.
- **Layout:** chart dominates upper 2/3. Captions below.
- **Spoken:** the overlay beat from spec §6 step 5. "Same patient, same physiology, one compression choice, two outcomes."

#### Slide 6: What this becomes

> **The shift is one link.**
> A SNF patient passes through dozens of handoffs across weeks of care.
> Two shifts is the minimum demonstration.
>
> The structure scales. The cost compounds. **1 in 4** Medicare SNF patients are readmitted within 30 days. Two-thirds preventable.
>
> ---
>
> **What we ship is memory infrastructure for clinical work, so the nurse can be more human, not less.**
>
> SF builds AI to replace human work.
> Tingin builds AI to free humans for the human work that matters.

- **Visual:** softened pink diamond mark, alone, top-left. Whitespace. Type-only otherwise.
- **Layout:** two beats, separated by a thin warm-amber rule. Top beat is the scaling argument. Bottom beat is the spine.
- **Spoken:** spec §6 step 6 plus step 7's last lines. The personal close ("urgent for someone I love") can live here or on Slide 3. Karl picks based on rehearsal flow.
- **Note:** this is the slide that does the bridge from hackathon demo to company. RL judges read the top half, everyone else feels the bottom half.

### 1.2 What the deck is NOT

- Not a feature dump. The "How" slide doesn't list architecture layers. The app is the architecture, visible.
- Not a market-size pitch. TAM/SAM stays out. This is a research-judges deck, not a YC deck.
- Not the YC deck. (That's a separate artifact, May 4.)
- No bullet lists with sub-bullets. Three numbers, three lines, one paragraph. That's the maximum density.
- No clip art, no stock photography. The mom photos are the only photos.

### 1.3 Sequencing decision: where the personal close lands

Two options. Karl picks based on rehearsal:

**Option A: Personal close lands on Slide 3 (Why), at the start.**
The picture and the line ("urgent for someone I love") set the stakes early. The rest of the deck operates with that emotional weight already deposited. Slide 6 is then pure thesis ("memory infrastructure / more human, not less").

**Option B: Personal close lands on Slide 6 (Close).**
Slide 3 is just the picture and the structural sentence ("She works the skilled nursing floor"). The personal "urgent for someone I love" lands at the end, alongside the thesis. The deck builds toward the personal beat instead of leading with it.

Default recommendation: **Option B**. The close is stronger when the picture has been on screen long enough that the audience already knows who she is. Don't decide before rehearsal.

---

## 2. Design Language: Kintsugi, applied to Tingin

Inherits from `~/Desktop/Vivi/projects/design_system.md`. This section gives the FE concrete tokens.

### 2.1 Metaphor

Dark lacquer surfaces with luminous pink/amber edges. The break lines (Voronoi fracture) are where the light comes through. **Warm dark, not cold dark.** Nothing in this surface is clinical-blue or hospital-grey.

The thesis maps to the metaphor: nursing care is the gold in the cracks. The handoff is the break line. The tool makes the gold visible.

### 2.2 Color tokens

Palette is dark warm. NEWS2 colors are warm-shifted, never primary clinical red/blue.

| Token | Hex | Use |
|---|---|---|
| `bg-deep` | `#0E0908` | Slide background, app body |
| `bg-surface` | `#1A1311` | Card surface, panel background |
| `bg-elevated` | `#241B18` | Elevated card, modal, focused panel |
| `border-subtle` | `#3A2C26` | Card edge, divider |
| `border-emphasis` | `#5B453B` | Highlighted edge |
| `text-primary` | `#F2E8D9` | Primary text, headlines |
| `text-secondary` | `#B5A294` | Captions, metadata, footnotes |
| `text-muted` | `#7A6B61` | Disabled, very-low-priority |
| `accent-rose` | `#F0A6B8` | Primary accent. Pink diamond, focal highlights, Run A traces. |
| `accent-amber` | `#D4A574` | Secondary accent. Run B traces, warm warnings. |
| `accent-amethyst` | `#9B7EC4` | Tertiary accent. Judge reasoning, system messages. |
| `signal-stable` | `#7FB069` | NEWS2 0-2. Warm-shifted green (sage). |
| `signal-watch` | `#D4A574` | NEWS2 3-4. Same as amber accent. |
| `signal-acute` | `#C44536` | NEWS2 ≥ 5. Warm-shifted red (rust, not clinical). |
| `signal-lost` | `#7A2E2E` | "Did not survive the handoff." Desaturated red, never primary. |

Rule: rose, amber, and amethyst appear sparingly. The deck and the app are 80% warm dark plus warm white text. Color is for emphasis only.

### 2.3 Typography

Anti-references (per `design_system.md`): Inter, Outfit, Satoshi. They lack age and presence.

Picks:
- **Display and headline:** **Fraunces** (Google Fonts. Variable weight plus opsz). Warm modern serif with character. Use opsz: large display for slide titles (96+px), medium for app section headers.
- **Body:** **Newsreader** (Google Fonts) or system serif fallback. Reading-weight, readable at small sizes.
- **Data and monospace:** **JetBrains Mono**. For NEWS2 numbers, vitals, tool-call timeline, JSON dumps.

Type scale (Fibonacci-derived. Spec §2.3):
- 11px: caption / footnote
- 14px: body small
- 18px: body
- 24px: H4
- 32px: H3
- 47px: H2 (slide subhead)
- 76px: H1 (slide title)
- 120px: display number (Slide 2 numbers)

### 2.4 Spacing

Fibonacci scale: **4, 7, 11, 18, 29, 47, 76, 123 px**. Anything between is wrong. Component padding defaults to 18 or 29. Section spacing defaults to 47 or 76.

### 2.5 Shape

The softened pink diamond is the signature. Superellipse, n ≈ 1.5 to 1.7. Use as:
- Decorative mark on the title slide and Slide 6
- Avatar/badge shape for nurse identifiers (RN1, RN2)
- Bullet glyph at slide level (sparingly. Once per slide max.)

CSS approximation:
```css
.diamond-mark {
  width: 47px; height: 47px;
  background: var(--accent-rose);
  clip-path: path("M24 0 L48 24 L24 48 L0 24 Z");  /* fallback */
  /* preferred: superellipse via SVG mask, n=1.6 */
}
```

For real fidelity, ship the diamond as SVG with a `superellipse` path generator (n=1.6, then rotate 45°). Hard-coded SVG is fine for the demo.

### 2.6 Surface: Voronoi grain

Subtle Voronoi tessellation as background texture. **5-8% opacity.** Never the focal element. Implementation options for the demo:
- Pre-rendered PNG at 1920×1080, blend mode `multiply` over `bg-deep`.
- Streamlit: serve a static PNG via `st.markdown` with custom CSS background.
- Slide deck: same PNG dropped into the master.

Don't generate Voronoi at runtime in the app. It's a demo, not a graphics showcase.

### 2.7 Motion archetypes (Streamlit only. Slides are static.)

From `design_system.md`:
- **Water:** transitions between views (200-400ms ease-out asymmetric).
- **Forest:** staggered reveal of patient cards on load (40-80ms gap, 3 cards).
- **Mountain:** selected/focused state. No motion.
- **Crystal:** hover gleam on interactive elements (100-150ms).

Streamlit motion is constrained. Use CSS transitions on hover/focus, no JS animation libraries. Don't fight the framework.

**No bouncing. No elastic easing. No overshooting.**

### 2.8 What to avoid (anti-references)

- shadcn defaults. Looks like every other LLM-rendered demo.
- Linear cold-blue dark mode
- Bouncy animations
- Inter / Outfit / Satoshi
- Hospital-clinical blue/green palette
- Stock medical iconography
- Bullet lists with three sub-bullets each

If something on screen looks like it could be from any other 2026 hackathon demo, it's wrong.

---

## 3. Streamlit App: view-by-view rendering

This section is the FE worker's brief. Schemas come from `tingin_env/contract.py` (see `geth/specs/2026-04-25-fe-be-contract.md`). Content comes from here.

**Tier collapse rule (load-bearing):** every view checks `render_tier(score_result)` and renders the highest tier supported by the data. Missing optional fields collapse to lower-tier rendering. FE never branches on `tier == 2:` directly. It branches on `score.breakdown is not None` etc.

**MockMode:** all six views below must render correctly with the mock fixtures in `app/mocks/` before BE compiles. `st.session_state["mock_mode"]` defaults to `True` in dev.

**Layout:** `st.set_page_config(layout="wide", page_title="Tingin", page_icon="◆")`. Custom CSS injected via `st.markdown` to load Fraunces/Newsreader/JetBrains Mono and apply the palette. CSS file lives at `app/static/kintsugi.css`.

### 3.1 Sidebar

Persistent across all views.

- App mark: pink diamond plus "Tingin" wordmark (Fraunces, 32px). 18px padding.
- Run selector:
  - `▶ Run A: Good Handoff`
  - `▶ Run B: Bad Handoff`
  - `▶ GPT-4.1 zero-shot` (Tier 2+ only. Hidden if no rollout JSON loaded.)
  - `◉ Overlay Comparison` (unlocked after both A and B viewed)
- View links:
  - `▤ Floor`
  - `▤ Handoff` (jumps to handoff view if past tick=20)
  - `▤ Finale`
  - `▤ MDP Formalization`
- Playback controls:
  - Speed slider: 1× / 4× / skip-to-handoff
  - Pause/play toggle
- Researcher mode toggle: ON by default. When ON, hidden physiology plus Markov transition probabilities visible to the user. (Researchers are the audience.)
- Footer: `Tingin contract v{contract.__version__}` (per FE/BE contract §6.4)

### 3.2 Floor view

Three patient cards in a row, equal width. Each card consumes a `PatientProfile` plus `ShiftState` pair from `floor_state`.

**Card structure (top to bottom):**
1. **Header row:** name (Fraunces 24px), age plus bed plus admission reason (Newsreader 14px, `text-secondary`). Soft pink-diamond glyph (11px) next to the focal patient (P2 = Mrs. Aquino).
2. **Social context line:** one line, italic Newsreader 14px.
3. **NEWS2 gauge:** large numeric (JetBrains Mono 47px), color-coded per `signal-*` tokens. Below: four horizontal mini-bars for HR / RR / O2 / SBP (each colored by NEWS2 sub-score contribution).
4. **Vitals strip:** current vitals as a single-line monospace strip. Trend arrows (↑/↓/→) for any value that's moved since prior reading.
5. **Ambient signal pane:** initially empty (`text-muted`, "no observation yet"). When `observe_patient(p)` fires, fill with the AmbientObservation text in `text-primary`, italic Newsreader 18px. Crystal-archetype gleam transition on first appearance.
6. **Chart entries:** scrollable list of `chart_entries` strings, JetBrains Mono 11px, `text-secondary`, timestamped.
7. **Hidden physiology badge** (researcher mode only): small pill in top-right corner showing `stable` / `slow_det` / `acute`. Use amethyst tone.

**Layout note:** the focal patient (P2, bed 2) sits in the middle column. The card has a subtle 1px `border-emphasis` outline that the others don't. This is the only visual emphasis on focality at the card level. Don't make P2's card a different color or size.

**Left rail:** tool-call timeline. List of `(tick, tool_name, target_patient, reward_delta)` rows in JetBrains Mono. Reward delta colored: green for positive, amber for negative, muted for zero. New rows appear with Forest-archetype stagger.

**Header bar:** shift indicator (`shift1` / `shift2`), current actor (`RN1` / `RN2`), tick counter (`t = 14 / 20`). Right-aligned: button to skip to handoff (active only when phase=`shift1` and `tick >= 20`).

### 3.3 Handoff view (the killer screen)

Full-screen takeover. Three columns, equal width.

**Left column: "End of Shift 1: Ground Truth"**
- Header: Fraunces 32px.
- Three patient summary blocks stacked vertically. Each block lists: name, NEWS2, vitals delta over shift, **all `ambient_observations`**, MAR, BBR notes, behavior changes, skin status.
- Background: `bg-elevated`.
- This is what the outgoing nurse knew.

**Middle column: "Handoff written"**
- Header: Fraunces 32px.
- Renders `HandoffRecord.body` verbatim. Newsreader 18px, generous line-height (1.6). Preserve markdown bold (`**...**`). Clinical emphasis is meaningful.
- Below the body: timestamp plus encoding nurse ID in `text-secondary`.
- Background: `bg-surface`. Subtle Voronoi grain at 8% opacity.
- This is what the outgoing nurse encoded.

**Right column: "What Shift 2 sees"**
- Header: Fraunces 32px.
- Renders the handoff `body` again **plus** the chart (the Tier 1 fields of `ShiftState` for shift1 that persist forward). Same body as middle column, but visually grayed-down, since it's now received instead of written.
- Background: `bg-elevated`.
- This is what the incoming nurse has to work with.

**Lost-fact highlights (Tier 1):**
- After the columns render, run a fact-overlap pass: any fact in the ground-truth list (left column) that is NOT matched in the handoff body (middle column) gets a `signal-lost` colored bar drawn across that fact in the left column.
- For Run A: typically 1-2 minor facts highlighted.
- For Run B: **the ambient observation on Mrs. Aquino is highlighted** in `signal-lost`. This is the load-bearing visual.

**Tier 2 enhancement:** below the three columns, render the weighted-fact breakdown panel. Table: `fact_id`, description, weight, matched (✓/✗). Sort by weight descending. Use `accent-rose` for high-weight matched, `signal-lost` for high-weight missed.

**Tier 3 enhancement:** replace the weighted-fact panel with the per-criterion IASHR breakdown. 16 rows, each with `criterion_name`, `weight`, `status` (✓/partial/✗ glyph), `judge_reasoning` (collapsible). Hallucinations rendered as a small `accent-amethyst` chip below the table.

**Continue button:** centered below all of the above. `Continue to shift 2 →`. Fraunces 24px. Crystal-archetype hover gleam.

### 3.4 Timeline view

Linear log of every tool call across the loaded run. Each row:
- `t=NN` (JetBrains Mono 14px, `text-muted`)
- Tool name (JetBrains Mono 14px, `text-primary`)
- Target patient plus relevant params (Newsreader 14px, `text-secondary`)
- Reward delta (JetBrains Mono 14px, colored)

**Tier 2:** add `reward_delta_breakdown` as a hover-tooltip. Show the per-component contribution (NEWS2 catch / med correctness / doc quality / etc.).

The timeline is the "what the agent did" view. For Tier 2's GPT-4.1 rollout, this is where the `nursing_decisions` summary lands as a header strip above the log: "Observations: 2 (P2, P3) | Handoff fidelity: 0.62 | Escalation accuracy: 1/1."

### 3.5 Finale view

The thesis-made-visible.

**Top half:** dual-line chart, NEWS2(t) for the focal patient (Mrs. Aquino) across both Run A and Run B.
- X axis: tick (0 to 41).
- Y axis: NEWS2 (0 to 9).
- Line A: `accent-rose`. Line B: `accent-amber`.
- Annotation at t=20 (handoff moment): vertical thin `border-subtle` line plus label "handoff."
- Annotation at terminal: line A's endpoint labeled "stable, discharged on schedule." Line B's endpoint labeled "NEWS2 7+ → ICU transfer."
- Chart library: Plotly. Tested at 1920×1080. Dark theme. No gridlines except at NEWS2 thresholds (2, 5, 7).

**Bottom half: outcome captions:**
- Left card (Run A): "Mrs. Aquino, day 6 post-CAP. Caught early. Stays on the floor. Discharge on schedule."
- Right card (Run B): "Mrs. Aquino, day 6 post-CAP. Decline missed. Rapid response called. ICU transfer. 30-day mortality in this band: 15-20%."
- Below both: `accent-rose` thin rule. Caption: **"Same patient, same physiology, one compression choice, two outcomes."** Fraunces 32px, centered.

**Tier 2 additions:**
- Above the chart, render nursing-performance summary for whichever run is loaded: observations made, handoff fidelity, escalation accuracy. JetBrains Mono header strip.
- For the GPT-4.1 rollout: the chart shows that run's NEWS2 trace (single line) instead of the A/B overlay. Caption changes to surface the agent's behavior.

**Tier 3 additions:**
- Replace the single-rollout chart with **distribution histograms** per policy class. Two histograms side-by-side: with-hint vs. without-hint. X axis: handoff fidelity score. Y axis: count.
- Patient-outcome counts as a small grid below: "Mrs. Aquino: lived 7, transferred 3, deteriorated 0" per policy class.

### 3.6 MDP view

Static rendering of `spec/mdp.md`. Layout:
- Title (Fraunces 47px): "MDP Formalization."
- Five sections (State / Action / Observation / Transition / Reward), each with its own header (Fraunces 32px) and body (Newsreader 18px) plus monospace inline blocks for math.
- Background: `bg-surface`.
- Single column, max-width 76rem. Centered.
- Render via `st.markdown` with custom CSS that applies the palette.

This view is for RL judges who want the formalization in text. It's not a primary view. Most pitches won't visit it. But it must render correctly when they click.

---

## 4. Cross-cutting requirements

### 4.1 Theming bootstrap

`app/theme.py` exports:
- A dict of all color tokens (single source of truth).
- A `kintsugi_css()` function returning the full CSS as a string, injected into `app.py` via `st.markdown(kintsugi_css(), unsafe_allow_html=True)` at the top of every page.
- Streamlit's native theme config in `.streamlit/config.toml` set to:
  ```toml
  [theme]
  base = "dark"
  primaryColor = "#F0A6B8"
  backgroundColor = "#0E0908"
  secondaryBackgroundColor = "#1A1311"
  textColor = "#F2E8D9"
  font = "serif"
  ```

### 4.2 Display target

All views tested at **1920×1080**. No mobile responsive design. No tablet layout. Demo runs on the venue projector. Single resolution target.

Per spec §7 R5: **test on external display before leaving for the venue.** Default Streamlit theme is too light for a projected screen. Kintsugi dark warm should project well, but verify.

### 4.3 Performance

- First view load < 2s on warm cache (per smoke-test G4).
- Cold start < 5s.
- Plotly charts render with explicit `width` / `height`. Don't rely on autosize.
- Don't generate Voronoi or diamond shapes at runtime. Pre-rendered PNG/SVG only.
- No JS animation libraries. CSS transitions only.

### 4.4 Fallback rendering

Per R5, pre-record screen captures of both runs at rehearsal. Save high-res PNGs (1920×1080) of:
- Floor view at tick=12 (mid-shift1)
- Handoff view (the killer screen) for both Run A and Run B
- Finale overlay

If live demo fails mid-pitch, switch to the recording. The deck slides 4 and 5 already host these screenshots as backdrop. They become the demo if the projector breaks.

---

## 5. Asset registry

| Asset | Source | Use |
|---|---|---|
| Mom photo (Karl plus mom) | `assets/us.jpeg` | Slide 3 (Why) |
| Mom photo (alone, take 1) | `assets/mom.jpeg` | Optional alternate. Slide 6 if Option B. |
| Mom photo (alone, take 2) | `assets/mom2.jpeg` | Optional alternate. Slide 6 if Option B. |
| Pink diamond mark | TBD. Generate as SVG (n=1.6 superellipse, rotated 45°), color `accent-rose`. | App sidebar mark, Slide 1, Slide 6, focal-patient glyph |
| Voronoi grain | TBD. Pre-render 1920×1080 PNG, 5-8% opacity, warm-dark base. | Slide backgrounds, app surfaces |
| Tingin wordmark | TBD. Fraunces 700, letter-spacing -0.02em. | App sidebar, Slide 1 |
| Fonts | Google Fonts: Fraunces, Newsreader, JetBrains Mono | App and slides |

**Generate-before-build list:**
1. SVG diamond mark (one file, parameterizable via CSS).
2. PNG Voronoi grain at 1920×1080 (one file, 5% opacity over `bg-deep`).
3. Wordmark. Can be CSS-only (Fraunces 700) for the app. For slides, render once as SVG and drop in.

**Note on filenames:** the three jpegs in `assets/` are currently UUID-named. Rename to `us.jpeg`, `mom.jpeg`, `mom2.jpeg` before pitch. The doc references the semantic names.

---

## 6. Open questions for Karl

1. **Slide 3 vs Slide 6 for personal close.** §1.3. Default Option B (close on Slide 6). Confirm at rehearsal.
2. **Wordmark.** "Tingin" set in Fraunces 700 is the default. If Karl wants a custom wordmark (his own hand, a friend's design, etc.), drop it as SVG into `assets/`.
3. **Slide 6 spine line.** Currently: "memory infrastructure for clinical work, so the nurse can be more human, not less." This is the spec's spine. Confirm it's the close he wants in the deck (vs. holding it for YC).

None of these block FE build. The FE worker can scaffold all six views against the mock fixtures with the design tokens above.
