## script.rpy — UBT Trainer main story flow.
##
## Scene order:
## intro → assessment → call_for_help → equipment_prep → procedure
##       → assessment_check → monitoring → quiz → results

define dr = Character("Dr. Amina", color="#7fd0d0")


label start:
    $ reset_training()
    jump scene_intro


## SCENE 1 — INTRO ############################################################

label scene_intro:
    scene bg clinic
    call screen intro_screen

    show nurse profile at nurse_stand with dissolve
    "You are a nurse on the maternity ward of a rural clinic."
    "Your patient, Maria, delivered a healthy baby twenty minutes ago. Suddenly, the doctor calls you urgently."
    dr "I need you here, now! Maria is bleeding heavily and it isn't slowing down."
    "Every decision from here on counts. Your training starts now."

    jump scene_assessment


## SCENE 2 — ASSESSMENT #######################################################

label scene_assessment:
    scene bg exam with dissolve
    show screen score_hud
    show screen vitals_card
    show nurse profile at nurse_stand

    dr "Here are her vitals. She delivered vaginally, the placenta is out and complete, and an oxytocin infusion is already running — but the bleeding continues."

    hide screen vitals_card
    show screen vitals_button

    menu:
        "Look at the vitals. Is this postpartum hemorrhage (PPH)?"

        "Yes — blood loss over 500mL with signs of shock.":
            call screen feedback(True, _("Correct"),
                _("Blood loss above 500mL after vaginal delivery is PPH. Her fast heart rate, low blood pressure and pale, clammy skin mean she is going into shock. Act now."))

        "No — this is normal postpartum bleeding.":
            $ deduct_score(__("Assessment: mistook PPH for normal bleeding. More than 500mL after vaginal delivery, with signs of shock, is PPH."), 10)
            call screen feedback(False, _("Incorrect"),
                _("This is not normal. Blood loss above 500mL after vaginal delivery is PPH — and her fast heart rate, low blood pressure and clammy skin are signs of shock."))

        "Unsure — wait and observe.":
            $ deduct_score(__("Assessment: waited instead of acting. Delay costs lives in PPH — recognise and act immediately."), 10)
            call screen feedback(False, _("Incorrect"),
                _("There is no time to wait. Blood loss above 500mL with signs of shock is PPH. Every minute of delay increases the danger to the mother's life."))

    hide screen vitals_button
    hide screen vitals_popup
    jump scene_call_for_help


## SCENE 3 — CALL FOR HELP ####################################################

label scene_call_for_help:
    dr "You've recognised the emergency. What do you do first?"

    menu:
        "What do you do first?"

        "Shout for help and call the emergency team.":
            call screen feedback(True, _("Correct"),
                _("PPH is a team emergency. Call for help first — you need extra hands for medication, monitoring, and preparing equipment while you stay with the patient."))

        "Insert the balloon immediately, by yourself.":
            $ deduct_score(__("First response: tried to manage PPH alone. Always call the team first — PPH management needs several people working together."), 10)
            call screen feedback(False, _("Incorrect"),
                _("Never manage PPH alone. Call for help first — one person cannot give drugs, monitor vitals, prepare equipment and perform the procedure at the same time."))

        "Quietly recheck her blood pressure.":
            $ deduct_score(__("First response: rechecked BP instead of calling for help. The diagnosis is already clear — escalate immediately."), 10)
            call screen feedback(False, _("Incorrect"),
                _("The vitals already tell the story. Rechecking wastes precious minutes — call the emergency team immediately, then continue monitoring."))

    dr "The team is here. Uterotonics haven't stopped the bleeding — the uterus is atonic. We need a uterine balloon tamponade."
    jump scene_equipment_prep


## SCENE 4 — EQUIPMENT PREP (drag-and-drop) ###################################

label scene_equipment_prep:
    dr "Gather the UBT equipment onto the sterile tray. Quickly, but choose carefully."

    $ init_equipment_positions()
    call screen equipment_prep

    dr "Good. Everything we need is on the tray. Gloves on — let's begin."
    jump scene_procedure


## SCENE 5 — PROCEDURE (ordered drag-and-drop steps) ##########################

label scene_procedure:
    dr "I'll guide you through the insertion. Follow each step in order."

    $ proc_current = 0
    call screen procedure_screen(0)
    "Speculum inserted. The cervix is now visible."

    $ proc_current = 1
    call screen procedure_screen(1)
    "You pass the UBT balloon catheter through the cervix into the uterine cavity."

    $ proc_current = 2
    call screen procedure_screen(2)
    "The 50mL syringe is connected to the catheter's inflation port."

    $ proc_current = 3
    call proc_inflate
    "The balloon is inflated with [inflate_volume]mL of normal saline."

    $ proc_current = 4
    call screen procedure_screen(4)
    show clamp_locked at truecenter with dissolve
    "The catheter is clamped. The balloon is locked in place."
    hide clamp_locked with dissolve

    jump scene_assessment_check


## Scene 5d — inflation slider with range check
label proc_inflate:
    call screen inflation_slider
    if 250 <= inflate_volume <= 500:
        return
    elif inflate_volume < 250:
        $ deduct_score(__("Inflation: under-inflated the balloon (%dmL). 250–500mL is needed for effective tamponade.") % inflate_volume, 5)
        call screen feedback(False, _("Under-inflated"),
            _("With less than 250mL, the balloon cannot press firmly against the uterine wall — the bleeding will continue. Draw up more saline and try again."))
        jump proc_inflate
    else:
        $ deduct_score(__("Inflation: over-inflated the balloon (%dmL). More than 500mL risks uterine injury.") % inflate_volume, 5)
        call screen feedback(False, _("Over-inflated"),
            _("More than 500mL over-distends the uterus and risks rupture or balloon failure. Release some saline and try again."))
        jump proc_inflate


## SCENE 6 — ASSESSMENT CHECK #################################################

label scene_assessment_check:
    dr "The balloon is in place. What do you check now?"

    menu:
        "The balloon is in place. What do you check now?"

        "Check whether the bleeding has stopped — the tamponade test.":
            call screen feedback(True, _("Correct"),
                _("If bleeding stops or slows markedly after inflation, the tamponade test is positive — the balloon is working. If bleeding continues, she needs escalation."))

        "Deflate the balloon to check underneath.":
            $ deduct_score(__("Post-insertion: deflated the balloon immediately. It must stay inflated for 24–48 hours to control the bleeding."), 10)
            call screen feedback(False, _("Incorrect"),
                _("Never deflate the balloon right after insertion — it must stay inflated for 24–48 hours. Instead, check whether visible bleeding has stopped: the tamponade test."))

        "Give more oxytocin and wait.":
            $ deduct_score(__("Post-insertion: relied on oxytocin alone instead of doing the tamponade test first."), 5)
            call screen feedback(False, _("Partially right"),
                _("Uterotonics do continue alongside UBT — but first you must confirm the balloon is working. Check whether the bleeding has stopped: the tamponade test."))

    dr "Bleeding has stopped — tamponade test positive. Well done. Now she needs close monitoring."
    jump scene_monitoring


## SCENE 7 — MONITORING CHECKLIST #############################################

label scene_monitoring:
    show nurse writing at nurse_stand
    call screen monitoring_checklist

    "Monitoring plan confirmed. Maria remains stable. The balloon will stay in place for 24–48 hours, then be deflated gradually while watching for re-bleeding."
    jump scene_quiz


## SCENE 8 — QUIZ #############################################################

label scene_quiz:
    show nurse writing at nurse_stand
    dr "Maria is safe. Before we finish — a quick knowledge check. Five questions."

    $ quiz_index = 0
    while quiz_index < 5:
        $ q = QUIZ_QUESTIONS[quiz_index]
        call screen quiz_screen(quiz_index)
        if _return == q["correct"]:
            call screen feedback(True, _("Correct"), q["explain"])
        else:
            $ deduct_score(__("Quiz Q%d: %s") % (quiz_index + 1, __(q["fix"])), 5)
            call screen feedback(False, _("Incorrect"), q["explain"])
        $ quiz_index += 1

    jump scene_results


## SCENE 9 — RESULTS ##########################################################

label scene_results:
    hide nurse
    hide screen score_hud
    scene bg clinic with dissolve
    call screen results_screen

    if _return == "again":
        $ reset_training()
        jump scene_assessment

    return
