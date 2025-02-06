import random
import os


def clear():
    os.system('cls')


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# ------------------------- creating deck --------------------------
class Card:
    def __init__(self, num, suit):
        self.number = num
        self.suit = suit

    def get_info(self):
        return self.number, self.suit


class Deck:
    def __init__(self):
        suit_list = ['Spades', 'Clubs', 'Hearts', 'Diamonds']
        num_list = ['Ace', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King']
        temp_list = []
        for suit in suit_list:
            for num in num_list:
                temp_list.append(Card(num, suit))
        self.card_list = temp_list.copy()

    def get_deck(self):
        return self.card_list

    def draw_card(self):
        index = random.randint(0, len(self.card_list) - 1)
        ret = self.card_list[index]
        self.card_list.pop(index)
        return ret


# --------------------------- logic for game ------------------------------
def value(hand):
    value_ = 0
    ace = 0
    soft_ = False
    for card in hand:
        num, suit = card.get_info()
        if num in ['Ace', 'Jack', 'Queen', 'King']:
            if num == 'Ace':
                ace += 1
            else:
                value_ += 10
        else:
            value_ += num

    while ace > 0:
        if value_ <= 10:
            value_ += 11
            soft_ = True
        else:
            value_ += 1
        ace -= 1

    return value_, soft_


def print_hand(hand, first):
    for card in hand:
        num, suit = card.get_info()
        print(f'{num} of {suit}')

    p_value, soft = value(hand)

    if value == 21 and first:
        print(Bcolors.BOLD + f'\nTotal Value: {p_value}\nBlackJack!' + Bcolors.ENDC)
        win()
    elif soft:
        print(Bcolors.BOLD + f'\nTotal Value: Soft {p_value}' + Bcolors.ENDC)
    else:
        print(Bcolors.BOLD + f'\nTotal Value: {p_value}' + Bcolors.ENDC)


def dealer_draw(deck, hand):
    card = deck.draw_card()
    hand.append(card)


def stand(deck, hand, bj=False, bust=False):
    # BlackJack = automatic win!
    if bj:
        print('Congratulations! \nYou have Won!')
        return True

    dealer_hand = []

    if bust:
        dealer_draw(deck, dealer_hand)
        dealer_draw(deck, dealer_hand)
        return dealer_hand

    # Play against dealer
    dealer_draw(deck, dealer_hand)
    dealer_draw(deck, dealer_hand)

    while value(dealer_hand)[0] < 17:
        dealer_draw(deck, dealer_hand)

    return dealer_hand


def hit(hand, deck):
    card = deck.draw_card()
    hand.append(card)
    if value(hand)[0] > 21:
        d_hand = stand(deck, hand, bust=True)
        end(d_hand, hand)
    else:
        print_hand(hand, False)


def end(dealer_hand, user_hand):
    dealer_value = value(dealer_hand)
    user_value = value(user_hand)

    print(Bcolors.OKBLUE + Bcolors.UNDERLINE + f'\nYour Hand:' + Bcolors.ENDC)
    print_hand(user_hand, False)
    print(Bcolors.OKCYAN + Bcolors.UNDERLINE + f'\nDealer Hand:' + Bcolors.ENDC)
    print_hand(dealer_hand, False)

    print()
    if value(user_hand)[0] > 21:
        print(Bcolors.FAIL + 'You Bust. Better Luck Next Time.' + Bcolors.ENDC)
    # loose
    elif user_value[0] < dealer_value[0] <= 21:
        print(Bcolors.FAIL + 'You Loose. \nBetter Luck Next Time.' + Bcolors.ENDC)
    # win
    elif dealer_value[0] < user_value[0] or dealer_value[0] > 21:
        print(Bcolors.OKGREEN + 'You Win!' + Bcolors.ENDC)
    # tie
    else:
        print('Tie! You Should Play Again.')

    print()


def play_game():
    # creating deck and hand
    current_deck = Deck()
    current_hand = []

    # drawing first two cards
    card = current_deck.draw_card()
    current_hand.append(card)
    card = current_deck.draw_card()
    current_hand.append(card)

    # print hand
    print_hand(current_hand, True)

    # check for BlackJack
    if value(current_hand) == 21:
        stand(current_deck, current_hand, bj=True)

    # hit or stand?
    while True and value(current_hand)[0] <= 21:
        hs = input('type \"hit\" to hit or \"stand\" to stand \n> ')
        if hs.lower() in ['hit', 'h']:
            clear()
            hit(current_hand, current_deck)
        elif hs.lower() in ['stand', 's']:
            clear()
            d_hand = stand(current_deck, current_hand)
            end(d_hand, current_hand)
            break
        else:
            print(Bcolors.WARNING + 'ERROR: unknown input\n' + Bcolors.ENDC)


# --------------------------- User Interface ------------------------------
if __name__ == '__main__':
    print('Welcome to BlackJack!')

    loop = True
    while loop:
        start = input('Type \"ready\" to begin or \"q\" to quit\n> ')
        if start.lower() in ['ready', 'r']:
            clear()
            print('Alright. Lets begun!\n')
            play_game()
        elif start.lower() == 'q':
            loop = False
        else:
            print(Bcolors.WARNING + 'ERROR: unknown input\n' + Bcolors.ENDC)

    print('\nThanks for playing!\n'
          'I hope to see you again.')
