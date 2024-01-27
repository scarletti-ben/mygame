
import pygame, random
from .core.constants import FPS
from .core.paths import defaults

class DamageNumber:
    """Visual animation that throws a number into the air in a random arc to signify that an entity has taken damage"""

    descriptor: str = 'default'
    font_name: str = defaults['font']
    font_size: int = 140
    fade_rate: int = 3
    # start_colour: list = [255,255,255]
    transition_rate: int = 1
    gravity: pygame.Vector2 = pygame.Vector2(0, 0.5)

    def __init__(self, text, position, final_colour = [0,255,0]):
        """Initialise a DamageNumber object that will change colour and position on update"""
        self.text = str(text)
        self.position = position
        self.final_colour = final_colour
        self.velocity = pygame.Vector2(random.uniform(-2, 2), -random.uniform(5,15))
        self.count = 0
        self.maximum = FPS
        self.finished = False
        self.font = pygame.font.Font(self.font_name, self.font_size)

    def update(self):
        """Update the current size, velocity, colour and position"""

        self.font_size -= self.fade_rate
        self.position += self.velocity
        self.count += 1
        self.velocity += self.gravity

        decimal = self.count / self.maximum
        r_shift = int(255 - self.final_colour[0])
        g_shift = int(255 - self.final_colour[1])
        b_shift = int(255 - self.final_colour[2])
        r = max(int(255 - (r_shift * decimal)), 0)
        g = max(int(255 - (g_shift * decimal)), 0)
        b = max(int(255 - (b_shift * decimal)), 0)

        self.font = pygame.font.Font(self.font_name, self.font_size)
        
        self.colour = (r, g, b)
        if decimal >= 1:
            self.finished = True

    @property
    def surface(self):
        """Get the current text surface in the current colour"""
        return self.font.render(self.text, True, self.colour)
    
    @property
    def rectangle(self):
        """Get the current rectangle at current position"""
        rect = self.surface.get_rect(center = self.position)
        return rect

    def enqueue(self, queue):
        """Add self to the queue to get surface and rectangle at runtime"""
        queue.add_dynamic(self)