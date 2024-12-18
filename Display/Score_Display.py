import pygame
from Configs.Color_Constans import WHITE

class ScoreDisplay:
    def __init__(self, window_size):
        """
        Ініціалізує об'єкт ScoreDisplay.

        :param window_size: Розмір вікна гри
        """
        self.window_size = window_size
        self.score = 0

    def set_score(self, score):
        """
        Встановлює поточний рахунок.

        :param score: Поточний рахунок
        """
        self.score = score

    def draw(self, screen, font):
        """
        Малює рахунок на екрані.

        :param screen: Екран для малювання
        :param font: Шрифт для відображення рахунку
        """
        # Створюємо напівпрозорий фон для рахунку
        score_bg = pygame.Surface((200, 50), pygame.SRCALPHA)
        score_bg.fill((0, 0, 0, 100))  # Темний напівпрозорий фон
        score_bg_rect = score_bg.get_rect(bottomright=(self.window_size[0] - 10, self.window_size[1] - 10))

        # Відображаємо текст рахунку з тінню
        shadow_text = font.render(f"Кількість очок: {self.score}", True, (50, 50, 50))
        score_text = font.render(f"Кількість очок: {self.score}", True, WHITE)

        # Позиціонуємо тінь з невеликим зсувом
        shadow_rect = score_text.get_rect(bottomright=(self.window_size[0] - 15, self.window_size[1] - 15))
        score_rect = score_text.get_rect(bottomright=(self.window_size[0] - 20, self.window_size[1] - 20))

        # Малюємо фон
        screen.blit(score_bg, score_bg_rect)

        # Малюємо тінь та текст для класичного 3D ефекту
        screen.blit(shadow_text, shadow_rect)
        screen.blit(score_text, score_rect)