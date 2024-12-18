import pygame
import math
import random

class ResultDisplay:
    def __init__(self, window_size):
        """
        Ініціалізує об'єкт ResultDisplay.

        :param window_size: Розмір вікна (ширина, висота)
        """
        self.result = None
        self.result_display_timer = 0
        self.result_display_duration = 60  # 1 секунда при 60 FPS
        self.window_size = window_size

    def set_result(self, result):
        """
        Встановлює результат для відображення.

        :param result: Результат для відображення
        """
        self.result = result
        self.result_display_timer = 0

    def update(self):
        """
        Оновлює таймер відображення результату.
        """
        if self.result is not None:
            self.result_display_timer += 1
            if self.result_display_timer >= self.result_display_duration:
                self.result = None

    def draw(self, screen):
        """
        Малює результат на екрані.

        :param screen: Екран для малювання
        """
        if self.result is not None:
            result_text = f"{self.result:.2f}".rstrip('0').rstrip('.')
            current_time = pygame.time.get_ticks()
            pulse_factor = math.sin(current_time / 200) * 0.2 + 1
            base_font_size = int(self.window_size[0] * 0.3 * pulse_factor)
            large_font = pygame.font.Font(None, base_font_size)
            text_surface = large_font.render(result_text, True, (0, 0, 0))
            gradient_surface = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
            for y in range(text_surface.get_height()):
                r = int(0 + (y / text_surface.get_height()) * 50)
                g = int(100 + (y / text_surface.get_height()) * 155)
                b = int(200 + (y / text_surface.get_height()) * 55)
                pygame.draw.line(gradient_surface, (r, g, b), (0, y), (text_surface.get_width(), y))
            text_surface.blit(gradient_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            shadow_offset = int(base_font_size * 0.05)
            shadow_surface = large_font.render(result_text, True, (50, 50, 50))
            text_width, text_height = text_surface.get_size()
            x = (self.window_size[0] - text_width) // 2
            y = (self.window_size[1] - text_height) // 2
            glow_surfaces = [
                pygame.transform.scale(text_surface, (int(text_width * (1 + i * 0.1)), int(text_height * (1 + i * 0.1))))
                for i in range(5)
            ]
            for i, glow_surface in enumerate(glow_surfaces):
                glow_surface.set_alpha(50 - i * 10)
                glow_x = x - (glow_surface.get_width() - text_width) // 2
                glow_y = y - (glow_surface.get_height() - text_height) // 2
                screen.blit(shadow_surface, (x + shadow_offset, y + shadow_offset))
                screen.blit(glow_surface, (glow_x, glow_y))
            screen.blit(text_surface, (x, y))
            self._draw_floating_particles(screen, x, y, text_width, text_height)

    def _draw_floating_particles(self, screen, x, y, width, height):
        """
        Малює плаваючі частинки навколо тексту.

        :param screen: Екран для малювання
        :param x: Координата X тексту
        :param y: Координата Y тексту
        :param width: Ширина тексту
        :param height: Висота тексту
        """
        current_time = pygame.time.get_ticks()
        for i in range(20):
            particle_x = x + width // 2 + math.sin(current_time / 500 + i) * width * 0.8
            particle_y = y + height // 2 + math.cos(current_time / 500 + i) * height * 0.8
            size = random.randint(2, 5)
            r = int(100 + math.sin(current_time / 200 + i) * 50)
            g = int(150 + math.cos(current_time / 200 + i) * 50)
            b = int(200 + math.sin(current_time / 300 + i) * 55)
            particle_surface = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, (r, g, b, 150), (size // 2, size // 2), size // 2)
            screen.blit(particle_surface, (particle_x, particle_y))