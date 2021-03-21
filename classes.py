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
        for y in range(int(sourceImageHeight / tileHeight)):
            for x in range(int(sourceImageWidth / tileWidth)):
                left, top = x * tileWidth, y * tileHeight
                tile = pygame.Surface((tileWidth, tileHeight))
                tile.blit(self.sourceImage, (0,0), pygame.Rect(left, top, tileWidth, tileHeight))
                self.tileSurfaces.append(tile)

    def getSurface(self, index):
        return self.tileSurfaces[index]


"""
TileSurface holds the pygame Surface object that gets rendered at those coordinates.
"""
class TileSurface():

    def __init__(self, surface):
        self.surface = surface

    def render(self, screen, x, y):
        screen.blit(self.surface, (x, y))


"""
basically a wrapper around a 2d list
"""
class Grid():

    def __init__(self, list2d, initialCount=0):
        self.values = []
        self.height = len(list2d)
        self.width = len(list2d[0])
        for y in range(self.height):
            self.values.append([])
            for x in list2d[y]:
                self.values[y].append(x)

    def getSubSection(self, x, y, width, height):
        pass

    def getCell(self, x, y):
        try:
            return self.values[y][x]
        except:
            return None

    def getNeighbors(self, x, y):
        neighbors = []
        reachable = lambda x, y: x >= 0 and x < self.width and y >= 0 and y < self.height
        if not reachable(x, y):
            return neighbors
        if reachable(x -1, y):
            neighbors.append((x-1, y))
        if reachable(x+1, y):
            neighbors.append((x+1, y))
        if reachable(x, y-1):
            neighbors.append((x, y-1))
        if reachable(x, y+1):
            neighbors.append((x, y+1))
        return neighbors

        


"""Drawn onto the screen to show which tile the mouse is currently over"""
class TileIndicator(Position):

    def __init__(self, pathToImage):
        super().__init__()
        self.image = Image(pathToImage)
        self.hidden = False

    def render(self, screen):
        if not self.hidden:
            self.image.render(screen, self.x, self.y)


class GridAgent(Position):

    def __init__(self, movement, grid):
        super().__init__()
        self.grid = grid
        self.gridPosition = 0, 0
        self.movement = movement
        self.image = Image("./resources/images/characters/player.png")
        self.tileIndicator = TileIndicator("./resources/images/tiles/indicator.png")
        self.showMovement = False

    def findMoves(self):
        visited = {
            str(self.gridPosition[0], self.gridPosition[1]): {"x": self.gridPosition[0], "y": self.gridPosition[1], "cost": 0}
        }


    def render(self, screen):
        self.image.render(screen, self.x, self.y)