# Product Requirements Document — UBT Trainer (UBTedugame)

| | |
|---|---|
| **Product** | UBT Trainer (project name: UBTedugame) |
| **Type** | Interactive educational game (desktop, offline) |
| **Status** | v1.0 implemented; written retrospectively as reference spec |
| **Date** | 2026-07-19 |
| **Platform** | Windows / macOS / Linux via Ren'Py 8.5 |

## 1. Overview

**One-line pitch:** A scenario-based training game that teaches nurses and midwives to recognise postpartum hemorrhage (PPH) and manage it with uterine balloon tamponade (UBT) — scoring every decision and explaining the clinical reasoning behind it.

**Problem.** Postpartum hemorrhage is a leading cause of maternal death, disproportionately in rural and low-resource settings. Uterine balloon tamponade is an effective, low-cost intervention when uterotonics fail, but it must be performed correctly and promptly — and hands-on training opportunities are scarce. Written protocols alone do not build the decision-making speed and procedural sequencing the emergency demands.

**Goal.** Give frontline maternity staff a safe, repeatable way to practise the full UBT emergency pathway — recognition, escalation, equipment, insertion, and monitoring — with immediate feedback on every mistake, so that the correct sequence is familiar before it is ever needed with a real patient.

> **Disclaimer:** UBT Trainer is a training aid. It is not a substitute for clinical guidelines, institutional protocols, or supervised hands-on training.

## 2. Target users

**Primary.** Nurses and midwives working on maternity wards in rural clinics and low-resource settings — the player character is explicitly a nurse in a rural clinic. Indonesian-speaking users are a first-class audience (full Bahasa Indonesia localization).

**Secondary.**
- Nursing and midwifery students learning PPH management.
- Clinical educators using the game as a teaching or refresher tool.

**Assumptions.** Users have basic clinical vocabulary, access to a desktop/laptop computer (no internet required after install), and limited time — a full playthrough takes roughly 10–15 minutes.

## 3. Learning objectives

After completing the game, the learner can:

1. Recognise PPH: blood loss above 500mL after vaginal delivery, with signs of shock (tachycardia, hypotension, pale clammy skin).
2. Escalate correctly: call for help first — PPH is a team emergency, never managed alone.
3. Select the correct UBT equipment (balloon catheter, 50mL syringe, 500mL IV normal saline, speculum, clamps, sterile gloves) and reject look-alike distractors.
4. Perform the insertion in the correct order: speculum → catheter placement → syringe connection → inflation → clamping.
5. Inflate the balloon within the safe 250–500mL range and explain the risks of under- and over-inflation.
6. Apply the tamponade test after insertion, and know the balloon stays in place 24–48 hours before staged deflation.
7. Build the post-insertion monitoring plan (vitals every 15 minutes, fundus, blood loss, urine output, documentation).
8. Recall key facts: PPH definitions (>500mL vaginal, >1000mL caesarean) and the uterine-rupture contraindication.

## 4. Product scope and user flow

A single guided scenario of nine scenes, played linearly (`game/script.rpy`):

| # | Scene | Interaction |
|---|---|---|
| 1 | Intro | Title screen; dialogue sets the scene (patient Maria, sudden heavy bleeding) |
| 2 | Assessment | Vitals card + decision menu: is this PPH? |
| 3 | Call for help | Decision menu: first action in the emergency |
| 4 | Equipment prep | Drag-and-drop: gather 6 correct tools onto a sterile tray from a 10-item shelf |
| 5 | Procedure | Ordered drag-and-drop steps + inflation slider |
| 6 | Tamponade check | Decision menu: what to check after insertion |
| 7 | Monitoring | Checklist: build the monitoring plan |
| 8 | Quiz | Five multiple-choice knowledge questions |
| 9 | Results | Final score, grade, mistake log, retry option |

Every wrong choice triggers immediate feedback explaining the correct clinical reasoning, then play continues — the learner always completes the scenario.

## 5. Functional requirements

### 5.1 Scenario engine
- **FR-1** The game presents the nine scenes in fixed order, driven by dialogue from a guiding character (Dr. Amina) and the narrator.
- **FR-2** Decision-point menus offer one correct and two or more incorrect options; each option shows a feedback overlay with the clinical explanation (correct choices too).

### 5.2 Equipment preparation (drag-and-drop)
- **FR-3** A shelf presents 10 tools — 6 correct (UBT balloon catheter, 50mL syringe, 500mL IV normal saline, speculum, clamps ×2, sterile gloves) and 4 distractors (forceps, episiotomy scissors, suture kit, Foley catheter).
- **FR-4** Dropping a correct tool on the tray snaps it into a tray slot; dropping a distractor rejects it with an explanation of why it is wrong (e.g. a Foley's ~30mL balloon cannot tamponade the uterus) and a 5-point penalty.
- **FR-5** The screen shows a live "On tray: n / 6" counter; the Proceed button appears only when all 6 correct tools are on the tray.

### 5.3 Procedure (ordered steps)
- **FR-6** Five steps in fixed order: insert speculum, insert UBT catheter (uterine cavity), connect syringe (inflation port), inflate balloon, clamp catheter. Steps 1–3 and 5 are drag-to-target on a patient diagram; the target zone pulses.
- **FR-7** Dragging the wrong tool to the target deducts 5 points, flashes red, shows the step hint plus why that tool is wrong, and returns the tool to the shelf.
- **FR-8** Inflation uses a volume slider; values outside 250–500mL deduct 5 points, explain the specific risk (ineffective tamponade / uterine injury), and loop until a safe volume is confirmed.

### 5.4 Monitoring and quiz
- **FR-9** The monitoring checklist offers five items (vitals every 15 min; fundus height and tone; vaginal blood loss; urine output; documentation of time and volume) that the learner checks before confirming the plan.
- **FR-10** The quiz asks five multiple-choice questions (balloon volume, dwell time, PPH definition, contraindication, tamponade test); each answer shows an explanation, wrong answers deduct 5 points.

### 5.5 Scoring and results
- **FR-11** The learner starts at 100 points; mistakes deduct 5 or 10 points (floor 0) and are logged with a human-readable reason. A persistent score HUD is visible from Scene 2 onward.
- **FR-12** The results screen shows the final score, a grade — Expert (≥90), Competent (≥70), Needs Review (<70) — and the full mistake log as "what to review". A perfect run gets a congratulatory message.
- **FR-13** "Review Again" resets all training state and restarts from the assessment scene; "Exit" returns to the main menu.

### 5.6 Localization
- **FR-14** The game is fully playable in English (default) and Bahasa Indonesia, including dialogue, UI, tool tiles, feedback, quiz, and results (`game/tl/indonesian/`).
- **FR-15** Language can be switched live from an EN/ID toggle on the main menu and a Language radio group in Preferences; the choice persists between sessions.
- **FR-16** Medical terminology follows Indonesian clinical usage (perdarahan pascapersalinan, tamponade balon uterus, atonia uteri, spekulum, klem).

## 6. Non-functional requirements

- **NFR-1 Offline & self-contained.** Single-player desktop app; no network access, accounts, or external dependencies beyond the Ren'Py 8.5 runtime.
- **NFR-2 Distribution.** Buildable for Windows, macOS, and Linux from the Ren'Py Launcher.
- **NFR-3 Translatability.** All user-visible strings flow through Ren'Py's translation system (`_()` / `__()` + `game/tl/`); adding a language requires no logic changes.
- **NFR-4 Replaceable art.** Illustrations are composed programmatically around fixed layout boxes (`game/ubt_images.rpy`); PNG assets can be swapped without touching game logic. Tool tiles keep a fixed 170×130 footprint so drag-and-drop hit detection stays valid.
- **NFR-5 Quality gate.** Scripts pass `renpy lint`; scene changes are smoke-tested via `--warp` before release.

## 7. Content requirements

- Clinical values used throughout (must stay consistent): PPH >500mL after vaginal delivery / >1000mL after caesarean; balloon inflation 250–500mL normal saline; balloon dwell 24–48 hours with staged deflation; uterine rupture is a contraindication; atonic uterus is the primary indication.
- All feedback text must explain *why*, not just mark right/wrong.
- Clinical content should be reviewed by a qualified clinician/educator before use in formal training programmes (open item — see §10).

## 8. Success metrics

- Learner completes the full scenario (completion rate).
- Grade of Competent or better (≥70) on a repeat playthrough.
- Quiz performance: 4/5 or better on the knowledge check.
- Educator adoption: usable as a self-contained refresher without facilitator support.

(No telemetry exists — metrics are observed in facilitated sessions or self-reported.)

## 9. Out of scope / future work

- Replacing programmatic placeholder art with illustrated assets (explicitly invited in the README).
- Additional languages beyond English and Bahasa Indonesia.
- Broader PPH curriculum: uterotonic drug management, referral/transport decisions, non-balloon interventions.
- Instructor dashboard, analytics, or learner accounts.
- Mobile or web builds.
- Formal clinical validation study.

## 10. Open questions

1. **License** — none chosen yet (README TODO); required before public distribution.
2. **Clinical review** — who owns sign-off on the medical content, and against which guideline (e.g. WHO recommendations on UBT for PPH)?
