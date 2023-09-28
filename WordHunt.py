from collections import deque
from time import perf_counter
import sys

global wordlist
global prefix
global benchmark
global listing

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class Letter:
	def __init__(self, id_, letter):
		self.id = id_
		self.letter = letter
		self.neighbors = set()

	def addNeighbor(self, neighbor):
		self.neighbors.add(neighbor)

class Node:
	def __init__(self, id_, parents, depth):
		self.id = id_
		self.parents = parents
		self.depth = depth

	def getWord(self, graph):
		return "".join([graph.letterMap[parent].letter for parent in self.parents]) + graph.letterMap[self.id].letter

class Graph:
	def __init__(self):
		self.letterMap = dict()
		self.letters = []
		for i in range(self.size ** 2):
			letter = Letter(i, "")
			self.letters.append(letter)
			self.letterMap[i] = letter

	def addPuzzle(self, letters):
		for i, letter in enumerate(self.letters):
			letter.letter = letters[i]

	def findWords(self, length):
		global wordlist
		global prefix
		global benchmark
		global listing

		final_words = set()
		fringe = deque([Node(i, [], 1) for i in range(self.size ** 2)])

		while fringe:
			node = fringe.popleft()
			word = node.getWord(self)
			if len(word) > 1 and node.depth < length and word not in prefix:
				continue
			if node.depth >= length:
				if word not in final_words and word in wordlist:
					if not benchmark and not listing:
						print("----------------------------------------------------------------")
						print(color.GREEN + word.upper() + color.END)
						for i in range(self.size):
							ids = list(range(i*self.size, i*self.size + self.size))
							ret = ""
							for id_ in ids:
								if id_ == node.parents[0]:
									ret += color.GREEN + self.letters[id_].letter.upper() + color.END + " "
								elif id_ == node.id:
									ret += color.RED + self.letters[id_].letter.upper() + color.END + " "
								elif id_ in node.parents:
									ret += color.YELLOW + self.letters[id_].letter.upper() + color.END + " "
								else:
									ret += self.letters[id_].letter.upper() + " "
							print(ret)
						input()
					final_words.add(word)
				continue
			letter = self.letterMap[node.id]
			neighbors = letter.neighbors
			for neighbor in neighbors:
				if neighbor.id in node.parents:
					continue
				fringe.appendleft(Node(neighbor.id, node.parents + [node.id], node.depth + 1))
		return final_words


class Graph4x4(Graph):
	def __init__(self):
		self.size = 4
		super().__init__()
		for letter in self.letters:
			isLeft = letter.id % 4 == 0
			isTop = letter.id < 4
			isBottom = letter.id >= 12
			isRight = letter.id % 4 == 3
			if isTop and isLeft:
				offsets = [1, 4, 5]
			elif isTop and isRight:
				offsets = [-1, 3, 4]
			elif isLeft and isBottom:
				offsets = [-4, -3, 1]
			elif isRight and isBottom:
				offsets = [-5, -4, -1]
			elif isTop:
				offsets = [-1, 1, 3, 4, 5]
			elif isLeft:
				offsets = [-4, -3, 1, 4, 5]
			elif isRight:
				offsets = [-5, -4, -1, 3, 4]
			elif isBottom:
				offsets = [-5, -4, -3, -1, 1]
			else:
				offsets = [-5, -4, -3, -1, 1, 3, 4, 5]

			for offset in offsets:
				neighbor_id = letter.id + offset
				letter.addNeighbor(self.letterMap[neighbor_id])

class Graph5x5(Graph):
	def __init__(self):
		self.size = 5
		super().__init__()
		for letter in self.letters:
			isLeft = letter.id % 5 == 0
			isTop = letter.id < 5
			isBottom = letter.id >= 20
			isRight = letter.id % 5 == 4
			if isTop and isLeft:
				offsets = [1, 5, 6]
			elif isTop and isRight:
				offsets = [-1, 4, 5]
			elif isLeft and isBottom:
				offsets = [-5, -4, 1]
			elif isRight and isBottom:
				offsets = [-6, -5, -1]
			elif isTop:
				offsets = [-1, 1, 4, 5, 6]
			elif isLeft:
				offsets = [-5, -4, 1, 5, 6]
			elif isRight:
				offsets = [-6, -5, -1, 4, 5]
			elif isBottom:
				offsets = [-6, -5, -4, -1, 1]
			else:
				offsets = [-6, -5, -4, -1, 1, 4, 5, 6]

			for offset in offsets:
				neighbor_id = letter.id + offset
				letter.addNeighbor(self.letterMap[neighbor_id])

def main():
	global wordlist
	global prefix
	global benchmark
	global listing

	benchmark = False
	listing = False

	if len(sys.argv) > 1:
		if "time" in sys.argv[1]:
			benchmark = True
		elif "list" in sys.argv[1]:
			listing = True


	wordlist = set()
	prefix = set()
	with open("dict.txt", "r") as f:
		for line in f:
			word = line.strip().lower()
			if len(word) >= 3:
				wordlist.add(word)
			for p in [word[:i] for i in range(2, len(word))]:
				prefix.add(p)

	puzzle_input = input("Enter puzzle input:").strip().lower()
	# puzzle_input = "qwertyuiopasdfghjklzxcvbn"

	if not puzzle_input.isalpha():
		print("Only alphabetic characters are allowed")
		exit()

	if len(puzzle_input) == 16:
		print("Using 4x4 board")
		graph = Graph4x4()

	elif len(puzzle_input) == 25:
		print("Using 5x5 board")
		graph = Graph5x5()

	else:
		print("Not a valid board size")
		exit()

	graph.addPuzzle(puzzle_input)

	word_count = 0
	t0 = perf_counter()
	results = []

	try:
		for i in reversed(range(3,12)):
			words = graph.findWords(i)
			word_count += len(words)
			if listing:
				for w in words:
					results.append(w)
	except KeyboardInterrupt:
		print('Manually stopped.\n')
		exit()

	if listing:
		print("TOTAL: %d words\n" % len(results))
		score = 0
		for i, w in enumerate(results):
			if len(w) == 3:
				val = 100
			elif len(w) == 4:
				val = 400
			elif len(w) == 5:
				val = 800
			else:
				val = 1400 + (len(w) - 6) * 400
			print("%d.\t%s%s%d" % (i + 1, w, " " * (16 - len(w)), val))
			score += val
		print("Maximum possible score: %d" % score)

	if benchmark:
		t1 = perf_counter()
		print("Took %.3f ms to find %d words for input \n%s" % 
				((t1 - t0) * 1000, word_count, 
					'\n'.join(s.replace("", " ")[1: -1] for s in list(map(''.join, zip(*[iter(puzzle_input.upper())]*graph.size))))))

if __name__ == '__main__':
	main()
