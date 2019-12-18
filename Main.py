import pygame
import logging
import environment
from controller import controller
from util_classes import *
from util_functions import *
from player import playerObject
from wall import wallObject, movableObject, movableMover, rectangleWallObject


# LOGGING
logger=logging.getLogger() 
logger.setLevel(environment.LOG_LEVEL) 

# PYGAME VARIABLES
version = 'my-pygame-v0.01'
fullscreen = False
running = True
monitor_size = 1920, 1080 
size = width, height = environment.SCREEN_WIDTH, environment.SCREEN_HEIGHT
background = 50, 50, 50
fps = environment.FPS
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

player = playerObject((300,300), player_controller, screen)

# wall = wallObject((200,200), screen)
wall_two = rectangleWallObject((64,64), screen)
wall_three = rectangleWallObject((96,64), screen)
wall_four = rectangleWallObject((128,64), screen)
wall_five = rectangleWallObject((64,96), screen)
wall_six = rectangleWallObject((64,128), screen)
wall_seven = rectangleWallObject((64, 160), screen)
wall_eight = rectangleWallObject((128,96), screen)
wall_nine = rectangleWallObject((128, 160), screen)
wall_ten = rectangleWallObject((96, 160), screen)
wall_eleven = rectangleWallObject((200, 200), screen)
wall_twelve = rectangleWallObject((230, 300), screen)

# NAVMESH GENERATION


# GAME LOOP
while running:

    dt = clock.tick(fps)

    # UPDATE----------------------------
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type is pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    player_controller.update(dt)

    for key in gameobject_dict:
        gameobject_dict[key].update(dt)


    # RENDER----------------------------
    screen.fill(background)

    for key in gameobject_dict:
        gameobject_dict[key].render()

    pygame.display.update()

    # pygame.transform.scale(screen, monitor_size, fullscreen)