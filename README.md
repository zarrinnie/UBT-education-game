# UBT Trainer (UBTedugame)

An interactive educational game built with [Ren'Py](https://www.renpy.org/) that trains nurses and midwives to recognise and manage **postpartum hemorrhage (PPH)** using **uterine balloon tamponade (UBT)**.

The player takes the role of a nurse on the maternity ward of a rural clinic. When a patient begins bleeding heavily after delivery, every decision counts: the game walks through the full emergency — recognising PPH, calling for help, preparing equipment, performing the balloon insertion, and monitoring the patient — while scoring each choice and giving immediate clinical feedback.

## Features

- **Scenario-based training flow** — nine scenes covering the complete UBT protocol: intro → assessment → call for help → equipment prep → procedure → tamponade check → monitoring → quiz → results.
- **Decision-point menus with clinical feedback** — every choice (right or wrong) is followed by an explanation of the underlying clinical reasoning.
- **Drag-and-drop equipment prep** — gather the correct UBT tools onto a sterile tray from a shelf that mixes in distractors (forceps, episiotomy scissors, suture kit, Foley catheter), each with an explanation of why it's wrong.
- **Ordered procedure steps** — perform the insertion in the correct sequence: speculum, catheter placement, syringe connection, inflation, clamping.
- **Inflation slider with range check** — the balloon must be inflated within the safe 250–500 mL range; under- and over-inflation are penalised and explained.
- **Monitoring checklist** — build the post-insertion monitoring plan.
- **Five-question knowledge quiz** — reinforces key facts after the scenario.
- **Scoring and grading** — players start at 100 points; mistakes deduct points and are logged with reasons. Final grades: *Expert* (≥90), *Competent* (≥70), *Needs Review* (<70), with the option to retry the training.

## Tech Stack

- **[Ren'Py 8.5](https://www.renpy.org/)** — visual novel engine (Python-based). All game logic is written in Ren'Py script and embedded Python; there are no external dependencies.
- Placeholder art is generated programmatically (flat colour tiles in `ubt_images.rpy`), intended to be replaced with illustrated SVG-derived assets later.

## Installation

1. **Install the Ren'Py SDK** (8.5.x recommended) from [renpy.org](https://www.renpy.org/latest.html).

2. **Clone the repository:**

   ```sh
   git clone <repository-url>
   cd UBTedugame
   ```

3. **Run the game.** Either:

   - **Ren'Py Launcher:** open the launcher, add the `UBTedugame` directory as a project (place or symlink it into your Ren'Py projects folder), then click **Launch Project**; or

   - **Command line:**

     ```sh
     /path/to/renpy-sdk/renpy.sh /path/to/UBTedugame run
     ```

## Usage

```sh
# Run the game
/path/to/renpy-sdk/renpy.sh . run

# Check the scripts for errors
/path/to/renpy-sdk/renpy.sh . lint

# Jump straight to a specific statement (useful when testing a scene)
/path/to/renpy-sdk/renpy.sh . run --warp game/script.rpy:100
```

Distributable builds for Windows, macOS, and Linux can be created from the Ren'Py Launcher via **Build Distributions**.

## Project Structure

```
UBTedugame/
└── game/
    ├── script.rpy           # Main story flow — the nine training scenes
    ├── ubt_mechanics.rpy    # Scoring system, game state, equipment/quiz data
    ├── ubt_screens.rpy      # Custom screens: HUD, drag-and-drop, slider, quiz, results
    ├── ubt_images.rpy       # Placeholder art (programmatic tiles, pending real assets)
    ├── options.rpy          # Ren'Py configuration (title, version, build settings)
    ├── screens.rpy          # Default Ren'Py UI screens
    ├── gui.rpy              # Default Ren'Py GUI theme
    ├── audio/               # Sound and music assets
    ├── images/              # Image assets
    └── tl/                  # Translations
```

The `ubt_*` files contain all project-specific code, keeping the stock Ren'Py files (`screens.rpy`, `gui.rpy`) untouched.

## Contributing

Contributions are welcome — particularly illustrated art assets to replace the placeholders in `ubt_images.rpy`, translations, and clinical-content review.

1. Fork the repository and create a feature branch.
2. Run `renpy.sh . lint` and play through the affected scenes before submitting.
3. Open a pull request with a clear description of the change.

## License

No license has been chosen yet. <!-- TODO: add a LICENSE file and update this section. -->
