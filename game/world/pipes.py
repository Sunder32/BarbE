
import pygame
import random
from game.constants import *
from game.sound_generator import play_sound


class Pipe:

    def __init__(self, x):
        self.x = x
        self.width = PIPE_WIDTH

        self.gap_y = random.randint(150, SCREEN_HEIGHT - GROUND_HEIGHT - 150)

        self.top_height = self.gap_y - PIPE_GAP // 2
        self.bottom_y = self.gap_y + PIPE_GAP // 2
        self.bottom_height = SCREEN_HEIGHT - GROUND_HEIGHT - self.bottom_y

        self.top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        self.bottom_rect = pygame.Rect(self.x, self.bottom_y, self.width, self.bottom_height)

        self.passed = False

        try:
            self.pipe_sprite = pygame.image.load("assets/images/closet.png").convert_alpha()
            self.has_sprite = True
        except:
            self.has_sprite = False

    def update(self, dt, speed=None):
        if speed is None:
            speed = PIPE_SPEED
        self.x -= speed * dt

        self.top_rect.x = int(self.x)
        self.bottom_rect.x = int(self.x)

    def is_off_screen(self):
        return self.x + self.width < 0

    def collides_with(self, barbie_rect):
        return barbie_rect.colliderect(self.top_rect) or barbie_rect.colliderect(self.bottom_rect)

    def render(self, screen):
        if self.has_sprite:
            try:
                top_sprite = pygame.transform.scale(self.pipe_sprite, (self.width, int(self.top_height)))
                screen.blit(top_sprite, (int(self.x), 0))

                bottom_sprite = pygame.transform.scale(self.pipe_sprite, (self.width, int(self.bottom_height)))
                screen.blit(bottom_sprite, (int(self.x), int(self.bottom_y)))
            except:
                self._render_fallback(screen)
        else:
            self._render_fallback(screen)

        self._render_stars(screen)

    def _render_fallback(self, screen):
        pygame.draw.rect(screen, PURPLE, (int(self.x), 0, self.width, int(self.top_height)))
        pygame.draw.rect(screen, DARK_PINK, (int(self.x), 0, self.width, int(self.top_height)), 3)

        pygame.draw.rect(screen, PURPLE, (int(self.x), int(self.bottom_y), self.width, int(self.bottom_height)))
        pygame.draw.rect(screen, DARK_PINK, (int(self.x), int(self.bottom_y), self.width, int(self.bottom_height)), 3)

    def _render_stars(self, screen):
        star_y = self.gap_y
        for i in range(3):
            offset_x = (i - 1) * 25
            self._draw_star(screen, int(self.x + self.width // 2 + offset_x), int(star_y), 8)

    def _draw_star(self, screen, x, y, size):
        points = []
        for i in range(10):
            angle = i * 36 * 3.14159 / 180
            r = size if i % 2 == 0 else size // 2
            px = x + int(r * pygame.math.Vector2(1, 0).rotate_rad(angle).x)
            py = y + int(r * pygame.math.Vector2(1, 0).rotate_rad(angle).y)
            points.append((px, py))
        pygame.draw.polygon(screen, GOLD, points)


class PipeManager:

    def __init__(self):
        self.pipes = []
        self.spawn_timer = 0
        self.spawn_delay = PIPE_SPACING / PIPE_SPEED
        self.score = 0

        self.current_speed = PIPE_SPEED
        self.current_gap = PIPE_GAP
        self.difficulty_level = 1

    def reset(self):
        self.pipes = []
        self.spawn_timer = 0
        self.score = 0
        self.current_speed = PIPE_SPEED
        self.current_gap = PIPE_GAP
        self.difficulty_level = 1

    def update(self, dt, barbie):
        if self.score > 0 and self.score % 5 == 0:
            new_level = (self.score // 5) + 1
            if new_level > self.difficulty_level:
                self.difficulty_level = new_level
                self._increase_difficulty()

        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_timer = 0
            new_pipe = Pipe(SCREEN_WIDTH)
            new_pipe.gap_y = random.randint(150, SCREEN_HEIGHT - GROUND_HEIGHT - 150)
            new_pipe.top_height = new_pipe.gap_y - self.current_gap // 2
            new_pipe.bottom_y = new_pipe.gap_y + self.current_gap // 2
            new_pipe.bottom_height = SCREEN_HEIGHT - GROUND_HEIGHT - new_pipe.bottom_y
            new_pipe.top_rect = pygame.Rect(new_pipe.x, 0, new_pipe.width, new_pipe.top_height)
            new_pipe.bottom_rect = pygame.Rect(new_pipe.x, new_pipe.bottom_y, new_pipe.width, new_pipe.bottom_height)
            self.pipes.append(new_pipe)

        for pipe in self.pipes[:]:
            pipe.update(dt, self.current_speed)

            if pipe.is_off_screen():
                self.pipes.remove(pipe)

            if not pipe.passed and pipe.x + pipe.width < barbie.x:
                pipe.passed = True
                self.score += 1
                play_sound('score')

            if barbie.is_alive and pipe.collides_with(barbie.rect):
                barbie.is_alive = False

    def _increase_difficulty(self):
        self.current_speed = min(PIPE_SPEED + (self.difficulty_level - 1) * 15, 250)

        self.current_gap = max(PIPE_GAP - (self.difficulty_level - 1) * 10, 120)

        self.spawn_delay = PIPE_SPACING / self.current_speed

        play_sound('levelup')

    def render(self, screen):
        for pipe in self.pipes:
            pipe.render(screen)
