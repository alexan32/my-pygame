from util_classes import gameObject
from hitbox import circle, rectangle
from util_abstractclasses import collidableClass
from util_functions import strip_from_sheet, checkForCollision
import gamemath

class wallObject(gameObject, collidableClass):

    def __init__(self, pos, screen):
        gameObject.__init__(self, pos, material='solid')
        collidableClass.__init__(self, circle(16, True, screen), pos)

    def render(self):
        collidableClass.render_hitbox(self)


class rectangleWallObject(gameObject, collidableClass):

    def __init__(self, pos, screen):
        gameObject.__init__(self, pos, material='solid')
        collidableClass.__init__(self, rectangle(32,32, True, screen), pos)

    def render(self):
        collidableClass.render_hitbox(self)


class movableObject(gameObject, collidableClass):

    def __init__(self, pos, screen):
        gameObject.__init__(self, pos, material='movable')
        collidableClass.__init__(self, circle(16, True, screen), pos)

    def render(self):
        collidableClass.render_hitbox(self)


class movableMover(gameObject, collidableClass):

    def __init__(self, pos, screen):
        gameObject.__init__(self, pos, material='movable')
        collidableClass.__init__(self, circle(16, True, screen), pos)
        self.moveSpeed = 0.05
        self.coordList = [(200,350), (400, 350)]
        self.index = 0

    def render(self):
        collidableClass.render_hitbox(self)

    def update(self, dt):
        theta = gamemath.degrees_between_two_points((self.x, self.y), self.coordList[self.index])
        xy = gamemath.get_xy_move(theta)
        self.increment_position(xy[0] * self.moveSpeed * dt, xy[1] * self.moveSpeed * dt)
        checkForCollision(self)

        if gamemath.distance_between_two_points((self.x, self.y), self.coordList[self.index]) < 7:
            self.index += 1
            print(self.index)
            if self.index > 1:
                self.index = 0

    def increment_position(self, dx, dy):
        gameObject.increment_position(self, dx, dy)
        self.hitbox.set_position(self.x + self.hitbox_offset[0], self.y + self.hitbox_offset[1])