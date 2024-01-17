# IMPORTANT!!! CHECK IF MODULES ARE PRESENT -----------------------------------------------
import subprocess, sys, pkg_resources

required = {'pygame', 'mysql-connector-python'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'pygame'])
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'mysql-connector-python'])
# --------------------------------------------------------------------------------------------
import pygame
from settings import *
from game_data import *
from support import *
from debug import debug
from game_updates import *
from intro import run_intro
from level_map import *
from level_manager import *

pygame.init()

# initialization of variables
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()
game_is_on = True

# default initialization of game objects
client_data = initialize_client()
game_state = inititialize_game()
ui_data = initialize_ui()
attack_data = initialize_attack_data()
initialize_audio()
level_state = initialize_level()
enemy_init_state = enemy_init_data()

# game loop
while game_is_on:

    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            import data_manager
            data = [client_data['attack'], client_data['defense'], client_data['coins']]
            data_manager.save_client_data(data)
            game_is_on = False

    screen.fill('black')

    # screen manager
    if ui_data['current_state'] == screens['intro']:
        run_intro(ui_data, event_list)
    elif ui_data['current_state'] == screens['map']:
        run_level_map(ui_data, event_list, client_data)
    elif ui_data['current_state'] == screens['thawk']:
        
        run_level('thawk', client_data, game_state, ui_data, attack_data, event_list, level_state, enemy_init_state)
    elif ui_data['current_state'] == screens['chunli']:
        
        run_level('chunli', client_data, game_state, ui_data, attack_data, event_list, level_state, enemy_init_state)
    
    # misc.
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()