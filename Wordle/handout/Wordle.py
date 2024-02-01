# The puzzle game 'Wordle'!
 
# Basic idea:
# the game loads in a set of 'known words' from a file or an array.
# All 'known words' must have the same length (e.g., 5 characters)

# When the game starts, a secret word is chosen from the list of known words.
# The player can then issue guesses.
# Each guess returns a Hint object instance that tells:
# - which characters in the guess are correct, and correctly located.
# - which characters in the guess are in the secret word, but not at the location guessed
# - which characters in the guess are not in the secret word

# If all characters in the guess are correctly located, the game is won ;)

import random
from Hint import Hint
class Wordle(object):
    """docstring for Wordle"""
    def __init__(self, file=None, wordList=[], length=0, minFreq=-1, maxFreq=-1):
       pass

    def numberOfKnownWords(self):
       pass


    # _Part 2: Implement this method._

    # Load words from a file. Each line of the file contains a word followed by one or more spaces followed
    # by a number whose value is higher for words that are more 'frequently occurring' than others.
    # Loaded words should have a frequency value in the range [minfreq, maxfreq]. However, at times, these
    # limits should be ignored (see comments below). Note that the words in the file may be many lengths
    # (e.g., 3-10 characters). Only words of the specified length should be loaded.

    # Hint: Here are directions for file reading in Python using the "with open(file, 'r') as inputFile" syntax:

    #     Use the "with open(file, 'r') as inputFile" statement to open the file in read mode. Replace "file" with the actual file path.
    #     Iterate over the file object "inputFile" using a for loop to process each line.
    #     Within the loop, extract the word and frequency value from each line. You can use string manipulation methods like "split()" to separate them.
    #     Apply any necessary filters to consider only words of the specified length.
    #     Words of the specified length should be added into the knownWords list if their frequencies are the in the range specified.
    #     The file will be automatically closed when the with block is exited, so you don't need to explicitly close the file.

    # Remember to adapt the directions based on your specific requirements and programming context.

    # Hint: somewhere around 10-20 lines is probably appropriate here unless you have a lot of comments

    # @param filenm  - the file name to load from
    # @param length  - the length of words we want to load (e.g., 5 to load 5 character words)
    # @param minfreq - the minimum allowable frequency for a loaded word
    # @param maxfreq - the maximum allowable frequenct for a loaded word; 0 indicates no maximum
    def loadWords(self, file, length, minFreq, maxFreq):
        '''This function loads the words into the game'''
        with open(file, 'r') as inputFile:
            for line in inputFile:
                word, freq = line.split()
            if freq >= minFreq and freq <= maxFreq:
                if len(word) == length:
                    self.knownWords.append(word)
    


    # _Part 3: Implement this method._

    # Obtain a list of known words. This method creates a new copy of the known words list.
    # Here, you simply need to copy the knownWords list and return that copy.

    # @return a new copy of list of known words.
    def getKnownWords(self):
        pass

    
    # Prepare the game for playing by choosing a new secret word.
    def initGame(self):
       pass


    # Supply a guess and get a hint!

    # Note that this implementation DOES NOT require that the guess be selected
    # from the known words. Rather, this implementation allows one to guess arbitrary
    # characters, so long as the guess is the same length as the secret word.

    # @param g - the guess (a string which is the same length as the secret word)
    # @return a hint indicating the letters guessed correctly/incorrectly
    # @returns None if the guess is not the same length as the secret word

    def guess(self, g):
        pass



