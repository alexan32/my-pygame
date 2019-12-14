import logging
import functions
import abstractclasses

# LOGGING
logger=logging.getLogger() 
logger.setLevel(logging.DEBUG)

"""
    the gameObject class:

    material: describes how the game object should be treated in collision detection. ie 'Wall' or 'Moveable.'
    flag: describes the type or class of object. ie 'Player', 'Enemy', or 'Trigger.'
    id: all gameobjects instances should have a unique id. Can be used to access that instance from the gameobject_dict.
    pos: tuple describing the position of the gameobject.
"""

class gameObject(abstractclasses.positionClass):

    def __init__(self, pos, material=None, flag=None, id=None):
        abstractclasses.positionClass.__init__(self, pos)
        self.material = material
        self.flag = flag
        if id == None:
            self.id = functions.generate_id()
        else:
            self.id = id
        functions.add_gameobject_to_dict(self)

    def destroy(self):
        functions.remove_gameobject_from_dict(self)

    def update(self, dt):
        pass

    def render(self):
        pass


class imageObject(gameObject):

    def __init__(self, pos, image, material=None, flag=None, id=None):
        gameObject.__init__(self, pos, material=material, flag=flag, id=id)
        self.image = image
        self.image.set_position(self.x, self.y)

    def increment_position(self, dx, dy):
        gameObject.increment_position(self, dx, dy)
        self.image.set_position(self.x, self.y)

    def set_position(self, x, y):
        gameObject.set_position(self, x, y)
        self.image.set_position(self.x, self.y)

    def render(self):
        self.image.render()


class spriteObject(gameObject):

    def __init__(self, pos, sprite_animation, material=None, flag=None, id=None):
        gameObject.__init__(self, pos, material=material, flag=flag, id=id)
        self.sprite_animation = sprite_animation 

    def increment_position(self, dx, dy):
        gameObject.increment_position(self, dx, dy)
        self.sprite_animation.set_position(self.x, self.y)

    def set_position(self, x, y):
        gameObject.set_position(self, x, y)
        self.sprite_animation.set_position(self.x, self.y)

    def render(self):
        self.sprite_animation.render()
        gameObject.render(self)

    def update(self, dt):
        gameObject.update(self, dt)
        self.sprite_animation.update(dt)


