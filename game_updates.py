import pygame
import player
import entity
import enemy
from level_ui import display
from random import randint
from intro import show_button
from intro import highlight_button
from intro import check_button_click
from settings import *

# updates the player. 
def update_player(player_state, enemy_state, attack_data, background_data, ui_data, event_list):
    player.get_status(player_state)
    player.key_input(player_state)
    entity.move_entity(player_state)
    player.get_status(player_state)
    entity.animate(player_state, enemy_state, attack_data, background_data, ui_data)
    player.collisions(player_state)
    player.cooldowns(player_state)

def update_enemy(enemy_state, player_state, background_data, attack_data, ui_data, event_list):
    enemy.get_status(enemy_state)
    enemy.enemy_ai(enemy_state, player_state, background_data)
    entity.move_entity(enemy_state)
    entity.animate(enemy_state, player_state, attack_data, background_data, ui_data)
    enemy.collisions(enemy_state)
    enemy.cooldowns(enemy_state)

def update_background(background_data, player):
    background_data['bgshake'] = False
    if pygame.time.get_ticks() - background_data['bgshake_time'] < background_data['bgshake_cooldown']:
        background_data['shake_offset'].x = background_data['offset'].x + randint(-background_data['bgshake_amp'], background_data['bgshake_amp'])
        background_data['shake_offset'].y = background_data['offset'].y + randint(-background_data['bgshake_amp'], background_data['bgshake_amp'])
        background_data['bgshake'] = True

    for index, background in enumerate(background_data['backgrounds']):
        if player['rect'].x > 485 and player['rect'].x < 1140:
            background_data['offset'].x = player['rect'].centerx - background_data['half_width']
        if player['rect'].y > 100:
            background_data['offset'].y = player['rect'].centery - background_data['half_height']

        rect = background.get_rect(topleft = (0, -150))
        bg_offset = pygame.math.Vector2()
        if background_data['bgshake']:
            bg_offset.x = (rect.topleft[0] - background_data['shake_offset'].x) * background_data['bgspeed_' + str(index)]
            bg_offset.y = rect.topleft[1] - background_data['shake_offset'].y
        else:
            bg_offset.x = (rect.topleft[0] - background_data['offset'].x) * background_data['bgspeed_' + str(index)]
            bg_offset.y = rect.topleft[1] - background_data['offset'].y
        
        pygame.display.get_surface().blit(background, bg_offset)

def update_ui(enemy_name, ui_data, data):
    display(enemy_name, data[0], data[1], ui_data, data)

def blit_entities(player_state, enemy_state, background_data):
    screen = pygame.display.get_surface()
    player_offset_fix = pygame.math.Vector2(0, 80)
    enemy_offset_fix = pygame.math.Vector2(0, -80)


    if background_data['bgshake']:
        player_state['offset'] = player_state['rect'].topleft - background_data['shake_offset'] + player_offset_fix
        enemy_state['offset'] = enemy_state['rect'].topleft - background_data['shake_offset'] + enemy_offset_fix
    else:
        player_state['offset'] = player_state['rect'].topleft - background_data['offset'] + player_offset_fix
        enemy_state['offset'] = enemy_state['rect'].topleft - background_data['offset'] + enemy_offset_fix

    screen.blit(enemy_state['image'], enemy_state['offset'])
    screen.blit(player_state['image'], player_state['offset'])

def countdown(ui_data):
    display = pygame.display.get_surface()
    current_time = pygame.time.get_ticks()
    time_passed = current_time - ui_data['countdown_text_time']
    if time_passed <= ui_data['countdown_text_duration']:
        ui_data['countdown_mask'].set_alpha(100)
        display.blit(ui_data['countdown_mask'], ui_data['countdown_mask_rect'])
        if time_passed < 3000:
            # numbers
            number = 3 - int(time_passed / 1000)
            path = 'count' + str(number) + '_text'
            text = ui_data[path]
            rect = ui_data[path + '_rect']

            display.blit(text, rect)
        else:
            # fight text
            display.blit(ui_data['fight_text'], ui_data['fight_text_rect'])
        
        return True
    return False

def check_game_over(player_state, enemy_state, level_state):
    if player_state['health'] <= 0:
        level_state['game_over'] = True
        level_state['game_won'] = False
    elif enemy_state['health'] <= 0:
        level_state['game_over'] = True
        level_state['game_won'] = True

def game_over(ui_data, event_list, level_state, game_state):
    
    display = pygame.display.get_surface()
    mask = ui_data['countdown_mask']
    mask_rect = ui_data['countdown_mask_rect']
    display.blit(mask, mask_rect)

    if level_state['game_won']:
        you_win_text = ui_data['youwin_text']
        you_win_rect = ui_data['youwin_text_rect']
        display.blit(you_win_text, you_win_rect)

    else:
        you_lose_text = ui_data['youlose_text']
        you_lose_rect = ui_data['youlose_text_rect']
        display.blit(you_lose_text, you_lose_rect)

    show_button('next', ui_data)
    highlight_button('next', ui_data['next_blit_rect'], ui_data)
    if check_button_click('next', ui_data, event_list):
        game_state['initialized_game'] = False
        level_state['game_over'] = False
        level_state['game_won'] = False
        ui_data['current_state'] = screens['map']
        pygame.mixer.music.load('./audio/menu.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
