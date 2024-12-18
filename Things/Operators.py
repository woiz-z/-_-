import pygame
from Configs.Color_Constans import *

class OperationButton:
    def __init__(self, x, y, width, height, text, font):
        """
        Ініціалізує об'єкт кнопки оператора.

        :param x: Координата x кнопки
        :param y: Координата y кнопки
        :param width: Ширина кнопки
        :param height: Висота кнопки
        :param text: Текст кнопки
        :param font: Шрифт тексту кнопки
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = BLACK
        self.text_color = WHITE
        self.hover_color = (50, 50, 50)
        self.border_color = WHITE
        self.is_hovered = False

    def draw(self, screen):
        """
        Малює кнопку на екрані.

        :param screen: Екран для малювання
        """
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, current_color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 2)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        """
        Перевіряє, чи була кнопка натиснута.

        :param pos: Позиція миші
        :return: True, якщо кнопка була натиснута, інакше False
        """
        return self.rect.collidepoint(pos)