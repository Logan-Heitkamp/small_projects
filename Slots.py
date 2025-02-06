import random
import secrets
from time import sleep
import os


def clear(): os.system('cls')


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


class Wheel:
    def __init__(self):
        self.faces = ['!', '@', '#', '$', '%', '^', '&', '*', '=', '+']
        self.done = False
        self.rng = secrets.SystemRandom()

    def spin(self):
        self.faces = self.faces[-1:] + self.faces[:-1]

    def randomize(self):
        move = self.rng.randrange(1, 10)
        self.faces = self.faces[move:] + self.faces[:move]
        self.rng = .SystemRandom()


class Machine:
    def __init__(self):
        self.wheels = [Wheel() for _ in range(3)]
        for w in self.wheels:
            w.randomize()
        self.display = []
        self.update_display()

    def spin(self):
        for w in self.wheels:
            if not w.done:
                w.spin()
                w.randomize()
        self.update_display()
        self.show()

    def run(self, b) -> int:
        for i in range(3):
            for j in range(15):
                self.spin()
                sleep(0.01)
            self.wheels[i].done = True

        for w in self.wheels:
            w.done = False

        return self.calc_win(b)

    def calc_win(self, b) -> int:
        result = self.display[1]
        for char in result:
            count = result.count(char)
            if count == 2:
                self.show_result(b * 2)
                return b * 2
            elif count == 3:
                self.show_result(b * 10)
                return b * 10
        self.show_result(0)
        return 0

    def update_display(self):
        self.display = []
        for i in range(3):
            temp = []
            for j in range(3):
                temp.append(self.wheels[j].faces[i])
            self.display.append(temp)

    def show(self, r=None):
        clear()

        if r == 'l':
            for idx, line in enumerate(self.display):
                for char in line:
                    print(Bcolors.BOLD + Bcolors.FAIL + char + Bcolors.ENDC, end='')
                print()

        elif r == 'w':
            for idx, line in enumerate(self.display):
                for char in line:
                    print(Bcolors.BOLD + Bcolors.OKGREEN + char + Bcolors.ENDC, end='')
                print()

        else:
            for idx, line in enumerate(self.display):
                for char in line:
                    if idx == 1:
                        print(Bcolors.BOLD + Bcolors.OKCYAN + char + Bcolors.ENDC, end='')
                    else:
                        print(Bcolors.BOLD + char + Bcolors.ENDC, end='')
                print()

    def show_result(self, w):
        if w == 0:
            self.show('l')
            print(Bcolors.FAIL + 'You Loose. \nBetter Luck Next Time.' + Bcolors.ENDC)
        else:
            self.show('w')
            print(Bcolors.OKGREEN + f'You have won ${w}!' + Bcolors.ENDC)


class Player:
    def __init__(self):
        self.bank = 1000
        self.debt = 0

    def pay(self, a) -> int:
        if self.bank == 0:
            clear()
            print(Bcolors.FAIL + 'You are out of money :( \nBalance: $0' + Bcolors.ENDC)
            return 0
        elif a > self.bank:
            return 1
        elif a < 0:
            return 1
        else:
            self.bank -= a
            return 2


main_machine = Machine()

# --------------------------- User Interface ------------------------------
if __name__ == '__main__':

    main_player = Player()

    print('Welcome to Slots!')

    loop = True
    while loop:
        start = input('Type \"ready\" to begin, \"q\" to quit, or \"balance\" to see your balance\n> ')
        if start.lower() in ['ready', 'r']:
            clear()
            print('Alright. Lets begun!\n')
            while True:
                try:
                    bet = int(input('How much would you like to bet?\n> '))
                except ValueError:
                    print(Bcolors.WARNING + 'ERROR: invalid bet\n' + Bcolors.ENDC)
                else:
                    play = main_player.pay(bet)
                    if play == 2:
                        win = main_machine.run(bet)
                        main_player.bank += win
                        print('Would you like to play again?')
                        break
                    elif play == 1:
                        print(Bcolors.WARNING + 'ERROR: Not enough money\n' + Bcolors.ENDC)
                    elif play == 0:
                        loan = input('Would you like to take out a loan? \n> ')  # TODO loans
                        if loan in ['yes', 'y']:
                            amount = input('How much would you like to withdraw? \n> ')
                            if amount.isnumeric():
                                amount = int(amount)
                                main_player.bank += amount
                                main_player.debt += amount
                            else:
                                print(Bcolors.WARNING + 'ERROR: invalid input\n' + Bcolors.ENDC)
                        else:
                            print(Bcolors.WARNING + 'ERROR: unknown input\n' + Bcolors.ENDC)

        elif start.lower() == 'q':
            loop = False
        elif start.lower() in ['balance', 'bal', 'b']:
            print(f'Balance: ${main_player.bank}')
        else:
            print(Bcolors.WARNING + 'ERROR: unknown input\n' + Bcolors.ENDC)

    final = main_player.bank - main_player.debt - 1000

    if final < 0:
        print(f'you walk away ${final * -1} in debt :(')
    elif final > 0:
        print(f'You walk away with ${final} in profit!')
    else:
        print('you walk away even!')

    print('\nThanks for playing!\n'
          'I hope to see you again soon.')
    end = input()
