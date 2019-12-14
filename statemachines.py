import pygame
from abstractclasses import positionClass


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
    