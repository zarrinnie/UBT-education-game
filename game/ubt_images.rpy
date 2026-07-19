## ubt_images.rpy — art for UBT Trainer.
##
## Real PNG assets live under game/images/. Each image below wraps its PNG in a
## Transform sized to the box the screen layouts in ubt_screens.rpy /
## ubt_mechanics.rpy are calibrated around. Palette: light teal #E0F5F5,
## warm white #FAFAFA, deep teal #2a7a7a, ink #1e3a3a.

init -1 python:

    # A rounded white nine-patch tinted to `hexcolor`. Reused everywhere.
    def _round_tinted(hexcolor):
        return Transform("gui/round_panel.png", matrixcolor=TintMatrix(hexcolor))

    # Rounded-corner panel background for `frame` styles (auto-sizes to the frame).
    def rpanel(hexcolor, alpha=1.0, border=20):
        d = Frame(_round_tinted(hexcolor), border, border)
        if alpha < 1.0:
            d = Transform(d, alpha=alpha)
        return d

    # A fixed-size rounded rectangle (single nine-patch Frame) for compositing.
    def rbox(hexcolor, w, h, alpha=1.0, xpos=0, ypos=0, border=16):
        d = Frame(_round_tinted(hexcolor), border, border, xysize=(w, h),
                  xpos=xpos, ypos=ypos)
        if alpha < 1.0:
            d = Transform(d, alpha=alpha, xpos=xpos, ypos=ypos)
        return d

    # Framed tool tile: rounded card, illustration above a colored caption bar.
    # Fixed 170x130 box so drag/drop hit-detection and shelf/tray spacing stay valid.
    def ubt_tool_tile(name, label_text, color, w=170, h=130, cap=44):
        return Fixed(
            rbox("#1e3a3a", w, h),                                       # rounded ink border
            rbox("#FAFAFA", w - 6, h - 6, xpos=3, ypos=3),              # rounded white face
            Fixed(
                Transform("images/tools/tool_" + name + ".png", fit="contain",
                          xysize=(w - 24, h - cap - 17), align=(0.5, 0.5)),
                xysize=(w - 24, h - cap - 17), xpos=12, ypos=7,
            ),
            rbox(color, w - 12, cap, xpos=6, ypos=h - cap - 5, border=14),
            Fixed(
                Text(label_text, size=13, color="#ffffff", bold=True,
                     text_align=0.5, xalign=0.5, yalign=0.5, xmaximum=w - 24),
                xysize=(w - 12, cap), xpos=6, ypos=h - cap - 5,
            ),
            xysize=(w, h),
        )

    # Rounded, translucent drop target zone (animated via target_pulse in the screen).
    def ubt_drop_zone(label_text, w=190, h=120):
        return Fixed(
            rbox("#2a7a7a", w, h, alpha=0.35),
            rbox("#2a7a7a", w - 10, h - 10, alpha=0.85, xpos=5, ypos=5),
            Text("⬇ " + __(label_text), size=22, color="#ffffff", bold=True,
                 text_align=0.5, xalign=0.5, yalign=0.5, xmaximum=w - 16),
            xysize=(w, h),
        )

    TOOL_COLORS = {
        "ubt_catheter": "#c46a6a",
        "syringe": "#5a8fb5",
        "iv_saline": "#4a9a7a",
        "speculum": "#7a6ab5",
        "clamps": "#b58a4a",
        "gloves": "#4aa5a5",
        "forceps": "#8a8a8a",
        "episiotomy": "#9a7a9a",
        "suture_kit": "#7a9a5a",
        "foley": "#b5b55a",
    }

    # One image per tool — illustration + name caption.
    for _name, _label in TOOL_LABELS.items():
        renpy.image("tool_" + _name, ubt_tool_tile(_name, _label, TOOL_COLORS.get(_name, "#4a7fa5")))


## Backgrounds — scaled to fill the 1920x1080 screen (cover crops overflow).
image main_menu_bg = Transform("images/backgrounds/main_menu_art.png", fit="cover", xysize=(1920, 1080))
image bg clinic = Transform("images/backgrounds/hospital_lobby.png", fit="cover", xysize=(1920, 1080))
image bg exam   = Transform("images/backgrounds/hospital_room.png",  fit="cover", xysize=(1920, 1080))

## Medical diagrams / status graphics — scaled to the boxes the layouts expect.
image patient_diagram = Transform("images/patient_diagram.png", xysize=(700, 650))
image connector_inset = Transform("images/connector_inset.png", xysize=(420, 330))
image ubt_tray        = Transform("images/ubt_tray.png",        xysize=(620, 560))
image intro_cross     = Transform("images/intro_cross.png",     xysize=(200, 200))
image clamp_locked    = Transform("images/clamp_locked.png", fit="contain", xysize=(520, 120))

## Nurse sprites (player character) — shown during dialogue scenes.
image nurse profile = "images/characters/nurse_profile.png"
image nurse writing = "images/characters/nurse_writing.png"

transform nurse_stand:
    xalign 0.02
    yalign 1.0

transform ubt_pulse:
    alpha 0.65
    linear 0.9 alpha 1.0
    linear 0.9 alpha 0.65
    repeat

## Fade-in for full-screen modal backdrops (Solids). NOTE: do NOT apply an
## *animated* transform to an auto-sizing `frame`/`window` — in this Ren'Py
## version that makes the panel's background expand to fill the whole layer
## (a static transform is fine; an animated one is not). Only animate
## fixed-size displayables (see target_pulse) or full-screen Solids.
transform dim_in:
    alpha 0.0
    linear 0.2 alpha 1.0

## Slow breathing glow for the procedure drop-targets.
transform target_pulse:
    alpha 0.75 zoom 1.0
    block:
        ease 0.9 alpha 1.0 zoom 1.03
        ease 0.9 alpha 0.75 zoom 1.0
        repeat
