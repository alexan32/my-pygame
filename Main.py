import pygame
import logging
import environment
from gamefunc import loadWorldDataFromPath
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
emptyEvents = {"mouse": None}

# INIT
pygame.init()
if fullscreen:
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode(size)
pygame.display.set_caption(version)
pygame.mouse.set_cursor(pygame.cursors.arrow)


worldGrid = Grid(loadWorldDataFromPath('./resources/level/map.json'))
print(worldGrid.getNeighbors(1, 1))

# tileIndicator = TileIndicator('./resources/images/tiles/indicator.png')
player = GridAgent(6, worldGrid)

def main():
    # GAME LOOP
    running = True
    while running:
        dt = clock.tick(fps)
        
        eventBus = emptyEvents.copy()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                eventBus['mouse'] = pygame.mouse.get_pos()

        update(dt, eventBus)
        render(dt)


def update(dt, eventBus):
    player_controller.update(dt)
    x, y = pygame.mouse.get_pos()



    tileX, tileY = int(x / environment.TILE_WIDTH), int(y / environment.TILE_HEIGHT)
    # tileIndicator.set_position(tileX * environment.TILE_WIDTH, tileY * environment.TILE_HEIGHT)


def render(dt):
    screen.fill(background)

    # improve with blits?
    for y in range(worldGrid.height):
        for x in range(worldGrid.width):
            cell = worldGrid.getCell(x, y)
            if cell != None:
                cell.render(screen, x * environment.TILE_WIDTH, y * environment.TILE_HEIGHT)

    player.render(screen)

    # tileIndicator.render(screen)

    pygame.display.update()


if __name__ == "__main__":
    main()