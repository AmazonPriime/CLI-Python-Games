import os, random

config = {
    'suits' : {
        'diamonds' : '♦',
        'spades' : '♠',
        'hearts' : '♥',
        'clubs' : '♣'
    },
    'special' : {
        'ace' : -1,
        'king' : 10,
        'queen' : 10,
        'jack' : 10
    }
}

'''
Class for Card object
'''
class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{config['suits'][self.suit]} {self.value}"

    def get_suit(self):
        return self.suit

    def get_value(self):
        if self.value in config['special']:
            return config['special'][self.value]
        return self.value

'''
Class for Card Collection objects
'''
class CardCollection:
    def __init__(self):
        self.cards = list()

    def __str__(self):
        if self.cards:
            return ", ".join([f'{card}' for card in self.cards])
        else:
            return "Collection is empty."

    def add(self, card):
        if type(card) == Card:
            self.cards.append(card)
        else:
            print('Card cannot be added to the collection.')

    def remove(self, card):
        if card in self.cards:
            self.cards.remove(card)
        else:
            print('Card is not in the collection and cannot be removed.')

    def shuffle(self):
        random.shuffle(self.cards)

    def size(self):
        return len(self.cards)

'''
Class for Deck object
    inherits from the CardCollection class
'''
class Deck(CardCollection):
    def __init__(self):
        super().__init__()
        for suit in config['suits']:
            for special in config['special']:
                self.add(Card(suit, special))
            for value in range(1, 11):
                self.add(Card(suit, value))

    def draw(self):
        return self.cards.pop()

'''
Class for Hand object
    inherits from the CardCollection class
'''
class Hand(CardCollection):
    def __init__(self):
        super().__init__()

    def hand_value(self):
        total, aces = 0, []
        for card in sorted(self.cards, key = lambda x: x.get_value(), reverse = True):
            if card.get_value() == -1:
                aces.append(card)
            else:
                total += card.get_value()
        for ace in aces:
            if total + 11 <= 21 and len(aces[aces.index(ace) + 1:]) == 1:
                total += 11
            elif total + 11 <= 21:
                total += 11
            else:
                total += 1
        return total

'''
Class for Player object
'''
class Player:
    def __init__(self):
        self.hand = Hand()
        self.bust = False

    def hand_check(self):
        self.bust = True if player.hand.hand_value() > 21 else False
        return player.hand.hand_value()

'''
Class for Dealer object
    inherits from the Player class
'''
class Dealer(Player):
    def __init__(self):
        super().__init__()

    def deal(self, deck, player, quantity = 1):
        for i in range(quantity):
            player.hand.add(deck.draw())

'''
Class for the Game object
'''
class Game:
    def __init__(self):
        self.deck = Deck()
        self.player = Player()
        self.dealer = Dealer()
        self.round = 1

    def setup(self):
        self.deck.shuffle()
        self.dealer.deal(self.deck, self.player, 2)
        self.dealer.deal(self.deck, self.dealer, 2)

    def loop(self):
        pass
