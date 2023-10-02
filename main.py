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

def run_game(player_state, enemy_state, background_data, ui_data, attack_data):
    
    update_player(player_state, enemy_state, attack_data, background_data)
    update_enemy(enemy_state, player_state, background_data, attack_data)
    update_background(background_data, player_state)
    blit_entities(player_state, enemy_state, background_data)
    update_ui(ui_data, [player_state, enemy_state, background_data])
    

# game loop
while game_is_on:

    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            game_is_on = False

    screen.fill('black')

    # screen manager
    if ui_data['current_state'] == 'intro':
        run_intro(ui_data, event_list)
    elif ui_data['current_state'] == 'level':
        run_game(player_state, enemy_state, background_data, ui_data, attack_data)

    # debug
    debug((player_state['inair'], player_state['is_jumping']))
    
    # misc.
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()