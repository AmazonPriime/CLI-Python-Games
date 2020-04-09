import os

print('Welcome to Python Hangman 1.0!')

word = input('Please enter the word that others will guess: ').lower()

words = list(word)
blank_word = "_ " * len(words)
blank_word = blank_word.split()
hanging = {0 : "|----|\n|\n|\n|\n|\n{}",
           1 : "|----|\n|    o\n|\n|\n|\n{}",
           2 : "|----|\n|    o\n|    |\n|\n|\n{}",
           3 : "|----|\n|    o\n|   /|\n|\n|\n{}",
           4 : "|----|\n|    o\n|   /|\\\n|\n|\n{}",
           5 : "|----|\n|    o\n|   /|\\\n|   /\n|\n{}",
           6 : "|----|\n|    o\n|   /|\\\n|   / \\\n|\n{}"}

letters, playing, turns, hang_counter = [], True, 0, 0
clear = lambda: os.system('clear')

clear()

while playing:
    letter = input("Letter: ").lower()

    if letter in letters:
        clear()
        print('Already used {}.'.format(letter))
    elif len(letter) > 1:
        clear()
        print('Please, just one character..')
    elif letter in words:
        turns += 1
        for i, l in enumerate(words):
            if l == letter:
                blank_word[word.index(letter, i)] = letter
                words.remove(letter)
        letters.append(letter)
        clear()
    else:
        letters.append(letter)
        turns += 1
        hang_counter += 1
        clear()

    print(hanging[hang_counter].format(" ".join(blank_word)))
    print("Letters used: %s" % ", ".join(map(str, letters)))

    if len(words) == 0:
        print("Word has been guessed in {} turns.".format(turns))
        playing = False
    elif hang_counter == 6:
        print("Game over.. The word was {}. Better luck next time!".format(word))
        playing = False
