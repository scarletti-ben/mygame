
import pygame
from ..core.locals import Image
from ..sprite.sprite import SpriteLite

class Card(SpriteLite):
    # Postit 320 x 410 proposed card size

    # scale = 1.5
    # margin = 4 * scale
    # 
    # description_font_size = int(18 * scale) + 2
    # title_font_size = int(28 * scale) + 1
    # description_font = pygame.font.Font(font_name, description_font_size)
    # title_font = pygame.font.Font(font_name, title_font_size)
    # description_font_colour = [255,255,255]
    # title_font_colour = [255,255,255]
    # outline_font_colour = [68,68,68]
    # path = "G:/Coding/Assets/Images/_main_11.png"
    # # path = "G:/Coding/Assets/Images/_main_11 - Copy.png"
    # # path = r"G:\Coding\assets_new\card\test\larger6.png"
    # base_image = pygame.image.load(path).convert_alpha()
    # base_width, base_height = base_image.get_size()
    # width, height = base_width * scale, base_height * scale
    # image = pygame.transform.scale(base_image, [width, height])

    # title_center = [116 * scale, 132 * scale]
    # description_topleft = [24 * scale, 152 * scale]
    # description_bottomright = [204 * scale, 266 * scale]

    # def __init__(self, name, description = 'test', pos = [100,100]):
    #     """Create a simple card"""
    #     self.name = name
    #     self._image = Card.image.copy()
    #     self.width, self.height = self._image.get_size()
    #     self._rect = self._image.get_rect()
    #     self.description = description
    #     self.surface = self.get_surface()
    #     self.rectangle = self.surface.get_rect(center = pos)

    filepath: str = "G:/Coding/Assets/Images/_main_11.png"
    descriptor: str = 'card'
    flavour: str = 'default'

    def __init__(self, name = 'name', description = 'description'):
        """Default card class"""

        self.name: str = name
        self.description: str = description
        self.surface: pygame.Surface = Image(self.filepath)
        self.rectangle: pygame.Rect = self.surface.get_rect()

    def __repr__(self) -> str:
        """Print representation of card"""
        return f'{self.name}: {self.description}'
    
    def enqueue(self, queue):
        """Queue Card surface and rectangle to draw queue"""
        queue.add(self.surface, self.rectangle, self.descriptor, shadowed = True)

    # def get_surface(self, x_correct = 2, y_correct = 0):
    #     """Return"""
    #     image = self._image.copy()
    #     text = self.description
    #     text_area = self.description_rectangle
    #     text_surface = pygame.Surface(text_area.size, pygame.SRCALPHA)
    #     colour = self.description_font_colour
    #     font = self.description_font
    #     lines = Card.get_width_fitting_strings(
    #         text, text_area.w, font, self.margin)
    #     y = 0
    #     for line in lines:
    #         line_surface = font.render(line, True, colour)
    #         line_rectangle = line_surface.get_rect()
    #         line_rectangle.centerx = text_area.w // 2
    #         line_rectangle.y = y
    #         y += line_rectangle.h
    #         text_surface.blit(line_surface, line_rectangle)
        
    #     cropped_surface = Card.crop_surface(text_surface)
    #     cropped_rectangle = cropped_surface.get_rect()
    #     cx, cy = text_area.center
    #     cropped_rectangle.center = cx + x_correct, cy - y_correct
    #     image.blit(cropped_surface, cropped_rectangle)


    #     circle_points = Card.circle_points
    #     title_surface = self.title_font.render(
    #         self.title, True, self.title_font_colour)
    #     outline_surface = self.title_font.render(
    #         self.title, True, self.outline_font_colour)
    #     title_rect = title_surface.get_rect(center = self.title_center)
    #     for px, py in circle_points:
    #         image.blit(outline_surface, title_rect.move(px, py))
    #     image.blit(title_surface, title_rect)

    #     return image
    
    # def collides(self, position):
    #     """Check if the rectangle of an object collides with given position"""
    #     return self.rectangle.collidepoint(position)

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

    # # outline_distance = 2
    # # circle_points = get_circle_points(outline_distance)
    # # description_rectangle = rect_between(
    # #     description_topleft, description_bottomright)
    
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
    #         if x + word_w > right:
    #             process(line)
    #             x = margin
    #             line = ''
            
    #         line += long
    #         x += long_w
    #     process(line)
    #     return lines

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