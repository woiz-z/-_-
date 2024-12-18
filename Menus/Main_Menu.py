import math
from pygame.locals import *
import pygame

from Configs import Configs
from Music_Manage import Music_Controller
from Things.Snig import Snowflake


class Menu:
    """
    Клас для створення та управління меню гри з зимовою темою.
    """

    def __init__(self, title):
        """
        Ініціалізує об'єкт меню.

        :param title: Назва меню.
        """
        pygame.init()
        self.running = True
        self.info = pygame.display.Info()
        self.set_window_size()
        self.set_screen_mode()
        pygame.display.set_caption(title)

        self.set_colors()
        self.set_fonts()
        self.pressed_button = None
        self.time = 0
        self.particles = []
        self.snowflake_manager = Snowflake(self.WINDOW_SIZE)
        self.hover_particles = []
        self.title_text = title
        self.buttons = []
        self.update_window_size()
        self.music = Music_Controller.sound_manager

    def set_window_size(self):
        """
        Встановлює розмір вікна на основі конфігурації.
        """
        self.WINDOW_SIZE = {0: (720, 480), 1: (1280, 720), 2: (1920, 1080)}.get(Configs.resolution_index)

    def set_screen_mode(self):
        """
        Встановлює режим екрану (повноекранний або змінюваний).
        """
        if Configs.fullscreen == 1:
            self.WINDOW_SIZE = (1280, 720)
            self.screen = pygame.display.set_mode(self.WINDOW_SIZE, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.WINDOW_SIZE, pygame.RESIZABLE)

    def set_colors(self):
        """
        Встановлює кольори для зимового меню.
        """
        self.GRADIENT_TOP = (0, 0, 51)
        self.GRADIENT_BOTTOM = (0, 0, 102)
        self.BUTTON_COLOR = (230, 230, 250)
        self.BUTTON_SHADOW = (70, 70, 100)
        self.BUTTON_HOVER = (200, 200, 230)
        self.BUTTON_PRESSED = (180, 180, 210)
        self.TEXT_COLOR = (20, 20, 50)
        self.TITLE_COLOR = (200, 200, 255)
        self.BUTTON_BORDER_COLOR = (100, 149, 237)
        self.BORDER_WIDTH = 15
        self.text_presed_color = (0, 0, 100)
        self.text_hover_color = (0, 0, 50)

    def set_fonts(self):
        """
        Встановлює шрифти для різних елементів меню.
        """
        self.cooficient = {0: 0.5, 1: 0.75, 2: 1.0}.get(Configs.resolution_index, 0.0)
        self.BUTTON_WIDTH = int(400 * self.cooficient)
        self.BUTTON_HEIGHT = int(70 * self.cooficient)
        self.BUTTON_MARGIN = 30
        self.SHADOW_OFFSET = 4
        self.fullscreen = 0
        self.title_font = pygame.font.Font(None, int(120 * self.cooficient))
        self.button_font = pygame.font.Font(None, int(48 * self.cooficient))
        self.made_by_font = pygame.font.Font(None, int(42 * self.cooficient))

    def update_window_size(self):
        """
        Оновлює розмір вікна та шрифти.
        """
        self.set_window_size()
        self.set_fonts()
        self.set_screen_mode()
        self.snowflake_manager = Snowflake(self.WINDOW_SIZE)

    def handle_resolution_change(self):
        """
        Обробляє зміну роздільної здатності екрану.
        """
        self.update_window_size()
        self.particles = []
        self.hover_particles = []
        self.setup_buttons()

    def setup_buttons(self):
        """
        Налаштовує кнопки меню.
        """
        self.button_scales = [1.0] * len(self.buttons)
        self.button_rotations = [0] * len(self.buttons)

    def update_particles(self):
        """
        Оновлює та малює частинки (сніжинки).
        """
        self.particles = [p for p in self.particles if p.update()]
        for p in self.particles:
            p.draw(self.screen)

    def draw_snowflakes(self):
        """
        Малює сніжинки на зимовому фоні.
        """
        self.snowflake_manager.update_and_draw(self.screen, self.time)

    def draw_gradient_background(self):
        """
        Малює градієнтний фон для зимового меню.
        """
        height = self.WINDOW_SIZE[1]
        for y in range(height):
            ratio = y / height
            base_color = [
                self.GRADIENT_TOP[i] * (1 - ratio) + self.GRADIENT_BOTTOM[i] * ratio
                for i in range(3)
            ]
            wave = (
                math.sin(y * 0.01 + self.time * 0.002) * 5 +
                math.cos(y * 0.02 + self.time * 0.003) * 3 +
                math.sin((y * 0.005 + self.time * 0.001) * 2) * 7
            )
            color = [max(0, min(255, c + wave)) for c in base_color]
            pygame.draw.line(self.screen, color, (0, y), (self.WINDOW_SIZE[0], y))

    def draw_button_with_effects(self, text, rect, state="normal", index=0):
        """
        Малює кнопку з ефектами для зимового меню.
        """
        scale = self.button_scales[index]
        text_surf = self.button_font.render(text, True, self.TEXT_COLOR)
        if state == "hover":
            text_surf = self.button_font.render(text, True, self.text_hover_color)
            self.button_scales[index] = min(1.1, scale + 0.01)
        else:
            self.button_scales[index] = max(1.0, scale - 0.01)

        button_surf = pygame.Surface((rect.width + 20, rect.height + 20), pygame.SRCALPHA)
        shadow_rect = pygame.Rect(10, 10 + (4 if state != "pressed" else 2), rect.width, rect.height)
        pygame.draw.rect(button_surf, (50, 50, 50), shadow_rect, border_radius=self.BORDER_WIDTH)

        button_rect = pygame.Rect(10, 10, rect.width, rect.height)
        color = {
            "normal": (70, 130, 180),
            "hover": (100, 149, 237),
            "pressed": (30, 144, 255)
        }[state]
        pygame.draw.rect(button_surf, color, button_rect, border_radius=self.BORDER_WIDTH)

        highlight_rect = button_rect.copy()
        highlight_rect.height //= 2
        pygame.draw.rect(button_surf,
                         (*[min(255, c + 30) for c in color], 180),
                         highlight_rect,
                         border_radius=self.BORDER_WIDTH)

        if state == "pressed":
            glow_rect = button_rect.copy()
            pygame.draw.rect(button_surf,
                             (255, 255, 255),
                             glow_rect,
                             width=5,
                             border_radius=self.BORDER_WIDTH)
            text_surf = self.button_font.render(text, True, (255, 255, 255))

        text_rect = text_surf.get_rect(center=(button_rect.centerx, button_rect.centery))
        button_surf.blit(text_surf, text_rect)

        scaled_size = (int(button_surf.get_width() * scale), int(button_surf.get_height() * scale))
        scaled_surf = pygame.transform.scale(button_surf, scaled_size)
        final_rect = scaled_surf.get_rect(center=rect.center)
        self.screen.blit(scaled_surf, final_rect)

    def get_button_rect(self, index):
        """
        Отримує прямокутник кнопки за індексом.
        """
        x = (self.WINDOW_SIZE[0] - self.BUTTON_WIDTH) // 2
        y = ((self.WINDOW_SIZE[1] // 2) + (self.BUTTON_HEIGHT + self.BUTTON_MARGIN) * index) - 70
        return pygame.Rect(x, y, self.BUTTON_WIDTH, self.BUTTON_HEIGHT)

    def draw_title_with_effects(self):
        """
        Малює заголовок меню з ефектами.
        """
        self.title_offset = math.sin(self.time * 0.05) * 10

        for offset in range(5, 0, -1):
            glow_surface = self.title_font.render(self.title_text, True, (*self.TITLE_COLOR[:3], 30 // offset))
            glow_rect = glow_surface.get_rect(center=(self.WINDOW_SIZE[0] // 2, self.WINDOW_SIZE[1] // 4 + self.title_offset))
            glow_rect = glow_rect.inflate(offset * 4, offset * 4)
            self.screen.blit(glow_surface, glow_rect)

        hue = (self.time * 0.5) % 360
        title_color = pygame.Color(0, 0, 0)
        title_color.hsva = (hue, 80, 100, 100)

        outline_color = (0, 0, 0)
        for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
            outline_surface = self.title_font.render(self.title_text, True, outline_color)
            outline_rect = outline_surface.get_rect(center=(self.WINDOW_SIZE[0] // 2 + dx, self.WINDOW_SIZE[1] // 4 + self.title_offset + dy))
            self.screen.blit(outline_surface, outline_rect)

        title_surface = self.title_font.render(self.title_text, True, title_color)
        title_rect = title_surface.get_rect(center=(self.WINDOW_SIZE[0] // 2, self.WINDOW_SIZE[1] // 4 + self.title_offset))
        self.screen.blit(title_surface, title_rect)

    def add_something_to_run(self):
        """
        Додає додаткові дії до основного циклу.
        """
        pass

    def add_something_previous_quit(self):
        """
        Додає додаткові дії перед виходом з гри.
        """
        pass

    def run(self):
        """
        Запускає основний цикл меню.
        """
        clock = pygame.time.Clock()
        previous_resolution = Configs.resolution_index
        previous_fullscreen = Configs.fullscreen
        while self.running:
            if previous_resolution != Configs.resolution_index or previous_fullscreen != Configs.fullscreen:
                self.handle_resolution_change()
                previous_resolution = Configs.resolution_index
                previous_fullscreen = Configs.fullscreen
            self.time += 1
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == VIDEORESIZE:
                    if not Configs.fullscreen:
                        self.WINDOW_SIZE = (event.w, event.h)
                        self.screen = pygame.display.set_mode(self.WINDOW_SIZE, pygame.RESIZABLE)
                        self.snowflake_manager = Snowflake(self.WINDOW_SIZE)
                if event.type == QUIT:
                    self.add_something_previous_quit()
                    self.running = False
                    quit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.music.play_sound("Klik", loops=0, volume=Configs.volume)
                        for i, (text, callback) in enumerate(self.buttons):
                            if self.get_button_rect(i).collidepoint(mouse_pos):
                                self.pressed_button = i
                elif event.type == MOUSEBUTTONUP:
                    if event.button == 1 and self.pressed_button is not None:
                        if self.get_button_rect(self.pressed_button).collidepoint(mouse_pos):
                            self.buttons[self.pressed_button][1]()
                        self.pressed_button = None
            self.draw_gradient_background()
            self.draw_snowflakes()
            self.draw_title_with_effects()
            self.update_particles()
            for i, (text, _) in enumerate(self.buttons):
                button_rect = self.get_button_rect(i)
                state = "normal"
                if i == self.pressed_button:
                    state = "pressed"
                elif button_rect.collidepoint(mouse_pos):
                    state = "hover"
                self.draw_button_with_effects(text, button_rect, state, i)
            self.add_something_to_run()
            pygame.display.flip()
            clock.tick(60)