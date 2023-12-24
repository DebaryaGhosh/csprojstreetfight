import pygame
from settings import *

def show_map(ui_data):
    # blits the map
    pygame.display.get_surface().blit(ui_data['level_map'], ui_data['level_map_rect'])


def show_coin_frame(ui_data, client_data):
    # blits the coin frame background, gets coin data, blits the text
    display = pygame.display.get_surface()

    display.blit(ui_data['coinmeter_img'], ui_data['coinmeter_rect']) # frame

    coins = ui_data['coins_font'].render(str(client_data['coins']), False, 'white')
    
    # offset to adjust the coins_rect
    coins_rect = coins.get_rect(topright = display.get_rect().topright + pygame.math.Vector2(-20, 10))
    display.blit(coins, coins_rect) # text

def show_upgrade_frame(ui_data, client_data):
    display = pygame.display.get_surface()

    ui_data['upgradevec_attack_blit'] = display.blit(ui_data['upgradevec_img'], ui_data['upgradevec_rect_attack']) 
    ui_data['upgradevec_defense_blit'] = display.blit(ui_data['upgradevec_img'], ui_data['upgradevec_rect_defense']) 

    # attack 
    fist_rect = display.blit(ui_data['fist_img'], ui_data['fist_rect'])
    attack_text = ': ' + str(client_data['attack'])
    attack_text_render = ui_data['upgrades_font'].render(attack_text, False, 'black')
    attack_text_rect = attack_text_render.get_rect(topleft = fist_rect.topright + pygame.math.Vector2(0, 10))
    display.blit(attack_text_render, attack_text_rect)

    # defense
    shield_rect = display.blit(ui_data['shield_img'], ui_data['shield_rect'])
    defense_text = ': ' + str(client_data['defense'])
    defense_text_render = ui_data['upgrades_font'].render(defense_text, False, 'black')
    defense_text_rect = defense_text_render.get_rect(topleft = shield_rect.topright + pygame.math.Vector2(0, 10))
    display.blit(defense_text_render, defense_text_rect)

    upgrade_text = ui_data['upgrades_font'].render('UPGRADE', False, 'black')
    upgrade_text_rect_attack = upgrade_text.get_rect(bottomright = ui_data['upgradevec_attack_blit'].bottomright + pygame.math.Vector2(-40, -30))
    upgrade_text_rect_defense = upgrade_text.get_rect(bottomright = ui_data['upgradevec_defense_blit'].bottomright + pygame.math.Vector2(-40, -30))
    display.blit(upgrade_text, upgrade_text_rect_attack)
    display.blit(upgrade_text, upgrade_text_rect_defense)

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

def check_icon_click(ui_data, event_list, client_data):
    # checks if mouse is clicked, checks if mouse is on a level rect and starts the level
    for event in event_list:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            for enemy in enemy_list:
                if ui_data[enemy + '_map_icon_blit_rect'].collidepoint(pos):

                    # setting some timers and states
                    ui_data['current_state'] = screens[enemy]
                    
                    # music, ADD A BOOL TO TURN IT OFF -------------------------------------------------
                    try:
                        click = pygame.mixer.Sound('./audio/sfx/ui/button_click.wav')
                        click.play()
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load('./audio/black_warrior.mp3')
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1)
                    except:
                        print('audio device not detected.')
                    return
            for item in ['attack', 'defense']:
                if ui_data['upgradevec_' + item + '_blit'].collidepoint(pos):
                    if client_data['coins'] >= UPGRADE_COST:
                        client_data[item] += UPGRADE_INCREMENT
                        client_data['coins'] -= UPGRADE_COST
                    return


def run_level_map(ui_data, event_list, client_data):
    show_map(ui_data)

    show_map_icon(ui_data['thawk_map_icon_img'], ui_data['thawk_map_icon_rect'], 'thawk', ui_data)
    show_map_icon(ui_data['chunli_map_icon_img'], ui_data['chunli_map_icon_rect'], 'chunli', ui_data)

    check_icon_highlight('thawk', ui_data['thawk_map_icon_blit_rect'], ui_data)
    check_icon_highlight('chunli', ui_data['chunli_map_icon_blit_rect'], ui_data)

    show_coin_frame(ui_data, client_data)
    show_upgrade_frame(ui_data, client_data)

    check_icon_click(ui_data, event_list, client_data)