
# Postit Notes 
    # Card collision rectangles are being skewed by mana circle
        # The card surface extends further than the edge of the card frame
    # Held and Hovered card system needs to be re-evalulated and finalised
    # Card building mechanics need to be added
    # Card stats and entity damage needed
    # Enemy intent indicators needed

# Postit - To avoid collision issues, slay the spire makes the hovered card larger but parts the waves so that other cards do not overlap with the hovered card


# --- Layouts and entity alignmnets of its current objects, with a sort of layering system similar to queue

# ~ General Imports and Initialisation
import pygame, mygame
from mygame.core.locals import *
pygame.init()
mygame.disable_dpi_scaling()
mygame.clear_terminal()

# ~ Object Imports
from mygame.sprite.entity import Entity
from mygame.sprite.button import Button
from mygame.experimental.traitA01 import Trait
from mygame.experimental.deckA01 import Deck
from mygame.experimental.cardA01 import Card
from mygame.experimental.wormA01 import Worm
from mygame.experimental.stateA01 import state
from mygame.experimental.intentA01 import Intent
from mygame.sprite.queue import Queue
from mygame.sprite.enemy import Enemy
from mygame.sprite.player import Player
from typing import List
from mygame.animation import DamageNumber

# ~ Setup
display = Display(W, H)
clock = Clock()
font = Font()
mygame.set_cursor()

# ~ Button
button = Button(name = 'End Turn', scale = 6)
button.rectangle.topright = [W, 0]
button.rectangle.center = CENTER

# ~ Player
player: Player = Player()
player.rectangle.bottom = CY + 200
player.rectangle.centerx = 300

# ~ Enemy
enemy: Enemy = Worm()
enemy.rectangle.bottom = player.rectangle.bottom
enemy.rectangle.centerx = W - 300

# ~ ======================================================================
# - Section Intent
# ~ ======================================================================

enemy.intention = Intent(enemy)

# ~ ======================================================================
# - Section END
# ~ ======================================================================

# ~ Trait
for _ in range(14):
    trait = Trait()
    trait.rectangle.center = CENTER
    player.traits.append(trait)

queue = Queue()

background = mygame.core.paths.defaults['background']
background = Image(background, size = [W, H])

entities: List[Entity] = [player, enemy]

player.deck: Deck = Deck()
for n in range(15):
    card = Card(f'test{n}')
    player.deck.add_card_to_owned(card)
# print(player.deck)
player.deck.shuffle_owned()
# print(player.deck)
player.deck.flip_owned()
player.deck.draw_many(5)
# print(player.deck)
rectangles = [card.rectangle for card in player.deck.hand]
y = H + card.rectangle.height // 2.5
mygame.other.align_rectangles_x(rectangles, y, overlap = 0.4)

cards: List[Card] = player.deck.hand

held = None

state.entities = entities

for entity in entities:
    if entity.side == 2:
        entity.intent = entity.get_intent(state)



# ~ Game Loop
while True:

    display.blit(background, [0,0])
    events = pygame.event.get()
    mouse = pygame.mouse.get_pos()

    button.enqueue(queue)
    button.update()
    if button.collides(mouse):
        button.tooltip.enqueue(queue)

    if held:
        player.enqueue_corners(queue)

    for entity in entities:

        if entity.collides(mouse):
            if entity.collides_mask(mouse):
                if held is None:
                    entity.enqueue_tooltip(queue)
                entity.enqueue_corners(queue)
                entity.enqueue_highlighted(queue)
            else:
                entity.enqueue(queue)
        else:
            entity.enqueue(queue)

        entity.align_healthbar()
        entity.healthbar.enqueue(queue)

        entity.align_traits(5)

        for trait in entity.traits:
            trait.enqueue(queue)
            if trait.collides_mouse():
                if held is None:
                    trait.enqueue_tooltip(queue)
                trait.enqueue_corners(queue)

    rects = [card.rectangle for card in cards if card is not held]
    mygame.other.align_rectangles_x(rects, y, overlap = 0.4)

    # n = 180
    # if held is None:
    #     for card in list(reversed(player.deck.hand)):
    #         if card is hovered:
    #             collision_rect = card.rectangle.copy()
    #             collision_rect.inflate_ip(0,n)
    #             collision_rect.bottom = card.rectangle.bottom
    #             if collision_rect.collidepoint(mouse):
    #                 hovered = card
    #                 pygame.draw.rect(display, [0,255,0], collision_rect)
    #                 pygame.draw.rect(display, [255,255,128], card.rectangle, 12)
    #                 break
    #         else:
    #             if card.collides(mouse):
    #                 hovered = card
    #                 break
    #     else:
    #         hovered = None

    hovered = None
    if held is None:
        for card in list(reversed(player.deck.hand)):
            if card.collides(mouse):
                hovered = card
                break
            
    for card in player.deck.hand:
        if card is hovered:
            rectangle = card.rectangle.move(0,-80)
            descriptor = 'hovered_card'
            queue.add(card.surface, rectangle, descriptor)
        elif card is held:
            rectangle = card.rectangle.copy()
            rectangle.center = mouse
            descriptor = 'held_card'
            queue.add(card.surface, rectangle, descriptor)
        else:
            queue.add(card.surface, card.rectangle, card.descriptor)

    for event in events:
        if event.type == pygame.QUIT:
            quit(f'\nExit Code: User has closed the application.\n')

        if event.type == pygame.KEYDOWN:
            intent = enemy.get_intent(state)
            # print(intent)

            for _ in range(5):

                test = DamageNumber('8', [200,200])
                test.enqueue(queue)

        if event.type == USER_EVENT:
            if getattr(event, 'subtype', None) == 'button_press':
                for entity in entities:
                    if entity.side == 2:
                        entity.block = 0
                        value, recipient, context = entity.intent
                        if context == 'damage':
                            recipient.assess_damage(value)
                        elif context == 'block':
                            recipient.block += value
                for entity in entities:
                    if entity.side == 1:
                        entity.block = 0
                    elif entity.side == 2:
                        entity.intent = entity.get_intent(state)

        if event.type == pygame.MOUSEBUTTONDOWN:
            for card in cards:
                if card.collides(event.pos):
                    held = card
        elif event.type == pygame.MOUSEBUTTONUP:
            held = None
            
        button.handle(event)
        for entity in entities:
            if entity.clicked(event):
                result = entity.assess_damage(3)
                if result['target_killed']:
                    quit(f'\nExit Code: {entity} has died\n')


    queue.rect(enemy.healthbar.bounding_rectangle)

    enemy.align_intention()
    enemy.intention.enqueue(queue)
    if enemy.intention.collidepoint(mouse):
        enemy.intention.tooltip.enqueue(queue)

    queue.draw(display)
    pygame.display.flip()
    clock.tick(FPS)