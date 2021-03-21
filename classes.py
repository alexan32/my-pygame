import pygame
import logging

# LOGGING
logger=logging.getLogger() 
logger.setLevel(logging.DEBUG)

"""
Position class provides standard utility for x y coordinates
"""
class Position:

    def __init__(self, pos=(0,0)):
        self.x, self.y = pos

    def set_position(self, x, y):
        self.x, self.y = x, y

    def increment_position(self, dx, dy):
        self.x += dx
        self.y += dy

    def get_position(self):
        return (self.x, self.y)


"""
Takes an image from a file path and makes a renderable pygame Surface
"""
class Image():

    def __init__(self, path):
        temp = pygame.image.load(path)
        self.surface = temp.convert_alpha()
        self.width, self.height = temp.get_rect().size

    def render(self, screen, x, y):
        screen.blit(self.surface, (x, y))


"""
TileMap takes an image from a file path and breaks it into pygame Surface objects
"""
class TileMap():

    def __init__(self, path, tileWidth, tileHeight):
        temp = pygame.image.load(path)
        sourceImageWidth, sourceImageHeight = temp.get_rect().size
        self.sourceImage = temp.convert_alpha()
        self.tileSurfaces = []
        for x in range(len(sourceImageWidth / tileWidth)):
            for y in range(len(sourceImageHeight / tileHeight)):
                left, top = x * tileWidth, y * tileHeight
                tile = pygame.Surface((tileWidth, tileHeight))
                tile.blit(self.sourceImage, (0,0), pygame.Rect(left, top, tileWidth, tileHeight))
                self.tileSurfaces.append(tile)

    def getSurface(self, index):
        return self.tileSurfaces[index]

"""
Tile holds the event properties for a single location within the grid, as well 
as the pygame Surface object that gets rendered at those coordinates.
"""
class Tile():

    def __init__(self, surface, properties):
        self.properties = properties
        self.surface = surface

    def render(self, screen, x, y):
        screen.blit(self.surface, (x, y))
