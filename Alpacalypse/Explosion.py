"""
Explosion.py: Explosion animation class.
"""

import config
import os
import pygame
import time


class Explosion(pygame.sprite.Sprite):
    def __init__(self, src_type, x_coord, y_coord):
        super().__init__()
        self.src_type = src_type
        img_list = os.listdir(f"img/{config.ORANGE_EXPLOSION_FILE}")
        img_list.sort()
        self.exp_size = self.set_exp_size()
        self.imgs = [pygame.transform.scale(pygame.image.load(f"img/{config.ORANGE_EXPLOSION_FILE}/{img}"), (self.exp_size, self.exp_size)) for img in img_list]
        self.rect = self.imgs[0].get_rect()
        self.rect.centerx = x_coord
        self.rect.bottom = y_coord
        self.img_index = 0
        self.img_timer = time.time()


    def generate_sprite_img(self):
        if time.time() - self.img_timer > config.EXPLOSION_ANIMATION_COOLDOWN:
            self.img_timer = time.time()
            self.img_index += 1
        if self.img_index < len(self.imgs):
            return self.imgs[self.img_index]
        return None


    def set_exp_size(self):
        if self.src_type == "megalopaca":
            return config.EXPLOSION_SIZE * config.MEGALPACA_EXPLOSION_SCALAR
        else:
            return config.EXPLOSION_SIZE