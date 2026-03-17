class Evaluator:

    def __init__(self):
        self.correct = 0
        self.total = 0

    def evaluate(self, expected, detected):

        self.total += 1

        if expected == detected:
            self.correct += 1
            return True

        return False