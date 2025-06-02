import math

class Calculator(object):
	"""docstring for Calculator"""
	# _Part 1: Implement this constructor_

	# Create a new Calculator with maxSize slots in the stack
	# @param maxSize - number of spaces in the stack
	def __init__(self, maxSize):
		self.maxSize = maxSize
		self.stack = []
		self.x = self.y = self.z = 0

	# _Part 2: Implement this method_

	# Push the specified double onto the stack
	# @param d - the value to push
	# Return False if the stack too large
	def push(self, value):
		if len(self.stack) < self.maxSize:
			self.stack.append(value)
		else:
			raise Exception("Stack is full.")
			return False


	# _Part 3: Implement this method_

	# Pop the top value off the stack.
	# Return None if the stack is currently empty.
	def pop(self):
		if len(self.stack) == 0:
			return None
			raise Exception("Stack is empty.")
		else:
			item = self.stack[0]
			del self.stack[0]
			return item

	# _Part 4: Implement this method_

	# Calculate the value from a String of operations.

	# Basic operations:
	# "+" - adds the top two entries on the stack
	# "*" - multiplies the top two entries on the stack
	# "-" - subtracts the top entry in the stack from the 2nd entry in the stack
	# "/" - divides the 2nd entry in the stack by the top entry in the stack
	# "^" - raises the 2nd entry in the stack to the power indicated by the top entry in the stack
	# "lg" - takes the lg (log base 2) of the top entry in the stack

	# Variables
	# expand the use of the calculator by supporting the use of
	# three variables 'x', 'y', and 'z' in expressions. Specifically
	# for each variable, there should be a way to set its value 
	# the tokens 'setx', 'sety', and 'setz' respectively, and a way to 
	# read its value -- the tokens: 'x', 'y', and 'z' respectively.
	# With these new operators we should be able to evaluate
	# expressions such as:
	# "10 4 + setx" (set the 'x' variable to 14)
	# "42 x /"      (divide 42 by the value stored for 'x' -- currently 14)
	# "x x -"       (subtract 14 from 14)

	# @param inputString - the string representing a mathematic expression
	# Return None if a specified operator is unknown.

	def calculate(self, inputString):
		calcTokenList = inputString.split(" ")
		for token in calcTokenList:
			if token.isnumeric():
				self.push(int(token))
			elif token == "x":
				self.push(int(self.x))
			elif token == "y":
				self.push(int(self.y))
			elif token == "z":
				self.push(int(self.z))
			elif token == "+":
				self.push(self.pop() + self.pop())
			elif token == "*":
				self.push(self.pop() * self.pop())
			elif token == "-":
				self.push(self.pop() - self.pop())
			elif token == "/":
				self.push(self.pop() / self.pop())
			elif token == "^":
				self.push(math.pow(self.pop(), self.pop()))
			elif token == "lg":
				self.push(math.log(self.pop(), 2))
			elif token == "setx":
				self.x = self.pop()
			elif token == "sety":
				self.y = self.pop()
			elif token == "setz":
				self.z = self.pop()
			else:
				return None
		return self.pop()
        
          
        	


	def getVariable(self, var):
		pass

#Some sample tests for you to run to make sure your code works.
if __name__ == '__main__':
	c = Calculator(5)
	print(c.calculate("10 4 +"), " should equal 14")
	print(c.calculate("4 2 /"), " should equal 2")
	print(c.calculate("10 4 + 3 * 2 /"), " should equal 21")
	print(c.calculate("16 lg"), " should equal 4")
	print(c.calculate("16 4 -"), " should equal 12")
	print(c.calculate("5 16 4 + -"), " should equal -15")
	print(c.calculate("5 20 -"), " should equal -15")
	print(c.calculate("5"), " should equal 5")
	print(c.calculate("10 4 + 3 * 2 /"), " should equal 21")
	print(c.calculate("10 4 + setx"), " should equal None")
	print(c.calculate("42 x /"), " should equal 3")
	print(c.calculate("x x -"), " should equal 0")





















