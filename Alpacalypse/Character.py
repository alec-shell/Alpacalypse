"""
Character.py: Class for all character sprites.
"""

import config
from Fireball import Fireball
import os
import pygame
import time


class Character(pygame.sprite.Sprite):
    def __init__(self, img_file, x_coord, y_coord, speed, health, health_scaler = 1, img_scaler = 1):
        super().__init__()
        # image and image rect vars
        walk_imgs = os.listdir(f"img/{img_file}")
        walk_imgs.sort()
        self.walk_img_list = [pygame.transform.scale(pygame.image.load(f"img/{img_file}/{img}"),
                                                     (35 * img_scaler, 60 * img_scaler)) for img in walk_imgs]
        self.walk_img_index = 0
        self.rect = self.walk_img_list[0].get_rect()
        self.img_time = time.time()
        self.img_update_rate = .1
        # position vars
        self.rect.centerx = x_coord
        self.rect.bottom = y_coord - config.BLOCK_SIZE
        # movement vars
        self.speed = speed
        self.is_running = True
        self.is_facing_left = False
        # health vars
        self.start_health = health * health_scaler
        self.current_health = self.start_health
        # jumping vars
        self.jump_strength = -10
        self.velocity = 0
        self.gravity = .5
        self.is_on_ground = True
        # fireball vars
        self.fireball_cooldown = 1
        self.fireball_time = time.time()


    def update(self, lvl_map, screen):
        self.apply_gravity()
        self.detect_floor(lvl_map)


    def generate_sprite_img(self):
        # running animation
        if self.is_running:
            return self.walking_animation()
        # if no movement input or running into wall
        else:
            if self.is_facing_left:
                return pygame.transform.flip(self.walk_img_list[0], True, False)
        return self.walk_img_list[0]


    def walking_animation(self):
        if self.is_facing_left:
            sprite_img = pygame.transform.flip(self.walk_img_list[self.walk_img_index], True, False)
        else:
            sprite_img = self.walk_img_list[self.walk_img_index]
        if time.time() - self.img_time > self.img_update_rate:
            self.walk_img_index = self.walk_img_index + 1 if self.walk_img_index + 1 < len(self.walk_img_list) else 0
            self.img_time = time.time()
        return sprite_img


    def move(self, left, right, lvl_map):
        if left:
            self.is_facing_left = True
            if not self.detect_wall(lvl_map, True, False):
                self.is_running = True
                self.rect.x -= self.speed
            else:
                self.is_running = False
        elif right:
            self.is_facing_left = False
            if not self.detect_wall(lvl_map, False, True):
                self.is_running = True
                self.rect.x += self.speed
            else:
                self.is_running = False


    def apply_gravity(self):
        if not self.is_on_ground:
            self.velocity += self.gravity
            self.rect.y += self.velocity


    def jump(self):
        if self.is_on_ground:
            self.is_on_ground = False
            self.velocity += self.jump_strength
            self.rect.y += self.velocity


    def detect_floor(self, lvl_map):
        # Define block positions above and below character
        x_left = self.rect.left // config.BLOCK_SIZE
        x_right = self.rect.right // config.BLOCK_SIZE
        bot_y = self.rect.bottom // config.BLOCK_SIZE
        # check if falling through open space
        if lvl_map[bot_y][x_left] == 0 and lvl_map[bot_y][x_right] == 0:
            self.is_on_ground = False
        # Check for ground collision
        elif (((lvl_map[bot_y][x_left] != 0
                and x_left * config.BLOCK_SIZE <= self.rect.left + config.SPRITE_COLLISION_OFFSET <= x_left * config.BLOCK_SIZE + config.BLOCK_SIZE)  # Left foot on ground?
               or (lvl_map[bot_y][x_right] != 0
                   and x_right * config.BLOCK_SIZE <= self.rect.right - config.SPRITE_COLLISION_OFFSET <= x_right * config.BLOCK_SIZE + config.BLOCK_SIZE))  # Right foot on ground?
              and self.rect.y <= bot_y * config.BLOCK_SIZE): # Sprite's rect.bottom aligned with ground's y-axis?
            self.is_on_ground = True
            self.rect.bottom = bot_y * config.BLOCK_SIZE
            self.velocity = 0


    def detect_ceil(self, lvl_map):
        # Define block positions above character
        x_left = self.rect.left // config.BLOCK_SIZE
        x_right = self.rect.right // config.BLOCK_SIZE
        top_y = self.rect.top // config.BLOCK_SIZE
        # Check for ceiling collision
        if (((lvl_map[top_y][x_left] != 0
              and x_left * config.BLOCK_SIZE <= self.rect.left + config.SPRITE_COLLISION_OFFSET <= x_left * config.BLOCK_SIZE + config.BLOCK_SIZE)  # Top left below ceiling?
             or (lvl_map[top_y][x_right] != 0
                 and x_right * config.BLOCK_SIZE <= self.rect.right - config.SPRITE_COLLISION_OFFSET <= x_right * config.BLOCK_SIZE + config.BLOCK_SIZE)) # Top right below ceiling?
            and top_y * config.BLOCK_SIZE + config.BLOCK_SIZE >= self.rect.top - config.SPRITE_COLLISION_OFFSET): # Sprite's rect.top about to impact ceiling?
            self.velocity = 0


    def detect_wall(self, lvl_map, left, right):
        # Define block positions to left and right of character
        top_y = self.rect.top // config.BLOCK_SIZE
        bottom_y = self.rect.bottom // config.BLOCK_SIZE - 1
        left_x = self.rect.left // config.BLOCK_SIZE
        right_x = self.rect.right // config.BLOCK_SIZE
        # Check collision if moving left
        if (left
                and ((lvl_map[top_y][left_x] != 0
                and top_y * config.BLOCK_SIZE + config.BLOCK_SIZE >= self.rect.top >= top_y * config.BLOCK_SIZE)
                or (lvl_map[bottom_y][left_x] != 0
                and bottom_y * config.BLOCK_SIZE + config.BLOCK_SIZE >= self.rect.bottom >= bottom_y * config.BLOCK_SIZE))):
            return True
        # Check collision if moving right
        if (right
                and ((lvl_map[top_y][right_x] != 0
                and top_y * config.BLOCK_SIZE + config.BLOCK_SIZE >= self.rect.top >= top_y * config.BLOCK_SIZE)
                or (lvl_map[bottom_y][right_x] != 0
                and bottom_y * config.BLOCK_SIZE + config.BLOCK_SIZE >= self.rect.bottom >= bottom_y * config.BLOCK_SIZE))):
            return True
        return False


    def fireball_is_cooled_down(self):
        if time.time() - self.fireball_time > self.fireball_cooldown:
            self.fireball_time = time.time()
            return True
        return False


    def fire_fireball(self):
        if self.fireball_is_cooled_down():
            return Fireball(config.ORANGE_FIREBALL_FILE, config.PLAYER_FIREBALL_SPEED, config.PLAYER_FIREBALL_DAMAGE, self.rect.centerx,
                            self.rect.y + (self.rect.height / 2), self.is_facing_left, "player")
        return None
