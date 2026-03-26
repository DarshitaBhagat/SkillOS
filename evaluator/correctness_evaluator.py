class Evaluator:

    def __init__(self):
        self.correct = 0
        self.total = 0

    ENHARMONIC = {"C#": "Db", "D#": "Eb", "F#": "Gb", "G#": "Ab", "A#": "Bb"}

    def normalize(self, note):
        if note is None:
            return None
        for sharp, flat in self.ENHARMONIC.items():
            note = note.replace(flat, sharp)
        return note

    def evaluate(self, expected, detected):
        self.total += 1
        if self.normalize(expected) == self.normalize(detected):
            self.correct += 1
            return True
        return False