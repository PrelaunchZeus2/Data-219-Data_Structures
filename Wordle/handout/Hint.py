# _Part 4: Implement this Constructor._
     
# Given a guess and the secret word, provide a hint.

# The Hint should follow these guidelines:
# - the Hint should not store any knowledge of the secret word itself.
# - correctlyPlaced should have a length equal to the length of the secret word
# - incorrectlyPlaced should have a length equal to the length of the secret word
# - notInPuzzle should have a length less than or equal to the length of the secret word/guess.

# A character in the guess that is both the correct letter, and in the correct location in the word
# will appear in that location in the correctlyPlaced String. Characters in the guess that are not
# correctly placed will appear as the char '-' in the correctlyPlaced String.

# Thus, for a guess "skate" and a secret word "score", the correctlyPlaced will be: "s---e"

# A character in the guess that is the correct letter, but not in the correct location in the word
# will appear in the same location as the guess when placed in the incorrectedPlaced String.
# Note that duplicate characters are a bit tricky, they must be examined for correctly placed characters
# before incorrectly placed ones.

# Thus, for a guess "scoop" and a secret word "poofs", the correctlyPlaced String is: "--o--" and
# incorrectlyPlaced String is: "s--op"
# Note that the first 'o' is correctly placed, thus it must be the second 'o' that is incorrectly placed.
# It is incorrect to say that the first 'o' is incorrectly placed, as it is incorrect to say that
# both 'o's are incorrectly placed.

# Characters that are in the guess and are neither correctly placed nor incorrectly placed should be
# added to the notInPuzzle String.  Thus, the length of the notInPuzzle String will never be greater
# than the length of the secret word, or the guess.

# @param guess
# @param secretWord


class Hint(object):
	"""docstring for Hint"""
	def __init__(self, guess, secretWord):
		pass
		

	def isWin(self):
		if self.guess == self.secretWord:
			gameWon = True
		else:
			gameWon = False
		return gameWon

	# Display a hint

	# Given a secret word: 'state', and a guess 'scope' display:

	# ---- Hint (scope) ----
	# Correctly placed  : s---e
	# Incorrectly placed: -----
	# Not in the puzzle : [cop]

	# Given a secret word: 'state', and a guess 'state' display:

	# ---- Hint (scope) ----
	# Correctly placed  : st--e
	# Incorrectly placed: --ta-
	# Not in the puzzle : []
 
	def generateHint(self):
		
		pass
 
	def __repr__(self):
		pass




