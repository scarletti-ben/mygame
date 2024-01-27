
import pygame
from ..core.tools import get_random_colour, get_inverted_colour

class TestRectangle:
    width = 180
    height = 280
    weight = 6
    background = [100,100,100]

    def __init__(self):
        """Initialise a rectangle and give it a random colour"""
        self.rectangle = pygame.Rect(0, 0, self.width, self.height)
        self.outer = get_random_colour()
        self.inner = get_inverted_colour(self.outer)

    @property
    def surface(self):
        """Get current surface"""
        surf = pygame.Surface(self.rectangle.size)
        rect = self.rectangle.copy()
        rect.topleft = [0,0]
        pygame.draw.rect(surf, self.background, rect)
        pygame.draw.rect(surf, self.outer, rect, self.weight * 2)
        pygame.draw.rect(surf, self.inner, rect, self.weight)
        return surf
    
    def draw(self, display):
        """Draw current rectangle to display"""
        display.blit(self.surface, self.rectangle)