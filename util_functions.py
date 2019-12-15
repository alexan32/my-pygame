import logging
import pygame
import gamemath

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
render_list = []

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


# ---------------------------------------------------------------------
# COLLISION
# ---------------------------------------------------------------------


"""should be called by a gameobject whenever it is moving"""

def checkForCollision(mover):
    for obj in collidable_list:
        if obj != mover and mover.hitbox.collides(obj.hitbox):
            handleCollision(mover, obj)

def checkForCollisionIgnore(mover, ignoreList):

    for obj in collidable_list:
        if obj != mover and obj not in ignoreList and mover.hitbox.collides(obj.hitbox):
            handleCollision(mover, obj)

"""determines how gameobjects should behave when a collision occurs"""

def handleCollision(objOne, objTwo):
    # MATERIAL
    if objOne.material == objTwo.material:
        move = physicsCollision(objOne, objTwo)
        # move objOne back 1/2 move
        objOne.hitbox.increment_position(move[0][0] * move[1] * -0.5, move[0][1] * move[1] * -0.5)
        objOne.set_position(objOne.hitbox.get_position()[0] - objOne.hitbox_offset[0], objOne.hitbox.get_position()[1]- objOne.hitbox_offset[1])
        # move objTwo forward 1/2 move
        objTwo.hitbox.increment_position(move[0][0] * move[1] * 0.5, move[0][1] * move[1] * 0.5)
        objTwo.set_position(objTwo.hitbox.get_position()[0] - objTwo.hitbox_offset[0], objTwo.hitbox.get_position()[1]- objTwo.hitbox_offset[1])
        # prevent from getting pushed through other objects
        checkForCollisionIgnore(objTwo, [objOne])
    elif objOne.material == 'solid' and objTwo.material == 'movable':
        pass
    
    elif objOne.material == 'movable' and objTwo.material == 'solid':
        move = physicsCollision(objOne, objTwo)
        objOne.hitbox.increment_position(move[0][0] * -move[1], move[0][1] * -move[1])
        objOne.set_position(objOne.hitbox.get_position()[0] - objOne.hitbox_offset[0], objOne.hitbox.get_position()[1]- objOne.hitbox_offset[1])
    
    elif objOne.material is None or objTwo.material is None:
        pass
    
    else:
        logger.warn('unhandled collision between gameObjects {} and {}'.format(objOne.id, objTwo.id))

    # FLAG

def physicsCollision(objOne, objTwo):
    if objOne.hitbox.shape == 'circle':
        if objTwo.hitbox.shape == 'rectangle':
            # self.circle_on_rectangle(objOne, objTwo)
            pass

        elif objTwo.hitbox.shape == 'circle':
            return circle_on_circle(objOne, objTwo)
    
    elif objOne.hitbox.shape == 'rectangle':
        if objTwo.hitbox.shape == 'rectangle':
            # self.rectangle_on_rectangle(x, y, hb)
            pass
        
        elif objTwo.hitbox.shape == 'circle':
            # self.rectangle_on_circle(objOne, objTwo)
            pass


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


def circle_on_circle(objOne, objTwo):
    hbOne = objOne.hitbox
    hbTwo = objTwo.hitbox
    theta = gamemath.radians_between_two_points(hbOne.get_position(), hbTwo.get_position())
    d = objTwo.hitbox.radius + hbOne.radius - gamemath.distance_between_two_points(hbOne.get_position(), hbTwo.get_position())
    xy = gamemath.get_xy_move(theta)
    return (xy, d)
    # hbOne.increment_position(xy[0]*-d, xy[1]*-d)
    # objOne.set_position(hbOne.get_position()[0] - objOne.hitbox_offset[0], hbOne.get_position()[1]- objOne.hitbox_offset[1])


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