"""
Portal.py: Look, a portal!
"""

import config
import pygame


class Portal(pygame.sprite.Sprite):
    def __init__(self, x_coord, y_coord):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(config.PORTAL_IMG_FILE), (config.BLOCK_SIZE, config.BLOCK_SIZE * 2))
        self.rect = self.image.get_rect()
        self.rect.centerx = x_coord
        self.rect.bottom = y_coord

    def generate_sprite_img(self, screen):
        screen.blit(self.image, self.rect)
