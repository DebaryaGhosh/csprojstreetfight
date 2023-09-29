import pygame
from settings import *

def show_bar(current, max_amount, bg_rect, color, entity_state, data1, data2):
    display_surface = pygame.display.get_surface()
    
    if entity_state['name'] == 'player':
        ratio = 1 - int(current) / max_amount
        pygame.draw.rect(display_surface, PLAYER_UI_BG_COLOR, bg_rect)
    else:
        ratio = (int(current) / max_amount)
        pygame.draw.rect(display_surface, ENEMY_UI_BG_COLOR, bg_rect)
    current_width = bg_rect.width * ratio
    current_rect = bg_rect.copy()
    current_rect.width = current_width

    
    pygame.draw.rect(display_surface, color, current_rect)
    pygame.draw.rect(display_surface, UI_BORDER_COLOR, bg_rect, width=3,)

    offset = None
    if data2['bgshake']:
        offset = entity_state['rect'].topleft - data2['shake_offset'] + pygame.math.Vector2(0, -30)
    else:
        offset = entity_state['rect'].topleft - data2['offset'] + pygame.math.Vector2(0, -30)
    
    # hitboxrect = pygame.Rect(offset[0], offset[1], entity_state['hitbox'].width, entity_state['hitbox'].height)
    # pygame.draw.rect(pygame.display.get_surface(), 'red', hitboxrect, width=3)

def show_mugshot(image, bg_rect):
    display_surface = pygame.display.get_surface()
    image_rect = image.get_rect(center = bg_rect.center)
    display_surface.blit(image, image_rect)

def update_timer(timer_rect, time_start, max_time, font):
    display_surface = pygame.display.get_surface()
    time_passed = pygame.time.get_ticks() - time_start
    time_left = (max_time - time_passed) // 1000

    minutes = time_left // 60
    seconds = time_left % 60

    if minutes < 10:
        minutes = '0' + str(minutes)
    if seconds < 10:
        seconds = '0' + str(seconds)

    time_left = str(minutes) + ':' + str(seconds)


    text_surface = font.render(time_left, False, 'white')
    
    text_rect = text_surface.get_rect(center=timer_rect.center)
    #pygame.draw.rect(display_surface, UI_BORDER_COLOR, timer_rect)
    display_surface.blit(text_surface, text_rect)

def show_names(ui_data):
    ryu_text = ui_data['names_font'].render('RYU', False, 'white')
    thawk_text = ui_data['names_font'].render('T-HAWK', False, 'white')

    pygame.display.get_surface().blit(ryu_text, ui_data['ryu_name_rect'])
    pygame.display.get_surface().blit(thawk_text, ui_data['thawk_name_rect'])
    

def display(player_data, enemy_data, ui_data, data):
    show_bar(player_data['health'], player_data['stats']['health'], ui_data['player_health_bar_rect'], PLAYER_HEALTH_COLOR, player_data, data[0], data[2])
    show_mugshot(ui_data['ryu_mug'], ui_data['player_mugshot_rect'])

    show_bar(enemy_data['health'], enemy_data['stats']['health'], ui_data['enemy_health_bar_rect'], ENEMY_HEALTH_COLOR, enemy_data, data[1], data[2])
    show_mugshot(ui_data['thawk_mug'], ui_data['enemy_mugshot_rect'])

    update_timer(ui_data['timer_rect'], ui_data['timer_start'], ui_data['max_time'], ui_data['timer_font'])

    show_names(ui_data)
    