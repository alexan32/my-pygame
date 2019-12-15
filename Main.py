import pygame
import logging
from util_classes import *
from util_functions import *
from player import playerObject
from wall import wallObject, movableObject, movableMover


# LOGGING
logger=logging.getLogger() 
logger.setLevel(logging.DEBUG) 

# PYGAME VARIABLES
version = 'my-pygame-v0.01'
fullscreen = False
running = True
monitor_size = 1920, 1080 
size = width, height = 640, 480
background = 50, 50, 50
fps = 60
clock = pygame.time.Clock()


# GAME INITIALIZATION      
pygame.init()
if fullscreen:
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode(size)
pygame.display.set_caption(version)


# OBJECT INIT
player_controller = controller()

frames = strip_from_sheet("resources/knight_combined.png", 32, 32, 13)
test_sprite = spriteObject((0,0), frames, screen)

test_image = imageObject((32,0), "resources/character.png", screen)

player = playerObject((96,96), player_controller, screen)

wall = wallObject((200,200), screen)

movable = movableObject((200, 300), screen)
movableTwo = movableObject((200, 332), screen)


# GAME LOOP
while running:

    dt = clock.tick(fps)

    # UPDATE----------------------------
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type is pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    player_controller.update()

    for key in gameobject_dict:
        gameobject_dict[key].update(dt)


    # RENDER----------------------------
    screen.fill(background)

    for key in gameobject_dict:
        gameobject_dict[key].render()

    pygame.display.update()

    # pygame.transform.scale(screen, monitor_size, fullscreen)