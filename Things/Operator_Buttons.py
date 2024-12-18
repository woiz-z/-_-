import pygame


from Things.Operators import OperationButton
from Configs.Configs import resolution_index


class OperatorButtons:
    def __init__(self, window_size):
        """
        Ініціалізує об'єкт кнопок операторів.

        :param window_size: Розмір вікна
        """
        self.window_size = window_size
        self.font = pygame.font.Font(None, int(48 * {0: 0.5, 1: 0.75, 2: 1.0}.get(resolution_index, 0.0)))
        self.buttons = self.create_operation_buttons()

    def create_operation_buttons(self):
        """
        Створює кнопки операторів.

        :return: Список кнопок операторів
        """
        button_width = 60
        button_height = 50
        margin_right = 20
        margin_top = 100
        vertical_spacing = 10
        button_texts = ['+', '-', '*', '/', '(', ')']
        button_x = self.window_size[0] - button_width - margin_right
        return [
            OperationButton(button_x, margin_top + i * (button_height + vertical_spacing), button_width, button_height, text, self.font)
            for i, text in enumerate(button_texts)
        ]

    def draw(self, screen):
        """
        Малює кнопки на екрані.

        :param screen: Екран для малювання
        """
        for button in self.buttons:
            button.draw(screen)

    def handle_mouse_motion(self, pos):
        """
        Обробляє рух миші.

        :param pos: Позиція миші
        """
        for button in self.buttons:
            button.is_hovered = button.rect.collidepoint(pos)

    def handle_mouse_click(self, pos):
        """
        Обробляє клік миші.

        :param pos: Позиція миші
        :return: Текст кнопки, якщо вона була натиснута, інакше None
        """
        for button in self.buttons:
            if button.is_clicked(pos):
                return button.text
        return None