## ubt_mechanics.rpy — score system, game data, and helper functions for UBT Trainer.

## ---------------------------------------------------------------------------
## Game state
## ---------------------------------------------------------------------------

default score = 100
default score_log = []          # list of (reason, points_deducted) tuples
default tools_on_tray = []      # correct tools currently on the sterile tray
default tray_slot_of = {}       # tool name -> tray slot index
default tool_pos = {}           # tool name -> current (x, y) on equipment screen
default monitor_checked = []    # indices of checked monitoring items
default inflate_volume = 0      # mL chosen on the inflation slider
default proc_current = 0        # current procedure step (0-4)
default quiz_index = 0
default difficulty = "medium"   # "easy" | "medium" | "hard" — preserved across retries


init -2 python:

    ## ------------------------------------------------------------------
    ## Difficulty
    ## ------------------------------------------------------------------

    ## Each level tunes four things: penalty size, grade thresholds, whether
    ## procedure hints are shown, how many equipment distractors appear, and how
    ## many quiz questions are asked.
    DIFFICULTY = {
        "easy":   {"penalty_mult": 0.5, "expert": 85, "pass": 60,
                   "show_hints": True,  "distractors": 1, "quiz_count": 3},
        "medium": {"penalty_mult": 1.0, "expert": 90, "pass": 70,
                   "show_hints": True,  "distractors": 2, "quiz_count": 5},
        "hard":   {"penalty_mult": 1.5, "expert": 95, "pass": 80,
                   "show_hints": False, "distractors": 4, "quiz_count": 7},
    }

    DIFFICULTY_LABEL = {"easy": _("Easy"), "medium": _("Medium"), "hard": _("Hard")}

    def diff_cfg(key):
        return DIFFICULTY[store.difficulty][key]

    def set_difficulty(name):
        store.difficulty = name

    ## ------------------------------------------------------------------
    ## Scoring
    ## ------------------------------------------------------------------

    def deduct_score(reason, points):
        points = max(1, int(round(points * diff_cfg("penalty_mult"))))
        store.score = max(0, store.score - points)
        store.score_log = store.score_log + [(reason, points)]

    def grade_for(score):
        if score >= diff_cfg("expert"):
            return _("Expert")
        if score >= diff_cfg("pass"):
            return _("Competent")
        return _("Needs Review")

    def grade_color(score):
        if score >= diff_cfg("expert"):
            return "#2d7a4f"
        if score >= diff_cfg("pass"):
            return "#b8860b"
        return "#7a2d2d"

    def reset_training():
        store.score = 100
        store.score_log = []
        store.tools_on_tray = []
        store.tray_slot_of = {}
        store.tool_pos = {}
        store.monitor_checked = []
        store.inflate_volume = 0
        store.proc_current = 0
        store.quiz_index = 0

    ## ------------------------------------------------------------------
    ## Scene 4 — equipment prep data
    ## ------------------------------------------------------------------

    CORRECT_TOOLS = ["ubt_catheter", "syringe", "iv_saline", "speculum", "clamps", "gloves"]

    TOOL_LABELS = {
        "ubt_catheter": _("UBT Balloon Catheter"),
        "syringe": _("50mL Syringe"),
        "iv_saline": _("500mL IV Normal Saline"),
        "speculum": _("Speculum"),
        "clamps": _("Clamps ×2"),
        "gloves": _("Sterile Gloves"),
        "forceps": _("Forceps"),
        "episiotomy": _("Episiotomy Scissors"),
        "suture_kit": _("Suture Kit"),
        "foley": _("Foley Catheter"),
    }

    DISTRACTOR_INFO = {
        "forceps": _("Forceps are used for assisted delivery — they are not needed for balloon tamponade."),
        "episiotomy": _("Episiotomy scissors are used during delivery, not for managing PPH with a balloon."),
        "suture_kit": _("A suture kit repairs tears and lacerations. UBT treats bleeding from an atonic uterus."),
        "foley": _("A Foley catheter drains the bladder — its small balloon (about 30mL) cannot tamponade the uterus. You need the UBT balloon catheter, which holds 250–500mL."),
    }

    ## Distractors added to the shelf, in order — the difficulty level chooses
    ## how many of these appear alongside the 6 correct tools.
    DISTRACTOR_ORDER = ["forceps", "episiotomy", "suture_kit", "foley"]

    def current_shelf():
        """The shelf tools for the active difficulty: 6 correct tools mixed with
        the first N distractors, interleaved so the layout still alternates."""
        distractors = DISTRACTOR_ORDER[:diff_cfg("distractors")]
        shelf = []
        for i, name in enumerate(CORRECT_TOOLS):
            shelf.append(name)
            if i < len(distractors):
                shelf.append(distractors[i])
        return shelf

    def shelf_pos(name):
        i = current_shelf().index(name)
        col, row = i % 2, i // 2
        return (80 + col * 200, 190 + row * 150)

    TRAY_SLOTS = [(1215 + c * 285, 340 + r * 160) for r in range(3) for c in range(2)]

    def init_equipment_positions():
        store.tools_on_tray = []
        store.tray_slot_of = {}
        store.tool_pos = {name: shelf_pos(name) for name in current_shelf()}

    def equipment_dragged(drags, drop):
        """`dragged` callback for shelf tools on the equipment_prep screen."""
        tool = drags[0]
        name = tool.drag_name
        on_tray = (drop is not None and drop.drag_name == "tray")

        if on_tray and name in CORRECT_TOOLS:
            if name not in store.tray_slot_of:
                used = set(store.tray_slot_of.values())
                slot = min(i for i in range(len(TRAY_SLOTS)) if i not in used)
                new_slots = dict(store.tray_slot_of)
                new_slots[name] = slot
                store.tray_slot_of = new_slots
                store.tools_on_tray = store.tools_on_tray + [name]
            pos = TRAY_SLOTS[store.tray_slot_of[name]]
        else:
            # Off the tray (or a distractor): send it back to the shelf.
            if name in store.tray_slot_of:
                new_slots = dict(store.tray_slot_of)
                del new_slots[name]
                store.tray_slot_of = new_slots
                store.tools_on_tray = [t for t in store.tools_on_tray if t != name]
            pos = shelf_pos(name)
            if on_tray:
                msg = DISTRACTOR_INFO[name]
                deduct_score(__("Equipment: chose %s. %s") % (__(TOOL_LABELS[name]), __(msg)), 5)
                renpy.show_screen("feedback", False, _("Wrong tool"), msg, Hide("feedback"))

        new_pos = dict(store.tool_pos)
        new_pos[name] = pos
        store.tool_pos = new_pos
        tool.snap(pos[0], pos[1], 0.25)
        renpy.restart_interaction()
        return None

    ## ------------------------------------------------------------------
    ## Scene 5 — procedure data
    ## ------------------------------------------------------------------

    ## target_pos values are absolute screen coordinates over the patient
    ## diagram (drawn at 120, 180) or the connector inset (step 3).
    PROC_STEPS = [
        {"tool": "speculum", "title": _("Step 1 — Insert the speculum"),
         "target": _("Vaginal opening"), "target_pos": (330, 640),
         "hint": _("Use the speculum first — you must see the cervix before inserting anything.")},
        {"tool": "ubt_catheter", "title": _("Step 2 — Insert the UBT catheter"),
         "target": _("Uterine cavity"), "target_pos": (330, 300),
         "hint": _("Insert the UBT balloon catheter through the cervix into the uterine cavity.")},
        {"tool": "syringe", "title": _("Step 3 — Connect the syringe"),
         "target": _("Inflation port"), "target_pos": (1090, 360),
         "hint": _("Connect the 50mL syringe to the catheter's inflation port (enlarged on the right).")},
        {"tool": None, "title": _("Step 4 — Inflate the balloon"),
         "target": None, "target_pos": None, "hint": None},   # slider step, no drag
        {"tool": "clamps", "title": _("Step 5 — Clamp the catheter"),
         "target": _("Catheter tube"), "target_pos": (330, 700),
         "hint": _("Clamp the catheter tube to keep the saline in and lock the balloon in place.")},
    ]

    PROC_STEP_OF_TOOL = {"speculum": 0, "ubt_catheter": 1, "syringe": 2, "clamps": 4}

    def proc_tools_for(step):
        """Tools shown on the shelf for a procedure step: everything not yet
        used, plus forceps as a permanent distractor."""
        tools = []
        for name in ["speculum", "ubt_catheter", "syringe", "clamps"]:
            if PROC_STEP_OF_TOOL[name] >= step:
                tools.append(name)
        tools.append("forceps")
        return tools

    def proc_shelf_pos(name):
        i = proc_tools_for(store.proc_current).index(name)
        return (1620, 220 + i * 150)

    def procedure_dragged(drags, drop):
        """`dragged` callback for tools on the procedure screen. Returning a
        non-None value ends the call screen interaction (step complete)."""
        tool = drags[0]
        name = tool.drag_name
        step = store.proc_current

        if drop is None or drop.drag_name != "target":
            pos = proc_shelf_pos(name)
            tool.snap(pos[0], pos[1], 0.2)
            return None

        correct = PROC_STEPS[step]["tool"]
        if name == correct:
            return "correct"

        if name in DISTRACTOR_INFO:
            why = DISTRACTOR_INFO[name]
        else:
            why = _("That tool is needed later, not now.")
        deduct_score(__("Procedure step %d: used %s instead of %s.") %
                     (step + 1, __(TOOL_LABELS[name]), __(TOOL_LABELS[correct])), 5)
        renpy.show_screen("red_flash")
        # On easy/medium, prepend the step hint; on hard, show only the reason.
        if diff_cfg("show_hints"):
            body = __(PROC_STEPS[step]["hint"]) + "\n\n" + __(why)
        else:
            body = __(why)
        renpy.show_screen("feedback", False, _("Wrong tool"),
                          body, Hide("feedback"))
        pos = proc_shelf_pos(name)
        tool.snap(pos[0], pos[1], 0.3)
        renpy.restart_interaction()
        return None

    ## ------------------------------------------------------------------
    ## Scene 7 — monitoring checklist
    ## ------------------------------------------------------------------

    MONITOR_ITEMS = [
        _("Vital signs every 15 minutes"),
        _("Uterine fundus — height and tone"),
        _("Vaginal blood loss"),
        _("Urine output"),
        _("Document procedure time and balloon volume"),
    ]

    def toggle_monitor(i):
        if i in store.monitor_checked:
            store.monitor_checked = [x for x in store.monitor_checked if x != i]
        else:
            store.monitor_checked = store.monitor_checked + [i]

    ## ------------------------------------------------------------------
    ## Scene 8 — quiz data
    ## ------------------------------------------------------------------

    QUIZ_QUESTIONS = [
        {
            "q": _("What volume of saline is used to inflate a UBT balloon?"),
            "options": [_("50–100mL"), _("250–500mL"), _("1000mL"), _("750mL")],
            "correct": 1,
            "explain": _("The UBT balloon is inflated with 250–500mL of normal saline — enough to press firmly against the uterine wall without over-distending it."),
            "fix": _("UBT balloon volume is 250–500mL of saline."),
        },
        {
            "q": _("After insertion, how long should the balloon remain before deflation?"),
            "options": [_("30 minutes"), _("2–4 hours"), _("24–48 hours"), _("1 week")],
            "correct": 2,
            "explain": _("The balloon stays in place for 24–48 hours, then is deflated gradually while watching for re-bleeding."),
            "fix": _("The balloon remains 24–48 hours before staged deflation."),
        },
        {
            "q": _("PPH is defined as blood loss of more than _____ mL after vaginal delivery."),
            "options": [_("250mL"), _("500mL"), _("1000mL"), _("100mL")],
            "correct": 1,
            "explain": _("PPH is blood loss over 500mL after vaginal delivery (or over 1000mL after caesarean section)."),
            "fix": _("PPH is more than 500mL blood loss after vaginal delivery."),
        },
        {
            "q": _("Which of the following is a contraindication to UBT?"),
            "options": [_("Placenta previa"), _("Atonic uterus"), _("Uterine rupture"), _("Cervical dilation")],
            "correct": 2,
            "explain": _("UBT must not be used with uterine rupture — the balloon cannot control bleeding through a torn uterine wall and delays surgery. An atonic uterus is the main indication for UBT."),
            "fix": _("Uterine rupture is a contraindication to UBT."),
        },
        {
            "q": _("What does 'tamponade test positive' mean?"),
            "options": [_("The balloon has ruptured"),
                        _("Bleeding has stopped after balloon inflation"),
                        _("The patient needs immediate surgery"),
                        _("The balloon is fully deflated")],
            "correct": 1,
            "explain": _("'Tamponade test positive' means bleeding stops (or slows markedly) after inflation — the balloon is controlling the hemorrhage."),
            "fix": _("Tamponade test positive means bleeding stopped after inflation."),
        },
    ]

    ## Extra questions asked only on Hard (appended after the base five).
    QUIZ_ADVANCED = [
        {
            "q": _("If the tamponade test is negative — bleeding continues after inflation — what is the priority?"),
            "options": [_("Add more saline until it stops"),
                        _("Escalate urgently for surgical management"),
                        _("Deflate and re-observe for an hour"),
                        _("Give a second dose of oxytocin and wait")],
            "correct": 1,
            "explain": _("A negative tamponade test means UBT has not controlled the bleeding. Do not delay — escalate immediately for surgical management (e.g. laparotomy) while resuscitation continues."),
            "fix": _("A negative tamponade test means escalate urgently for surgery — don't just add saline or wait."),
        },
        {
            "q": _("While the balloon is in place, which of these should also be given?"),
            "options": [_("Prophylactic antibiotics"),
                        _("Nothing further is needed"),
                        _("Immediate balloon deflation every hour"),
                        _("Oral iron only")],
            "correct": 0,
            "explain": _("An indwelling uterine balloon is a foreign body, so prophylactic antibiotics are given to reduce infection risk while uterotonics and monitoring continue."),
            "fix": _("Give prophylactic antibiotics while the balloon is in place."),
        },
    ]

    def active_quiz():
        """The quiz questions for the active difficulty: the base set, extended
        with advanced questions, truncated to the level's quiz_count."""
        return (QUIZ_QUESTIONS + QUIZ_ADVANCED)[:diff_cfg("quiz_count")]
