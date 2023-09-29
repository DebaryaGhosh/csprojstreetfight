import pygame
from settings import *


# changes the status of the player to a new status, and sets frame_index to 0 if new status is different
def frame_and_status_change(entity_state, new_status):
    if entity_state['status'] != new_status:
        entity_state['frame_index'] = 0
        entity_state['status'] = new_status

# initializes move and sets some values
def initialize_move(entity_state, move):
    frame_and_status_change(entity_state, move)
    entity_state['attack_time'] = pygame.time.get_ticks()
    entity_state['is_attacking'] = True
    entity_state['direction'].x = 0
    entity_state['direction'].y = 0
    entity_state['attack_animation_playing'] = True

    
    if entity_state['name'] == 'player':
        if move == 'jump':
            entity_state['y_vel'] = -40
            entity_state['is_jumping'] = True
        
        if move == 'lpunch':
            entity_state['attack_cooldown'] = 200
            entity_state['animation_speed'] = 0.22

        if move in ['hkick', 'mhpunch']:
            entity_state['animation_speed'] = 0.2
            entity_state['attack_cooldown'] = 200

        if move == 'crouch' or move == 'block':
            entity_state['attack_cooldown'] = 50

        if move == 'lmkick':
            entity_state['animation_speed'] = 0.175
            entity_state['attack_cooldown'] = 200

        if move == 'fwjump':
            entity_state['speed'] = 10
            entity_state['animation_speed'] = 0.2
            entity_state['direction'].x = 1

# moves the player
def move_entity(entity_state):

    # entity direction reverses the direction of the enemy, so that they can avail the same formula
    entity_state['hitbox'].x += entity_state['speed'] * entity_state['direction'].x * entity_state['entity_direction'] 
    entity_state['hitbox'].y += entity_state['speed'] * entity_state['direction'].y
    
    # if character is jumping, increase his y velocity by the gravity.
    if entity_state['is_jumping']:
        entity_state['hitbox'].y += entity_state['y_vel']
        entity_state['y_vel'] += GRAVITY
        

# animates the player.
def animate(entity_state, defender_state, attack_data):
    # selects animation. face direction chooses the sprite corresponding to the side they are facing.
    animation = entity_state['animations'][entity_state['face_direction']][entity_state['status']]
    
    entity_state['frame_index'] += entity_state['animation_speed']

    # improvements to be made to the animation to accommodate for 'reaction time' feature.
    if entity_state['frame_index'] >= len(animation):
        if entity_state['is_jumping']:
            entity_state['frame_index'] = len(animation) - 1
            if entity_state['y_vel'] > 0:
                entity_state['attack_animation_playing'] = False
        elif entity_state['status'] in ATTACK_MOVES_LIST:
            check_attack(entity_state, defender_state, attack_data)
            entity_state['frame_index'] = 0
            entity_state['attack_animation_playing'] = False
        else:
            entity_state['frame_index'] = 0
            
        if defender_state['hitbox'].x - entity_state['hitbox'].x > 0: 
            entity_state['face_direction'] = 1
        elif defender_state['hitbox'].x - entity_state['hitbox'].x < 0:
            entity_state['face_direction'] = -1
        entity_set_idle_values(entity_state)

    entity_state['image'] = animation[int(entity_state['frame_index'])]
    entity_state['rect'] = entity_state['image'].get_rect(bottomleft = entity_state['hitbox'].bottomleft)
            

# sets the values of the player to what they were when player was idle. 
# player changes speed and direction when attacking, so it is needed.
def entity_set_idle_values(entity_state):
    if entity_state['name'] == 'player':
        entity_state['speed'] = 5
        
    else:
        entity_state['speed'] = 3
    entity_state['direction'].x = 0
    entity_state['direction'].y = 0
    entity_state['animation_speed'] = 0.15

def check_attack(attacker, defender, attack_data):
    if abs(attacker['hitbox'].x - defender['hitbox'].x) < 200 and defender['is_vulnerable']:
        attack = attacker['status']
        defense = defender['status'] 

        if attack in ATTACK_MOVES_LIST:
            if defense == 'block' or attack == 'crouch': return
            if attack == 'block' or attack == 'crouch': return
            defender['health'] -= attack_data[attack]['attack']
            if defender['health'] < 0:
                defender['health'] = 0
            defender['is_vulnerable'] = False
            defender['vulnerability_time'] = pygame.time.get_ticks()