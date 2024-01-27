
import pygame

LENGTH_DIVISOR = 3
LENGTH_MINIMUM = 20

# ~ Corners Class
class Corners:
    descriptor = 'selection'
    inner_colour = [20,20,20]
    outer_colour = [255,255,255]

    def __init__(self, sprite, speed = 1, scale = 1, thickness = 4, offset = 20, **kwargs):
        """Get default attributes from a given sprite"""
        self.sprite = sprite
        self.stages = 35 // speed
        self.scale = scale
        self.offset = self.offset_minimum = offset
        self.thickness = thickness
        self.offset_maximum = 100
        self.interval = (self.offset_maximum - self.offset_minimum) / self.stages
        self.flipped = False
        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self):
        """Update offset at a given rate, and flip direction to move inwards when edges reached"""
        if not self.flipped:
            self.offset += self.interval
            if self.offset > self.offset_maximum:
                self.offset = self.offset_maximum
                self.flipped = not self.flipped
        else:
            self.offset -= self.interval
            if self.offset < self.offset_minimum:
                self.offset = self.offset_minimum
                self.flipped = not self.flipped

    def draw(self, display, animating = True, **kwargs):
        """Draw animated corner surface to draw queue, optionally update corner positions"""
        if animating:
            self.update()
        w, h = self.sprite.rectangle.w + self.offset, self.sprite.rectangle.h + self.offset
        length = max((min(*self.sprite.rectangle.size) / LENGTH_DIVISOR) * self.scale, LENGTH_MINIMUM)
        surface = pygame.Surface([w, h], pygame.SRCALPHA)
        rectangle = surface.get_rect()
        inner_colour = kwargs.get('inner_colour', self.inner_colour)
        outer_colour = kwargs.get('outer_colour', self.outer_colour)
        pygame.draw.rect(surface, inner_colour, rectangle, self.thickness * 2)
        pygame.draw.rect(surface, outer_colour, rectangle, self.thickness)
        surface.fill(0, rectangle.inflate(-length, 0))
        surface.fill(0, rectangle.inflate(0, -length))
        rectangle.center = self.sprite.rectangle.center
        display.blit(surface, rectangle)

    def enqueue(self, queue, animating = True, **kwargs):
        """Add surface and rectangle to draw queue"""
        if animating:
            self.update()
        w, h = self.sprite.rectangle.w + self.offset, self.sprite.rectangle.h + self.offset
        length = max((min(*self.sprite.rectangle.size) / LENGTH_DIVISOR) * self.scale, LENGTH_MINIMUM)
        surface = pygame.Surface([w, h], pygame.SRCALPHA)
        rectangle = surface.get_rect()
        inner_colour = kwargs.get('inner_colour', self.inner_colour)
        outer_colour = kwargs.get('outer_colour', self.outer_colour)
        pygame.draw.rect(surface, inner_colour, rectangle, self.thickness * 2)
        pygame.draw.rect(surface, outer_colour, rectangle, self.thickness)
        surface.fill(0, rectangle.inflate(-length, 0))
        surface.fill(0, rectangle.inflate(0, -length))
        rectangle.center = self.sprite.rectangle.center
        queue.add(surface, rectangle, self.descriptor)