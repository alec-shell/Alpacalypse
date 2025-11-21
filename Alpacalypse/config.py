####PLAYER AND ENEMY CONFIG####

# player vars
PLAYER_SPEED = 4
PLAYER_HEALTH = 60
PLAYER_IMG_FILE = "character/Sorcerer/Walking"
PLAYER_FIREBALL_SPEED = 6
PLAYER_FIREBALL_DAMAGE = 10
ORANGE_FIREBALL_FILE = "fireball/orange_balls/"
SPRITE_COLLISION_OFFSET = 5

# llama settings
ENEMY_SPEED = 2
ENEMY_HEALTH = 20
ENEMY_IMG_FILE = "enemy"
LLAMA_FIREBALL_SPEED = 5
LLAMA_FIREBALL_DAMAGE = 10
BLUE_FIREBALL_FILE = "fireball/blue_balls/"

# megalopaca settings
FIREBALL_SPEED_MEGA = 2
FIREBALL_DAMAGE_MEGA = 20

###EXPLOSIONS AND FIREBALLS CONFIG###

# Explosion settings
ORANGE_EXPLOSION_FILE = "explosion/Orange"
EXPLOSION_SIZE = 64
EXPLOSION_ANIMATION_COOLDOWN = 0.05
MEGALPACA_EXPLOSION_SCALAR = 5

# fireball scalar vals
PLAYER_FIREBALL_SCALER = 1
LLAMA_FIREBALL_SCALER = 1
MEGALOPACA_FIREBALL_SCALER = 5

###ITEMS CONFIG###

# health potion
HEALTH_POTION_IMG = "health_potion.png"
HEALTH_POTION_GAIN = 40

# lvl up potion
LEVEL_UP_POTION_IMG = "level_up.png"
MAX_HEALTH_POTION_GAIN = 20

###MAPS CONFIG####

BLOCK_SIZE = 40
BLOCK_FILE_PATHS = {
    1: ["img/background/Grass/grass_01.png",
        "img/background/Grass/grass_02.png",
        "img/background/Grass/grass_03.png",
        "img/background/Grass/grass_04.png"],
    2: ["img/background/Stone_Vines/Stone_Vines_1.png",
        "img/background/Stone_Vines/Stone_Vines_2.png",
        "img/background/Stone_Vines/Stone_Vines_3.png",
        "img/background/Stone_Vines/Stone_Vines_4.png",
        "img/background/Stone_Vines/Stone_Vines_5.png"],
    3: ["img/background/Grass/grass_Edge_L.png"],
    4: ["img/background/Grass/grass_Edge_R.png"]
    }

###PORTAL CONFIG###

PORTAL_IMG_FILE = "img/background/Portal/lvl_Portal.png"

###OFF MAP####

BELOW_MAP = 16 * BLOCK_SIZE
