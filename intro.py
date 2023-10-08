import pygame
from settings import *

def animate_background(ui_data):

    # gets the animaton frames list, increases frame by speed and sets the image
    animation = ui_data['intro_backgrounds']

    ui_data['background_anim_frameindex'] += ui_data['background_anim_speed']

    # setting frame to 0 so that animation runs in a loop
    if ui_data['background_anim_frameindex'] >= len(animation):
        ui_data['background_anim_frameindex'] = 0
    
    ui_data['intro_background_img'] = animation[int(ui_data['background_anim_frameindex'])]
    

def show_background(ui_data):
    # blitting the intro screen background 
    display = pygame.display.get_surface()
    offset = pygame.math.Vector2(20, 20)
    display.blit(ui_data['intro_background_img'], ui_data['intro_background_rect'].topleft - offset)

def show_logo(ui_data):
    # blitting the game logo 
    display = pygame.display.get_surface()
    offset = pygame.math.Vector2(0, 50)
    display.blit(ui_data['logo_img'], ui_data['logo_rect'].topleft - offset)

def show_button(name, ui_data):
    # blits the button at a specific rect, with an offset
    display = pygame.display.get_surface()
    ui_data[name + '_img'].set_alpha(ui_data[name + '_alpha'])
    ui_data[name + '_blit_rect'] = display.blit(ui_data[name + '_img'], ui_data[name + '_rect'])

def update_transition_anim(ui_data):
        # checks if background has any opacity
        if ui_data['intro_alpha'] > 0:
            # if it does, then the opacity is reduced by the given amount
            ui_data['intro_background_img'].set_alpha(int(ui_data['intro_alpha']))
            ui_data['intro_alpha'] -= 2.5

            # checks if the image is transparent to start timer for next transition
            if ui_data['intro_alpha'] <= 0: 
                ui_data['logo_alpha_transition_delay_time'] = pygame.time.get_ticks()
        
        # if intro background has become transparent
        if ui_data['intro_alpha'] <= 0:
            current_time = pygame.time.get_ticks()
            # we will start reducing the opacity of the logo, but ONLY after it has been 'logo_alpha_transition_delay' ms
            if current_time - ui_data['logo_alpha_transition_delay_time'] >= ui_data['logo_alpha_transition_delay']:
                ui_data['logo_img'].set_alpha(int(ui_data['logo_alpha']))
                ui_data['logo_alpha'] -= 10
        
        # if logo has become transparent as well, then we switch screens to map.
        if ui_data['logo_alpha'] <= 0:
            ui_data['current_state'] = screens['map']


def check_button_click(name, ui_data, event_list):

    # checks if user clicked on play button, then sets transition to True which plays transition and switches screens
    for event in event_list:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if ui_data[name + '_blit_rect'].collidepoint(pos):
                # a click sound.
                click = pygame.mixer.Sound('./audio/sfx/ui/button_click.wav')
                click.play()
                return True
    return False

def highlight_button(name, blit_rect, ui_data):

    # if mouse pointer is on button, it highlights it.
    pos = pygame.mouse.get_pos()
    if blit_rect.collidepoint(pos):
        ui_data[name + '_img'] = ui_data[name + '_h']
    else:
        ui_data[name + '_img'] = ui_data[name + '_n']
                

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
    show_button('play', ui_data)
    highlight_button('play', ui_data['play_blit_rect'], ui_data)

    # check if buttons are clicked
    if not ui_data['transition']:
        if check_button_click('play', ui_data, event_list):
            ui_data['transition'] = True
            ui_data['play_alpha'] = 0         # the button is made transparent
        