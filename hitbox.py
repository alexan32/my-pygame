import pygame
import gamemath

# the hitbox class is the parent object for all hitboxes, but is not meant to ever be
# instantiated. propertyFlag is intended to be shared with other collidables on collisions.
# intended as a string representing physics property but could be any datatype
class hitbox:

    def __init__(self, draw=False, screen=None, property_flag=None):
        self.property_flag = property_flag
        self.draw = draw
        self.screen = screen
        self.shape = None

    def get_property_flag(self):
        return self.property_flag

    def get_shape(self):
        return self.shape

    def collides(self, hb):
        return False

    def point_in_hitbox(self, point):
        return False

# unlike rectangle, pygame has no collision functions for circles.
class circle(hitbox):
    
    def __init__(self, radius, x=0, y=0, draw=False, screen=None, property_flag=None):
        hitbox.__init__(self, draw=draw, screen=screen, property_flag=property_flag)
        self.shape = 'circle'
        self.x = x
        self.y = y
        self.radius = radius

    def set_position(self, x, y):
        self.x = x
        self.y = y
        # print(str(self.x) + ", " + str(self.y))

    def increment_position(self, x, y):
        self.x += x
        self.y += y

    def get_position(self):
        return (self.x, self.y)

    def point_in_hitbox(self, pos):
        if gamemath.distance_between_two_points((self.x, self.y),pos) < self.radius:
            return True
        return False

    def collides(self, hb):
        if hb.shape =='circle':
            if gamemath.distance_between_two_points(self.get_position(), hb.get_position()) < self.radius + hb.radius:
                return True
        elif hb.shape =='rectangle':
            coords = self.get_position()
            if hb.point_in_hitbox(coords):
                return True
            if gamemath.distance_between_two_points(coords, gamemath.closest_point_in_rectangle(coords, hb.rect)) < self.radius:
                return True
        return False

    def render(self):
        if self.draw:
            try: 
                pygame.draw.circle(self.screen, (255, 0, 0), (int(self.x), int(self.y)), self.radius, 1)
                pygame.draw.circle(self.screen, (255, 0, 0), (int(self.x), int(self.y)), 2, 1)
            except TypeError as err:
                print(err)
                self.draw = False


class rectangle(hitbox):

    # xy default to 0. when game object is created with a hitbox parameter, the gameobject
    # constructor calls the hitbox.set_position() function. offset variables set hitbox to
    # a position relative to the gameobject. if draw=True then a screen object must also be
    # provided. shape is a property used to communicate what the hitbox geometry is and how
    # to handle it

    def __init__(self, w, h, x=0, y=0, draw=False, screen=None, property_flag=None):
        hitbox.__init__(self, draw=draw, screen=screen, property_flag=property_flag)
        self.offset_x = w / -2.0
        self.offset_y = h / -2.0
        self.rect = pygame.Rect(x + self.offset_x, y + self.offset_y, w, h)
        self.shape = 'rectangle'

    # position minus offset should be the center?
    def get_position(self):
        return (self.rect.x - self.offset_x, self.rect.y-self.offset_y)

    def set_position(self, x, y):
        self.rect.center = x,y

    def increment_position(self, x, y):
        self.rect.center = self.rect.center[0] + x, self.rect.center[1] + y

    def get_top_left(self):
        return (self.rect.x, self.rect.y)

    def set_top_left(self, x, y):
        self.rect.topleft = x,y

    def point_in_hitbox(self, pos):
        if self.rect.collidepoint(pos):
            return True
        return False

    def collides(self, hb):
        if hb.shape == 'circle':
            if gamemath.distance_between_two_points(hb.get_position(), gamemath.closest_point_in_rectangle(hb.get_position(), self.rect)) < hb.radius:
                return True
            return False
        elif hb.shape == 'rectangle':
            return self.rect.colliderect(hb.rect)
        return False

    def render(self):
        if self.draw:
            try:
                pygame.draw.rect(self.screen, (255, 0, 0), self.rect, 1)        # the rectangle
                pygame.draw.circle(self.screen,(255, 0, 0), (int(self.rect.x - self.offset_x), int(self.rect.y - self.offset_y)), 2, 1)
            except TypeError as err:
                print(err)
                self.draw = False