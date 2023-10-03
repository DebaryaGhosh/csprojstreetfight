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

def update_transition_anim(ui_data):
        if ui_data['intro_alpha'] > 0:
            ui_data['intro_background_img'].set_alpha(int(ui_data['intro_alpha']))
            ui_data['intro_alpha'] -= 2.5
            if ui_data['intro_alpha'] <= 0:
                ui_data['logo_alpha_transition_delay_time'] = pygame.time.get_ticks()

        if ui_data['intro_alpha'] <= 0:
            current_time = pygame.time.get_ticks()
            if current_time - ui_data['logo_alpha_transition_delay_time'] >= ui_data['logo_alpha_transition_delay']:
                ui_data['logo_img'].set_alpha(int(ui_data['logo_alpha']))
                ui_data['logo_alpha'] -= 10
        
        if ui_data['logo_alpha'] <= 0:
            ui_data['current_state'] = screens['map']


def check_button_click(ui_data, event_list):
    for event in event_list:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if ui_data['play_blit_rect'].collidepoint(pos):
                ui_data['transition'] = True
                ui_data['play_alpha'] = 0
                click = pygame.mixer.Sound('./audio/sfx/ui/button_click.wav')
                click.play()
                

def run_intro(ui_data, event_list):

    # backgrounds
    if ui_data['intro_alpha'] > 0:
        animate_background(ui_data)
    if ui_data['transition']:
        update_transition_anim(ui_data)
    show_background(ui_data)

    # logo
    show_logo(ui_data)

    # buttons
    ui_data['play_img'].set_alpha(ui_data['play_alpha'])
    show_button(ui_data['play_img'], ui_data['play_rect'], pygame.math.Vector2(0, 150), ui_data)

    # check if buttons are clicked
    if not ui_data['transition']:
        check_button_click(ui_data, event_list)
        