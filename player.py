from gameobject import gameObject
from statemachines import stateMachine
from images import (spriteState, 
                    strip_from_sheet)


class playerObject(gameObject):

    def __init__(self, pos, controller, screen):   
        gameObject.__init__(self, pos, id='player')

        self.speed = 0.05
        self.moving = False
        self.flip_sprite = False
        self.controller = controller    # controller updated outside of class

        frames = strip_from_sheet("resources/knight_combined.png", 32, 32, 13)
        animations = {
            'idle' : spriteState('idle', frames[:1], screen),
            'walk' : spriteState('walk', frames[7:13], screen),
            'attack' : spriteState('attack', frames[1:7], screen, next_state_key='idle', exit_on_finish=True)
        }
        self.spriteHandler = stateMachine('idle', animations)

    def render(self):
        self.spriteHandler.render_at(self.x, self.y, self.flip_sprite)

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

        if x != 0:
            self.increment_position(dt*x, 0)
            if x < 0:
                self.flip_sprite = False
            else:
                self.flip_sprite = True
        if y != 0:
            self.increment_position(0, dt*y)

        self.handle_sprite(x, y, input)
        self.spriteHandler.update(dt)

        gameObject.update(self, dt)


    def handle_sprite(self, dx, dy, input):
        
        if input['attack'] and self.spriteHandler.current_state.key != 'attack':
            self.spriteHandler.set_state('attack')

        if (dx != 0 or dy != 0) and self.spriteHandler.current_state.key != 'walk':
            self.spriteHandler.set_state('walk')
        
        elif (dx == 0 and dy == 0) and self.spriteHandler.current_state.key not in ['attack', 'idle']:
            self.spriteHandler.set_state('idle')

