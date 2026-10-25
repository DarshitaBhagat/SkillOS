import time
import json
import os
import glob
import pygame

from audio.audio_engine import AudioEngine
from evaluator.expected_note_tracker import ExpectedNoteTracker
from evaluator.correctness_evaluator import Evaluator
from evaluator.metrics import SessionMetrics
from evaluator.event import Event
from evaluator.timing import timing_error
from storage.db import Database
from ui.interface import UI


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXERCISES_DIR = os.path.join(BASE_DIR, "exercises")


def load_exercise_list():
    paths = sorted(glob.glob(os.path.join(EXERCISES_DIR, "*.json")))
    exercises = []
    for path in paths:
        with open(path) as f:
            data = json.load(f)
        exercises.append((data.get("name", os.path.basename(path)), path))
    return exercises


def main():
    audio = AudioEngine()
    db = Database()
    ui = UI()

    # 4-second bouncing 6-7 meme intro splash
    ui.show_intro_splash(duration=4.0)

    exercise_list = load_exercise_list()
    if not exercise_list:
        print("No exercises found in exercises/ folder.")
        return

    chosen_path = ui.show_exercise_menu(exercise_list)
    with open(chosen_path) as f:
        exercise = json.load(f)

    ui.show_countdown()

    tracker = ExpectedNoteTracker(exercise)
    evaluator = Evaluator()
    metrics = SessionMetrics()

    session_id = db.start_session()
    audio.start()

    print(f"Starting practice: {exercise.get('name', 'Exercise')}")

    clock = pygame.time.Clock()
    running = True

    last_evaluated_beat = -1
    current_feedback = {
        "expected": None,
        "detected": None,
        "correct": None,
        "timing": None,
    }

    try:
        while running:
            running = ui.handle_events()
            if not running:
                break

            # Finish session when all notes in the exercise have passed
            if tracker.is_finished():
                break

            expected, expected_time = tracker.get_current()
            current_beat_idx = tracker.get_current_index()

            detected = audio.process_pitch()

            if detected and expected:
                # Debounce per beat: score a note only once per beat duration
                if current_beat_idx != last_evaluated_beat:
                    last_evaluated_beat = current_beat_idx
                    actual_time = time.time()
                    correct_note = evaluator.evaluate(expected, detected)
                    timing = timing_error(expected_time, actual_time)

                    metrics.record(correct_note)
                    db.insert_event(
                        session_id,
                        expected,
                        detected,
                        actual_time,
                        timing,
                        correct_note
                    )

                    current_feedback["expected"] = expected
                    current_feedback["detected"] = detected
                    current_feedback["correct"] = correct_note
                    current_feedback["timing"] = timing
                else:
                    # Update live detected note during the same beat without duplicate scoring
                    current_feedback["detected"] = detected
            else:
                if expected:
                    current_feedback["expected"] = expected
                if not detected:
                    current_feedback["detected"] = None

            progress = tracker.get_progress()
            ui.draw(
                expected=current_feedback["expected"] or expected,
                detected=current_feedback["detected"],
                correct=current_feedback["correct"],
                timing=current_feedback["timing"],
                tempo=tracker.tempo,
                progress=(min(progress[0] + 1, progress[1]), progress[1]),
                exercise_notes=tracker.notes,
                current_index=current_beat_idx
            )

            clock.tick(60)

    except KeyboardInterrupt:
        pass

    accuracy = metrics.accuracy()
    print(f"\nSession ended. Final Accuracy: {accuracy:.2f}%")

    db.end_session(session_id, accuracy)
    audio.stop()

    if running:
        ui.show_summary(accuracy)

    pygame.quit()


if __name__ == "__main__":
    main()
