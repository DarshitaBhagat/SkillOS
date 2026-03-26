import pygame
import time

class UI:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((800, 400))
        pygame.display.set_caption("SkillOS Guitar Coach")

        self.font = pygame.font.SysFont(None, 40)
        self.big_font = pygame.font.SysFont(None, 60)

    def draw(self, expected, detected, correct, timing, tempo):

        self.screen.fill((30, 30, 30))

        
        expected_text = self.font.render(f"Expected: {expected}", True, (255,255,255))
        detected_text = self.font.render(f"Detected: {detected}", True, (255,255,255))

        self.screen.blit(expected_text, (50, 80))
        self.screen.blit(detected_text, (50, 140))

        
        if correct:
            color = (0, 200, 0)
            message = "Correct"
        else:
            color = (200, 0, 0)
            message = "Wrong"

        feedback_text = self.big_font.render(message, True, color)
        self.screen.blit(feedback_text, (50, 220))

        
        timing_text = self.font.render(f"Timing: {timing}", True, (200,200,200))
        self.screen.blit(timing_text, (50, 300))

        
        beat_duration = 60 / tempo
        beat = int(time.time() / beat_duration) % 2

        if beat == 0:
            color = (200,200,200)
        else:
            color = (100,100,100)

        pygame.draw.circle(self.screen, color, (700, 200), 30)

        pygame.display.flip()

    def show_summary(self, accuracy):

        self.screen.fill((20,20,20))

        text = self.big_font.render(f"Accuracy: {accuracy:.1f}%", True, (255,255,255))
        self.screen.blit(text, (250, 180))

        pygame.display.flip()

    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        return True