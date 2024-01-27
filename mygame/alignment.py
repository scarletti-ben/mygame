
import pygame

# ~ ======================================================================
# - Alignment functions
# ~ ======================================================================

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

def align_sprites_x(sprites, y, overlap = 0.2):
    """Align sprites horizontally with overlap about CX and a given y"""
    W = pygame.display.get_window_size()[0]
    width = sprites[0].rectangle.width
    overlap = overlap * width
    quantity = len(sprites)
    total_w = quantity * width - (quantity - 1) * overlap
    start_x = (W - total_w) / 2
    for n, sprite in enumerate(sprites):
        sprite.rectangle.bottomleft = start_x + n * (width - overlap), y

def align_rectangles_to_grid_with_height_spacing(rectangles, columns, height_spacing = 16):
    """Align equal sized rectangles to display in a grid with calclated width spacing"""
    if not rectangles:
        return
    display_rectangle = pygame.display.get_surface().get_rect()
    dw, dh = display_rectangle.size
    rw, rh = rectangles[0].size

    # Calculate the width spacing based on the number of columns and the width of rectangles
    width_spacing = (dw - (columns * rw)) / (columns + 1)

    # Initialize variables to keep track of the current position
    x = width_spacing
    y = height_spacing

    # Loop through the rectangles and update their positions to align them in a grid
    for rectangle in rectangles:

        # Set the position of the rectangle
        rectangle.topleft = (x, y)

        # Update the x-coordinate for the next rectangle
        x += rw + width_spacing

        # If we've reached the end of a row, reset x and update y
        if x + rw > dw:
            x = width_spacing
            y += rh + height_spacing

def align_rectangles_to_grid_with_rows(rectangles, columns, rows):
    """Align equal-sized rectangles to display in a grid with calculated width and height spacing"""
    if not rectangles:
        return

    # Get the size of the display surface
    display_rectangle = pygame.display.get_surface().get_rect()
    dw, dh = display_rectangle.size

    rw, rh = rectangles[0].size

    # Calculate the width and height spacing based on the number of columns and rows
    width_spacing = (dw - (columns * rw)) / (columns + 1)
    height_spacing = (dh - (rows * rh)) / (rows + 1)

    # Initialize variables to keep track of the current position
    x = width_spacing
    y = height_spacing

    # Loop through the rectangles and update their positions to align them in a grid
    for rectangle in rectangles:

        # Set the position of the rectangle
        rectangle.topleft = (x, y)

        # Update the x-coordinate for the next rectangle
        x += rw + width_spacing

        # If we've reached the end of a row, reset x and update y
        if x + rw > dw:
            x = width_spacing
            y += rh + height_spacing

# ~ ======================================================================
# - Alignment methods for classes
# ~ ======================================================================

class methods:
    def align_traits(self, items_per_row = 8, y_offset = 12, x_spacing = 0):
        """Align the rectangles of each trait sprite in a grid"""
        if not self.traits:
            return
        size = self.traits[0].rectangle.w
        start_x, start_y = self.rectangle.bottomleft
        index = 0
        quantity = len(self.traits)
        rows = 1 + (quantity - 1) // items_per_row
        for row in range(rows):
            start_y += y_offset
            for n in range(items_per_row):
                x = n * (size + x_spacing) + start_x
                y = row * size + start_y
                trait = self.traits[index]
                trait.rectangle.topleft = x, y
                index += 1
                if index > len(self.traits) - 1:
                    break
            else:
                continue
            break

    def align_relics(self, x_offset = 8, y_offset = 8, spacing = 0):
        """Align relics along the top of the display"""
        x, y = x_offset, y_offset
        for relic in self.relics:
            relic.rectangle.topleft = x, y
            x += relic.rectangle.w + spacing

    def align_potions(self, x_offset = 8, y_offset = 8, spacing = 0):
        """Align potions from the top right of the display"""
        w, h = pygame.display.get_surface().get_size()
        x, y = w - x_offset, 0 + y_offset
        for potion in self.potions:
            potion.rectangle.topright = x, y
            x -= (potion.rectangle.w + spacing)

    def align_healthbar(self, y_offset = - 16):
        """Align the entity healthbar rectangle about the entity"""
        position = self.rectangle.move(0, y_offset).midtop
        self.healthbar.rectangle.midbottom = position

    def align_intention(self, y_offset = - 16):
        """Align the entity intent rectangle above the entity healthbar"""
        bounding = self.healthbar.bounding_rectangle
        rectangle = self.healthbar.rectangle
        mx = rectangle.centerx
        by = bounding.top + y_offset
        self.intention.rectangle.midbottom = mx, by

    def align_all(self):
        """Align associated rectangles with default values"""
        self.align_relics()
        self.align_traits()