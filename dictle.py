#!/usr/bin/python3
# SPDX-Identifier: AGPL-3.0-only

import os
import random
import sys

from colorama import Fore, Back

def p(c: str, text: str) -> None:
    return print(f"{c}{text}{Fore.RESET}")

def w(c: str, text: str) -> int:
    return sys.stdout.write(f"{c}{text}{Back.RESET}")

def get_in(prompt: str) -> str:
    sys.stdout.write(prompt)
    sys.stdout.flush()
    return sys.stdin.readline()

# TODO - doesn't work for German or Turkish
def okay(word: str, length: int) -> bool:
    return len(word) == length and word.islower()

p(Fore.LIGHTBLUE_EX, "Welcome to dictle!")
dictionary = get_in("What dictionary are we using? [/usr/share/dict/words]: ")
assert(dictionary[-1] == "\n")
dictionary = dictionary[:-1]
if len(dictionary) == 0:
    dictionary = "/usr/share/dict/words"
if not os.path.exists(dictionary):
    print(f"{dictionary} not found; giving up")
    exit(1)

with open(dictionary, "r") as f:
    words = f.read().split("\n")

length = int(get_in("What length words would you like? [5]: "))
assert(length > 0)

words = [word for word in words if okay(word, length)]
random.shuffle(words)

words_set = set(words) # keep a copy of the wordlist around
word = words.pop()
p(Fore.LIGHTBLUE_EX, "Word selected.  Guess away!")

while True:
    line = sys.stdin.readline()
    assert(line[-1] == "\n")
    line = line[:-1]

    # clear the entry
    sys.stdout.write("\033[F\033[K")
    sys.stdout.flush()
    
    if len(line) != length:
        p(Fore.RED, "Wrong length - try again")
        continue
    elif line == word:
        p(Fore.LIGHTGREEN_EX, word)
        p(Fore.LIGHTBLUE_EX, "Congratulations - you win!")
        exit(0)
    elif line not in words_set:
        p(Fore.RED, f"\"{line}\" is not in the dictionary")
        continue

    word_letters = set(word)
    for i, letter in enumerate(list(line)):
        if word[i] == letter:
            w(Back.GREEN, letter)
        elif letter in word_letters:
            # yellow typically is tinted toward orange
            w(Back.YELLOW, letter)
        else:
            sys.stdout.write(letter)
    print()
