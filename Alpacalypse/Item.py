"""
Item.py: Defines class for collectible items.
"""

import config
import pygame


class Item(pygame.sprite.Sprite):
    def __init__(self, item_type, x_coord, y_coord):
        super().__init__()
        self.item_type = item_type
        self.img_file = None
        self.assign_type()
        self.img = pygame.transform.scale(pygame.image.load(f"img/item/{self.img_file}"), (20, 20))
        self.rect = self.img.get_rect()
        self.rect.x = x_coord
        self.rect.bottom = y_coord


    def update(self, player, screen):
        collision = self.detect_collision(player)
        if not collision:
            screen.blit(self.img, self.rect)
        return collision


    def assign_type(self):
        if self.item_type == "health":
            self.img_file = config.HEALTH_POTION_IMG
        elif self.item_type == "level_up":
            self.img_file = config.LEVEL_UP_POTION_IMG


    def detect_collision(self, player):
        if self.rect.colliderect(player.rect):
            if self.item_type == "health":
                if player.current_health == player.start_health:
                    return False
                elif player.start_health - player.current_health >= config.HEALTH_POTION_GAIN:
                    player.current_health += config.HEALTH_POTION_GAIN
                else:
                    player.current_health = player.start_health
            elif self.item_type == "level_up":
                player.start_health += config.MAX_HEALTH_POTION_GAIN
                player.current_health = player.start_health
            return True
        return False
