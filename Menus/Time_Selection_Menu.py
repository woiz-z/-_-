from Menus.Main_Menu import Menu


class TimeSelectionMenu(Menu):
    def __init__(self):
        """
        Ініціалізує меню вибору часу гри.
        """
        super().__init__("Вибір Часу Гри")

        # Список доступних варіантів часу
        self.time_options = [
            ("30 секунд", 30),
            ("60 секунд", 60),
            ("90 секунд", 90),
            ("120 секунд", 120),
            ("Назад", None)
        ]

        # Створення кнопок для кожного варіанту часу
        self.buttons = [(option, lambda t=time: self.select_time(t)) for option, time in self.time_options]

        # Додаткова змінна для збереження вибраного часу
        self.selected_time = None

        self.setup_buttons()

    def select_time(self, time):
        """
        Обробляє вибір часу гри.

        :param time: Вибраний час гри в секундах
        """
        if time is None:
            # Повернення до попереднього меню
            self.running = False
            self.selected_time = None
        else:
            # Встановлення вибраного часу
            self.selected_time = time
            self.running = False

    def run(self):
        """
        Запускає меню вибору часу.

        :return: Вибраний час гри або None
        """
        super().run()
        return self.selected_time