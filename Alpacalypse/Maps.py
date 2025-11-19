"""
Maps.py: Build and load level maps
"""

import config
from Enemy import Enemy
from Item import Item
from Portal import Portal
import pygame
import random


def build_level(file):
    lvl, lvl_imgs, enemies_list, items = [], [], [], []
    backdrop = None
    player_start_pos = None
    portal = None
    with open(f'levels/{file}', 'r') as file:
        for line in file:
            if line.startswith("backdrop = "):
                backdrop_file = f"img/background/Backdrop/{line.replace('backdrop = ', '').strip()}"
                backdrop = pygame.image.load(backdrop_file.strip())
                continue
            lvl_line, img_line = [], []
            for index, character in enumerate(line.split(",")):
                if character == '\n':
                    continue
                # Define empty space
                if character == '00':
                    lvl_line.append(0)
                    img_line.append(None)
                # Add stone and grass blocks
                elif character == '01' or character == '02':
                    lvl_line.append(int(character))
                    img_file = config.BLOCK_FILE_PATHS[int(character)][random.randint(0, len(config.BLOCK_FILE_PATHS[int(character)]) - 1)]
                    img_line.append(pygame.transform.scale(pygame.image.load(img_file), (config.BLOCK_SIZE, config.BLOCK_SIZE)))
                elif character == '03' or character == '04':
                    lvl_line.append(int(character))
                    img_file = config.BLOCK_FILE_PATHS[int(character)][0]
                    img_line.append(pygame.transform.scale(pygame.image.load(img_file), (config.BLOCK_SIZE, config.BLOCK_SIZE)))
                # Place enemy
                elif character == '05':
                    lvl_line.append(0)
                    img_line.append(None)
                    enemies_list.append(Enemy(config.ENEMY_IMG_FILE,
                                              index * config.BLOCK_SIZE,
                                              (len(lvl) + 1) * config.BLOCK_SIZE,
                                              config.ENEMY_SPEED,
                                              config.ENEMY_HEALTH,
                                              "llama"))
                # player's starting position
                elif character == '06':
                    lvl_line.append(0)
                    img_line.append(None)
                    player_start_pos = (index * config.BLOCK_SIZE, (len(lvl) + 1) * config.BLOCK_SIZE)
                # health potion
                elif character == '07':
                    lvl_line.append(0)
                    img_line.append(None)
                    items.append(Item("health", index * config.BLOCK_SIZE, (len(lvl) + 1) * config.BLOCK_SIZE))
                # level_up potion
                elif character == '08':
                    lvl_line.append(0)
                    img_line.append(None)
                    items.append(Item("level_up", index * config.BLOCK_SIZE, (len(lvl) + 1) * config.BLOCK_SIZE))
                elif character == '09':
                    lvl_line.append(0)
                    img_line.append(None)
                    portal = Portal(index * config.BLOCK_SIZE, (len(lvl) + 1) * config.BLOCK_SIZE)
                elif character == '10':
                    lvl_line.append(0)
                    img_line.append(None)
                    enemies_list.append(Enemy(config.ENEMY_IMG_FILE,
                                              index * config.BLOCK_SIZE,
                                              (len(lvl) + 1) * config.BLOCK_SIZE,
                                              config.ENEMY_SPEED,
                                              config.ENEMY_HEALTH,
                                              "megalopaca",
                                              5,
                                              5,
                                              40))
            lvl.append(lvl_line)
            lvl_imgs.append(img_line)
    # return backdrop img, level map, img map, enemy object list, player starting position, and items object list
    return backdrop, lvl, lvl_imgs, enemies_list, player_start_pos, items, portal


def draw_background(screen, lvl_imgs, backdrop):
    # fill blank space
    screen.blit(backdrop, (0, 0))
    # loop and blit images
    for i in range(len(lvl_imgs)):
        for j in range(len(lvl_imgs[0])):
            if lvl_imgs[i][j] is not None:
                screen.blit(lvl_imgs[i][j], (j * config.BLOCK_SIZE, i * config.BLOCK_SIZE))
