import pygame
from settings import *
from entity import *

# check for input from user
def key_input(player_state, background_data):
    # keys pressed by user
    keys = pygame.key.get_pressed()

    if player_state['is_jumping']:
        if keys[BUTTON_MAP['walk_right']]:
            player_state['direction'].x = 1
        elif keys[BUTTON_MAP['walk_left']]:
            player_state['direction'].x = -1
        else:
            player_state['direction'].x = 0

    # checking which keys the player pressed
    if not player_state['attack_animation_playing']:
        if keys[BUTTON_MAP['walk_right']]:
            player_state['direction'].x = 1
            player_state['status'] = 'walk'
        elif keys[BUTTON_MAP['walk_left']]:
            player_state['direction'].x = -1
            player_state['status'] = 'walk'
        else:
            player_state['direction'].x = 0

        if keys[BUTTON_MAP['jump']] and not player_state['is_jumping']:
            initialize_move(player_state, 'jump')
        
        if not player_state['is_attacking']:

            for attack_move in ATTACK_MOVES_LIST:
                if keys[BUTTON_MAP[attack_move]]:
                    initialize_move(player_state, attack_move)
                    background_data['bgshake_time'] = pygame.time.get_ticks()


# manages cooldowns for buttons so that they are not abused
def cooldowns(player_state):
    current_time = pygame.time.get_ticks()
    
    if player_state['is_attacking'] and not player_state['attack_animation_playing']:
        if current_time - player_state['attack_time'] > player_state['attack_cooldown']:
            player_state['is_attacking'] = False
            player_state['direction'].x = 0
            player_state['direction'].y = 0
            player_state['attack_cooldown'] = 400

    if not player_state['is_vulnerable']:
        if current_time - player_state['vulnerability_time'] > player_state['vulnerability_cooldown']:
            player_state['is_vulnerable'] = True


# manages the status of the player and sets them to idle when required
def get_status(player_state):
    if not player_state['attack_animation_playing']:
        if player_state['direction'].x == 0 and player_state['direction'].y == 0:
            if not player_state['status'] == 'idle':
                player_state['status'] = 'idle'
                player_state['frame_index'] = 0
        else:
            player_state['status'] = 'walk'
    if player_state['is_attacking'] and not player_state['attack_animation_playing']:
        player_state['status'] = 'idle'


def collisions(entity_state):
    if entity_state['hitbox'].x < 60:
        entity_state['hitbox'].x = 60
    elif entity_state['hitbox'].x > 1600:
        entity_state['hitbox'].x = 1600
    if entity_state['hitbox'].y > 180:
        entity_state['hitbox'].y = 180
        entity_state['is_jumping'] = False