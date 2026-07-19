## ubt_screens.rpy — game screens for UBT Trainer.
## New styles are defined here so screens.rpy and gui.rpy stay untouched.

## ---------------------------------------------------------------------------
## Styles
## ---------------------------------------------------------------------------

style ubt_frame is frame:
    background rpanel("#FAFAFA", alpha=0.93)
    padding (30, 24)

style ubt_text is text:
    color "#1e3a3a"
    size 26

style ubt_title is text:
    color "#1e3a3a"
    size 40
    bold True

style ubt_button is button:
    background rpanel("#2a7a7a")
    hover_background rpanel("#3a9a9a")
    padding (28, 14)

style ubt_button_text is button_text:
    color "#ffffff"
    hover_color "#ffffff"
    size 28
    bold True

style ubt_check_button is button:
    background None

style ubt_check_button_text is button_text:
    color "#1e3a3a"
    hover_color "#2a7a7a"
    size 28

style ubt_quiz_button is button:
    background rpanel("#e8f4f4")
    hover_background rpanel("#cfeaea")
    xsize 1100
    padding (24, 14)

style ubt_quiz_button_text is button_text:
    color "#1e3a3a"
    hover_color "#1e3a3a"
    size 27
    text_align 0.0

## Main menu bottom-dock buttons.
style ubt_nav_button is button:
    background rpanel("#2a7a7a")
    hover_background rpanel("#3a9a9a")
    padding (30, 14)
    yalign 0.5

style ubt_nav_button_text is button_text:
    color "#ffffff"
    hover_color "#E0F5F5"
    size 28
    bold True

## Rounded in-game choice menu buttons (match the rest of the rounded UI).
style choice_button:
    background rpanel("#1e3a3a", alpha=0.85)
    hover_background rpanel("#2a7a7a")

style choice_button_text:
    color "#ffffff"
    hover_color "#ffffff"


## ---------------------------------------------------------------------------
## Shared: score HUD, feedback overlay, red flash, step progress
## ---------------------------------------------------------------------------

screen score_hud():
    zorder 100
    frame:
        style "ubt_frame"
        xalign 0.985
        ypos 20
        text "Score: [score]" style "ubt_text" size 30 bold True

screen feedback(correct, title, message, continue_action=Return()):
    modal True
    zorder 200
    add Solid("#00000088") at dim_in
    frame:
        background (rpanel("#2d7a4f") if correct else rpanel("#7a2d2d"))
        xalign 0.5
        yalign 0.5
        xsize 900
        padding (40, 32)
        vbox:
            spacing 22
            text (("✓  " if correct else "✗  ") + title) size 44 color "#ffffff" bold True
            text message size 27 color "#ffffff"
            textbutton "Continue" style "ubt_button" action continue_action xalign 1.0

transform ubt_flash_out:
    alpha 0.55
    linear 0.5 alpha 0.0

screen red_flash():
    zorder 150
    add Solid("#cc2222") at ubt_flash_out
    timer 0.55 action Hide("red_flash")

screen step_progress(stepnum):
    zorder 80
    frame:
        style "ubt_frame"
        xalign 0.5
        ypos 20
        hbox:
            spacing 14
            text "STEP [stepnum] of 5" style "ubt_text" bold True yalign 0.5
            for i in range(5):
                add Solid(("#2a7a7a" if i < stepnum else "#b8d8d8"), xsize=44, ysize=16) yalign 0.5


## ---------------------------------------------------------------------------
## Scene 1 — intro
## ---------------------------------------------------------------------------

screen intro_screen():
    add "bg clinic"
    frame:
        background rpanel("#1e3a3a", alpha=0.78)
        xalign 0.5
        yalign 0.45
        padding (70, 48)
        vbox:
            spacing 28
            add "intro_cross" at ubt_pulse xalign 0.5
            text "UBT TRAINER" size 64 bold True color "#ffffff" xalign 0.5
            text "Uterine Balloon Tamponade — Interactive Tutorial" size 30 color "#E0F5F5" xalign 0.5
            null height 16
            textbutton "Begin Training" style "ubt_button" action Return() xalign 0.5


## ---------------------------------------------------------------------------
## Scene 2 — vitals card (shown alongside dialogue)
## ---------------------------------------------------------------------------

## Shared vitals content — used by the side card and the popup.
screen vitals_info():
    vbox:
        spacing 14
        text "PATIENT VITALS" style "ubt_text" size 30 bold True
        text "Heart rate: 128 bpm (high)" style "ubt_text"
        text "Blood pressure: 88/54 mmHg (low)" style "ubt_text"
        text "Est. blood loss: ~700mL, ongoing" style "ubt_text"
        text "Skin: pale, clammy" style "ubt_text"
        text "Uterus: soft, poorly contracted" style "ubt_text"

## Side card shown while the doctor presents the vitals (hidden before choices).
screen vitals_card():
    zorder 90
    frame:
        style "ubt_frame"
        xpos 1380
        ypos 140
        xsize 480
        use vitals_info

## Small button available while the choice menu is up.
screen vitals_button():
    zorder 95
    textbutton "▤  See patient vitals":
        style "ubt_button"
        xalign 0.985
        ypos 110
        action Show("vitals_popup")

## Vitals as a popup: click anywhere outside the card to close it. The
## full-screen dismiss button swallows every click, so `modal` is not needed
## (and `modal True` + `renpy.pause` proved unreliable in this Ren'Py version).
screen vitals_popup():
    zorder 190
    add Solid("#00000066") at dim_in
    button:
        xfill True
        yfill True
        background None
        action Hide("vitals_popup")
    button:
        background rpanel("#FAFAFA", alpha=0.97)
        xalign 0.5
        yalign 0.5
        padding (44, 36)
        action NullAction()
        use vitals_info


## ---------------------------------------------------------------------------
## Scene 4 — equipment prep drag-and-drop
## ---------------------------------------------------------------------------

screen equipment_prep():
    add "bg exam"

    frame:
        style "ubt_frame"
        xalign 0.5
        ypos 20
        vbox:
            spacing 6
            text "Prepare the equipment tray" style "ubt_title" xalign 0.5
            text "Drag the 6 tools needed for UBT onto the sterile tray." style "ubt_text" xalign 0.5

    draggroup:
        drag:
            drag_name "tray"
            draggable False
            droppable True
            xpos 1150
            ypos 270
            add "ubt_tray"

        for name in SHELF_ORDER:
            drag:
                drag_name name
                drag_raise True
                droppable False
                dragged equipment_dragged
                xpos tool_pos[name][0]
                ypos tool_pos[name][1]
                add ("tool_" + name)

    frame:
        style "ubt_frame"
        xpos 80
        yalign 0.96
        text "On tray: [len(tools_on_tray)] / 6" style "ubt_text" bold True

    if len(tools_on_tray) == 6:
        textbutton "Proceed ▶" style "ubt_button" action Return() xalign 0.97 yalign 0.96


## ---------------------------------------------------------------------------
## Scene 5 — procedure drag-and-drop steps
## ---------------------------------------------------------------------------

screen procedure_screen(step):
    add "bg exam"
    use step_progress(step + 1)

    frame:
        style "ubt_frame"
        xalign 0.5
        ypos 110
        vbox:
            spacing 6
            text PROC_STEPS[step]["title"] style "ubt_title" size 34 xalign 0.5
            text "Drag the correct tool to the highlighted target." style "ubt_text" xalign 0.5

    add "patient_diagram" xpos 120 ypos 180

    if step == 2:
        add "connector_inset" xpos 1000 ypos 240

    draggroup:
        drag:
            drag_name "target"
            draggable False
            droppable True
            xpos PROC_STEPS[step]["target_pos"][0]
            ypos PROC_STEPS[step]["target_pos"][1]
            add ubt_drop_zone(PROC_STEPS[step]["target"]) at target_pulse

        for i, name in enumerate(proc_tools_for(step)):
            drag:
                drag_name name
                drag_raise True
                droppable False
                dragged procedure_dragged
                xpos 1620
                ypos (220 + i * 150)
                add ("tool_" + name)


## Scene 5d — inflation slider
screen inflation_slider():
    add "bg exam"
    use step_progress(4)

    frame:
        style "ubt_frame"
        xalign 0.5
        yalign 0.5
        xsize 900
        vbox:
            spacing 26
            text "Inflate the balloon" style "ubt_title"
            text "Draw up normal saline and inflate the balloon.\nTarget: 250–500mL." style "ubt_text"
            bar value VariableValue("inflate_volume", 700) xsize 800
            text "Volume: [inflate_volume] mL" style "ubt_text" size 34 bold True
            textbutton "Confirm inflation" style "ubt_button" action Return()


## ---------------------------------------------------------------------------
## Scene 7 — monitoring checklist
## ---------------------------------------------------------------------------

screen monitoring_checklist():
    add "bg exam"
    frame:
        style "ubt_frame"
        xalign 0.5
        yalign 0.5
        xsize 1000
        vbox:
            spacing 18
            text "Monitoring plan" style "ubt_title"
            text "Select every item you will monitor while the balloon is in place:" style "ubt_text"
            null height 6
            for i, item in enumerate(MONITOR_ITEMS):
                textbutton (("☑  " if i in monitor_checked else "☐  ") + item):
                    style "ubt_check_button"
                    action Function(toggle_monitor, i)
            null height 6
            if len(monitor_checked) == len(MONITOR_ITEMS):
                textbutton "Monitoring plan confirmed ▶" style "ubt_button" action Return()


## ---------------------------------------------------------------------------
## Scene 8 — quiz
## ---------------------------------------------------------------------------

screen quiz_screen(index):
    add "bg exam"
    $ q = QUIZ_QUESTIONS[index]
    $ qnum = index + 1
    $ qtotal = len(QUIZ_QUESTIONS)
    frame:
        style "ubt_frame"
        xalign 0.5
        yalign 0.5
        xsize 1250
        vbox:
            spacing 20
            text "Question [qnum] of [qtotal]" style "ubt_text" size 22
            text q["q"] style "ubt_title" size 34
            null height 10
            for i, opt in enumerate(q["options"]):
                textbutton ("ABCD"[i] + ".   " + opt) style "ubt_quiz_button" action Return(i)


## ---------------------------------------------------------------------------
## Scene 9 — results
## ---------------------------------------------------------------------------

screen results_screen():
    add "bg clinic"
    frame:
        style "ubt_frame"
        xalign 0.5
        yalign 0.5
        xsize 1300
        vbox:
            spacing 18
            text "Training results" style "ubt_title"
            text "Final score: [score] / 100" style "ubt_text" size 36 bold True
            text ("Grade: " + grade_for(score)) size 40 bold True color grade_color(score)
            null height 8
            if score_log:
                text "What to review:" style "ubt_text" bold True
                viewport:
                    ysize 360
                    scrollbars "vertical"
                    mousewheel True
                    vbox:
                        spacing 12
                        for reason, pts in score_log:
                            text "−[pts]   [reason]" style "ubt_text" size 24
            else:
                text "Perfect run — no mistakes. Excellent work!" style "ubt_text" bold True color "#2d7a4f"
            null height 12
            hbox:
                spacing 30
                textbutton "Review Again" style "ubt_button" action Return("again")
                textbutton "Exit" style "ubt_button" action Return("exit")
