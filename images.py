import pygame


def strip_from_sheet(path, frame_width, frame_height, columns, rows=1):
    frames = []
    sheet = pygame.image.load(path)
    for j in range(rows):
        for i in range(columns):
            location = (frame_width * i, frame_height*j)
            frames.append(sheet.subsurface(pygame.Rect(location,(frame_width, frame_height))))
    return frames


class staticImage:

    def __init__(self, screen, path, offset_x=0, offset_y=0, draw=True):
        self.image = pygame.image.load(path)
        self.screen = screen
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.draw = draw
    
    def set_offset(self, offset_x, offset_y):
        self.offset_x = offset_x
        self.offset_y = offset_y

    def render(self, x, y):
        if self.draw:
            self.screen.blit(self.image, (x + self.offset_x, y + self.offset_y))


class spriteAnimation(pygame.sprite.Sprite):

    def __init__(self, screen, frames, pos=(0,0), frame_rate=7):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.pos = pos
        self.frames = frames
        self.index = 0
        self.frame_rate = 7
        self.time_since_frame_start = 0.0

    def render(self):
        self.screen.blit(self.frames[self.index], (self.pos[0], self.pos[1]))

    def update(self, dt):
        # get time increment in milliseconds
        self.time_since_frame_start += dt 
        # frame change when time change > 1 second / number of frames per second
        if self.time_since_frame_start > 1000.0 / self.frame_rate:
            self.index += 1
            self.time_since_frame_start = 0.0
            if self.index >= len(self.frames):
                self.index = 0  


