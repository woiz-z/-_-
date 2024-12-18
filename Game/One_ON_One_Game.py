import random
import ctypes
import pygame

from Configs import Configs
from Game.Game_Main_Module import CardGame, Card
from Music_Manage import Music_Controller


class MultiplayerCardGame(CardGame):
    def __init__(self, time=60):
        """
        Ініціалізує об'єкт багатокористувацької карткової гри.

        :param time: Час гри (в секундах)
        """
        pygame.font.init()  # Ініціалізація модуля шрифтів
        super().__init__(time)

    def reset_game_state(self):
        """
        Скидає стан гри до початкового.
        """
        if self.result == 24:
            random.shuffle(self.deck)

            card_width_final = self.WINDOW_SIZE[0] // 7
            card_height_final = self.WINDOW_SIZE[1] // 3
            card_width_start = 100
            card_height_start = 150
            card_y = (self.WINDOW_SIZE[1] - card_height_final) // 2
            spacing = (self.WINDOW_SIZE[0] - (card_width_final * 4)) // 7
            vidstyp = (self.WINDOW_SIZE[0] - ((card_width_final + spacing) * 4)) // 2 - spacing // 2

            self.card_deal_positions = [
                {
                    'start_x': self.deck_rect.centerx - card_width_start // 2,
                    'start_y': self.deck_rect.centery - card_height_start // 2,
                    'final_x': spacing + i * (card_width_final + spacing) + vidstyp,
                    'final_y': card_y,
                    "start_width": card_width_start,
                    "start_height": card_height_start,
                    "final_width": card_width_final,
                    "final_height": card_height_final
                }
                for i in range(4)
            ]

            lib = ctypes.CDLL('./C_Expansion/libKyrsova_vuraz.dll')
            lib.solve_24.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
            lib.solve_24.restype = ctypes.c_char_p

            while True:
                random.shuffle(self.deck)
                self.cards = [
                    Card(value, mast, pos['start_x'], pos['start_y'], pos['start_width'], pos['start_height'],
                         self.card_font, f'done_cards/{value}_{mast}.png')
                    for (value, mast), pos in zip(self.deck, self.card_deal_positions)
                ]
                solve = lib.solve_24(self.cards[0].value, self.cards[1].value, self.cards[2].value,
                                     self.cards[3].value).decode('utf-8')
                if solve != "-1":
                    self.solve = solve
                    print(self.solve)
                    break

            self.dealing_cards = True
            self.deal_progress = 0

        for card in self.selected_cards:
            card.is_selected = False
        self.selected_cards.clear()
        self.expression = ""
        self.last_input_type = None
        self.result = None
        self.result_display_timer = 0

        if not self.timer.is_running:
            self.timer.start()

    def run(self):
        """
        Запускає основний цикл гри.
        """
        clock = pygame.time.Clock()
        Music_Controller.sound_manager.stop_sound("Fon")
        while self.running:
            self.handle_events()
            if self.dealing_cards:
                self.update_dealing_animation()
            if self.result is not None:
                self.handle_result_display()

            if self.timer.update():
                self.running = False
                return self.score

            self.draw_deck()
            self.draw()
            self.time += 1
            clock.tick(60)
        Music_Controller.sound_manager.stop_sound("Jazz")
        Music_Controller.sound_manager.play_sound("Fon", volume=Configs.volume * 0.2,priority=True)
        return self.score