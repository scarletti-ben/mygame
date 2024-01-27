
from ..sprite.enemy import Enemy
from ..core.tools import filtered
from ..core.paths import defaults
import random

class Sorcerer(Enemy):

    name: str = 'sorcerer'
    filepath: str = defaults['sorcerer']
    image_scale: int = 1
    intent_history: list = []
    
    # def get_intent(self, state):
    #     """Get entity intent based on current state"""
    #     entities = state.entities
    #     rivals = self.get_rivals(entities)
    #     relatives = self.get_relatives(entities, True)
    #     value = 5 if relatives else 10
    #     recipient = filtered(rivals, 'hp', min)
    #     context = 'damage'
    #     return value, recipient, context

    def align_intention(self, y_offset = - 16):
        """Align the entity intent rectangle above the entity healthbar"""
        bounding = self.healthbar.bounding_rectangle
        rectangle = self.healthbar.rectangle
        mx = rectangle.centerx
        by = bounding.top + y_offset
        self.intention.rectangle.midbottom = mx, by

    def get_intent(self, state):
        """Get entity intent based on current state"""
        entities = state.entities
        rivals = self.get_rivals(entities)
        relatives = self.get_relatives(entities, True)


        percentage = (self.hp / self.hp_max) * 100
        if percentage > 50:
            value = 5
            context = 'damage'
        else:
            contexts = ['damage', 'block']
            values = [5,12]
            if self.intent_history:
                v, r, c = self.intent_history[-1]
                if c == 'block':
                    contexts = ['damage']
                    values = [18]
            value = random.choice(values)
            context = random.choice(contexts)
        if context == 'damage':
            recipient = filtered(rivals, 'hp', min)
        else:
            recipient = self

            
        self.intent_history.append((value, recipient, context))
        return value, recipient, context
    
    def get_tooltip_lines(self):
        """Get lines to be rendered by sprite tooltip"""
        return [
            f'{self.name.title()}',
            f'HP: {self.hp} / {self.hp_max}',
            f'Traits: {len(self.traits)}',
            f'Relics: {len(self.relics)}',
            f'Mana: {self.mana} / {self.base_mana}',
            f'Card Draw: {self.card_draw}',
            # f'Intent: {str(self.get_intent(state))}'
            f'Block: {self.block}'
            ]
    

