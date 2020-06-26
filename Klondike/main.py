# import and initialise colorama so the ANSI colour codes are handled for Windows
from colorama import init
init()

import os, sys, random

"""
Python Klondike ---------------
(D)->[2♥] | {♣} {♥} {♠} {♦}
-------------------------------
   A   B   C   D   E   F   G
1  J♦  []  []  []  []  []  []
2      8♥  []  []  []  []  []
3          7♠  []  []  []  []
4              2♥  []  []  []
5                  J♠  []  []
6                      Q♦  []
7                          A♦
...
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


class CardCollection:
    """ Class representing a collection of cards.

    The collection will initially be empty, cannot be populated during instanitation.

    Attributes:
        cards: a standard list containing all the cards in the collection
    """

    def __init__(self):
        self.cards = list()

    def add(self, card):
        if type(card) == Card:
            self.cards.append(card)
        else:
            print('Card cannot be added to the collection, must be of type Card.')

    def remove(self, card):
        if card in self.cards:
            self.cards.remove(card)
        else:
            print('Card is not in the collection and cannot be removed.')

    def merge(self, collection):
        for card in collection:
            self.add(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def size(self):
        return len(self.cards)


class Deck(CardCollection):
    """ Class representing the game deck.

    Inherits from the CardCollection class.

    Attributes:
        suits (class): dictionary containing all the suits and details about them
        cards (inherited): a standard list containing all the cards in the collection
    """

    suits = {
        'clubs' : Suit('clubs', '♣', 'black'),
        'spades' : Suit('spades', '♠', 'black'),
        'hearts' : Suit('hearts', '♥', 'red'),
        'diamonds' : Suit('diamonds', '♦', 'red')
    }

    def __init__(self):
        super().__init__()
        for suit in self.suits:
            card_values = list(range(2,11)) + ['A', 'J', 'Q', 'K']
            for i in range(len(card_values)):
                self.add(Card(suit, card_values[i], i))
        self.shuffle()


class Board:
    """ Class representing the game board

    Attributes:
        deck: deck used in the game
        waste: card collection of the cards drawn from the deck
        foundations: list to store the 4 suit ace-king piles
        tableau: list to represent the main board of the game - 7 piles of cards
    """

    def __init__(self):
        self.deck = Deck()
        self.waste = CardCollection()
        self.foundations = [CardCollection() for i in range(4)]
        self.tableau = [CardCollection() for i in range(7)]

    def move(self, a, b):
        """ Function to facilitate moving cards to other piles

        Arguments:
            a: the card(s) which are being moved - 'C4'
            b: location cards are being moved to - 'A'
        """
        pass


def main():
    """ Main function of the program bringing all the code together
    """


if __name__ == '__main__':
    main()
