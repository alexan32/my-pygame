import pygame
from abstractclasses import positionClass
from statemachines import(
    state,
    stateMachine
)


def strip_from_sheet(path, frame_width, frame_height, columns, rows=1):
    frames = []
    sheet = pygame.image.load(path)
    for j in range(rows):
        for i in range(columns):
            location = (frame_width * i, frame_height*j)
            frames.append(sheet.subsurface(pygame.Rect(location,(frame_width, frame_height))))
    return frames


"""image class:
image class contains a static image. loads an image from a file path on init. is drawn to the screen at a
preset offset from its XY position."""

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


"""
    spriteState requires 3 parameters and offers 4 optional parameters:

    key: string key for this state
    frames: number of frames in the animation.
    screen: the pygame surface to render to.
    next_state_key: string key for next state (default empty string.)
    pos: tuple x and y coordinates (default 0, 0)
    frame_rate: frames per second (default 7)
    exit_on_finish: boolean. (defualt False) if true, state will return the next_state_key after the animation has gone through one cycle.
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


