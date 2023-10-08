import pygame
from settings import *

def show_map(ui_data):
    # blits the map
    pygame.display.get_surface().blit(ui_data['level_map'], ui_data['level_map_rect'])



def show_coin_frame(ui_data, player_state):
    # blits the coin frame background, gets coin data, blits the text
    display = pygame.display.get_surface()

    display.blit(ui_data['coinmeter_img'], ui_data['coinmeter_rect']) # frame

    coins = ui_data['coins_font'].render(str(player_state['coins']), False, 'white')
    
    # offset to adjust the coins_rect
    coins_rect = coins.get_rect(topright = display.get_rect().topright + pygame.math.Vector2(-20, 10))
    display.blit(coins, coins_rect) # text

def show_map_icon(icon_img, icon_rect, name, ui_data):
    # shows the icons of levels on map, and blits it.
    display = pygame.display.get_surface()

    # name is name of the enemy, concatenated with the string to get dict key
    ui_data[name + '_map_icon_blit_rect'] = display.blit(icon_img, icon_rect)

def check_icon_highlight(name, blit_rect, ui_data):
    # gets mouse position, if mouse is on rect, then sets image as highlighted image
    pos = pygame.mouse.get_pos()
    if blit_rect.collidepoint(pos):
        ui_data[name + '_map_icon_img'] = ui_data[name + '_map_icon_h']
    # otherwise the normal image is set on the surface.
    else:
        ui_data[name + '_map_icon_img'] = ui_data[name + '_map_icon_n']

def check_icon_click(ui_data, event_list):
    # checks if mouse is clicked, checks if mouse is on a level rect and starts the level
    for event in event_list:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            for enemy in enemy_list:
                if ui_data[enemy + '_map_icon_blit_rect'].collidepoint(pos):

                    # setting some timers and states
                    ui_data['current_state'] = screens[enemy]
                    
                    # music, ADD A BOOL TO TURN IT OFF -------------------------------------------------
                    click = pygame.mixer.Sound('./audio/sfx/ui/button_click.wav')
                    click.play()
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load('./audio/black_warrior.mp3')
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)

                    break

def run_level_map(ui_data, event_list, player_state):
    show_map(ui_data)

    show_map_icon(ui_data['thawk_map_icon_img'], ui_data['thawk_map_icon_rect'], 'thawk', ui_data)
    show_map_icon(ui_data['chunli_map_icon_img'], ui_data['chunli_map_icon_rect'], 'chunli', ui_data)

    check_icon_highlight('thawk', ui_data['thawk_map_icon_blit_rect'], ui_data)
    check_icon_highlight('chunli', ui_data['chunli_map_icon_blit_rect'], ui_data)

    check_icon_click(ui_data, event_list)

    show_coin_frame(ui_data, player_state)