
import pygame
from ..core.paths import defaults
from ..core.locals import Image

if not pygame.display.get_init():
    raise UserWarning(f'{__name__} generates images and must be imported after the display has been initialised')
else:
    print(f'{__name__} has initialised images for use')

class tilesheet:
    """Tilesheet as object"""
    scale = 1
    w = 32 * scale
    filepath = defaults['traits']
    sheet = Image(filepath, scale)
    vulnerable: pygame.Surface = sheet.subsurface([2 * w, 3 * w, 1 * w, 1 * w])
    dexterity: pygame.Surface = sheet.subsurface([2 * w, 6 * w, 1 * w, 1 * w])
    strength: pygame.Surface = sheet.subsurface([11 * w, 5 * w, 1 * w, 1 * w])
    weak: pygame.Surface = sheet.subsurface([10 * w, 17 * w, 1 * w, 1 * w])
    wrath: pygame.Surface = sheet.subsurface([11 * w, 3 * w, 1 * w, 1 * w])
    darksign: pygame.Surface = sheet.subsurface([9 * w, 3 * w, 1 * w, 1 * w])
    intangible: pygame.Surface = sheet.subsurface([6 * w, 1 * w, 1 * w, 1 * w])
    counter: pygame.Surface = sheet.subsurface([5 * w, 2 * w, 1 * w, 1 * w])
    vigor: pygame.Surface = sheet.subsurface([7 * w, 1 * w, 1 * w, 1 * w])
    reaper: pygame.Surface = sheet.subsurface([8 * w, 1 * w, 1 * w, 1 * w])
    boot: pygame.Surface = sheet.subsurface([2 * w, 8 * w, 1 * w, 1 * w])
    dazed: pygame.Surface = sheet.subsurface([14 * w, 3 * w, 1 * w, 1 * w])
    dummy: pygame.Surface = sheet.subsurface([7 * w, 3 * w, 1 * w, 1 * w])
    needle: pygame.Surface = sheet.subsurface([10 * w, 4 * w, 1 * w, 1 * w])
    enlightenment: pygame.Surface = sheet.subsurface([7 * w, 4 * w, 1 * w, 1 * w])
    snecko: pygame.Surface = sheet.subsurface([13 * w, 13 * w, 1 * w, 1 * w])
    preparation: pygame.Surface = sheet.subsurface([0 * w, 10 * w, 1 * w, 1 * w])
    hinder: pygame.Surface = sheet.subsurface([0 * w, 4 * w, 1 * w, 1 * w])
    barricade: pygame.Surface = sheet.subsurface([8 * w, 3 * w, 1 * w, 1 * w])
    freedom: pygame.Surface = sheet.subsurface([12 * w, 14 * w, 1 * w, 1 * w])
    artefact: pygame.Surface = sheet.subsurface([0 * w, 11 * w, 1 * w, 1 * w])
    curlup: pygame.Surface = sheet.subsurface([6 * w, 2 * w, 1 * w, 1 * w])
    thorns: pygame.Surface = sheet.subsurface([13 * w, 5 * w, 1 * w, 1 * w])
    time: pygame.Surface = sheet.subsurface([15 * w, 10 * w, 1 * w, 1 * w])
    bandages: pygame.Surface = sheet.subsurface([15 * w, 9 * w, 1 * w, 1 * w])
    pestle: pygame.Surface = sheet.subsurface([12 * w, 11 * w, 1 * w, 1 * w])
    payback: pygame.Surface = sheet.subsurface([12 * w, 12 * w, 1 * w, 1 * w])
    bomb: pygame.Surface = sheet.subsurface([12 * w, 10 * w, 1 * w, 1 * w])
    smoothstone: pygame.Surface = sheet.subsurface([1 * w, 17 * w, 1 * w, 1 * w])
    electrify: pygame.Surface = sheet.subsurface([8 * w, 16 * w, 1 * w, 1 * w])
    thick_skin: pygame.Surface = sheet.subsurface([8 * w, 17 * w, 1 * w, 1 * w])
    potion_red : pygame.Surface = sheet.subsurface([0 * w, 9 * w, 1 * w, 1 * w])
    potion_blue : pygame.Surface = sheet.subsurface([1 * w, 9 * w, 1 * w, 1 * w])
    potion_green : pygame.Surface = sheet.subsurface([2 * w, 9 * w, 1 * w, 1 * w])
    potion_yellow : pygame.Surface = sheet.subsurface([3 * w, 9 * w, 1 * w, 1 * w])
    potion_orange : pygame.Surface = sheet.subsurface([13 * w, 9 * w, 1 * w, 1 * w])
    potion_purple : pygame.Surface = sheet.subsurface([14 * w, 9 * w, 1 * w, 1 * w])
    potion_shiny : pygame.Surface = sheet.subsurface([10 * w, 9 * w, 1 * w, 1 * w])
    potion_empty : pygame.Surface = sheet.subsurface([0 * w, 19 * w, 1 * w, 1 * w])

















