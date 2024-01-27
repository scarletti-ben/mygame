
import pygame, os, random, numpy, math, time, ctypes, typing, sys
from .constants import USER_EVENT
from .paths import defaults

__all__ = [
    'disable_dpi_scaling',
    'clear_termninal',
    'post',
]

def disable_dpi_scaling():
    """Use ctypes.windll.user32.SetProcessDPIAware() to disable dpi scaling of windows preventing graphical issues"""
    ctypes.windll.user32.SetProcessDPIAware()
    print('DPI scaling of window resolution disabled')

def clear_terminal():
    """Use os.system('cls') to clear terminal"""
    os.system('cls')

def post(subtype, **kwargs):
    """Post user event with subtype and keyword arguments"""
    dictionary = {'subtype': subtype}
    dictionary.update(kwargs)
    event_code = USER_EVENT
    event = pygame.event.Event(event_code, dictionary)
    pygame.event.post(event)

def set_cursor(surface: pygame.Surface = None) -> None:
    """Set the current cursor to a given surface, faster than blitting"""
    if surface is None:
        try:
            filename = defaults['cursor']
            surface = pygame.image.load(filename).convert_alpha()
        except pygame.error:
            raise UserWarning('set_cursor must be called after display = pygame.set_mode()')
    hotspot = (0,0)
    cursor = pygame.cursors.Cursor(hotspot, surface)
    pygame.mouse.set_cursor(cursor)

def remove_icon() -> None:
    """Set pygame window icon to an invisible surface"""
    invisible_icon = pygame.Surface([32,32], pygame.SRCALPHA)
    pygame.display.set_icon(invisible_icon)

def set_caption(text = '') -> None:
    """Set window caption to given text, leave blank to remove caption"""
    pygame.display.set_caption(text)

def update_directory(_file = None):
    """Set the current directory to be the folder the of the __file__ provided"""
    if _file is None:
        raise FileNotFoundError("You must pass the current module's __file__ built-in")
    file_path = os.path.abspath(_file)
    current_directory = os.path.dirname(file_path)
    os.chdir(current_directory)
    print(f'Current working directory set to:\n{current_directory}')

# * Used for outputting files from --onefile frozen exe applications to external directory
def get_frozen_resourece_path_external(filename = 'data.csv'):
    """Get filepath relative to the directory the .exe application file is being run in"""

    # ~ If being run as a script then regular behaviour looks for file in script.py directory
    if __file__ is not None:
        file_path = os.path.abspath(__file__)
        directory = os.path.dirname(file_path)
        return os.path.join(directory, filename)

    # ~ Determine if application is a python script file or frozen exe
    if getattr(sys, 'frozen', False):
        working_directory = os.path.dirname(sys.executable)
    elif __file__:
        working_directory = os.path.dirname(__file__)
    filepath = os.path.join(working_directory, filename)
    return filepath

# ~ Used for inputting files from internal structure --onefile frozen appliactions
def get_frozen_resource_path_internal(filename = 'monogram.ttf'):
    """Get filepath relative to the internal directory of the .exe application"""

    # ~ If being run as a script then regular behaviour looks for file in script.py directory
    if __file__ is not None:
        file_path = os.path.abspath(__file__)
        directory = os.path.dirname(file_path)
        return os.path.join(directory, filename)

    # ~ Determine if application is a python script file or frozen exe
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, filename)

# def update_frozen_directory():
#     """Set the current directory to be the folder the of the frozen .exe file being run"""
#     if getattr(sys, 'frozen', False):
#         working_directory = os.path.dirname(sys.executable)
#     elif __file__:
#         working_directory = os.path.dirname(__file__)
#     os.chdir(working_directory)

def save_image(image, name = 'image', extension = '.png'):
    """Save image to file with a given name and extension [png, jpeg]"""
    filename = name + extension
    pygame.image.save(image, filename)

def filtered(items, attribute, operation = None):
    """Filter a list of items by attribute and operation and return"""
    if not items:
        return items
    return operation(items, key = lambda item: getattr(item, attribute))

def get_random_colour(alpha = None) -> list:
    """Get a random colour in RGBA"""
    red = random.randint(0,255)
    green = random.randint(0,255)
    blue = random.randint(0,255)
    colour = red, green, blue
    if alpha:
        colour.append(alpha)
    return colour

def get_inverted_colour(colour) -> list:
    """Invert a given colour and return"""
    r, g, b = colour[0:3]
    inverted = [255 - r, 255 - g, 255, b]
    if len(colour) == 4:
        alpha = colour[3]
        inverted.append(alpha)
    return inverted

def get_bounding_rectangle(rectangles) -> pygame.Rect:
    """For a set of rectangles, get the rectangle that encompasses all of them"""
    min_x = min(rect[0] for rect in rectangles)
    min_y = min(rect[1] for rect in rectangles)
    max_x = max(rect[0] + rect[2] for rect in rectangles)
    max_y = max(rect[1] + rect[3]for rect in rectangles)
    width = max_x - min_x
    height = max_y - min_y
    return pygame.Rect(min_x, min_y, width, height)

def zero_fill(number, minimum_figures = 1) -> str:
    """Prefix a number with zeros if below minimum figures, returns a string"""
    number = str(number)
    return number.zfill(minimum_figures)

zfill = zero_fill
minimum_figures = zero_fill
min_significant_figures = zero_fill