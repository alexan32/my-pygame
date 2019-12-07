import pygame
from pygame.locals import *
import logging
import hitbox
from controller import controller
from gameobject import *
from images import *
from statemachines import animationController


# TODO short term goals:
# need to finish up collision detection. collision between rectangles, circles
# need to implement sprites instead of static images.

# TODO longterm goals
# dynamic camera. can be set to follow, stationary, jump around map?
# environment objects: walls, doors, traps, chests, collectables. need these objects before we can try to 
# create a level and file system. (can use JSON to store levels?)


# VARIABLES
version = 'my-pygame-v0.01'

fullscreen = False
monitor_size = 1920, 1080 
size = width, height = 640, 480

background = 50, 50, 50                # the background color
running = True
fps = 60
clock = pygame.time.Clock()


# GAME INITIALIZATION               # pygame stuff
pygame.init()

if fullscreen:
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode(size)


pygame.display.set_caption(version)

#GAMEOBJECT INIT
player_controller = controller()

img2 = staticImage(screen, 'resources/character.png', offset_x=-16, offset_y=-16)                   # centered
img3 = staticImage(screen, 'resources/character.png', offset_x=-16, offset_y=-16, draw=False)       # centered

hb3 = hitbox.circle(16, draw=True, screen=screen)
hb2 = hitbox.rectangle(32, 32, draw=True, screen=screen, property_flag='wall')
hb4 = hitbox.circle(32, draw=True, screen=screen, property_flag='wall')

player = playerObject(screen, img3, 200, 200, player_controller, hitbox=hb3)
wall = imageObject(screen, img2, 96, 96, hitbox=hb2)
round_wall = gameObject(300, 300, hitbox=hb4)

gameobjects=[player, wall, round_wall]     # remove img object, work in sprites

# FUNCTION TEST

# frames = strip_from_sheet("resources/knight_combined.png", 32, 32, 13)
# attack = spriteAnimation(screen, frames[1:7], (192,0))

animation_controller = animationController(screen)


# GAME LOOP
while running:
    # CLOCK
    dt = clock.tick(fps) # delta time 

    # UPDATE----------------------------
    # events
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type is KEYDOWN and event.key == K_ESCAPE):
            running = False

    # controller
    player_controller.update()

    # gameObjects
    for obj in gameobjects:
        obj.update(dt)

    # animation
    animation_controller.update(dt)


    # RENDER----------------------------
    screen.fill(background)
    animation_controller.render()

    # Draw level/gameobjects here
    for obj in gameobjects:
        obj.render()

    pygame.display.update()

    # pygame.transform.scale(screen, monitor_size, fullscreen)