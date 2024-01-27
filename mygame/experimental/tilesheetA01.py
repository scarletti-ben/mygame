
from typing import Any
import pygame
from ..core.paths import defaults
from ..core.locals import Image
from dataclasses import dataclass

# filepath = defaults['traits']

# def get_trait_image_dictionary(scale = 1) -> dict:
#     """Get trait images as a key, value dictionary"""
#     sheet = Image(filepath, scale)
#     w = 32 * scale
#     rectangle_dictionary = {
#         'vulnerable': [2 * w, 3 * w, 1 * w, 1 * w],
#         'dexterity': [2 * w, 6 * w, 1 * w, 1 * w],
#         'strength': [11 * w, 5 * w, 1 * w, 1 * w],
#         'weak': [10 * w, 17 * w, 1 * w, 1 * w],
#         'wrath': [11 * w, 3 * w, 1 * w, 1 * w],
#         'darksign': [9 * w, 3 * w, 1 * w, 1 * w],
#         'intangible': [12 * w, 1 * w, 1 * w, 1 * w],
#         'vigor': [4 * w, 3 * w, 1 * w, 1 * w],
#         'boot': [2 * w, 8 * w, 1 * w, 1 * w],
#         'dazed': [14 * w, 3 * w, 1 * w, 1 * w],
#         'dummy': [7 * w, 3 * w, 1 * w, 1 * w],
#         'needle': [10 * w, 4 * w, 1 * w, 1 * w],
#         'enlightenment': [7 * w, 4 * w, 1 * w, 1 * w],
#         'snecko': [13 * w, 13 * w, 1 * w, 1 * w],
#         'preparation': [0 * w, 10 * w, 1 * w, 1 * w],
#         'hinder': [0 * w, 4 * w, 1 * w, 1 * w],
#         'barricade': [8 * w, 3 * w, 1 * w, 1 * w],
#         'freedom': [0 * w, 11 * w, 1 * w, 1 * w],
#         'curlup': [6 * w, 2 * w, 1 * w, 1 * w],
#         'thorns': [13 * w, 5 * w, 1 * w, 1 * w],
#     }
#     subsurface_dictionary = {key: sheet.subsurface(rectangle) for key, rectangle in rectangle_dictionary.items()}
#     return subsurface_dictionary

class __MetaClass(type):

    def __getattr__(cls, name):
        """Override default attribute access from type in metaclassed children"""
        if not cls.initialised:
            raise UserWarning(f'{cls.__name__} not initialised, please run {cls.__name__}.init()')
        return super().__getattribute__(name)

class TileSheet(metaclass = __MetaClass):
    scale = 1
    w = 32 * scale
    filepath = defaults['traits']
    rectangle_dictionary = {
        'vulnerable': [2 * w, 3 * w, 1 * w, 1 * w],
        'dexterity': [2 * w, 6 * w, 1 * w, 1 * w],
        'strength': [11 * w, 5 * w, 1 * w, 1 * w],
        'weak': [10 * w, 17 * w, 1 * w, 1 * w],
        'wrath': [11 * w, 3 * w, 1 * w, 1 * w],
        'darksign': [9 * w, 3 * w, 1 * w, 1 * w],
        'intangible': [12 * w, 1 * w, 1 * w, 1 * w],
        'vigor': [13 * w, 1 * w, 1 * w, 1 * w],
        'boot': [2 * w, 8 * w, 1 * w, 1 * w],
        'dazed': [14 * w, 3 * w, 1 * w, 1 * w],
        'dummy': [7 * w, 3 * w, 1 * w, 1 * w],
        'needle': [10 * w, 4 * w, 1 * w, 1 * w],
        'enlightenment': [7 * w, 4 * w, 1 * w, 1 * w],
        'snecko': [13 * w, 13 * w, 1 * w, 1 * w],
        'preparation': [0 * w, 10 * w, 1 * w, 1 * w],
        'hinder': [0 * w, 4 * w, 1 * w, 1 * w],
        'barricade': [8 * w, 3 * w, 1 * w, 1 * w],
        'freedom': [0 * w, 11 * w, 1 * w, 1 * w],
        'curlup': [6 * w, 2 * w, 1 * w, 1 * w],
        'thorns': [13 * w, 5 * w, 1 * w, 1 * w],
    }
    vulnerable: pygame.Surface = NotImplemented
    dexterity: pygame.Surface = NotImplemented
    strength: pygame.Surface = NotImplemented
    weak: pygame.Surface = NotImplemented
    wrath: pygame.Surface = NotImplemented
    darksign: pygame.Surface = NotImplemented
    intangible: pygame.Surface = NotImplemented
    vigor: pygame.Surface = NotImplemented
    boot: pygame.Surface = NotImplemented
    dazed: pygame.Surface = NotImplemented
    dummy: pygame.Surface = NotImplemented
    needle: pygame.Surface = NotImplemented
    enlightenment: pygame.Surface = NotImplemented
    snecko: pygame.Surface = NotImplemented
    preparation: pygame.Surface = NotImplemented
    hinder: pygame.Surface = NotImplemented
    barricade: pygame.Surface = NotImplemented
    freedom: pygame.Surface = NotImplemented
    curlup: pygame.Surface = NotImplemented
    thorns: pygame.Surface = NotImplemented
    initialised: bool = False

    @classmethod
    def init(cls):
        """Initialise the tilesheet with surfaces"""
        if not cls.initialised:
            sheet = Image(cls.filepath, cls.scale)
            for key, rectangle in cls.rectangle_dictionary.items():
                setattr(cls, key, sheet.subsurface(rectangle))
            cls.initialised = True