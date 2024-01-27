
# ~ Import List
import pygame, os, sys, random, itertools, numpy
import typing, math, time, datetime, ctypes, string
import mygame

# ~ Initialisation
pygame.init()
ctypes.windll.user32.SetProcessDPIAware()
os.system('cls')
# function prompt {"> "}

# ~ Setup
W = 1280
H = 720
FPS = 60
CENTER = CX, CY = W // 2, H // 2
GREY = [63,63,63]
clock = pygame.time.Clock()
display = pygame.display.set_mode([W,H], pygame.RESIZABLE)
user_event = pygame.USEREVENT + 1
font_name = "G:/Coding/Assets/Fonts/Monogram/monogram.ttf"
font = pygame.font.Font(font_name, 24)

class Rotator:
    """Simple rotator object to give Sprite objects rotation"""

    preference: str = 'rotozoom'
    
    def __init__(self, sprite, degrees = 0, scale = 1):
        """Create a rotator object to handle rotation for its sprite"""
        self.sprite = sprite
        self.degrees = degrees
        self.scale = scale
    
    @property
    def surface(self):
        """Get the rotated version of the sprite surface"""
        if self.degrees != 0:
            if self.preference == 'rotozoom':
                return pygame.transform.rotozoom(self.sprite.surface, self.degrees, self.scale)
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

    def draw(self, display):
        """Draw surface at rectangle on display"""
        display.blit(self.surface, self.rectangle)

class Sprite:
    def __init__(self, image):
        """Create sprite from surface"""
        self.surface = image
        self.rectangle = image.get_rect()

filepath = r"G:\Coding\assets_new\energyBlueVFX.png"
surface = mygame.core.locals.Image(filepath)
sprite = Sprite(surface)
sprite.rectangle.center = CENTER
sprite.rotator = Rotator(sprite)

def get_scale(ticks, fps = FPS):

    min_scale = 0.80
    max_scale = 1.2
    oscillation_period = 4 # In seconds, the time it takes to go from minimum to maximum and back to minimum

    # Calculate the phase of the oscillation
    phase = (2.0 * math.pi * ticks) / (oscillation_period * 1000)  # Convert ticks to seconds

    # Use a sine wave to smoothly oscillate between -1 and 1
    oscillation = math.sin(phase)

    # Map the sine wave output to the desired scale range
    scale = (oscillation + 1.0) * 0.417 + 0.66  # Map [-1, 1] to [0.66, 1.5]
    
    return scale

sprite.rotator.degrees = 1

# ~ Game Loop
while True:

    display.fill(GREY)
    events = pygame.event.get()
    keys = pygame.key.get_pressed()
    buttons = pygame.mouse.get_pressed()
    mouse = mx, my = pygame.mouse.get_pos()


    ticks = pygame.time.get_ticks()
    sprite.rotator.scale = get_scale(ticks)
    # sprite.rotator.degrees += 10 / FPS
    surface = sprite.rotator.surface
    rectangle = sprite.rotator.rectangle

    display.blit(surface, rectangle)

    for event in events:

        if event.type == pygame.QUIT: 
            quit()
        if event.type == pygame.KEYDOWN: ...
        if event.type == pygame.MOUSEBUTTONDOWN: ...
        elif event.type == pygame.MOUSEBUTTONUP: ...

    pygame.display.flip()	
    clock.tick(FPS)

