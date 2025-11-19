"""
Enemy.py: Enemy class.
"""

import Character
import config
from Fireball import Fireball
import random
import time


class Enemy(Character.Character):
    def __init__(self, img_file, x_coord, y_coord, speed, health, enemy_type, img_scaler = 1, health_scaler = 1, pacing_dist = 80):
        self.enemy_type = enemy_type
        super().__init__(img_file, x_coord, y_coord, speed, health, health_scaler, img_scaler)
        # override default Character jump_img_list
        self.jump_img_list = self.walk_img_list
        self.pacing_left = 1
        self.pacing_dist = pacing_dist
        self.dist_traveled = 0
        self.dist_time = time.time()
        self.start_direction()
        # fireball settings
        self.fireball_speed, self.fireball_dmg = self.assign_type_settings()


    def update(self, lvl_map, screen, player_x, player_top, player_bottom):
        super().update(lvl_map, screen)
        is_targeting, is_cooled_down = self.track_target(player_x, player_top, player_bottom)
        if is_targeting:
            self.is_running = False
            if is_cooled_down:
                return self.fire_fireball()
        else:
            self.move(lvl_map)
            return None


    def start_direction(self):
        start_dir = random.randint(0, 10)
        if start_dir % 2 == 0:
            self.pacing_left = -1
            self.is_facing_left = True


    def move(self, lvl_map):
        self.is_running = True
        cooldown = .05
        if time.time() - self.dist_time > cooldown:
            self.dist_time = time.time()
            wall_hit = self.detect_wall(lvl_map, self.is_facing_left, not self.is_facing_left)
            if self.dist_traveled < self.pacing_dist and not wall_hit:
                self.rect.x += self.speed * self.pacing_left
                self.dist_traveled += self.speed
            else:
                self.dist_traveled = 0
                self.is_facing_left = not self.is_facing_left
                self.pacing_left *= -1


    def track_target(self, player_x, player_top, player_bottom):
        top_intersect = self.rect.top <= player_top <= self.rect.bottom
        bottom_intersect = self.rect.bottom >= player_bottom >= self.rect.top
        if top_intersect or bottom_intersect:
            if (self.is_facing_left
                    and self.rect.centerx - 320 <= player_x <= self.rect.x
                    or not self.is_facing_left
                    and self.rect.centerx <= player_x <= self.rect.centerx + 320):
                if super().fireball_is_cooled_down():
                    return True, True
                else:
                    return True, False
        return False, False


    def fire_fireball(self):
            return Fireball(config.BLUE_FIREBALL_FILE, self.fireball_speed, self.fireball_dmg, self.rect.centerx,
                            self.rect.y + (self.rect.height / 2), self.is_facing_left, self.enemy_type)



    def assign_type_settings(self):
        if self.enemy_type == "llama":
            return config.LLAMA_FIREBALL_SPEED, config.LLAMA_FIREBALL_DAMAGE
        elif self.enemy_type == "megalopaca":
            return config.FIREBALL_SPEED_MEGA, config.FIREBALL_DAMAGE_MEGA
