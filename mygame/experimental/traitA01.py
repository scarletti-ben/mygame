
import pygame
from ..sprite.sprite import Sprite
from ..core.paths import defaults
from ..core.locals import Image

class Trait(Sprite):
    """Default Trait docstring"""

    image: pygame.Surface = None
    descriptor: str = 'trait'
    filepath: str = defaults['trait']
    stacking: str = 'value'
    value: int = None
    count: int = None
    turns: int = None

    def __init__(self, image = None, stacking = None, value = None, count = None, turns = None):
        """Create trait object from image"""
        if image is None:
            if self.image is None:
                image = Image(self.filepath, scale = 1)
            else:
                image = self.image
        self.surface = image
        self.image = image
        self.rectangle = image.get_rect()
        self.stacking = self.stacking if stacking is None else stacking
        self.value = self.value if value is None else value
        self.count = self.count if count is None else count
        self.turns = self.turns if turns is None else turns

    subclasses = {}
    def __init_subclass__(cls, **kwargs):
        """When a subclass is created add it to the subclass dictionary"""
        super().__init_subclass__(**kwargs)
        key = cls.__name__.lower()
        cls.subclasses[key] = cls
        print("\nSubclass of Trait class created:", cls.__name__)

    def get_integer_overlay(self):
        """Get string based on current stacking"""
        if self.stacking == 'turns':
            return self.turns
        elif self.stacking == 'count':
            return self.count
        elif self.stacking == 'value':
            return self.value
        elif self.stacking == None:
            return self.value

    def enqueue(self, queue, *args, **kwargs):
        """Add current surface and rectangle to the draw queue"""
        
        inset = 4
        x, y = self.rectangle.bottomright
        integer = self.get_integer_overlay()

        if integer is not None:
            
            shadow_offset = 4
            for n in range(shadow_offset):
                s = self.font.render(str(integer), True, [20,20,20])
                r = s.get_rect(center = [x - inset - n, y - inset + n])
                queue.add(s, r, 'overlay')


            s = self.font.render(str(integer), True, [0,255,200])
            r = s.get_rect(center = [x - inset, y - inset])

            queue.add(s, r, 'overlay')

        queue.add(self.surface, self.rectangle, self.descriptor, **kwargs)

    def get_tooltip_lines(self):
        """Get lines to be rendered by tooltip"""
        return [
            f'Trait: {self.__class__.__name__}',
            f'Stacking: {str(self.stacking).title()}',
            f'V:{self.value} C:{self.count} T:{self.turns}',
            f'- - -',
            f'{self.__class__.__doc__}']