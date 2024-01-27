
import pygame

class Rotator:
    """Simple rotator object to give Sprite objects rotation"""

    preference: str = 'rotozoom'
    
    def __init__(self, sprite, degrees = 0):
        """Create a rotator object to handle rotation for its sprite"""
        self.sprite = sprite
        self.degrees = degrees
    
    @property
    def surface(self):
        """Get the rotated version of the sprite surface"""
        if self.degrees != 0:
            if self.preference == 'rotozoom':
                return pygame.transform.rotozoom(self.sprite.surface, self.degrees, 1)
            else:
                return pygame.transform.rotate(self.sprite.surface, self.degrees)
        else:
            return self.sprite.surface

    @property
    def rectangle(self):
        """Get current rotated surface centered around the sprite rectangle center"""
        if self.degrees != 0:
            rect = self.surface.get_rect(center = self.sprite.rectangle.center)
            return rect
        else:
            return self.sprite.rectangle

    @property
    def mask(self):
        """Get mask from the current surface"""
        if self.degrees != 0:
            return pygame.mask.from_surface(self.surface)
        else:
            return self.sprite.mask
        
    def reset(self):
        """Set degrees to zero to disable rotation"""
        self.degrees = 0
        
    def enqueue(self, queue):
        """Add surface and rectangle to draw queue"""
        queue.add(self.surface, self.rectangle, self.sprite.descriptor)