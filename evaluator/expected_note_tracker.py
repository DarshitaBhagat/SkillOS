import time

class ExpectedNoteTracker:

    def __init__(self, exercise):
        self.notes = exercise["notes"]
        self.tempo = exercise["tempo"]
        self.start_time = time.time()

    def get_expected_note(self):
        time_passed = time.time() - self.start_time
        beat_duration = 60 / self.tempo

        index = int(time_passed / beat_duration)

        if index < len(self.notes):
            return self.notes[index]

        return None