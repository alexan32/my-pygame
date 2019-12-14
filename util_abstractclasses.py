import logging
from util_functions import (
    collidable_list, 
    add_collidable_to_list
    )

logger=logging.getLogger() 
logger.setLevel(logging.DEBUG) 


class triggerClass:

    def onTriggered(self, obj):
        logger.info('trigger detected object with id {}.'.format(obj.id))
        # do something


class positionClass:

    def __init__(self, pos):
        self.x, self.y = pos

    def set_position(self, x, y):
        self.x, self.y = x, y

    def increment_position(self, dx, dy):
        self.x += dx
        self.y += dy


    



