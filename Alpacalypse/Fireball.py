"""
Fireball.py: Fireball object class
"""

import config
import os
import pygame
import time


class Fireball(pygame.sprite.Sprite):
    def __init__(self, img_file, speed, damage, x_coord, y_coord, left, origin):
        pygame.sprite.Sprite.__init__(self)
        self.origin = origin
        self.scalar = self.assign_scalar()
        imgs = os.listdir(f"img/{img_file}")
        self.img_list = [pygame.transform.scale(pygame.image.load(f"img/{img_file}/{img}"), (20 * self.scalar, 20 * self.scalar)) for img in imgs]
        self.img_index = 0
        self.img_interval = 0.2
        self.speed = speed
        self.damage = damage
        self.rect = self.img_list[0].get_rect()
        self.start_x = x_coord
        self.rect.centerx = x_coord - self.rect.width if left else x_coord + self.rect.width
        self.rect.y = y_coord
        self.moving_left = left
        self.time = time.time()


    def update(self, lvl_map, map_width, enemies_list, player_rect):
        collision_code = self.detect_collision(lvl_map, map_width, enemies_list, player_rect)
        if collision_code == -1:
            self.move()
        return collision_code


    def assign_scalar(self):
        if self.origin == "player":
            return config.PLAYER_FIREBALL_SCALER
        elif self.origin == "llama":
            return config.LLAMA_FIREBALL_SCALER
        elif self.origin == "megalopaca":
            return config.MEGALOPACA_FIREBALL_SCALER
        else:
            return config.PLAYER_FIREBALL_SCALER


    def generate_sprite_img(self):
        img = self.img_list[self.img_index]
        if time.time() - self.time > self.img_interval:
            self.time = time.time()
            self.img_index += 1
            if self.img_index == len(self.img_list):
                self.img_index = 0
        return img


    def move(self):
        if self.moving_left:
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


    def detect_collision(self, lvl_map, map_width, enemies_list, player_rect):
        # bounds limit
        if self.moving_left and self.rect.centerx + 300 <= self.start_x\
                or not self.moving_left and self.rect.centerx - 300 >= self.start_x:
            return -2
        y = self.rect.centery // config.BLOCK_SIZE
        x = self.rect.centerx // config.BLOCK_SIZE
        # -1 == no collision, -2 == wall/boundary collision, -3 == player collision, enemies_list index == enemy collision
        if x < 0 or x >= map_width // config.BLOCK_SIZE or lvl_map[y][x] != 0:
            return -2
        if self.origin != "player":
            if player_rect.colliderect(self.rect):
                return -3
        elif self.origin == "player":
            for enemy in range(len(enemies_list)):
                if enemies_list[enemy].rect.colliderect(self.rect):
                    return enemy
        return -1
