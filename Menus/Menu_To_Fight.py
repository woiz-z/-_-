from Module_to_Game.Game_Ower_Summary import GameSummaryScreen
from Module_to_Game.Game_Ower_Screen import GameOverScreen
from Game.One_ON_One_Game import MultiplayerCardGame
from Game.Infinity_Mode import InfinityMode
from Menus.Time_Selection_Menu import TimeSelectionMenu
from Menus.Main_Menu import Menu

class Menu_To_Fight(Menu):
    def __init__(self):
        """
        Ініціалізує об'єкт меню для вибору режиму гри.
        """
        super().__init__("24 Карти!")
        self.buttons = [
            ("Безкінечна гра", self.infinity_mode),
            ("Гра 1 на 1", self.one_on_one_mode),
            ("Час для гри", self.time_selection),
            ("Назад", self.back)
        ]
        self.setup_buttons()

    def infinity_mode(self):
        """
        Запускає режим безкінечної гри.
        """
        start_game = InfinityMode()
        score = start_game.run()
        game_over_screen = GameOverScreen()
        game_over_screen.activate(score)

    def one_on_one_mode(self):
        """
        Запускає режим гри 1 на 1.
        """

        player_time = 60  # Час для кожного гравця (в секундах)
        player1_score = self.run_multiplayer_game(player_time)
        player2_score = self.run_multiplayer_game(player_time)

        self.show_game_summary(player1_score, player2_score)

    def run_multiplayer_game(self, player_time):
        """
        Запускає гру для одного гравця в режимі 1 на 1.

        :param player_time: Час для кожного гравця (в секундах)
        :return: Результат гри для гравця
        """
        game = MultiplayerCardGame(player_time)
        score = game.run()
        game_over_screen = GameOverScreen()
        game_over_screen.activate(score)
        return score

    def show_game_summary(self, player1_score, player2_score):
        """
        Показує підсумки гри.

        :param player1_score: Результат першого гравця
        :param player2_score: Результат другого гравця
        """
        summary_screen = GameSummaryScreen()
        if player1_score > player2_score:
            summary_screen.activate("Гравець 1", player1_score, player2_score)
        elif player1_score < player2_score:
            summary_screen.activate("Гравець 2", player1_score, player2_score)
        else:
            summary_screen.activate("Нічия", player1_score, player2_score)

    def time_selection(self):
        """
        Запускає меню вибору часу гри.
        """
        time_menu = TimeSelectionMenu()
        time = time_menu.run()
        if time is not None:
            player1_score = self.run_multiplayer_game(time)
            player2_score = self.run_multiplayer_game(time)
            self.show_game_summary(player1_score, player2_score)

    def back(self):
        """
        Повертає до попереднього меню.
        """
        self.running = False