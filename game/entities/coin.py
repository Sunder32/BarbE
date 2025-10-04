
import pygame
import random
import math
from game.constants import *
from game.sound_generator import play_sound


class Coin:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collected = False
        self.animation_time = 0
        self.bob_offset = random.uniform(0, math.pi * 2)

        try:
            self.image = pygame.image.load("assets/images/money.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (COIN_SIZE, COIN_SIZE))
        except:
            self.image = pygame.Surface((COIN_SIZE, COIN_SIZE), pygame.SRCALPHA)
            pygame.draw.circle(self.image, GOLD, (COIN_SIZE//2, COIN_SIZE//2), COIN_SIZE//2)
            pygame.draw.circle(self.image, (255, 255, 0), (COIN_SIZE//2, COIN_SIZE//2), COIN_SIZE//2 - 5, 3)

        self.original_image = self.image.copy()

    def update(self, dt):
        if not self.collected:
            self.animation_time += dt * 3

            self.bob_offset += dt * 2

    def render(self, screen):
        if not self.collected:
            bob_y = math.sin(self.bob_offset) * 10

            scale = abs(math.sin(self.animation_time)) * 0.3 + 0.7
            scaled_width = int(COIN_SIZE * scale)
            scaled_image = pygame.transform.scale(self.original_image, (scaled_width, COIN_SIZE))

            glow_surf = pygame.Surface((COIN_SIZE + 20, COIN_SIZE + 20), pygame.SRCALPHA)
            glow_alpha = int(abs(math.sin(self.animation_time * 2)) * 100 + 50)
            pygame.draw.circle(glow_surf, (*GOLD[:3], glow_alpha),
                             (COIN_SIZE//2 + 10, COIN_SIZE//2 + 10), COIN_SIZE//2 + 10)

            screen.blit(glow_surf, (self.x - scaled_width//2 - 10, self.y + bob_y - 10))
            screen.blit(scaled_image, (self.x - scaled_width//2, self.y + bob_y))

    def check_collision(self, barbie):
        if self.collected:
            return False

        distance = math.sqrt((self.x - barbie.x)**2 + (self.y - barbie.y)**2)
        return distance < COIN_COLLECT_RADIUS


class CoinManager:

    def __init__(self):
        self.coins = []
        self.collected_count = 0

    def spawn_coin(self, x, y):
        coin = Coin(x, y)
        self.coins.append(coin)

    def update(self, dt, barbie):
        for coin in self.coins[:]:
            coin.update(dt)

            if coin.check_collision(barbie):
                coin.collected = True
                self.collected_count += 1
                play_sound('score')
                self.coins.remove(coin)

            elif coin.x < -100:
                self.coins.remove(coin)

    def render(self, screen):
        for coin in self.coins:
            coin.render(screen)

    def reset(self):
        self.coins.clear()
        self.collected_count = 0
