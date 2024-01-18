import csplot
from time import sleep
import sys
import random

class Life():

	def __init__(self, fileName):
		pass
		
	def __repr__(self):
		pass

	
if __name__ == '__main__':
	main()


def createOneRow(n):
	'''Ths Function takes in a number n and returns a list of n length with zeros as the elements.'''
	R = []
	for col in range(n):
		R += [0]
	return R

def createBoard(width, height): #Returns a 2d list of the given dimensions with zeros as the elements.
	'''This function takes in a width and height and returns a 2d list of the given dimensions with zeros as the elements.'''
	A = []
	for row in range(height): #for each row we create a row of thee specified width and add that row to the board.
		A += [createOneRow(width)]
	return A

B = createBoard(10, 10)
csplot.show(B)
csplot.update(B)
csplot.done(B)
