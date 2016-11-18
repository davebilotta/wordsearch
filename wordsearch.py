"""
   Simple app to Generate word search puzzles
"""

import sys
from random import randint


words = []
additional_words = []
BOARD_WIDTH = 25
BOARD_HEIGHT = 25
board = []
output_file = "word_search.txt"
max_word_count = 30
max_word_length = 20

filler_words = ["Bread","Bagel","Blueberry","Pizza","Bread","Broccoli","Chicken","Steak","Potato","Pasta",
"Apple","Banana","Raspberry","Strawberry","Cereal","Pretzel","Fish","Bread","Beans","Cheese",
"Water","Milk","Selter","Juice","Pizza",
"Nose","Arm","Leg","Foot","Brain","Stomach","Throat","Neck","Butt","Knee",
"Pencil","House","Chair","Table","Flower","Tree","Television",
"Mother","Father","Brother","Sister","Friend","Aunt","Uncle","Grandmother","Grandfather",
"Teacher","Librarian","Doctor","Veterinarian","Policeman","Fireman","Chef","Dancer","Baker",
"Book","Library","Class","Computer","Tablet","Potty","Playground","Swingset","Couch","Chair",
"Monkey","Gorilla","Dog","Cat","Zebra","Horse","Rhinoceros","Hippopotamus","Snake","Duck","Goose","Sheep"]

def scrubInput(string):
	# Scrub user-entered word

	s = ""

	# TODO: Enforce a max word length?

	for letter in string:
		o = ord(letter.upper()) - 64
		if (o > 0 and o < 27):
			s += letter

	return s.upper()

def randomLayout():
	# Determines if word is Horizontal or Vertical

	# Diagonal coming soon
	#return randint(0,2)

	return randint(0,1)

def randomDirection():
	# Gets a random direction (1 = left-to-right/up-to-down, -1 = right-to-left/down-to-up
	return 1 if randint(0,1) == 0 else -1

def randomRow():
	# Gets a random row on the board

	return randint(0,BOARD_HEIGHT-1)

def randomCol():
	# Gets a random column on the board

	return randint(0,BOARD_WIDTH-1)

def randomFillerWord():
	# Picks a word at random for additional words list

	return filler_words[randint(0,len(filler_words)-1)]

def randomLetter():
	# Returns a random letter

	return chr(65+randint(0,25))

def generateWordsAddl():
	# Now generate any additional words, if any, up to max to fill board

	num_additional_words = max_word_count - len(words)
	print "Will generate " + str(num_additional_words) + " additional"

	for i in range(0,num_additional_words):
		generate = True

		while generate:
			word = randomFillerWord().upper()
			if word not in additional_words and word not in words:
				print "Adding word " + str(word)
				generate = False
				additional_words.append(word.upper())

def insertWords():
	# Inserts words into board

	# Combine original words plus additional
	words.extend(additional_words)

	# Now place them in the board - max tries limited to 10 to avoid Infinite Loop

	# TODO - remove from list if can't be added so it's not printed in list of words to find
	max_try_count = 10

	for word in words:
		count = 0
		needs_placing = True

		while needs_placing and count < max_try_count:
			row = randomRow()
			col = randomCol()
			word_layout = randomLayout()
			direction = randomDirection()
			count += 1

			if canFit(word,row,col,word_layout,direction):
				needs_placing = False
				placeWord(word,row,col,word_layout,direction)

def placeWord(word,row,col,layout,direction):
	# Place word on board - at this point it has already been determined if word can fit

	length = len(word)

	i = 0

	# Horizontal
	if layout == 0:
		for letter in word:
			board[row][col+i] = letter
			i += direction

	# Vertical
	elif layout == 1:
		for letter in word:
			board[row+i][col] = letter
			i += direction
	# Diagonal (not done yet)
	else:
		return True

def fillBoard():
	# Fill any "" spaces in board with random letters

	for row in range(0,BOARD_HEIGHT):
		line = []
		for col in range(0,BOARD_WIDTH):
			#
			if board[row][col] == "":
				board[row][col] = randomLetter()

def outputBoard():
	# Output board to file

	f = open(output_file,'w')

	f.write("WORD SEARCH\n\n")
	f.write("*" * BOARD_WIDTH * 2 + "\n")

	for line in board:
		for letter in line:
			if letter == "":
				letter = " "
			f.write(letter + " ")
		f.write("\n")

	f.write("*" * BOARD_WIDTH * 2 + "\n")
	f.write("Find these words:\n")
	for word in words:
		f.write(" " * 5 + word.ljust(max_word_length) + "\n")

	for word in additional_words:
		f.write(" " * 5 + word.ljust(max_word_length) + "\n")

	f.close()

def addWord(s):
	# Scrub word and add to list of words

	word = scrubInput(s)
	if word not in words:
		words.append(word)

def canFit(word,row,col,layout,direction):
	# Determines if a word can fit 1) size-wise and 2) if all spaces are unoccupied

	if not fitsBySize(word,row,col,layout,direction):
		return False
	if not fitsUnoccupied(word,row,col,layout,direction):
		return False
	else:
		return True

def fitsBySize(word,row,col,layout,direction):
	# Determines if a word fits into the board based on the current position

	length = len(word)

	# Horizontal
	if layout == 0:
		if direction == 1:
			return col + (length - 1) < BOARD_WIDTH
		else:
			return col - (length - 1) > 0

	# Vertical
	elif layout == 1:
		if direction == 1:
			return row + (length - 1) < BOARD_HEIGHT
		else:
			return row - (length - 1) > 0

	# Diagonal TODO: for now just return False
	else:
		return False

def fitsUnoccupied(word,row,col,layout,direction):
	# Determines if all spaces where word is going to go are unoccupied

	fits = True
	i = 0

	if layout == 0:
		for letter in word:
			if not board[row][col+i] == "":
				fits = False
				break
			i += direction


	# Vertical
	elif layout == 1:
		for letter in word:
			if not board[row+i][col] == "":
				fits = False
				break
			i += direction

	# Diagonal - TODO:
	else:
		fits = False

	return fits

def initBoard():
	# Initialize board

	for row in range(0,BOARD_HEIGHT):
		line = []
		for col in range(0,BOARD_WIDTH):
			line.append("")

		board.append(line)

def main():

	initBoard()

	done = False
	while True:
		s = raw_input("Type word (Up to " + str(max_word_count) + " max, <Enter> to quit): ")

		if not s == "":
			addWord(s)

		if (s == "" or len(words) >= max_word_count):
			done = True
			generateWordsAddl()
			insertWords()
			fillBoard()
			outputBoard()
			break

		if done:
			break


if __name__ == '__main__': main()
