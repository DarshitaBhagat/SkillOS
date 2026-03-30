import pygame
import time


class UI:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("SkillOS Guitar Coach")

        self.font =pygame.font.Font("assets/fonts/Poppins-Regular.ttf", 30) 
        self.big_font = pygame.font.Font("assets/fonts/Montserrat-Regular.ttf", 50)
        self.small_font = pygame.font.Font("assets/fonts/Orbitron-Regular.ttf", 40)


    def show_exercise_menu(self, exercise_list):

        selected = None
        item_height = 52
        padding_top = 80

        while selected is None:
            self.screen.fill((18, 18, 28))

            title = self.small_font.render("Choose an Exercise", True, (220, 220, 255))
            self.screen.blit(title, (800 // 2 - title.get_width() // 2, 20))

            mouse_pos = pygame.mouse.get_pos()

            for i, (name, path) in enumerate(exercise_list):
                y = padding_top + i * item_height
                rect = pygame.Rect(100, y, 600, item_height - 6)

                if rect.collidepoint(mouse_pos):
                    pygame.draw.rect(self.screen, (60, 80, 140), rect, border_radius=8)
                else:
                    pygame.draw.rect(self.screen, (40, 40, 60), rect, border_radius=8)

                label = self.font.render(name, True, (240, 240, 240))
                self.screen.blit(label, (rect.x + 16, rect.y + 10))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, (name, path) in enumerate(exercise_list):
                        y = padding_top + i * item_height
                        rect = pygame.Rect(100, y, 600, item_height - 6)
                        if rect.collidepoint(event.pos):
                            selected = path

        return selected


    def show_countdown(self):

        steps = ["3", "2", "1", "Go!"]

        for step in steps:
            start = time.time()
            while time.time() - start < 1.0:
                self.screen.fill((15, 15, 25))

                color = (100, 220, 100) if step == "Go!" else (240, 240, 100)
                text = self.big_font.render(step, True, color)

                big = pygame.font.Font("assets/fonts/Orbitron-Regular.ttf", 40)
                rendered = big.render(step, True, color)
                x = 800 // 2 - rendered.get_width() // 2
                y = 400 // 2 - rendered.get_height() // 2
                self.screen.blit(rendered, (x, y))

                hint = self.small_font.render("Get ready...", True, (150, 150, 150))
                self.screen.blit(hint, (800 // 2 - hint.get_width() // 2, 340))

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        raise SystemExit

                time.sleep(0.05)


    def draw(self, expected, detected, correct, timing, tempo):

        self.screen.fill((18, 18, 28))

        expected_text = self.font.render(f"Expected: {expected}", True, (255, 255, 255))
        detected_text = self.font.render(f"Detected: {detected}", True, (255, 255, 255))

        self.screen.blit(expected_text, (50, 80))
        self.screen.blit(detected_text, (50, 140))

        if correct:
            color = (0, 200, 0)
            message = "Correct"
        else:
            color = (200, 0, 0)
            message = "Wrong"

        feedback_text = self.small_font.render(message, True, color)
        self.screen.blit(feedback_text, (50, 220))

        timing_text = self.font.render(f"Timing: {timing}", True, (200, 200, 200))
        self.screen.blit(timing_text, (50, 300))

        beat_duration = 60 / tempo
        beat = int(time.time() / beat_duration) % 2

        dot_color = (200, 200, 200) if beat == 0 else (100, 100, 100)
        pygame.draw.circle(self.screen, dot_color, (700, 200), 30)

        pygame.display.flip()


    def show_summary(self, accuracy):

        self.screen.fill((20, 20, 20))

        text = self.small_font.render(f"Accuracy: {accuracy:.1f}%", True, (255, 255, 255))
        self.screen.blit(text, (250, 180))

        pygame.display.flip()


    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        return True
