import pygame
from settings import *

def animate_background(ui_data):
    animation = ui_data['intro_backgrounds']

    ui_data['background_anim_frameindex'] += ui_data['background_anim_speed']

    if ui_data['background_anim_frameindex'] >= len(animation):
        ui_data['background_anim_frameindex'] = 0
    
    ui_data['intro_background_img'] = animation[int(ui_data['background_anim_frameindex'])]

def show_background(ui_data):
    display = pygame.display.get_surface()
    offset = pygame.math.Vector2(20, 20)
    display.blit(ui_data['intro_background_img'], ui_data['intro_background_rect'].topleft - offset)

def show_logo(ui_data):
    display = pygame.display.get_surface()
    offset = pygame.math.Vector2(0, 50)
    display.blit(ui_data['logo_img'], ui_data['logo_rect'].topleft - offset)

def show_button(surf, rect, offset, ui_data):
    display = pygame.display.get_surface()
    ui_data['play_blit_rect'] = display.blit(surf, rect.topleft + offset)

def check_button_click(ui_data, event_list):
    for event in event_list:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if ui_data['play_blit_rect'].collidepoint(pos):
                ui_data['current_state'] = 'level'

def run_intro(ui_data, event_list):

    # backgrounds
    animate_background(ui_data)
    show_background(ui_data)

    # logo
    show_logo(ui_data)

    # buttons
    show_button(ui_data['play_img'], ui_data['play_rect'], pygame.math.Vector2(0, 150), ui_data)

    # check if buttons are clicked
    check_button_click(ui_data, event_list)


