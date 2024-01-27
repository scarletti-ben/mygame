
from .entity import Entity
from ..core.paths import defaults

class Enemy(Entity):

    side: int = 2
    highlighted_colour: list = [100, 100, 0]
    filepath: str = defaults['enemy']
    image_scale: int = 5