
from ..core.paths import intents
from ..core.locals import Image
from ..sprite.sprite import Sprite
from ..experimental.stateA01 import state

class Intent(Sprite):

    filepath = intents['attack3']
    descriptor = 'intent'

    def __init__(self, entity) -> None:
        """Intent object for entity to draw visual intent to the display"""
        self.entity = entity
        self.images = {
            'damage': Image(intents['attack3']),
            'block': Image(intents['defend'])
        }
        self.value = 5
        self.rectangle = self.images['damage'].get_rect()

    def enqueue(self, queue):
        """Add all visuals to the draw queue"""

        visuals = []

        integer, recipient, flavour = self.entity.intent

        surface = self.images[flavour]
        # rectangle = surface.get_rect()
        # healthbar_rectangle = self.entity.healthbar.text_rectangle.move(0,-32)
        # rectangle.midbottom = healthbar_rectangle.midtop


        visuals.append((surface, self.rectangle, self.descriptor))

        inset = 4
        x, y = self.rectangle.move(-8, 0).midleft
        

        if integer is not None and flavour == 'damage':
            
            shadow_offset = 4
            for n in range(shadow_offset):
                s = self.font.render(str(integer), True, [20,20,20])
                r = s.get_rect(center = [x - inset - n, y - inset + n])
                queue.add(s, r, 'overlay')

            s = self.font.render(str(integer), True, [0,255,200])
            r = s.get_rect(center = [x - inset, y - inset])

            queue.add(s, r, 'overlay')


        
        for surface, rectangle, descriptor in visuals:
            queue.add(surface, rectangle, descriptor)

    def get_tooltip_lines(self):
        """Get lines to be rendered by tooltip"""
        integer, recipient, flavour = self.entity.intent
        return [
            f'Value: {integer}',
            f'Flavour: {flavour}',
            f'Recipient: {recipient}']
    