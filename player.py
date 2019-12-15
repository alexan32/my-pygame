from util_classes import (spriteState,
                        stateMachine,
                        gameObject)
from hitbox import circle
from util_abstractclasses import collidableClass
from util_functions import strip_from_sheet, checkForCollision


class playerObject(gameObject, collidableClass):

    def __init__(self, pos, controller, screen):   
        gameObject.__init__(self, pos, material='movable', id='player')

        self.speed = 0.05
        self.controller = controller

        # HITBOX
        # create circle hitbox w/ radius 16, set it to render, position it with player
        collidableClass.__init__(self, circle(10, True, screen), pos=(self.x, self.y), offset=(16,20))

        # GRAPHICS
        self.flip_sprite = False
        frames = strip_from_sheet("resources/knight_combined.png", 32, 32, 13)
        animations = {
            'idle' : spriteState('idle', frames[:1], screen),
            'walk' : spriteState('walk', frames[7:13], screen),
            'attack' : spriteState('attack', frames[1:7], screen, next_state_key='idle', exit_on_finish=True)
        }
        self.spriteHandler = stateMachine('idle', animations)


    def update(self, dt):
        input = self.controller.get_input()
        # movement
        x, y = 0, 0
        if input['left']: 
            x -= self.speed
        if input['right']:
            x += self.speed
        if input['up']: 
            y -= self.speed
        if input['down']:
            y += self.speed

        if (x != 0 or y != 0):
            if x != 0:
                self.increment_position(dt*x, 0)
                if x < 0:
                    self.flip_sprite = False
                else:
                    self.flip_sprite = True

            if y != 0:
                self.increment_position(0, dt*y)

            checkForCollision(self)

        self.handle_sprite(x, y, input)
        self.spriteHandler.update(dt)
        gameObject.update(self, dt)


    def increment_position(self, dx, dy):
        gameObject.increment_position(self, dx, dy)
        self.hitbox.set_position(self.x + self.hitbox_offset[0], self.y + self.hitbox_offset[1])


    def handle_sprite(self, dx, dy, input):
        
        if input['attack'] and self.spriteHandler.current_state.key != 'attack':
            self.spriteHandler.set_state('attack')

        if (dx != 0 or dy != 0) and self.spriteHandler.current_state.key != 'walk':
            self.spriteHandler.set_state('walk')
        
        elif (dx == 0 and dy == 0) and self.spriteHandler.current_state.key not in ['attack', 'idle']:
            self.spriteHandler.set_state('idle')


    def render(self):
        self.spriteHandler.render_at(self.x, self.y, self.flip_sprite)
        self.hitbox.render()