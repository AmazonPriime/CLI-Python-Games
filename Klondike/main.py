# import and initialise colorama so the ANSI colour codes are handled for Windows
from colorama import init
init()

import os, sys, random, datetime

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
            return f"{self.ansi_codes[self.suit.get_colour()]}{self.value}{self.suit}{self.ansi_codes['reset']}"
        else:
            return '[]'

    def get_value(self):
        return self.value

    def get_rank(self):
        return self.rank

    def get_suit(self):
        return self.suit

    def set_shown(self):
        self.shown = True

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

    def __str__(self):
        if self.size() > 0:
            return str(self.get_card(-1))
        else:
            return 'E'

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
        if self.size() > index and self.size() > 0:
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

    def check_index(self, card_index):
        try:
            index = int(card_index)
            if index >= 0:
                self.cards[int(card_index)]
            else:
                return 0
            return 1
        except:
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
        'J' : 'jack',
        'Q' : 'queen',
        'K' : 'king',
    }

    def __init__(self):
        super().__init__()
        for suit in self.suits.values():
            card_values = ['A'] + list(range(2,11)) + list(self.faces)
            for i in range(len(card_values)):
                self.add(Card(suit, card_values[i], i))
        self.shuffle()

    def __str__(self):
        if self.size() > 0:
            return f'({self.size()})'
        else:
            return '(E)'

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

    def __str__(self):
        if self.size() > 0:
            return str(self.get_card(-1))
        else:
            return f'{Card.ansi_codes[self.suit.get_colour()]}{self.suit}{Card.ansi_codes["reset"]}'

    def add(self, card):
        if card.get_suit() == self.suit:
            self.cards.append(card)
            return 1
        return 0

    def get_suit(self):
        return self.suit


class Board:
    """ Class representing the game board

    Attributes:
        deck: deck used in the game
        waste: card collection of the cards drawn from the deck
        foundations: list to store the 4 suit ace-king piles
        tableau: list to represent the main board of the game - 7 piles of cards
    """

    columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

    help = '''Commands:
    To draw a card type 'draw'.
    To move cards between tableau piles type '[A-G]{row number} [A-G]'.
    To move cards from waste pile to the tableau type 'W [A-G]'.
    To move cards from foundation pile to the tableau type '*{1-4} [A-G]'. (numbers are left-right)
    To move cards from tableau pile to foundation type '[A-G] *'.
    To move cards from waste pile to foundation type 'W *'.
    To exit the game type 'quit'.
    '''

    def __init__(self):
        self.deck = Deck()
        self.waste = CardCollection()
        self.foundations = [Foundation(suit) for suit in Deck.suits.values()]
        self.tableau = [CardCollection() for i in range(7)]
        self.message = 'Type \'help\' for a list of commands.'

    def setup(self):
        # setup the tableau piles by drawing from the deck and change the last card of each draw to be shown
        for i in range(7):
            for j in range(i + 1):
                card = self.deck.draw()
                self.tableau[i].add(card)
                if i == j:
                    card.set_shown()

    def draw(self):
        # if the deck has cards in it we draw the card and add to waste pile
        if self.deck.size() > 0:
            card = self.deck.draw()
            self.waste.add(card)
            card.set_shown()
        # if there are no cards in the deck then we recycle the waste
        else:
            for card in self.waste.get_cards()[::-1]:
                self.waste.remove(card)
                self.deck.add(card)

    def get_foundation(self, card):
        collection_b = 0
        for foundation in self.foundations:
            if foundation.get_suit() == card.get_suit():
                collection_b = foundation
                break
        return collection_b

    def move(self, a, b):
        """ Function to facilitate moving cards to other piles

        Arguments:
            a: location which card(s) are being moved from
            b: location which card(s) are being moved to

        Returns:
            -1: if the arguments are invalid
            0: if the move cannot be done
            1: if the move was successful

        Examples:
            1. moving cards from tableau pile to another tableau pile: a:'C4', b:'A'
            2. moving cards from foundation pile to tableau pile: a:'*1', b:'C'
            3. moving cards from waste pile to a tableau pile: a:'W', b:'C'
            4. moving cards from waste pile to the foundation pile: a:'W', b:'*'
            5. moving cards from tableau pile to foundation pile: a:'C', b:'*'
        """

        # check which of the different move commands is being issued
        if a[0].upper() in self.columns and len(a) > 1 and b.upper() in self.columns:
            "checks for example 1"
            # assign each collection to a variable for easier referencing
            collection_a = self.tableau[self.columns.index(a[0].upper())]
            collection_b = self.tableau[self.columns.index(b.upper())]
            # check that the index in arg a is valid
            if not collection_a.check_index(int(a[1:]) - 1):
                return -1
            # make sure the card is shown
            a_index = int(a[1:]) - 1
            if not collection_a.get_card(a_index).is_shown():
                return -1

        elif a[0] == '*' and len(a) == 2 and b.upper() in self.columns:
            "checks for example 2"
            try:
                index = int(a[1])
                if index < 1 or index > 4:
                    return -1
            except:
                return -1
            # assign each collection to a variable for easier referencing and -1 index for last card
            collection_a = self.foundations[index - 1]
            collection_b = self.tableau[self.columns.index(b.upper())]
            a_index = -1

        elif a.upper() == 'W':
            # make sure the waste pile has cards
            if self.waste.size() == 0:
                return -1
            # assign collection a and -1 index for last card
            collection_a = self.waste
            a_index = -1
            if b.upper() in self.columns:
                "checks for example 3"
                # assign collection b
                collection_b = self.tableau[self.columns.index(b.upper())]

            elif b == "*":
                "checks for example 4"
                # get card for checks and assign collection b to the correct foundation
                card = collection_a.get_card(a_index)
                collection_b = self.get_foundation(card)
                # make sure a valid foundation was found
                if collection_b == 0:
                    return -1
                # if foundation has no cards ensure the card being moved is an ace
                if collection_b.size() == 0:
                    if card.get_rank() != 0:
                        return -1
                    # handle the moving on an ace here
                    collection_a.remove(card)
                    collection_b.add(card)
                    next_card = collection_a.get_card(-1)
                    if isinstance(next_card, Card):
                        next_card.set_shown()
                    return 1

        elif a.upper() in self.columns and b == "*":
            "checks for example 5"
            # assign collection a and -1 index for last card
            collection_a = self.tableau[self.columns.index(a.upper())]
            a_index = -1
            if collection_a.size() == 0:
                return -1
            # get card for checks and assign collection b to the correct foundation
            card = collection_a.get_card(a_index)
            collection_b = self.get_foundation(card)
            # make sure a valid foundation was found
            if collection_b == 0:
                return 0
            # if foundation has no cards ensure the card being moved is an ace
            if collection_b.size() == 0:
                if card.get_rank() != 0:
                    return -1
                # handle the moving on an ace here
                collection_a.remove(card)
                collection_b.add(card)
                next_card = collection_a.get_card(-1)
                if isinstance(next_card, Card):
                    next_card.set_shown()
                return 1
        else:
            return -1

        # cards to be moved from collection_a and the first card in the collection for easier referencing
        cards_moving = collection_a.get_cards()[a_index:]
        first_card = cards_moving[0]

        # if collection b is empty then the first card being moved must be a king
        if collection_b.size() == 0:
            if first_card.get_rank() == 12:
                for card in cards_moving:
                    collection_a.remove(card)
                    collection_b.add(card)
                next_card = collection_a.get_card(-1)
                if isinstance(next_card, Card):
                    next_card.set_shown()
            else:
                return 0

        if collection_b.get_card(-1).get_rank() - 1 == first_card.get_rank():
            if isinstance(collection_b, Foundation):
                if first_card.get_suit() == collection_b.get_suit():
                    collection_a.remove(first_card)
                    collection_b.add(first_card)
                    next_card = collection_a.get_card(-1)
                    if isinstance(next_card, Card):
                        next_card.set_shown()
            else:
                if first_card.get_suit().get_colour() != collection_b.get_card(-1).get_suit().get_colour():
                    for card in cards_moving:
                        collection_a.remove(card)
                        collection_b.add(card)
                    next_card = collection_a.get_card(-1)
                    if isinstance(next_card, Card):
                        next_card.set_shown()
        elif isinstance(collection_b, Foundation) and first_card.get_rank() - 1 == collection_b.get_card(-1).get_rank():
            collection_a.remove(card)
            collection_b.add(card)
            next_card = collection_a.get_card(-1)
            if isinstance(next_card, Card):
                next_card.set_shown()
        else:
            return 0

    def set_message(self, message):
        self.message = message

    def display(self, username, score):
        # run the correct terminal clear command
        if sys.platform == 'win32':
            os.system('cls')
        else:
            os.system('clear')
        # start to build the output for this cycle
        horizontal_rule = '--------------------------------\n'
        top = f' {username} {score} '.center(len(horizontal_rule) - 1, '-') + '\n'
        title = ' Python Klondike '.center(len(horizontal_rule) - 1, '-') + '\n'
        deck_foundation = f'{self.deck}->[{self.waste}] | {{{self.foundations[0]}}} {{{self.foundations[1]}}} {{{self.foundations[2]}}} {{{self.foundations[3]}}}\n'
        # build the output without the actual board
        output = top + title + deck_foundation + horizontal_rule
        # process of building the board from the different tableau piles
        column_letters = '    ' + '   '.join(self.columns) + '\n'
        output += column_letters
        # find out which pile has the highest number of cards and store that value
        rows = max([collection.size() for collection in self.tableau])
        # loop through n times based on how many rows adding each card from each pile if there is one to output
        for i in range(rows):
            output += f'{i + 1}.'.ljust(3, ' ')
            for collection in self.tableau:
                card = collection.get_card(i)
                if card:
                    if card.is_shown():
                        output += str(card) + ' ' * (3 - len(str(card.get_value())))
                    else:
                        output += str(card) + '  '
                else:
                    output += ' ' * 4

            output += '\n'
        output += horizontal_rule
        output += self.message + '\n'
        print(output)


class Game:
    """ Class representing the game itself

    Attributes:
        board: the board with all the different piles of cards
        score: the players score during the game
        start_time: the time the game was initialised
        username: the user who is playing
    """

    def __init__(self, username):
        self.board = Board()
        self.score = 0
        self.start_time = datetime.datetime.now().time()
        self.username = username

    def help(self):
        # run the correct terminal clear command
        if sys.platform == 'win32':
            os.system('cls')
        else:
            os.system('clear')
        print(Board.help)
        input('Type anything and press enter to continue.')

    def start(self):
        self.board.setup()
        while True:
            self.board.display(self.username, self.score)
            user_input = input('Enter Move: ')
            if user_input.lower() == 'help':
                self.help()
            elif user_input.lower() == 'quit':
                print('Thanks for playing.')
                break
            elif user_input.lower() == 'draw':
                self.board.draw()
            elif len(user_input.split()) == 2:
                a, b = user_input.split()
                result = self.board.move(a, b)
                if result == -1:
                    self.board.set_message('Invalid command type \'help\' to see a list of commands.')
                elif result == 0:
                    self.board.set_message('Move could not be done as it\'s an invalid move.')
                else:
                    self.board.set_message('Nice move! Remember if you need help to type \'help\'')
            else:
                self.board.set_message('Unknown command type \'help\' to see a list of commands.')
            # game is over when all the top cards in foundation pile are kings (cards ranked 12)
            done = True
            for foundation in self.board.foundations:
                if foundation.size() > 0:
                    if foundation.get_card(-1).get_rank() != 12:
                        done = False
                        break
                else:
                    done = False
                    break
            # if the game is finished then break the loop and print a congratulatory message
            if done:
                print('Congratulations you have won the game!')
                break

def main():
    username = input('Please enter a username: ')
    game = Game(username)
    game.start()

if __name__ == '__main__':
    main()
