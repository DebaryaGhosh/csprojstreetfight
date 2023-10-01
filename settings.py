import pygame

WIDTH = 1000
HEIGHT = 600
FPS = 60

GAME_TITLE = 'Street Fight'

STAGE_HEIGHT = 180

GRAVITY = 1

ATTACK_MOVES_LIST = [
    'lpunch',
    'hkick',
    'block',
    'crouch',
    'mhpunch',
    'lmkick',
    'fwjump',
    'jump',
]

BUTTON_MAP = {
    'walk_right': pygame.K_RIGHT,
    'walk_left': pygame.K_LEFT,

    'block': pygame.K_q,
    'crouch': pygame.K_DOWN,

    'jump': pygame.K_UP,
    'lpunch': pygame.K_f,
    'hkick': pygame.K_d,
    'mhpunch': pygame.K_s,
    'lmkick': pygame.K_a,
    'fwjump': pygame.K_e,
}

UI_FONT = './graphics/font/mangat.ttf'
TIMER_FONT_SIZE = 35
NAMES_FONT_SIZE = 25

HEALTH_BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 400

PLAYER_UI_BG_COLOR = '#fa0a22'
ENEMY_UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
PLAYER_HEALTH_COLOR = '#222222'
ENEMY_HEALTH_COLOR = '#fa0a22'