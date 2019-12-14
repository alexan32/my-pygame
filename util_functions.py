import logging
import pygame

# LOGGING
logger=logging.getLogger() 
logger.setLevel(logging.DEBUG) 

# ---------------------------------------------------------------------
# GAME OBJECTS
# ---------------------------------------------------------------------

"""These variables and functions provide access to game objects"""

counter = 0
gameobject_dict = {}
collidable_list = []

def generate_id():
    global counter
    counter += 1
    return counter - 1

def add_gameobject_to_dict(obj):
    gameobject_dict[obj.id] = obj
    print("{} added to gameobject_dict".format(obj.id))

def add_collidable_to_list(obj):
    collidable_list.append(obj)
    logger.info("{} added to collidable_list".format(obj.id))

def remove_gameobject_from_dict(obj):
    try:
        del gameobject_dict[obj.id]
        logger.info("{} removed from gameobject_dict".format(obj.id))
    except KeyError:
        logger.error("failed to remove '{}'from collidable_list".format(obj.id))

def remove_collidable_from_list(obj):
    try:
        logger.info("{} removing from collidable_list".format(obj.id))
    except:
        logger.error("failed to remove '{}'from collidable_list".format(obj.id))


# ---------------------------------------------------------------------
# IMAGES
# ---------------------------------------------------------------------


"""Use this function to parse sprite sheets into frames for animation"""

def strip_from_sheet(path, frame_width, frame_height, columns, rows=1):
    frames = []
    sheet = pygame.image.load(path)
    for j in range(rows):
        for i in range(columns):
            location = (frame_width * i, frame_height*j)
            frames.append(sheet.subsurface(pygame.Rect(location,(frame_width, frame_height))))
    return frames