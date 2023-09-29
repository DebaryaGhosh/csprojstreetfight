import pygame
from os import walk

def import_folder(path):
    surface_list = []

    for _, _, image_files in walk(path):
        for image_name in image_files:
            full_path = path + '/' + image_name
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

        return surface_list