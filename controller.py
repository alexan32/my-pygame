import pygame
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
    key,
    mouse
)

hold_sensitivity = 200


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
            'quit' : False,
            'mouse_pos' : (0,0),
            'mouse_buttons' : (False, False, False),
            'mouse_held' : False
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
        self.left_mouse_held = False
        self.hold_timer = 0.0

    def set_keys(self, map):
        self.key_map = map

    def set_alternate_keys(self, map):
        self.alt_map = map
    
    def update(self, dt):
        key = pygame.key.get_pressed()
        self.input['left'] = key[self.key_map['left']] or key[self.alt_map['left']]
        self.input['right'] = key[self.key_map['right']] or key[self.alt_map['right']]
        self.input['up'] = key[self.key_map['up']] or key[self.alt_map['up']]
        self.input['down'] = key[self.key_map['down']] or key[self.alt_map['down']]
        self.input['attack'] = key[self.key_map['attack']]
        self.input['quit'] =  key[self.key_map['quit']]
        
        self.input['mouse_pos'] = mouse.get_pos()
        self.input['mouse_buttons'] = mouse.get_pressed()


        if self.input['mouse_buttons'][0]:
            self.hold_timer += dt
            if self.hold_timer > hold_sensitivity and not self.input['mouse_held']:
                self.input['mouse_held'] = True
                print('held')
        else:
            self.hold_timer = 0.0
            self.input['mouse_held'] = False

    def get_input(self):
        return self.input