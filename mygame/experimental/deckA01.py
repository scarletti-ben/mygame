
# ~ Imports
import pygame, random
from .cardA01 import Card
from typing import List

# ~ Shuffle Class of Deck Tools
class Shuffle:
    def shuffle_owned(self):
        """Shuffle owned"""
        self.announce(message = 'Shuffling owned')
        random.shuffle(self.owned)
    
    def shuffle_draw(self):
        """Shuffle draw"""
        self.announce(message = 'Shuffling draw')
        random.shuffle(self.draw)
    
    def shuffle_hand(self):
        """Shuffle hand"""
        self.announce(message = 'Shuffling hand')
        random.shuffle(self.hand)
    
    def shuffle_discard(self):
        """Shuffle discard"""
        self.announce(message = 'Shuffling discard')
        random.shuffle(self.discard)
    
    def shuffle_exile(self):
        """Shuffle exile"""
        self.announce(message = 'Shuffling exile')
        random.shuffle(self.exile)

# ~ Flip Class of Deck Tools to Move Piles of Cards onto Other Piles
class Flip:
    def flip_owned(self, shuffle = True, clear = True):
        """Move cards from owned to draw and optionally shuffle draw"""
        if clear:
            self.draw.clear()
            self.hand.clear()
            self.discard.clear()
            self.exile.clear()
        cards = self.owned[:]
        for card in cards:
            self.add_card_to_draw(card)
        if shuffle: 
            self.shuffle_draw()
        self.announce(message = f"Cards in draw: {self.cards_in_draw}")

    def flip_hand(self, shuffle = False):
        """Move cards from hand to discard and optionally shuffle discard"""
        self.announce(message = f'Discarding {self.cards_in_hand} card(s) from hand')
        cards = self.hand[:]
        for card in cards:
            self.remove_card_from_hand(card)
            self.add_card_to_discard(card)
        if shuffle:
            self.shuffle_discard()

    def flip_discard(self, shuffle = True):
        """Move cards from discard to draw and optionally shuffle draw"""
        self.draw += self.discard
        self.discard.clear()
        if shuffle: self.shuffle_draw()

# ~ Pull Class of Deck Tools to Move Single Cards to Hand
class Pull:
    def pull_from_draw(self, card):
        """Move a specific card from draw to hand"""
        self.remove_card_from_draw(card)
        self.add_card_to_hand(card)

    def pull_from_discard(self, card):
        """Move a specific card from discard to hand"""
        self.remove_card_from_discard(card)
        self.add_card_to_hand(card)

    def pull_from_exile(self, card):
        """Move a specific card from exile to hand"""
        self.remove_card_from_exile(card)
        self.add_card_to_hand(card)

    def pull_from_draw_top(self):
        """Move card from top of draw to hand"""
        card = self.top_of_draw()
        self.remove_card_from_draw(card)
        self.add_card_to_hand(card)
        self.announce(message = f'Drew {card.name} from draw')

    def pull_from_discard_top(self):
        """Move card from top of discard to hand"""
        if self.cards_in_discard > 0:
            card = self.top_of_discard()
            self.remove_card_from_discard(card)
            self.add_card_to_hand(card)
        else:
            self.announce(message = 'No cards in discard')

    def pull_from_exile_top(self):
        """Move card from top of exile to hand"""
        card = self.top_of_exile()
        self.remove_card_from_exile(card)
        self.add_card_to_hand(card)

    def pull_from_draw_random(self):
        """Get a random card from draw and move to hand"""
        if self.cards_in_draw > 0:
            card = self.random_card_in_draw()
            self.pull_from_draw(card)
        else:
            self.announce(message = 'No cards in draw')

    def pull_from_discard_random(self):
        """Get a random card from discard and move to hand"""
        if self.cards_in_discard > 0:
            card = self.random_card_in_discard()
            self.pull_from_discard(card)
        else:
            self.announce(message = 'No cards in discard')

    def pull_from_exile_random(self):
        """Get a random card from exile and move to hand"""
        if self.cards_in_exile > 0:
            card = self.random_card_in_exile()
            self.pull_from_exile(card)
        else:
            self.announce(message = 'No cards in exile')

# ~ Unused Transfer Class
class Transfer:
    pass

# ~ Push Class of Deck Tools to Move Single Cards from Hand
class Push:
    def push_to_draw(self, card, bottom = False):
        """Move a specific card from hand to draw, top or bottom"""
        self.remove_card_from_hand(card)
        self.add_card_to_draw(card, bottom)
        self.announce(message = f'{card.name} moved to draw')

    def push_to_discard(self, card, bottom = False):
        """Move a specific card from hand to discard, top or bottom"""
        self.remove_card_from_hand(card)
        self.add_card_to_discard(card, bottom)
        self.announce(message = f'{card.name} moved to discard')

    def push_to_exile(self, card, bottom = False):
        """Move a specific card from hand to exile, top or bottom"""
        self.remove_card_from_hand(card)
        self.add_card_to_exile(card, bottom)
        self.announce(message = f'{card.name} moved to exile')

    def push_to_draw_random(self, bottom = False):
        """Get a random card from hand and move to draw"""
        card = self.random_card_in_hand()
        self.push_to_draw(card, bottom)
        self.announce(message = f'{card.name} moved to draw')

    def push_to_discard_random(self, bottom = False):
        """Get a random card from hand and move to discard"""
        card = self.random_card_in_hand()
        self.push_to_discard(card, bottom)
        self.announce(message = f'{card.name} moved to discard')

    def push_to_exile_random(self, bottom = False):
        """Get a random card from hand and move to exile"""
        card = self.random_card_in_hand()
        self.push_to_exile(card, bottom)
        self.announce(message = f'{card.name} moved to exile')

# ~ Add Class of Deck Tools to Add a Single Card to a Pile
class Add:
    def add_card_to_owned(self, card, bottom = False):
        """Add a card to owned"""
        if not bottom: self.owned.append(card)
        else: self.owned.insert(0, card)

    def add_card_to_draw(self, card, bottom = False):
        """Add a card to draw"""
        if not bottom: self.draw.append(card)
        else: self.draw.insert(0, card)

    def add_card_to_hand(self, card, bottom = False):
        """Add a given card to hand, if it does not fit, discard it"""
        if self.cards_in_hand < 10:
            if not bottom: self.hand.append(card)
            else: self.hand.insert(0, card)
            self.announce(message = f'{card.name} added to hand')
        else:
            self.announce(message = f'No space in hand, {card.name} discarded')
            self.add_card_to_discard(card)

    def add_card_to_discard(self, card, bottom = False):
        """Add a card to discard"""
        if not bottom: self.discard.append(card)
        else: self.discard.insert(0, card)

    def add_card_to_exile(self, card, bottom = False):
        """Add a card to exile"""
        if not bottom: self.exile.append(card)
        else: self.exile.insert(0, card)

# ~ Top Class of Deck Tools to Check the Top Card of a Pile
class Top:
    def top_of_owned(self):
        """Return most recent card in owned"""
        return self.owned[-1]
    
    def top_of_draw(self):
        """Return most recent card in draw"""
        return self.draw[-1]

    def top_of_hand(self):
        """Return most recent card in hand"""
        return self.hand[-1]

    def top_of_discard(self):
        """Return most recent card in discard"""
        return self.discard[-1]

    def top_of_exile(self):
        """Return most recent card in exile"""
        return self.exile[-1]

# ~ Bottom Class of Deck Tools to Check the Bottom Card of a Pile
class Bottom:
    def bottom_of_owned(self):
        """Return bottom card in owned"""
        return self.owned[0]
    
    def bottom_of_draw(self):
        """Return bottom card in draw"""
        return self.draw[0]

    def bottom_of_hand(self):
        """Return bottom card in hand"""
        return self.hand[0]

    def bottom_of_discard(self):
        """Return bottom card in discard"""
        return self.discard[0]

    def bottom_of_exile(self):
        """Return bottom card in exile"""
        return self.exile[0]

# ~ Remove Class of Deck Tools Remove a Card from a Pile
class Remove:
    def remove_card_from_owned(self, card):
        """Remove a specific card from owned"""
        self.owned.remove(card)
        self.announce(message = f'{card.name} removed from owned')

    def remove_card_from_draw(self, card):
        """Remove a specific card from draw"""
        self.draw.remove(card)
        self.announce(message = f'{card.name} removed from draw')

    def remove_card_from_hand(self, card):
        """Remove a specific card from hand"""
        self.hand.remove(card)
        self.announce(message = f'{card.name} removed from hand')

    def remove_card_from_discard(self, card):
        """Remove a specific card from discard"""
        self.discard.remove(card)
        self.announce(message = f'{card.name} removed from discard')

    def remove_card_from_exile(self, card):
        """Remove a specific card from exile"""
        self.exile.remove(card)
        self.announce(message = f'{card.name} removed from exile')

# ~ Random Class of Deck Tools to Choose a Random Card in a Pile
class Random:
    def random_card_in_owned(self):
        """Return a random card from owned"""
        return random.choice(self.owned)

    def random_card_in_draw(self):
        """Return a random card from draw"""
        return random.choice(self.draw)

    def random_card_in_hand(self):
        """Return a random card from hand"""
        return random.choice(self.hand)

    def random_card_in_discard(self):
        """Return a random card from discard"""
        return random.choice(self.discard)

    def random_card_in_exile(self):
        """Return a random card from exile"""
        return random.choice(self.exile)

# ~ Quantity Class of Deck Tools to Check Number of Cards that Match Criteria
class Quantity:

    @property
    def cards_in_owned(self):
        """Return the number of cards in owned"""
        return len(self.owned)

    @property
    def cards_in_draw(self):
        """Return the number of cards in draw"""
        return len(self.draw)

    @property    
    def cards_in_hand(self):
        """Return the number of cards in hand"""
        return len(self.hand)

    @property
    def cards_in_discard(self):
        """Return the number of cards in discard"""
        return len(self.discard)

    @property    
    def cards_in_exile(self):
        """Return the number of cards in exile"""
        return len(self.exile)

# ~ Deck Class to Combine Deck Tools
class Deck(Shuffle, Flip, Quantity, Pull, Add, Remove, Random, Top, Bottom, Push, Transfer):
    def __init__(self, owned = None):
        """Initialise 5 card piles as list objects from a single owned set"""
        self.owned: List[Card] = owned if owned is not None else []
        self.draw: List[Card] = []
        self.hand: List[Card] = []
        self.discard: List[Card] = []
        self.exile: List[Card] = []
        self.piles = self.owned, self.draw, self.hand, self.discard, self.exile

    def announce(self, **kwargs):
        """Create a user event with subtype and keyword arguments"""
        if pygame.get_init():
            event_code = pygame.USEREVENT + 1
            event = pygame.event.Event(event_code, kwargs)
            pygame.event.post(event)
        else:
            print(kwargs.get('message', "No message"))

    def draw_one(self):
        """Draw a card, obey limitations of hand size and cards in draw pile"""

        if self.cards_in_hand >= 10:
            self.announce(message = 'You can only hold 10 cards in hand.')

        elif self.cards_in_draw > 0:
            self.pull_from_draw_top()

        elif self.cards_in_discard > 0:
            self.announce(message = 'No cards left in draw pile, flipping discard onto draw')
            self.flip_discard()
            self.draw_one()
        else:
            self.announce(message = 'There are no cards left to draw')

    def draw_many(self, quantity):
        """Draw multiple cards to hand from the draw pile"""
        self.announce(message = f'Drawing {quantity}')
        for _ in range(quantity):
            self.draw_one()

    def discard_card(self, card):
        """Discard a given card and move from hand to discard"""
        self.hand.remove(card)
        self.discard.append(card)
        self.announce(message = f'Discarding {card.name}')

    def discard_random(self):
        """Pick a random card in hand and discard it"""
        if self.cards_in_hand == 0:
            self.announce(message = 'No cards to discard')
        else:
            card = random.choice(self.hand)
            self.discard_card(card)
            self.announce(message = f'Discarded {card.name}')

    def exile_card(self, card):
        """Exile a given card and move from hand to exile"""
        self.hand.remove(card)
        self.exile.append(card)
        self.announce(message = f'Exiling {card.name}')

    def exile_random(self):
        """Pick a random card in hand and exile it"""
        if self.cards_in_hand == 0:
            self.announce(message = 'No cards to exile')
        else:
            card = random.choice(self.hand)
            self.exile_card(card)

    def destroy_card(self, card):
        """Destroy a given card and remove it from any relevant piles"""
        for pile in self.piles:
            if card in pile:
                pile.remove(card)

    def __repr__(self) -> str:
        """Useful debugging function to print card lists"""

        def names(pile):
            """Return object name if available"""
            output = []
            for item in pile:
                if hasattr(item, 'name'):
                    output.append(item.name)
                else:
                    output.append(item)
            return output

        return f"""
-----------------------------------------------------------
Owned:    {self.cards_in_owned} cards: {names(self.owned)}
Draw:     {self.cards_in_draw} cards: {names(self.draw)} 
Hand:     {self.cards_in_hand} cards: {names(self.hand)} 
Discard:  {self.cards_in_discard} cards: {names(self.discard)} 
Exile:    {self.cards_in_exile} cards: {names(self.exile)} 
-----------------------------------------------------------
        """

# ~ Testing
if __name__ == '__main__':

    print("""-------------------------------------
    Testing Information:
        - Simple card class of coloured number squares for visual testing of card movements between piles
        - Render text queue to show movements by printing to pygame window""")

    # ~ Imports
    import pygame, random
    import ctypes

    # ~ Initialise Pygame
    pygame.init()

    # ~ Disable Display Scaling
    ctypes.windll.user32.SetProcessDPIAware()

    # ~ Setup
    W = 1600
    H = 900
    fps = 60
    clock = pygame.time.Clock()
    display = pygame.display.set_mode([W,H])
    fill = [63,63,63]
    user_event = pygame.USEREVENT + 1
    font_name = "G:/Coding/Assets/Fonts/Monogram/monogram.ttf"
    font_size = 32
    font = pygame.font.Font(font_name, font_size)
    font_small = pygame.font.Font(font_name, 24)


    text_queue = []
    def add_render(text, ticks = 160, colour = [0,255,0]):
        """Render text on screen for a period of time"""
        text = str(text).splitlines()
        for line in text:
            surface = font.render(line, True, colour)
            text_queue.append([surface, ticks])

    def render(display, x_offset = 5, y_offset = 5):
        """Display the text queue on screen and update ticks"""
        x, y = display.get_rect().left + x_offset, y_offset
        for item in text_queue[:]:
            item[1] -= 1
            if item[1] <= 0:
                text_queue.remove(item)
                continue
            surface = item[0]
            rectangle = surface.get_rect(topleft = [x, y])
            display.blit(surface, rectangle)
            y += rectangle.h

    def show_title(name, center):
        """Show a simple rendered title"""
        surface = font_small.render(name, True, [255,0,255])
        rectangle = surface.get_rect(center = center)
        display.blit(surface, rectangle)

    # ~ Classes and Functions
    class Card:
        current_value = 1
        def __init__(self):
            """Create card with a simple integer written on a square surface"""
            self.value = Card.current_value
            self.name = f'C{self.value}'
            self.colour = self.get_random_colour()
            self.invert = self.get_inverted_colour(self.colour)
            self.w = 50
            self.h = 50
            self.surface = pygame.Surface([self.w, self.h])
            self.rectangle = self.surface.get_rect()
            self.surface.fill(self.colour)
            rend = font.render(str(self.value), True, self.invert)
            rend_rect = rend.get_rect(center = self.rectangle.center)
            self.surface.blit(rend, rend_rect)
            Card.current_value += 1

        def get_random_colour(self, alpha = None) -> list:
            """Get a random colour in RGB, or RGBA"""
            red = random.randint(0,255)
            green = random.randint(0,255)
            blue = random.randint(0,255)
            if alpha is not None:
                colour = red, green, blue, alpha
            else:
                colour = red, green, blue
            return colour

        def get_inverted_colour(self, colour):
            """Invert colour for visible text"""
            new_colour = []
            for element in colour:
                new_element = 255 - element
                new_colour.append(new_element)
            return new_colour

        def draw(self, display):
            """Draw Card surface at the position of Card rectangle"""
            display.blit(self.surface, self.rectangle)

        def under_mouse(self):
            """Check if rectangle collides with mouse position"""
            return self.rectangle.collidepoint(pygame.mouse.get_pos())

        def draw_outline(self, display, weight = 2, colour = [255,0,0]):
            """Draw an outline rectangle with inflation, outside surface"""
            expansion = int(weight / 2)
            outline = self.rectangle.inflate(expansion, expansion)
            pygame.draw.rect(display, colour, outline, weight)

        def handle(self, *args, **kwargs):
            pass
            
        def update(self, *args, **kwargs):
            pass

        def __repr__(self) -> str:
            return f'C{self.value}'


    def place_left_to_right(group, start_point, spacing = 4):
        """Place all cards in a group from left to right"""
        top, left = start_point
        for item in group:
            item.rectangle.topleft = top, left
            left += item.rectangle.width + spacing

    # ~ Render Controls
    add_render("Try Return, Space, r, up, down, 1, 2, 3, 4, 5, LMB, RMB", 60000)

    # ~ Cards
    deck = Deck([Card() for _ in range(13)])
    deck.flip_owned()
    Deck.announce(deck, message = deck)


    # ~ Game Loop
    while True:

        # ~ Clear Display
        display.fill(fill)

        # ~ Get Current State
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        mx, my = mouse_position = pygame.mouse.get_pos()
        buttons = pygame.mouse.get_pressed()

        # ~ Event Queue
        for event in events:
            if event.type == pygame.QUIT: quit()
            if event.type == user_event:
                if hasattr(event, 'message'):
                    add_render(event.message)
    
            # ~ Handle Single Mouse Button and Key Presses, and Mouse Release
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    deck.flip_hand()
                    deck.draw_many(5)
                elif event.key == pygame.K_i:
                    print(deck)
                elif event.key == pygame.K_SPACE:
                    deck.draw_many(5)
                elif event.key == pygame.K_ESCAPE: ...
                elif event.key == pygame.K_r:
                    deck.flip_owned()
                elif event.key == pygame.K_UP:
                    deck.draw_one()
                elif event.key == pygame.K_DOWN:
                    deck.push_to_discard_random()
                elif event.key == pygame.K_1:
                    deck.draw_many(1)
                elif event.key == pygame.K_2:
                    deck.draw_many(2)
                elif event.key == pygame.K_3:
                    deck.draw_many(3)
                elif event.key == pygame.K_4:
                    deck.draw_many(4)
                elif event.key == pygame.K_5:
                    deck.draw_many(5)
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for card in deck.hand:
                        if card.under_mouse():
                            deck.discard_card(card)
                            break
                    else:
                        for card in deck.draw:
                            if card.under_mouse():
                                deck.pull_from_draw(card)
                                break
                        else:
                            for card in deck.discard:
                                if card.under_mouse():
                                    deck.pull_from_discard(card)
                                    break
                            else:
                                for card in deck.exile:
                                    if card.under_mouse():
                                        deck.pull_from_exile(card)
                                        break
                    
                elif event.button == 3:
                    for card in deck.hand:
                        if card.under_mouse():
                            deck.exile_card(card)
                            break
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: ...
                elif event.button == 3: ...

        # ~ Handle Held Buttons and Keys
        if keys[pygame.K_UP]: ...
        elif keys[pygame.K_DOWN]: ...
        if keys[pygame.K_LEFT]: ...
        elif keys[pygame.K_RIGHT]: ...
        if keys[pygame.K_w]: ...
        elif keys[pygame.K_s]: ...
        if keys[pygame.K_a]: ...
        elif keys[pygame.K_d]: ...
        if buttons[0]: ...
        elif buttons[2]: ...

        place_left_to_right(deck.owned, [10,40], 4)
        show_title('Owned', [35,20])
        for item in deck.owned:
            item.draw(display)
            if item.under_mouse():
                item.draw_outline(display, 4)

        place_left_to_right(deck.draw, [110,40], 4)
        show_title('Draw', [135,20])
        for item in deck.draw:
            item.draw(display)
            if item.under_mouse():
                item.draw_outline(display, 4)

        place_left_to_right(deck.hand, [210,40], 4)
        show_title('Hand', [235,20])
        for item in deck.hand:
            item.draw(display)
            if item.under_mouse():
                item.draw_outline(display, 4)

        place_left_to_right(deck.discard, [310,40], 4)
        show_title('Discard', [335,20])
        for item in deck.discard:
            item.draw(display)
            if item.under_mouse():
                item.draw_outline(display, 4)

        place_left_to_right(deck.exile, [410,40], 4)
        show_title('Exile', [435,20])
        for item in deck.exile:
            item.draw(display)
            if item.under_mouse():
                item.draw_outline(display, 4)
            
        # ~ Update Display
        render(display, 500)
        pygame.display.flip()	
        clock.tick(fps)

# > Information
elif __name__ != "__main__":
    print("""-------------------------------------
deck.py imported successfully
-------------------------------------
    Name: deck.py
    Purpose: Sort, shuffle and transfer cards between the 5 card piles
    Information:
        - Card movements are announced as pygame event messages
            - Messages could be tagged 'deck' if needed
        - The Deck class is for 5 lists interacting
        - Vast array of functions for moving cards between piles
        """)