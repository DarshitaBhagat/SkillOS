import pygame
import time
import os
import math
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class UI:

    def __init__(self):
        pygame.init()

        self.width = 1000
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("SkillOS Guitar Coach")

        # Fonts cached once during initialization
        font_dir = os.path.join(BASE_DIR, "assets", "fonts")
        poppins_path = os.path.join(font_dir, "Poppins-Regular.ttf")
        montserrat_path = os.path.join(font_dir, "Montserrat-Regular.ttf")
        orbitron_path = os.path.join(font_dir, "Orbitron-Regular.ttf")

        self.font = pygame.font.Font(poppins_path, 26)
        self.title_font = pygame.font.Font(poppins_path, 34)
        self.big_font = pygame.font.Font(montserrat_path, 50)
        self.note_font = pygame.font.Font(montserrat_path, 64)
        self.ribbon_note_font = pygame.font.Font(montserrat_path, 32)
        self.small_font = pygame.font.Font(orbitron_path, 28)
        self.status_font = pygame.font.Font(orbitron_path, 20)
        self.badge_font = pygame.font.Font(poppins_path, 16)

    def show_intro_splash(self, duration=4.0):
        clock = pygame.time.Clock()
        start_time = time.time()

        splash_font = pygame.font.Font(os.path.join(BASE_DIR, "assets", "fonts", "Montserrat-Regular.ttf"), 130)
        subtitle_font = self.status_font
        hint_font = self.badge_font

        # Helper to pre-render multi-layer neon glow surfaces
        def create_glow_digit(text, font, text_color, glow_color, radius=6):
            base = font.render(text, True, text_color)
            bw, bh = base.get_size()
            pad = radius * 3
            surf = pygame.Surface((bw + pad * 2, bh + pad * 2), pygame.SRCALPHA)
            for r in range(radius, 0, -2):
                alpha = int(140 / (r * 1.2))
                g_surf = font.render(text, True, (*glow_color[:3], alpha))
                for dx, dy in [(-r, 0), (r, 0), (0, -r), (0, r), (-r, -r), (r, r), (-r, r), (r, -r)]:
                    surf.blit(g_surf, (pad + dx, pad + dy))
            surf.blit(base, (pad, pad))
            return surf

        surf_6 = create_glow_digit("6", splash_font, (255, 255, 255), (70, 160, 255))
        surf_7 = create_glow_digit("7", splash_font, (255, 255, 255), (255, 100, 160))

        base_w6, base_h6 = surf_6.get_size()
        base_w7, base_h7 = surf_7.get_size()

        particles = []
        fade_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        running = True
        while running:
            elapsed = time.time() - start_time
            if elapsed >= duration:
                break

            # Allow instant skip via SPACE, ESCAPE, ENTER, or mouse click
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    running = False
                    break

            if not running:
                break

            # Deep dark background
            self.screen.fill((12, 14, 22))

            # Background animated audio equalizer grid
            num_bars = 48
            for bi in range(num_bars):
                bx = 40 + bi * 19
                wave_val = math.sin(elapsed * 6.0 + bi * 0.25) * 0.5 + 0.5
                bar_h = int(15 + wave_val * 45)
                bar_color = (25 + int(wave_val * 20), 30 + int(wave_val * 25), 45 + int(wave_val * 35))
                pygame.draw.rect(self.screen, bar_color, (bx, 380 - bar_h // 2, 10, bar_h), border_radius=3)

            # Harmonic alternating bouncing kinematics
            bounce_freq = 2.4
            bounce_amp = 50.0
            center_y = 225
            center_x = self.width // 2

            # "6" bounces with organic squash & stretch
            p6 = math.sin(elapsed * math.pi * bounce_freq)
            vel6 = math.cos(elapsed * math.pi * bounce_freq)
            y6 = center_y + p6 * bounce_amp
            sy6 = 1.0 + 0.12 * abs(vel6) - 0.16 * max(0.0, -p6)
            sx6 = 1.0 / math.sqrt(max(0.2, sy6))

            # "7" bounces opposite (pi phase offset)
            p7 = math.sin(elapsed * math.pi * bounce_freq + math.pi)
            vel7 = math.cos(elapsed * math.pi * bounce_freq + math.pi)
            y7 = center_y + p7 * bounce_amp
            sy7 = 1.0 + 0.12 * abs(vel7) - 0.16 * max(0.0, -p7)
            sx7 = 1.0 / math.sqrt(max(0.2, sy7))

            # Positions for "6" and "7" bouncing side-by-side
            spacing = 68
            x6 = center_x - spacing
            x7 = center_x + spacing

            # Spawn dynamic particle sparks
            if random.random() < 0.8:
                particles.append([
                    x6 + random.uniform(-20, 20),
                    y6 + base_h6 * 0.35 + random.uniform(-10, 10),
                    random.uniform(-1.5, 1.5),
                    random.uniform(-2.0, 1.0),
                    255,
                    (80, 180, 255)
                ])
                particles.append([
                    x7 + random.uniform(-20, 20),
                    y7 + base_h7 * 0.35 + random.uniform(-10, 10),
                    random.uniform(-1.5, 1.5),
                    random.uniform(-2.0, 1.0),
                    255,
                    (255, 100, 170)
                ])

            # Update & render particle sparks
            for p in particles[:]:
                p[0] += p[2]
                p[1] += p[3]
                p[4] -= 9
                if p[4] <= 0:
                    particles.remove(p)
                else:
                    p_alpha = max(0, min(255, int(p[4])))
                    radius = max(1, int(p_alpha / 65))
                    p_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                    pygame.draw.circle(p_surf, (*p[5], p_alpha), (radius, radius), radius)
                    self.screen.blit(p_surf, (int(p[0] - radius), int(p[1] - radius)))

            # Render "6" with squash & stretch scaling
            w6 = max(10, int(base_w6 * sx6))
            h6 = max(10, int(base_h6 * sy6))
            scaled_6 = pygame.transform.smoothscale(surf_6, (w6, h6))
            self.screen.blit(scaled_6, (int(x6 - w6 // 2), int(y6 - h6 // 2)))

            # Render "7" with squash & stretch scaling
            w7 = max(10, int(base_w7 * sx7))
            h7 = max(10, int(base_h7 * sy7))
            scaled_7 = pygame.transform.smoothscale(surf_7, (w7, h7))
            self.screen.blit(scaled_7, (int(x7 - w7 // 2), int(y7 - h7 // 2)))

            # Subtitle: Centered "SKILLOS"
            sub_title = subtitle_font.render("SKILLOS", True, (180, 200, 240))
            self.screen.blit(sub_title, (center_x - sub_title.get_width() // 2, 450))

            # Progress / loading bar
            bar_w = 420
            bar_h = 6
            bar_x = center_x - bar_w // 2
            bar_y = 495
            pygame.draw.rect(self.screen, (30, 34, 52), (bar_x, bar_y, bar_w, bar_h), border_radius=3)

            progress = min(1.0, elapsed / duration)
            fill_w = int(bar_w * progress)
            if fill_w > 0:
                pygame.draw.rect(self.screen, (100, 200, 255), (bar_x, bar_y, fill_w, bar_h), border_radius=3)

            # Skip hint
            skip_text = hint_font.render("Press SPACE or click to skip", True, (110, 120, 145))
            self.screen.blit(skip_text, (center_x - skip_text.get_width() // 2, 530))

            # Cinematic Fade-in (0 to 0.4s) & Fade-out (3.4s to 4.0s)
            if elapsed < 0.4:
                fade_alpha = int(255 * (1.0 - elapsed / 0.4))
                fade_surface.fill((12, 14, 22, max(0, min(255, fade_alpha))))
                self.screen.blit(fade_surface, (0, 0))
            elif elapsed > (duration - 0.6):
                fade_alpha = int(255 * ((elapsed - (duration - 0.6)) / 0.6))
                fade_surface.fill((12, 14, 22, max(0, min(255, fade_alpha))))
                self.screen.blit(fade_surface, (0, 0))

            pygame.display.flip()
            clock.tick(60)

    def show_exercise_menu(self, exercise_list):
        selected = None
        item_height = 54
        padding_top = 90
        box_width = 640
        scroll_y = 0.0

        clock = pygame.time.Clock()
        total_content_height = padding_top + len(exercise_list) * item_height + 25
        visible_height = self.height
        max_scroll = max(0.0, float(total_content_height - visible_height))

        # Viewport for scrolling list (underneath the header bar)
        viewport_rect = pygame.Rect(0, padding_top - 5, self.width, self.height - padding_top + 5)

        scrollbar_width = 10
        scrollbar_x = self.width // 2 + box_width // 2 + 18
        track_y = padding_top
        track_height = self.height - padding_top - 20

        dragging_scrollbar = False
        drag_start_y = 0
        drag_start_scroll = 0.0

        while selected is None:
            self.screen.fill((18, 18, 28))
            mouse_pos = pygame.mouse.get_pos()
            box_x = self.width // 2 - box_width // 2

            # 1. Render scrollable content with clipping
            self.screen.set_clip(viewport_rect)
            for i, (name, path) in enumerate(exercise_list):
                y = padding_top + i * item_height - int(scroll_y)
                rect = pygame.Rect(box_x, y, box_width, item_height - 8)

                # Only draw items in or near the visible window
                if rect.bottom >= padding_top - 10 and rect.top <= self.height + 10:
                    is_hovered = rect.collidepoint(mouse_pos) and viewport_rect.collidepoint(mouse_pos)
                    if is_hovered:
                        pygame.draw.rect(self.screen, (60, 90, 160), rect, border_radius=8)
                        pygame.draw.rect(self.screen, (100, 140, 230), rect, width=2, border_radius=8)
                    else:
                        pygame.draw.rect(self.screen, (35, 38, 55), rect, border_radius=8)

                    label = self.font.render(name, True, (240, 240, 245))
                    self.screen.blit(label, (rect.x + 20, rect.y + 10))

            self.screen.set_clip(None)

            # 2. Render fixed header with dark background so scrolled cards pass behind
            header_rect = pygame.Rect(0, 0, self.width, padding_top - 6)
            pygame.draw.rect(self.screen, (18, 18, 28), header_rect)
            pygame.draw.line(self.screen, (35, 40, 60), (0, padding_top - 6), (self.width, padding_top - 6), 2)

            title = self.title_font.render("Choose an Exercise", True, (220, 225, 255))
            self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 20))

            if max_scroll > 0:
                hint_str = "Scroll with mouse wheel or arrow keys"
                hint_text = self.badge_font.render(hint_str, True, (130, 140, 170))
                self.screen.blit(hint_text, (self.width // 2 - hint_text.get_width() // 2, 60))

            # 3. Render vertical scrollbar if list exceeds visible height
            if max_scroll > 0:
                # Track
                track_rect = pygame.Rect(scrollbar_x, track_y, scrollbar_width, track_height)
                pygame.draw.rect(self.screen, (28, 30, 44), track_rect, border_radius=5)

                # Thumb
                thumb_height = max(36, int(track_height * (visible_height / total_content_height)))
                thumb_y = track_y + int((track_height - thumb_height) * (scroll_y / max_scroll))
                thumb_rect = pygame.Rect(scrollbar_x, thumb_y, scrollbar_width, thumb_height)

                is_thumb_hovered = thumb_rect.collidepoint(mouse_pos) or dragging_scrollbar
                thumb_color = (110, 140, 200) if is_thumb_hovered else (70, 85, 125)
                pygame.draw.rect(self.screen, thumb_color, thumb_rect, border_radius=5)

            pygame.display.flip()

            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

                # Mouse Wheel Scrolling
                elif event.type == pygame.MOUSEWHEEL:
                    scroll_y -= event.y * 36

                # Keyboard Arrow Scrolling
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_DOWN, pygame.K_j):
                        scroll_y += item_height
                    elif event.key in (pygame.K_UP, pygame.K_k):
                        scroll_y -= item_height
                    elif event.key == pygame.K_PAGEDOWN:
                        scroll_y += item_height * 4
                    elif event.key == pygame.K_PAGEUP:
                        scroll_y -= item_height * 4

                # Mouse Drag & Click Handling
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if max_scroll > 0 and 'thumb_rect' in locals() and thumb_rect.collidepoint(event.pos):
                        dragging_scrollbar = True
                        drag_start_y = event.pos[1]
                        drag_start_scroll = scroll_y
                    else:
                        for i, (name, path) in enumerate(exercise_list):
                            y = padding_top + i * item_height - int(scroll_y)
                            rect = pygame.Rect(box_x, y, box_width, item_height - 8)
                            if rect.collidepoint(event.pos) and viewport_rect.collidepoint(event.pos):
                                selected = path

                # Legacy mouse wheel support (buttons 4 and 5)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button in (4, 5):
                    if event.button == 4:
                        scroll_y -= 36
                    elif event.button == 5:
                        scroll_y += 36

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    dragging_scrollbar = False

                elif event.type == pygame.MOUSEMOTION and dragging_scrollbar:
                    dy = event.pos[1] - drag_start_y
                    scroll_ratio = max_scroll / max(1, (track_height - thumb_height))
                    scroll_y = drag_start_scroll + dy * scroll_ratio

            # Clamp scroll bounds
            scroll_y = max(0.0, min(scroll_y, max_scroll))
            clock.tick(60)

        return selected

    def show_countdown(self):
        steps = ["3", "2", "1", "Go!"]
        clock = pygame.time.Clock()

        for step in steps:
            start = time.time()
            color = (100, 240, 120) if step == "Go!" else (255, 220, 90)
            rendered = self.big_font.render(step, True, color)
            hint = self.font.render("Get ready to play...", True, (160, 165, 180))

            while time.time() - start < 1.0:
                self.screen.fill((15, 15, 25))

                x = self.width // 2 - rendered.get_width() // 2
                y = self.height // 2 - rendered.get_height() // 2 - 20
                self.screen.blit(rendered, (x, y))

                hx = self.width // 2 - hint.get_width() // 2
                self.screen.blit(hint, (hx, self.height // 2 + 60))

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        raise SystemExit

                clock.tick(60)

    def draw(self, expected, detected, correct, timing, tempo, progress=None, exercise_notes=None, current_index=0):
        self.screen.fill((18, 18, 28))

        # Top Bar: Progress / Exercise Header
        if progress:
            curr_idx, total_notes = progress
            prog_text = self.status_font.render(f"Step {curr_idx} of {total_notes}", True, (160, 175, 210))
            self.screen.blit(prog_text, (50, 24))

        # Target Note Box (Left Column, Top)
        pygame.draw.rect(self.screen, (28, 32, 48), pygame.Rect(50, 60, 560, 110), border_radius=10)
        exp_label = self.font.render("Target Note:", True, (175, 185, 210))
        self.screen.blit(exp_label, (70, 72))
        exp_note_str = str(expected) if expected else "-"
        exp_note = self.note_font.render(exp_note_str, True, (255, 255, 255))
        self.screen.blit(exp_note, (70, 102))

        # Detected Note Box (Left Column, Middle)
        pygame.draw.rect(self.screen, (28, 32, 48), pygame.Rect(50, 185, 560, 110), border_radius=10)
        det_label = self.font.render("Detected:", True, (175, 185, 210))
        self.screen.blit(det_label, (70, 197))
        if detected:
            det_color = (100, 230, 140) if correct else ((240, 90, 90) if correct is False else (220, 220, 240))
            det_note = self.note_font.render(str(detected), True, det_color)
        else:
            det_note = self.font.render("Listening... (pluck string)", True, (120, 130, 150))
        self.screen.blit(det_note, (70, 228))

        # Evaluation & Timing Feedback Row
        if correct is True:
            feedback_str = "CORRECT"
            fb_color = (50, 220, 90)
        elif correct is False:
            feedback_str = "WRONG"
            fb_color = (240, 70, 70)
        else:
            feedback_str = "READY"
            fb_color = (130, 140, 170)

        feedback_text = self.small_font.render(feedback_str, True, fb_color)
        self.screen.blit(feedback_text, (50, 312))

        timing_str = f"Timing: {timing.capitalize() if timing else '-'}"
        timing_text = self.font.render(timing_str, True, (185, 195, 215))
        self.screen.blit(timing_text, (50, 360))

        # Metronome Box (Right Column)
        pygame.draw.rect(self.screen, (28, 32, 48), pygame.Rect(640, 60, 310, 345), border_radius=10)
        metro_label = self.font.render("Metronome", True, (175, 185, 210))
        self.screen.blit(metro_label, (640 + 155 - metro_label.get_width() // 2, 78))

        bpm_label = self.status_font.render(f"{tempo} BPM", True, (140, 150, 175))
        self.screen.blit(bpm_label, (640 + 155 - bpm_label.get_width() // 2, 120))

        # Pulsing beat circle
        beat_sec = 60.0 / tempo
        phase = (time.time() % beat_sec) / beat_sec
        intensity = int(max(60, 255 * (1.0 - phase * 1.5)))
        dot_color = (intensity, int(intensity * 0.9), min(255, int(intensity * 1.2)))
        radius = int(34 + 8 * (1.0 - phase))
        pygame.draw.circle(self.screen, dot_color, (795, 225), radius)

        pulse_label = self.font.render("PULSE", True, (100, 110, 130))
        self.screen.blit(pulse_label, (795 - pulse_label.get_width() // 2, 290))

        # -------------------------------------------------------------
        # Bottom Note Sequence Ribbon (Horizontal Scrolling Note Horizon)
        # -------------------------------------------------------------
        ribbon_rect = pygame.Rect(50, 425, 900, 150)
        pygame.draw.rect(self.screen, (24, 27, 40), ribbon_rect, border_radius=12)
        pygame.draw.rect(self.screen, (40, 46, 68), ribbon_rect, width=1, border_radius=12)

        ribbon_title = self.status_font.render("Exercise Notes Sequence:", True, (160, 175, 205))
        self.screen.blit(ribbon_title, (70, 437))

        if exercise_notes:
            notes_count_text = self.badge_font.render(f"Total: {len(exercise_notes)} notes", True, (130, 140, 165))
            self.screen.blit(notes_count_text, (70 + ribbon_title.get_width() + 15, 440))

            card_w = 64
            card_h = 72
            spacing = 14
            step = card_w + spacing
            visible_track_w = 850
            track_viewport = pygame.Rect(70, 465, visible_track_w, card_h + 10)

            # Auto-scroll so target note stays in central focus
            target_center_x = 70 + visible_track_w // 2 - card_w // 2
            total_track_width = len(exercise_notes) * step
            ideal_scroll = current_index * step - (visible_track_w // 2 - card_w // 2)
            scroll_x = max(0, min(ideal_scroll, max(0, total_track_width - visible_track_w)))

            self.screen.set_clip(track_viewport)
            for idx, n in enumerate(exercise_notes):
                card_x = 70 + idx * step - scroll_x
                card_y = 470
                card_rect = pygame.Rect(card_x, card_y, card_w, card_h)

                if card_rect.right < 60 or card_rect.left > 940:
                    continue

                if idx < current_index:
                    # Completed Note
                    pygame.draw.rect(self.screen, (28, 40, 36), card_rect, border_radius=8)
                    pygame.draw.rect(self.screen, (45, 75, 60), card_rect, width=1, border_radius=8)
                    n_text = self.ribbon_note_font.render(str(n), True, (130, 170, 145))
                    tag = self.badge_font.render("done", True, (80, 140, 100))
                    self.screen.blit(tag, (card_x + card_w // 2 - tag.get_width() // 2, card_y + 4))
                elif idx == current_index:
                    # Current Target Note (Enlarged & Glowing)
                    glow_rect = pygame.Rect(card_x - 3, card_y - 3, card_w + 6, card_h + 6)
                    pygame.draw.rect(self.screen, (40, 75, 130), glow_rect, border_radius=10)
                    pygame.draw.rect(self.screen, (75, 170, 255), glow_rect, width=2, border_radius=10)
                    n_text = self.ribbon_note_font.render(str(n), True, (255, 255, 255))
                    tag = self.badge_font.render("PLAY", True, (100, 220, 255))
                    self.screen.blit(tag, (card_x + card_w // 2 - tag.get_width() // 2, card_y + 4))
                else:
                    # Upcoming Note
                    pygame.draw.rect(self.screen, (34, 38, 56), card_rect, border_radius=8)
                    pygame.draw.rect(self.screen, (48, 54, 80), card_rect, width=1, border_radius=8)
                    n_text = self.ribbon_note_font.render(str(n), True, (200, 210, 230))
                    idx_label = self.badge_font.render(f"#{idx+1}", True, (110, 120, 145))
                    self.screen.blit(idx_label, (card_x + card_w // 2 - idx_label.get_width() // 2, card_y + 4))

                self.screen.blit(n_text, (card_x + card_w // 2 - n_text.get_width() // 2, card_y + 26))

            self.screen.set_clip(None)

        pygame.display.flip()

    def show_summary(self, accuracy):
        clock = pygame.time.Clock()
        waiting = True

        while waiting:
            self.screen.fill((16, 18, 26))

            title = self.big_font.render("Practice Complete!", True, (120, 230, 160))
            self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 140))

            acc_color = (100, 240, 130) if accuracy >= 70 else (240, 200, 80) if accuracy >= 50 else (240, 90, 90)
            acc_text = self.big_font.render(f"Final Accuracy: {accuracy:.1f}%", True, acc_color)
            self.screen.blit(acc_text, (self.width // 2 - acc_text.get_width() // 2, 230))

            hint = self.font.render("Press ANY KEY or CLICK to exit", True, (170, 175, 195))
            self.screen.blit(hint, (self.width // 2 - hint.get_width() // 2, 350))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type in (pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    waiting = False

            clock.tick(30)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
