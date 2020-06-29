# import and initialise colorama so the ANSI colour codes are handled for Windows
from colorama import init
init()

import os, sys, random

""" Notice for functions which return any values
Functions will return 1 or the value asked for when run,
if an error occurs or arguments are invalid they'll return a 0.
"""

class Suit:
    """ Class representing each suit in the deck of cards.

    Attributes:
        name: name of the suit
        symbol: the symbol associated with the suit
        colour: the colour the suit is
    """

    def __init__(self, name, symbol, colour):
        self.name = name
        self.symbol = symbol
        self.colour = colour

    def __str__(self):
        return self.symbol

    def get_name(self):
        return self.name

    def get_colour(self):
        return self.colour


class Card:
    """ Class representing each card in the game.

    Attributes:
        ansi_codes (class): contains the escape codes for displaying colours
        suit: one of 4 values - diamonds, hearts, spades or clubs
        value: the value of the card, 2-10, ace, king, queen, jack
        rank: the ranking of the card 0-12 so we know what order they should be in
        shown: whether or not the card is facing up or down on the board
    """

    ansi_codes = {
        'red' : '\u001b[31m',
        'black' : '',
        'reset' : '\u001b[0m'
    }

    def __init__(self, suit, value, rank, shown = False):
        self.suit = suit
        self.value = value
        self.rank = rank
        self.shown = shown

    def __str__(self):
        if self.shown:
            return f"{self.ansi_codes[self.suit.colour]}{self.value}{self.suit}{self.ansi_codes['reset']}"
        else:
            return '[]'

    def get_value(self):
        return self.value

    def get_rank(self):
        return self.rank

    def get_suit(self):
        return self.suit

    def toggle_shown(self):
        self.shown = !self.shown

    def is_shown(self):
        return self.shown


class CardCollection:
    """ Class representing a collection of cards.

    The collection will initially be empty, cannot be populated during instanitation.

    Attributes:
        cards: a standard list containing all the cards in the collection
    """

    def __init__(self):
        self.cards = list()

    def add(self, card):
        if isinstance(card, Card):
            self.cards.append(card)
            return 1
        return 0

    def remove(self, card):
        if card in self.cards:
            self.cards.remove(card)
            return 1
        return 0

    def get_cards(self):
        return self.cards

    def get_card(self, index):
        if self.size() > index:
            return self.cards[index]
        else:
            return 0

    def merge(self, collection):
        if isinstance(collection, list):
            for card in collection:
                self.add(card)
            return 1
        elif isinstance(collection, CardCollection):
            for card in collection.get_cards():
                self.add(card)
            return 1
        return 0

    def create_subset(self, index):
        if index < self.size():
            collection = CardCollection()
            for card in self.get_cards():
                collection.add(card)
            return collection
        else:
            return 0

    def shuffle(self):
        random.shuffle(self.cards)

    def size(self):
        return len(self.cards)


class Deck(CardCollection):
    """ Class representing the game deck.

    Inherits from the CardCollection class.

    Attributes:
        suits (class): dictionary containing all the suits and details about them
        faces (class): dictionary containing the various face cards
        cards (inherited): a standard list containing all the cards in the collection
    """

    suits = {
        'clubs' : Suit('clubs', '♣', 'black'),
        'spades' : Suit('spades', '♠', 'black'),
        'hearts' : Suit('hearts', '♥', 'red'),
        'diamonds' : Suit('diamonds', '♦', 'red')
    }

    faces = {
        'K' : 'king',
        'Q' : 'queen',
        'J' : 'jack'
    }

    def __init__(self):
        super().__init__()
        for suit in self.suits:
            card_values = ['A'] + list(range(2,11)) + list(self.faces)
            for i in range(len(card_values)):
                self.add(Card(suit, card_values[i], i))
        self.shuffle()

    def draw(self):
        if self.size() > 0:
            return self.cards.pop()
        return 0


class Foundation(CardCollection):
    """ Class representing the game deck.

    Inherits from the CardCollection class.

    Attributes:
        cards (inherited): a standard list containing all the cards in the collection
        suit: the suit this foundation will contain
    """

    def __init__(self, suit):
        super().__init__()
        self.suit = suit

    def add(self, card):
        if card.get_suit() == self.suit:
            self.cards.append(card)
            return 1
        return 0


class Board:
    """ Class representing the game board

    Attributes:
        deck: deck used in the game
        waste: card collection of the cards drawn from the deck
        foundations: list to store the 4 suit ace-king piles
        tableau: list to represent the main board of the game - 7 piles of cards
    """

    columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

    def __init__(self):
        self.deck = Deck()
        self.waste = CardCollection()
        self.foundations = [CardCollection() for i in range(4)]
        self.tableau = [CardCollection() for i in range(7)]

    def move(self, a, b):
        """ Function to facilitate moving cards to other piles

        Arguments:
            a: location which card(s) are being moved from
            b: location which card(s) are being moved to

        Returns:
            1 or 0 depending on if the move could be done or not

        Examples:
            1. moving cards from tableau pile to another tableau pile: a:'C4', b:'A'
            2. moving cards from foundation pile to tableau pile: a:'*1', b:'C'
            3. moving cards from waste pile to a tableau pile: a:'W', b:'C'
            4. moving cards from waste pile to the foundation pile: a:'W', b:'*'
            5. moving cards from tableau pile to foundation pile: a:'C', b:'*'
        """

        if a[0].upper() in columns and len(a) > 1 and b.upper() in columns:
            "means it's for 1"
        elif a[0] == '*' and len(a) > 1 and b.upper() in columns:
            "means it's for 2"
        elif a.upper() == 'W':
            if b.upper() in columns:
                "means it's for 3"
            elif b == "*":
                "means it's for 4"
        elif a.upper() in columns and b == "*":
            "means it's for 5"



def main():
    pass

if __name__ == '__main__':
    main()
