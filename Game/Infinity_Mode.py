from Game.Game_Main_Module import *

class InfinityMode(CardGame):
    def __init__(self):
        """
        Ініціалізує режим нескінченної гри.
        """
        super().__init__()
        self.result_display = ResultDisplay(self.WINDOW_SIZE)
        self.score_display = ScoreDisplay(self.WINDOW_SIZE)
        self.operator_buttons = OperatorButtons(self.WINDOW_SIZE)

    def handle_events(self):
        """
        Обробляє події гри.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                self.operator_buttons.handle_mouse_motion(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r:
                    self.reset_game_state()
            elif not self.dealing_cards and self.result is None and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_mouse_click(event.pos)

    def draw(self):
        """
        Малює всі елементи гри на екрані.
        """
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
        pygame.display.flip()

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
            self.draw_deck()
            self.draw()
            self.time += 1
            clock.tick(60)
        Music_Controller.sound_manager.stop_sound("Jazz")
        Music_Controller.sound_manager.play_sound("Fon", volume=Configs.volume * 0.2,priority=True)
        return self.score
