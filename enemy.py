import pygame
from entity import *
from settings import *

def get_status(enemy_state):
    if not enemy_state['attack_animation_playing']:
        if enemy_state['direction'].x == 0 and enemy_state['direction'].y == 0:
            if not enemy_state['status'] == 'idle':
                enemy_state['status'] = 'idle'
                enemy_state['frame_index'] = 0
        else:
            enemy_state['status'] = 'walk'
    if enemy_state['is_attacking'] and not enemy_state['attack_animation_playing']:
        enemy_state['status'] = 'idle'

def collisions(entity_state):
    if entity_state['hitbox'].x < 60:
        entity_state['hitbox'].x = 60
    elif entity_state['hitbox'].x > 1600:
        entity_state['hitbox'].x = 1600
    if entity_state['hitbox'].y > 180:
        entity_state['hitbox'].y = 180
        entity_state['is_jumping'] = False

def enemy_ai(enemy_state, player_state, background_data):
    from random import randint, choice

    if not enemy_state['attack_animation_playing']:
        if enemy_state['status'] != 'walk':
            if abs(enemy_state['hitbox'].x - player_state['hitbox'].x) > 300:
                enemy_state['direction'].x = - enemy_state['face_direction']
                enemy_state['status'] = 'walk'
                enemy_state['in_range'] = False
            # elif abs(enemy_state['hitbox'].x - player_state['hitbox'].x) < 100:
            #     enemy_state['direction'].x = enemy_state['face_direction']
            #     enemy_state['status'] = 'walk'
            else:
                enemy_state['in_range'] = True
        if not enemy_state['is_attacking'] and enemy_state['in_range']:
            if randint(0, 100) <= 2:
                move = choice(['lpunch', 'hkick', 'lmkick', 'mhpunch'])
                initialize_move(enemy_state, move)
                #background_data['bgshake_time'] = pygame.time.get_ticks()


def cooldowns(enemy_state):
    current_time = pygame.time.get_ticks()

    if enemy_state['is_dodging']:
        if current_time - enemy_state['dodge_time'] >= enemy_state['dodge_cooldown']:
            enemy_state['direction'].x = 0
            enemy_state['is_dodging'] = False

    if enemy_state['is_attacking'] and not enemy_state['attack_animation_playing']:
        if current_time - enemy_state['attack_time'] >= enemy_state['attack_cooldown']:
            enemy_state['is_attacking'] = False
            enemy_state['direction'].y = 0
            enemy_state['direction'].x = 0

    if not enemy_state['is_vulnerable']:
        if current_time - enemy_state['vulnerability_time'] > enemy_state['vulnerability_cooldown']:
            enemy_state['is_vulnerable'] = True

    