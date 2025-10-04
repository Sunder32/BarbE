
import pygame
import json
import os
import time
from game.constants import *
from game.states.menu_state import MenuState
from game.states.playing_state import PlayingState
from game.states.game_over_state import GameOverState


class GameManager:

    def __init__(self, screen):
        self.screen = screen
        self.current_state = None
        self.states = {}
        self.score = 0
        self.game_start_time = 0

        self.states[GAME_STATE_MENU] = MenuState(self)
        self.states[GAME_STATE_PLAYING] = PlayingState(self)
        self.states[GAME_STATE_GAME_OVER] = GameOverState(self)

        self.change_state(GAME_STATE_MENU)

    def update_stats_on_death(self):
        try:
            stats_file = "stats.json"
            if os.path.exists(stats_file):
                with open(stats_file, 'r') as f:
                    stats = json.load(f)
            else:
                stats = {
                    "high_score": 0,
                    "total_games": 0,
                    "total_deaths": 0,
                    "total_time_played": 0
                }

            stats["total_games"] += 1
            stats["total_deaths"] += 1

            if self.score > stats["high_score"]:
                stats["high_score"] = self.score
                print(f"🏆 НОВЫЙ РЕКОРД: {self.score}!")

            if self.game_start_time > 0:
                play_time = int(time.time() - self.game_start_time)
                stats["total_time_played"] += play_time

            with open(stats_file, 'w') as f:
                json.dump(stats, f, indent=4)

            print(f"📊 Статистика обновлена! Игр: {stats['total_games']}, Рекорд: {stats['high_score']}")

        except Exception as e:
            print(f"⚠️ Ошибка сохранения статистики: {e}")

    def change_state(self, state_name):
        if self.current_state:
            self.current_state.exit()

        if state_name == GAME_STATE_PLAYING:
            self.game_start_time = time.time()
            self.score = 0

        if state_name == GAME_STATE_GAME_OVER:
            self.update_stats_on_death()

        self.current_state = self.states.get(state_name)

        if self.current_state:
            self.current_state.enter()

    def handle_event(self, event):
        if self.current_state:
            self.current_state.handle_event(event)

    def update(self, dt):
        if self.current_state:
            self.current_state.update(dt)

    def render(self):
        if self.current_state:
            self.current_state.render(self.screen)
