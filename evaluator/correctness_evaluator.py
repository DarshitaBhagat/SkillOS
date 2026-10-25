import re


class Evaluator:

    ENHARMONIC = {
        "Db": "C#",
        "Eb": "D#",
        "Gb": "F#",
        "Ab": "G#",
        "Bb": "A#",
    }

    def __init__(self):
        self.correct = 0
        self.total = 0

    @staticmethod
    def strip_octave(note_str):
        if not note_str:
            return ""
        return re.sub(r"\d+", "", str(note_str)).strip()

    def normalize(self, note, strip_octave=True):
        if note is None:
            return None

        n = str(note).strip()
        if strip_octave:
            n = self.strip_octave(n)

        # Standardize flats to sharps
        for flat, sharp in self.ENHARMONIC.items():
            n = n.replace(flat, sharp)

        if not n:
            return ""

        # Normalize casing (e.g. c# -> C#)
        if len(n) == 1:
            return n.upper()
        return n[0].upper() + n[1:]

    def evaluate(self, expected, detected, strict_octave=False):
        if expected is None or detected is None:
            return False

        self.total += 1

        # Only require strict octave if explicitly enabled and expected contains an octave digit
        has_octave = bool(re.search(r"\d", str(expected)))
        strip = not (strict_octave and has_octave)

        norm_expected = self.normalize(expected, strip_octave=strip)
        norm_detected = self.normalize(detected, strip_octave=strip)

        if norm_expected == norm_detected:
            self.correct += 1
            return True
        return False
