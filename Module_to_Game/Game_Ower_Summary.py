import random
import pygame
import sys

from Configs import Configs


class GameSummaryScreen:
    def __init__(self):
        """Ініціалізує екран підсумків гри."""
        pygame.font.init()  # Ініціалізація модуля шрифтів
        self.set_window_size()
        self.set_fonts()
        self.is_active = False

        # Кольори
        self.background_color = (20, 20, 40)  # Глибокий синій колір
        self.text_color = (240, 240, 255)  # М'який білий колір
        self.accent_color = (100, 150, 255)  # М'який синій акцент

        # Анімація та частинки
        self.animation_progress = 0
        self.animation_speed = 0.02
        self.particles = []

        # Деталі результату гри
        self.winner = ""
        self.player1_score = 0
        self.player2_score = 0

    def set_window_size(self):
        """Встановлює розмір вікна на основі конфігурації."""
        self.window_size = {0: (720, 480), 1: (1280, 720), 2: (1920, 1080)}.get(Configs.resolution_index)
        if Configs.fullscreen == 1:
            self.window_size = (1280, 720)
            self.screen = pygame.display.set_mode(self.window_size, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)

    def set_fonts(self):
        """Встановлює шрифти для екрану підсумків."""
        coefficient = {0: 0.5, 1: 0.75, 2: 1.0}.get(Configs.resolution_index, 0.0)
        self.title_font = pygame.font.Font(None, int(120 * coefficient))
        self.score_font = pygame.font.Font(None, int(48 * coefficient))

    def activate(self, winner, player1_score, player2_score):
        """Активує екран підсумків з результатами гри."""
        self.is_active = True
        self.winner = winner
        self.player1_score = player1_score
        self.player2_score = player2_score
        self.animation_progress = 0
        self._generate_particles()
        self.run()

    def _generate_particles(self):
        """Генерує декоративні частинки для екрану підсумків."""
        self.particles = []
        for _ in range(100):
            x = random.randint(0, self.window_size[0])
            y = random.randint(0, self.window_size[1])
            speed = random.uniform(0.5, 2)
            size = random.uniform(1, 3)
            color = list(self.accent_color)
            color[0] += random.randint(-30, 30)
            color[1] += random.randint(-30, 30)
            color[2] += random.randint(-30, 30)
            color = tuple(max(0, min(255, c)) for c in color)
            self.particles.append({
                'pos': [x, y],
                'speed': speed,
                'size': size,
                'color': color,
                'alpha': random.randint(50, 200)
            })

    def handle_events(self):
        """Обробляє події, специфічні для екрану підсумків."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Будь-яке натискання клавіші або клік миші виходить з екрану
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                self.is_active = False

    def draw(self, screen):
        """Малює екран підсумків гри."""
        self.animation_progress = min(1, self.animation_progress + self.animation_speed)
        screen.fill(self.background_color)

        # Малює частинки
        for particle in self.particles:
            particle['pos'][1] += particle['speed']
            if particle['pos'][1] > self.window_size[1]:
                particle['pos'][1] = 0
            pygame.draw.circle(screen, particle['color'], particle['pos'], particle['size'])

        # Малює текст переможця
        winner_text = self.title_font.render(f"Переможець: {self.winner}", True, self.text_color)
        winner_rect = winner_text.get_rect(center=(self.window_size[0] // 2, self.window_size[1] // 4))
        screen.blit(winner_text, winner_rect)

        # Малює рахунки
        player1_text = self.score_font.render(f"Гравець 1: {self.player1_score}", True, self.text_color)
        player1_rect = player1_text.get_rect(center=(self.window_size[0] // 2, self.window_size[1] // 2))
        screen.blit(player1_text, player1_rect)

        player2_text = self.score_font.render(f"Гравець 2: {self.player2_score}", True, self.text_color)
        player2_rect = player2_text.get_rect(center=(self.window_size[0] // 2, self.window_size[1] // 2 + 50))
        screen.blit(player2_text, player2_rect)

        pygame.display.flip()

    def run(self):
        """Запускає цикл екрану підсумків."""
        clock = pygame.time.Clock()
        while self.is_active:
            self.handle_events()
            self.draw(self.screen)
            clock.tick(60)