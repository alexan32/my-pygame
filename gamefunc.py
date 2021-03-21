import json
import environment
from classes import TileMap, Tile


def loadGridFromPath(path, tileWidth=None, tileHeight=None):
    with open(path) as f:
        _map = json.load(f)

    # create tilemap
    tileWidth = environment.TILE_WIDTH if tileWidth == None else tileWidth
    tileHeight = environment.TILE_HEIGHT if tileHeight == None else tileHeight
    tileMap = TileMap(f"./resources/images/tiles/{_map['tileset']}", tileWidth, tileHeight)

    # build grid
    gridJson = _map['grid']
    grid = []
    for y in range(len(gridJson)):
        grid.append([])
        for x in range(len(gridJson[y])):
            surface = tileMap.getSurface(gridJson[y][x])
            grid[y].append(Tile(surface, None))

    return grid