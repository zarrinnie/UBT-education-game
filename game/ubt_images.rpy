## ubt_images.rpy — placeholder art for UBT Trainer.
##
## Every displayable in this file is a flat Solid/Text composite standing in
## for a future flat-illustration SVG asset. Palette: light teal #E0F5F5,
## warm white #FAFAFA, deep teal #2a7a7a, ink #1e3a3a.

init -1 python:

    # TODO: replace with illustrated asset — generic labeled tool tile
    def ubt_tile(label_text, color, w=170, h=110, ts=20):
        return Fixed(
            Solid("#1e3a3a"),                                            # bold outline
            Transform(Solid(color), xpos=4, ypos=4, xsize=w - 8, ysize=h - 8),
            Text(label_text, size=ts, color="#ffffff", bold=True,
                 text_align=0.5, xalign=0.5, yalign=0.5, xmaximum=w - 16),
            xysize=(w, h),
        )

    # TODO: replace with illustrated asset — highlighted drop target zone
    def ubt_drop_zone(label_text, w=190, h=120):
        return Fixed(
            Solid("#ffffff"),
            Transform(Solid("#2a7a7aaa"), xpos=4, ypos=4, xsize=w - 8, ysize=h - 8),
            Text("⬇ " + label_text, size=22, color="#ffffff", bold=True,
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

    # TODO: replace with illustrated assets — one image per tool
    for _name, _label in TOOL_LABELS.items():
        renpy.image("tool_" + _name, ubt_tile(_label, TOOL_COLORS.get(_name, "#4a7fa5")))

    # TODO: replace with illustrated asset — stylized patient cross-section diagram
    def ubt_patient_diagram(w=700, h=650):
        return Fixed(
            Solid("#1e3a3a"),
            Transform(Solid("#f5e6d3"), xpos=4, ypos=4, xsize=w - 8, ysize=h - 8),
            Text("PATIENT — CROSS-SECTION (stylized diagram)", size=20, bold=True,
                 color="#5a4a3a", xalign=0.5, ypos=24),
            # uterus
            Transform(Solid("#e8b4b8"), xpos=190, ypos=80, xsize=320, ysize=210),
            Text("Uterus", size=26, bold=True, color="#5a2d33", xpos=300, ypos=160),
            # cervix
            Transform(Solid("#d49aa0"), xpos=270, ypos=290, xsize=160, ysize=90),
            Text("Cervix", size=22, bold=True, color="#5a2d33", xpos=305, ypos=320),
            # vaginal canal
            Transform(Solid("#c9848c"), xpos=300, ypos=380, xsize=100, ysize=200),
            Text("Vaginal\ncanal", size=20, bold=True, color="#ffffff",
                 text_align=0.5, xpos=308, ypos=440),
            xysize=(w, h),
        )

    # TODO: replace with illustrated asset — enlarged catheter inflation port inset
    def ubt_connector_inset(w=420, h=330):
        return Fixed(
            Solid("#1e3a3a"),
            Transform(Solid("#FAFAFA"), xpos=4, ypos=4, xsize=w - 8, ysize=h - 8),
            Text("Catheter inflation port\n(enlarged view)", size=22, bold=True,
                 color="#1e3a3a", text_align=0.5, xalign=0.5, ypos=24),
            Transform(Solid("#c46a6a"), xpos=180, ypos=120, xsize=60, ysize=180),
            Text("Port", size=20, bold=True, color="#ffffff", xpos=188, ypos=190),
            xysize=(w, h),
        )

    # TODO: replace with illustrated asset — sterile equipment tray
    def ubt_tray_img(w=620, h=560):
        return Fixed(
            Solid("#1e3a3a"),
            Transform(Solid("#c8d8d8"), xpos=4, ypos=4, xsize=w - 8, ysize=h - 8),
            Text("STERILE TRAY", size=30, bold=True, color="#4a6a6a",
                 xalign=0.5, ypos=20),
            xysize=(w, h),
        )


## TODO: replace with illustrated asset — maternity ward background
image bg clinic = Fixed(
    Solid("#2a7a7a"),
    Text("MATERNITY WARD  (placeholder background)", size=28, bold=True,
         color="#ffffff40", xalign=0.5, ypos=40),
)

## TODO: replace with illustrated asset — procedure room background
image bg exam = Fixed(
    Solid("#E0F5F5"),
    Text("PROCEDURE ROOM  (placeholder background)", size=28, bold=True,
         color="#1e3a3a30", xalign=0.5, ypos=40),
)

image patient_diagram = ubt_patient_diagram()
image connector_inset = ubt_connector_inset()
image ubt_tray = ubt_tray_img()

## TODO: replace with illustrated asset — animated medical cross for the intro
image intro_cross = Fixed(
    Solid("#2a7a7a"),
    Transform(Solid("#FAFAFA"), xpos=8, ypos=8, xsize=184, ysize=184),
    Text("+", size=150, bold=True, color="#2a7a7a", xalign=0.5, yalign=0.42),
    xysize=(200, 200),
)

## TODO: replace with illustrated asset — clamped catheter "locked" state
image clamp_locked = Fixed(
    Solid("#1e3a3a"),
    Transform(Solid("#2d7a4f"), xpos=4, ypos=4, xsize=512, ysize=112),
    Text("✓ CLAMPED — balloon locked in place", size=28, bold=True,
         color="#ffffff", xalign=0.5, yalign=0.5),
    xysize=(520, 120),
)

transform ubt_pulse:
    alpha 0.65
    linear 0.9 alpha 1.0
    linear 0.9 alpha 0.65
    repeat
