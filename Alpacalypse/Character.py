"""
Character.py: Class for player and enemies.
"""

import config
from Fireball import Fireball
import os
import pygame
import pygame.font
import time

pygame.font.init()


class Character(pygame.sprite.Sprite):
    def __init__(self, img_file, x_coord, y_coord, speed, health, health_scaler = 1, img_scaler = 1):
        super().__init__()
        # image and image rect vars
        walk_imgs = os.listdir(f"img/{img_file}")
        walk_imgs.sort()
        shield_imgs = os.listdir(f"img/character/Sorcerer/Crouching")
        shield_imgs.sort()
        jump_imgs = os.listdir(f"img/character/Sorcerer/Jumping")
        jump_imgs.sort()
        self.shield_img_list = [pygame.transform.scale(pygame.image.load(f"img/character/Sorcerer/Crouching/{img}"),
                                                       (77 * img_scaler, 70 * img_scaler)) for img in shield_imgs]
        self.walk_img_list = [pygame.transform.scale(pygame.image.load(f"img/{img_file}/{img}"),
                                                     (35 * img_scaler, 60 * img_scaler)) for img in walk_imgs]
        self.jump_img_list = [pygame.transform.scale(pygame.image.load(f"img/character/Sorcerer/Jumping/{img}"),
                                               (35 * img_scaler, 60 * img_scaler)) for img in jump_imgs]
        self.walk_img_index = 0
        self.shield_img_index = 0
        self.jump_img_index = 0
        self.rect = self.walk_img_list[0].get_rect()
        self.img_time = time.time()
        self.img_update_rate = .1
        # position vars
        self.rect.left = x_coord
        self.rect.bottom = y_coord - config.BLOCK_SIZE
        # movement vars
        self.speed = speed
        self.is_running = True
        self.is_facing_left = False
        # health vars
        self.start_health = health * health_scaler
        self.current_health = self.start_health
        # jumping vars
        self.velocity = 0
        self.gravity = .5
        self.jump_strength = -10
        self.is_on_ground = True
        # fireball vars
        self.fireball_cooldown = 1
        self.fireball_time = time.time()
        # shield vars
        self.is_shielding = False
        self.total_shield = 10
        self.available_shield = 10
        self.shield_depletion_rate = 0.05
        self.shield_cooldown = 10
        self.reverse_shield_animation = False
        self.last_use = time.time() - self.shield_cooldown
        # kill count
        self.enemies_killed = 0


    def update(self, lvl_map, screen):
        self.apply_gravity()
        if self.is_on_ground or self.velocity >= 0:
            self.jump_img_index = 0
            self.detect_floor(lvl_map)
        self.detect_ceil(lvl_map)
        if self.is_shielding:
            self.engage_shield()
            self.can_shield()
        if not self.is_shielding:
            self.replenish_shield()
        self.draw_health_bar(screen)


    def generate_sprite_img(self):
        # shield animation
        if self.is_shielding:
            return self.shield_animation()
        # jumping
        elif not self.is_on_ground and not self.is_shielding:
            return self.jump_animation()
        # running animation
        elif self.is_running:
            return self.running_animation()
        # if no movement input or running into wall
        else:
            if self.is_facing_left:
                return pygame.transform.flip(self.walk_img_list[0], True, False)
        return self.walk_img_list[0]


    def running_animation(self):
        if self.is_facing_left:
            sprite_img = pygame.transform.flip(self.walk_img_list[self.walk_img_index], True, False)
        else:
            sprite_img = self.walk_img_list[self.walk_img_index]
        if time.time() - self.img_time > self.img_update_rate:
            self.walk_img_index = self.walk_img_index + 1 if self.walk_img_index + 1 < len(self.walk_img_list) else 0
            self.img_time = time.time()
        return sprite_img


    def shield_animation(self):
        if not self.is_facing_left:
            sprite_img = self.shield_img_list[self.shield_img_index]
        else:
            sprite_img = pygame.transform.flip(self.shield_img_list[self.shield_img_index], True, False)
        if time.time() - self.img_time > self.img_update_rate:
            if self.reverse_shield_animation:
                if self.shield_img_index > 0:
                    self.shield_img_index -= 1
            elif self.shield_img_index < len(self.shield_img_list) - 1:
                self.shield_img_index += 1
            self.img_time = time.time()
        return sprite_img


    def jump_animation(self):
        if not self.is_facing_left:
            sprite_img = self.jump_img_list[self.jump_img_index]
        else:
            sprite_img = pygame.transform.flip(self.jump_img_list[self.jump_img_index], True, False)
        if time.time() - self.img_time > self.img_update_rate:
            if self.jump_img_index < len(self.jump_img_list) - 1:
                self.jump_img_index += 1
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


    def can_shield(self):
        if self.available_shield > 0 and (self.last_use is None or time.time() - self.last_use > self.shield_cooldown):
            return True
        elif self.available_shield <= 0:
            self.last_use = time.time()
            self.reverse_shield_animation = False
        self.is_shielding = False
        return False


    def engage_shield(self):
        self.is_shielding = True
        self.is_on_ground = False
        self.available_shield -= self.shield_depletion_rate
        if self.available_shield <= 1.2:
            self.reverse_shield_animation = True


    def replenish_shield(self):
        if not self.is_shielding and self.available_shield < self.total_shield:
            self.available_shield = self.total_shield


    def draw_health_bar(self, screen):
        pygame.draw.rect(screen, "black", pygame.Rect(self.rect.x - 12, self.rect.y - 12, 54, 14))
        pygame.draw.rect(screen, "red", pygame.Rect(self.rect.x - 10, self.rect.y - 10, 50, 10))
        pygame.draw.rect(screen, "green", pygame.Rect(self.rect.x - 10, self.rect.y - 10,
                         50 * (self.current_health / self.start_health), 10))


    def draw_shield_bar(self, screen):
        pygame.draw.rect(screen, "black", pygame.Rect(self.rect.x - 12, self.rect.y - 24, 54, 14))
        pygame.draw.rect(screen, "yellow", pygame.Rect(self.rect.x - 10, self.rect.y - 22, 50, 10))
        load_val = 50 * ((time.time() - self.last_use) / self.shield_cooldown) \
            if not self.is_shielding \
            else 50 * (self.available_shield / self.total_shield)
        pygame.draw.rect(screen, "blue", pygame.Rect(self.rect.x - 10, self.rect.y - 22, min(50, load_val), 10))


    def display_stats(self, screen, world_number):
        pygame.draw.rect(screen, "black", pygame.Rect(10, 10, 100, 42))
        font = pygame.font.SysFont("Arial", 12)
        kill_count = font.render(f"Kill Count: {self.enemies_killed}", True, "green")
        max_health = font.render(f"Health: {self.current_health}/{self.start_health}", True, "green")
        level_count = font.render(f"Level: {world_number}", True, "green")
        screen.blit(kill_count, (12, 12))
        screen.blit(max_health, (12, 24))
        screen.blit(level_count, (12, 36))
