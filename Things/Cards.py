import pygame

class Card:
    def __init__(self, value, mast, x, y, width, height, font, texture):
        """
        Ініціалізує об'єкт карти.

        :param value: Значення карти
        :param mast: Масть карти
        :param x: Координата x верхнього лівого кута карти
        :param y: Координата y верхнього лівого кута карти
        :param width: Ширина карти
        :param height: Висота карти
        :param font: Шрифт для тексту на карті
        :param texture: Текстура карти
        """
        self.value = value
        self.mast = mast
        self.original_rect = pygame.Rect(x, y, width, height)
        self.rect = self.original_rect.copy()
        self.is_selected = False
        self.font = font
        self.texture = texture
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self._draw_card()

    def _draw_card(self):
        """
        Малює карту з текстурою та закругленими кутами.
        """
        self.surface.fill((0, 0, 0, 0))
        texture_surface = pygame.image.load(self.texture)
        texture_surface = pygame.transform.smoothscale(texture_surface, (self.rect.width, self.rect.height))
        mask = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=20)
        masked_texture = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        masked_texture.blit(texture_surface, (0, 0))
        masked_texture.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.surface.blit(masked_texture, (0, 0))

    def update_surface(self):
        """
        Оновлює поверхню карти.
        """
        self.surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self._draw_card()

    def draw(self, screen):
        """
        Малює карту на екрані.

        :param screen: Поверхня екрану для малювання
        """
        if self.is_selected:
            scaled_width = int(self.rect.width * 1.2)
            scaled_height = int(self.rect.height * 1.2)
            texture_surface = pygame.image.load(self.texture)
            texture_surface = pygame.transform.smoothscale(texture_surface, (scaled_width, scaled_height))
            mask = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
            pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=20)
            masked_texture = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
            masked_texture.blit(texture_surface, (0, 0))
            masked_texture.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            scaled_rect = masked_texture.get_rect(center=self.rect.center)
            screen.blit(masked_texture, scaled_rect)
        else:
            screen.blit(self.surface, self.rect)

    def is_clicked(self, pos):
        """
        Перевіряє, чи була карта натиснута.

        :param pos: Координати натискання миші
        :return: True, якщо карта була натиснута, інакше False
        """
        return self.rect.collidepoint(pos)