class SessionMetrics:

    def __init__(self):
        self.correct = 0
        self.total = 0

    def record(self, correct):
        self.total += 1
        if correct:
            self.correct += 1

    def accuracy(self):
        if self.total == 0:
            return 0
        return (self.correct / self.total) * 100