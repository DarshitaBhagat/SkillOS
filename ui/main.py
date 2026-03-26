import time
import json

from audio.audio_engine import AudioEngine
from evaluator.expected_note_tracker import ExpectedNoteTracker
from evaluator.correctness_evaluator import Evaluator
from evaluator.metrics import SessionMetrics
from evaluator.event import Event
from evaluator.timing import timing_error
from storage.db import Database
from ui.ui import UI


import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

exercise_path = os.path.join(BASE_DIR, "exercises", "e_major.json")

with open(exercise_path) as f:
    exercise = json.load(f)


audio = AudioEngine()
tracker = ExpectedNoteTracker(exercise)
evaluator = Evaluator()
metrics = SessionMetrics()
db = Database()
ui = UI()

session_id = db.start_session()

audio.start()

print("Starting practice...")


last_note = None

PROCESS_INTERVAL = 0.2
last_process_time = 0

running = True

try:

    while running:

        # handle window close
        running = ui.handle_events()

        current_time = time.time()

        if current_time - last_process_time < PROCESS_INTERVAL:
            time.sleep(0.01)
            continue

        last_process_time = current_time

        detected = audio.get_detected_note()
        expected = tracker.get_expected_note()
        expected_time = tracker.get_expected_time()

        if detected and expected:

            if detected != last_note:

                event = Event(detected, time.time())

                correct_note = evaluator.evaluate(expected, event.note)
                timing = timing_error(expected_time, event.timestamp)

                metrics.record(correct_note)

                

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