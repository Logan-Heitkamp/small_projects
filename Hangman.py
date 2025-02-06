import random

# Starting message
print("Welcome to Hangman in Python!\n")


# main function to run the game
def game():
    # creating variables
    lives = 7
    guesses = []
    playing = True

    # list of available words
    word_list = ["apple", "orange", "blue", "computer", "python", "keyboard", "table", "cup", "water"]

    # chooses word from word_list
    answer = random.choice(word_list)

    # returns the letters and dashes that will be displayed
    def get_word_progress():
        ret = ""
        for letter in answer:
            if letter in guesses:
                ret += "{} ".format(letter)
            else:
                ret += "_ "
        if "_" not in ret or not playing:
            ret = ("Congrats! you have won!\n"
                   "The correct answer was : {}".format(answer))
        return ret

    # returns the current game board
    def print_man():
        if lives == 7:
            print("     |=======|\n"
                  "     |       |\n"
                  "             |\n"
                  "             |\n"
                  "             |\n"
                  "             |\n"
                  "          ___|___\n\n"
                  "{}\n"
                  "7 lives remaining!".format(get_word_progress()))
        elif lives == 6:
            print("     |=======|\n"
                  "     |       |\n"
                  "     O       |\n"
                  "             |\n"
                  "             |\n"
                  "             |\n"
                  "          ___|___\n\n"
                  "{}\n"
                  "6 lives remaining!".format(get_word_progress()))
        elif lives == 5:
            print("     |=======|\n"
                  "     |       |\n"
                  "     O       |\n"
                  "     |       |\n"
                  "             |\n"
                  "             |\n"
                  "          ___|___\n\n"
                  "{}\n"
                  "5 lives remaining!".format(get_word_progress()))
        elif lives == 4:
            print("     |=======|\n"
                  "     |       |\n"
                  "     O       |\n"
                  "     |       |\n"
                  "     |       |\n"
                  "             |\n"
                  "          ___|___\n\n"
                  "{}\n"
                  "4 lives remaining!".format(get_word_progress()))
        elif lives == 3:
            print("     |=======|\n"
                  "     |       |\n"
                  "     O       |\n"
                  "     |/      |\n"
                  "     |       |\n"
                  "             |\n"
                  "          ___|___\n\n"
                  "{}\n"
                  "3 lives remaining!".format(get_word_progress()))
        elif lives == 2:
            print("     |=======|\n"
                  "     |       |\n"
                  "     O       |\n"
                  "    \|/      |\n"
                  "     |       |\n"
                  "             |\n"
                  "          ___|___\n\n"
                  "{}\n"
                  "2 lives remaining!".format(get_word_progress()))
        elif lives == 1:
            print("     |=======|\n"
                  "     |       |\n"
                  "     O       |\n"
                  "    \|/      |\n"
                  "     |       |\n"
                  "    /        |\n"
                  "          ___|___\n\n"
                  "{}\n"
                  "Only 1 life left!".format(get_word_progress()))
        elif lives == 0:
            print("     |=======|\n"
                  "     |       |\n"
                  "     O       |\n"
                  "    \|/      |\n"
                  "     |       |\n"
                  "    / \      |\n"
                  "          ___|___\n\n"
                  "{}\n"
                  "GAME OVER! \nBetter luck next time! :P\n\n"
                  "Correct answer: {}".format(get_word_progress(), answer))

    # returns False if game is finished
    def check_finished():
        letter_check = True
        for letter in answer:
            if letter not in guesses:
                letter_check = False

        if lives == 0:
            return False
        elif letter_check:
            return False
        else:
            return True

    # loops through the game
    while check_finished() and playing:
        # Displays current game board
        print_man()
        print()

        # user chooses to guess letter or word
        option = input("Would you like to guess a letter \"l\" or word \"w\"?")
        if option in ["w", "l"]:
            while playing:
                if option.casefold() == "l":
                    guess = input("Please enter a letter\n").casefold()
                    # checks for one letter
                    if guess.isalpha() and len(guess) == 1:
                        # checks if you have already guessed the letter
                        if guess not in guesses:
                            guesses += [guess]
                            if guess in answer:
                                print("Correct!\n")
                                break
                            else:
                                lives -= 1
                                print("Incorrect! there goes a life!\n")
                                break
                        else:
                            print("You have already guessed that.")
                            break
                    else:
                        print("please enter a valid character.")
                        break
                elif option.casefold() == "w":
                    guess = input("Please enter a word")
                    if guess.isalpha():
                        if guess == answer:
                            print("Correct! You have won!\n\nThe answer was : {}".format(answer))
                            playing = False
                            break
                        else:
                            print("Incorrect! there goes a life!")
                            lives -= 1
                            break
                    else:
                        print("Please enter a valid word")
                        break
        else:
            print("Please enter a valid option")
    print_man()


game()
