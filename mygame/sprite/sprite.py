
import pygame, math
from .methods import Methods
from .tooltip import Tooltip
from .corners import Corners
from .rotator import Rotator
from ..core.paths import defaults
from ..core.locals import Image

class __Sprite(Methods):
    """Class primarily for typehinting object/class attributes to improve code completion"""

    font: pygame.font.Font = None
    tooltip: Tooltip = None
    corners: Corners = None

class Sprite(__Sprite):
    """Fully functional Sprite class with many automatic initialisations of relevant objects"""

    def __new__(cls, *args, **kwargs):
        """Called before __init__ to force essential object initialisation"""
        instance = super().__new__(cls)
        instance.font = pygame.font.Font(instance.font_name, instance.font_size)
        instance.tooltip = Tooltip(instance, instance.font)
        instance.corners = Corners(instance)
        print(f"Sprite initialised objects for {instance.__class__.__name__}")
        return instance

    def __init__(self):
        """Placeholder method for testing a default Sprite object"""
        self.x = 100
        self.y = 100
        self.w = 100
        self.h = 100
        self.surface = pygame.Surface([self.w, self.h]).convert_alpha()
        self.rectangle = self.surface.get_rect(topleft = [self.x, self.y])

    def draw_tooltip(self, display):
        """Draw sprite tooltip to the display"""
        self.tooltip.draw(display)

    def enqueue_tooltip(self, queue):
        """Enqueue the tooltip to the draw queue"""
        self.tooltip.enqueue(queue)

    def draw_corners(self, display, animating = True):
        """Draw rectangle corners to display, with optional animation"""
        self.corners.draw(display, animating)

    def enqueue_corners(self, queue, animating = True):
        """Enqueue the corners to the draw queue, with optional animation"""
        self.corners.enqueue(queue, animating)

class SpriteLite(__Sprite):
    """A lightweight Sprite class with only a few automatic initialisations of important objects"""

    def __new__(cls, *args, **kwargs):
        """Called before __init__ to force essential object initialisation"""
        instance = super().__new__(cls)
        instance.font = pygame.font.Font(instance.font_name, instance.font_size)
        print(f"SpriteLite initialised objects for {instance.__class__.__name__}")
        return instance
    
    def __init__(self):
        """Placeholder method for testing a default SpriteLite object"""
        self.x = 100
        self.y = 100
        self.w = 100
        self.h = 100
        self.surface = pygame.Surface([self.w, self.h]).convert_alpha()
        self.rectangle = self.surface.get_rect(topleft = [self.x, self.y])

class SpriteRotating(__Sprite):

    degrees: int = 0
    rotator: Rotator = None

    def __new__(cls, *args, **kwargs):
        """Called before __init__ to force essential object initialisation"""
        instance = super().__new__(cls)
        instance.font: pygame.font.Font = pygame.font.Font(instance.font_name, instance.font_size)
        instance.rotator: Rotator = Rotator(instance)
        print(f"SpriteRotating.__new__ initialised objects for {instance.__class__.__name__}")
        return instance
    
    def __init__(self):
        """Placeholder method for testing a default SpriteRotating object"""
        self.surface = Image(defaults['scroll'])
        self.rectangle = self.surface.get_rect()

class __SpriteRotating:

    def update_rotation(self):
        """Get surface, rectangle and mask for rotated Sprite"""
        self.rot_surf = pygame.transform.rotate(self.surface, self.angle)
        self.rot_rect = self.rot_surf.get_rect(center = self.rectangle.center)
        self.rot_mask = pygame.mask.from_surface(self.rot_surf)

    def update_rotation_alt(self):
        """Rotozoom is suggested as a better alternative for custom images"""
        self.rot_surf = pygame.transform.rotozoom(self.surface, self.angle, 1)
        self.rot_rect = self.rot_surf.get_rect(center = self.rectangle.center)
        self.rot_mask = pygame.mask.from_surface(self.rot_surf)

    def draw_rotated_surface(self, display):
        """Draw rotated surface centered about original rectangle"""
        display.blit(self.rot_surf, self.rot_rect)
    
    def draw_rotated_rectangle(self, display, weight = 2, colour = [255,128,0]):
        """Draw the rotated rectangle inside surface, without inflation"""
        pygame.draw.rect(display, colour, self.rot_rect, weight)

    def draw_rotated_mask(self, display, fill = False):
        """Draw the image mask to the display as outline or filled rect"""
        weight = 0 if fill else 2
        outline_points = self.rot_mask.outline()
        surface = self.rot_surf.copy()
        surface.fill([0,0,0,0])
        pygame.draw.polygon(surface, (200,0,150), outline_points, weight)
        display.blit(surface, self.rot_rect)

    def angle_to_position(self, position, offset = 0):
        """Use math module to calculate angle from center to position"""
        origin = self.rectangle.center
        ox, oy = origin
        px, py = position
        dx = px - ox
        dy = py - oy
        radians = math.atan2(-dy, dx)
        radians %= 2 * math.pi
        degrees = math.degrees(radians)
        return degrees - offset

    def ___rotate_about_position(self, position, radians):
        # Postit - Unfinished
        """Rotate about position and maintain line length"""
        origin = self.rectangle.center
        end = position
        distance = math.dist(origin, end)
        ox, oy = origin
        ex, ey = end
        dx = ex - ox
        dy = ey - oy
        angle = math.atan2(dy, dx) + math.radians(radians)
        ex = ox + distance * math.cos(angle)
        ey = oy + distance * math.sin(angle)
        print(ex, ey)
        # self.angle = math.degrees(angle)
        # self.rectangle.center = ex, ey

    def face_mouse(self):
        """Set angle of Sprite to face the mouse from midtop node"""
        self.angle = self.angle_to_position(self.mouse_position, offset = 90)
        self.update_rotation()

    def face_center(self):
        """Set angle of Sprite to face the display center from midtop node"""
        W, H = pygame.display.get_window_size()
        self.angle = self.angle_to_position([W //2, H // 2], offset = 90)
        self.update_rotation()

    def rotate_clockwise(self, degrees = 90, round_to_degree = None):
        """Rotate surface clockwise and round number to a number of degrees"""
        self.angle -= degrees
        if round_to_degree is not None:
            self.angle = (self.angle // round_to_degree) * round_to_degree
        self.update_rotation()

    def move_toward_angle(self, multiplier = 1):
        """Get current direction using angle from top of Sprite and move toward or away along that angle line depending on """
        radians = math.radians(self.angle - 180)
        direction = pygame.Vector2(math.sin(radians), math.cos(radians))
        self.x += direction[0] * self.velocity * multiplier
        self.y += direction[1] * self.velocity * multiplier
        self.rot_rect.center = self.rectangle.center = self.x, self.y

    def move_relative_to_angle(self, multiplier = 1, key = 'horizontal'):
        """Get current direction using angle from top of Sprite and move relative to angle"""
        if key == 'horizontal': offset = - 90
        elif key == 'vertical': offset = 180
        radians = math.radians(self.angle - offset)
        direction = pygame.Vector2(math.sin(radians), math.cos(radians))
        self.x += direction[0] * self.velocity * multiplier
        self.y += direction[1] * self.velocity * multiplier
        self.rot_rect.center = self.rectangle.center = self.x, self.y
    
    def update(self):
        """Update and handle held keys"""
        keys = pygame.key.get_pressed()
        buttons = pygame.mouse.get_pressed()
        if keys[pygame.K_UP]: self.move_toward_angle(1)
        elif keys[pygame.K_DOWN]: self.move_toward_angle(-1)
        if keys[pygame.K_LEFT] or keys[pygame.K_q]: 
            self.rotate_clockwise(-5)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_e]: 
            self.rotate_clockwise(5)
        if keys[pygame.K_w]: self.move_relative_to_angle(1, 'vertical')
        elif keys[pygame.K_s]: self.move_relative_to_angle(-1, 'vertical')
        if keys[pygame.K_d]: self.move_relative_to_angle(1, 'horizontal')
        elif keys[pygame.K_a]: self.move_relative_to_angle(-1, 'horizontal')
        if keys[pygame.K_SPACE]:
            self.face_center()
            self.move_relative_to_angle(-1, 'horizontal')
        elif buttons[0]:
            self.face_mouse()
            self.move_relative_to_angle(-1, 'horizontal')

        # ~ Limit to Window
        W, H = pygame.display.get_window_size()
        if self.rectangle.centerx < 0:
            self.rectangle.centerx = self.rot_rect.centerx = self.x = 0
        elif self.rectangle.centerx > W:
            self.rectangle.centerx = self.rot_rect.centerx = self.x = W
        if self.rectangle.centery < 0:
            self.rectangle.centery = self.rot_rect.centery = self.y = 0
        elif self.rectangle.centery > H:
            self.rectangle.centery = self.rot_rect.centery = self.y = H

    def draw(self, display):
        """Draw current surface at current rectangle"""
        self.draw_line_from_center(display)
        if self.angle != 0:
            display.blit(self.rot_surf, self.rot_rect)
            self.draw_rotated_mask(display)
            self.draw_mask(display)
            self.draw_rectangle(display, colour = [0,128,0])
            self.draw_rotated_rectangle(display)
        else:
            display.blit(self.surface, self.rectangle)

if __name__ != "__main__":
    print("""
-------------------------------------
mygame.sprite.py imported successfully
-------------------------------------
    Package: mygame
    Name: sprite.py
    Important Classes: Sprite, SpriteLite
    Classes from Other Modules: SpriteTools
    Purpose: Parent classes for visual objects
""")
     