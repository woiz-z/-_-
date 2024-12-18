import ctypes
import os
import pygame
import sys
import random


from Configs import Configs
from Things.Cards import Card
from Configs.Color_Constans import *
from Things.Timer import Timer
from Things.Operator_Buttons import OperatorButtons
from Display.Result_Display import ResultDisplay
from Display.Score_Display import ScoreDisplay
from Music_Manage import Music_Controller

# Ініціалізація Pygame
pygame.init()


class CardGame:
    """
    Клас для гри в карти "24 КАРТИ!".

    Атрибути:
    ----------
    time : int
        Тривалість гри в секундах.
    """
    def __init__(self, time=60):
        """
        Ініціалізує гру з заданою тривалістю.

        Параметри:
        ----------
        time : int
            Тривалість гри в секундах.
        """
        os.add_dll_directory(r"C:\msys64\mingw64\bin")
        self.setup_screen()
        self.load_fonts()
        self.initialize_game_variables()
        self.load_textures()
        self.create_and_shuffle_deck()
        self.start_dealing_animation()
        self.result_display = ResultDisplay(self.WINDOW_SIZE)
        self.score_display = ScoreDisplay(self.WINDOW_SIZE)
        self.operator_buttons = OperatorButtons(self.WINDOW_SIZE)
        Music_Controller.sound_manager.play_sound("Jazz", volume=Configs.volume)
        self.running = True

        # Створення таймера
        timer_x = 100
        timer_y = 100
        timer_width = 60
        timer_duration = time
        self.timer = Timer(timer_x, timer_y, timer_width, timer_width, timer_duration, self.button_font)

    def setup_screen(self):
        """Налаштовує екран гри."""
        self.update_window_size()
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE, pygame.RESIZABLE)
        pygame.display.set_caption("24 КАРТИ!")

    def update_window_size(self):
        """Оновлює розмір вікна гри відповідно до налаштувань."""
        self.WINDOW_SIZE = {0: (720, 480), 1: (1280, 720), 2: (1920, 1080)}.get(Configs.resolution_index)
        if Configs.fullscreen == 1:
            self.screen = pygame.display.set_mode(self.WINDOW_SIZE, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.WINDOW_SIZE, pygame.RESIZABLE)

    def load_fonts(self):
        """Завантажує шрифти для гри."""
        self.cooficient = {0: 0.5, 1: 0.75, 2: 1.0}.get(Configs.resolution_index, 0.0)
        self.title_font = pygame.font.Font(None, int(72 * self.cooficient))
        self.card_font = pygame.font.Font(None, int(72 * self.cooficient))
        self.expression_font = pygame.font.Font(None, int(48 * self.cooficient))
        self.button_font = pygame.font.Font(None, int(36 * self.cooficient))
        self.result_font = pygame.font.Font(None, int(120 * self.cooficient))

    def initialize_game_variables(self):
        """Ініціалізує змінні гри."""
        self.cards = []
        self.dealing_cards = False
        self.deal_progress = 0
        self.deal_speed = 90
        self.card_deal_positions = []
        self.selected_cards = []
        self.current_operator = None
        self.expression = ""
        self.last_input_type = None
        self.result = None
        self.result_display_timer = 0
        self.result_display_duration = 60
        self.time = 0
        self.score = 0

    def load_textures(self):
        """Завантажує текстури для гри."""
        self.background_texture = self.load_and_scale_texture('done_cards/Table.png', self.WINDOW_SIZE)
        self.deck_texture = self.load_and_scale_texture('done_cards/deck.png', (100, 150))
        self.deck_rect = self.deck_texture.get_rect(center=(self.WINDOW_SIZE[0] // 2, self.WINDOW_SIZE[1] // 2 - 250))

    def create_and_shuffle_deck(self):
        """Створює та перемішує колоду карт."""
        self.deck = self.create_deck()
        random.shuffle(self.deck)

    def create_deck(self):
        """Створює колоду карт."""
        values = list(range(1, 11))
        masts = ['B', 'C', 'H', 'P']
        return [(value, mast) for value in values for mast in masts]

    def load_and_scale_texture(self, path, size):
        """Завантажує та масштабує текстуру."""
        texture = pygame.image.load(path)
        return pygame.transform.smoothscale(texture, size)

    def start_dealing_animation(self):
        """Створення 4-х карт."""
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

        self.cards = [
            Card(value, mast, pos['start_x'], pos['start_y'], pos['start_width'], pos['start_height'], self.card_font, f'done_cards/{value}_{mast}.png')
            for (value, mast), pos in zip(self.deck, self.card_deal_positions)
        ]
        self.solve = lib.solve_24(self.cards[0].value, self.cards[1].value, self.cards[2].value, self.cards[3].value).decode('utf-8')
        while self.solve == "-1":
            random.shuffle(self.deck)
            self.cards = [
                Card(value, mast, pos['start_x'], pos['start_y'], pos['start_width'], pos['start_height'], self.card_font, f'done_cards/{value}_{mast}.png')
                for (value, mast), pos in zip(self.deck, self.card_deal_positions)
            ]
            self.solve = lib.solve_24(self.cards[0].value, self.cards[1].value, self.cards[2].value, self.cards[3].value).decode('utf-8')
        self.dealing_cards = True
        print(self.solve)
        self.deal_progress = 0

    def update_dealing_animation(self):
        """Оновлює анімацію роздачі карт."""
        if not self.dealing_cards:
            return

        self.deal_progress += 1

        card_index = self.deal_progress // self.deal_speed
        if card_index >= len(self.cards):
            self.dealing_cards = False
            return
        card = self.cards[card_index]
        pos_info = self.card_deal_positions[card_index]
        t = (self.deal_progress % self.deal_speed) / self.deal_speed
        smooth_t = self.cubic_ease_in_out(t)
        card.rect.x = pos_info['start_x'] + (pos_info['final_x'] - pos_info['start_x']) * smooth_t
        card.rect.y = pos_info['start_y'] + (pos_info['final_y'] - pos_info['start_y']) * smooth_t
        card.rect.width = pos_info['start_width'] + (pos_info['final_width'] - pos_info['start_width']) * smooth_t
        card.rect.height = pos_info['start_height'] + (pos_info['final_height'] - pos_info['start_height']) * smooth_t
        card.update_surface()
        if t >= 1:
            self.deal_progress = (card_index + 1) * self.deal_speed
        self.timer.start()

    def cubic_ease_in_out(self, t):
        """Функція плавного переходу для анімації."""
        return 4 * t * t * t if t < 0.5 else (t - 1) * (2 * t - 2) * (2 * t - 2) + 1

    def handle_events(self):
        """Обробляє події гри."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                self.operator_buttons.handle_mouse_motion(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running=False
                elif event.key == pygame.K_r:
                    self.reset_game_state()
                elif event.key == pygame.K_t:
                    if self.timer.is_running:
                        self.timer.pause()
                    else:
                        self.timer.start()
            elif not self.dealing_cards and self.result is None and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_mouse_click(event.pos)

    def handle_mouse_click(self, pos):
        """Обробляє події кліків миші."""
        button_text = self.operator_buttons.handle_mouse_click(pos)
        if button_text:
            if self.last_input_type != 'operator' or self.last_input_type == "dyzka" or button_text == '(':
                self.expression += button_text
                if button_text == ')':
                    self.last_input_type = "dyzka"
                else:
                    self.last_input_type = 'operator'
            return
        for card in self.cards:
            if card.is_clicked(pos) and not card.is_selected and self.last_input_type != 'card':
                card.is_selected = True
                self.selected_cards.append(card)
                self.expression += str(card.value)
                self.last_input_type = 'card'
                if len(self.selected_cards) == 4:
                    self.evaluate_expression()

    def evaluate_expression(self):
        """Оцінює вираз та оновлює результат."""
        lib = ctypes.CDLL('./C_Expansion/libKyrsova.dll')
        lib.evaluate_expression.argtypes = [ctypes.c_char_p]
        lib.evaluate_expression.restype = ctypes.c_double
        expression = self.expression.encode('utf-8')
        a = 0
        while a == 0:
            try:
                self.result = lib.evaluate_expression(expression)
                a = 1
            except:
                expression = (self.expression + ")").encode('utf-8')
        if self.result == 24:
            self.score += 1
        self.result_display.set_result(self.result)
        self.score_display.set_score(self.score)

    def handle_result_display(self):
        """Обробляє відображення результату."""
        self.result_display.update()
        if self.result_display.result is None:
            self.reset_game_state()

    def reset_game_state(self):
        """Скидає стан гри."""
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

    def draw_background_texture(self):
        """Малює текстуру фону."""
        self.screen.blit(self.background_texture, (0, 0))

    def draw_deck(self):
        """Малює колоду карт."""
        layers = 5
        offset = 1
        for i in range(layers):
            layer_rect = self.deck_rect.copy()
            layer_rect.x += i * offset
            layer_rect.y -= i * offset
            self.screen.blit(self.deck_texture, layer_rect)

    def draw(self):
        """Малює всі елементи гри на екрані."""
        self.draw_background_texture()
        for card in self.cards:
            card.draw(self.screen)
        self.operator_buttons.draw(self.screen)
        self.draw_deck()
        if self.expression:
            expr_surface = self.expression_font.render(self.expression, True, WHITE)
            expr_rect = expr_surface.get_rect(centerx=self.WINDOW_SIZE[0] // 2, bottom=self.WINDOW_SIZE[1] - 50)
            self.screen.blit(expr_surface, expr_rect)
        self.result_display.draw(self.screen)
        self.score_display.draw(self.screen, self.button_font)
        self.timer.draw(self.screen)
        pygame.display.flip()


