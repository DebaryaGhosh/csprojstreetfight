import pygame
from settings import *
from game_data import *
from game_updates import *
from debug import debug

def run_level(enemy_name, client_data, game_state, ui_data, attack_data, event_list, level_state, enemy_init_state):
    if not game_state['initialized_game']:
        level_state['player_state'] = initialize_player(client_data)
        level_state['enemy_state'] = initialize_enemy(enemy_name, enemy_init_state)
        level_state['background_data'] = initialize_background()

        game_state['initialized_game'] = True
        ui_data['countdown_text_time'] = pygame.time.get_ticks()
        ui_data['timer_start'] = pygame.time.get_ticks()
    else: 
        player_state = level_state['player_state']
        enemy_state = level_state['enemy_state']
        background_data = level_state['background_data']

        #print(type(player_state), type(enemy_state), type(background_data))

        run_game(enemy_name, player_state, enemy_state, background_data, ui_data, attack_data, level_state, event_list, game_state)

        debug
        debug(('isjumping:'      + str(player_state['is_jumping']),
            'inair:'          + str(player_state['inair']),
            'isinvulnerable:' + str(not player_state['is_vulnerable'])
        ))

def run_game(enemy_name, player_state, enemy_state, background_data, ui_data, attack_data, level_state, event_list, game_state):
    update_background(background_data, player_state)
    if not countdown(ui_data):
        if not level_state['game_over']:
            update_player(player_state, enemy_state, attack_data, background_data, ui_data, event_list)
            update_enemy(enemy_state, player_state, background_data, attack_data, ui_data, event_list)
            blit_entities(player_state, enemy_state, background_data)
            update_ui(enemy_name, ui_data, [player_state, enemy_state, background_data])
            check_game_over(player_state, enemy_state, level_state)
        else:
            game_over(ui_data, event_list, level_state, game_state)