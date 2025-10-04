
import pygame
import math
import random
from game.constants import *
from game.sound_generator import play_sound


class FlappyBarbie:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = BARBIE_SIZE
        self.height = BARBIE_SIZE
        self.rect = pygame.Rect(x - self.width//2, y - self.height//2, self.width, self.height)

        self.velocity_y = 0
        self.rotation = 0
        self.is_alive = True

        # СУПЕР МЕГА ПРАЙМ ЭФФЕКТЫ!
        self.trail = []
        self.sparkle_timer = 0
        self.sparkles = []
        self.glow_pulse = 0

        try:
            self.sprite = pygame.image.load("assets/images/barbi.gif").convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))
            self.has_sprite = True
        except:
            self.sprite = None
            self.has_sprite = False

    def flap(self):
        if self.is_alive:
            self.velocity_y = FLAP_STRENGTH
            play_sound('flap')

    def update(self, dt):
        if not self.is_alive:
            return

        self.velocity_y += GRAVITY * dt

        if self.velocity_y > MAX_FALL_SPEED:
            self.velocity_y = MAX_FALL_SPEED

        self.y += self.velocity_y * dt

        # СУПЕР МЕГА ПРАЙМ ЭФФЕКТЫ!
        self.trail.append((int(self.x), int(self.y), self.rotation))
        if len(self.trail) > TRAIL_LENGTH:
            self.trail.pop(0)

        self.sparkle_timer += dt
        if self.sparkle_timer >= SPARKLE_INTERVAL:
            self.sparkle_timer = 0
            self._create_sparkle()

        for sparkle in self.sparkles[:]:
            sparkle['life'] -= dt
            sparkle['y'] -= sparkle['speed'] * dt
            if sparkle['life'] <= 0:
                self.sparkles.remove(sparkle)

        self.glow_pulse += dt * 5
        if self.glow_pulse > 2 * math.pi:
            self.glow_pulse = 0

        self.rotation = -self.velocity_y / 10
        if self.rotation > 25:
            self.rotation = 25
        if self.rotation < -90:
            self.rotation = -90

        self.rect.x = int(self.x - self.width // 2)
        self.rect.y = int(self.y - self.height // 2)

        if self.y > SCREEN_HEIGHT - GROUND_HEIGHT:
            self.y = SCREEN_HEIGHT - GROUND_HEIGHT
            self.is_alive = False
        if self.y < 0:
            self.y = 0
            self.velocity_y = 0

    def reset(self):
        self.y = BARBIE_START_Y
        self.velocity_y = 0
        self.rotation = 0
        self.is_alive = True
        self.trail = []
        self.sparkles = []
        self.sparkle_timer = 0
        self.glow_pulse = 0

    def _create_sparkle(self):
        sparkle = {
            'x': self.x + random.randint(-10, 10),
            'y': self.y + random.randint(-10, 10),
            'life': random.uniform(0.3, 0.6),
            'speed': random.randint(20, 50),
            'size': random.randint(2, 5),
            'color': random.choice([GOLD, LIGHT_PINK, WHITE, HOT_PINK])
        }
        self.sparkles.append(sparkle)

    def render(self, screen):
        # СУПЕР МЕГА ПРАЙМ ЭФФЕКТЫ!
        self._render_trail(screen)

        self._render_glow(screen)

        if self.has_sprite and self.sprite:
            rotated_sprite = pygame.transform.rotate(self.sprite, self.rotation)
            rotated_rect = rotated_sprite.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(rotated_sprite, rotated_rect.topleft)
        else:
            pygame.draw.circle(screen, HOT_PINK, (int(self.x), int(self.y)), self.width // 2)
            eye_offset_x = 8
            eye_offset_y = -5
            pygame.draw.circle(screen, BLACK,
                             (int(self.x - eye_offset_x), int(self.y + eye_offset_y)), 3)
            pygame.draw.circle(screen, BLACK,
                             (int(self.x + eye_offset_x), int(self.y + eye_offset_y)), 3)

        self._render_sparkles(screen)

    def _render_trail(self, screen):
        for i, (tx, ty, rot) in enumerate(self.trail):
            alpha = int(255 * (i / len(self.trail))) if self.trail else 0
            size = int(self.width * (0.5 + 0.5 * i / len(self.trail))) if self.trail else 0
            color = (*HOT_PINK, alpha)
            trail_surf = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(trail_surf, color, (size//2, size//2), size//2)
            screen.blit(trail_surf, (tx - size//2, ty - size//2))

    def _render_glow(self, screen):
        pulse = abs(math.sin(self.glow_pulse))
        glow_size = int(self.width * (1.5 + 0.5 * pulse))
        alpha = int(100 * pulse)

        glow_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*GOLD, alpha), (glow_size//2, glow_size//2), glow_size//2)
        screen.blit(glow_surf, (int(self.x - glow_size//2), int(self.y - glow_size//2)))

        inner_size = glow_size // 2
        inner_surf = pygame.Surface((inner_size, inner_size), pygame.SRCALPHA)
        pygame.draw.circle(inner_surf, (*HOT_PINK, alpha * 2), (inner_size//2, inner_size//2), inner_size//2)
        screen.blit(inner_surf, (int(self.x - inner_size//2), int(self.y - inner_size//2)))

    def _render_sparkles(self, screen):
        for sparkle in self.sparkles:
            alpha = int(255 * (sparkle['life'] / 0.6))
            size = sparkle['size']
            color = (*sparkle['color'][:3], alpha)

            x, y = int(sparkle['x']), int(sparkle['y'])
            points = []
            for i in range(8):
                angle = i * 45 * math.pi / 180
                r = size if i % 2 == 0 else size // 2
                px = x + int(r * math.cos(angle))
                py = y + int(r * math.sin(angle))
                points.append((px, py))

            sparkle_surf = pygame.Surface((size*3, size*3), pygame.SRCALPHA)
            offset_points = [(p[0] - x + size*1.5, p[1] - y + size*1.5) for p in points]
            if len(offset_points) >= 3:
                pygame.draw.polygon(sparkle_surf, color, offset_points)
            screen.blit(sparkle_surf, (x - size*1.5, y - size*1.5))
