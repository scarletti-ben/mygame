
from .core.locals import *
from .core.paths import *
from .core.tools import clear_terminal, disable_dpi_scaling, post, set_cursor
from .sprite.queue import Queue
from .sprite.sprite import Sprite, SpriteLite, SpriteRotating
from pygame.locals import *
import sys
import re

from typing import Any, List
# from pygame.freetype import SysFont


pygame.init()
disable_dpi_scaling()

display = Display(W, H)
clock = Clock()
font = Font()
queue = Queue()
background = Image(defaults['background'], size = [W,H])

from mygame.experimental.tilesheetA02 import tilesheet
from mygame.sprite.entity import Entity
from mygame.experimental.wormA01 import Worm
from mygame.experimental.sorcererA01 import Sorcerer
from mygame.experimental.traitA01 import Trait as TraitParent
from mygame.sprite.player import Player
from mygame.experimental.card_width_fitting_textA01 import Card as WidthCard
from mygame.experimental.card_builderA01 import CardBuilder
from mygame.other import align_rectangles_x
from mygame.experimental.deckA01 import Deck
from mygame.other import draw_framerate

def open_frame():
    """Clear the display"""
    display.fill(GREY)

def close_frame():
    """Update the display and progress framerate clock"""
    pygame.display.flip()
    clock.tick(FPS)

def handle_quit(event):
    """Handle a quit event in the queue"""
    if event.type == pygame.QUIT:
        quit()

clear_terminal()
# disable_dpi_scaling()
set_cursor()

class Events:
    def __iter__(self):
        """Create an iterator out of pygame events"""
        items = pygame.event.get()
        return iter(items)

events = Events()

