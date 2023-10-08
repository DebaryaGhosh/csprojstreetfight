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

def initialize_player(client_data):
    # screen setup
    screen = pygame.display.get_surface()

    # sprite setup
    sprite = pygame.sprite.Sprite()
    img = pygame.image.load('./graphics/ryu/idle/idle0.png').convert_alpha()
    rect = img.get_rect()
    rect.x = 700
    rect.y = STAGE_HEIGHT
    hitbox = rect.inflate(-70, 0)
    
    # moevement setup
    direction = pygame.math.Vector2()

    # animation setup
    character_path = './graphics/ryu'
    animations = {
        1: {
            'idle': [],
            'walk': [],
            'jump': [],
            'inair': [],
            'lpunch': [],
            'hkick': [],
            'block': [],
            'crouch': [],
            'mhpunch': [],
            'lmkick': [],
            'fwjump': [],
            'hit': [],
        },
        -1: {
            'idle': [],
            'walk': [],
            'jump': [],
            'inair': [],
            'lpunch': [],
            'hkick': [],
            'block': [],
            'crouch': [],
            'mhpunch': [],
            'lmkick': [],
            'fwjump': [],
            'hit': [],
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
        'health': client_data['health'],
        'attack': client_data['attack'],
        'defense': client_data['defense'],
        'speed': client_data['speed'],
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
        'inair': False,

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
            'speed': 5,
        },
        'health': stats['health'],
        'attack': stats['attack'],
        'defense': stats['defense'],
        'speed': stats['speed'],
        'coins': client_data['coins'],

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

def initialize_enemy(name, enemy_init_data):
    # screen setup
    screen = pygame.display.get_surface()
    screen_rect = screen.get_rect()

    character_path = enemy_init_data[name]['character_path']

    # sprite setup
    sprite = pygame.sprite.Sprite()
    img = pygame.image.load(character_path + '/idle/idle0.png').convert_alpha()
    rect = img.get_rect()
    rect.x = 1000
    rect.y = STAGE_HEIGHT
    hitbox = rect.inflate(-80, 0)

    direction = pygame.math.Vector2()

    # animation setup
    
    animations = {
        1: {
            'idle': [],
            'walk': [],
            'lpunch': [],
            'hkick': [],
            'lmkick': [],
            'mhpunch': [],
            'hit': [],
        },
        -1: {
            'idle': [],
            'walk': [],
            'lpunch': [],
            'hkick': [],
            'lmkick': [],
            'mhpunch': [],
            'hit': [],
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
    stats = enemy_init_data[name]['stats']

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
        'vulnerability_cooldown': 1500,

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
    pygame.mixer.init()
    pygame.mixer.music.load('./audio/menu.mp3')
    pygame.mixer.music.set_volume(0.5)

    pygame.mixer.music.play(-1)

def initialize_ui():

    timer_font = pygame.font.Font(UI_FONT, TIMER_FONT_SIZE)
    names_font = pygame.font.Font(UI_FONT, NAMES_FONT_SIZE)
    coins_font = pygame.font.Font(UI_FONT, COINS_FONT_SIZE)

    player_health_bar_rect = pygame.Rect(50, 70, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT)
    player_mugshot_rect = pygame.Rect(0, 0, 150, 150)

    enemy_health_bar_rect = pygame.Rect(550, 70, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT)
    enemy_mugshot_rect = pygame.Rect(850, 0, 150, 150)

    ryu_mugshot = pygame.image.load('./graphics/mugshots/ryu.png').convert_alpha()
    thawk_mugshot = pygame.image.load('./graphics/mugshots/thawk.png').convert_alpha()
    chunli_mugshot = pygame.image.load('./graphics/mugshots/chunli.png').convert_alpha()

    timer_rect = pygame.Rect(450, 10, 100, 50)

    ryu_name_rect = pygame.Rect(100, 35, 100, 50)
    enemy_name_rect = pygame.Rect(800, 35, 100, 50)

    display = pygame.display.get_surface().get_rect()

    intro_background_anim = import_folder('./graphics/intro/background')
    intro_background_img = pygame.image.load('./graphics/intro/background/frame_00_delay-0.08s.png').convert_alpha()
    intro_background_rect = intro_background_img.get_rect(topleft = display.topleft)

    logo = pygame.image.load('./graphics/intro/ui/logo.png').convert_alpha()
    logo_rect = logo.get_rect(center = display.center)

    play = pygame.image.load('./graphics/intro/ui/play_n.png').convert_alpha()
    play_h = pygame.image.load('./graphics/intro/ui/play_h.png').convert_alpha()
    play_rect = play.get_rect(center = display.center + pygame.math.Vector2(0, 150))

    level_map = pygame.image.load('./graphics/map/map1.png').convert_alpha()
    level_map_rect = level_map.get_rect(center = display.center)

    thawk_map_icon = pygame.image.load('./graphics/map/ui/icons/thawk_icon_n.png').convert_alpha()
    thawk_map_icon_h = pygame.image.load('./graphics/map/ui/icons/thawk_icon_h.png').convert_alpha()
    thawk_map_icon_rect = thawk_map_icon.get_rect(center = (138, 180))
    chunli_map_icon = pygame.image.load('./graphics/map/ui/icons/chunli_icon_n.png').convert_alpha()
    chunli_map_icon_h = pygame.image.load('./graphics/map/ui/icons/chunli_icon_h.png').convert_alpha()
    chunli_map_icon_rect = thawk_map_icon.get_rect(center = (395, 321))

    fight_text = pygame.image.load('./graphics/map/ui/text/fight.png').convert_alpha()
    fight_text_rect = fight_text.get_rect(center = display.center)

    count3_text = pygame.image.load('./graphics/map/ui/text/3.png').convert_alpha()
    count3_text_rect = count3_text.get_rect(center = display.center)
    count2_text = pygame.image.load('./graphics/map/ui/text/2.png').convert_alpha()
    count2_text_rect = count2_text.get_rect(center = display.center)
    count1_text = pygame.image.load('./graphics/map/ui/text/1.png').convert_alpha()
    count1_text_rect = count1_text.get_rect(center = display.center)

    countdown_mask = pygame.image.load('./graphics/map/ui/text/countdown_mask.png').convert_alpha()
    countdown_mask_rect = countdown_mask.get_rect(topleft = display.topleft)

    coinmeter = pygame.image.load('./graphics/map/ui/icons/coin_meter.png').convert_alpha()
    coinmeter_rect = coinmeter.get_rect(topright = display.topright)

    youwin_text = pygame.image.load('./graphics/level/youwin.png').convert_alpha()
    youlose_text = pygame.image.load('./graphics/level/youlose.png').convert_alpha()
    youwin_text_rect = youwin_text.get_rect(center = display.center - pygame.math.Vector2(0, 150))
    youlose_text_rect = youlose_text.get_rect(center = display.center - pygame.math.Vector2(0, 150))

    next_button = pygame.image.load('./graphics/level/next_n.png').convert_alpha()
    next_button_h = pygame.image.load('./graphics/level/next_h.png').convert_alpha()
    next_button_rect = next_button.get_rect(center = display.center + pygame.math.Vector2(0, 150))

    ui_data = {

        'current_state': screens['intro'],

        'timer_font': timer_font,
        'names_font': names_font,
        'coins_font': coins_font,

        'player_health_bar_rect': player_health_bar_rect,
        'player_mugshot_rect': player_mugshot_rect,

        'enemy_health_bar_rect': enemy_health_bar_rect,
        'enemy_mugshot_rect': enemy_mugshot_rect,

        'ryu_mug': ryu_mugshot,
        'thawk_mug': thawk_mugshot,
        'chunli_mug': chunli_mugshot,

        'ryu_name_rect': ryu_name_rect,
        'enemy_name_rect': enemy_name_rect,

        'thawk_display_name': 'T-HAWK',
        'chunli_display_name': 'CHUN-LI',

        'timer_rect': timer_rect,
        'time_passed': 0,
        'max_time': 3000 * 100,

        'intro_background_img': intro_background_img,
        'intro_background_rect': intro_background_rect,
        'intro_backgrounds': intro_background_anim,
        'background_anim_frameindex': 0,
        'background_anim_speed': 0.15,
        'transition': False,
        'intro_alpha': 255,

        'logo_img': logo,
        'logo_rect': logo_rect,
        'logo_alpha': 255,
        'logo_alpha_transition_delay_time': 0,
        'logo_alpha_transition_delay': 3000,

        'play_img': play,
        'play_n': play,
        'play_h': play_h,
        'play_rect': play_rect,
        'play_blit_rect': None,
        'play_alpha': 255,

        'level_map': level_map,
        'level_map_rect': level_map_rect,

        'thawk_map_icon_img': thawk_map_icon,
        'thawk_map_icon_n': thawk_map_icon,
        'thawk_map_icon_h': thawk_map_icon_h,
        'thawk_map_icon_rect': thawk_map_icon_rect,
        'thawk_map_icon_blit_rect': None,

        'chunli_map_icon_img': chunli_map_icon,
        'chunli_map_icon_n': chunli_map_icon,
        'chunli_map_icon_h': chunli_map_icon_h,
        'chunli_map_icon_rect': chunli_map_icon_rect,
        'chunli_map_icon_blit_rect': None,

        'fight_text': fight_text,
        'fight_text_rect': fight_text_rect,
        'countdown_text_time': None,
        'countdown_text_duration': 4000,

        'count3_text': count3_text,
        'count3_text_rect': count3_text_rect,
        'count2_text': count2_text,
        'count2_text_rect': count2_text_rect,
        'count1_text': count1_text,
        'count1_text_rect': count1_text_rect,

        'countdown_mask': countdown_mask,
        'countdown_mask_rect': countdown_mask_rect,

        'coinmeter_img': coinmeter,
        'coinmeter_rect': coinmeter_rect,

        'youwin_text': youwin_text,
        'youwin_text_rect': youwin_text_rect,
        'youlose_text': youlose_text,
        'youlose_text_rect': youlose_text_rect,

        'next_img': next_button,
        'next_n': next_button,
        'next_h': next_button_h,
        'next_rect': next_button_rect,
        'next_blit_rect': None,
        'next_alpha': 255,
        
    }
    return ui_data

def initialize_attack_data():
    attack_data = {
        'lpunch': {
            'attack': 10, # 5
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

def initialize_level():
    level_state = {
        'game_over': False,
        'game_won': False,

        'player_state': None,
        'enemy_state': None,
        'background_data': None
    }
    return level_state

def initialize_client():

    client_data = {
        'health': 100,
        'attack': 5,
        'defense': 7,
        'speed': 5,
        'coins': 0,
    }

    return client_data

def inititialize_game():
    game_state = {
        'initialized_game': False,
    }
    return game_state

def enemy_init_data():
    enemy_init_data = {
        'thawk': {
            'character_path': './graphics/thawk',
            'stats': {
                'health': 100,
                'attack': 6,
                'defense': 7,
                'speed': 3,
            },
            'reward': 500,
        },
        'chunli': {
            'character_path': './graphics/chunli',
            'stats': {
                'health': 100,
                'attack': 6,
                'defense': 7,
                'speed': 3,
            },
            'reward': 1000,
        },
    }

    return enemy_init_data