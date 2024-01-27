
import pygame

class Queue:
    """Draw queue class for sprites, surfaces and rectangles to be drawn in layer order"""

    descriptor_priorities = [
        None,
        'default',
        'intent',
        'trait',
        'relic',
        'entity',
        'sprite',
        'healthbar',
        'card',
        'hovered_card',
        'overlay',
        'button',
        'selection',
        'tooltip',
        'held_card',
        ]
    highlighted_colour = [28,40,148]

    # Postit Queue a group of visuals to be handled together or apart
    
    def __init__(self):
        """Initialise static and dynamic draw queues as lists of visual dictionaries"""
        self.static_visuals: list = []
        self.dynamic_visuals: list = []

    def add(self, surface, rectangle, descriptor = 'default', shadowed = False, **kwargs):
        """Add static surface and rectangle to a dictionary with a descriptor and any keyword arguments"""
        visual = {
            'surface': surface,
            'rectangle': rectangle,
            'descriptor': descriptor,
            'shadowed': shadowed}
        visual.update(kwargs)
        self.static_visuals.append(visual)

    def add_dynamic(self, item, shadowed = False, **kwargs):
        """Add dynamic item to queue, surface and rectangle are updated each frame"""
        visual = {
            'item': item,
            'surface': None,
            'rectangle': None,
            'descriptor': item.descriptor,
            'shadowed': shadowed}
        visual.update(kwargs)
        self.dynamic_visuals.append(visual)

    def populate_static(self):
        """Update all dynamic visuals and add them to the static queue"""
        continuing = []
        for visual in self.dynamic_visuals:
            item = visual['item']
            item.update()
            if not item.finished:
                self.add(item.surface, item.rectangle, item.descriptor)
                continuing.append(visual)
        self.dynamic_visuals = continuing

    def draw_static(self, display):
        """Draw all objects in the static visuals queue"""

        priorities = self.descriptor_priorities
        priority = lambda visual: priorities.index(visual['descriptor'])
        self.static_visuals.sort(key = priority)
        
        show_cursor = True

        for visual in self.static_visuals:

            surface = visual['surface']
            rectangle = visual['rectangle']
            descriptor = visual['descriptor']
            shadowed = visual['shadowed']

            if shadowed:
                shadow = self.get_shadow(surface)
                position = rectangle.move(-4,4)
                display.blit(shadow, position)

            match descriptor:
                case 'tooltip':
                    show_cursor = False
                case 'held_card':
                    show_cursor = False
                case 'healthbar':
                    if rectangle.collidepoint(pygame.mouse.get_pos()):
                        dimmed = self.get_dimmed(surface)
                        display.blit(dimmed, rectangle)
                        continue

            if 'highlighted' in visual:
                highlighted = self.get_highlighted(surface)
                display.blit(highlighted, rectangle)
            elif 'dimmed' in visual:
                dimmed = self.get_dimmed(surface)
                display.blit(dimmed, rectangle)
            else:
                display.blit(surface, rectangle)

            if getattr(visual, 'outlined', False):
                pygame.draw.rect(display, [0,128,128], rectangle, 2)


        if show_cursor == False:
            pygame.mouse.set_visible(False)
        elif not pygame.mouse.get_visible():
            pygame.mouse.set_visible(True)

        self.static_visuals.clear()

    def draw(self, display):
        """Draw all visuals from the queue to the display, sorted by descriptor"""
        self.populate_static()
        self.draw_static(display)

    def rect(self, rectangle, colour = [128,0,128], width = 3):
        """Queue a rectangle to be drawn to the display as a surface"""
        surface = pygame.Surface(rectangle.size, pygame.SRCALPHA)
        canvas_rectangle = surface.get_rect()
        pygame.draw.rect(surface, colour, canvas_rectangle, width)
        self.add(surface, rectangle)

    def debug(self, display, clearing = True):
        """Debug visuals by only drawing outline rectangles and tooltips"""

        priorities = self.descriptor_priorities
        priority = lambda visual: priorities.index(visual['descriptor'])
        self.visuals.sort(key = priority)
        
        show_cursor = True

        for visual in self.visuals:

            surface = visual['surface']
            rectangle = visual['rectangle']
            descriptor = visual['descriptor']

            if descriptor == 'tooltip':
                display.blit(surface, rectangle)
            else:
                pygame.draw.rect(display, [0,255,0], rectangle, 2)

        if show_cursor == False:
            pygame.mouse.set_visible(False)
        elif not pygame.mouse.get_visible():
            pygame.mouse.set_visible(True)

        if clearing:
            self.visuals.clear()

    def get_shadow(self, surface, colour = [40,40,40]):
        """Get the shadow of a given surface using pygame mask"""
        colour = [1,1,1] if colour in [[0,0,0], [0,0,0,0]] else colour
        mask = pygame.mask.from_surface(surface)
        shadow = mask.to_surface()
        shadow.set_colorkey((0,0,0))
        shadow.fill(colour, special_flags = pygame.BLEND_RGBA_MIN)
        return shadow
    
    def get_highlighted(self, surface):
        """Convert a surface to a version with a colour tint"""
        colour = self.highlighted_colour
        highlighted = surface.copy()
        highlighted.fill(colour, special_flags = pygame.BLEND_RGB_MAX)
        return highlighted

    def get_dimmed(self, surface, percentage = 50):
        """Get current surface with a colour tint"""
        alpha = int((100 - percentage) / 100 * 255)
        colour = [255, 255, 255, alpha]
        dimmed = surface.copy()
        dimmed.fill(colour, special_flags = pygame.BLEND_RGBA_MULT)
        return dimmed