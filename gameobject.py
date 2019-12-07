import pygame
import gamemath
from controller import controller


object_list = []            # all instantiated gameObjects 
collision_list = []         # all instantiated gameObjects that have hitboxes
id_counter = -1


def get_id():
    global id_counter
    id_counter += 1
    return id_counter


class gameObject:

    def __init__(self, x, y, hitbox=None):
        self.id = get_id()
        object_list.append(self)
        self.x = x
        self.y = y
        self.hitbox = hitbox
        if hitbox != None:
            self.hitbox.set_position(self.x, self.y)
            collision_list.append(self)
        print(str(self.id) + ' created at ' + str(self.x) + ',' + str(self.y))

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_position_by_tuple(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def increment_position(self, x, y):
        self.x += x
        self.y += y

    def update(self, dt):
        pass

    def render(self):
        if self.hitbox != None:
            self.hitbox.render()


# imageObjects have an image and can be drawn to the pygame screen
# offset variables describe the displacement of the image relative
# to the objects x and y coordinates
class imageObject(gameObject):

    def __init__(self, screen, image, x, y, hitbox=None, sprite=None):      # get sprite system working, remove image
        gameObject.__init__(self, x, y, hitbox=hitbox)
        self.screen = screen                                                                  
        self.image = image
        self.sprite = sprite

    def render(self):
        self.image.render(self.x, self.y)
        gameObject.render(self)


class mobile(imageObject):
     
    def __init__(self, screen, image, x, y, speed=0.2, hitbox=None, sprite=None):
        imageObject.__init__(self, screen, image, x, y, hitbox=hitbox, sprite=sprite)
        self.speed = speed

    # moves the object a small amount, and moves the hitbox
    def increment_position(self, x, y):
        self.x += x
        self.y += y
        if self.hitbox != None:
            self.hitbox.set_position(self.x, self.y)
            for obj in object_list:
                if obj != self and obj.hitbox != None:
                    # if collision detected
                    if self.hitbox.collides(obj.hitbox):
                        self.handle_collision(x, y, obj.hitbox)

    # logic here for what to do on collision
    def handle_collision(self, x, y, hb):
        pass


class controlledObject(mobile):

    def __init__(self, screen, image, x, y, controller, speed=0.2, hitbox=None, sprite=None):
        mobile.__init__(self, screen, image, x, y, speed=speed, hitbox=hitbox, sprite=sprite)
        self.controller = controller
        self.input = self.controller.get_input()

    def update(self, dt):
        self.input = self.controller.get_input()


class playerObject(controlledObject):

    def __init__(self, screen, image, x, y, controller, speed=0.2, hitbox=None, sprite=None):
        controlledObject.__init__(self, screen, image, x, y, controller, speed=speed, hitbox=hitbox, sprite=sprite)

    def update(self, dt):
        controlledObject.update(self, dt)
        if self.input['left']: 
            self.increment_position(-self.speed * dt, 0)
        if self.input['right']:
            self.increment_position(self.speed * dt, 0)
        if self.input['up']:
            self.increment_position(0, -self.speed * dt)
        if self.input['down']:
            self.increment_position(0, self.speed * dt)

    def handle_collision(self, x, y, hb):
        if self.hitbox.shape == 'circle':
            if hb.shape == 'rectangle':
                self.circle_on_rectangle(x, y, hb)
            elif hb.shape == 'circle':
                self.circle_on_circle(x, y, hb)
        elif self.hitbox.shape == 'rectangle':
            if hb.shape == 'rectangle':
                self.rectangle_on_rectangle(x, y, hb)
            elif hb.shape == 'circle':
                self.rectangle_on_circle(x, y, hb)

    def rectangle_on_circle(self, x, y, hb):
        if hb.property_flag == 'wall':
            closest_point = gamemath.closest_point_in_rectangle(hb.get_position(), self.hitbox.rect)
            # calculate the angle:
            theta = gamemath.radians_between_two_points(closest_point, hb.get_position())
             # calculate the distance of the intersect:
            d = hb.radius - gamemath.distance_between_two_points(closest_point, hb.get_position())
            # move back d
            xy = gamemath.get_xy_move(theta)
            self.hitbox.increment_position(xy[0]*-d, xy[1]*-d)
            self.set_position_by_tuple(self.hitbox.get_position())

    def circle_on_rectangle(self, x, y, hb):
        if hb.property_flag == 'wall':
            closest_point = gamemath.closest_point_in_rectangle(self.hitbox.get_position(), hb.rect)
            # calculate the angle:
            theta = gamemath.radians_between_two_points(self.hitbox.get_position(), closest_point)
            # calculate the distance of the intersect:
            d = self.hitbox.radius - gamemath.distance_between_two_points(self.hitbox.get_position(), closest_point)
            # move back d
            xy = gamemath.get_xy_move(theta)
            self.hitbox.increment_position(xy[0]*-d, xy[1]*-d)
            self.set_position_by_tuple(self.hitbox.get_position())

    def circle_on_circle(self, x, y, hb):
        if hb.property_flag == 'wall':
            # calculate the angle:
            theta = gamemath.radians_between_two_points(self.hitbox.get_position(), hb.get_position())
            # calculate the distance of the intersect:
            d = hb.radius + self.hitbox.radius - gamemath.distance_between_two_points(self.hitbox.get_position(), hb.get_position())
            # move back d
            xy = gamemath.get_xy_move(theta)
            self.hitbox.increment_position(xy[0]*-d, xy[1]*-d)
            self.set_position_by_tuple(self.hitbox.get_position())

    def rectangle_on_rectangle(self, x, y, hb):
        if hb.property_flag == 'wall':
            if x > 0: # Moving right; Hit the left side of the wall
                self.hitbox.rect.right = hb.rect.left
            elif x < 0: # Moving left; Hit the right side of the wall
                self.hitbox.rect.left = hb.rect.right
            if y > 0: # Moving down; Hit the top side of the wall
                self.hitbox.rect.bottom = hb.rect.top
            elif y < 0: # Moving up; Hit the bottom side of the wall
                self.hitbox.rect.top = hb.rect.bottom
            self.set_position_by_tuple(self.hitbox.get_position())

