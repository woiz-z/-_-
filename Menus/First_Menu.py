import sys
from Menus.Setings_Menu import SettingsMenu
from Menus.Menu_To_Fight import Menu_To_Fight
from Menus.Main_Menu import *
from Music_Manage import Music_Controller


class First_Menu(Menu):
    """
    Клас для створення та управління головним меню гри.
    """

    def __init__(self):
        """
        Ініціалізує об'єкт головного меню.
        """
        super().__init__("24 КАРТИ!")
        self.buttons = [
            ("Грати", self.start_game),
            ("Налаштування", self.settings),
            ("Вийти", self.quit_game)
        ]
        self.setup_buttons()
        self.music = Music_Controller.sound_manager
        self.music.play_sound("Fon", loops=-1, volume=0.1 * Configs.volume)

    def draw_made_by_text(self):
        """
        Малює надпис 'MADE BY WOIZZZ' з ефектом світіння та зимовими кольорами.
        """
        made_by_text = "MADE BY WOIZZZ"
        bottomright = (self.WINDOW_SIZE[0] - 20, self.WINDOW_SIZE[1] - 20)

        # Створюємо кілька шарів тексту для світіння
        for offset in range(10, 0, -1):
            glow_surface = self.made_by_font.render(made_by_text, True, (255, 255, 255, 20 // offset))
            glow_rect = glow_surface.get_rect(bottomright=bottomright)
            glow_rect.inflate_ip(offset * 2, offset * 2)
            self.screen.blit(glow_surface, glow_rect)

        # Основний текст з зимовим ефектом
        hue = (self.time * 0.5) % 360
        made_by_color = pygame.Color(0, 0, 0)
        made_by_color.hsva = (hue, 20, 100, 100)

        # Малюємо тінь тексту
        for shift_x, shift_y in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
            shadow_surface = self.made_by_font.render(made_by_text, True, (0, 0, 0, 100))
            shadow_rect = shadow_surface.get_rect(bottomright=(bottomright[0] + shift_x, bottomright[1] + shift_y))
            self.screen.blit(shadow_surface, shadow_rect)

        # Основний кольоровий текст
        made_by_surface = self.made_by_font.render(made_by_text, True, made_by_color)
        made_by_rect = made_by_surface.get_rect(bottomright=bottomright)
        self.screen.blit(made_by_surface, made_by_rect)

    def add_something_to_run(self):
        """
        Додає функцію для малювання надпису 'MADE BY WOIZZZ' до основного циклу.
        """
        self.draw_made_by_text()

    def start_game(self):
        """
        Запускає гру.
        """
        fight_menu = Menu_To_Fight()
        fight_menu.run()

    def settings(self):
        """
        Відкриває меню налаштувань.
        """
        settings_menu = SettingsMenu()
        settings_menu.run()
        self.music.stop_all_sounds()
        self.music.play_sound("Fon", loops=-1, volume=0.1 * Configs.volume)


    def quit_game(self):
        """
        Виходить з гри.
        """
        pygame.quit()
        sys.exit()