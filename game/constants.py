
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60
GAME_TITLE = "Flappy Barbie - Pink Dreams 💗"

FULLSCREEN = False
RESIZABLE = True

SOUND_ENABLED = True
MUSIC_VOLUME = 0.3
SFX_VOLUME = 0.5

# Цвета (RGB) - Розовая палитра!
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 192, 203)
DARK_PINK = (255, 105, 180)
HOT_PINK = (255, 20, 147)
LIGHT_PINK = (255, 182, 193)
PURPLE = (218, 112, 214)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
SKY_BLUE = (135, 206, 235)
GOLD = (255, 215, 0)

GRAVITY = 1800
FLAP_STRENGTH = -650
MAX_FALL_SPEED = 1200

PIPE_SPEED = 350
PIPE_GAP = 400
PIPE_SPACING = 700
PIPE_WIDTH = 180

BARBIE_SIZE = 100
BARBIE_ROTATION_SPEED = 3

GAME_STATE_MENU = "menu"
GAME_STATE_PLAYING = "playing"
GAME_STATE_PAUSED = "paused"
GAME_STATE_GAME_OVER = "game_over"
GAME_STATE_WIN = "win"

GROUND_HEIGHT = 150
BARBIE_START_Y = 540

# Эффекты и частицы (СУПЕР МЕГА ПРАЙМ ДИЗАЙН!)
PARTICLE_COUNT = 80
TRAIL_LENGTH = 15
STAR_COUNT = 50
SPARKLE_INTERVAL = 0.1

COIN_SIZE = 60
COIN_SPAWN_CHANCE = 0.3
COINS_PER_SCORE = 1
COIN_COLLECT_RADIUS = 80

SKINS = {
    "default": {"name": "Классическая Барби", "price": 0, "file": None},
    "skin1": {"name": "Гламурная Барби", "price": 50, "file": "1.png"},
    "skin2": {"name": "Спортивная Барби", "price": 100, "file": "2.png"},
    "skin3": {"name": "Принцесса Барби", "price": 200, "file": "3.png"},
    "skin4": {"name": "Рок-звезда Барби", "price": 350, "file": "4.png"},
    "skin5": {"name": "Королева Барби", "price": 500, "file": "5.png"}
}

LOCATIONS = {
    "default": {"name": "Розовое небо", "price": 0, "colors": [(135, 206, 235), (255, 192, 203)]},
    "sunset": {"name": "Закат", "price": 75, "colors": [(255, 94, 77), (255, 154, 162)]},
    "night": {"name": "Звездная ночь", "price": 150, "colors": [(25, 25, 112), (138, 43, 226)]},
    "rainbow": {"name": "Радужный рай", "price": 250, "colors": [(255, 105, 180), (186, 85, 211)]},
    "galaxy": {"name": "Космос", "price": 400, "colors": [(10, 10, 50), (75, 0, 130)]},
    "candy": {"name": "Конфетная страна", "price": 600, "colors": [(255, 182, 193), (255, 228, 225)]}
}
