
import pygame
from ..core.locals import Image
from ..sprite.sprite import Sprite

# ~ HealthbarB01
class Healthbar(Sprite):
    descriptor = 'healthbar'
    paths = {
        'end_cap_left': r"G:\Coding\assets_new\end_cap_left.png",
        'end_cap_right': r"G:\Coding\assets_new\end_cap_right.png",
        'center_filled': r"G:\Coding\assets_new\center_filled.png",
        'center_empty': r"G:\Coding\assets_new\center_empty.png",
        'block_plate': r"G:\Coding\assets_new\block_number_plate.png",
        'end_cap_left_block': r"G:\Coding\assets_new\end_cap_left_block.png",
        'end_cap_right_block': r"G:\Coding\assets_new\end_cap_right_block.png",
        'center_filled_block': r"G:\Coding\assets_new\center_filled_block.png",
        'center_empty_block': r"G:\Coding\assets_new\center_empty_block.png",
        }
    scale = 8
    shadowed = False
    highlighted_colour = [0,40,140]

    def __init__(self, entity, font, scale = None):
        """Create simple healthbar"""
        self.entity = entity
        self.font = font
        self.scale = scale if scale is not None else self.scale

        self.end_cap_left = Image(self.paths['end_cap_left'], self.scale)
        self.end_cap_right = Image(self.paths['end_cap_right'], self.scale)
        self.center_empty = Image(self.paths['center_empty'], self.scale)
        self.center_filled = Image(self.paths['center_filled'], self.scale)
        self.end_cap_left_block = Image(self.paths['end_cap_left_block'], self.scale)
        self.end_cap_right_block = Image(self.paths['end_cap_right_block'], self.scale)
        self.center_empty_block = Image(self.paths['center_empty_block'], self.scale)
        self.center_filled_block = Image(self.paths['center_filled_block'], self.scale)
        self.block_plate = Image(self.paths['block_plate'], self.scale)

        self.left_width = self.end_cap_left.get_width()
        self.center_width = self.center_filled.get_width()
        self.right_width = self.end_cap_right.get_width()
        self.width = self.left_width + self.center_width + self.right_width
        self.height = self.end_cap_left.get_height()

        self.base = self.get_base()
        self.base_block = self.get_base_block()
        self.update()
        self.rectangle = self.surface.get_rect()

    def get_base(self):
        """Attach left, center and end surfaces together to form base surface"""
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        surface.blit(self.end_cap_left, (0, 0))
        surface.blit(self.center_empty, (self.left_width, 0))
        surface.blit(self.end_cap_right, (self.width - self.right_width, 0))
        return surface

    def get_base_block(self):
        """Attach left, center and end surfaces together to form base surface"""
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        surface.blit(self.end_cap_left_block, (0, 0))
        surface.blit(self.center_empty_block, (self.left_width, 0))
        surface.blit(
            self.end_cap_right_block, (self.width - self.right_width, 0))
        return surface
    
    def get_textbox(self, colour = [0,255,0]):
        """Get HP textbox to be displayed above the healthbar"""
        text = f'HP: {self.entity.hp}/{self.entity.hp_max}'
        textbox = self.font.render(text, True, colour)
        return textbox
    
    @property
    def decimal(self):
        """Get decimal as a ratio of entity current hp and max hp"""
        return self.entity.hp / self.entity.hp_max
    
    def get_subsurface(self):
        """Get the subsurface from current decimal value and center width"""
        width = self.decimal * self.center_width
        if self.entity.hp > 0:
            width = max(width, 1)
        rectangle = [0, 0, width, self.height]
        return self.center_filled.subsurface(rectangle)
    
    def update(self):
        """Blit the subsurface on the base surface offset by end cap width"""
        if self.entity.block > 0:
            self.surface = self.base_block.copy()
        else:
            self.surface = self.base.copy()
        subsurface = self.get_subsurface()
        self.surface.blit(subsurface, [self.left_width, 0])

    def get_visuals(self, update = True):
        """Draw current surface above entity"""

        visuals = []
        rectangles = []

        if update:
            self.update()

        y_offset = -16

        visuals.append([self.surface, self.rectangle, self.descriptor])

        px, py = self.rectangle.move(0, y_offset).midtop

        textbox = self.get_textbox()
        rectangle = textbox.get_rect(midbottom = [px, py])
        visuals.append([textbox, rectangle, self.descriptor])
        self.text_rectangle = rectangle

        plate = self.block_plate.copy()
        plate_rect = plate.get_rect(topleft = self.rectangle.topright)
        block = self.font.render(str(self.entity.block), True, [255,255,255])
        shadow = self.font.render(str(self.entity.block), True, [0,0,0])
        center = plate.get_rect().center
        shadow_center = center[0] - 2, center[1] + 2
        block_rect = block.get_rect(center = center)
        shadow_rect = shadow.get_rect(center = shadow_center)
        block_rect.y -= 2
        shadow_rect.y -= 2
        plate.blit(shadow, shadow_rect)
        plate.blit(block, block_rect)
        
        if self.entity.block > 0:
            visuals.append([plate, plate_rect, self.descriptor])

        self.visuals = visuals

        self.rectangles = [visual[1] for visual in visuals]

        return visuals
    
    def enqueue(self, queue):
        """Add current surface, rectangle and descriptor to the draw queue"""
        visuals = self.get_visuals()
        for surface, rectangle, descriptor in visuals:
            queue.add(surface, rectangle, descriptor, shadowed = self.shadowed)

    def draw(self, display):
        """Draw current surface at current rectangle"""
        visuals = self.get_visuals()
        for surface, rectangle, descriptor in visuals:
            display.blit(surface, rectangle)