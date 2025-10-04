
import pygame
import random
import math
from game.constants import *


class ParticleSystem:

    def __init__(self):
        self.particles = []
        self._create_particles()

    def _create_particles(self):
        for _ in range(PARTICLE_COUNT):
            particle = {
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT - GROUND_HEIGHT),
                'speed': random.uniform(10, 30),
                'size': random.randint(1, 3),
                'color': random.choice([LIGHT_PINK, WHITE, GOLD, PURPLE]),
                'alpha': random.randint(50, 150),
                'pulse': random.uniform(0, math.pi * 2)
            }
            self.particles.append(particle)

    def update(self, dt):
        for particle in self.particles:
            particle['x'] -= particle['speed'] * dt

            particle['pulse'] += dt * 2
            if particle['pulse'] > 2 * math.pi:
                particle['pulse'] = 0

            if particle['x'] < -10:
                particle['x'] = SCREEN_WIDTH + 10
                particle['y'] = random.randint(0, SCREEN_HEIGHT - GROUND_HEIGHT)

    def render(self, screen):
        for particle in self.particles:
            pulse = abs(math.sin(particle['pulse']))
            alpha = int(particle['alpha'] * pulse)
            size = int(particle['size'] * (0.5 + 0.5 * pulse))

            particle_surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
            color = (*particle['color'][:3], alpha)
            pygame.draw.circle(particle_surf, color, (size, size), size)
            screen.blit(particle_surf, (int(particle['x']) - size, int(particle['y']) - size))


class BackgroundStars:

    def __init__(self):
        self.stars = []
        self._create_stars()

    def _create_stars(self):
        for _ in range(STAR_COUNT):
            star = {
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT - GROUND_HEIGHT),
                'size': random.randint(3, 6),
                'twinkle': random.uniform(0, math.pi * 2),
                'speed': random.uniform(0.5, 2)
            }
            self.stars.append(star)

    def update(self, dt):
        for star in self.stars:
            star['twinkle'] += dt * star['speed']
            if star['twinkle'] > 2 * math.pi:
                star['twinkle'] = 0

    def render(self, screen):
        for star in self.stars:
            brightness = abs(math.sin(star['twinkle']))
            alpha = int(255 * brightness)
            size = star['size']

            x, y = int(star['x']), int(star['y'])
            points = []
            for i in range(10):
                angle = i * 36 * math.pi / 180
                r = size if i % 2 == 0 else size // 2
                px = x + int(r * math.cos(angle))
                py = y + int(r * math.sin(angle))
                points.append((px, py))

            star_surf = pygame.Surface((size*3, size*3), pygame.SRCALPHA)
            offset_points = [(p[0] - x + size*1.5, p[1] - y + size*1.5) for p in points]
            if len(offset_points) >= 3:
                pygame.draw.polygon(star_surf, (*GOLD, alpha), offset_points)
            screen.blit(star_surf, (x - size*1.5, y - size*1.5))


class RainbowEffect:

    def __init__(self):
        self.offset = 0
        self.colors = [
            (255, 0, 0),
            (255, 127, 0),
            (255, 255, 0),
            (0, 255, 0),
            (0, 0, 255),
            (75, 0, 130),
            (148, 0, 211)
        ]

    def update(self, dt):
        self.offset += dt * 50
        if self.offset > SCREEN_WIDTH:
            self.offset = 0

    def render(self, screen):
        stripe_height = 3
        for i, color in enumerate(self.colors):
            y = i * stripe_height
            for x in range(SCREEN_WIDTH):
                wave_offset = int(5 * math.sin((x + self.offset) * 0.02))
                alpha = 100
                surf = pygame.Surface((2, stripe_height), pygame.SRCALPHA)
                surf.fill((*color, alpha))
                screen.blit(surf, (x, y + wave_offset))


class ScoreEffect:

    def __init__(self):
        self.active_effects = []

    def create_effect(self, x, y, score):
        effect = {
            'x': x,
            'y': y,
            'life': 1.0,
            'score': score,
            'particles': []
        }

        for _ in range(20):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 150)
            particle = {
                'x': x,
                'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'color': random.choice([GOLD, HOT_PINK, LIGHT_PINK, PURPLE])
            }
            effect['particles'].append(particle)

        self.active_effects.append(effect)

    def update(self, dt):
        for effect in self.active_effects[:]:
            effect['life'] -= dt

            for particle in effect['particles']:
                particle['x'] += particle['vx'] * dt
                particle['y'] += particle['vy'] * dt
                particle['vy'] += 200 * dt

            if effect['life'] <= 0:
                self.active_effects.remove(effect)

    def render(self, screen):
        for effect in self.active_effects:
            alpha = int(255 * effect['life'])

            font = pygame.font.Font(None, 120)
            text = font.render("+1", True, GOLD)
            text.set_alpha(alpha)
            y_offset = int((1 - effect['life']) * 50)
            screen.blit(text, (int(effect['x']) - 20, int(effect['y']) - y_offset))

            for particle in effect['particles']:
                size = int(3 * effect['life'])
                if size > 0:
                    particle_surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
                    pygame.draw.circle(particle_surf, (*particle['color'], alpha),
                                     (size, size), size)
                    screen.blit(particle_surf,
                              (int(particle['x']) - size, int(particle['y']) - size))
