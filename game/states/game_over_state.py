import pygame
from game.states.base_state import BaseState
from game.constants import *

class GameOverState(BaseState):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.font_big = pygame.font.Font(None, 180)
        self.font_small = pygame.font.Font(None, 90)

    def enter(self):
        pass

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game_manager.change_state(GAME_STATE_PLAYING)
            elif event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                self.game_manager.change_state(GAME_STATE_MENU)

    def render(self, screen):
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(255 - 100 * ratio)
            g = int(192 - 100 * ratio)
            b = int(203 - 50 * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        title = self.font_big.render("GAME OVER", True, DARK_PINK)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 300)))

        score = getattr(self.game_manager, "score", 0)
        score_text = self.font_big.render(str(score), True, GOLD)
        screen.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH//2, 540)))

        msg = self.font_small.render("Press SPACE to Play Again", True, HOT_PINK)
        screen.blit(msg, msg.get_rect(center=(SCREEN_WIDTH//2, 850)))
