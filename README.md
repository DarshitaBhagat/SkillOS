# SkillOS

**Learning new skills is difficult — but it doesn't have to be tedious.**

What makes practice frustrating isn't the difficulty. It's not knowing *how* to learn, *what* to practice, or *whether you're actually improving*. Most people practice in a vacuum: no feedback, no structure, no signal.

SkillOS is a learning platform and infrastructure layer that fixes that. It observes how you perform a skill, analyzes your mistakes and patterns, adapts difficulty and pacing accordingly, and gives you a session summary with actionable feedback after every practice.

It's not a replacement for teachers or coaches. It's what makes the time *between* sessions count.

---

## The Problem

Existing skill-training tools are:
- **Expensive** — priced for institutions, not individuals
- **Cloud-dependent** — your practice data lives on someone else's server
- **Closed-source** — no transparency about how feedback is generated
- **Data-hungry** — collecting behavioral data without clear purpose

SkillOS is different: **privacy-first, fully offline, open-source, and free.**

No accounts. No telemetry. No data collection. Your practice stays on your device.

---

## What It Does

SkillOS captures raw human actions through sensors (microphone, keyboard, camera), converts them into structured learning signals, and runs them through an evaluation pipeline:

```
Sensor Input → Standardized Events → Evaluator → Feedback + Session Summary
                                                         ↓
                                                   Local Database
```

Each sensor emits standardized events. The event-driven architecture makes the system modular — you can plug in new sensors, new exercises, and new evaluators without touching the core.

After each session, SkillOS shows you:
- **Accuracy %** — how often you hit the right notes/keys/actions
- **Weakest zones** — where you're consistently making errors
- **Timing consistency** — how steady your rhythm is
- **Next practice suggestion** — what to work on in your next session

---

## Guitar Coach — Reference Implementation

Guitar Coach is the first complete implementation of the SkillOS framework. It listens to your guitar through a microphone and gives you real-time feedback on every note you play.

### Features

- **Real-time pitch detection** — detects the note you're playing as you play it
- **Note accuracy evaluation** — compares your note against the expected note (with enharmonic equivalents)
- **Timing validation** — checks whether you're hitting notes in time with the tempo
- **Live visual feedback** — green for correct, red for wrong, metronome pulse for beat
- **Exercise selection** — choose which scale or pattern to practice from a menu at launch
- **Countdown before start** — a 1 → 2 → 3 → Go! countdown gives you time to get ready
- **Session tracking** — every note event is logged to a local SQLite database
- **Session summary** — accuracy %, weakest zones, timing consistency, and a next-session suggestion
- **Completely offline** — no internet required, ever

---

## Project Structure

```
SkillOS/
├── assets/
│   └── fonts
│       ├── Monsterrat-Regular
│       ├── Orbitron-Regular
│       └── Poppins-Regular     
├── audio/
│   └── audio_engine.py            # Mic capture, pitch detection, note conversion
├── evaluator/
│   ├── correctness_evaluator.py   # Note matching with enharmonic handling
│   ├── event.py                   # Note event dataclass
│   ├── expected_note_tracker.py   # Tracks current expected note in sequence
│   ├── metrics.py                 # Accuracy calculation
│   └── timing.py                  # Timing error measurement
├── exercises/
│   ├── C_major.json
│   ├── D_major.json
│   ├── e_major.json
│   └── ...                        # Add your own exercise JSON files here
├── storage/
│   └── db.py                      # SQLite session and note event logging
├── ui/
│   ├── interface.py               # pygame window: menu, countdown, live feedback
│   └── main.py                    # Entry point
└── requirements.txt
```

---

## Getting Started

```

### Install

```bash
pip install -r requirements.txt
```

### Run

```bash
python -m ui.main
```

A window will open with a list of available exercises. Click one to select it. A 1 → 2 → 3 → Go! countdown plays, then practice begins.

---

## Exercises

Exercises are plain JSON files in the `exercises/` folder:

```json
{
    "name": "C Major Scale",
    "tempo": 80,
    "notes": ["C", "D", "E", "F", "G", "A", "B", "C"]
}
```

Add your own by dropping a new `.json` file in the same format into `exercises/`. It will appear in the menu automatically on next launch.

---

## Exercise Selection + Countdown (v0.2)

On launch, instead of jumping straight into a hardcoded exercise:

1. **Exercise picker** — all `.json` files from the `exercises/` folder are listed in a clickable menu. Rows highlight on hover.
2. **Countdown** — a full-screen 1 → 2 → 3 → **Go!** sequence (one second per step) plays before notes start.

Both are handled in `ui/interface.py` via `show_exercise_menu()` and `show_countdown()`.

---

## What You Can Build With SkillOS

The core framework is sensor-agnostic and domain-agnostic. Guitar Coach is one implementation. The same architecture supports:

| Domain | Implementation |
|---|---|
| Music | Guitar tutor, piano coach, ear training |
| Typing | Typing trainer with per-finger heatmaps |
| Speech | Pronunciation coach, language learning |
| Accessibility | Alternative input interfaces |
| Research | Audio ML datasets, human performance benchmarking |
| HCI | Gesture and movement recognition systems |

Any skill that can be observed through a sensor can be turned into structured feedback with SkillOS.

---

## Database

Sessions and events are stored in `skillos.db` (SQLite, auto-created on first run):

| Table | Contents |
|---|---|
| `sessions` | Start/end time, final accuracy per session |
| `note_events` | Expected note, detected note, timestamp, timing error, correct/wrong |

All data stays local. Nothing is sent anywhere.

---

## Future Plans

- **More exercises** — arpeggios, chord progressions, pentatonic patterns, full songs
- **Visual fretboard** — show expected vs. played position on a guitar neck diagram
- **Difficulty adaptation** — auto-adjust tempo based on recent accuracy trends
- **Progress dashboard** — accuracy and timing charts across sessions
- **MIDI support** — accept input from MIDI keyboards and controllers
- **Custom exercise builder** — in-app UI to build and save exercises without editing JSON
- **Speech coach module** — pronunciation and cadence feedback using the mic
- **Typing trainer module** — WPM, accuracy, and per-key weakness tracking
- **Camera sensor support** — posture, hand position, and movement analysis
- **Export session reports** — save session data as PDF or CSV
- **Plugin API** — formal interface for third-party sensors and evaluators

---

## License

GNU General Public License v3.0

SkillOS is free and open-source. Any modified version must also be released as open-source under the same terms. This ensures the platform stays transparent and community-owned — no one can take this codebase, add cloud telemetry, and ship it as a closed proprietary product.

See [LICENSE](LICENSE) for the full text.
