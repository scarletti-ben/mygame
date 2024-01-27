
# ~ General Imports and Initialisation
import pygame, mygame
from mygame.core.locals import *
pygame.init()
mygame.disable_dpi_scaling()
mygame.clear_terminal()

# ~ Object Imports
from mygame.experimental.test_rectangleA01 import TestRectangle
from mygame.mouse import get_held, set_held, get_hovered, set_hovered

# ~ Setup
display = Display(W, H)
clock = Clock()
font = Font()
mygame.set_cursor()
background = Image(defaults['background'], size = [W, H])

# ~ Create Sprites
sprites = []
for _ in range(5):
    s = TestRectangle()
    sprites.append(s)

def align_rectangles_x(rectangles, y, overlap = 0.2):
    """Align overlapping rectangles centered about CX, with a fixed y"""
    W = pygame.display.get_window_size()[0]
    width = rectangles[0].width
    overlap = overlap * width
    quantity = len(rectangles)
    total_w = quantity * width - (quantity - 1) * overlap
    start_x = (W - total_w) / 2
    for n, rectangle in enumerate(rectangles):
        rectangle.bottomleft = start_x + n * (width - overlap), y

class Card:

    filepath: str = defaults['card']
    descriptor: str = 'card'
    flavour: str = 'default'

    def __init__(self, name = 'name', description = 'description'):
        """Default card class"""

        self.name: str = name
        self.description: str = description
        self.surface: pygame.Surface = Image(self.filepath)
        self.rectangle: pygame.Rect = self.surface.get_rect()

def collide_mask(surface, rectangle, position):
    """Check if position collides with a non alpha pixel in the mask"""
    x, y = position
    relative_position = x - rectangle.x, y - rectangle.y
    mask = pygame.mask.from_surface(surface)
    try:
        pixel_colour = mask.get_at(relative_position)
        collides = True if pixel_colour == True else False
        return collides
    except IndexError:
        pass

# ~ Create Sprites
sprites = []
for _ in range(5):
    s = Card()
    sprites.append(s)

hovered_rectangle = None
hovered_surface = None

# ~ Game Loop
while True:

    display.blit(background, [0,0])
    events = pygame.event.get()
    mouse = list(pygame.mouse.get_pos())

    hovered = get_hovered()
    held = get_held()

    rs = [s.rectangle for s in sprites if s is not held]
    align_rectangles_x(rs, H + 50, overlap = 0.4)

    rotozoom = 1.4
    if hovered is not None and not held:
        hovered_surface = hovered.surface.copy()
        hovered_surface = pygame.transform.rotozoom(hovered_surface, 0, rotozoom)
        hovered_rectangle = hovered_surface.get_rect()
        hovered_rectangle.centerx = hovered.rectangle.centerx
        hovered_rectangle.bottom = H
        position = mouse
        if mouse[1] > hovered.rectangle.move(0,-0).top and collide_mask(hovered_surface, hovered_rectangle, position):
            pass
        else:
            set_hovered(None)

    if not held and not hovered:
        for sprite in list(reversed(sprites)):
            if collide_mask(sprite.surface, sprite.rectangle, mouse):
                set_hovered(sprite)
                break
            
    for sprite in sprites:
        surface = sprite.surface
        rectangle = sprite.rectangle.copy()
        if sprite is hovered:
            continue 
        elif sprite is held:
            continue
        display.blit(surface, rectangle)

    if hovered is not None and held is None:
        hovered_surface = hovered.surface.copy()
        hovered_surface = pygame.transform.rotozoom(hovered_surface, 0, rotozoom)
        hovered_rectangle = hovered_surface.get_rect()
        hovered_rectangle.centerx = hovered.rectangle.centerx
        hovered_rectangle.bottom = H
        display.blit(hovered_surface, hovered_rectangle)

    if held is not None:
        rectangle = held.rectangle.copy()
        surface = held.surface
        # surface = pygame.transform.rotozoom(surface, 0, 1.2)
        rectangle.center = mouse
        rectangle.clamp_ip(display.get_rect())
        display.blit(surface, rectangle)

    for event in events:
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if hovered is not None:
                if hovered.rectangle.collidepoint(event.pos):
                    set_held(hovered)
        elif event.type == pygame.MOUSEBUTTONUP:
            set_held(None)
            set_hovered(None)


    pygame.display.flip()
    clock.tick(FPS)
