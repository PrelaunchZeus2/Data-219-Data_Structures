from Wordle import Wordle

# This is a main that will run your game once you finish 
# creating the other methods. Use it as a guide for how
# I will interact with your Classes.
class WordleGame(object):
	"""docstring for WordleGame"""
	def __init__(self):
		self.maxGuesses = 10
		self.nGuesses = 0

	#Here are two ways to create the puzzle. Using an array is good for testing
    #using the file is good for playing...
	def startGame(self):
		shortList = ['state']
		#puzzle = Wordle(wordList=shortList)
		puzzle = Wordle(file='norvig200.txt', length=5, minFreq=0, maxFreq=10000000000000000)
		puzzle.initGame()

		
		
		while(self.nGuesses < self.maxGuesses):
			self.nGuesses += 1
			token = input('Your guess: ')
			token = token.lower() #converts the guess to lower case so that case doesn't matter
			print("Got:'"+token+"'")
			h = puzzle.guess(token)
			if h:
				print(h)
				if h.isWin():
					print('You won in',self.nGuesses,'moves!')
					break
			else:
				print('...try again...')
				self.nGuesses += 1 #Don't want to count this one...

		if not h.isWin():
			print('Too many moves! You lose!')

def main():
	myGame = WordleGame()
	myGame.startGame()


if __name__ == '__main__':
	main()