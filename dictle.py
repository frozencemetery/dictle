#!/usr/bin/python3
# SPDX-Identifier: AGPL-3.0-only

import os
import random
import re
import sys

from colorama import Fore, Back

def p(c: str, text: str) -> None:
    return print(f"{c}{text}{Fore.RESET}")

dictionary = "/usr/share/dict/words"
if not os.path.exists(dictionary):
    print(f"{dictionary} not found; giving up")
    exit(1)

with open(dictionary, "r") as f:
    words = f.read().split("\n")

# TODO - only works for English
okay = re.compile("[a-z]{5}$")
words = [word for word in words if okay.match(word)]
random.shuffle(words)

p(Fore.LIGHTBLUE_EX, "Welcome to dictle!")

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
    
    if len(line) != 5:
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
            sys.stdout.write(f"{Back.GREEN}{letter}{Back.RESET}")
        elif letter in word_letters:
            # yellow typically is tinted toward orange
            sys.stdout.write(f"{Back.YELLOW}{letter}{Back.RESET}")
        else:
            sys.stdout.write(letter)
    print()
