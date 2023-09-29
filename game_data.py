import pygame
from support import *
from settings import *


animation_frame_data_ryu = {
    'walk': {
        0: 0.15,
        1: 0.15,
        2: 0.15,
        3: 0.15,
        4: 0.15
    },
    'idle': {
        0: 0.15,
        1: 0.15,
        2: 0.15,
        3: 0.15,
    },
}

animation_frame_data_thawk = {
    
}

def initialize_player():
    # screen setup
    screen = pygame.display.get_surface()

    # sprite setup
    sprite = pygame.sprite.Sprite()
    img = pygame.image.load('./graphics/ryu/idle/idle0.png').convert_alpha()
    rect = img.get_rect()
    rect.x = 500
    rect.y = STAGE_HEIGHT
    hitbox = rect
    
    # moevement setup
    direction = pygame.math.Vector2()

    # animation setup
    character_path = './graphics/ryu'
    animations = {
        1: {
            'idle': [],
            'walk': [],
            'jump': [],
            'lpunch': [],
            'hkick': [],
            'block': [],
            'crouch': [],
            'mhpunch': [],
            'lmkick': [],
            'fwjump': [],
        },
        -1: {
            'idle': [],
            'walk': [],
            'jump': [],
            'lpunch': [],
            'hkick': [],
            'block': [],
            'crouch': [],
            'mhpunch': [],
            'lmkick': [],
            'fwjump': [],
        },
    }
    for face_direction in animations.keys():
        for animation in animations[face_direction].keys():
            folder_path = character_path + '/' + animation
            animation_graphics = import_folder(folder_path)
            if face_direction == -1:
                for i, graphic in enumerate(animation_graphics):
                    graphic = pygame.transform.flip(graphic, True, False)
                    animation_graphics[i] = graphic
            animations[face_direction][animation] = animation_graphics

    # stats
    status = 'idle'
    stats = {
        'health': 100,
        'attack': 5,
        'defense': 7,
        'speed': 5,
    }

    player_data = {
        # sprite data
        'name': 'player',
        'sprite': sprite,
        'image': img,
        'rect': rect,
        'hitbox': hitbox,
        'offset': pygame.math.Vector2(),

        # movement data
        'direction': direction,
        'entity_direction': 1,
        'face_direction': 1,
        'y_vel': 0,
        'is_jumping': False,
        'is_attacking': False,
        'attack_time': 0,
        'attack_cooldown': 400,

        # animation data
        'animations': animations,
        'frame_index': 0,
        'animation_speed': 0.15,
        'attack_animation_playing': False,

        #stats
        'status': status,
        'stats': {
            'health': 100,
            'attack': 5,
            'defense': 7,
            'speed': 10,
        },
        'health': stats['health'],
        'attack': stats['attack'],
        'defense': stats['defense'],
        'speed': stats['speed'],

        # vulnerability
        'is_vulnerable': False,
        'vulnerability_time': 0,
        'vulnerability_cooldown': 1500,

        # knockback
        'is_knockbackked': False,
        'knockback_time': 0,
        'knockback_cooldown': 200

    }

    return player_data

def initialize_enemy():
    # screen setup
    screen = pygame.display.get_surface()
    screen_rect = screen.get_rect()

    # sprite setup
    sprite = pygame.sprite.Sprite()
    img = pygame.image.load('./graphics/thawk/idle/idle0.png').convert_alpha()
    rect = img.get_rect()
    rect.x = 1000
    rect.y = STAGE_HEIGHT
    hitbox = rect

    direction = pygame.math.Vector2()

    # animation setup
    character_path = './graphics/thawk'
    animations = {
        1: {
            'idle': [],
            'walk': [],
            'lpunch': [],
            'hkick': [],
            'lmkick': [],
            'mhpunch': []
        },
        -1: {
            'idle': [],
            'walk': [],
            'lpunch': [],
            'hkick': [],
            'lmkick': [],
            'mhpunch': [],
        }
    }

    for face_direction in animations.keys():
        for animation in animations[face_direction].keys():
            folder_path = character_path + '/' + animation
            animation_graphics = import_folder(folder_path)
            if face_direction == 1:
                for i, graphic in enumerate(animation_graphics):
                    graphic = pygame.transform.flip(graphic, True, False)
                    animation_graphics[i] = graphic
            animations[face_direction][animation] = animation_graphics

    #stats
    status = 'idle'
    stats = {
        'health': 100,
        'attack': 6,
        'defense': 7,
        'speed': 3,
    }

    enemy_data = {
        # sprite data
        'name': 'enemy',
        'sprite': sprite,
        'image': img,
        'rect': rect,
        'hitbox': hitbox,
        'offset': pygame.math.Vector2(),

        # movement data
        'direction': direction,
        'entity_direction': -1,
        'face_direction': -1,
        'y_vel': 0,
        'is_jumping': False,
        'is_attacking': False,
        'attack_time': 0,
        'attack_cooldown': 2000,
        'in_range': False,

        # animation data
        'animations': animations,
        'frame_index': 0,
        'animation_speed': 0.15,
        'attack_animation_playing': False,

        # ai flags and timers
        'is_dodging': False,
        'dodge_time': 0,
        'dodge_cooldown': 800,

        #stats
        'status': status,
        'stats': {
        'health': 100,
        'attack': 6,
        'defense': 7,
        'speed': 3,
        },
        'health': stats['health'],
        'attack': stats['attack'],
        'defense': stats['defense'],
        'speed': stats['speed'],

        # vulnerability
        'is_vulnerable': True,
        'vulnerability_time': 0,
        'vulnerability_cooldown': 100,

        # knockback
        'is_knockbackked': False,
        'knockback_time': 0,
        'knockback_cooldown': 200
    }

    return enemy_data


def initialize_background():
    # screen setup
    screen = pygame.display.get_surface()
    half_width = screen.get_size()[0] // 2
    half_height = screen.get_size()[1] // 2
    offset = pygame.math.Vector2()

    backgrounds = import_folder('./graphics/background')

    background_data = {
        'half_width': half_width,
        'half_height': half_height,
        'offset': offset,
        'shake_offset': pygame.math.Vector2(),

        'backgrounds': backgrounds,

        'bgspeed_0': 0.7,
        'bgspeed_1': 0.8,
        'bgspeed_2': 1,

        'bgshake': False,
        'bgshake_amp': 10,
        'bgshake_time': 0,
        'bgshake_cooldown': 300,
    }

    return background_data

def initialize_audio():

    pygame.mixer.music.load('./audio/forest_of_death.mp3')
    pygame.mixer.music.set_volume(0.5)

    #pygame.mixer.music.play(-1)

def initialize_ui():

    timer_font = pygame.font.Font(UI_FONT, TIMER_FONT_SIZE)
    names_font = pygame.font.Font(UI_FONT, NAMES_FONT_SIZE)

    player_health_bar_rect = pygame.Rect(50, 70, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT)
    player_mugshot_rect = pygame.Rect(0, 0, 150, 150)

    enemy_health_bar_rect = pygame.Rect(550, 70, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT)
    enemy_mugshot_rect = pygame.Rect(850, 0, 150, 150)

    ryu_mugshot = pygame.image.load('./graphics/mugshots/ryu.png').convert_alpha()
    thawk_mugshot = pygame.image.load('./graphics/mugshots/thawk.png').convert_alpha()

    timer_start = pygame.time.get_ticks()
    timer_rect = pygame.Rect(450, 10, 100, 50)

    ryu_name_rect = pygame.Rect(100, 35, 100, 50)
    thawk_name_rect = pygame.Rect(800, 35, 100, 50)

    ui_data = {
        'timer_font': timer_font,
        'names_font': names_font,

        'player_health_bar_rect': player_health_bar_rect,
        'player_mugshot_rect': player_mugshot_rect,

        'enemy_health_bar_rect': enemy_health_bar_rect,
        'enemy_mugshot_rect': enemy_mugshot_rect,

        'ryu_mug': ryu_mugshot,
        'thawk_mug': thawk_mugshot,

        'ryu_name_rect': ryu_name_rect,
        'thawk_name_rect': thawk_name_rect,

        'timer_start': timer_start,
        'timer_rect': timer_rect,
        'time_passed': 0,
        'max_time': 3000 * 100
    }
    return ui_data

def initialize_attack_data():
    attack_data = {
        'lpunch': {
            'attack': 5,
            'cooldown': 200,
        },
        'hkick': {
            'attack': 7,
            'cooldown': 400,
        },
        'mhpunch': {
            'attack': 10,
            'cooldown': 600
        },
        'lmkick': {
            'attack': 8,
            'cooldown': 500
        },
        'fwjump': {
            'attack': 0,
            'cooldown': 900
        }
    }

    return attack_data
