import pygame
from settings import *
from game_data import *
from support import *
from debug import debug
from game_updates import *
from intro import run_intro

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

current_state = screens['intro']

def run_game(player_state, enemy_state, background_data, ui_data, attack_data):
    
    update_player(player_state, enemy_state, attack_data, background_data)
    update_enemy(enemy_state, player_state, background_data, attack_data)
    update_background(background_data, player_state)
    update_ui(ui_data, [player_state, enemy_state, background_data])

    if background_data['bgshake']:
        player_state['offset'] = player_state['rect'].topleft - background_data['shake_offset'] + pygame.math.Vector2(0, 80)
        enemy_state['offset'] = enemy_state['rect'].topleft - background_data['shake_offset'] + pygame.math.Vector2(0, -30)
    else:
        player_state['offset'] = player_state['rect'].topleft - background_data['offset'] + pygame.math.Vector2(0, 80)
        enemy_state['offset'] = enemy_state['rect'].topleft - background_data['offset'] + pygame.math.Vector2(0, -30)

    screen.blit(enemy_state['image'], enemy_state['offset'])
    screen.blit(player_state['image'], player_state['offset'])
    

# game loop
while game_is_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_is_on = False

    screen.fill('black')

    if current_state == 'intro':
        run_intro(ui_data, current_state)
    elif current_state == 'game':
        run_game(player_state, enemy_state, background_data, ui_data, attack_data)

    debug((player_state['inair'], player_state['is_jumping']))
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()