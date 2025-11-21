"""
Player.py: The player class.
"""

import config
import Character
import os
import pygame
import pygame.font
import time

pygame.font.init()


class Player(Character.Character):
    def __init__(self, x_coord, y_coord):
        super().__init__(config.PLAYER_IMG_FILE, x_coord, y_coord, config.PLAYER_SPEED, config.PLAYER_HEALTH)
        # shield and jump imgs
        shield_imgs = os.listdir(f"img/character/Sorcerer/Crouching")
        shield_imgs.sort()
        jump_imgs = os.listdir(f"img/character/Sorcerer/Jumping")
        jump_imgs.sort()
        self.shield_img_list = [pygame.transform.scale(pygame.image.load(f"img/character/Sorcerer/Crouching/{img}"),
                                                       (77, 70)) for img in shield_imgs]
        self.jump_img_list = [pygame.transform.scale(pygame.image.load(f"img/character/Sorcerer/Jumping/{img}"),
                                                     (35, 60)) for img in jump_imgs]
        self.shield_img_index = 0
        self.jump_img_index = 0
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
        # player lives
        self.lives = 3


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
        self.draw_shield_bar(screen)
        self.draw_health_bar(screen)


    def reset(self, start_x, start_y):
        self.rect.centerx = start_x
        self.rect.bottom = start_y - config.BLOCK_SIZE
        self.current_health = self.start_health


    def generate_sprite_img(self):
        # shield animation
        if self.is_shielding:
            return self.shield_animation()
        # jumping
        elif not self.is_on_ground and not self.is_shielding:
            return self.jump_animation()
        # running animation
        elif self.is_running:
            return self.walking_animation()
        # if no movement input or running into wall
        else:
            if self.is_facing_left:
                return pygame.transform.flip(self.walk_img_list[0], True, False)
        return self.walk_img_list[0]


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


    def draw_shield_bar(self, screen):
        pygame.draw.rect(screen, "black", pygame.Rect(self.rect.x - 12, self.rect.y - 24, 54, 14))
        pygame.draw.rect(screen, "yellow", pygame.Rect(self.rect.x - 10, self.rect.y - 22, 50, 10))
        load_val = 50 * ((time.time() - self.last_use) / self.shield_cooldown) \
            if not self.is_shielding \
            else 50 * (self.available_shield / self.total_shield)
        pygame.draw.rect(screen, "blue", pygame.Rect(self.rect.x - 10, self.rect.y - 22, min(50, load_val), 10))


    def display_stats(self, screen, world_number):
        font = pygame.font.SysFont("Arial", 12)
        kill_count = font.render(f"Kill Count: {self.enemies_killed}", True, "green")
        max_health = font.render(f"Health: {self.current_health}/{self.start_health}", True, "green")
        level_count = font.render(f"Level: {world_number}", True, "green")
        lives_left = font.render(f"Lives: {self.lives}", True, "green")
        pygame.draw.rect(screen, "black", pygame.Rect(10, 10, 100, 54))
        screen.blit(kill_count, (12, 12))
        screen.blit(max_health, (12, 24))
        screen.blit(level_count, (12, 36))
        screen.blit(lives_left, (12, 48))
