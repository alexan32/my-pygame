import logging
import gamemath
import environment
from util_functions import (
    collidable_list, 
    add_collidable_to_list,
    add_gameobject_to_dict,
    remove_gameobject_from_dict,
    generate_id
    )

logger=logging.getLogger() 
logger.setLevel(logging.DEBUG) 


class positionClass:

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
    the gameObject class:

    material: describes how the game object should be treated in collision detection. ie 'Wall' or 'Moveable.'
    flag: describes the type or class of object. ie 'Player', 'Enemy', or 'Trigger.'
    id: all gameobjects instances should have a unique id. Can be used to access that instance from the gameobject_dict.
    pos: tuple describing the position of the gameobject.
"""

class gameObject(positionClass):

    def __init__(self, pos, material=None, flag=None, id=None):
        positionClass.__init__(self, pos)
        self.material = material
        self.flag = flag
        if id == None:
            self.id = generate_id()
        else:
            self.id = id
        add_gameobject_to_dict(self)

    def destroy(self):
        remove_gameobject_from_dict(self)

    def update(self, dt):
        pass

    def render(self):
        pass


class triggerClass:

    def onTriggered(self, obj):
        logger.info('trigger detected object with id {}.'.format(obj.id))
        # do something


class collidableClass:

    def __init__(self, hitbox, pos=(0,0), offset=(0,0)):
        self.hitbox = hitbox
        self.hitbox_offset = offset
        self.hitbox.set_position(pos[0] + offset[0], pos[1] + offset[1])
        collidable_list.append(self)

    def render_hitbox(self):
        self.hitbox.render()

