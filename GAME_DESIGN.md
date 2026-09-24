# Game Design Document — UBT Trainer (UBTedugame)

| | |
|---|---|
| **Working title** | UBT Trainer |
| **Genre** | Educational serious-game / interactive visual novel (single-player) |
| **Engine** | Ren'Py 8.5 (Python-based) |
| **Platform** | Windows / macOS / Linux — offline desktop |
| **Session length** | ~10–15 minutes per playthrough |
| **Audience** | Nurses, midwives, and students in rural / low-resource maternity care |
| **Languages** | English (default), Bahasa Indonesia |
| **Status** | v1.0 implemented; this GDD describes the shipped design |

> This document describes the game from a **design** perspective — the player
> experience, core loop, systems, feedback, and balancing. For requirements framing
> (target users, functional requirements, success metrics) see the companion
> **[PRD](ubt-game-PRD.md)**; for setup and file layout see the **[README](README.md)**.
> Where the two overlap (learning objectives, clinical constants), this GDD
> cross-references rather than restates.

---

## 1. Design Pitch

> *You are the nurse when the bleeding won't stop.* UBT Trainer drops the player into a
> single life-or-death emergency and asks them to run the full uterine balloon tamponade
> (UBT) pathway — recognise, escalate, prepare, insert, monitor — scoring every decision
> and explaining the clinical *why* behind each one, so the correct sequence is muscle
> memory before it is ever needed with a real patient.

The design goal is **decision fluency under pressure**, built through *doing* rather than
reading, in a space where failure is safe and always explained.

---

## 2. Design Pillars

| Pillar | What it means | Expressed in |
|---|---|---|
| **Decision under pressure** | The player is always the one acting in a live emergency, not a passive reader. | Decision menus, timed-feeling framing, always-visible score HUD |
| **Learn by doing — then learn *why*** | Every interaction is followed by a clinical explanation, for right answers *and* wrong ones. | `feedback` overlay on every choice; per-quiz `explain`; distractor rationale |
| **Safe, repeatable failure** | Mistakes cost points and are logged, but never end the run — the learner always completes the pathway and sees what to review. | Score floor of 0, no game-over, mistake log on results, "Review Again" |
| **Low-resource authenticity** | The scenario, tools, and constraints mirror a rural clinic where UBT is the right low-cost intervention. | Nurse-in-rural-clinic framing, real equipment list + look-alike distractors |

Each pillar maps to a concrete mechanic — nothing in the pillar list exists only as
aspiration.

---

## 3. Player & Fantasy

**Role.** The player *is* the nurse on a rural maternity ward. The player character is
silent and second-person ("You are a nurse…"); the player's agency is entirely in their
choices and actions, not in dialogue.

**Emotional arc.** The run opens in sudden crisis — a healthy delivery turns, twenty
minutes later, into heavy bleeding — and moves toward earned competence: recognise →
escalate → prepare → perform → stabilise → confirm knowledge → see your grade. The
intended feeling at the end of a clean run is *"I could do this."*

**Mastery fantasy.** Mastery looks like moving through the whole pathway without
hesitation: instantly reading the vitals as PPH, calling the team first, building the
tray with no distractors, sequencing the insertion correctly, hitting the safe inflation
band on the first try, and scoring **Expert**.

---

## 4. Core Gameplay Loop

The entire game is built from one repeating micro-loop:

```
   ┌─────────────────────────────────────────────────────────┐
   │                                                         │
   ▼                                                         │
 PROMPT ──▶ PLAYER ACTION ──▶ EVALUATE ──▶ FEEDBACK (the WHY) ┘
(dialogue/  (choose / drag /   (correct?)   ├─ correct → affirm + advance
 screen)     slide / check)                 └─ wrong  → deduct + explain + retry/advance
                                                         │
                                                         ▼
                                                 SCORE + MISTAKE LOG
```

- **Prompt** — Dr. Amina or the narrator frames the situation and poses the task.
- **Action** — the player interacts: pick a menu option, drag a tool, move a slider,
  tick a checklist, answer a question.
- **Evaluate** — the game checks the action against the correct clinical answer.
- **Feedback** — a modal overlay explains the reasoning. Green (✓) for correct, red (✗)
  for wrong. *Feedback fires even when the player is right* — reinforcement, not just
  correction.
- **Consequence** — wrong actions call `deduct_score(reason, points)`, which lowers the
  score (floored at 0) and appends a human-readable entry to the mistake log. The run
  never ends early.

The loop is identical across very different interaction types, which keeps the game
readable while the *content* of each beat teaches a different step of the protocol.

---

## 5. Game Flow / Scene Map

A single guided scenario of nine scenes, played linearly (`game/script.rpy`). Difficulty
is chosen on the main menu, which routes through `start_easy` / `start_medium` /
`start_hard` before `reset_training()`.

| # | Scene (`label`) | Interaction | Teaches |
|---|---|---|---|
| 1 | `scene_intro` | Title card + dialogue | Sets the emergency (patient Maria, sudden heavy bleeding) |
| 2 | `scene_assessment` | Vitals card + decision menu | Recognising PPH vs. normal bleeding |
| 3 | `scene_call_for_help` | Decision menu | Escalate first — PPH is a team emergency |
| 4 | `scene_equipment_prep` | Drag-and-drop onto a tray | Selecting the 6 correct UBT tools, rejecting distractors |
| 5 | `scene_procedure` | Ordered drag-to-target ×4 + inflation slider | Correct insertion sequence + safe inflation volume |
| 6 | `scene_assessment_check` | Decision menu | The tamponade test after insertion |
| 7 | `scene_monitoring` | Checklist | Building the post-insertion monitoring plan |
| 8 | `scene_quiz` | Multiple-choice questions | Reinforcing key facts |
| 9 | `scene_results` | Score, grade, mistake log | Reflection + retry |

The scenes are hard-sequenced by `jump`s; there is no branching narrative. The decision
points are **scored choices on a single linear path** — a wrong choice deducts points and
shows its explanation, then play continues down the same path. The learner always reaches
the results screen (no dead ends, no game-over, no divergent routes).

### 5.1 The five learning stages

Beneath the nine-scene structure, the game teaches **five core clinical stages**, each
mapped to a distinct interactive mechanic. This is the pedagogical spine — the nine scenes
above are how these five stages are paced and framed.

| # | Learning stage | Scene(s) | Mechanic | What the player must get right |
|---|---|---|---|---|
| 1 | **Recognise the signs of PPH** | Scene 2 (`scene_assessment`) | Vitals card + scored decision menu | Read the vitals (HR 128, BP 88/54, ~700 mL ongoing, pale/clammy) as PPH with shock, and act rather than wait |
| 2 | **Prepare the equipment tray** | Scene 4 (`scene_equipment_prep`) | Drag-and-drop with distractors | Gather the 6 correct UBT tools and reject look-alikes (e.g. the Foley's ~30 mL balloon) |
| 3 | **Correct insertion & placement** | Scene 5, steps 1–3 & 5 (`scene_procedure`) | Ordered drag-to-target on the patient diagram | Sequence the insertion correctly: speculum → catheter → syringe → (inflate) → clamp |
| 4 | **Inflate to the right volume** | Scene 5, step 4 (`proc_inflate`) | Volume slider with safe-band check | Inflate within **250–500 mL**; under- and over-inflation are penalised and explained |
| 5 | **Select a monitoring plan** | Scene 7 (`scene_monitoring`) | Completeness checklist | Build the full post-insertion plan: vitals q15min, fundus, blood loss, urine output, documentation |

The remaining scenes wrap and reinforce these five stages: the intro sets the emergency
(Scene 1), calling for help teaches escalation (Scene 3), the tamponade test confirms the
placement worked (Scene 6), the quiz reinforces the facts behind all five stages (Scene
8), and the results screen turns any mistakes into a review list (Scene 9). Each stage is
a *scored decision point on the linear path*, never a branch.

---

## 6. Systems & Mechanics

All mechanics live in `game/ubt_mechanics.rpy` (logic/data) and
`game/ubt_screens.rpy` (presentation).

### 6.1 Scoring

- The player starts at **100** points (`default score = 100`).
- Mistakes call **`deduct_score(reason, points)`**, which multiplies the base penalty by
  the difficulty's `penalty_mult`, subtracts it (never below 0), and appends
  `(reason, points)` to **`score_log`**.
- Base penalties are **10** (major clinical decisions) or **5** (procedural / quiz
  slips).
- **`grade_for(score)`** returns *Expert*, *Competent*, or *Needs Review* against the
  difficulty's thresholds; **`grade_color(score)`** colour-codes it (green / amber / red).
- A persistent **`score_hud`** shows the live score from Scene 2 onward (top-right).

The mistake log is the real learning payoff — it doubles as a personalised "what to
review" list on the results screen.

### 6.2 Decision menus

Standard Ren'Py `menu` blocks with one correct option and two or more wrong ones. Every
option — **including the correct one** — routes to the `feedback(correct, title, message)`
screen with a clinical explanation. Wrong options additionally call `deduct_score` with a
reason phrased for the log (e.g. *"Assessment: mistook PPH for normal bleeding…"*). Used
in Scenes 2, 3, and 6.

### 6.3 Equipment preparation (drag-and-drop) — Scene 4

- The shelf shows the **6 correct tools** (`CORRECT_TOOLS`: UBT balloon catheter, 50 mL
  syringe, 500 mL IV normal saline, speculum, clamps ×2, sterile gloves) mixed with
  **distractors** (`DISTRACTOR_ORDER`: forceps, episiotomy scissors, suture kit, Foley
  catheter). How many distractors appear is set by difficulty.
- `current_shelf()` interleaves correct tools and distractors so the 2-column layout
  still alternates; `shelf_pos()` / `TRAY_SLOTS` place them.
- **`equipment_dragged(drags, drop)`** is the drag callback:
  - Correct tool dropped on the tray → snaps into the next free tray slot, added to
    `tools_on_tray`.
  - Distractor dropped on the tray → **rejected**, bounced back to the shelf, `−5`
    penalty, and a `feedback` overlay explaining *why* it's wrong (from
    `DISTRACTOR_INFO`; e.g. a Foley's ~30 mL balloon cannot tamponade the uterus).
  - Anything dragged back off the tray is removed from the count.
- A live **"On tray: n / 6"** counter is shown; the **Proceed** button only appears when
  all 6 correct tools are on the tray.

### 6.4 Procedure — ordered steps — Scene 5

- Five fixed-order steps (`PROC_STEPS`): (1) insert speculum, (2) insert UBT catheter,
  (3) connect syringe, (4) inflate balloon *(slider — see 6.5)*, (5) clamp catheter.
- Steps 1–3 and 5 are **drag-to-target** on a patient diagram; the target zone
  **pulses** (`target_pulse`) to signal where to drop.
- Only the tools still needed (plus a permanent **forceps** distractor) appear on the
  shelf each step (`proc_tools_for`).
- **`procedure_dragged(drags, drop)`**:
  - Correct tool on the target → step complete (returns `"correct"`, ending the screen).
  - Wrong tool on the target → **`−5`**, a **red flash** (`red_flash`), a `feedback`
    overlay, and the tool snaps back to the shelf. On easy/medium the step *hint* is
    prepended to the explanation; on hard, only the reason is shown (see 6.7).
- A **`step_progress`** bar ("STEP n of 5") sits at the top throughout.

### 6.5 Inflation slider — Scene 5, step 4

- `proc_inflate` shows the **`inflation_slider`** screen — a bar bound to
  `inflate_volume` (range 0–700 mL).
- The safe band is **250–500 mL**. On confirm:
  - In band → proceed.
  - **< 250 mL** → `−5`, "Under-inflated" explanation (balloon can't press against the
    uterine wall), loop back.
  - **> 500 mL** → `−5`, "Over-inflated" explanation (risks uterine injury/rupture),
    loop back.
- The step **loops until a safe volume is confirmed** — the player cannot advance with an
  unsafe value, but each unsafe attempt is penalised and explained.

### 6.6 Monitoring checklist — Scene 7

- Five items (`MONITOR_ITEMS`: vitals q15min, fundus height/tone, vaginal blood loss,
  urine output, document time + volume), each a toggle (`toggle_monitor`).
- The **confirm** button appears only when **all five** are checked — this is a
  *completeness* exercise (build the full plan) rather than a scored trap.

### 6.7 Quiz — Scene 8

- Multiple-choice questions from `QUIZ_QUESTIONS` (base 5) plus `QUIZ_ADVANCED` (2 harder
  ones). **`active_quiz()`** returns `(base + advanced)[:quiz_count]`, so the *number of
  questions* is set by difficulty.
- Each answer shows its `explain` text; wrong answers deduct **5** and log a `fix`
  summary. Topics: balloon volume, dwell time, PPH definition, contraindication,
  tamponade test (+ negative-test escalation and prophylactic antibiotics on hard).

---

## 7. Difficulty Design

Difficulty is chosen at the main menu and **preserved across retries** (it survives
`reset_training()`). One `DIFFICULTY` table tunes five knobs at once:

| Knob | Easy | Medium | Hard |
|---|---|---|---|
| Penalty multiplier (`penalty_mult`) | 0.5× | 1.0× | 1.5× |
| Expert threshold (`expert`) | 85 | 90 | 95 |
| Pass / Competent threshold (`pass`) | 60 | 70 | 80 |
| Procedure hints shown (`show_hints`) | Yes | Yes | No |
| Equipment distractors (`distractors`) | 1 | 2 | 4 |
| Quiz questions (`quiz_count`) | 3 | 5 | 7 |

**How each knob changes game feel:**

- **Penalty multiplier** scales how punishing a slip is (rounded, minimum 1 point).
- **Grade thresholds** raise the bar for the same score — Expert on hard demands a nearly
  clean run.
- **Hints** removes the safety-net step hint in the procedure, forcing recall of the
  sequence rather than recognition.
- **Distractors** widens the equipment shelf, making tool selection genuinely
  discriminating rather than obvious.
- **Quiz count** adds the two advanced clinical-judgement questions on hard.

Together these move the experience from *guided walkthrough* (easy) to *unassisted
assessment* (hard) without changing a single line of scene flow.

---

## 8. Feedback & Game Feel

The game leans hard on immediate, legible feedback:

- **Feedback overlay** (`feedback`) — modal, dimmed backdrop, **green panel for correct /
  red for wrong**, big ✓/✗, explanation body, and a Continue button. The core teaching
  surface.
- **Red flash** (`red_flash`) — a brief full-screen red pulse on a wrong procedure drop:
  visceral "no" before the explanation reads.
- **Target pulse** (`target_pulse`) — the procedure drop zone breathes to draw the eye to
  the correct target.
- **Snap animations** — tools glide to their slot / back to the shelf (`tool.snap`),
  making drag outcomes feel physical and clear.
- **Live score HUD** — always-present score keeps stakes visible without a timer.
- **Step progress bar** — orients the player inside the 5-step procedure.
- **Rule: always explain the *why*.** No feedback is ever a bare "wrong" — every overlay
  and quiz answer carries clinical reasoning. This is the single most important game-feel
  rule and applies to correct answers too.

---

## 9. Progression & Replay

- **Single scenario, no unlocks.** Depth comes from difficulty and from chasing a clean
  run, not from new content.
- **Results screen** (`results_screen`) shows difficulty, final score /100, the
  colour-coded grade, and — the key artifact — the full **mistake log** under *"What to
  review"* (scrollable). A flawless run instead shows a congratulatory message.
- **Retry loop.** *Review Again* returns `"again"`, which calls `reset_training()` and
  jumps back to `scene_assessment` (skipping the intro) at the same difficulty; *Exit*
  returns to the main menu.

The replay incentive is explicit and pedagogical: play again, apply the review list,
raise the grade.

---

## 10. Content

> Clinical constants are the source of truth and must stay internally consistent; see
> PRD §7 for the authoritative list. Summarised here for design reference.

**Clinical constants**

- PPH: **> 500 mL** after vaginal delivery (**> 1000 mL** after caesarean).
- Balloon inflation: **250–500 mL** normal saline.
- Balloon dwell: **24–48 hours**, then staged deflation.
- Primary indication: **atonic uterus**. Contraindication: **uterine rupture**.

**Patient vitals (Scene 2, `vitals_info`)** — HR 128 bpm, BP 88/54 mmHg, est. blood loss
~700 mL ongoing, pale/clammy skin, soft poorly-contracted uterus. Deliberately
unambiguous: this *is* PPH with shock.

**Equipment**

| Correct (6) | Distractors (4) | Why the distractor is wrong |
|---|---|---|
| UBT balloon catheter | Forceps | Assisted delivery, not tamponade |
| 50 mL syringe | Episiotomy scissors | Used during delivery, not PPH |
| 500 mL IV normal saline | Suture kit | Repairs tears; UBT treats atonic bleeding |
| Speculum | Foley catheter | ~30 mL balloon can't tamponade the uterus |
| Clamps ×2 | | |
| Sterile gloves | | |

**Quiz bank** — 5 base + 2 advanced questions covering balloon volume, dwell time, PPH
definition, contraindication, the tamponade test, negative-test escalation, and
prophylactic antibiotics.

> **Open item:** clinical content should be reviewed by a qualified clinician/educator
> against a recognised guideline (e.g. WHO UBT recommendations) before use in formal
> training. See PRD §10.

---

## 11. Narrative & Characters

Minimal, functional narrative in service of the mechanics.

- **Dr. Amina** (`dr`) — the guide/mentor. Presents the situation, poses each task, and
  confirms outcomes ("Bleeding has stopped — tamponade test positive. Well done."). She
  is the diegetic wrapper around every mechanic.
- **The nurse** — the player. Silent, second-person; all agency is in choices/actions.
- **Maria** — the patient. Off-screen stakes; never a talking character, but the reason
  every decision matters.

**Tone.** Urgent but supportive — high stakes without melodrama, matching a real
clinical mentor talking a colleague through an emergency. Dialogue always frames *why*
this step comes now, seeding the reasoning that the feedback then reinforces.

---

## 12. Art & Audio Direction

**Current state.** Art is **programmatic placeholder** (flat colour tiles / composed
shapes in `game/ubt_images.rpy`) — deliberately swappable. Tool tiles keep a fixed
**170×130** footprint and screens position art around fixed layout boxes, so illustrated
PNG/SVG-derived assets can drop in **without touching game logic** or breaking
drag-and-drop hit detection.

**Visual language.** A calm clinical palette — teal/dark-teal (`#1e3a3a`, `#2a7a7a`) on
near-white — with rounded panels (`rpanel`, `ubt_frame`) and clear semantic colour:
green = correct/expert, red = wrong, amber = competent. The UI reads as clinical,
readable, and unfussy.

**Audio.** Currently minimal (empty `audio/`). Direction for future work: subtle
ambience for the ward, distinct correct/wrong stings to reinforce the feedback overlays,
and a heartbeat/urgency cue during the emergency scenes — never so loud it competes with
reading the clinical text.

**Art direction for future assets.** Replace tiles with clear, instrument-accurate
illustrations of each tool (so selection is a *recognition* skill), and an anatomically
readable patient diagram for the procedure targets. Keep footprints/layout boxes fixed.

---

## 13. UX / Screen Inventory

| Screen (`ubt_screens.rpy`) | Role |
|---|---|
| `score_hud` | Persistent live score (top-right, Scene 2+) |
| `feedback` | The universal correct/wrong explanation overlay |
| `red_flash` | Wrong-drop visual punch |
| `step_progress` | "STEP n of 5" during the procedure |
| `intro_screen` | Title card + Begin Training |
| `vitals_info` / `vitals_card` / `vitals_button` / `vitals_popup` | Patient vitals as a side card and re-openable popup |
| `equipment_prep` | Tray drag-and-drop + "On tray n/6" + Proceed |
| `procedure_screen` | Ordered drag-to-target on the patient diagram |
| `inflation_slider` | Volume bar with safe-band check |
| `monitoring_checklist` | Toggle list + confirm-when-complete |
| `quiz_screen` | One MCQ per screen |
| `results_screen` | Score, grade, mistake log, Review Again / Exit |

The **main menu** (in `screens.rpy`) routes the Start button to the difficulty entry
labels and hosts the **EN/ID language toggle**.

---

## 14. Localization

- Fully playable in **English (default)** and **Bahasa Indonesia**, covering dialogue,
  UI, tool tiles, feedback, quiz, and results (`game/tl/indonesian/`).
- All user-visible strings flow through Ren'Py's translation system — `_()` for
  translate-at-display and `__()` for translate-now (used where strings are built in
  Python, e.g. log reasons and composed feedback bodies).
- Language switches **live** from the main-menu toggle and a Preferences radio group, and
  the choice **persists** between sessions.
- Medical terminology follows Indonesian clinical usage (perdarahan pascapersalinan,
  tamponade balon uterus, atonia uteri, spekulum, klem). Adding a language requires no
  logic changes — only a new `tl/` folder.

---

## 15. Success Criteria, Scope & Future Work

**What a good outcome looks like (design view).** The learner completes the full pathway,
scores **Competent or better** on a repeat run, gets **4/5+** on the quiz, and can use
the game unfacilitated as a refresher. (No telemetry exists; observed in facilitated or
self-reported sessions. See PRD §8.)

**Deliberately out of scope** (see PRD §9): branching narrative, uterotonic drug
management, referral/transport decisions, non-balloon interventions, instructor
dashboards/accounts/analytics, and mobile/web builds.

**Most valuable future work:**

1. Replace placeholder art with illustrated, instrument-accurate assets (fixed
   footprints already support this).
2. Clinical sign-off against a recognised guideline.
3. Light audio pass (ambience + feedback stings) to sharpen game feel.
4. Additional languages beyond EN/ID.
5. Optional: broaden the PPH curriculum as additional scenarios reusing the same core
   loop.
