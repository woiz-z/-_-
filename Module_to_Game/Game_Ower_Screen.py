import random
import pygame
import sys
from Menus.Main_Menu import Menu

class GameOverScreen:
    def __init__(self):
        """
        Ініціалізує екран завершення гри.
        """
        self.menu = Menu("Кінець Гри")
        self.window_size = self.menu.WINDOW_SIZE
        self.score_font = self.menu.button_font
        self.title_font = self.menu.title_font
        self.is_active = False
        self.final_score = 0

        # Кольорова палітра
        self.background_color = (20, 20, 40)  # Темно-синій
        self.overlay_color = (0, 0, 0)  # Чорний
        self.text_color = (240, 240, 255)  # М'який білий
        self.accent_color = (100, 150, 255)  # М'який синій акцент

        # Властивості анімації та переходу
        self.animation_progress = 0
        self.animation_speed = 0.02
        self.particles = []

    def activate(self, final_score):
        """
        Активує екран завершення гри з фінальним рахунком.

        Параметри:
        ----------
        final_score : int
            Фінальний рахунок гравця.
        """
        self.is_active = True
        self.final_score = final_score
        self.animation_progress = 0
        self._generate_particles()
        self.run()

    def _generate_particles(self):
        """
        Генерує декоративні частинки для екрану завершення гри.
        """
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
        """
        Обробляє події, специфічні для екрану завершення гри.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                self.is_active = False

    def draw(self, screen):
        """
        Малює екран завершення гри.

        Параметри:
        ----------
        screen : pygame.Surface
            Поверхня, на якій малюється екран.
        """
        self.animation_progress = min(1, self.animation_progress + self.animation_speed)

        background_surface = pygame.Surface(self.window_size)
        for y in range(self.window_size[1]):
            r = int(self.background_color[0] * (1 - y / self.window_size[1]))
            g = int(self.background_color[1] * (1 - y / self.window_size[1]))
            b = int(self.background_color[2] * (1 - y / self.window_size[1]))
            pygame.draw.line(background_surface, (r, g, b), (0, y), (self.window_size[0], y))
        screen.blit(background_surface, (0, 0))

        for particle in self.particles:
            particle['pos'][1] += particle['speed']
            if particle['pos'][1] > self.window_size[1]:
                particle['pos'][1] = 0

            particle_surf = pygame.Surface((particle['size'], particle['size']), pygame.SRCALPHA)
            particle_color = list(particle['color'])
            particle_color.append(int(particle['alpha'] * self.animation_progress))
            particle_surf.fill(particle_color)

            screen.blit(particle_surf, particle['pos'])

        title_text = "Час вийшов!"
        title_surface = self.title_font.render(title_text, True, self.text_color)
        title_rect = title_surface.get_rect(center=(self.window_size[0] // 2, self.window_size[1] // 2 - 150))
        screen.blit(title_surface, title_rect)

        score_text = f"Ваш рахунок: {self.final_score}"
        score_surface = self.score_font.render(score_text, True, self.text_color)
        score_surface.set_alpha(int(255 * self.animation_progress))
        score_rect = score_surface.get_rect(centerx=self.window_size[0] // 2, centery=self.window_size[1] // 2)
        screen.blit(score_surface, score_rect)

    def run(self):
        """
        Запускає екран завершення гри у новому вікні.
        """
        pygame.init()
        screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Game Over")

        while self.is_active:
            self.handle_events()
            self.draw(screen)
            pygame.display.flip()