import json
import environment
from classes import TileMap, TileSurface, Grid, CollisionGrid

"""
returns a dictionary of grids containing layer data
"""
def loadWorldDataFromPath(path, tileWidth=None, tileHeight=None):
    with open(path) as f:
        _map = json.load(f)

    # create tilemap
    tileWidth = environment.TILE_WIDTH if tileWidth == None else tileWidth
    tileHeight = environment.TILE_HEIGHT if tileHeight == None else tileHeight
    tileMap = TileMap(f"./resources/images/tiles/{_map['tileset']}", tileWidth, tileHeight)

    allLayers = {}

    # build grid
    layerJson = _map['layer_1']
    layer_1 = []
    for y in range(len(layerJson)):
        layer_1 .append([])
        for x in range(len(layerJson[y])):
            surface = tileMap.getSurface(layerJson[y][x])
            layer_1 [y].append(TileSurface(surface))

    allLayers = {
        "layer_1": Grid(layer_1),
        "collision": CollisionGrid(_map['collision'])
    }

    return allLayers