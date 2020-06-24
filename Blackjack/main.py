import os, sys, random

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

commands = {
    'clear' : {
        'win32' : 'cls',
        'cygwin' : 'cls'
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
            for value in range(2, 11):
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
        self.stand = False

    def hand_check(self):
        self.bust = True if self.hand.hand_value() > 21 else False

    def set_stand(self):
        self.stand = True

    def is_standing(self):
        return self.stand

    def is_bust(self):
        return self.bust

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
        self.output = ( f"{' '.join(config['suits'].values())} Blackjack - %%round%%\n"
                        'Current hand (%%hand_value%%): %%player_hand%%\n'
                        'Dealers hand: x%%dealer_hand_size%% cards\n'
                        'Cards in deck: x%%deck_size%%\n')

    def setup(self):
        self.deck.shuffle()
        self.dealer.deal(self.deck, self.player, 2)
        self.dealer.deal(self.deck, self.dealer, 2)

    def update_output(self):
        updated_output = self.output[:]
        context = {
            '%%round%%' : self.round,
            '%%player_hand%%' : self.player.hand,
            '%%hand_value%%' : self.player.hand.hand_value(),
            '%%dealer_hand_size%%' : self.dealer.hand.size(),
            '%%deck_size%%' : self.deck.size()
        }
        for tag, value in context.items():
            updated_output = updated_output.replace(tag, str(value))
        return updated_output

    def display(self):
        os.system(commands['clear'].get(sys.platform, 'clear'))
        print(self.update_output())

    def loop(self):
        # main game loop
        while True:
            self.display()

            # check hands to see if either player or dealer has bust
            self.player.hand_check()
            self.dealer.hand_check()

            if self.player.is_bust() and self.dealer.is_bust():
                print('It is a draw, both you and the dealer have bust.')
                break
            elif self.player.is_bust():
                print('You have bust, you have lost the game.')
                break
            elif self.dealer.is_bust():
                print('The dealer has bust, you have won the game!')
                break

            # check if either player or dealer has blackjack
            if self.player.hand.hand_value() == 21:
                print('You have a blackjack! You win the game!')
                break
            elif self.dealer.hand.hand_value() == 21:
                print('The dealer has a blackjack, you have lost the game.')
                break

            # check if both the player and the dealer are standing
            if self.player.is_standing() and self.dealer.is_standing():
                if self.player.hand.hand_value() > self.dealer.hand.hand_value():
                    print('You have a higher value hand than the dealer! You have won the game!')
                elif self.player.hand.hand_value() < self.dealer.hand.hand_value():
                    print('The dealer has a higher value hand than you, you have lost the game.')
                else:
                    print('It is a draw, both you and the dealer have the same value hand.')
                break

            # dealer will hit unless their hand value is more than or equal to 17
            if self.dealer.hand.hand_value() <= 16:
                self.dealer.deal(self.deck, self.dealer)
            else:
                self.dealer.set_stand()

            # player can input hit or stand - as long as they're not all ready standing
            if not self.player.is_standing():
                move = input('- What would you like to do? (\'hit\' or \'stand\'): ')
                if move.lower() == 'hit':
                    self.dealer.deal(self.deck, self.player)
                elif move.lower() == 'stand':
                    self.player.set_stand()

            # incremenet the round value
            self.round += 1

def main():
    game = Game()
    game.setup()
    game.loop()

if __name__ == '__main__':
    main()
