
import pygame, string

DEBUGGING: bool = False
W: int = 1600
H: int = 900
CX: int =  W // 2
CY: int = H // 2
FULLSCREEN: bool = False
CENTER: list = CX, CY
FPS: int = 60
GREY: list = [63,63,63]
USER_EVENT: int = pygame.USEREVENT + 1
FONT_NAME: str = "G:/Coding/Assets/Fonts/Monogram/monogram.ttf"
FONT_SIZE: int = 24
CHARACTERS: set = set(string.ascii_letters + string.digits + string.punctuation)

# ~ ======================================================================
# - ANSI Colour Codes for Terminal Colours / Colour Console
    # -- Example usage found in terminal_colour_ANSI.py
    # -- print(f'{ANSI_YELLOW + UNDERLINE}yellow underlined words go here{ANSI_COLOUR_OFF + UNDERLINE_OFF})
# ~ ======================================================================

ANSI_RESET = ANSI_OFF = '\033[0m'
ANSI_COLOUR_OFF = '\033[39m'
ANSI_BOLD = '\033[1m'
ANSI_BOLD_OFF = '\033[22m'
ANSI_UNDERLINE = '\033[4m'
ANSI_UNDERLINE_OFF = '\033[24m'
ANSI_LIGHTMAGENTA = '\033[95m'
ANSI_LIGHTBLUE = '\033[94m'
ANSI_LIGHTCYAN = '\033[96m'
ANSI_LIGHTGREEN = '\033[92m'
ANSI_YELLOW = '\033[93m'
ANSI_DARKRED = '\033[91m'
ANSI_BLACK = '\033[30m'
ANSI_RED = '\033[31m'
ANSI_LIMEGREEN = '\033[32m'
ANSI_LIGHTYELLOW = '\033[33m'
ANSI_BLUE = '\033[34m'
ANSI_MAGENTA = '\033[35m'
ANSI_CYAN = '\033[36m'
ANSI_WHITE = '\033[37m'
ANSI_POSTIT = '\033[48;2;255;238;88m\033[38;2;0;0;0m'
ANSI_POSTIT_OFF = '\033[0m'
# ANSI_RGB_CUSTOM = '\033[38;2;{0 to 255 RED HERE};{0 to 255 GREEN HERE};{0 to 255 BLUE HERE}m'

if __name__ != "__main__":
    print("""
-------------------------------------
mygame.constants.py imported successfully
-------------------------------------
    Package: mygame
    Purpose: Add constants from mygame that are useful in the local namespace
    Information: 
        - None
""")