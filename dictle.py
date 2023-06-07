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
    ret = sys.stdin.readline()
    assert(ret[-1] == "\n")
    return ret[:-1]

# TODO - doesn't work for German or Turkish
def okay(word: str, length: int) -> bool:
    return len(word) == length and word.islower() and word.isalpha()

def run_one_dictle(word: str, length: int, words_set: set[str]) -> None:
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
            return
        elif not okay(line, length):
            p(Fore.RED, f"\"{line}\" contains invalid characters")
            continue
        elif line not in words_set:
            p(Fore.RED, f"\"{line}\" is not in the dictionary")
            continue

        # Conduct two passes so that we flag the right number of missing
        # letters.
        missing: list[str] = []
        z = list(zip(list(word), list(line))) # zip results drain
        for wl, ll in z:
            if ll != wl:
                missing += wl

        for wl, ll in z:
            if wl == ll:
                w(Back.GREEN, ll)
            elif ll in missing:
                missing.remove(ll)
                # yellow typically is tinted toward orange
                w(Back.YELLOW, ll)
            else:
                sys.stdout.write(ll)
        print()
    return

if __name__ == "__main__":
    p(Fore.LIGHTBLUE_EX, "Welcome to dictle!")
    dpath = get_in("What dictionary are we using? [/usr/share/dict/words]: ")
    if len(dpath) == 0:
        dpath = "/usr/share/dict/words"
    if not os.path.exists(dpath):
        print(f"{dpath} not found; giving up")
        exit(1)

    with open(dpath, "r") as f:
        words = f.read().split("\n")

    length_raw = get_in("What length words would you like? [5]: ")
    if length_raw == "":
        length_raw = "5"
    length = int(length_raw)
    assert(length > 0)

    words = [word for word in words if okay(word, length)]
    random.shuffle(words)

    words_set = set(words) # keep a copy of the wordlist around
    while True:
        word = words.pop()
        p(Fore.LIGHTBLUE_EX, "Word selected.  Guess away!")
        run_one_dictle(word, length, words_set)
