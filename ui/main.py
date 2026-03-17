import time
import json

from audio.audio_engine import AudioEngine
from evaluator.expected_note_tracker import ExpectedNoteTracker
from evaluator.correctness_evaluator import Evaluator
from evaluator.metrics import SessionMetrics
from evaluator.event import Event
from evaluator.timing import timing_error


# load exercise
with open("../exercises/e_major_scale.json") as f:
    exercise = json.load(f)


audio = AudioEngine()
tracker = ExpectedNoteTracker(exercise)
evaluator = Evaluator()
metrics = SessionMetrics()

audio.start()

print("Starting practice...")


last_note = None

try:

    while True:

        detected = audio.get_detected_note()
        expected = tracker.get_expected_note()
        expected_time = tracker.get_expected_time()

        if detected and expected:

            if detected != last_note:

                event = Event(detected, time.time())

                correct_note = evaluator.evaluate(expected, event)

                timing = timing_error(expected_time, event.timestamp)

                metrics.record(correct_note)

                print(
                    f"Expected: {expected} | "
                    f"Detected: {event.note} | "
                    f"Timing: {timing} | "
                    f"Correct Note: {correct_note}"
                )

                last_note = detected
        time.sleep(0.05)

except KeyboardInterrupt:

    print("\nSession ended")
    print(f"Accuracy: {metrics.accuracy():.2f}%")

    audio.stop()