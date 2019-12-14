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
    key
)

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