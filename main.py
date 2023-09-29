import pygame
from settings import *
from game_data import *
from support import *
from debug import debug
import player
import entity
import enemy
from ui import display
from random import randint

pygame.init()

# initialization of variables
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()
game_is_on = True

# default initialization of game objects
player_state = initialize_player()
enemy_state = initialize_enemy()
background_data = initialize_background()
ui_data = initialize_ui()
attack_data = initialize_attack_data()
initialize_audio()


# updates the player. 
def update_player(player_state, enemy_state, attack_data):
    player.get_status(player_state)
    player.key_input(player_state, background_data)
    entity.move_entity(player_state)
    entity.animate(player_state, enemy_state, attack_data)
    player.collisions(player_state)
    player.cooldowns(player_state)

def update_enemy(enemy_state, player_state, background_data, attack_data):
    enemy.get_status(enemy_state)
    enemy.enemy_ai(enemy_state, player_state, background_data)
    entity.move_entity(enemy_state)
    entity.animate(enemy_state, player_state, attack_data)
    enemy.collisions(enemy_state)
    enemy.cooldowns(enemy_state)

def update_background(background_data, player):
    background_data['bgshake'] = False
    if pygame.time.get_ticks() - background_data['bgshake_time'] < background_data['bgshake_cooldown']:
        background_data['shake_offset'].x = background_data['offset'].x + randint(-background_data['bgshake_amp'], background_data['bgshake_amp'])
        background_data['shake_offset'].y = background_data['offset'].y + randint(-background_data['bgshake_amp'], background_data['bgshake_amp'])
        background_data['bgshake'] = True

    for index, background in enumerate(background_data['backgrounds']):
        if player['rect'].x > 485 and player['rect'].x < 1140:
            background_data['offset'].x = player['rect'].centerx - background_data['half_width']
        background_data['offset'].y = player['rect'].centery - background_data['half_height']

        rect = background.get_rect(topleft = (0, -150))
        bg_offset = pygame.math.Vector2()
        if background_data['bgshake']:
            bg_offset.x = (rect.topleft[0] - background_data['shake_offset'].x) * background_data['bgspeed_' + str(index)]
            bg_offset.y = rect.topleft[1] - background_data['shake_offset'].y
        else:
            bg_offset.x = (rect.topleft[0] - background_data['offset'].x) * background_data['bgspeed_' + str(index)]
            bg_offset.y = rect.topleft[1] - background_data['offset'].y
        screen.blit(background, bg_offset)

def update_ui(ui_data, data):
    display(player_state, enemy_state, ui_data, data)

def run_game(player_state, enemy_state, background_data, ui_data, attack_data):
    
    update_player(player_state, enemy_state, attack_data)
    update_enemy(enemy_state, player_state, background_data, attack_data)
    update_background(background_data, player_state)
    update_ui(ui_data, [player_state, enemy_state, background_data])
    

# game loop
while game_is_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_is_on = False

    screen.fill('black')

    run_game(player_state, enemy_state, background_data, ui_data, attack_data)

    if background_data['bgshake']:
        player_state['offset'] = player_state['rect'].topleft - background_data['shake_offset'] + pygame.math.Vector2(0, 80)
        enemy_state['offset'] = enemy_state['rect'].topleft - background_data['shake_offset'] + pygame.math.Vector2(0, -30)
    else:
        player_state['offset'] = player_state['rect'].topleft - background_data['offset'] + pygame.math.Vector2(0, 80)
        enemy_state['offset'] = enemy_state['rect'].topleft - background_data['offset'] + pygame.math.Vector2(0, -30)

    screen.blit(enemy_state['image'], enemy_state['offset'])
    screen.blit(player_state['image'], player_state['offset'])
    #debug((enemy_state['is_attacking'], enemy_state['status'], enemy_state['attack_animation_playing'], enemy_state['attack_cooldown']))
    debug((enemy_state['is_attacking']))
    
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()