# import and initialise colorama so the ANSI colour codes are handled for Windows
from colorama import init
init()

import os, sys, random

print("""
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
""")

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
        if type(card) == Card:
            self.cards.append(card)
        else:
            print('Card cannot be added to the collection, must be of type Card.')

    def remove(self, card):
        if card in self.cards:
            self.cards.remove(card)
        else:
            print('Card is not in the collection and cannot be removed.')



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
        elif isinstance(collection, CardCollection):
            for card in collection.get_cards():
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
        return self.cards.pop()


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

    def tableau_merge(self, collection_a, collection_b, index):
        # create a new collection and add the cards to it from location A
        temp_collection = CardCollection()
        temp_collection.merge(collection_a.get_cards()[index:])
        # remove the cards in the new collection from the location A collection
        for card in temp_collection.get_cards():
            collection_a.remove(card)
        # merge new collection and location B collections together
        collection_b.merge(temp_collection)

    def tableau_arg_check(self, arg):
        # if the locations are invalid then do nothing
        if not arg[0].upper() in self.columns:
            return -1
        # if row is either not a number or is less than 1 then do nothing
        try:
            int(arg[1:])
            if int(arg[1:]) < 1:
                return -1
        except:
            return -1
        # if the location row number is out of bounds then do nothing
        if int(arg[1:]) > self.tableau[self.columns.index(arg[0].upper())].size():
            return -1
        return 1

    def move(self, *args):
        """ Function to facilitate moving cards to other piles

        Arguments:
            *args: depending on which action number of arguments may vary, check examples below

        Examples:
            ✓ moving cards from tableau pile to another tableau pile: a:'C4', b:'A'
            ✗ moving cards from foundation pile to tableau pile: a:'FP1', b:'C'
            ✗ moving cards from waste pile to a tableau pile: a:'W', 'C'
            ✗ moving cards from tableau pile to foundation pile: a:'C', b:'FP'
        """

        # check which of the types of moves is being performed
        if len(args) == 2:
            # the case that tableau to tableau
            if len(args[0]) >= 2 and len(args[1]) == 1:
                a, b = args[0], args[1]
                # if the locations are invalid then do nothing
                if not b.upper() in self.columns:
                    return -1
                # check argument for the tableau location
                if tableau_arg_check(self, a) == -1:
                    return
                # create the collection reference variables
                collection_a = self.tableau[self.columns.index(a[0].upper())]
                a_index = int(a[1:] - 1)
                collection_b = self.tableau[self.columns.index(b.upper())]
            elif len(args[0]) == 3 and len(args[1]) == 2:
                # turn the top card of the foundation into collection a and collection b being the tableau pile
                try:
                    int(args[0][-1])
                    if int(args[0][-1]) < 1 or int(args[0][-1]) > 4:
                        return
                except:
                    return
                # if the foundation pile is empty do nothing
                if self.foundation[int(args[0][-1])].size() == 0:
                    return
                # check argument for the tableau location
                if tableau_arg_check(self, a) == -1:
                    return
                # create the collection reference variables
                collection_a = CardCollection()
                collection_a.add(self.foundation[int(args[0][-1])].get_card(-1))
                a_index = 0
            else:
                return
        elif len(args) == 1:
            pass
        else:
            return



        ######### above make sure collection a and b are defined




        # if first card in the cards being moved isn't shown (faced up) then do nothing
        card_a = collection_a.get_card(a_index)
        if not collection_a.get_card(a_index).is_shown():
            return

        # if the collection at location B has cards then handle it appropiately
        if collection_b.size() > 0:
            card_b = collection_b.get_card(-1)
            # if the suits don't alternate in colour between card in location A and B then do nothing
            if card_a.get_suit().get_colour() == card_b.get_suit().get_colour():
                return
            # if rank of card on end of collection at location B is exactly 1 higher then move cards over
            if (card_b.get_rank() - 1) == card_a.get_rank():
                # merge the two collections together
                tableau_merge(collection_a, collection_b, a_index)
            else:
                return
        # if the card A value is King then move the partial collection over
        elif card_a.get_value() == 'K':
            # merge the two collections together
            tableau_merge(collection_a, collection_b, a_index)
        else:
            return



def main():
    """ Main function of the program bringing all the code together
    """


if __name__ == '__main__':
    main()
