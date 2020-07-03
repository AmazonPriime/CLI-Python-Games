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
        # if there are cards in the collection then return the string version of the final card
        if self.size() > 0:
            return str(self.get_card(-1))
        else:
            return 'E'

    def add(self, card):
        # if the item being added is a card then add it to the collection
        if isinstance(card, Card):
            self.cards.append(card)
            return 1
        return 0

    def remove(self, card):
        # if the card is in the collection then remove it
        if card in self.cards:
            self.cards.remove(card)
            return 1
        return 0

    def get_cards(self):
        return self.cards

    def get_card(self, index):
        # if the index provided is less than the number of cards, that there are cards in the collection and index is more or equal than -1 then return the card
        if self.size() > index and self.size() > 0 and index >= -1:
            return self.cards[index]
        else:
            return 0

    def check_index(self, card_index):
        # checks to make sure the index is valid
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
    To draw a card type 'draw' or 'dd'.
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
        # adds cards to the tableau increasing by 1 for each pile and setting last card in each pile to shown
        for i in range(7):
            for j in range(i + 1):
                card = self.deck.draw()
                self.tableau[i].add(card)
                if i == j:
                    card.set_shown()

    def draw(self):
        # if there are cards in the deck then draw a card and add it to waste pile
        if self.deck.size() > 0:
            card = self.deck.draw()
            self.waste.add(card)
            card.set_shown()
        # otherwise recycle the cards in the waste pile
        else:
            for card in self.waste.get_cards()[::-1]:
                self.waste.remove(card)
                self.deck.add(card)
        # if the deck has cards and wast does not then call the function again
        if self.waste.size() == 0 and self.deck.size() != 0:
            self.draw()

    def get_foundation(self, card):
        # finds the foundation the card belongs to
        collection_b = 0
        for foundation in self.foundations:
            if foundation.get_suit() == card.get_suit():
                return foundation

    def foundation_ace(self, collection_a, collection_b, card):
        # if the collection b has no cards then it must be an ace to be moved over
        if collection_b.size() == 0:
            if card.get_rank() != 0:
                return -1
            collection_a.remove(card)
            collection_b.add(card)
            next_card = collection_a.get_card(-1)
            if isinstance(next_card, Card):
                next_card.set_shown()
            return 1

    def last_card_shown(card):
        # if the card is a card then make it set to being shown
        if isinstance(next_card, Card):
            next_card.set_shown()

    def move_cards(collection_a, collection_b, cards):
        # loops through the cards to be moved and removes them from collection a and adds to collection b
        for card in cards_moving:
            collection_a.remove(card)
            collection_b.add(card)

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

        # checks for the first example - tableau to tableau
        if a[0].upper() in self.columns and len(a) > 1 and b.upper() in self.columns:
            # store each collection for easier referencing
            collection_a = self.tableau[self.columns.index(a[0].upper())]
            collection_b = self.tableau[self.columns.index(b.upper())]
            # if the index is not valid then cancel and return number representing invalid move
            if not collection_a.check_index(int(a[1:]) - 1):
                return -1
            # if the card being moved is not shown then return number representing invalid move
            a_index = int(a[1:]) - 1
            if not collection_a.get_card(a_index).is_shown():
                return -1

        # checks for the second example - foundation to tableau
        elif a[0] == '*' and len(a) == 2 and b.upper() in self.columns:
            # make sure that the number given is a number and is 1-4 otherwise return number representing invalid move
            try:
                index = int(a[1])
                if index < 1 or index > 4:
                    return -1
            except:
                return -1
            # store each collection for easier referencing
            collection_a = self.foundations[index - 1]
            collection_b = self.tableau[self.columns.index(b.upper())]
            a_index = -1

        # check for the third and fourth examples - moving from the waste pile
        elif a.upper() == 'W':
            # make sure the waste has cards otherwise return number representing invalid move
            if self.waste.size() == 0:
                return -1
            # store each collection for easier referencing
            collection_a = self.waste
            a_index = -1

            # check where collection b will come from the tableau
            if b.upper() in self.columns:
                collection_b = self.tableau[self.columns.index(b.upper())]

            # check if collection b will come from the foundation
            elif b == "*":
                # store the card being moved and also get store reference to the correct foundation
                card = collection_a.get_card(a_index)
                collection_b = self.get_foundation(card)
                # if the collection cannot be found then return invalid command error
                if collection_b == 0:
                    return -1
                # check if foundation is empty and if so make sure the card is ace and move it over
                result = self.foundation_ace(collection_a, collection_b, card)
                if result == -1:
                    return -1
                elif result == 1:
                    return 1
            else:
                return -1

        # check for fifth example - moving from column to the foundation
        elif a.upper() in self.columns and b == "*":
            # store the first collection for referencing and index for last card
            collection_a = self.tableau[self.columns.index(a.upper())]
            a_index = -1
            # if the collection is empty then show invalid command error
            if collection_a.size() == 0:
                return -1
            # store the card being moved and also get store reference to the correct foundation
            card = collection_a.get_card(a_index)
            collection_b = self.get_foundation(card)
            # if the collection cannot be found then return invalid command error
            if collection_b == 0:
                return 0
            # check if foundation is empty and if so make sure the card is ace and move it over
            result = self.foundation_ace(collection_a, collection_b, card)
            if result == -1:
                return -1
            elif result == 1:
                return 1
        else:
            return -1

        # store a list of the card(s) to be moved and also take note of the first card for easier referencing
        cards_moving = collection_a.get_cards()[a_index:]
        first_card = cards_moving[0]

        # if the destination collection is empty then make sure the first card being moved is a king
        if collection_b.size() == 0:
            # checks if card is a king
            if first_card.get_rank() == 12:
                # moves the cards over
                self.move_cards(collection_a, collection_b, cards_moving)
                # makes the card at end of old collection be visible/shown
                self.last_card_shown(collection_a.get_card(-1))
            else:
                return 0

        # if the card being mved is 1 rank less than the end card of the destination collection
        if collection_b.get_card(-1).get_rank() - 1 == first_card.get_rank():
            # if the destination collection is a foundation
            if isinstance(collection_b, Foundation):
                # if card is being sent to the correct foundation then move the card over
                if first_card.get_suit() == collection_b.get_suit():
                    self.move_cards(collection_a, collection_b, cards_moving)
                    # makes the card at end of old collection be visible/shown
                    self.last_card_shown(collection_a.get_card(-1))

            # if card is being sent to a tableau pile
            else:
                # if the card alternates in colour the move the card(s) over
                if first_card.get_suit().get_colour() != collection_b.get_card(-1).get_suit().get_colour():
                    # move the cards over
                    self.move_cards(collection_a, collection_b, cards_moving)
                    # makes the card at end of old collection be visible/shown
                    self.last_card_shown(collection_a.get_card(-1))

        # if the destination is a foundation and the card being moved is one rank higher than destination
        elif isinstance(collection_b, Foundation) and first_card.get_rank() - 1 == collection_b.get_card(-1).get_rank():
            # move the card over
            self.move_cards(collection_a, collection_b, cards_moving)
            # makes the card at end of old collection be visible/shown
            self.last_card_shown(collection_a.get_card(-1))

        # return 0 if nothing can be done to display invalid move error message to user
        else:
            return 0

    def set_message(self, message):
        self.message = message

    def display(self, username, score):
        # clear the terminal for the user
        Game.clear()
        # setup basic lines to be printed to output
        horizontal_rule = '--------------------------------\n'
        top = f' {username} {score} '.center(len(horizontal_rule) - 1, '-') + '\n'
        title = ' Python Klondike '.center(len(horizontal_rule) - 1, '-') + '\n'
        deck_foundation = f'{self.deck}->[{self.waste}] | {{{self.foundations[0]}}} {{{self.foundations[1]}}} {{{self.foundations[2]}}} {{{self.foundations[3]}}}\n'
        column_letters = '    ' + '   '.join(self.columns) + '\n'
        # concatinate each of the lines to an output variable
        output = top + title + deck_foundation + horizontal_rule + column_letters
        # find out which of the tableau's are the largest and use to to determine how many rows there will be
        rows = max([collection.size() for collection in self.tableau])
        for i in range(rows):
            # concatinate the row number
            output += f'{i + 1}.'.ljust(3, ' ')
            for collection in self.tableau:
                # get the card if there is one
                card = collection.get_card(i)
                # if there is a card then concatinate it in a specific style with spaces following it
                if card:
                    if card.is_shown():
                        output += str(card) + ' ' * (3 - len(str(card.get_value())))
                    else:
                        output += str(card) + '  '
                # when there is not a card just append spaces
                else:
                    output += ' ' * 4
            # append a newline after each row is concatinated
            output += '\n'
        # concatinate a line and the message to be displayed to the user then print it out
        output += horizontal_rule + self.message + '\n'
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

    def clear():
        # checks the platform and if windows uses 'cls' command otherwise 'clear' command
        if sys.platform == 'win32':
            os.system('cls')
        else:
            os.system('clear')

    def help(self):
        # clears the terminal and prints out the help message
        Game.clear()
        print(Board.help)
        input('Type anything and press enter to continue.')

    def start(self):
        # sets up the board by dealing out to the tableau piles
        self.board.setup()
        # sets up infinite loop which can only be broken when users issues the quit command, an error occurs or the game is won
        while True:
            # prints out the display
            self.board.display(self.username, self.score)
            # takes in the user input
            user_input = input('Enter Move: ')
            # if the user issues the help command then a help message is displayed to them
            if user_input.lower() == 'help':
                self.help()
            # if the users issues the quit command then the game stops
            elif user_input.lower() == 'quit':
                print('Thanks for playing.')
                break
            # if the user isses the draw or dd command then a card is drawn and added to the waste pile
            elif user_input.lower() == 'draw' or user_input.lower() == 'dd':
                self.board.draw()
            # if there are two arguments it's possible the user wants to move, so we issue the move command
            elif len(user_input.split()) == 2:
                a, b = user_input.split()
                result = self.board.move(a, b)
                # based on the output then update the board message appropiately -1 invalid command, 0 invalid move, anything else is a valid move
                if result == -1:
                    self.board.set_message('Invalid command type \'help\' to see a list of commands.')
                elif result == 0:
                    self.board.set_message('Move could not be done as it\'s an invalid move.')
                else:
                    self.board.set_message('Nice move! Remember if you need help to type \'help\'')
            # if no valid command is entered then set the board message to reflect it
            else:
                self.board.set_message('Unknown command type \'help\' to see a list of commands.')
            # checking for win conditions
            done = True
            # if any of the foundations do not contain a king on top then set done to False and game loop continues
            for foundation in self.board.foundations:
                if foundation.size() > 0:
                    if foundation.get_card(-1).get_rank() != 12:
                        done = False
                        break
                else:
                    done = False
                    break
            # if the deck and waste are empty then check for any cards which are not shwon if all cards are shown the game is finished and won
            if self.board.deck.size() == 0 and self.board.waste.size() == 0:
                for collection in self.board.tableau:
                    for card in collection.get_cards():
                        if card.is_shown():
                            done = False
                            break
            # if done variable is true, means the player has won the game
            if done:
                print('Congratulations you have won the game!')
                break


def main():
    # take in the players username
    username = input('Please enter a username: ')
    # create the game object
    game = Game(username)
    # start the game
    game.start()


if __name__ == '__main__':
    main()
