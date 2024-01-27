
import pygame, math

class Oscillator:
    """Simple oscillator object to give Sprite objects updating rotation and scale"""
    
    def __init__(self, sprite, min_scale = 0.75, max_scale = 1.25, seconds = 2, degrees_per_second = 20):
        """Create an oscillator object to handle rotation and scale for its sprite"""
        self.sprite = sprite
        self.min_scale = min_scale
        self.max_scale = max_scale
        self.seconds = seconds # Time taken to change scale between min_scale and max_scale
        self.degrees_per_second = degrees_per_second
        self.update()

    def update(self):
        """Update current scale and angle in degrees from current ticks"""
        ticks = pygame.time.get_ticks()
        self.scale = self.get_scale(ticks)
        self.degrees = self.get_degrees(ticks)

    @property
    def surface(self):
        """Get the rotated version of the sprite surface"""
        return pygame.transform.rotozoom(self.sprite.surface, self.degrees, self.scale)

    @property
    def rectangle(self):
        """Get current rotated surface centered around the sprite rectangle center"""
        return self.surface.get_rect(center = self.sprite.rectangle.center)    

    @property
    def mask(self):
        """Get mask from the current surface"""
        return pygame.mask.from_surface(self.surface)

    def get_scale(self, ticks):
        """Get current scale of the surface"""
        seconds = ticks / 1000
        phase = (2.0 * math.pi * seconds) / self.seconds
        oscillation = math.sin(phase)
        oscillation += 1 # ~ Move sine wave out of the negative from [-1 to 1] to [0 to 2]
        midpoint = (self.max_scale - self.min_scale) / 2
        scale = oscillation * midpoint + self.min_scale
        return scale
    
    def get_degrees(self, ticks):
        """Get the rotation in degrees based on time (ticks)"""
        seconds = ticks / 1000
        degrees = seconds * self.degrees_per_second
        return degrees
        
    def enqueue(self, queue):
        """Add surface and rectangle to draw queue with current scale and rotation"""
        self.update()
        queue.add(self.surface, self.rectangle, self.sprite.descriptor)

    def draw(self, display):
        """Draw current surface at current rectangle on the display with current scale and rotation"""
        self.update()
        display.blit(self.surface, self.rectangle)


if __name__ == '__main__':

    # ~ Import List
    import pygame, os, sys, random, itertools, numpy
    import typing, math, time, datetime, ctypes, string
    import mygame

    # ~ Initialisation
    pygame.init()
    ctypes.windll.user32.SetProcessDPIAware()
    os.system('cls')

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

    class Sprite:
        def __init__(self, image):
            """Create sprite from surface"""
            self.surface = image
            self.rectangle = image.get_rect()

    filepath = r"G:\Coding\assets_new\energyBlueVFX.png"
    surface = mygame.core.locals.Image(filepath)
    sprite = Sprite(surface)
    sprite.rectangle.center = CENTER
    sprite.oscillator = Oscillator(sprite)

    # ~ Game Loop
    while True:

        display.fill(GREY)
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        buttons = pygame.mouse.get_pressed()
        mouse = mx, my = pygame.mouse.get_pos()
        

        if sprite.rectangle.collidepoint(mouse):
            sprite.oscillator.draw(display)
        else:
            display.blit(sprite.oscillator.surface, sprite.oscillator.rectangle)

        for event in events:

            if event.type == pygame.QUIT: 
                quit()
            if event.type == pygame.KEYDOWN: ...
            if event.type == pygame.MOUSEBUTTONDOWN: ...
            elif event.type == pygame.MOUSEBUTTONUP: ...

        pygame.display.flip()	
        clock.tick(FPS)

