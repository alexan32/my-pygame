import pygame
import logging
import environment
from gamefunc import loadGridFromPath
from controller import Controller
from classes import *

# LOGGING
logger=logging.getLogger() 
logger.setLevel(environment.LOG_LEVEL) 

# PYGAME VARIABLES
version = 'my-pygame-v0.01'
fullscreen = False
monitor_size = 1920, 1080 
size = width, height = environment.SCREEN_WIDTH, environment.SCREEN_HEIGHT
background = 50, 50, 50
fps = environment.FPS
clock = pygame.time.Clock()
player_controller = Controller()

# INIT
pygame.init()
if fullscreen:
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode(size)
pygame.display.set_caption(version)


worldGrid = loadGridFromPath('./resources/level/map.json')

def main():
    # GAME LOOP
    running = True
    while running:
        dt = clock.tick(fps)

        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        update(dt)
        render(dt)


def update(dt):
    player_controller.update(dt)


def render(dt):
    screen.fill(background)

    for y in range(len(worldGrid)):
        for x in range(len(worldGrid[y])):
            worldGrid[y][x].render(screen, x * environment.TILE_WIDTH, y * environment.TILE_HEIGHT)

    pygame.display.update()


if __name__ == "__main__":
    main()