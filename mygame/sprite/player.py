
from .entity import Entity
from ..core.paths import defaults

class Player(Entity):

    side: int = 1
    highlighted_colour: list = [128, 0, 64]
    filepath: str = defaults['player']
    image_scale: int = 3
    name: str = 'player'
