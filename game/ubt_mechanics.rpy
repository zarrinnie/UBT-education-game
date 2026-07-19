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


init -2 python:

    ## ------------------------------------------------------------------
    ## Scoring
    ## ------------------------------------------------------------------

    def deduct_score(reason, points):
        store.score = max(0, store.score - points)
        store.score_log = store.score_log + [(reason, points)]

    def grade_for(score):
        if score >= 90:
            return _("Expert")
        if score >= 70:
            return _("Competent")
        return _("Needs Review")

    def grade_color(score):
        if score >= 90:
            return "#2d7a4f"
        if score >= 70:
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

    ## Shelf mixes correct tools and distractors.
    SHELF_ORDER = ["ubt_catheter", "forceps", "syringe", "episiotomy",
                   "iv_saline", "suture_kit", "speculum", "foley",
                   "clamps", "gloves"]

    def shelf_pos(name):
        i = SHELF_ORDER.index(name)
        col, row = i % 2, i // 2
        return (80 + col * 200, 190 + row * 150)

    TRAY_SLOTS = [(1215 + c * 285, 340 + r * 160) for r in range(3) for c in range(2)]

    def init_equipment_positions():
        store.tools_on_tray = []
        store.tray_slot_of = {}
        store.tool_pos = {name: shelf_pos(name) for name in SHELF_ORDER}

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
        renpy.show_screen("feedback", False, _("Wrong tool"),
                          __(PROC_STEPS[step]["hint"]) + "\n\n" + __(why), Hide("feedback"))
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
