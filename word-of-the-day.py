import random
import re
import requests


def getwotd():
    url = 'https://www.merriam-webster.com/word-of-the-day'
    mwpage = requests.get(url)
    page = str(mwpage.content)
    string = r'<title>Word of the Day: \S+ '
    match = re.search(string, page)
    return [match.group().split()[-1].lower()]


def getmorewotd():
    url = 'https://www.merriam-webster.com/wotd/feed/rss2'
    mwpage = requests.get(url)
    page = str(mwpage.content)
    string = r'<title><!\[CDATA\[\S+\]'
    match = re.findall(string, page)
    for i, string in enumerate(match):
        # split by / to iselect for the final part of the url with the wotd and
        # date, then select the last item in the resulting list (minus two
        # characters to remove the closing square brackets, then split by
        # hyphens only once to separate wotd from the date)
        match[i] = string.split('/')[-1][:-2].split('-', 1)[0].lower()
    try:
        match.remove(getwotd()[0])
    except ValueError:
        pass
    return match


def find_all(word, char):
    indices = list()
    wordcopy = word
    n = 0
    while wordcopy.find(char) != -1:
        curr_index = wordcopy.find(char)
        indices.append(curr_index + n)
        wordcopy = wordcopy[:curr_index] + wordcopy[curr_index + 1:]
        n += 1
    return indices


class Game:

    def __init__(self, wordlist):
        self.wordlist = wordlist
        self.word = None
        self.wordguess = ""

    def get_word(self):
        rand = random.Random()
        length = len(self.wordlist)
        self.word = self.wordlist[rand.randrange(0, length)].lower()
        for i in range(len(self.word)):
            if i in find_all(self.word, "-"):
                self.wordguess += "- "
            else:
                self.wordguess += "_ "
        return self.word

    def get_guess(self):
        guess = input("Please enter a missing letter guess:")
        if guess:
            pass
        else:
            return self.get_guess()
        match = re.fullmatch('[a-z]{1}', guess, re.IGNORECASE)
        if match:
            return guess
        else:
            print("Please only enter one letter at a time.")
            return self.get_guess()

    def iscorrectguess(self, guess):
        try:
            lcword = self.word.lower()
        except AttributeError:
            print(f"guess = {guess}")
        lcguess = guess.lower()
        if lcguess in lcword:
            for i in find_all(lcword, lcguess):
                self.wordguess = (self.wordguess[:i*2] + f"{lcguess} "
                                  + self.wordguess[i*2 + 2:])
            return True
        else:
            return False


def playgame(wordlist):
    count = 0
    game = Game(wordlist)
    game.get_word()
    guesses = []
    while "_" in game.wordguess:
        print(f"Guess which letters are missing from: {game.wordguess}")
        guess = game.get_guess()
        while True:
            if guess not in guesses:
                guesses.append(guess)
                break
            else:
                print(f"You have already guessed letter {guess}, please try a"
                      " different letter.")
                guess = game.get_guess()
        if game.iscorrectguess(guess):
            print("Great job, you guessed correctly!")
        else:
            print(f"Sorry, the letter '{guess}' is not part of the word."
                  " Please try again.")
        count += 1
    if count <= int((len(game.word) * 1.7)):
        msg = ("Thanks to your superb language abilities, you managed to "
               f"figure it out in {count} attempts!")
    else:
        msg = f"You managed to figure it out in {count} attempts."
    print(f"\nThat's right, the word was {game.word}!", msg, sep="\n")
    playagain = input("Would you like to play again with another recent Word"
                      " of the Day (Y/N)?")
    if playagain in "Yy":
        playgame(getmorewotd())

if __name__ == "__main__":
    playgame(getwotd())