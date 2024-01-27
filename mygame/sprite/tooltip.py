
import pygame
from .methods import Methods

class Tooltip(Methods):
    """Tooltip class to draw Sprite/Entity information to display on mouse hover"""
    
    descriptor = 'tooltip'
    font_colour = [255,255,255]
    background_colour = [20, 20, 28]
    outline_colour = [110,53,74]
    default_width = 300
    outline_width = 4
    x_margin = 16
    y_margin = 16
    alpha = 230

    def __init__(self, entity, font, width = None):
        """Create a tooltip  with a given entity and font object"""
        self.entity = entity
        self.font = font
        self.width = self.default_width if width is None else width

    def get_surface(self):
        """Get a surface comprised of rendered lines across a semi-fixed width"""
        
        font = self.font
        font_colour = self.font_colour
        background_colour = self.background_colour
        outline_colour = self.outline_colour
        width = self.width
        x_margin, y_margin = self.x_margin, self.y_margin
        outline_width = self.outline_width
        alpha = self.alpha

        if hasattr(self.entity, 'get_tooltip_lines'):
            lines = self.entity.get_tooltip_lines()
        else:
            lines = [
                'Default Tooltip - hasattr(self.entity, "get_tooltip_lines") is False',
                f'{self.entity}']

        renders = []
        for line in lines:
            words = line.split()
            text = words[0]
            for word in words[1:]:
                proposed_text = text + " " + word
                proposed_width = font.size(proposed_text)[0]
                if proposed_width < width:
                    text = proposed_text
                else:
                    render = font.render(text, True, font_colour)
                    renders.append(render)
                    text = word
            render = font.render(text, True, font_colour)
            renders.append(render)

        total_width = max([render.get_width() for render in renders]) + 2 * x_margin
        total_height = sum([render.get_height() for render in renders]) + 2 * y_margin
        surface = pygame.Surface((total_width, total_height))
        surface.fill(background_colour)

        y = y_margin
        for render in renders:
            x = (total_width - render.get_width()) // 2
            surface.blit(render, (x, y))
            y += render.get_height()

        outline_rectangle = surface.get_rect()
        pygame.draw.rect(surface, outline_colour, outline_rectangle, outline_width)
        surface.set_alpha(alpha)
        return surface

    def draw(self, display: pygame.Surface):
        """Draw tooltip surface and rectangle to the display, ensuring tooltip is clamped and not off screen"""
        display.blit(self.surface, self.rectangle)

    @property
    def surface(self):
        """Get current tooltip surface"""
        return self.get_surface()

    @property
    def rectangle(self):
        """Get current tooltip rectangle at mouse position, ensuring tooltip is clamped and not off screen"""
        mouse = pygame.mouse.get_pos()
        rect = self.surface.get_rect()
        rect.topleft = mouse
        display_rectangle = pygame.display.get_surface().get_rect()
        rect.clamp_ip(display_rectangle)
        return rect

    # @property
    # def rectangle(self):
    #     """Get current tooltip rectangle at mouse position, ensuring tooltip is clamped and not off screen"""
    #     mx, my = pygame.mouse.get_pos()
    #     rect = self.surface.get_rect()
    #     rect.topleft = mx, my
    #     display_rectangle = pygame.display.get_surface().get_rect()

    #     print(rect, display_rectangle)

    #     rect.left = mx
    #     if rect.right > display_rectangle.right:
    #         rect.right = mx

    #     rect.top = my
    #     if rect.bottom > display_rectangle.bottom:
    #         rect.bottom = my

    #     return rect