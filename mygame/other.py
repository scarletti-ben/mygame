
import pygame
from typing import Generator
import datetime

def align_rectangles_x(rectangles, y, overlap = 0.2):
    """Align overlapping rectangles centered about CX, with a fixed y"""
    if not rectangles:
        return
    W = pygame.display.get_window_size()[0]
    width = rectangles[0].width
    overlap = overlap * width
    quantity = len(rectangles)
    total_w = quantity * width - (quantity - 1) * overlap
    start_x = (W - total_w) / 2
    for n, rectangle in enumerate(rectangles):
        rectangle.bottomleft = start_x + n * (width - overlap), y

def collide_mask_surface(surface, rectangle, position):
    """Check if position collides with a non alpha pixel in the created mask"""
    x, y = position
    relative_position = x - rectangle.x, y - rectangle.y
    mask = pygame.mask.from_surface(surface)
    try:
        pixel_colour = mask.get_at(relative_position)
        collides = True if pixel_colour == True else False
        return collides
    except IndexError:
        return False

def collide_mask_sprite(sprite, position):
    """Check if position collides with a non alpha pixel in the sprite mask"""
    x, y = position
    relative_position = x - sprite.rectangle.x, y - sprite.rectangle.y
    try:
        pixel_colour = sprite.mask.get_at(relative_position)
        collides = True if pixel_colour == True else False
        return collides
    except IndexError:
        return False
    
def clamp_to_display_ip(rectangle: pygame.Rect) -> None:
    """Clamp a rectangle to the display so it does not go off screen, done in place"""
    display_rectangle = pygame.display.get_surface().get_rect()
    rectangle.clamp_ip(display_rectangle)

def clamp_to_display(rectangle: pygame.Rect) -> pygame.Rect:
    """Clamp a rectangle to the display so it does not go off screen, returns rectangle"""
    display_rectangle = pygame.display.get_surface().get_rect()
    return rectangle.clamp(display_rectangle)

def generator_run_every_n_calls(function, n = 60) -> Generator:
    """Returns a generator object that can be iterated with next(generator) to run a function every n ticks"""
    count = 0
    while True:
        count += 1
        if count % n == 2:
            function()
        yield

class Animation:
    """
    ```python

    # Generator style object to run function at delta time intervals, a number of times

    # ~ Create an animation to run 'func' every 3 seconds, 3 times
    animation = Animation(func, FPS * 3, 3)
    animations.append(animation)

    # ~ Update all animations every frame and remove those that have ended
    for animation in animations[:]:
        if animation.active:
            animation.update()
        else:
            animations.remove(animation)
    ```
    """

    # framerate: int = FPS
    
    def __init__(self, func, yield_interval: int, yield_count_max: int) -> None:
        """Create an animation object"""
        self.func: function = func
        self.yield_interval: int = yield_interval
        self.yield_count_max: int = yield_count_max
        self.yield_count: int = 0
        self.previous_time: int = 0
        self.active: bool = True

    def update(self) -> None:
        """Update every frame and run the function each time the interval is reached, until yield count max is met"""
        if self.yield_count >= self.yield_count_max:
            self.active = False
            return
        current_time = pygame.time.get_ticks()
        dt = current_time - self.previous_time
        # print(f'Delta Time: {dt}')
        if dt >= self.yield_interval:
            self.func()
            self.previous_time = current_time
            self.yield_count += 1
    
    # def add_animation(animation: Animation):
    # """Add animation if it does not already exist"""
    # if not any(type(animation) == type(item) for item in animations):
    #     animations.append(animation)
    #     print('Animation added')
    # else:
    #     print('Animation already in queue')

def draw_framerate(display, clock, font, foreground = [0,255,0], background = [0,0,0,64], node = 'topleft'):
    """Blit high contrast framerate on translucent surface in topright of the display, draw fps"""
    text = f'{int(clock.get_fps())} FPS'
    text_surface = font.render(text, True, foreground)
    surface = text_surface.copy()
    surface.fill(background)
    surface.blit(text_surface, [0,0])
    text_rectangle = text_surface.get_rect()
    position = getattr(display.get_rect(), node)
    setattr(text_rectangle, node, position)
    display.blit(surface, text_rectangle)
                 
def draw_system_time(display, font, foreground = [0,255,0], background = [0,0,0,64]):
    """Show the current system time on the screen in HH:MM:SS in the bottomright of the display"""
    now = datetime.datetime.now()
    current_time = now.strftime('%H:%M:%S')
    text_string = f'{current_time}'
    text_surface = font.render(text_string, True, foreground)
    surface = text_surface.copy()
    surface.fill(background)
    surface.blit(text_surface, [0,0])
    rectangle = surface.get_rect(bottomright = pygame.display.get_window_size())
    display.blit(surface, rectangle)

class Timer:
    """Timer in seconds"""
    framerate = 60

    def __init__(self, seconds):
        """Initialise a timer object and calculate duration"""
        self.seconds = seconds
        self.duration = self.framerate * seconds

    def begin(self):
        """Initialise object with initial and final ticks"""
        self.initial = pygame.time.get_ticks()
        self.final = self.initial + self.duration

    def check(self):
        """Check if the timer has ended"""
        current = pygame.time.get_ticks()
        if current > self.final:
            return True
        
def render_cropped_text(font: pygame.font.Font, text: str, colour: list = [255,255,255], aa: bool = True) -> pygame.Surface:
    """Crops text render to remove transparent space, removes ascent, descent, left bearing and right bearing from font rendering"""
    surface = font.render(str(text), aa, colour)
    mask = pygame.mask.from_surface(surface)
    bounding_rects = mask.get_bounding_rects()
    left = min(rectangle.left for rectangle in bounding_rects)
    top = min(rectangle.y for rectangle in bounding_rects)
    right = max(rectangle.right for rectangle in bounding_rects)
    bottom = max(rectangle.bottom for rectangle in bounding_rects)
    w = right - left
    h = bottom - top
    rectangle = pygame.Rect(left, top, w, h)
    subsurface = surface.subsurface(rectangle)
    return subsurface


# Postit - To Check
# def get_circle_points(r):
#     """Return a set of points around a center to blit outline font"""
#     points = []
#     x, y, e = r, 0, 1 - r
#     while x >= y:
#         points.append((x, y))
#         y += 1
#         if e < 0:
#             e += 2 * y - 1
#         else:
#             x -= 1
#             e += 2 * (y - x) - 1
#     points += [(y, x) for x, y in points if x > y]
#     points += [(-x, y) for x, y in points if x]
#     points += [(x, -y) for x, y in points if y]
#     points.sort()
#     return points

# def rect_between(point_1, point_2):
#     """Get the rectangle between two points"""
#     x_1, y_1 = point_1
#     x_2, y_2 = point_2
#     width, height = abs(x_1 - x_2), abs(y_1 - y_2)
#     top, left = min(y_1, y_2), min(x_1, x_2)
#     rectangle = pygame.Rect(left, top, width, height)
#     return rectangle

# def crop_surface(surface) -> pygame.Surface:
#     """Crop or trim an image or surface to remove transparent alpha space"""
#     mask = pygame.mask.from_surface(surface)
#     bounding_rects = mask.get_bounding_rects()
#     left = min(rectangle.left for rectangle in bounding_rects)
#     top = min(rectangle.y for rectangle in bounding_rects)
#     right = max(rectangle.right for rectangle in bounding_rects)
#     bottom = max(rectangle.bottom for rectangle in bounding_rects)
#     w = right - left
#     h = bottom - top
#     rectangle = pygame.Rect(left, top, w, h)
#     subsurface = surface.subsurface(rectangle)
#     return subsurface  

# def get_width_fitting_strings(text, width, font, margin = 0):
#     """Return a list of strings that each fit across the width of a surface"""

#     right = width - margin
#     lines = []
#     words = text.split()

#     def process(line):
#         """Add line and remove end spaces"""
#         if len(line) > 0 and line[-1] == ' ':
#             line = line[:-1]
#         lines.append(line)

#     x = margin
#     line = ''
#     for word in words:
#         long = word + ' '
#         word_w = font.size(word)[0]
#         long_w = font.size(long)[0]
#         print(x)
#         if x + word_w > right:
#             process(line)
#             x = margin
#             line = ''
        
#         line += long
#         x += long_w
#     process(line)
#     return lines