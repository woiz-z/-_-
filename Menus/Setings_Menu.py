from Configs import Configs
from Menus.Main_Menu import Menu
from Other.Other_Functions import file_write

class SettingsMenu(Menu):
    def __init__(self):
        """
        Ініціалізує меню налаштувань.
        """
        super().__init__("Налаштування")
        self.buttons = [
            ("Роздільна здатність", self.change_resolution),
            ("Гучність", self.change_volume),
            ("Повноекранний режим", self.toggle_fullscreen_setting),
            ("Повернутися", self.back_to_main_menu),
        ]
        self.resolutions = [
            (720, 480),
            (1280, 720),
            (1920, 1080),
        ]
        self.setup_buttons()

    def draw_settings_values(self):
        """
        Відображає поточні значення налаштувань біля кнопок.
        """
        for i, (text, _) in enumerate(self.buttons):
            button_rect = self.get_button_rect(i)
            value_text = ""

            if text == "Роздільна здатність":
                current_res = self.resolutions[Configs.resolution_index]
                value_text = f"{current_res[0]}x{current_res[1]}"
            elif text == "Гучність":
                value_text = f"{int(Configs.volume * 100)}%"
            elif text == "Повноекранний режим":
                value_text = "✓" if Configs.fullscreen else "×"

            if value_text:
                value_surface = self.button_font.render(value_text, True, self.BUTTON_HOVER)
                value_rect = value_surface.get_rect(midleft=(button_rect.right + 20, button_rect.centery))
                self.screen.blit(value_surface, value_rect)

    def change_resolution(self):
        """
        Змінює роздільну здатність циклічно.
        """
        Configs.resolution_index = (Configs.resolution_index + 1) % len(self.resolutions)

    def change_volume(self):
        """
        Змінює гучність циклічно (0.2 -> 0.4 -> 0.6 -> 0.8 -> 1.0 -> 0.2).
        """
        Configs.volume = round((Configs.volume + 0.2) % 1.2, 1)

    def toggle_fullscreen_setting(self):
        """
        Перемикає повноекранний режим.
        """
        Configs.fullscreen = not Configs.fullscreen

    def back_to_main_menu(self):
        """
        Повертає до головного меню.
        """
        file_write()
        self.running = False

    def add_something_previous_quit(self):
        """
        Додає додаткові дії перед виходом з гри.
        """
        file_write()

    def add_something_to_run(self):
        """
        Додаткова функція для відображення значень налаштувань.
        """
        self.draw_settings_values()