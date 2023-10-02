import pygame
from settings import *

def show_map(ui_data):
    pygame.display.get_surface().blit(ui_data['level_map'], ui_data['level_map_rect'])

def run_level_map(ui_data):
    show_map(ui_data)
