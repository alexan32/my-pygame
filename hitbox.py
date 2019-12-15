import pygame
import gamemath
from util_abstractclasses import positionClass


class hitbox(positionClass):

    def __init__(self, draw=False, screen=None):
        positionClass.__init__(self)
        self.draw = draw
        self.screen = screen
        self.shape = None

    def get_shape(self):
        return self.shape

    def collides(self, hb):
        return False

    def point_in_hitbox(self, point):
        return False


class circle(hitbox):
    
    def __init__(self, radius, draw=False, screen=None):
        hitbox.__init__(self, draw=draw, screen=screen)
        self.shape = 'circle'
        self.radius = radius

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
                pygame.draw.circle(self.screen, (255, 0, 0), (int(self.x), int(self.y)), self.radius, 1)    # circle border
                pygame.draw.circle(self.screen, (255, 0, 0), (int(self.x), int(self.y)), 2, 1)              # circle center
            except TypeError as err:
                print(err)
                self.draw = False


class rectangle(hitbox):

    def __init__(self, w, h, draw=False, screen=None):
        hitbox.__init__(self, draw=draw, screen=screen)
        self.rect = pygame.Rect(self.x, self.y, self.x+w, self.y+h)
        self.shape = 'rectangle'

    def get_position(self):
        return (self.rect.x, self.rect.y)

    def set_position(self, x, y):
        self.rect.topleft = x,y

    def increment_position(self, dx, dy):
        self.rect.center = self.rect.topleft + dx, self.rect.topleft[1] + dy

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
                pygame.draw.rect(self.screen, (255, 0, 0), self.rect, 1)                # the rectangle
                pygame.draw.circle(self.screen,(255, 0, 0), (self.rect.center), 2, 1)   # center of rect
            except TypeError as err:
                print(err)
                self.draw = False


    