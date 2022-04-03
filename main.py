import numpy as np
import time
import difflib
import os
import sys
from nltk.corpus import words
allWords = words.words()

def deleteLastLine():
    "Use this function to delete the last line in the STDOUT"

    #cursor up one line
    sys.stdout.write('\x1b[1A')

    #delete last line
    sys.stdout.write('\x1b[2K')


# generate random words from vowels and consonants alternating
def generateRandomWord(minLength, maxLength, vowels, consonants, punctuations, newKey=None):
    # generate random length of word
    length = np.random.randint(minLength, maxLength+1)
    
    if newKey and not newKey.isPunctuation:
        # generate random word with focus on new key

        word = ""

        for i in range(length):
            rng = np.random.rand()

            if newKey.isVowel:

                if i % 3 == 0:
                    word += newKey.key if rng < 0.3 else np.random.choice(vowels)
                else:
                    word += np.random.choice(consonants)

            else:
                if i % 3 == 0:
                    word += np.random.choice(vowels)
                else:
                    word += newKey.key if rng < 0.3 else np.random.choice(consonants)



    else:
    
        word = ''.join(
            np.random.choice(vowels)
            if i % 3 == 0
            else np.random.choice(consonants)
            for i in range(length)
        )

    # if word in allWords or np.random.rand() < 0.1:

    if len(punctuations) > 0 and np.random.rand() < 0.2:
        word = word + np.random.choice(punctuations)


    if np.random.rand() < 0.2:
        word = word.capitalize()
        
    return word



def generateRandomSentence(length, keys, newKey=None):
    # generate random length of sentence

    vowels = []
    consonants = []
    punctuations = []

    
    for key in keys:
        if key.isPunctuation == 1:
            punctuations.append(key.key)
        elif key.isVowel == 1:
            vowels.append(key.key)
        elif key.isConsonant == 1:
            consonants.append(key.key)

    return ' '.join(
        generateRandomWord(3, 6, vowels, consonants, punctuations, newKey)
        for _ in range(length)
    )


class key:
    def __init__(self, key: str, isVowel: bool, isPunctuation=False, isCapital=False):
        self.key = key
        self.isVowel = isVowel
        self.isConsonant = not isVowel
        self.isPunctuation = isPunctuation
        self.isCapital = isCapital
        self.performance = 0


    # add function to print all attributes of object
    def __str__(self):
        return f"{self.key=} {self.isVowel=} {self.isConsonant=} {self.isCapital=} {self.isPunctuation=} {self.performance=}"


def main():


    # create a list of key objects for all english letters
    allKeys = np.array([
        key(letter, bool(int(isVowel)), bool(int(isPunctuation)))
        for letter, isVowel, isPunctuation in zip(
            "abcdefghijklmnopqrstuvwxyz,.-", "10001000100000100000100000000", "00000000000000000000000000111")
    ])



    myKeys = np.array([ 
        key(letter, bool(int(isVowel)))
        for letter, isVowel in zip(
            "asdfjkl", "1000000")
    ])


    toAddKeys = np.array([
        key(letter, bool(int(isVowel)), bool(int(isPunctuation)))
        for letter, isVowel, isPunctuation in zip(
            "urieowztpqhgnbmkv,c.x-y", "10001000100000100000100000", "00000000000000000000101010")
    ])


    newKey = None

    # parameters
    charsPerS = 3.  # characters per second
    wordsPerTest = 15  # words per test
    allowedErrorRate = 0.2  # allowed errors per word


    for i in range(100):

        test = generateRandomSentence(wordsPerTest, myKeys, newKey)

        startTest = input(f"\n\n Run {i}: Press enter to start test")
        deleteLastLine

        print(test)
        t0 = time.time()

        typed = input()
        t1 = round(time.time() - t0, 2)

        errorList = [li for li in difflib.ndiff(test, typed) if li[0] != ' ']
        errors = len(errorList)

        if test == typed and t1 < len(test)/charsPerS and errors <= allowedErrorRate*wordsPerTest:
        # if True:
            print(f"Correct!\nTime: {t1}s\nErrors: {errors}\nChars per s: {len(test)/t1:.2f}")

            myKeys = np.append(myKeys, toAddKeys[0])
            toAddKeys = np.delete(toAddKeys, 0)

            newKey = myKeys[-1]
            print(f"Added key: {newKey.key}")


        elif test == typed and t1 > len(test)/charsPerS and errors <= allowedErrorRate*wordsPerTest:
            print(f"Correct but too slow!\nTime: {t1}s\nErrors: {errors}\nChars per s: {len(test)/t1:.2f}")

        else:
            print(f"Too many errors!\nTime: {t1}s\nErrors: {errors}\nChars per s: {len(test)/t1:.2f}")

if __name__ == '__main__':
    main()


# TODO
# - adjust setting for capitalization
# - make real words more likely
# - add performance measure
# - add database
# - add GUI / website
# - support multiple layouts / languages