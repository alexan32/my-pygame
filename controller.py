import pygame


class controller:

    def __init__(self):
        self.input = {
            'left' : False,
            'right' : False,
            'up' : False,
            'down' : False
        }
        self.key_map = {
            'left' : pygame.K_LEFT,
            'right' : pygame.K_RIGHT,
            'up' : pygame.K_UP,
            'down' : pygame.K_DOWN
        }
        self.alt_map = {
            'left' : pygame.K_a,
            'right' : pygame.K_d,
            'up' : pygame.K_w,
            'down' : pygame.K_s
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

    def get_input(self):
        return self.input