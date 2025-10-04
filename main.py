import pygame
import sys
from game.game_manager import GameManager
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_TITLE, FULLSCREEN, RESIZABLE
from game.sound_generator import get_sound_generator

def main():
    pygame.init()

    try:
        pygame.mixer.quit()
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.mixer.set_num_channels(16)
        print("🔊 Звуковая система готова!")
    except Exception as e:
        print(f"⚠️ Ошибка звука: {e}")

    is_fullscreen = FULLSCREEN

    if is_fullscreen:
        display_info = pygame.display.Info()
        screen_w, screen_h = display_info.current_w, display_info.current_h
        screen = pygame.display.set_mode((screen_w, screen_h), pygame.FULLSCREEN | pygame.NOFRAME)
        print(f"🖥️ Полноэкранный режим {screen_w}x{screen_h}")
    else:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        print(f"🪟 Оконный режим {SCREEN_WIDTH}x{SCREEN_HEIGHT}")

    game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)

    sound_gen = get_sound_generator()
    clock = pygame.time.Clock()
    game_manager = GameManager(game_surface)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    is_fullscreen = not is_fullscreen
                    if is_fullscreen:
                        display_info = pygame.display.Info()
                        screen = pygame.display.set_mode(
                            (display_info.current_w, display_info.current_h),
                            pygame.FULLSCREEN | pygame.NOFRAME
                        )
                        print("🖥️ Полный экран включен")
                    else:
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                        print("🪟 Оконный режим")
                else:
                    game_manager.handle_event(event)
            else:
                game_manager.handle_event(event)

        dt = clock.tick(FPS) / 1000.0
        game_manager.update(dt)
        game_manager.render()

        screen_w, screen_h = screen.get_size()
        game_w, game_h = game_surface.get_size()
        scale = min(screen_w / game_w, screen_h / game_h)
        scaled_w = int(game_w * scale)
        scaled_h = int(game_h * scale)
        offset_x = (screen_w - scaled_w) // 2
        offset_y = (screen_h - scaled_h) // 2

        screen.fill((0, 0, 0))
        scaled_surface = pygame.transform.smoothscale(game_surface, (scaled_w, scaled_h))
        screen.blit(scaled_surface, (offset_x, offset_y))
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
