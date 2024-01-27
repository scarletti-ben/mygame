
# ~ Imports
import pygame, math
from ..core.constants import USER_EVENT
from typing import List
from ..core import tools
from .. import mouse

# ~ Sprite Methods Class with Sprite Methods
class Methods:
    surface: pygame.Surface = NotImplemented
    image: pygame.Surface = NotImplemented
    mask: pygame.mask = NotImplemented
    rectangle: pygame.Rect = NotImplemented
    rectangles: List[pygame.Rect] = NotImplemented
    collision_rectangle: pygame.Rect = NotImplemented
    index: int = 0
    layer: int = 0
    descriptor: str = 'sprite'
    alpha: int = 255
    scale: int = 1
    outlined: bool = False
    antialias: bool = True
    bold: bool = False
    italic: bool = False
    font_name: str = "G:/Coding/Assets/Fonts/Monogram/monogram-extended.ttf"
    font_size: int = 24
    font_colour: list = [0,255,0]
    outline_colour: list = [255,128,0]
    outline_weight: int = 2
    line_weight: int = 2
    line_colour: list = [255,128,0]
    highlighted_colour: list = [0,40,140]
    shadow_colour: list = [40,40,40]
    shadowed: bool = False
    angle: float = 0.0
    # rotated_surface: pygame.Surface = NotImplemented
    # rotated_mask: pygame.mask.Mask = NotImplemented
    # rotated_rectangle: pygame.Rect = NotImplemented
    active: bool = True
    # rotating: bool = False
    debugging: bool = False
    velocity: float = 0.0
    description: str = 'default_description'
    name: str = 'default_name'
    x: int = 0
    y: int = 0
    w: int = 0
    h: int = 0
    font: pygame.font.Font = None

    node: str = 'topleft'
    position: list = NotImplemented

# ~ ======================================================================
# - New Methods in Testing
# ~ ======================================================================

    # * ======================================================================
    # * Bounding Rectangles
    # * ======================================================================

    # * Information:
        # - Sprites usually have a surface and a rectangle
        # - A handful of sprites have multiple elements, such as a healthbar
            # - Healthbar, block indicator if needed, text above bar etc.
        # - For sprites with multiple elements it is good to be able to check their bounding rectangle
            # - Each sprite element is added as a rectangle to self.rectangles
            # - The bounding rectangle is found from these rectangles

    def get_bounding_rectangle(self):
        """If this sprite has multiple rectangles, get the rectangle that encompasses all of them, otherwise return self.rectangle"""
        if self.rectangles:
            bounding_rectangle = tools.get_bounding_rectangle(self.rectangles)
            return bounding_rectangle
        else:
            return self.rectangle
    
    @property
    def bounding_rectangle(self):
        """Property to return the current bounding rectangle"""
        return self.get_bounding_rectangle()
    
    # * ======================================================================
    # * Methods and Properties to check Mouse status
    # * ======================================================================

    @property
    def held(self):
        """Check if the item currently held by the mouse is this sprite"""
        return mouse.get_held() is self
    
    def is_held(self):
        """Check if the item currently held by the mouse is this sprite"""
        return mouse.get_held() is self
    
    @property
    def hovered(self):
        """Check if the item currently hovered by the mouse is this sprite"""
        return mouse.get_hovered() is self
    
    def is_hovered(self):
        """Check if the item currently held by the mouse is this sprite"""
        return mouse.get_held() is self

# ~ ======================================================================
# - Placeholder __init__ to advise user to definine child __init__ method
# ~ ======================================================================

    def __init__(self, *args, **kwargs):
        """SpriteTools __init__ method to advise user to definine child __init__ method"""
        raise UserWarning(f'SpriteTools.__init__ called for {self.__class__.__name__}, child objects should have their own __init__') 

# ~ ======================================================================
# - Other Magic Methods
# ~ ======================================================================

    def __repr__(self):
        """Default representation of Sprite objects"""
        return self.__class__.__name__.title()

# ~ ======================================================================
# - Methods for drawing to display - Part I
# ~ ======================================================================

    def enqueue(self, queue, *args, **kwargs):
        """Add current surface and rectangle to the queue"""
        queue.add(self.surface, self.rectangle, self.descriptor, **kwargs)

    queue = enqueue

    def draw(self, display, *args, **kwargs):
        """Draw sprite surface at current sprite rectangle position"""
        display.blit(self.surface, self.rectangle)

    render = draw

# ~ ======================================================================
# - Methods for adding to draw queue - Part II
# ~ ======================================================================

    def enqueue_highlighted(self, queue, colour = None):
        """Blit the sprite surface with colour tint"""
        surface = self.get_highlighted_surface(colour)
        queue.add(surface, self.rectangle)

    def enqueue_rectangle(self, queue, colour = [0,255,0]):
        """Add rectangle to the queue to be drawn as a surface"""
        queue.rect(self.rectangle, colour)

# ~ ======================================================================
# - Methods for drawing to display - Part II
# ~ ======================================================================

    def draw_highlighted(self, display, colour = None):
        """Blit the sprite surface with colour tint"""
        surface = self.get_highlighted_surface(colour)
        display.blit(surface, self.rectangle)

    def draw_dimmed(self, display, percentage = 50):
        """Blit the sprite surface with dimming effect"""
        surface = self.get_dimmed_surface(percentage)
        display.blit(surface, self.rectangle)

    def draw_rectangle_inside(self, display, weight = None, colour = None):
        """Blit sprite rectangle to display at a position inside the sprite surface"""
        colour = self.outline_colour if colour is None else colour
        weight = self.outline_weight if weight is None else weight
        pygame.draw.rect(display, colour, self.rectangle, weight)

    draw_outline_inside = draw_rectangle_inside
    
    def draw_rectangle_outside(self, display, weight = None, colour = None):
        """Blit sprite rectangle to display at a position outside the sprite surface"""
        colour = self.outline_colour if colour is None else colour
        weight = self.outline_weight if weight is None else weight
        expansion = int(weight / 2)
        outline = self.rectangle.inflate(expansion, expansion)
        pygame.draw.rect(display, colour, outline, weight)

    draw_outline_outside = draw_rectangle_outside

    def draw_rectangle(self, display, weight = None, colour = None, outside = False):
        """Blit sprite rectangle to display at a position inside or outside the sprite surface"""
        if outside:
            self.draw_rectangle_outside(display, weight, colour)
        else:
            self.draw_rectangle_inside(display, weight, colour)

    draw_outline = draw_rectangle

    def draw_rectangle_alpha(self, display, colour = [128,128,128,128]):
        """Blit sprite rectangle to display with optional transparency"""
        surface = pygame.Surface(self.rectangle.size).convert_alpha()
        surface.fill(colour)
        display.blit(surface, self.rectangle)

    def draw_mask(self, display, colour = None, fill = False):
        """Draw the sprite mask to the display as an outline or filled polygon"""
        surface = self.get_mask_as_surface(colour, fill)
        display.blit(surface, self.rectangle)

    def draw_layered_outline(self, display, colours: list, weight = None) -> None:
        """Draw rectangles of decreasing size within the surface area of the sprite rectangle"""
        weight = self.outline_weight if weight is None else weight
        weight = 2 * weight
        for n, colour in reversed(list(enumerate(colours))):
            pygame.draw.rect(display, colour, self.rectangle, weight * (n + 1))

    draw_layered_rectangle = draw_layered_outline

    def draw_positioning_lines(self, display, length = 16, weight = None, colour = None):
        """Draw positioning lines through the center of the sprite rectangle with added length"""
        weight = self.line_weight if weight is None else weight
        colour = self.line_colour if colour is None else colour
        left = self.rectangle.left - length // 2, self.rectangle.centery
        right = self.rectangle.right + length // 2, self.rectangle.centery
        top = self.rectangle.centerx, self.rectangle.top - length // 2
        bottom = self.rectangle.centerx, self.rectangle.bottom + length // 2
        pygame.draw.line(display, colour, left, right, weight)
        pygame.draw.line(display, colour, top, bottom, weight)

    def draw_line_to_mouse(self, display, node = 'center', colour = None, weight = None):
        """Draw a line between a sprite rectangle node and the current mouse position"""
        colour = self.line_colour if colour is None else colour
        weight = self.line_weight if weight is None else weight
        start = getattr(self.rectangle, node)
        end = pygame.mouse.get_pos()
        pygame.draw.line(display, colour, start, end, weight)

    def draw_line_at_angle(self, display, angle, length = 100, node = 'center', colour = None, weight = None):
        """Draw a line of a given length from a sprite rectangle node at a given angle"""
        colour = self.line_colour if colour is None else colour
        weight = self.line_weight if weight is None else weight
        x1, y1 = getattr(self.rectangle, node)
        x2 = x1 + math.sin(math.radians(angle - 180)) * length
        y2 = y1 + math.cos(math.radians(angle - 180)) * length
        pygame.draw.line(display, colour, [x1,y1], [x2,y2], weight)

    def draw_line_at_current_angle(self, display, length, node = 'center', colour = None, weight = None):
        """Draw a line of a given length from a sprite rectangle node at the current sprite angle"""
        self.draw_line_at_angle(display, self.angle, length, node, colour, weight)

# ~ ======================================================================
# - Methods for collision
# ~ ======================================================================

    def collides_mouse(self) -> bool:
        """Check if the sprite rectangle collides with current mouse position"""
        position = pygame.mouse.get_pos()
        return self.rectangle.collidepoint(position)
    
    under_mouse = collides_mouse
    
    def collides(self, position) -> bool:
        """Check if the sprite rectangle collides with a given coordinate"""
        return self.rectangle.collidepoint(position)
    
    collidepoint = collides

    def collides_rectangle(self, rectangle) -> bool:
        """Check if the sprite rectangle collides with a given rectangle"""
        return self.rectangle.colliderect(rectangle)
    
    colliderect = collides_rectangle
        
    def collides_mask(self, position) -> bool:
        """Check if a given position collides with a non-alpha pixel in the entity's mask"""
        x, y = position
        relative_position = x - self.rectangle.x, y - self.rectangle.y
        if not hasattr(self, 'mask') or not isinstance(self.mask, pygame.mask.Mask):
            self.mask = pygame.mask.from_surface(self.surface)
            print('No mask found, mask created.')
        pixel_colour = self.mask.get_at(relative_position)
        collides = True if pixel_colour == True else False
        return collides

    def collides_other_sprite_rectangle(self, sprite) -> bool:
        """Check if this sprite's rectangle collides with another sprite's rectangle"""
        return self.collides_rectangle(sprite.rectangle)
    
    def collides_other_sprite_mask(self, sprite) -> bool:
        """Check if this sprite's mask collides with another sprite's mask"""
        x_offset = sprite.rectangle[0] - self.rectangle[0]
        y_offset = sprite.rectangle[1] - self.rectangle[1]
        self.rect = self.rectangle
        sprite.rect = sprite.rectangle
        collision_points = self.mask.overlap(sprite.mask, (x_offset, y_offset))
        collides = bool(collision_points)
        return collides

# ~ ======================================================================
# - Methods for getting various modified surfaces
# ~ ======================================================================
    
    def get_mask_from_surface(self):
        """Get a pygame mask from current surface"""
        return pygame.mask.from_surface(self.surface)

    def get_mask_as_surface(self, colour = None, fill = False):
        """Get the sprite mask drawn to a surface as an outline or filled polygon"""
        weight = 0 if fill else self.outline_weight
        colour = self.outline_colour if colour is None else colour
        outline_points = self.mask.outline()
        surface = self.get_blank_surface()
        pygame.draw.polygon(surface, colour, outline_points, weight)
        return surface
    
    def get_transparent_surface(self, alpha = None):
        """Get sprite surface with transparency"""
        alpha = self.alpha if alpha is None else alpha
        surface = self.surface.copy()
        surface.set_alpha(alpha)
        return surface
    
    def get_dimmed_surface(self, percentage = 50):
        """Get sprite surface with a dimming effect"""
        alpha = int((100 - percentage) / 100 * 255)
        colour = [255, 255, 255, alpha]
        dimmed = self.surface.copy()
        dimmed.fill(colour, special_flags = pygame.BLEND_RGBA_MULT)
        return dimmed
    
    def get_highlighted_surface(self, colour = None):
        """Get sprite surface with a colour tint"""
        colour = self.highlighted_colour if colour is None else colour
        surface = self.surface.copy()
        surface.fill(colour, special_flags = pygame.BLEND_RGB_MAX)
        return surface
    
    def get_outlined_surface(self, colour = None, weight = None):
        """Get sprite surface with an outline rectangle drawn on"""
        colour = self.outline_colour if colour is None else colour
        weight = self.outline_weight if weight is None else weight
        surface = self.surface.copy()
        rectangle = surface.get_rect()
        pygame.draw.rect(surface, colour, rectangle, weight)
        return surface
    
    def get_blank_surface(self):
        """Get a blank copy of sprite surface"""
        surface = self.surface.copy()
        surface.fill([0,0,0,0])
        return surface
    
# ~ ======================================================================
# - Methods for posting to pygame event queue
# ~ ======================================================================

    def post(self, subtype, **kwargs):
        """Post user event with subtype and any keyword arguments"""
        dictionary = {
            'subtype': subtype}
        dictionary.update(kwargs)
        event = pygame.event.Event(USER_EVENT, dictionary)
        pygame.event.post(event)

    announce = post

    def post_message(self, message, **kwargs):
        """Post message event with a given message"""
        subtype = 'message'
        dictionary = {
            'message': message}
        dictionary.update(kwargs)
        self.post(subtype, **kwargs)

# ~ ======================================================================
# - Placeholder methods for handle and update
# ~ ======================================================================

    def update(self, *args, **kwargs) -> None: ...
    def handle(self, event, **kwargs) -> None: ...

# ~ ======================================================================
# - Methods for detecting events
# ~ ======================================================================

    def clicked(self, event, button = 1):
        """Check if the sprite has been clicked by a given mouse button"""
        result = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == button:
            if self.collides(event.pos):
                result = True
        return result
    
    def released(self, event, button = 1):
        """Check if a given mouse button has been released"""
        return event.type == pygame.MOUSEBUTTONUP and event.button == button
        
# ~ ======================================================================
# - Methods for sprite state
# ~ ======================================================================

    def toggle(self):
        """Set the sprite active or not active"""
        self.active = not self.active

# ~ ======================================================================
# - Methods for sprite movement and rectangle placement
# ~ ======================================================================

    def move_rectangle(self, dx, dy):
        """Move the sprite rectangle by a given change in x and y"""
        self.rectangle.move_ip(dx, dy)    

    def move_coordinates(self, dx, dy, move_rectangle = True):
        """Move the x and y coordinates of the sprite, avoiding quantisation"""
        self.x += dx
        self.y += dy
        if move_rectangle:
            self.rectangle.topleft = self.x, self.y

    def place(self, position, node = 'topleft'):
        """Place the sprite rectangle at a given position, respecting node / corner"""
        setattr(self.rectangle, node, position)

    def place_at_mouse(self, node = 'center'):
        """Place sprite rectangle's node at the current mouse position"""
        position = pygame.mouse.get_pos()
        self.place(position, node)

    def place_at_corner(self, corner = 'bottomright'):
        """Place sprite rectangle in the corner of the display"""
        rectangle = pygame.display.get_surface().get_rect()
        position = getattr(rectangle, corner)
        setattr(self.rectangle, corner, position)
        # self.place(position, corner)

    def clamp(self):
        """Ensure that Sprite rectangle is within the display rectangle area"""
        display_rectangle = pygame.display.get_surface().get_rect()
        self.rectangle.clamp_ip(display_rectangle)

# * ======================================================================
# * Unfinshed Parent classes for Sprite-style objects
# * ======================================================================

# * Class to be subclassed so that sprites can access their internal rectangle
class __AccessRectangleAttributes:
    """
    ```python
    # Used as a parent class so that objects can access their internal rectangle
    class Sprite(AccessRectangleAttributes)
    ```    
    """

    def __getattribute__(self, __name: str):
        """Hijack get attribute to access internal rectangle"""
        rectangle_attributes = [
            'w', 'h', 'width', 'height', 'right',  'bottom',
            'x', 'y', 'left', 'top',
            'center', 'midbottom', 'midtop',  'midright', 'midleft', 'centerx', 'centery',
            'topleft', 'topright', 'bottomleft', 'bottomright',
            'size']
        if __name in rectangle_attributes:
            return getattr(self.rectangle, __name)
        else:
            return super().__getattribute__(__name)

# * Class to be subclassed so that sprites can rotated
class __Rotation:

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

# * Class for other sprite tools
class __OtherTools:
    def __setattr__(self, __name, __value):
        """Post user events corresponding to specific attribute changes"""
        if getattr(self, 'debugging', False):
            if __name == 'debugging':
                suffix = 'enabled' if __value == True else 'disabled'
                self.post_message(f'{self.name} debugging {suffix}')
            elif __name == 'enabled':
                suffix = 'enabled' if __value == True else 'disabled'
                self.post_message(f'{self.name} sprite {suffix}')
            elif __name == 'attached_sprite':
                if __value is not None:
                    self.post_message(f'{self.name} attached to {__value.name}')
        return super().__setattr__(__name, __value)
    
    def draw_corners_ALT(self, display):
        """Draw the corners of surface with centers cut out"""
        surface = self.blank_surface
        rectangle = surface.get_rect()
        pygame.draw.rect(surface, [20,20,20], rectangle, 8)
        pygame.draw.rect(surface, [255,255,255], rectangle, 4)
        surface.fill(0, rectangle.inflate(-40,0))
        surface.fill(0, rectangle.inflate(0,-40))
        display.blit(surface, self.rectangle)

    def draw_corners(self, display, outer_colour = [0,0,0], inner_colour = [255,255,255], weight = 4, scale = 4):
        """Draw outline corners by cutting out the horizontal and vertical centers"""
        surface = pygame.Surface(self.rectangle.size, pygame.SRCALPHA)
        rectangle = surface.get_rect()
        length = min(rectangle.w, rectangle.h) * (scale / 10)
        pygame.draw.rect(surface, outer_colour, rectangle, 2 * weight)
        pygame.draw.rect(surface, inner_colour, rectangle, 1 * weight)
        surface.fill([0,0,0,0], rectangle.inflate(-length, 0))
        surface.fill([0,0,0,0], rectangle.inflate(0, -length))
        display.blit(surface, self.rectangle)

    def draw_corner_surface(self, display, offset = 40, length = 40):
        """Draw shadow corner surface at an offset from the original surface"""
        width, height = self.rectangle.w + offset, self.rectangle.h + offset
        surface = pygame.Surface([width, height], pygame.SRCALPHA)
        rectangle = surface.get_rect()
        pygame.draw.rect(surface, [20,20,20], rectangle, 8)
        pygame.draw.rect(surface, [255,255,255], rectangle, 4)
        surface.fill(0, rectangle.inflate(-length,0))
        surface.fill(0, rectangle.inflate(0,-length))
        rectangle.center = self.rectangle.center
        display.blit(surface, rectangle)

    def get_angle_to_mouse_position(self):
        """Use math module to calculate angle from center to mouse position"""
        mouse_position = pygame.mouse.get_pos()
        return self.get_angle_to_position_in_degrees(mouse_position)
    
    def draw_corners(
        self, 
        display, 
        c1 = [30,30,30], 
        c2 = [255,255,255], 
        w = 4, 
        scale = 4):
        """Draw rectangle/shadow  inside surface then remove centers"""
        surface = self.blank_surface
        rectangle = surface.get_rect()
        length = min(rectangle.w, rectangle.h) * (scale / 10)
        pygame.draw.rect(surface, c1, rectangle, 2 * w)
        pygame.draw.rect(surface, c2, rectangle, 1 * w)
        surface.fill([0,0,0,0], rectangle.inflate(-length, 0))
        surface.fill([0,0,0,0], rectangle.inflate(0, -length))
        display.blit(surface, self.rectangle)