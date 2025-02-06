import random


def rand_color():  # returns a random color [red, blue, black]
    num = random.randint(0, 10)
    if num <= 3:
        return "red"
    elif num >= 6:
        return "blue"
    else:
        return "black"


class Slice:

    def __init__(self):
        self.value = random.randint(1, 10000)
        self.color = str(rand_color())

    def get_value(self):
        return self.value

    def get_color(self):
        return self.color


class Spinner:
    def __init__(self):
        self.slices = [Slice() for _ in range(10)]

    def get_slice(self, slnum):
        return self.slices[slnum]

    def spin(self):  # returns a list with [0] = value and [1] = color
        slice_number = random.randint(0, 9)
        return [MainSpinner.get_slice(slice_number).get_value(), MainSpinner.get_slice(slice_number).get_color()]

    def list_all_slices(self):
        ret = ""
        for i in range(0, 10):
            ret += "Slice {}: ${}, {}\n".format(i + 1, self.get_slice(i).get_value(), self.get_slice(i).get_color())
        return ret

    def reroll(self):
        self.slices = [Slice() for _ in range(10)]


def play():
    ret = ""
    score = 0

    s1 = MainSpinner.spin()
    s2 = MainSpinner.spin()
    s3 = MainSpinner.spin()

    ret += "Spin 1: ${}, {}\n".format(s1[0], s1[1])
    ret += "Spin 1: ${}, {}\n".format(s2[0], s2[1])
    ret += "Spin 1: ${}, {}\n".format(s3[0], s3[1])

    score += s1[0] + s2[0] + s3[0]

    if s1[1] == s2[1] == s3[1] == "red":
        score *= 2
        ret += "Triple reds! Score multiplied by 2!\n"

    if s1[1] == s2[1] == s3[1] == "blue":
        score *= 2
        ret += "Triple blues! Score multiplied by 2!\n"

    if s1[1] == s2[1] == s3[1] == "black":
        score *= 10
        ret += "Triple blacks! Score multiplied by 10!\n"

    ret += "Final score: ${}".format(score)

    return ret


MainSpinner = Spinner()  # Main spinner everything runs off of

print("Welcome to Money Wheel!")
input("Press ENTER to start!")

while True:
    option = input("Type \"p\" to play, \"l\" to list all slices, and \"r\" to reroll all slices.")

    if option.casefold() == "p":
        print(play())
    elif option.casefold() == "l":
        print(MainSpinner.list_all_slices())
    elif option.casefold() == "r":
        MainSpinner.reroll()
    else:
        print("Please type a valid option")
