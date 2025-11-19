"""
Main.py: An epic tale of... something, or the main game loop.
"""

from Character import Character
import config
from Explosion import Explosion
import Maps
import pygame

pygame.init()
pygame.display.set_caption("Alpacalypse")

# screen vars
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_INST = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
GAME_CLOCK = pygame.time.Clock()
screen_is_running = True
FPS = 60

# fireball vars
fireballs = []

# explosion vars
explosions = []

# world vars
world_number = 1
(backdrop,
 level,
 lvl_imgs,
 enemies_list,
 player_start_pos,
 items,
 portal) = Maps.build_level(f"lvl_0{world_number}.txt")

# player vars
PLAYER_INST = Character(config.PLAYER_IMG_FILE,
                        player_start_pos[0],
                        player_start_pos[1],
                        config.PLAYER_SPEED,
                        config.PLAYER_HEALTH)
player_is_alive = True


def update_fireballs():
    for fireball in fireballs[:]:
        collision_code = fireball.update(level, SCREEN_WIDTH, enemies_list, PLAYER_INST.rect)
        # no collision
        if collision_code == -1:
            SCREEN_INST.blit(fireball.generate_sprite_img(), (fireball.rect.x, fireball.rect.y))
        # wall collision
        elif collision_code == -2:
            explosions.append(Explosion(fireball.origin, fireball.rect.x, fireball.rect.y))
            fireballs.remove(fireball)
        # player collision
        elif collision_code == -3:
            explosions.append(Explosion(fireball.origin, PLAYER_INST.rect.x, PLAYER_INST.rect.centery))
            fireballs.remove(fireball)
            if not PLAYER_INST.is_shielding:
                PLAYER_INST.current_health -= fireball.damage
            if PLAYER_INST.current_health <= 0:
                global player_is_alive
                player_is_alive = False
        # enemy collision
        else:
            explosions.append(Explosion(fireball.origin,
                                        enemies_list[collision_code].rect.x,
                                        enemies_list[collision_code].rect.centery))
            fireballs.remove(fireball)
            enemies_list[collision_code].current_health -= fireball.damage
            if enemies_list[collision_code].current_health <= 0:
                PLAYER_INST.enemies_killed += 1
                enemies_list.remove(enemies_list[collision_code])


def update_explosions():
    for exp in explosions[:]:
        exp_animation = exp.generate_sprite_img()
        if exp_animation:
            SCREEN_INST.blit(exp_animation, exp.rect.center)
        else:
            explosions.remove(exp)


def update_enemies():
    for enemy in enemies_list[:]:
        fireball = enemy.update(level, SCREEN_INST, PLAYER_INST.rect.x, PLAYER_INST.rect.top, PLAYER_INST.rect.bottom)
        if fireball:
            fireballs.append(fireball)
        SCREEN_INST.blit(enemy.generate_sprite_img(), (enemy.rect.x, enemy.rect.y))


def update_items():
    # checks for collected items
    for item in items[:]:
        if item.update(PLAYER_INST, SCREEN_INST):
            items.remove(item)


def update_screen():
    if portal:
        if update_lvl():
            PLAYER_INST.is_facing_left = not PLAYER_INST.is_facing_left
    Maps.draw_background(SCREEN_INST, lvl_imgs, backdrop)
    update_items()
    if player_is_alive:
        PLAYER_INST.update(level, SCREEN_INST)
        PLAYER_INST.draw_shield_bar(SCREEN_INST)
        SCREEN_INST.blit(PLAYER_INST.generate_sprite_img(), (PLAYER_INST.rect.x, PLAYER_INST.rect.y))
    if portal:
        portal.generate_sprite_img(SCREEN_INST)
    update_fireballs()
    update_enemies()
    update_explosions()
    PLAYER_INST.display_stats(SCREEN_INST, world_number)


def update_lvl():
    global backdrop, level, lvl_imgs, enemies_list, player_start_pos, items, portal, world_number
    if PLAYER_INST.rect.colliderect(portal.rect):
        world_number += 1
        (backdrop,
        level,
        lvl_imgs,
        enemies_list,
        player_start_pos,
        items,
        portal) = Maps.build_level(f"lvl_0{world_number}.txt")
        return True
    return False



def events_handler():
    # detect events
    for event in pygame.event.get():
        # quit event
        if event.type == pygame.QUIT:
            global screen_is_running
            screen_is_running = False
            quit()
        if event.type == pygame.KEYDOWN and player_is_alive:
            # jump event
            if event.key == pygame.K_SPACE:
                PLAYER_INST.jump()
            # fireball event
            if event.key == pygame.K_f:
                fireball = PLAYER_INST.fire_fireball()
                if fireball:
                    fireballs.append(fireball)
            # shield event
            if event.key == pygame.K_r and PLAYER_INST.can_shield():
                PLAYER_INST.engage_shield()


def get_key_presses():
    if player_is_alive:
        # detect pressed keys and update character movement
        pressed = pygame.key.get_pressed()
        # move left
        if pressed[pygame.K_a] and PLAYER_INST.rect.x >= 0:
            PLAYER_INST.move(True, False, level)
        # move right
        elif pressed[pygame.K_d] and PLAYER_INST.rect.x < SCREEN_WIDTH - PLAYER_INST.rect.width:
            PLAYER_INST.move(False, True, level)
        # none or invalid input
        else:
            PLAYER_INST.is_running = False

# running loop
def main():
    while screen_is_running:
        update_screen()
        # continuous key presses
        if not PLAYER_INST.is_shielding:
            get_key_presses()
        # one-time events and key-presses
        events_handler()
        # update display
        pygame.display.flip()
        # maintain frame rate
        GAME_CLOCK.tick(FPS)

main()
pygame.quit()
