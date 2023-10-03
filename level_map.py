import pygame
from settings import *

def show_map(ui_data, event_list):
    pygame.display.get_surface().blit(ui_data['level_map'], ui_data['level_map_rect'])
    for event in event_list:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            print(pygame.mouse.get_pos())

def show_coin_frame(ui_data):
    pass

def show_map_icon(icon_img, icon_rect, name, ui_data):
    display = pygame.display.get_surface()

    ui_data[name + '_map_icon_blit_rect'] = display.blit(icon_img, icon_rect)

def check_icon_highlight(name, blit_rect, ui_data):
    pos = pygame.mouse.get_pos()
    if blit_rect.collidepoint(pos):
        ui_data[name + '_map_icon_img'] = ui_data[name + '_map_icon_h']
    else:
        ui_data[name + '_map_icon_img'] = ui_data[name + '_map_icon_n']

def check_icon_click(ui_data, event_list):
    for event in event_list:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if ui_data['thawk_map_icon_blit_rect'].collidepoint(pos):
                ui_data['current_state'] = screens['level']
                ui_data['timer_start'] = pygame.time.get_ticks()
                click = pygame.mixer.Sound('./audio/sfx/ui/button_click.wav')
                click.play()
                pygame.mixer.music.stop()
                pygame.mixer.music.load('./audio/forest_of_death.mp3')
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)



def run_level_map(ui_data, event_list):
    show_map(ui_data, event_list)
    show_map_icon(ui_data['thawk_map_icon_img'], ui_data['thawk_map_icon_rect'], 'thawk', ui_data)
    check_icon_highlight('thawk', ui_data['thawk_map_icon_blit_rect'], ui_data)
    check_icon_click(ui_data, event_list)

