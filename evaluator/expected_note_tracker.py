import time

class ExpectedNoteTracker:

    def __init__(self, exercise):
        self.notes = exercise["notes"]
        self.tempo = exercise["tempo"]
        self.start_time = time.time()

    def get_current(self):
        time_passed = time.time() - self.start_time
        beat_duration = 60 / self.tempo
        index = int(time_passed / beat_duration)
        if index >= len(self.notes):
            return None, None
        return self.notes[index], self.start_time + index * beat_duration