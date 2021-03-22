import pygame
import logging
import copy
import environment

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
basically a wrapper around a 2d list for building the map/performing pathfinding
"""
class Grid():

    def __init__(self, list2d):
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

    def setCell(self, x, y, value):
        self.values[y][x] = value


"""
Grid that provides functionality for pathfinding. expects a 2d list with a value of
-1 for each tile that is not passable, and a high number for walkable tiles. 
    ie:     99 99 99 99
            99 -1 99 99
            99 -1 -1 99
            99 99 99 99
"""
class CollisionGrid(Grid):

    def __init__(self, list2d):
        super().__init__(list2d)

    def getReachableTiles(self, startX, startY, movement):     
        collisionList = copy.deepcopy(self.values)
        collisionList [startY][startX] = 0

        for row in collisionList:
            rowString = ""
            for val in row:
                rowString += f"{val}".ljust(4)
            print(rowString)

        queue = [(startX, startY)]
        reachable = []

        while len(queue) > 0:
            currentNode = queue.pop(0)
            currentNodeValue = collisionList[currentNode[1]][currentNode[0]]

            neighbors = self.getNeighbors(currentNode[0], currentNode[1])

            for neighbor in neighbors:
                value = collisionList[neighbor[1]][neighbor[0]]
                moveCost = 1.5 if neighbor[0] - currentNode[0] != 0 and neighbor[1] - currentNode[1] != 0 else 1.0
                if value > currentNodeValue + moveCost and currentNodeValue + moveCost <= movement:
                    collisionList[neighbor[1]][neighbor[0]] = currentNodeValue + moveCost
                    queue.append(neighbor)

            if currentNode not in reachable:
                reachable.append(currentNode)
        
        print()
        for row in collisionList:
            rowString = ""
            for val in row:
                rowString += f"{val}".ljust(4)
            print(rowString)

        return reachable

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
        if reachable(x-1, y-1):
            neighbors.append((x-1, y-1))
        if reachable(x-1, y+1):
            neighbors.append((x-1, y+1))
        if reachable(x+1, y-1):
            neighbors.append((x+1, y-1))
        if reachable(x+1, y+1):
            neighbors.append((x+1, y+1))
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


class GridAgent():

    def __init__(self, movement):
        self.gridPosition = 0, 0
        self.movement = movement
        self.image = Image("./resources/images/characters/player.png")
        self.tileIndicator = TileIndicator("./resources/images/tiles/indicator.png")
        self.showMovement = False
        self.availableMovement = []

    def getAvailableMovement(self, collisionGrid):
        self.availableMovement = collisionGrid.getReachableTiles(self.gridPosition[0], self.gridPosition[1], self.movement)

    def render(self, screen):
        self.image.render(screen, self.gridPosition[0] * environment.TILE_WIDTH, self.gridPosition[1] * environment.TILE_HEIGHT)

        if self.showMovement:
            for coords in self.availableMovement:
                self.tileIndicator.set_position(coords[0] * environment.TILE_WIDTH, coords[1]* environment.TILE_HEIGHT)
                self.tileIndicator.render(screen)