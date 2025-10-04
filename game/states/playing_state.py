
import pygame
import random
import json
import os
from game.states.base_state import BaseState
from game.constants import *
from game.entities.flappy_barbie import FlappyBarbie
from game.entities.coin import CoinManager
from game.world.pipes import PipeManager
from game.sound_generator import play_sound
from game.effects import ParticleSystem, BackgroundStars, RainbowEffect, ScoreEffect


class PlayingState(BaseState):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.barbie = None
        self.pipe_manager = None
        self.coin_manager = None
        self.paused = False
        self.ui_font = None
        self.title_font = None
        self.game_started = False
        self.particle_system = None
        self.background_stars = None
        self.rainbow_effect = None
        self.score_effect = None
        self.last_score = 0
        self.coins_collected = 0
        self.current_skin = "default"
        self.current_location = "default"
        self.current_fps = 60

    def enter(self):
        self.ui_font = pygame.font.Font(None, 180)
        self.title_font = pygame.font.Font(None, 120)
        self._load_shop_settings()
        self.barbie = FlappyBarbie(100, BARBIE_START_Y)
        self._apply_skin()
        self.pipe_manager = PipeManager()
        self.coin_manager = CoinManager()
        self.particle_system = ParticleSystem()
        self.background_stars = BackgroundStars()
        self.rainbow_effect = RainbowEffect()
        self.score_effect = ScoreEffect()
        self.last_score = 0
        self.paused = False
        self.game_started = False
        self.coins_collected = 0

        self.coin_icon = None
        try:
            self.coin_icon = pygame.image.load("assets/images/money.png").convert_alpha()
            self.coin_icon = pygame.transform.scale(self.coin_icon, (60, 60))
        except:
            pass

        self.background_surface = self._create_background_surface()

    def _load_shop_settings(self):
        try:
            if os.path.exists("shop.json"):
                with open("shop.json", 'r') as f:
                    shop_data = json.load(f)
                    self.current_skin = shop_data.get("current_skin", "default")
                    self.current_location = shop_data.get("current_location", "default")
        except:
            pass

    def _apply_skin(self):
        if self.current_skin != "default":
            skin_data = SKINS.get(self.current_skin)
            if skin_data and skin_data.get("file"):
                try:
                    skin_path = f"assets/images/{skin_data['file']}"
                    skin_image = pygame.image.load(skin_path).convert_alpha()
                    skin_image = pygame.transform.scale(skin_image, (BARBIE_SIZE, BARBIE_SIZE))
                    self.barbie.sprite = skin_image
                    self.barbie.has_sprite = True
                    print(f"✅ Применён скин: {skin_data['name']}")
                except Exception as e:
                    print(f"❌ Ошибка загрузки скина {self.current_skin}: {e}")

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._save_collected_coins()
                self.game_manager.change_state(GAME_STATE_MENU)
            elif event.key == pygame.K_SPACE:
                if not self.game_started:
                    self.game_started = True
                self.barbie.flap()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not self.game_started:
                self.game_started = True
            self.barbie.flap()

    def update(self, dt):
        if self.paused:
            return

        self.current_fps = int(1 / dt) if dt > 0 else 60

        self.particle_system.update(dt)
        self.background_stars.update(dt)
        self.rainbow_effect.update(dt)
        self.score_effect.update(dt)
        self.barbie.update(dt)
        if self.game_started:
            prev_score = self.pipe_manager.score
            self.pipe_manager.update(dt, self.barbie)
            if self.pipe_manager.score > prev_score:
                self.score_effect.create_effect(SCREEN_WIDTH // 2, 100, self.pipe_manager.score)
                for _ in range(COINS_PER_SCORE):
                    self.coins_collected += 1
            self.coin_manager.update(dt, self.barbie)
        if not self.barbie.is_alive:
            play_sound('death')
            self._save_collected_coins()
            self._show_screamer()
            pygame.time.wait(1000)
            self.game_manager.score = self.pipe_manager.score
            self.game_manager.change_state(GAME_STATE_GAME_OVER)

    def _save_collected_coins(self):
        if self.coins_collected > 0:
            try:
                shop_file = "shop.json"
                shop_data = {}
                if os.path.exists(shop_file):
                    with open(shop_file, 'r') as f:
                        shop_data = json.load(f)
                current_coins = shop_data.get("coins", 0)
                shop_data["coins"] = current_coins + self.coins_collected
                with open(shop_file, 'w') as f:
                    json.dump(shop_data, f, indent=4)
                print(f"Collected coins: {self.coins_collected}")
            except:
                pass

    def render(self, screen):
        self._render_background(screen)
        self.rainbow_effect.render(screen)
        self.background_stars.render(screen)
        self.particle_system.render(screen)
        self.pipe_manager.render(screen)
        self.coin_manager.render(screen)
        self._render_ground(screen)
        self.barbie.render(screen)
        self.score_effect.render(screen)
        score_text = self.ui_font.render(str(self.pipe_manager.score), True, GOLD)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        shadow_text = self.ui_font.render(str(self.pipe_manager.score), True, DARK_PINK)
        shadow_rect = shadow_text.get_rect(center=(SCREEN_WIDTH // 2 + 5, 105))
        screen.blit(shadow_text, shadow_rect)
        screen.blit(score_text, score_rect)
        coin_font = pygame.font.Font(None, 90)

        if self.coin_icon:
            screen.blit(self.coin_icon, (30, 25))
            coin_text = coin_font.render(f"{self.coins_collected}", True, GOLD)
            screen.blit(coin_text, (110, 30))
        else:
            coin_text = coin_font.render(f"💰 {self.coins_collected}", True, GOLD)
            screen.blit(coin_text, (30, 30))
        if self.pipe_manager.difficulty_level > 1:
            diff_font = pygame.font.Font(None, 90)
            diff_text = diff_font.render(f"Level {self.pipe_manager.difficulty_level}", True, PURPLE)
            screen.blit(diff_text, (SCREEN_WIDTH - 250, 30))

        fps_font = pygame.font.Font(None, 50)
        fps_color = WHITE if self.current_fps >= 50 else RED
        fps_text = fps_font.render(f"FPS: {self.current_fps}", True, fps_color)
        screen.blit(fps_text, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 50))
        if not self.game_started:
            hint_text = self.title_font.render("SPACE / CLICK", True, WHITE)
            hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(hint_text, hint_rect)
            hint2_text = self.title_font.render("to FLY!", True, HOT_PINK)
            hint2_rect = hint2_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(hint2_text, hint2_rect)

    def _create_background_surface(self):
        bg_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))
        location_data = LOCATIONS.get(self.current_location, LOCATIONS["default"])
        colors = location_data["colors"]

        for y in range(SCREEN_HEIGHT - GROUND_HEIGHT):
            ratio = y / (SCREEN_HEIGHT - GROUND_HEIGHT)
            r = int(colors[0][0] + (colors[1][0] - colors[0][0]) * ratio)
            g = int(colors[0][1] + (colors[1][1] - colors[0][1]) * ratio)
            b = int(colors[0][2] + (colors[1][2] - colors[0][2]) * ratio)
            pygame.draw.line(bg_surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        return bg_surface

    def _render_background(self, screen):
        screen.blit(self.background_surface, (0, 0))

    def _render_ground(self, screen):
        ground_y = SCREEN_HEIGHT - GROUND_HEIGHT
        pygame.draw.rect(screen, DARK_PINK, (0, ground_y, SCREEN_WIDTH, GROUND_HEIGHT))
        pygame.draw.rect(screen, HOT_PINK, (0, ground_y, SCREEN_WIDTH, 5))
        heart_spacing = 100
        for x in range(0, SCREEN_WIDTH, heart_spacing):
            self._draw_heart(screen, x + 50, ground_y + 50, 20)

    def _draw_heart(self, screen, x, y, size):
        pygame.draw.circle(screen, HOT_PINK, (x - size//2, y), size//2)
        pygame.draw.circle(screen, HOT_PINK, (x + size//2, y), size//2)
        points = [(x - size, y), (x, y + size), (x + size, y)]
        pygame.draw.polygon(screen, HOT_PINK, points)

    def _show_screamer(self):
        screen = self.game_manager.screen
        current_screen = screen.copy()
        try:
            barbie_sprite = pygame.image.load("assets/images/barbi.gif").convert_alpha()
            screamer_size = min(SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT)
        except:
            barbie_sprite = None
            screamer_size = 400
        for i in range(10):
            flash = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            flash.fill((255, 0, 0))
            flash.set_alpha(200 - i * 20)
            screen.blit(current_screen, (0, 0))
            screen.blit(flash, (0, 0))
            if barbie_sprite:
                scale_factor = 0.5 + (i / 10) * 0.5
                scaled_size = int(screamer_size * scale_factor)
                scaled_barbie = pygame.transform.scale(barbie_sprite, (scaled_size, scaled_size))
                shake_x = random.randint(-10, 10)
                shake_y = random.randint(-10, 10)
                x = (SCREEN_WIDTH - scaled_size) // 2 + shake_x
                y = (SCREEN_HEIGHT - GROUND_HEIGHT - scaled_size) // 2 + shake_y
                screen.blit(scaled_barbie, (x, y))
            else:
                screamer_font = pygame.font.Font(None, 400)
                text = screamer_font.render("GAME OVER!", True, (255, 255, 255))
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                shake_x = random.randint(-15, 15)
                shake_y = random.randint(-15, 15)
                text_rect.x += shake_x
                text_rect.y += shake_y
                screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.wait(80)
