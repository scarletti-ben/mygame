
import pygame
import os
from .paths import defaults, assets
from .constants import *

# ~ ======================================================================
# - Section 1: Collection of pygame-based local mygame classes
    # - Used to return pygame objects and improve native functionality
# ~ ======================================================================

class Image:
    """Image import class for importing  files from paths at different scales and sizes"""
    def __new__(cls, path = None, scale = None, size = None, smooth = False) -> pygame.Surface:
        """Get image from filepath with optional parameters for scale or size"""
        path = defaults['scroll'] if path is None else path
        try:
            image = pygame.image.load(path).convert_alpha()
        except FileNotFoundError:
            print(f'{path} does not exist, generating default image')
            image = pygame.Surface([100,100], pygame.SRCALPHA)
            pygame.draw.rect(image, [128,200,0], [0,0,100,100], 14)
        if scale is not None:
            size = image.get_width() * scale, image.get_height() * scale
        if size is not None:
            if smooth:
                image = pygame.transform.smoothscale(image, size)
            else:
                image = pygame.transform.scale(image, size)
        return image
    
class Negative:
    directory = assets

    def __init__(self, filename, scale = None, size = None, smooth = False):
        """Create an image negative object to develop an image later"""
        self.filename = filename
        self.scale = scale
        self.size = size
        self.smooth = smooth

    @property
    def filepath(self):
        """Get the filepath to the image"""
        return os.path.join(self.directory, self.filename)

    def get_developed(self) -> pygame.Surface:
        """Convert the negative to a pygame Surface and return"""
        return Image(self.filepath, self.scale, self.size, self.smooth)
    
class Surface:
    def __new__(cls, w = 64, h = 64, colour = None) -> pygame.Surface:
        """Get alpha enabled pygame surface, transparent if no colour"""
        surface = pygame.Surface([w, h]).convert_alpha()
        colour = [0,0,0,0] if colour is None else colour
        surface.fill(colour)
        return surface

class Subsurface:
    def __new__(cls, image, rectangle, scale = None, size = None) -> pygame.Surface:
        """Get subsurface from image and resize or apply scaling"""
        image = image.subsurface(rectangle)
        initial_size = image.get_size()
        if scale is not None:
            size = image.get_width() * scale, image.get_height() * scale
            image = pygame.transform.scale(image, size)
        elif size is not None:
            image = pygame.transform.scale(image, size)
        current_size = image.get_size()
        print(f'Subsurface of size {initial_size} imported at {current_size}')
        return image

class Mask:
    def __new__(cls, surface, threshold = 127) -> pygame.mask.Mask:
        """Convert pygame surface to pygame mask with threshold"""
        return pygame.mask.from_surface(surface, threshold)

class Rectangle:
    def __new__(cls, surface, **kwargs) -> pygame.rect.Rect:
        """Convert pygame surface to pygame rectangle"""
        return surface.get_rect(**kwargs)

class Display:
    def __new__(cls, width, height, flags = 0, **kwargs) -> pygame.Surface:
        """Get pygame display surface"""
        return pygame.display.set_mode([width, height], flags, **kwargs)
    
# class Display:
#     def __new__(cls, width = None, height = None, flags = 0, **kwargs) -> pygame.Surface:
#         """Get pygame display surface"""
#         if width is None or height is None:
#             if FULLSCREEN:
#                 pygame.display.set_mode([W, H], pygame.FULLSCREEN)
#             else:
#                 pygame.display.set_mode([W, H])
#         else:
#             return pygame.display.set_mode([width, height], flags, **kwargs)
    
class Clock:
    def __new__(cls) -> pygame.time.Clock:
        """Get pygame clock object"""
        return pygame.time.Clock()

class Vector:
    def __new__(cls, x, y)  -> pygame.Vector2:
        """Get 2 point vector from x, y coordinates"""
        return pygame.Vector2(x, y)
    
class Font:
    def __new__(cls, name = None, size = None, bold = True) -> pygame.font.Font:
        """If name contains file extension load via the pygame Font class. Otherwise load it as SysFont. User fonts are not affected by the bold argument."""
        name = FONT_NAME if name is None else name
        size = FONT_SIZE if size is None else size
        if name.endswith(('.ttf', '.otf')):
            return pygame.font.Font(name, size)
        else:
            return pygame.font.SysFont(name, size, bold)
        
class Sound:
    def __init__(self, filepath):
        """Create a pygame sound object to be played as needed"""
        return pygame.mixer.Sound(filepath)
    
if __name__ != "__main__":
    print("""
-------------------------------------
mygame.locals.py imported successfully
-------------------------------------
    Package: mygame
    Purpose: Add locals from mygame that are useful in the local namespace
    Information: 
        - Also imports constants from mygame.constants
""")