import pygame
import logging
import util_functions
from util_abstractclasses import *
from pygame import(
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_a,
    K_d,
    K_s,
    K_w,
    K_e,
    key
)

# LOGGING
logger=logging.getLogger() 
logger.setLevel(logging.DEBUG)

# ---------------------------------------------------------------------
# GAME OBJECTS
# ---------------------------------------------------------------------
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
            self.id = util_functions.generate_id()
        else:
            self.id = id
        util_functions.add_gameobject_to_dict(self)

    def destroy(self):
        util_functions.remove_gameobject_from_dict(self)

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
    
# ---------------------------------------------------------------------
# IMAGES
# ---------------------------------------------------------------------

class image(positionClass):

    def __init__(self, pos,  path, screen, draw=True):
        positionClass.__init__(self, pos)
        self.image = pygame.image.load(path)
        self.screen = screen
        self.draw = draw

    def render(self):
        if self.draw:
            self.screen.blit(self.image, (self.x, self.y))


class spriteAnimation(pygame.sprite.Sprite, positionClass):

    def __init__(self, frames, screen, pos=(0,0), frame_rate=7):
        pygame.sprite.Sprite.__init__(self)
        positionClass.__init__(self, pos)
        self.screen = screen
        self.frames = frames
        self.index = 0
        self.frame_rate = 7
        self.frame_timer = 0.0

    def render(self):
        self.screen.blit(self.frames[self.index], (self.x, self.y))

    def render_at(self, x, y, mirrored=False):
        if mirrored:
            self.screen.blit(pygame.transform.flip(self.frames[self.index], True, False), (x,y))
        else:
            self.screen.blit(self.frames[self.index], (x, y))

    def update(self, dt):
        self.update_frame(dt)

    def update_frame(self, dt):
        self.frame_timer += dt 
        # frame change when time change > 1 second / fps
        if self.frame_timer > 1000.0 / self.frame_rate:
            self.index += 1
            self.frame_timer = 0.0
            if self.index >= len(self.frames):
                self.index = 0 


# ---------------------------------------------------------------------
# STATE MACHINE
# ---------------------------------------------------------------------


class state:

    def __init__(self, key, next_state_key=""):
        self.key = key
        self.state_timer = 0.0
        self.next_state_key = next_state_key

    def update_state(self, dt):
        self.state_timer += dt
        return self.key

    def enter_state(self):
        pass

    def exit_state(self):
        pass

"""
    spriteState requires 3 parameters and offers 4 optional parameters:

    key: string key for this state
    frames: number of frames in the animation.
    screen: the pygame surface to render to.
    next_state_key: string key for next state (default empty string.)
    pos: tuple x and y coordinates (default 0, 0)
    frame_rate: frames per second (default 7)
    exit_on_finish: boolean. (defualt False) if true, state will return the next_state_key after one animation cycle.
    do not set to true unless you have assigned next_state_key a value

    when update is called, sprite state will return a key value. This allows the state logic to choose the next state.
"""
class spriteState(spriteAnimation, state):

    def __init__(self, key, frames, screen, next_state_key="", pos=(0,0), frame_rate=7, exit_on_finish=False):
        spriteAnimation.__init__(self, frames, screen, pos=pos, frame_rate=frame_rate)
        state.__init__(self, key, next_state_key)
        self.exit_on_finish = exit_on_finish
        self.return_key = self.key

    def enter_state(self):
        self.return_key = self.key
        self.index = 0          # reset old values
        self.frame_timer = 0

    def update_state(self, dt):
        self.update_frame(dt) 
        self.state_timer += dt
        return self.return_key
    
    def update_frame(self, dt):
        self.frame_timer += dt 
        if self.frame_timer > 1000.0 / self.frame_rate:
            self.index += 1
            self.frame_timer = 0.0
            if self.index >= len(self.frames):
                self.index = 0  
                if self.exit_on_finish:
                    self.return_key = self.next_state_key


class stateMachine:

    def __init__(self, initial_state_key, states_dict):
        self.states = states_dict
        self.current_state = self.states[initial_state_key]

    def set_state(self, state_key):
        self.current_state.exit_state()
        # print('entering state: {}'.format(state_key))
        self.current_state = self.states[state_key]
        self.current_state.enter_state()

    def update(self, dt=0):
        key = self.current_state.update_state(dt)
        if key != self.current_state.key:
            self.set_state(key)

    def render(self):
        self.current_state.render()

    def render_at(self, x, y, flipped=False):
        self.current_state.render_at(x, y, flipped)


# ---------------------------------------------------------------------
# CONTROLLER
# ---------------------------------------------------------------------

class controller:

    def __init__(self):
        self.input = {
            'left' : False,
            'right' : False,
            'up' : False,
            'down' : False,
            'attack' : False,
            'quit' : False
        }
        self.key_map = {
            'left' : K_LEFT,
            'right' : K_RIGHT,
            'up' : K_UP,
            'down' : K_DOWN,
            'attack' : K_e,
            'quit': K_ESCAPE
        }
        self.alt_map = {
            'left' : K_a,
            'right' : K_d,
            'up' : K_w,
            'down' : K_s,
            'attack' : K_e,
            'quit' : K_ESCAPE
        }

    def set_keys(self, map):
        self.key_map = map

    def set_alternate_keys(self, map):
        self.alt_map = map
    
    def update(self):
        key = pygame.key.get_pressed()
        self.input['left'] = key[self.key_map['left']] or key[self.alt_map['left']]
        self.input['right'] = key[self.key_map['right']] or key[self.alt_map['right']]
        self.input['up'] = key[self.key_map['up']] or key[self.alt_map['up']]
        self.input['down'] = key[self.key_map['down']] or key[self.alt_map['down']]
        self.input['attack'] = key[self.key_map['attack']]
        self.input['quit'] =  key[self.key_map['quit']]

    def get_input(self):
        return self.input