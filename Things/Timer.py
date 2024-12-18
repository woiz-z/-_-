import math
import pygame

class Timer:
    def __init__(self, x, y, width, height, duration, font):
        """
        Ініціалізує об'єкт таймера.

        :param x: Координата X центру таймера
        :param y: Координата Y центру таймера
        :param width: Ширина таймера
        :param height: Висота таймера
        :param duration: Загальна тривалість таймера в секундах
        :param font: Шрифт для відображення часу
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.total_duration = duration
        self.remaining_time = duration
        self.font = font
        self.last_update = pygame.time.get_ticks()
        self.is_running = False

        # Елементи дизайну таймера
        self.outer_color = (0, 0, 0)  # Темно-сірий зовнішній круг
        self.inner_color = (220, 220, 220)  # Світло-сірий внутрішній фон
        self.text_color = (0, 0, 0)  # Чорний текст
        self.warning_color = (255, 0, 0)  # Червоний колір при низькому часі

    def start(self):
        """Запускає таймер."""
        self.is_running = True
        self.last_update = pygame.time.get_ticks()

    def pause(self):
        """Призупиняє таймер."""
        self.is_running = False

    def reset(self):
        """Скидає таймер до початкового значення."""
        self.remaining_time = self.total_duration
        self.is_running = False

    def update(self):
        """
        Оновлює залишковий час таймера.

        :return: Повертає True, якщо час вийшов, інакше False
        """
        if self.is_running:
            current_time = pygame.time.get_ticks()
            self.remaining_time -= (current_time - self.last_update) / 1000
            self.last_update = current_time

            if self.remaining_time <= 0:
                self.remaining_time = 0
                self.is_running = False
                return True
        return False

    def draw(self, screen):
        """
        Малює таймер на екрані.

        :param screen: Екран для малювання
        """
        # Малюємо зовнішнє кільце
        pygame.draw.circle(screen, self.outer_color, (self.x, self.y), self.width)

        # Малюємо внутрішній фон
        pygame.draw.circle(screen, self.inner_color, (self.x, self.y), self.width - 5)

        # Обчислюємо прогрес
        progress_angle = 360 * (1 - self.remaining_time / self.total_duration)

        # Вибираємо колір прогресу
        progress_color = self.warning_color if self.remaining_time / self.total_duration < 0.2 else (100, 200, 100)

        # Створюємо поверхню для дуги з прозорістю
        arc_surface = pygame.Surface((self.width * 2, self.width * 2), pygame.SRCALPHA)
        pygame.draw.arc(arc_surface, progress_color + (150,), (0, 0, self.width * 2, self.width * 2),
                        -math.pi / 2, -math.pi / 2 + math.radians(progress_angle), 10)
        screen.blit(arc_surface, (self.x - self.width, self.y - self.width))

        # Малюємо текст часу
        minutes = int(self.remaining_time // 60)
        seconds = int(self.remaining_time % 60)
        time_text = f"{minutes:02d}:{seconds:02d}"
        text_surface = self.font.render(time_text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        screen.blit(text_surface, text_rect)