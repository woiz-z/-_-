import sys
import pygame

class EventHandler:
    """
    Клас для обробки подій гри.

    Атрибути:
    ----------
    game : object
        Об'єкт гри, який містить стан гри та методи для взаємодії з нею.
    """
    def __init__(self, game):
        """
        Ініціалізує обробник подій з об'єктом гри.

        Параметри:
        ----------
        game : object
            Об'єкт гри.
        """
        self.game = game

    def handle_events(self):
        """
        Обробляє події, що надходять від користувача.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                self.game.operator_buttons.handle_mouse_motion(event.pos)
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event)
            elif (not self.game.dealing_cards and self.game.result is None and
                  event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                self.game.handle_mouse_click(event.pos)

    def handle_keydown(self, event):
        """
        Обробляє події натискання клавіш.

        Параметри:
        ----------
        event : pygame.event.Event
            Подія натискання клавіші.
        """
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        elif event.key == pygame.K_r:
            self.game.reset_game_state()
        elif event.key == pygame.K_t:
            self.toggle_timer()
        elif event.key == pygame.K_z:
            self.reset_timer()

    def toggle_timer(self):
        """
        Перемикає стан таймера між паузою та відновленням.
        """
        if self.game.timer.is_running:
            self.game.timer.pause()
        else:
            self.game.timer.start()

    def reset_timer(self):
        """
        Скидає таймер та запускає його знову.
        """
        self.game.timer.reset()
        self.game.timer.start()