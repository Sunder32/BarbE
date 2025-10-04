
import pygame
import json
import os
from game.states.base_state import BaseState
from game.constants import *
from game.sound_generator import play_sound


class MenuState(BaseState):

    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.title_font = None
        self.menu_font = None
        self.small_font = None

        self.tabs = ["PLAY", "STATS", "SHOP", "SETTINGS"]
        self.current_tab = 0

        self.play_options = ["START GAME", "EXIT GAME"]
        self.stats_options = ["RESET STATS", "BACK TO MENU"]
        self.shop_tabs = ["SKINS", "LOCATIONS"]
        self.current_shop_tab = 0
        self.shop_scroll = 0
        self.settings_options = ["SOUND: ON", "FULLSCREEN: OFF", "BACK TO MENU"]

        self.selected_option = 0

        self.stats = self.load_stats()

        self.sound_enabled = True
        self.fullscreen_enabled = False

        self.shop_data = self.load_shop_data()
        self.total_coins = self.shop_data.get("coins", 0)
        self.owned_skins = self.shop_data.get("owned_skins", ["default"])
        self.owned_locations = self.shop_data.get("owned_locations", ["default"])
        self.current_skin = self.shop_data.get("current_skin", "default")
        self.current_location = self.shop_data.get("current_location", "default")

        self.animation_offset = 0
        self.animation_direction = 1

    def load_stats(self):
        stats_file = "stats.json"
        default_stats = {
            "high_score": 0,
            "total_games": 0,
            "total_deaths": 0,
            "total_time_played": 0
        }

        try:
            if os.path.exists(stats_file):
                with open(stats_file, 'r') as f:
                    return json.load(f)
        except:
            pass

        return default_stats

    def save_stats(self):
        try:
            with open("stats.json", 'w') as f:
                json.dump(self.stats, f, indent=4)
        except:
            pass

    def reset_stats(self):
        self.stats = {
            "high_score": 0,
            "total_games": 0,
            "total_deaths": 0,
            "total_time_played": 0
        }
        self.save_stats()

    def load_shop_data(self):
        shop_file = "shop.json"
        default_data = {
            "coins": 0,
            "owned_skins": ["default"],
            "owned_locations": ["default"],
            "current_skin": "default",
            "current_location": "default"
        }

        try:
            if os.path.exists(shop_file):
                with open(shop_file, 'r') as f:
                    return json.load(f)
        except:
            pass

        return default_data

    def save_shop_data(self):
        shop_data = {
            "coins": self.total_coins,
            "owned_skins": self.owned_skins,
            "owned_locations": self.owned_locations,
            "current_skin": self.current_skin,
            "current_location": self.current_location
        }

        try:
            with open("shop.json", 'w') as f:
                json.dump(shop_data, f, indent=4)
        except:
            pass

    def add_coins(self, amount):
        self.total_coins += amount
        self.save_shop_data()

    def buy_item(self, item_type, item_id):
        if item_type == "skin":
            item_data = SKINS.get(item_id)
            if item_id not in self.owned_skins:
                if self.total_coins >= item_data["price"]:
                    self.total_coins -= item_data["price"]
                    self.owned_skins.append(item_id)
                    self.current_skin = item_id
                    self.save_shop_data()
                    play_sound('levelup')
                    return True
        elif item_type == "location":
            item_data = LOCATIONS.get(item_id)
            if item_id not in self.owned_locations:
                if self.total_coins >= item_data["price"]:
                    self.total_coins -= item_data["price"]
                    self.owned_locations.append(item_id)
                    self.current_location = item_id
                    self.save_shop_data()
                    play_sound('levelup')
                    return True
        return False

    def select_item(self, item_type, item_id):
        if item_type == "skin" and item_id in self.owned_skins:
            self.current_skin = item_id
            self.save_shop_data()
            play_sound('menu_select')
        elif item_type == "location" and item_id in self.owned_locations:
            self.current_location = item_id
            self.save_shop_data()
            play_sound('menu_select')

    def enter(self):
        self.title_font = pygame.font.Font(None, 180)
        self.menu_font = pygame.font.Font(None, 120)
        self.small_font = pygame.font.Font(None, 70)
        self.selected_option = 0
        self.current_tab = 0
        self.current_shop_tab = 0
        self.shop_scroll = 0
        self.stats = self.load_stats()
        self.shop_data = self.load_shop_data()
        self.total_coins = self.shop_data.get("coins", 0)
        self.owned_skins = self.shop_data.get("owned_skins", ["default"])
        self.owned_locations = self.shop_data.get("owned_locations", ["default"])
        self.current_skin = self.shop_data.get("current_skin", "default")
        self.current_location = self.shop_data.get("current_location", "default")

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.current_tab == 2:
                self._handle_shop_event(event)
                return

            if event.key == pygame.K_LEFT:
                self.current_tab = (self.current_tab - 1) % len(self.tabs)
                self.selected_option = 0
                play_sound('menu_move')
            elif event.key == pygame.K_RIGHT:
                self.current_tab = (self.current_tab + 1) % len(self.tabs)
                self.selected_option = 0
                play_sound('menu_move')

            elif event.key == pygame.K_UP:
                options = self.get_current_options()
                self.selected_option = (self.selected_option - 1) % len(options)
                play_sound('menu_move')
            elif event.key == pygame.K_DOWN:
                options = self.get_current_options()
                self.selected_option = (self.selected_option + 1) % len(options)
                play_sound('menu_move')

            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                play_sound('menu_select')
                self.select_option()

    def _handle_shop_event(self, event):
        if event.key == pygame.K_LEFT:
            self.current_shop_tab = (self.current_shop_tab - 1) % len(self.shop_tabs)
            self.shop_scroll = 0
            play_sound('menu_move')
        elif event.key == pygame.K_RIGHT:
            self.current_shop_tab = (self.current_shop_tab + 1) % len(self.shop_tabs)
            self.shop_scroll = 0
            play_sound('menu_move')
        elif event.key == pygame.K_UP:
            self.shop_scroll = max(0, self.shop_scroll - 1)
            play_sound('menu_move')
        elif event.key == pygame.K_DOWN:
            if self.current_shop_tab == 0:
                max_scroll = len(SKINS) - 1
            else:
                max_scroll = len(LOCATIONS) - 1
            self.shop_scroll = min(max_scroll, self.shop_scroll + 1)
            play_sound('menu_move')
        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            self._handle_shop_purchase()
        elif event.key == pygame.K_ESCAPE:
            self.current_tab = 0
            self.selected_option = 0
            play_sound('menu_move')

    def _handle_shop_purchase(self):
        if self.current_shop_tab == 0:
            skin_ids = list(SKINS.keys())
            selected_skin = skin_ids[self.shop_scroll]

            if selected_skin in self.owned_skins:
                self.select_item("skin", selected_skin)
            else:
                if self.buy_item("skin", selected_skin):
                    pass
                else:
                    play_sound('death')
        else:
            location_ids = list(LOCATIONS.keys())
            selected_location = location_ids[self.shop_scroll]

            if selected_location in self.owned_locations:
                self.select_item("location", selected_location)
            else:
                if self.buy_item("location", selected_location):
                    pass
                else:
                    play_sound('death')

    def get_current_options(self):
        if self.current_tab == 0:
            return self.play_options
        elif self.current_tab == 1:
            return self.stats_options
        else:
            return self.settings_options

    def select_option(self):
        options = self.get_current_options()
        selected = options[self.selected_option]

        if selected == "START GAME":
            self.game_manager.change_state(GAME_STATE_PLAYING)

        elif selected == "EXIT GAME":
            pygame.event.post(pygame.event.Event(pygame.QUIT))

        elif selected == "RESET STATS":
            self.reset_stats()
            play_sound('menu_select')

        elif selected.startswith("SOUND:"):
            self.sound_enabled = not self.sound_enabled
            self.settings_options[0] = f"SOUND: {'ON' if self.sound_enabled else 'OFF'}"
            if self.sound_enabled:
                pygame.mixer.set_num_channels(8)
            else:
                pygame.mixer.stop()
            play_sound('menu_select')

        elif selected.startswith("FULLSCREEN:"):
            self.fullscreen_enabled = not self.fullscreen_enabled
            self.settings_options[1] = f"FULLSCREEN: {'ON' if self.fullscreen_enabled else 'OFF'}"
            pygame.display.toggle_fullscreen()

        elif selected == "BACK TO MENU":
            self.current_tab = 0
            self.selected_option = 0

    def update(self, dt):
        self.animation_offset += self.animation_direction * 0.5
        if abs(self.animation_offset) > 10:
            self.animation_direction *= -1

    def render(self, screen):
        self._render_background(screen)

        self._render_title(screen)

        self._render_tabs(screen)

        if self.current_tab == 0:
            self._render_play_tab(screen)
        elif self.current_tab == 1:
            self._render_stats_tab(screen)
        elif self.current_tab == 2:
            self._render_shop_tab(screen)
        else:
            self._render_settings_tab(screen)

        self._render_hints(screen)

    def _render_background(self, screen):
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(255 - 100 * ratio)
            g = int(192 - 100 * ratio)
            b = int(203 - 50 * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        for i in range(5):
            x = (i * 100 + int(self.animation_offset * 2)) % (SCREEN_WIDTH + 100)
            y = 50 + i * 120
            radius = 30 + i * 10
            color = (255, 182, 193, 30)
            pygame.draw.circle(screen, LIGHT_PINK, (x, y), radius, 2)

    def _render_title(self, screen):
        shadow = self.title_font.render("💖 FLAPPY BARBIE 💖", True, (139, 0, 139))
        shadow_rect = shadow.get_rect(center=(SCREEN_WIDTH // 2 + 5, 105 + int(self.animation_offset)))
        screen.blit(shadow, shadow_rect)

        title = self.title_font.render("💖 FLAPPY BARBIE 💖", True, HOT_PINK)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100 + int(self.animation_offset)))
        screen.blit(title, title_rect)

        version = self.small_font.render("v2.3 - Pink Edition", True, WHITE)
        version_rect = version.get_rect(center=(SCREEN_WIDTH // 2, 220))
        screen.blit(version, version_rect)

    def _render_tabs(self, screen):
        tab_y = 300
        tab_width = SCREEN_WIDTH // len(self.tabs)

        for i, tab in enumerate(self.tabs):
            x = i * tab_width

            if i == self.current_tab:
                color = HOT_PINK
                text_color = WHITE
                pygame.draw.rect(screen, color, (x, tab_y, tab_width, 80))
                pygame.draw.rect(screen, GOLD, (x, tab_y, tab_width, 80), 4)
            else:
                color = PURPLE
                text_color = LIGHT_PINK
                pygame.draw.rect(screen, color, (x, tab_y, tab_width, 80))

            text = self.menu_font.render(tab, True, text_color)
            text_rect = text.get_rect(center=(x + tab_width // 2, tab_y + 40))
            screen.blit(text, text_rect)

    def _render_play_tab(self, screen):
        start_y = 550

        for i, option in enumerate(self.play_options):
            y = start_y + i * 150

            if i == self.selected_option:
                button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 300, y - 50, 600, 110)
                pygame.draw.rect(screen, GOLD, button_rect, 0, 20)
                pygame.draw.rect(screen, HOT_PINK, button_rect, 5, 20)

                arrow_left = self.menu_font.render("►", True, HOT_PINK)
                arrow_right = self.menu_font.render("◄", True, HOT_PINK)
                screen.blit(arrow_left, (SCREEN_WIDTH // 2 - 380, y - 30))
                screen.blit(arrow_right, (SCREEN_WIDTH // 2 + 320, y - 30))

                text_color = DARK_PINK
            else:
                button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 300, y - 50, 600, 110)
                pygame.draw.rect(screen, LIGHT_PINK, button_rect, 0, 20)
                pygame.draw.rect(screen, PURPLE, button_rect, 3, 20)
                text_color = PURPLE

            text = self.menu_font.render(option, True, text_color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            screen.blit(text, text_rect)

        if self.stats["high_score"] > 0:
            record_text = self.small_font.render(f"🏆 Best Score: {self.stats['high_score']}", True, GOLD)
            record_rect = record_text.get_rect(center=(SCREEN_WIDTH // 2, 920))
            screen.blit(record_text, record_rect)

    def _render_stats_tab(self, screen):
        start_y = 480

        stats_data = [
            ("🏆 High Score", self.stats["high_score"]),
            ("🎮 Total Games", self.stats["total_games"]),
            ("💀 Total Deaths", self.stats["total_deaths"]),
            ("⏱️ Time Played", f"{self.stats['total_time_played']}s"),
        ]

        for i, (label, value) in enumerate(stats_data):
            y = start_y + i * 90

            stat_rect = pygame.Rect(100, y - 30, SCREEN_WIDTH - 200, 70)
            pygame.draw.rect(screen, LIGHT_PINK, stat_rect, 0, 15)
            pygame.draw.rect(screen, HOT_PINK, stat_rect, 3, 15)

            label_text = self.small_font.render(label, True, PURPLE)
            value_text = self.small_font.render(str(value), True, DARK_PINK)

            screen.blit(label_text, (150, y - 10))
            screen.blit(value_text, (SCREEN_WIDTH - 300, y - 10))

        button_y = 860
        for i, option in enumerate(self.stats_options):
            y = button_y + i * 100

            if i == self.selected_option:
                color = GOLD
                text_color = DARK_PINK
            else:
                color = PURPLE
                text_color = LIGHT_PINK

            button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 250, y - 40, 500, 80)
            pygame.draw.rect(screen, color, button_rect, 0, 15)

            text = self.small_font.render(option, True, text_color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            screen.blit(text, text_rect)

    def _render_shop_tab(self, screen):
        coin_text = self.menu_font.render(f"💰 {self.total_coins} монет", True, GOLD)
        coin_rect = coin_text.get_rect(center=(SCREEN_WIDTH // 2, 270))
        screen.blit(coin_text, coin_rect)

        shop_tab_y = 360
        shop_tab_width = 400
        shop_tab_x_start = SCREEN_WIDTH // 2 - shop_tab_width

        for i, tab in enumerate(self.shop_tabs):
            x = shop_tab_x_start + i * shop_tab_width

            if i == self.current_shop_tab:
                color = GOLD
                text_color = DARK_PINK
                border = 5
            else:
                color = LIGHT_PINK
                text_color = PURPLE
                border = 2

            tab_rect = pygame.Rect(x, shop_tab_y, shop_tab_width, 60)
            pygame.draw.rect(screen, color, tab_rect, 0, 10)
            pygame.draw.rect(screen, HOT_PINK, tab_rect, border, 10)

            text = self.small_font.render(tab, True, text_color)
            text_rect = text.get_rect(center=(x + shop_tab_width // 2, shop_tab_y + 30))
            screen.blit(text, text_rect)

        start_y = 480

        if self.current_shop_tab == 0:
            self._render_shop_items(screen, SKINS, "skin", start_y)
        else:
            self._render_shop_items(screen, LOCATIONS, "location", start_y)

    def _render_shop_items(self, screen, items_dict, item_type, start_y):
        item_ids = list(items_dict.keys())

        visible_start = max(0, self.shop_scroll - 1)
        visible_end = min(len(item_ids), visible_start + 3)

        for i in range(visible_start, visible_end):
            item_id = item_ids[i]
            item_data = items_dict[item_id]
            y = start_y + (i - visible_start) * 160

            if item_type == "skin":
                owned = item_id in self.owned_skins
                selected = item_id == self.current_skin
            else:
                owned = item_id in self.owned_locations
                selected = item_id == self.current_location

            if i == self.shop_scroll:
                border_color = GOLD
                bg_color = (255, 240, 200)
            else:
                border_color = PURPLE
                bg_color = LIGHT_PINK

            card_rect = pygame.Rect(SCREEN_WIDTH // 2 - 450, y - 60, 900, 140)
            pygame.draw.rect(screen, bg_color, card_rect, 0, 15)
            pygame.draw.rect(screen, border_color, card_rect, 4, 15)

            name_text = self.small_font.render(item_data["name"], True, DARK_PINK if i == self.shop_scroll else PURPLE)
            screen.blit(name_text, (SCREEN_WIDTH // 2 - 420, y - 40))

            if owned:
                if selected:
                    status_text = self.small_font.render("✓ ВЫБРАНО", True, GREEN)
                else:
                    status_text = self.small_font.render("КУПЛ  ЕНО - НАЖМИ ENTER", True, HOT_PINK)
            else:
                price_text = self.small_font.render(f"💰 {item_data['price']} монет", True, GOLD)
                status_text = price_text

            screen.blit(status_text, (SCREEN_WIDTH // 2 - 420, y + 10))

        if self.shop_scroll > 0:
            arrow_up = self.menu_font.render("▲", True, HOT_PINK)
            screen.blit(arrow_up, (SCREEN_WIDTH // 2 - 60, start_y - 100))

        if self.shop_scroll < len(item_ids) - 1:
            arrow_down = self.menu_font.render("▼", True, HOT_PINK)
            screen.blit(arrow_down, (SCREEN_WIDTH // 2 - 60, start_y + 400))

    def _render_settings_tab(self, screen):
        start_y = 550

        for i, option in enumerate(self.settings_options):
            y = start_y + i * 140

            if i == self.selected_option:
                button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 300, y - 50, 600, 110)
                pygame.draw.rect(screen, GOLD, button_rect, 0, 20)
                pygame.draw.rect(screen, HOT_PINK, button_rect, 5, 20)
                text_color = DARK_PINK

                if "BACK" not in option:
                    arrow_left = self.small_font.render("◄", True, HOT_PINK)
                    arrow_right = self.small_font.render("►", True, HOT_PINK)
                    screen.blit(arrow_left, (SCREEN_WIDTH // 2 - 380, y - 20))
                    screen.blit(arrow_right, (SCREEN_WIDTH // 2 + 320, y - 20))
            else:
                button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 300, y - 50, 600, 110)
                pygame.draw.rect(screen, LIGHT_PINK, button_rect, 0, 20)
                pygame.draw.rect(screen, PURPLE, button_rect, 3, 20)
                text_color = PURPLE

            text = self.small_font.render(option, True, text_color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            screen.blit(text, text_rect)

    def _render_hints(self, screen):
        hints = [
            "← → Switch Tabs",
            "↑ ↓ Navigate",
            "ENTER Select",
            "F11 Fullscreen"
        ]

        hint_y = SCREEN_HEIGHT - 40
        hint_x = 20

        for hint in hints:
            text = pygame.font.Font(None, 50).render(hint, True, WHITE)
            screen.blit(text, (hint_x, hint_y))
            hint_x += 120
