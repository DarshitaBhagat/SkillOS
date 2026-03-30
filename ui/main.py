import time
import json
import os
import glob

from audio.audio_engine import AudioEngine
from evaluator.expected_note_tracker import ExpectedNoteTracker
from evaluator.correctness_evaluator import Evaluator
from evaluator.metrics import SessionMetrics
from evaluator.event import Event
from evaluator.timing import timing_error
from storage.db import Database
from ui.interface import UI


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
EXERCISES_DIR = os.path.join(BASE_DIR, "exercises")


def load_exercise_list():

    paths = sorted(glob.glob(os.path.join(EXERCISES_DIR, "*.json")))
    exercises = []
    for path in paths:
        with open(path) as f:
            data = json.load(f)
        exercises.append((data.get("name", os.path.basename(path)), path))
    return exercises


audio = AudioEngine()
db = Database()
ui = UI()


exercise_list = load_exercise_list()
chosen_path = ui.show_exercise_menu(exercise_list)

with open(chosen_path) as f:
    exercise = json.load(f)


ui.show_countdown()


tracker = ExpectedNoteTracker(exercise)
evaluator = Evaluator()
metrics = SessionMetrics()

session_id = db.start_session()

audio.start()

print(f"Starting practice: {exercise['name']}")

PROCESS_INTERVAL = 0.3
last_process_time = 0
running = True

try:
    while running:
        running = ui.handle_events()

        current_time = time.time()

        if current_time - last_process_time < PROCESS_INTERVAL:
            time.sleep(0.01)
            continue

        last_process_time = current_time

        detected = audio.process_pitch()
        expected, expected_time = tracker.get_current()

        if detected and expected:
                
                event = Event(detected, time.time())

                correct_note = evaluator.evaluate(expected, event.note)
                timing = timing_error(expected_time, event.timestamp)

                metrics.record(correct_note)

                db.insert_event(
                    session_id,
                    expected,
                    event.note,
                    event.timestamp,
                    timing,
                    correct_note
                )

                ui.draw(
                    expected,
                    event.note,
                    correct_note,
                    timing,
                    tracker.tempo
                )

except KeyboardInterrupt:
    pass

accuracy = metrics.accuracy()

print("\nSession ended")
print(f"Accuracy: {accuracy:.2f}%")

db.end_session(session_id, accuracy)

ui.show_summary(accuracy)

time.sleep(3)

audio.stop()
