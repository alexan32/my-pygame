from images import spriteAnimation, strip_from_sheet
import pygame


class state:

    def __init__(self):
        pass

    def update(self, dt):
        pass

    def enter_state(self):
        pass

    def exit_state(self):
        pass


class stateMachine:

    def __init__(self, initial_state_key, states_dict):
        self.states = states_dict
        self.current_state_key = initial_state_key
        self.current_state = self.states[initial_state_key]

    def set_state_full(self, state_key):
        self.current_state_key = state_key
        self.current_state.exit_state()
        self.current_state = self.states[state_key]
        self.current_state.enter_state()

    def set_state_simple(self, state_key):
        self.current_state_key = state_key
        self.current_state = self.states[state_key]

    def update(self, dt=0):
        self.current_state.update(dt)


class animationController(stateMachine):

    def __init__(self, screen):

        frames = strip_from_sheet('resources/knight_combined.png', 32, 32, 13)
        idle = spriteAnimation(screen, frames[0:1], (64,0))
        walk = spriteAnimation(screen, frames[7:13], (128,0))
        attack = spriteAnimation(screen, frames[1:7], (192,0))
        states_dict = {'idle' : idle, 'walk' : walk, 'attack' : attack}
        stateMachine.__init__(self, 'idle', states_dict)
        self.time_elapsed = 0

    def render(self):
        self.current_state.render()

    def update(self, dt):
        self.current_state.update(dt)
        self.time_elapsed += dt
        # every 5 seconds
        if self.time_elapsed > 3000:
            print(self.time_elapsed)
            self.time_elapsed = 0.0
            self.set_state_simple(self.next_state())
        # end attack animation after first cycle
        if self.current_state_key == "attack" and self.current_state.index == 6:
            self.set_state_simple(self.next_state())

    def next_state(self):
        if self.current_state_key == 'idle':
            return 'walk'
        elif self.current_state_key == 'walk':
            return 'attack'
        else:
            return 'idle'

