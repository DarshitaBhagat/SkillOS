import time


class ExpectedNoteTracker:

    def __init__(self, exercise):
        self.notes = exercise["notes"]
        self.tempo = exercise["tempo"]
        self.start_time = time.time()

    @property
    def beat_duration(self):
        return 60.0 / self.tempo

    def get_current_index(self):
        time_passed = time.time() - self.start_time
        return int(time_passed / self.beat_duration)

    def get_current(self):
        index = self.get_current_index()
        if index >= len(self.notes):
            return None, None
        expected_time = self.start_time + index * self.beat_duration
        return self.notes[index], expected_time

    def is_finished(self):
        return self.get_current_index() >= len(self.notes)

    def get_progress(self):
        idx = min(self.get_current_index(), len(self.notes))
        return idx, len(self.notes)
