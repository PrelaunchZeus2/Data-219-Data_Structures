import csplot
import time
from time import sleep
import sys
import random

class Life():

	def __init__(self, fileName):
		pass
		
	def __repr__(self):
		pass


def main():

    life(10, 10)
    
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

def update1( B ):
	'''Takes an empty board as input and modiifis that board so that it has
	a diagonal strip of "on" cells.
	'''
	
	width = len(B[0])
	height = len(B)
	
	for row in range(height):
		for col in range(width):
			if row == col:
				B[row][col] = 1
			else:
				B[row][col] = 0

def update2( B ):
    '''Takes a board as input and modifies the board so that all cells are live except the one cell wide boarder
    '''
    width = len(B[0])
    height = len(B)
    
    for row in range(height):
        for col in range(width):
            if row == 0 or row == height - 1 or col == 0 or col == width - 1: #if the cell is on the boarder
                B[row][col] = 0
            else: #cell is not on the boarder
                B[row][col] = 1

def updateRandom ( B ):
	'''Takes a board as input and modifies the board so that there is a 1 cell wide boarder of dead cells and the other cells are randomly set to being alive or dead.
	'''
	width = len(B[0])
	height = len(B)
	
	for row in range(height):
		for col in range(width):
			if row == 0 or row == height - 1 or col == 0 or col == width - 1: #if the cell is on the boarder
				B[row][col] = 0
			else: #cell is not on the boarder
				B[row][col] = random.choice([0,1])

def updateReversed (oldB, newB):
	'''Takes an old board and creates a new board where all of the cells of the old board are in the opposite state in the new board. except the outer edge which always
	stays off'''
	width = len(oldB[0])
	height = len(oldB)
	

	for row in range(height):
		for col in range(width):
			if row == 0 or row == height - 1 or col == 0 or col == width - 1: #if cell is on the boarder set it to dead
				newB[row][col] = 0
			else: #cell is not on the boarder so it needs to be swapped
				if oldB[row][col] == 0:
					newB[row][col] = 1
				else: 
					newB[row][col] = 0


def countNeighbors(row, col, B):
	'''Takes in a row colunm pair and a board then counts the number of live cells in the 8 cells surrounding the given cell'''
	alive_neighbor_count = 0
	for i in range(-1, 1): #row
		for j in range(-1, 1): #col
			if B[row + i][col + j] == 1:
				alive_neighbor_count = alive_neighbor_count + 1
	return alive_neighbor_count


def updateNextLife(oldB, newB):
	'''This function creates a new board based on the rules of Conway's Game of Life
	1. a cell that has fewer than 2 live neighbors dies
	2. a cell that has more than 3 live neighbors dies
	3. a dead cell with 3 live neighbors comes to life
	4. all other cells maintain their state'''

	width = len(oldB[0])
	height = len(oldB)

	for row in range(height):
		for col in range(width):
			neighbor_count = countNeighbors(row, col, oldB)
			if row == 0 or row == height - 1 or col == 0 or col == width - 1: #cell is on border
				newB[row][col] = 0 #set to dead
			elif neighbor_count <  2 or neighbor_count > 3: #to many or too few neighbors
				newB[row][col] = 0 #set to dead
			elif neighbor_count == 3 and oldB[row][col] == 0: #dead cell with 3 neighbors
				newB[row][col] = 1
			else: #everything else
				newB[row][col] = oldB[row][col]
	return newB


def life (width, height):
	'''will become John Conway's Game of Life'''
	B = createBoard(width, height)
	csplot.showAndClickInIdle(B)
	
	while True:
		csplot.show(B)
		time.sleep(0.25)
		oldB = B
		B = createBoard(width, height)
		B = updateNextLife(oldB, B)
  
def life2 (width, height):
    '''debug with random board'''
    B = createBoard(width, height)
    updateRandom(B)
    
    while True:
        csplot.show(B)
        time.sleep(0.5)
        oldB = B
        B = createBoard(width, height)
        B = updateNextLife(oldB, B)
		
        
            

if __name__ == '__main__':
	main()
