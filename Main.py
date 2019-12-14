import pygame
import logging
import abstractclasses
import gameobject
import images
from player import playerObject
from controller import controller


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

# image module
test_img = images.image((64,0), "resources/character.png", screen)
frames = images.strip_from_sheet("resources/knight_combined.png", 32, 32, 13)
test_sprite = images.spriteAnimation(frames, screen)

# gameobject
test_gameobj = gameobject.gameObject((0, 0))
test_imageobj = gameobject.imageObject((160, 0), test_img)

# player
player = playerObject((96,96), player_controller, screen)

#if it has an update(self, dt) it goes here
update_list=[test_sprite, player]

# if it has a render() it goes here
render_list=[test_img, test_sprite, player]


# GAME LOOP
while running:

    dt = clock.tick(fps)

    # UPDATE----------------------------
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type is pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    player_controller.update()

    for obj in update_list:
        obj.update(dt)


    # RENDER----------------------------
    screen.fill(background)

    for obj in render_list:
        obj.render()

    pygame.display.update()

    # pygame.transform.scale(screen, monitor_size, fullscreen)