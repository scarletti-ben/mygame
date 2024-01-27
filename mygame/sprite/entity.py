
import pygame
from .sprite import Sprite
from .healthbar import Healthbar
from ..core.paths import defaults
from ..core.locals import Image

class Entity(Sprite):

    side: str = None
    descriptor: str = 'entity'
    highlighted_colour: list = [0,40,140]
    filepath: str = defaults['entity']
    image_scale: int = 3

    def __init__(self, name = None, image = None, side = None):
        """Default entity class"""
        self.name: str = self.name if name is None else name
        if image is None:
            image = Image(self.filepath, self.image_scale)
        self.surface: pygame.Surface = image
        self.rectangle: pygame.rect.Rect = image.get_rect()
        self.traits: list = []
        self.relics: list = []
        self.potions: list = []
        self.hp: int = 50
        self.hp_max: int = 70
        self.block: int = 4
        self.mana: int = 3
        self.base_mana: int = 3
        self.card_draw: int = 5
        self.side: int = self.side if side is None else side
        self.healthbar: Healthbar = Healthbar(self, self.font)

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

    def get_tooltip_lines(self):
        """Get lines to be rendered by sprite tooltip"""
        return [
            f'{self.name.title()}',
            f'HP: {self.hp} / {self.hp_max}',
            f'Traits: {len(self.traits)}',
            f'Relics: {len(self.relics)}',
            f'Potions: {len(self.potions)}',
            f'Mana: {self.mana} / {self.base_mana}',
            f'Card Draw: {self.card_draw}',
            f'Block: {self.block}'
            ]
    
    def get_rivals(self, entities):
        """Get all entities that are not on the same side"""
        return [entity for entity in entities if entity.side != self.side]

    def get_relatives(self, entities, remove_self = True):
        """Get all entities that are on the same side"""
        relatives = [entity for entity in entities if entity.side == self.side]
        if remove_self:
            relatives.remove(self)
        return relatives
    
# ~ ======================================================================
# - Section Unrefined Methods
# ~ ======================================================================

    def assess_damage(self, damage):
        """Assess damage vs block and return all initial and final values"""

        damage = damage
        starting_block = self.block
        starting_hp = self.hp
        final_block = max(0, starting_block - damage)
        blocked_damage = starting_block - final_block
        flesh_damage = max(0, damage - starting_block)
        final_hp = self.hp - flesh_damage
        block_broken = starting_block > 0 and final_block == 0
        target_killed = final_hp <= 0

        print('---------------------\nAssessing damage')
        for key, value in locals().items():
            print(f'    {key} = {value}')
        print('')

        self.block = final_block
        self.hp = final_hp

        return locals()
